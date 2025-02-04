import pytest
from time import sleep
from config import TEST_USER

def test_sign_in_user_password(d):
    """Test sign in with valid user and password"""
    # Handle notification permission if it appears
    if d(text="Allow").exists:
        d(text="Allow").click()
        sleep(1)
    
    # Find and click Sign In button
    sign_in = None
    if d(description="Sign In").exists(timeout=5):
        sign_in = d(description="Sign In")
    elif d(text="Sign In").exists(timeout=5):
        sign_in = d(text="Sign In")
    
    assert sign_in is not None, "Could not find Sign In button"
    sign_in.click()
    sleep(2)
    
    # Enter email
    email_field = d(text="Email")
    assert email_field.exists(timeout=5), "Email field not found"
    email_field.click()
    d.send_keys(TEST_USER['email'])
    sleep(1)
    
    # Enter password
    password_field = d(text="Password")
    assert password_field.exists(timeout=5), "Password field not found"
    password_field.click()
    d.send_keys(TEST_USER['password'])
    sleep(1)
    
    # Click Log in and verify
    login_attempts = 2
    for attempt in range(login_attempts):
        # Find and click login button
        login_button = d(text="Log in")
        assert login_button.exists(timeout=5), "Log in button not found"
        login_button.click()
        sleep(5)
        
        # Check for error messages
        error_messages = [
            "Invalid email or password",
            "Login failed",
            "Error",
            "Something went wrong",
            "No internet connection"
        ]
        
        error_found = False
        for error_msg in error_messages:
            if d(textContains=error_msg).exists(timeout=2):
                error_found = True
                break
        
        if error_found:
            if attempt < login_attempts - 1:
                # Try to go back if needed
                if d(text="Back").exists():
                    d(text="Back").click()
                    sleep(1)
                continue
            else:
                d.screenshot("debug_login_error.png")
                assert False, f"Login failed - Error message found"
        
        # Try multiple verification attempts
        verify_attempts = 3
        for _ in range(verify_attempts):
            # Check for success indicators
            for indicator in ["Events", "Home", "Profile", "Search"]:
                if d(text=indicator).exists(timeout=3):
                    d.screenshot("1_1_sign_in_user_password.png")
                    return
            sleep(2)  # Wait between verification attempts
        
        if attempt < login_attempts - 1:
            # Try to go back if needed
            if d(text="Back").exists():
                d(text="Back").click()
                sleep(1)
    
    # If we get here, login failed
    d.screenshot("debug_login_failed.png")
    assert False, "Login failed - Could not verify successful login"
