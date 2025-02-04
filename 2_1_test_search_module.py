import uiautomator2 as u2
import pytest
from time import sleep
from config import TEST_USER

@pytest.fixture
def d():
    # Connect to the device
    device = u2.connect()
    print("\nStarting app...")
    device.app_start("com.eatvermont")
    sleep(3)  # Wait for app to load
    
    # Verify app is running
    current_app = device.app_current()
    print(f"Current app: {current_app}")
    assert current_app['package'] == "com.eatvermont", "App is not running!"
    
    yield device
    device.app_stop("com.eatvermont")

def test_search_events(d):
    """Test searching for events using uiautomator2"""
    # Verify app is still running
    current_app = d.app_current()
    print(f"\nCurrent app before search: {current_app}")
    if current_app['package'] != "com.eatvermont":
        print("App not running, restarting...")
        d.app_start("com.eatvermont")
        sleep(3)
    
    # Take screenshot to debug
    d.screenshot("before_signin.png")
    print("\nTaking screenshot before_signin.png")
    
    # Print current UI hierarchy
    print("\nCurrent UI hierarchy:")
    print(d.dump_hierarchy())
    
    # Handle notification permission if it appears
    if d(text="Allow").exists:
        d(text="Allow").click()
        sleep(1)
    
    # Try to find Sign In button using different selectors with wait
    print("\nLooking for Sign In button...")
    sign_in = None
    
    # Try by description
    if d(description="Sign In").exists(timeout=5):
        print("Found Sign In by description")
        sign_in = d(description="Sign In")
    # Try by text
    elif d(text="Sign In").exists(timeout=5):
        print("Found Sign In by text")
        sign_in = d(text="Sign In")
    # Try by content-desc (another way to specify description)
    elif d(resourceId="Sign In").exists(timeout=5):
        print("Found Sign In by resourceId")
        sign_in = d(resourceId="Sign In")
        
    assert sign_in is not None, "Could not find Sign In button"
    print("Clicking Sign In button...")
    sign_in.click()
    sleep(1)
    
    # Enter email
    email_field = d(text="Email")
    email_field.click()
    d.send_keys(TEST_USER['email'])
    
    # Enter password
    password_field = d(text="Password")
    password_field.click()
    d.send_keys(TEST_USER['password'])
    
    # Click Log in
    d(text="Log in").click()
    sleep(3)  # Wait for home screen
    
    # Click on Search in bottom navigation
    d(description="Search").click()
    sleep(1)
    
    # Click search field and enter text
    search_field = d(description="Search")
    search_field.click()
    d.send_keys("Burlington")
    d.press("enter")
    sleep(2)
    
    # Verify results
    assert d(textContains="Burlington").exists, "No search results found for Burlington"
    
    # Take screenshot of results
    d.screenshot("search_results.png")
