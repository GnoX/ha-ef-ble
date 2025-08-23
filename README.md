# EcoFlow BLE

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![Validation hassfest](https://github.com/rabits/ha-ef-ble/actions/workflows/validate-hassfest.yaml/badge.svg)](https://github.com/rabits/ha-ef-ble/actions/workflows/validate-hassfest.yaml)
[![Validation HACS](https://github.com/rabits/ha-ef-ble/actions/workflows/validate-hacs.yaml/badge.svg)](https://github.com/rabits/ha-ef-ble/actions/workflows/validate-hacs.yaml)

Unofficial EcoFlow BLE devices Home Assistant integration will allow you to communicate with a
number of EcoFlow devices through bluetooth and monitor their status / control parameters.

Recognized devices:
<details><summary>
<b>Smart Home Panel 2 (EF-HD3####, FW Version: 4.0.0.122, WiFi Version: 2.0.1.20)</b>
</summary>

| *Sensors*                      |
|--------------------------------|
| Battery Level                  |
| Input Power                    |
| Output Power                   |
| Grid Power                     |
| Power In Use                   |
| Circuit Power (Each Circuit)   |
| Circuit Current (Each Circuit) |
| Channel Current (Each Channel) |
</details>
<details><summary>
<b>Delta Pro Ultra (EF-YJ####, FW Version: 5.0.0.25, WiFi Version: 2.0.2.4)</b>
</summary>

| *Sensors*                            |
|--------------------------------------|
| Battery Level                        |
| Individual Battery Levels (disabled) |
| Input Power                          |
| Output Power                         |
| Low Voltage Solar Power              |
| High Voltage Solar Power             |
| AC L1 (1) Output Power               |
| AC L1 (2) Output Power               |
| AC L2 (1) Output Power               |
| AC L2 (2) Output Power               |
| AC TT-30R Output Power               |
| AC L14-30P Output Power              |
| AC I/O Output Power                  |
</details>
<details><summary>
<b>River 3 (Plus, UPS, Plus Wireless) (EF-R3####)</b>
</summary>

| *Sensors*                       | *Switches*     | *Sliders*            | *Selects*            |
|---------------------------------|----------------|----------------------|----------------------|
| AC Input Energy                 | AC Port        | Backup Reserve Level | Led Mode (Plus only) |
| AC Input Power                  | DC Port        | Max Charge Limit     | DC Charging Type     |
| AC Output Energy                | Backup Reserve | Min Discharge Limit  |                      |
| AC Output Power                 |                | AC Charging Speed    |                      |
| Main Battery Level (Plus only)  |                | DC Charging Max Amps |                      |
| Battery Level                   |                |                      |                      |
| DC 12V Port Output Energy       |                |                      |                      |
| DC 12V Port Output Power        |                |                      |                      |
| DC Input Energy                 |                |                      |                      |
| DC Input Power                  |                |                      |                      |
| Input Energy Total              |                |                      |                      |
| Input Power Total               |                |                      |                      |
| Output Energy Total             |                |                      |                      |
| Output Power Total              |                |                      |                      |
| USB A Output Energy             |                |                      |                      |
| USB A Output Power              |                |                      |                      |
| USB C Output Energy             |                |                      |                      |
| USB C Output Power              |                |                      |                      |
| Battery Input Power (disabled)  |                |                      |                      |
| Battery Output Power (disabled) |                |                      |                      |
| Cell Temperature (disabled)     |                |                      |                      |
</details>

<details><summary>
<b>Delta 3 (Plus) (EF-D3####)</b>
</summary>

| *Sensors*                           | *Switches*     | *Sliders*                            |
|-------------------------------------|----------------|--------------------------------------|
| Main Battery Level                  | AC Ports       | Backup Reserve Level                 |
| Battery Level                       | DC Ports       | Max Charge Limit                     |
| AC Input Power                      | Backup Reserve | Min Discharge Limit                  |
| AC Output Power                     | USB Ports      | AC Charging Speed                    |
| DC 12V Port Output Power            |                | DC Charging Max Amps                 |
| DC Port Input Power                 |                | DC (2) Charging Max Amps (Plus only) |
| DC Port Input State                 |                |                                      |
| DC Port (2) Input Power (Plus only) |                |                                      |
| DC Port (2) Input State (Plus only) |                |                                      |
| Solar Power                         |                |                                      |
| Solar Power (2) (Plus only)         |                |                                      |
| Input Power Total                   |                |                                      |
| Output Power Total                  |                |                                      |
| USB A Output Power                  |                |                                      |
| USB A (2) Output Power              |                |                                      |
| USB C Output Power                  |                |                                      |
| USB C (2) Output Power              |                |                                      |
| AC Plugged In                       |                |                                      |
| Battery Input Power (disabled)      |                |                                      |
| Battery Output Power (disabled)     |                |                                      |
| Cell Temperature (disabled)         |                |                                      |
</details>

<details><summary>
<b>Delta Pro 3 (EF-DP3####)</b>
</summary>

| *Sensors*                   | *Switches*     | *Sliders*            |
|-----------------------------|----------------|----------------------|
| Main Battery Level          | AC Ports       | Backup Reserve Level |
| Battery Level               | DC Ports       | Max Charge Limit     |
| AC Input Power              | Backup Reserve | Min Discharge Limit  |
| AC LV Output Power          |                | AC Charging Speed    |
| AC HV Output Power          |                |                      |
| DC 12V Output Power         |                |                      |
| DC LV Input Power           |                |                      |
| DC LV Input State           |                |                      |
| DC HV Input Power           |                |                      |
| DC HV Input State           |                |                      |
| Solar LV Power              |                |                      |
| Solar HV Power              |                |                      |
| Input Power Total           |                |                      |
| Output Power Total          |                |                      |
| USB A Output Power          |                |                      |
| USB A (2) Output Power      |                |                      |
| USB C Output Power          |                |                      |
| USB C (2) Output Power      |                |                      |
| AC Plugged In               |                |                      |
| Cell Temperature (disabled) |                |                      |
</details>

<details><summary>
<b>STREAM (AC, AC Pro, Max, Pro, Ultra)</b>
</summary>

| *Sensors*                              | *Switches*                       | *Sliders*             | *Selects*       |
|----------------------------------------|----------------------------------|-----------------------|-----------------|
| Battery Level                          | Feed Grid                        | Feed Grid Power Limit | Energy Strategy |
| Grid Power                             | AC (1) (AC Pro, Max, Pro, Ultra) | Backup Reserve Level  |                 |
| Grid Voltage                           | AC (2) (AC Pro, Pro, Ultra)      | Charge Limit          |                 |
| Grid Frequency                         |                                  | Discharge Limit       |                 |
| Load from Battery                      |                                  |                       |                 |
| Load from Grid                         |                                  |                       |                 |
| Load from PV (Max, Pro, Ultra)         |                                  |                       |                 |
| AC (1) Power (AC Pro, Max, Pro, Ultra) |                                  |                       |                 |
| AC (2) Power (AC Pro, Pro, Ultra)      |                                  |                       |                 |
| PV (1) Power (Max, Pro, Ultra)         |                                  |                       |                 |
| PV (2) Power (Max, Pro, Ultra)         |                                  |                       |                 |
| PV (3) Power (Pro, Ultra)              |                                  |                       |                 |
| PV (4) Power (Ultra)                   |                                  |                       |                 |
| Cell Temperature (disabled)            |                                  |                       |                 |
</details>

</p>

**NOTICE**: this integration utilizes Bluetooth LE of the EF device, which is supporting just one
connection at a time - so if you want to manage the device through BLE from your phone, you will
need to disable this device in HA for that and later re-enable it to continue to collect data. It's
an internal EF device limitation, so not much to do here...

## WARNING: Support & Warranty

Sorry, limited support and no warranty - you on your own and I take no responsibility for any of
your actions. We all grown-ups here and know that we deal with quite dangerous voltages and storage
devices that could injure or cause death. So make sure you know what you doing for each and every
step - otherwise you can't use the provided information in this repository or integration.

In case you see some issues with your device after using this integration - ecoflow support could
be unable to help you. Author of the integration is not connected to EcoFlow anyhow and they can't
support anything you will find here.

## Usage

Install the integration as custom_component and it will automatically find the supported devices.
It will also require your user id that was created during initialization of your device with app.

Please refer to the wiki page to find more info: <https://github.com/rabits/ha-ef-ble/wiki>

## Development & Reverse

Information about how that was reversed you can find here: <https://github.com/rabits/ef-ble-reverse>

If you want to help with this integration - your changes will be most welcomed, but I recommend to
create a ticket first to discuss the needed features or upcoming changes to make sure they fit the
purpose of the integration.

## Legal

This repository is not for sale.

The work was done in order to localize devices and make them available / controllable in disaster
situations (unavailability of internet or cut-off the ecoflow servers). The official application
allows to connect via bluetooth, but to do that you have to login to the server. No server is here
and you screwed.

The requests to ecoflow usually ends up in support department and generally ignored, so there is no
way to get support from them. That gave me right to take it in my own hands and use my knowledge &
time to make my own way. There is no intention to harm any people anyhow - just to make sure you
will be safe in emergency situation, which is critical for such a product.
