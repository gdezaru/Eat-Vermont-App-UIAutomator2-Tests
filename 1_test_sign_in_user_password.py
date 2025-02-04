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

def test_sign_in_user_password(d):
    """Test sign in with valid user and password"""
    # Take screenshot to debug initial state
    d.screenshot("before_signin.png")
    print("\nTaking screenshot before_signin.png")
    
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
        
    assert sign_in is not None, "Could not find Sign In button"
    print("Clicking Sign In button...")
    sign_in.click()
    sleep(1)
    
    # Enter email
    print("\nEntering email...")
    email_field = d(text="Email")
    email_field.click()
    d.send_keys(TEST_USER['email'])
    
    # Enter password
    print("Entering password...")
    password_field = d(text="Password")
    password_field.click()
    d.send_keys(TEST_USER['password'])
    
    # Click Log in
    print("Clicking Log in button...")
    d(text="Log in").click()
    sleep(3)  # Wait for home screen
    
    # Verify successful login by checking Events text is visible
    print("\nVerifying successful login...")
    assert d(textContains="Events").exists(timeout=10), "Login failed - Events text not found after login"
    
    # Take screenshot after successful login
    d.screenshot("login_success.png")
    print("Login successful! Screenshot saved as login_success.png")
