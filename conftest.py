import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_connection import AppiumConnection
from selenium.webdriver.common.options import BaseOptions
from selenium.webdriver.common.selenium_manager import SeleniumManager
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.remote_connection import RemoteConnection
from appium.options.common.base import AppiumOptions
from selenium.webdriver.remote.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import random
import subprocess
import uiautomator2 as u2
from datetime import datetime

def run_adb_command(command):
    """Run an ADB command and return its output"""
    try:
        # Use explicit path to ADB and force local server
        adb_path = os.path.expanduser("~/AppData/Local/Android/Sdk/platform-tools/adb.exe")
        if not os.path.exists(adb_path):
            print(f"ADB not found at {adb_path}")
            # Try alternative path
            adb_path = "adb"  # Use adb from PATH
            
        result = subprocess.run(f"{adb_path} {command}", shell=True, capture_output=True, text=True)
        if result.stderr:
            print(f"ADB command warning/error: {result.stderr}")
        return result.stdout.strip()
    except Exception as e:
        print(f"Error running ADB command: {e}")
        return None

@pytest.fixture
def driver():
    driver = None
    system_port = random.randint(8200, 8299)
    device_id = 'b0ba3ece'
    
    # First, kill any existing ADB server
    print("\nRestarting ADB server...")
    run_adb_command("kill-server")
    sleep(2)
    run_adb_command("start-server")
    sleep(2)

    # Check USB connected devices
    print("\nChecking USB connected devices...")
    devices = run_adb_command("devices")
    print(f"Connected devices: {devices}")

    if device_id not in str(devices):
        raise Exception(
            "Device not found. Please ensure:\n"
            f"1. Device {device_id} is connected via USB\n"
            "2. USB debugging is enabled on the device\n"
            "3. You have approved the USB debugging prompt on your device\n"
            "Current connected devices: " + str(devices)
        )
    
    capabilities = {
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'deviceName': device_id,
        'appPackage': 'com.eatvermont',
        'appActivity': '.MainActivity',
        'noReset': True,
        'autoLaunch': True,
        # Minimal timeouts
        'newCommandTimeout': 15,
        'uiautomator2ServerLaunchTimeout': 20000,
        'uiautomator2ServerInstallTimeout': 20000,
        'androidInstallTimeout': 30000,
        'adbExecTimeout': 20000,
        'waitForIdleTimeout': 0,
        # Quick startup options
        'systemPort': system_port,
        'skipServerInstallation': False,
        'skipDeviceInitialization': False,
        'enforceAppInstall': True,
        'autoGrantPermissions': True,
        'disableWindowAnimation': True,
        'ignoreHiddenApiPolicyError': True,
        'noSign': True,
        'dontStopAppOnReset': True
    }

    options = UiAutomator2Options().load_capabilities(capabilities)

    try:
        # Force stop the app and clear UiAutomator data
        print("\nClearing app and UiAutomator state...")
        run_adb_command(f"-s {device_id} shell am force-stop {capabilities['appPackage']}")
        run_adb_command(f"-s {device_id} shell pm clear io.appium.uiautomator2.server")
        run_adb_command(f"-s {device_id} shell pm clear io.appium.uiautomator2.server.test")
        sleep(1)
        
        # Uninstall UiAutomator2 server if it exists
        print("\nRemoving old UiAutomator2 server...")
        run_adb_command(f"-s {device_id} uninstall io.appium.uiautomator2.server")
        run_adb_command(f"-s {device_id} uninstall io.appium.uiautomator2.server.test")
        sleep(1)
        
        print(f"\nStarting driver with system port: {system_port}")
        driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
        
        # Quick app restart
        print("\nRestarting app...")
        driver.terminate_app('com.eatvermont')
        sleep(1)
        driver.activate_app('com.eatvermont')
        sleep(2)  # Keep minimal wait for app to load
        
        yield driver
        
    except Exception as e:
        print(f"\nError during driver setup: {str(e)}")
        # Get device logs for debugging
        logs = run_adb_command(f"-s {device_id} logcat -d")
        if logs:
            print("\nDevice logs:")
            print(logs)
        raise
        
    finally:
        if driver:
            driver.quit()
            run_adb_command(f"-s {device_id} shell pm clear io.appium.uiautomator2.server")
            run_adb_command(f"-s {device_id} shell pm clear io.appium.uiautomator2.server.test")

@pytest.fixture
def d():
    # Connect to the device using direct USB connection
    device = u2.connect_usb()
    
    # Clean up the app state before starting
    print("\nCleaning up app state...")
    run_adb_command("shell am force-stop com.eatvermont")
    run_adb_command("shell pm clear com.eatvermont")
    sleep(1)  # Wait for cleanup
    
    # Grant necessary permissions before starting
    print("\nGranting necessary permissions...")
    permissions = [
        "android.permission.POST_NOTIFICATIONS",
        "android.permission.CAMERA",
        "android.permission.ACCESS_FINE_LOCATION",
        "android.permission.ACCESS_COARSE_LOCATION",
        "android.permission.READ_EXTERNAL_STORAGE"
    ]
    for permission in permissions:
        run_adb_command(f"shell pm grant com.eatvermont {permission}")
    
    print("\nStarting app...")
    run_adb_command("shell monkey -p com.eatvermont -c android.intent.category.LAUNCHER 1")
    sleep(3)  # Wait for app to load
    
    # Handle any remaining permission dialogs
    if device(text="Allow").exists:
        device(text="Allow").click()
        sleep(1)
    
    # Verify app is running
    current_app = device.app_current()
    print(f"Current app: {current_app}")
    assert current_app['package'] == "com.eatvermont", "App is not running!"
    
    yield device
    
    # Cleanup after test
    print("\nCleaning up after test...")
    run_adb_command("shell am force-stop com.eatvermont")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # We only look at actual test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        try:
            if "d" in item.funcargs:  # Check if test has the 'd' fixture
                driver = item.funcargs["d"]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                # Get the test name from the item
                test_module = item.module.__name__  # Gets the module name (e.g., test_login)
                test_name = item.name  # Gets the test function name
                
                # Extract step number from the test function's docstring or code
                step_num = "unknown_step"
                if hasattr(item.function, '__doc__') and item.function.__doc__:
                    doc = item.function.__doc__
                    # Look for step number in docstring (format: Step X:)
                    import re
                    step_match = re.search(r'Step (\d+):', doc)
                    if step_match:
                        step_num = step_match.group(1)
                
                # Format: failure_[module]_[test_name]_step[X]_[timestamp].png
                screenshot_name = f"failure_{test_module}_{test_name}_step{step_num}_{timestamp}.png"
                screenshot_dir = "screenshots/failures"
                
                # Create failures directory if it doesn't exist
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)
                
                screenshot_path = os.path.join(screenshot_dir, screenshot_name)
                driver.screenshot(screenshot_path)
                print(f"\nTest failed! Screenshot saved: {screenshot_path}")
                
                # Also capture device logs with the same naming convention
                device_id = 'b0ba3ece'  # This is already defined in the fixture
                logs = run_adb_command(f"-s {device_id} logcat -d")
                if logs:
                    log_name = f"failure_{test_module}_{test_name}_step{step_num}_{timestamp}.log"
                    log_path = os.path.join(screenshot_dir, log_name)
                    with open(log_path, 'w') as f:
                        f.write(logs)
                    print(f"Device logs saved: {log_path}")
        except Exception as e:
            print(f"Failed to capture failure screenshot: {str(e)}")
