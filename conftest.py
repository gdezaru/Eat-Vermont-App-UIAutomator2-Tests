import pytest
import os
import random
import subprocess
from time import sleep
import uiautomator2 as u2
from datetime import datetime
from test_reporter import ExcelReporter

# Initialize test items list
pytest.test_items = []

def pytest_collection_modifyitems(items):
    """Store test items for later use in reporting"""
    pytest.test_items = items

    """Order test files numerically based on their filename prefix."""
    def get_test_order(item):
        # Extract the number from the test file name (e.g., '1' from '1_tests_sign_in_user_password.py')
        try:
            return int(item.module.__file__.split('\\')[-1].split('_')[0])
        except (ValueError, IndexError):
            return float('inf')  # Put non-numbered files at the end
    
    # Sort the test items based on their numerical prefix
    items.sort(key=get_test_order)

# Create a single instance of the reporter
reporter = ExcelReporter()

def pytest_configure(config):
    """Configure pytest and register the Excel reporter."""
    # Register the reporter as a plugin
    config.pluginmanager.register(reporter)

def pytest_addoption(parser):
    """Add command line options."""
    pass

@pytest.fixture
def d():
    """Initialize UI Automator 2 device connection and setup"""
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

    # Connect to the device using direct USB connection
    device = u2.connect_usb()
    
    # Restart UI Automator service
    print("\nRestarting UI Automator service...")
    run_adb_command(f"-s {device_id} shell am force-stop com.github.uiautomator")
    run_adb_command(f"-s {device_id} shell am force-stop com.github.uiautomator.test")
    sleep(2)
    device.service("uiautomator").stop()
    sleep(2)
    device.service("uiautomator").start()
    sleep(3)  # Wait for service to fully start
    
    # Clean up the app state before starting
    print("\nCleaning up app state...")
    force_stop_output = run_adb_command(f"-s {device_id} shell am force-stop com.eatvermont")
    clear_output = run_adb_command(f"-s {device_id} shell pm clear com.eatvermont")
    print(f"Force stop output: {force_stop_output}")
    print(f"Clear output: {clear_output}")
    sleep(1)  # Wait for cleanup
    
    # Grant necessary permissions before starting
    permissions = [
        'android.permission.ACCESS_FINE_LOCATION',
        'android.permission.ACCESS_COARSE_LOCATION',
        'android.permission.CAMERA',
        'android.permission.READ_EXTERNAL_STORAGE',
        'android.permission.POST_NOTIFICATIONS',
        'android.permission.RECORD_AUDIO',
        'android.permission.READ_CALENDAR',
        'android.permission.WRITE_CALENDAR'
    ]
    
    print("\nGranting app permissions...")
    for permission in permissions:
        run_adb_command(f"-s {device_id} shell pm grant com.eatvermont {permission}")
    
    # Start the app using UI Automator 2's app_start
    print("\nStarting app...")
    device.app_start("com.eatvermont", ".MainActivity")
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

    # Cleanup after tests
    print("\nCleaning up after tests...")
    device.app_stop("com.eatvermont")
    run_adb_command(f"-s {device_id} shell am force-stop com.eatvermont")

@pytest.fixture
def screenshots_dir():
    """Get the screenshots directory for saving test screenshots"""
    screenshots_dir = os.path.join(os.getcwd(), 'screenshots')
    os.makedirs(screenshots_dir, exist_ok=True)
    return screenshots_dir

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

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Extends test reporting to include screenshots.
    """
    outcome = yield
    report = outcome.get_result()
    
    test_fn = item.function.__name__
    
    # Take screenshot on failure using UI Automator 2
    if report.when == "call" and report.failed:
        try:
            device = item.funcargs['d']  # Get the device fixture
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_dir = os.path.join(os.getcwd(), 'screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)
            
            screenshot_path = os.path.join(
                screenshot_dir,
                f"fail_{test_fn}_{timestamp}.png"
            )
            
            # Take screenshot using UIAutomator2
            device.screenshot(screenshot_path)
            
            # Add screenshot to the report
            reporter.add_screenshot(item.nodeid, screenshot_path)
            
        except Exception as e:
            print(f"Failed to capture screenshot: {e}")
    
    # Collect steps to reproduce
    if report.when == "call":
        # Get docstring as steps if available
        if item.function.__doc__:
            steps = [step.strip() for step in item.function.__doc__.split('\n') if step.strip()]
            for step in steps:
                reporter.add_step(item.nodeid, step)
        
        # Add test result to reporter
        reporter.pytest_runtest_logreport(report)
