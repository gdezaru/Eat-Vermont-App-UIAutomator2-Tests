import uiautomator2 as u2

# Initialize the device
d = u2.connect()
print("Device info:", d.info)
print("\nInstalling uiautomator APK...")
d.uiautomator.start()  # Install and start uiautomator server
print("Done! Your device is ready for testing.")
