import time
from time import sleep
from config import TEST_USER
from locators import Events


def test_events_popup(d):
    """Tests the contents of the events popup."""
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

        # Check if events popup is visible and handle it
        events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
        if events_popup.exists:
            print("\nEvents popup is visible, closing it...")
            # Take screenshot of the events popup
            d.screenshot("3_6_1_events_popup.png")
            time.sleep(7)
            # Take second screenshot of the events popup
            d.screenshot("3_6_2_events_popup.png")
            close_button = d.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
            print("\nChecking close button...")
            print(f"Close button exists: {close_button.exists}")
            if close_button.exists:
                print(f"Close button info: {close_button.info}")
            assert close_button.exists, "Close button not found on events popup"
            print("\nAttempting to click close button...")
            close_button.click()
            print("\nClose button clicked")
            time.sleep(3)  # Wait for popup to close

            # Verify popup is closed
            print("\nVerifying popup is closed...")
            events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
            assert not events_popup.exists, "Events popup is still visible after clicking close button"
            print("Events popup successfully closed")
        else:
            print("\nNo events popup found, continuing with next steps...")
            time.sleep(10)


def test_events_card(d):
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

    # Click on Events carousel item
    print("\nLocating Events carousel item...")
    carousel_item = d.xpath(Events.CAROUSEL_ITEM)
    assert carousel_item.exists, "Could not find Events carousel item"
    print("Events carousel item found, clicking...")
    carousel_item.click()
    sleep(7)

    # Scroll until event details text is visible
    print("\nScrolling to find event details...")
    max_swipes = 5
    found = False
    for i in range(max_swipes):
        if d.xpath(Events.EVENT_DETAILS_TEXT).exists:
            found = True
            break
        d.swipe_ext("up", scale=0.8)
        sleep(1)
    
    assert found, "Could not find event details text after scrolling"
    print("Event details text found")

    # Take a screenshot of the event details
    print("\nTaking screenshot of event details...")
    d.screenshot("6_2_1_events_details.png")
    print("Screenshot saved as 6_2_1_events_details.png")

    # Check for More Info tab
    print("\nChecking for More Info tab...")
    more_info_tab = d.xpath(Events.EVENT_CARD_MORE_INFO_TAB)
    if more_info_tab.exists:
        print("More Info tab found, clicking...")
        more_info_tab.click()
        sleep(2)  # Wait for tab content to load
        print("More Info tab clicked")
        
        # Scroll to bottom of screen
        print("\nScrolling to bottom of screen...")
        max_swipes = 5
        last_screen = ""
        for i in range(max_swipes):
            current_screen = d.dump_hierarchy()
            if current_screen == last_screen:  # We've reached the bottom when screen doesn't change
                print(f"Reached bottom after {i+1} swipes")
                break
            last_screen = current_screen
            d.swipe_ext("up", scale=0.8)
            sleep(1)
            print(f"Swipe {i+1}/{max_swipes}")
        
        # Take screenshot of More Info contents
        print("\nTaking screenshot of More Info contents...")
        d.screenshot("6_2_2_more_info_contents.png")
        print("Screenshot saved as 6_2_2_more_info_contents.png")
    else:
        print("More Info tab not found, test complete")

    # Check for Add To Calendar button
    print("\nChecking for Add To Calendar button...")
    add_to_calendar = d.xpath(Events.ADD_TO_CALENDAR)
    assert add_to_calendar.exists, "Could not find Add To Calendar button"
    print("Add To Calendar button found")

    # Click Add To Calendar and capture screenshot
    print("Clicking Add To Calendar button...")
    add_to_calendar.click()
    sleep(2)  # Wait for calendar dialog to appear
    print("\nTaking screenshot of calendar dialog...")
    d.screenshot("6_2_3_add_to_calendar.png")
    print("Screenshot saved as 6_2_3_add_to_calendar_button_working.png")

    sleep(10)
