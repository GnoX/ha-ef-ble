from . import shp3


class Device(shp3.Device):
    """
    EcoFlow Smart Gateway (200A)

    Speaks the Smart Home Panel 3 protocol - identical `cmd_set`/`cmd_id` and the same
    `DisplayPropertyUpload` message - but reports from a different module address, so only
    `MAIN_SRC` and the identifying prefixes differ. Verified against a capture from a
    200 A unit on firmware 7.0.1.95: eight load channels with per-circuit power, voltage
    and current, split-phase L1/L2, PV total, grid state and operating mode all populate
    from the inherited fields.
    """

    SN_PREFIX = (b"HR65",)
    NAME_PREFIX = "EF-GW"

    MAIN_SRC = 0x34
