import pytest
from time import sleep
from config import TEST_USER

def test_search_events(d):
    """Test searching for events using uiautomator2"""
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
        sleep(5)  # Wait for login process
        
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
        
        if error_found and attempt < login_attempts - 1:
            continue
        
        # Verify successful login by checking for common elements
        success_indicators = ["Events", "Home", "Profile", "Search"]
        for indicator in success_indicators:
            if d(text=indicator).exists(timeout=5):
                break
        else:
            if attempt < login_attempts - 1:
                # Try to go back if needed
                if d(text="Back").exists():
                    d(text="Back").click()
                    sleep(1)
                continue
            assert False, "Login failed - Could not verify successful login"
    
    # Find and click Search in bottom navigation
    search_button = None
    if d(description="Search").exists(timeout=5):
        search_button = d(description="Search")
    elif d(text="Search").exists(timeout=5):
        search_button = d(text="Search")
    elif d(resourceId="Search").exists(timeout=5):
        search_button = d(resourceId="Search")
        
    assert search_button is not None, "Could not find Search button"
    search_button.click()
    sleep(2)
    
    # Find and click search field
    search_field = None
    search_selectors = [
        lambda: d(description="Search"),
        lambda: d(text="Search"),
        lambda: d(resourceId="search-input"),
        lambda: d(className="android.widget.EditText")
    ]
    
    for selector in search_selectors:
        if selector().exists(timeout=3):
            search_field = selector()
            break
    
    assert search_field is not None, "Could not find search field"
    search_field.click()
    sleep(1)
    
    # Enter search term and submit
    d.send_keys("Burlington")
    sleep(1)
    d.press("enter")
    sleep(2)
    
    # Verify search results
    verify_attempts = 3
    for _ in range(verify_attempts):
        if (d(textContains="Burlington").exists(timeout=5) or
            d(textContains="Results").exists(timeout=5) or
            d(textContains="Event").exists(timeout=5)):
            d.screenshot("2_1_search_events.png")
            return
        sleep(2)
    
    assert False, "Search failed - Could not verify search results"