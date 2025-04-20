import sounddevice as sd

# Query the list of devices
devices = sd.query_devices()

# Iterate through the devices and print their names
for i in range(len(devices)):
    print(f"Device {i+1}: {devices[i]['name']}")

