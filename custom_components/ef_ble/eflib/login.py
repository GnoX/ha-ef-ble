"""EcoFlow account login helper - region routing and credential probing."""

import base64
import hashlib
import hmac
import json
import secrets
import string
import time
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

import aiohttp

# HTTP request-signing material for the EcoFlow consumer app (package `com.ecoflow`).
# The `/iot-service/*` endpoints reject unsigned requests: every call carries a `token`
# header (HMAC keyed by the login bearer) and an `X-Sign` header (HMAC keyed by the app
# signing-cert SHA-1 concatenated with a per-package salt returned by the app's native
# `getHttpSalt`). `/auth/login` itself is unsigned, so only device calls sign. The salt
# and cert fingerprint are fixed app-integrity constants, not user credentials.
_APP_VERSION = "6.15.0.111"
_SYS_VERSION = "13"
_PHONE_MODEL = "SM-S911B"  # common Android Build.MODEL, blends with real traffic
_PACKAGE_NAME = "com.ecoflow"
_APP_CERT_SHA1 = "3bc4556d6cefafc678995b517e0df31678da03c2"
_HTTP_SALT = "Ev7f82PUhUTNkLCo"
_X_SIGN_KEY = _APP_CERT_SHA1 + _HTTP_SALT
_NONCE_ALPHABET = string.ascii_letters + string.digits


def _hmac_sha256_hex(message: str, key: str) -> str:
    """Lowercase-hex HMAC-SHA256 of `message` under `key`, matching the app"""
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()


class Region(StrEnum):
    """Selectable EcoFlow API host"""

    AUTO = "auto"
    API = "api"
    API_E = "api-e"
    API_A = "api-a"
    API_J = "api-j"
    API_R = "api-r"
    API_CN = "api-cn"

    @classmethod
    def _missing_(cls, value: object) -> "Region | None":
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        return None

    @property
    def base_url(self) -> str | None:
        """Hostname for this region, or None for `AUTO`"""
        if self is Region.AUTO:
            return None
        return f"{self.value}.ecoflow.com"


@dataclass(frozen=True)
class LoginResult:
    user_id: str | None = None
    token: str | None = None
    base_url: str | None = None
    error: str | None = None


@dataclass(frozen=True)
class DeviceBindInfo:
    """Cloud-issued material to complete a PowerOcean (OMOS) BLE bind"""

    random_code: str | None = None
    user_info_en: str | None = None
    error: str | None = None


def decode_device_token(token: str) -> DeviceBindInfo:
    """
    Decode the base64 bind-token blob from the companion device-token web page

    The blob is base64(JSON) of `{sn, randomCode, userInfoEn}`. Returns a
    `DeviceBindInfo` with the bind material, or with `error` set when it cannot be
    parsed.
    """
    try:
        payload = json.loads(base64.b64decode(token, validate=True))
    except (ValueError, json.JSONDecodeError) as exc:
        return DeviceBindInfo(error=f"invalid device token: {exc}")
    random_code = payload.get("randomCode")
    user_info_en = payload.get("userInfoEn")
    if not random_code or not user_info_en:
        return DeviceBindInfo(error="device token is missing bind material")
    return DeviceBindInfo(random_code=random_code, user_info_en=user_info_en)


class EcoFlowLogin:
    """Resolve an EcoFlow user ID from credentials and a region selection"""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session = session

    @staticmethod
    def is_phone_identifier(identifier: str) -> bool:
        """Return True if identifier looks like an E.164 phone number"""
        digits = identifier.removeprefix("+").replace(" ", "")
        return digits.isdigit() and 6 <= len(digits) <= 15

    async def login(
        self,
        identifier: str,
        password: str,
        region: Region | str,
    ) -> LoginResult:
        """Resolve an EcoFlow user ID for the given identifier/password/region"""
        region = Region(region)
        identifier = identifier.strip()
        is_phone = self.is_phone_identifier(identifier)

        if region is Region.API_CN and not is_phone:
            return LoginResult(error="api-cn requires phone number, not email")

        if region is Region.AUTO:
            region = Region.API_CN if is_phone else Region.API

        assert region.base_url is not None
        return await self._try_login_at(
            region.base_url,
            identifier,
            password,
            is_phone=is_phone and region is Region.API_CN,
        )

    async def _try_login_at(
        self,
        base_url: str,
        identifier: str,
        password: str,
        *,
        is_phone: bool,
    ) -> LoginResult:
        json_payload: dict[str, Any] = {
            "scene": "IOT_APP",
            "appVersion": "1.0.0",
            "password": base64.b64encode(password.encode()).decode(),
            "oauth": {"bundleId": "com.ef.EcoFlow"},
            "userType": "ECOFLOW",
        }
        if is_phone:
            json_payload["phone"] = identifier.removeprefix("+86")
        else:
            json_payload["email"] = identifier

        async with self._session.post(
            url=f"https://{base_url}/auth/login",
            json=json_payload,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        ) as response:
            if not response.ok:
                return LoginResult(
                    error=(
                        f"Login failed with status code {response.status}: "
                        f"{response.reason}"
                    )
                )

            result_json = await response.json()
            if result_json["code"] != "0":
                return LoginResult(error=f"Login failed: '{result_json['message']}'")

            data = result_json["data"]
            return LoginResult(
                user_id=data["user"]["userId"],
                token=data.get("token"),
                base_url=base_url,
            )

    def _signed_headers(
        self, method: str, path: str, sorted_query: str, bearer: str
    ) -> dict[str, str]:
        now_ms = int(time.time() * 1000)
        nonce = secrets.randbelow(900_000) + 100_000

        raw_token = bearer.replace("Bearer", "").strip()
        authorization = f"Bearer {raw_token}"

        token_msg = (
            f"phoneModel={_PHONE_MODEL}&platform=android"
            f"&sysVersion={_SYS_VERSION}&version={_APP_VERSION}"
            f"&nonce={nonce}&timestamp={now_ms}"
        )
        token_sig = _hmac_sha256_hex(token_msg, raw_token)

        x_nonce = "".join(secrets.choice(_NONCE_ALPHABET) for _ in range(8))
        x_sign_msg = f"{method}{path}{sorted_query}null{now_ms}{x_nonce}"
        x_sign = _hmac_sha256_hex(x_sign_msg, _X_SIGN_KEY).upper()

        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "platform": "android",
            "version": _APP_VERSION,
            "sysVersion": _SYS_VERSION,
            "phoneModel": _PHONE_MODEL,
            "lang": "en-us",
            "countryCode": "US",
            "nonce": str(nonce),
            "timestamp": str(now_ms),
            "token": token_sig,
            "Authorization": authorization,
            "Package": _PACKAGE_NAME,
            "X-Timestamp": str(now_ms),
            "X-Nonce": x_nonce,
            "X-Sign": x_sign,
        }

    async def _signed_get(
        self, base_url: str, path: str, sorted_query: str, bearer: str
    ) -> tuple[dict[str, Any] | None, str | None]:
        headers = self._signed_headers("GET", path, sorted_query, bearer)
        url = f"https://{base_url}{path}"
        if sorted_query:
            url = f"{url}?{sorted_query}"

        async with self._session.get(url=url, headers=headers) as response:
            if not response.ok:
                return None, (f"HTTP {response.status}: {response.reason}")
            result_json = await response.json()
            if str(result_json.get("code")) != "0":
                return (
                    None,
                    f"code={result_json.get('code')}: {result_json.get('message')}",
                )
            return result_json, None

    async def verify_session(self, base_url: str, bearer: str) -> str | None:
        """Check the bearer + request signing against a device-independent endpoint"""
        _, error = await self._signed_get(
            base_url,
            "/iot-service/user/security/key",
            "scene=APP_SECURITY_KEY",
            bearer,
        )
        return error

    async def get_device_bind_info(
        self, base_url: str, bearer: str, sn: str
    ) -> DeviceBindInfo:
        """Fetch the cloud bind material for `sn` needed by PowerOcean OMOS auth"""
        result_json, error = await self._signed_get(
            base_url, "/iot-service/user/device/refreshToken", f"sn={sn}", bearer
        )
        if error is not None or result_json is None:
            return DeviceBindInfo(error=error or "empty response")

        data = result_json.get("data") or {}
        return DeviceBindInfo(
            random_code=data.get("randomCode"),
            user_info_en=data.get("userInfoEn"),
        )
