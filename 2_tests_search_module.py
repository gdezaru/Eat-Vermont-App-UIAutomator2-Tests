import pytest
from time import sleep
from config import TEST_USER
from locators import Events
from utils import handle_notification_permission


@pytest.mark.smoke
def test_search_events(d):
    """Test searching for events"""
    handle_notification_permission(d)

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

            # Check if events popup is visible and handle it
        events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
        if events_popup.exists:
            print("\nEvents popup is visible, closing it...")
            sleep(3)
            close_button = d.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
            print("\nChecking close button...")
            print(f"Close button exists: {close_button.exists}")
            if close_button.exists:
                print(f"Close button info: {close_button.info}")
            assert close_button.exists, "Close button not found on events popup"
            print("\nAttempting to click close button...")
            close_button.click()
            print("\nClose button clicked")
            sleep(3)  # Wait for popup to close

            # Verify popup is closed
            print("\nVerifying popup is closed...")
            events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
            assert not events_popup.exists, "Events popup is still visible after clicking close button"
            print("Events popup successfully closed")
        else:
            print("\nNo events popup found, continuing with next steps...")

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
            sleep(10)
            d.screenshot("2_1_search_events.png")
            return
        sleep(10)

    assert False, "Search failed - Could not verify search results"


@pytest.mark.smoke
def test_search_businesses(d):
    """Test searching for businesses"""
    handle_notification_permission(d)

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

            # Check if events popup is visible and handle it
        events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
        if events_popup.exists:
            print("\nEvents popup is visible, closing it...")
            sleep(3)
            close_button = d.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
            print("\nChecking close button...")
            print(f"Close button exists: {close_button.exists}")
            if close_button.exists:
                print(f"Close button info: {close_button.info}")
            assert close_button.exists, "Close button not found on events popup"
            print("\nAttempting to click close button...")
            close_button.click()
            print("\nClose button clicked")
            sleep(3)  # Wait for popup to close

            # Verify popup is closed
            print("\nVerifying popup is closed...")
            events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
            assert not events_popup.exists, "Events popup is still visible after clicking close button"
            print("Events popup successfully closed")
        else:
            print("\nNo events popup found, continuing with next steps...")

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
    d.send_keys("Big Fatty BBQ")
    sleep(1)
    d.press("enter")
    sleep(2)

    # Verify search results
    verify_attempts = 3
    for _ in range(verify_attempts):
        if (d(textContains="Big Fatty BBQ").exists(timeout=5) or
                d(textContains="Results").exists(timeout=5) or
                d(textContains="Big Fatty BBQ").exists(timeout=5)):
            sleep(10)
            d.screenshot("2_2_search_business.png")
            return
        sleep(10)

    assert False, "Search failed - Could not verify search results"


@pytest.mark.smoke
def test_search_day_trips(d):
    """Test searching for day trips"""
    handle_notification_permission(d)

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

    events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
    if events_popup.exists:
        print("\nEvents popup is visible, closing it...")
        sleep(3)
        close_button = d.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
        print("\nChecking close button...")
        print(f"Close button exists: {close_button.exists}")
        if close_button.exists:
            print(f"Close button info: {close_button.info}")
        assert close_button.exists, "Close button not found on events popup"
        print("\nAttempting to click close button...")
        close_button.click()
        print("\nClose button clicked")
        sleep(3)  # Wait for popup to close

        # Verify popup is closed
        print("\nVerifying popup is closed...")
        events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
        assert not events_popup.exists, "Events popup is still visible after clicking close button"
        print("Events popup successfully closed")
    else:
        print("\nNo events popup found, continuing with next steps...")

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
    d.send_keys("Day Trip")
    sleep(1)
    d.press("enter")
    sleep(2)

    # Verify search results
    verify_attempts = 3
    for _ in range(verify_attempts):
        if (d(textContains="Day Trip").exists(timeout=5) or
                d(textContains="Results").exists(timeout=5) or
                d(textContains="Day Trip").exists(timeout=5)):
            # Scroll to bottom of results
            screen_size = d.window_size()
            for _ in range(3):  # Scroll 3 times to ensure we reach bottom
                d.swipe(screen_size[0] * 0.5, screen_size[1] * 0.8,
                        screen_size[0] * 0.5, screen_size[1] * 0.2,
                        duration=0.5)
                sleep(2)  # Wait for content to load
            sleep(10)
            d.screenshot("2_3_search_day_trips.png")
            return
        sleep(10)

    assert False, "Search failed - Could not verify search results"


@pytest.mark.smoke
def test_search_videos(d):
    """Test searching for videos"""
    handle_notification_permission(d)

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

    events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
    if events_popup.exists:
        print("\nEvents popup is visible, closing it...")
        sleep(3)
        close_button = d.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
        print("\nChecking close button...")
        print(f"Close button exists: {close_button.exists}")
        if close_button.exists:
            print(f"Close button info: {close_button.info}")
        assert close_button.exists, "Close button not found on events popup"
        print("\nAttempting to click close button...")
        close_button.click()
        print("\nClose button clicked")
        sleep(3)  # Wait for popup to close

        # Verify popup is closed
        print("\nVerifying popup is closed...")
        events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
        assert not events_popup.exists, "Events popup is still visible after clicking close button"
        print("Events popup successfully closed")
    else:
        print("\nNo events popup found, continuing with next steps...")

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
    d.send_keys("Rocket")
    sleep(1)
    d.press("enter")
    sleep(2)

    # Verify search results
    verify_attempts = 3
    for _ in range(verify_attempts):
        if (d(textContains="Rocket").exists(timeout=5) or
                d(textContains="Results").exists(timeout=5) or
                d(textContains="Rocket").exists(timeout=5)):
            # Scroll to bottom of results
            screen_size = d.window_size()
            for _ in range(3):  # Scroll 3 times to ensure we reach bottom
                d.swipe(screen_size[0] * 0.5, screen_size[1] * 0.8,
                        screen_size[0] * 0.5, screen_size[1] * 0.2,
                        duration=0.5)
                sleep(2)  # Wait for content to load
            sleep(10)
            d.screenshot("2_4_search_videos.png")
            return
        sleep(10)

    assert False, "Search failed - Could not verify search results"
