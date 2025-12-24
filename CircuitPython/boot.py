# boot.py
import usb_cdc
import usb_hid

# Enable both console and data CDC channels
usb_cdc.enable(console=True, data=True)

# Enable HID devices
usb_hid.enable((usb_hid.Device.KEYBOARD,))
