import pytest
from time import sleep
from config import TEST_USER

def test_search_events(d):
    """Test searching for events using uiautomator2"""
    # Take screenshot to debug initial state
    d.screenshot("before_search.png")
    print("\nTaking screenshot before_search.png")
    
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
    
    # Click on Search in bottom navigation
    print("\nNavigating to search...")
    d(description="Search").click()
    sleep(1)
    
    # Click search field and enter text
    print("Entering search term...")
    search_field = d(description="Search")
    search_field.click()
    d.send_keys("Burlington")
    
    # Press enter key twice with a pause
    print("Pressing enter key...")
    d.press("enter")
    sleep(2)
    d.press("enter")
    sleep(3)  # Wait for search results
    
    # Verify results
    print("\nVerifying search results...")
    assert d(textContains="Burlington").exists(timeout=10), "No search results found for Burlington"
    
    # Take screenshot of results
    d.screenshot("search_results.png")
    print("Search successful! Screenshot saved as search_results.png")