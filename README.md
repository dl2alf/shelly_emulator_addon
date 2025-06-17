# Shelly Emulator Add-on

This Home Assistant add-on emulates a Shelly smart energy counter by fetching data from a Tasmota device.

## Configuration

- **tasmota_ip**: IP address of your Tasmota device (default: 192.168.1.50)

## Usage

- Clone or download this repository into your Home Assistant add-on directory.
- Configure the IP address of the Tasmota device in the add-on options.
- Start the add-on and monitor logs to confirm it's working.
- Access the Shelly-compatible API at `http://<homeassistant_ip>:8081/status`
