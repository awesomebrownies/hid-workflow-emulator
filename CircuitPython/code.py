import time
import board
import digitalio
import usb_hid
import usb_cdc
import sys
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import storage
import microcontroller

# Initialize USB HID keyboard
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# Initialize USB CDC for serial communication
# Use data port if available, otherwise None
serial = usb_cdc.data if usb_cdc.data is not None else None

# Set up serial with a timeout and configure it to be always ready
if serial:
    serial.timeout = 0.1
    # Clear any pending data in the serial buffer
    while serial.in_waiting > 0:
        serial.read(serial.in_waiting)
        time.sleep(0.01)

# Initialize button on GPIO12
button = digitalio.DigitalInOut(board.GP12)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Storage file for persistent workflow ID
WORKFLOW_FILE = "/workflow_id.txt"
BOOT_ORDER_FILE = "/boot_order.txt"

def read_workflow_id():
    """Read workflow ID from storage"""
    try:
        with open(WORKFLOW_FILE, "r") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0

def write_workflow_id(workflow_id):
    """Write workflow ID to storage"""
    try:
        with open(WORKFLOW_FILE, "w") as f:
            f.write(str(workflow_id))
    except OSError:
        pass

def read_boot_order():
    """Read boot order from storage"""
    try:
        with open(BOOT_ORDER_FILE, "r") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0

def write_boot_order(boot_order):
    """Write boot order to storage"""
    try:
        with open(BOOT_ORDER_FILE, "w") as f:
            f.write(str(boot_order))
    except OSError:
        pass

def type_animation(text):
    """Types text character by character with delay"""
    for char in text:
        layout.write(char)
        time.sleep(0.05)
    time.sleep(0.05)

def open_application(app_name):
    """Opens application via system menu"""
    # Press Super key (Windows/Meta key)
    kbd.press(Keycode.GUI)
    time.sleep(0.01)
    kbd.release(Keycode.GUI)
    time.sleep(0.1)
    
    type_animation(app_name)
    kbd.press(Keycode.ENTER)
    kbd.release(Keycode.ENTER)

def dual_boot_workflow():
    """Toggle between Linux and Windows boot order and restart"""
    boot_order = read_boot_order()
    
    if boot_order == 1:
        # Windows sequence
        write_boot_order(0)  # Set next boot to Linux
        
        # Windows+R
        kbd.press(Keycode.GUI, Keycode.R)
        time.sleep(0.01)
        kbd.release_all()
        time.sleep(0.3)
        
        layout.write("shutdown /r /t 0\n")
    else:
        # Linux sequence
        write_boot_order(1)  # Set next boot to Windows
        
        # Ctrl+Alt+T for terminal
        kbd.press(Keycode.CONTROL, Keycode.ALT, Keycode.T)
        time.sleep(0.01)
        kbd.release_all()
        time.sleep(0.75)
        
        layout.write("bash -c 'sudo efibootmgr -n 0000")
        layout.write(str(boot_order))
        layout.write(";reboot'\n")

def circuits_workflow():
    """Open VSCode and KiCAD"""
    open_application("vscode")
    time.sleep(0.5)
    open_application("kicad")

def system_admin_workflow():
    """Start backup processes - placeholder for future implementation"""
    pass

def github_analyzation():
    """Check git status across multiple repositories"""
    # Ctrl+Alt+T for terminal
    kbd.press(Keycode.CONTROL, Keycode.ALT, Keycode.T)
    time.sleep(0.01)
    kbd.release_all()
    time.sleep(0.75)
    
    layout.write("cd ./Documents/GitHub\n")
    layout.write("mgitstatus\n")

def read_serial_line(timeout_ms=5000):
    """Read a line from USB CDC serial with timeout, filtering escape sequences"""
    if serial is None:
        return None
    
    start_time = time.monotonic()
    buffer = bytearray()
    in_escape_sequence = False
    
    while (time.monotonic() - start_time) < (timeout_ms / 1000.0):
        bytes_available = serial.in_waiting
        
        if bytes_available > 0:
            data = serial.read(bytes_available)
            
            for byte_val in data:
                byte = bytes([byte_val])
                
                # Filter out escape sequences (ESC [ ... or ESC ] ...)
                if byte == b'\x1b':  # ESC character
                    in_escape_sequence = True
                    continue
                
                if in_escape_sequence:
                    # Skip until we hit a letter (end of escape sequence)
                    # or specific terminators
                    if byte in (b'\x07', b'\\'):  # BEL or backslash can end sequences
                        in_escape_sequence = False
                    elif 64 <= byte_val <= 126:  # Letters and some symbols
                        in_escape_sequence = False
                    continue
                
                # Check for line endings
                if byte == b'\n':
                    if len(buffer) > 0:
                        try:
                            result = buffer.decode('utf-8').strip()
                            # Filter out control characters (keep only ASCII 32-126 and whitespace)
                            result = ''.join(c for c in result if ord(c) >= 32 or c in '\t\n\r')
                            result = result.strip()
                            if result:  # Only return non-empty results
                                return result
                            buffer = bytearray()  # Clear and continue
                        except Exception:
                            buffer = bytearray()
                elif byte == b'\r':
                    if len(buffer) > 0:
                        try:
                            result = buffer.decode('utf-8').strip()
                            result = ''.join(c for c in result if ord(c) >= 32 or c in '\t\n\r')
                            result = result.strip()
                            if result:
                                return result
                            buffer = bytearray()
                        except Exception:
                            buffer = bytearray()
                else:
                    buffer.extend(byte)
        
        time.sleep(0.01)
    
    # Timeout reached
    if len(buffer) > 0:
        try:
            result = buffer.decode('utf-8').strip()
            result = ''.join(c for c in result if ord(c) >= 32 or c in '\t\n\r')
            result = result.strip()
            if result:
                return result
        except Exception:
            pass
    
    return None

def query(prompt, timeout_ms=5000):
    """Query user for input via terminal and read response via serial"""
    # Clear any pending serial data before query
    if serial:
        while serial.in_waiting > 0:
            serial.read(serial.in_waiting)
            time.sleep(0.01)
    
    # Ctrl+Alt+T for terminal
    kbd.press(Keycode.CONTROL, Keycode.ALT, Keycode.T)
    time.sleep(0.01)
    kbd.release_all()
    time.sleep(0.75)
    
    # Use stty to disable echo and special processing, send raw data
    layout.write("bash -c '")
    # Configure the serial port for raw mode first
    layout.write("P=$(ls /dev/ttyACM* | tail -1); ")
    layout.write("stty -F \"$P\" raw -echo; ")
    # Now do the prompt and send
    layout.write("clear; echo \"")
    layout.write(prompt)
    layout.write("\"; read -t 10 r; ")
    # Send ONLY the response, no escape codes
    layout.write("printf \"%s\\n\" \"$r\" > \"$P\"")
    layout.write("'\n")
    
    time.sleep(1.5)
    
    # Read response from serial
    response = read_serial_line(timeout_ms)
    
    if response is None or response == "":
        response = "-1"
    
    time.sleep(0.2)
    layout.write("exit\n")
    time.sleep(0.2)
    
    return response

def programming_workflow():
    """Open programming environment"""
    # Query for subworkflow
    response = query("[java/dart] [python/javascript] [go/c++]", 5000)
    
    # You can now act on the response if needed
    # For example:
    if "spigot" in response.lower():
        open_application("firefox")
    #     # Open Minecraft development docs
    #     pass
    # elif "research" in response.lower():
    #     # Open research documentation
    #     pass
    
    # time.sleep(0.5)
    # open_application("intellij")
    # time.sleep(0.5)
    # open_application("github desktop")
    # time.sleep(2.0)
    # github_analyzation()

# Main execution
time.sleep(1.0)  # Wait for USB to be recognized

# Set up persistent serial listener (optional but recommended)
# Comment this out if you prefer the inline cat method
# setup_serial_listener()

workflow_id = read_workflow_id()
workflow_min = 0
workflow_max = 3

# Check if button is pressed (active LOW)
if button.value:
    prompt = "Select ID: [0] Programming, [1] Dual Boot, [2] Circuits, [3] Sys-Admin"
    prompt = prompt.replace(f"[{workflow_id}]", f"[{workflow_id}:MEM-SEL]")
    
    response = query(prompt, 10000)  # 10 second timeout for selection
    
    try:
        test_id = int(response.strip())
        if workflow_min <= test_id <= workflow_max and test_id != workflow_id:
            workflow_id = test_id
            write_workflow_id(workflow_id)
    except (ValueError, AttributeError):
        pass

# Execute workflow based on ID
if workflow_id == 0:
    programming_workflow()
elif workflow_id == 1:
    dual_boot_workflow()
elif workflow_id == 2:
    circuits_workflow()
elif workflow_id == 3:
    system_admin_workflow()

# CircuitPython runs continuously, but this workflow completes once
print(f"Workflow {workflow_id} completed")
