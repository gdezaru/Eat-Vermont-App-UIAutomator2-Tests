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
