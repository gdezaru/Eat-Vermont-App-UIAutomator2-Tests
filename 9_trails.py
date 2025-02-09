import time
from time import sleep
from config import TEST_USER
from locators import Events, HomeScreen, Trails
from utils import handle_notification_permission


def test_trails_screen(d):
    """Test the Trails functionality"""
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

    # Click on Trails button
    print("\nClicking on Trails button...")
    trails_button = d.xpath(HomeScreen.TRAILS_BUTTON)
    assert trails_button.wait(timeout=5), "Trails button not found"
    trails_button.click()
    sleep(2)

    # Find and verify any trail name
    print("\nFinding trail name...")
    # First find any TextView containing "Trail" to get its text
    trail_text = d(textContains="Trail").get_text()
    print(f"Found trail: {trail_text}")
    
    # Now use that text with our TRAIL_NAME locator
    trail_element = d.xpath(Trails.TRAIL_NAME.format(trail_text))
    assert trail_element.wait(timeout=5), f"Trail element not found"
    sleep(1)

    # Verify trail status
    print("\nChecking trail status...")
    status_element = d.xpath(Trails.TRAILS_STATUS)
    assert status_element.wait(timeout=5), "Trail status not found"
    current_status = status_element.get_text()
    print(f"Trail status is: {current_status}")
    assert current_status in ["Not Started", "In Progress", "Complete"], f"Unexpected trail status: {current_status}"
    sleep(1)

    # Take screenshot of trails main screen
    print("\nTaking screenshot of trails main screen...")
    d.screenshot("9_1_1_trails_main_screen.png")
    sleep(1)


def test_trails_details(d):
    """Test the Trails details screen"""
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

    # Click on Trails button
    print("\nClicking on Trails button...")
    trails_button = d.xpath(HomeScreen.TRAILS_BUTTON)
    assert trails_button.wait(timeout=5), "Trails button not found"
    trails_button.click()
    sleep(2)

    # Click Read More button
    print("\nClicking Read More button...")
    read_more_button = d.xpath(Trails.READ_MORE_TRAILS)
    assert read_more_button.wait(timeout=5), "Read More button not found"
    read_more_button.click()
    sleep(5)  # Increased wait time

    # Verify percentage progress
    print("\nVerifying percentage progress...")
    percentage_element = d.xpath(Trails.PERCENTAGE_PROGRESS)
    assert percentage_element.wait(timeout=5), "Percentage progress not found"
    percentage = percentage_element.get_text()
    print(f"Trail progress: {percentage}")

    # Verify visits completed text and number
    print("\nVerifying visits completed...")
    visits_text = d.xpath(Trails.VISITS_COMPLETED_TEXT)
    assert visits_text.wait(timeout=5), "Visits completed text not found"
    
    visits_number = d.xpath(Trails.VISITS_COMPLETED_NUMBER)
    assert visits_number.wait(timeout=5), "Visits completed number not found"
    visits = visits_number.get_text()
    print(f"Visits completed: {visits}")

    # Take screenshot of trail details
    print("\nTaking screenshot of trail details...")
    d.screenshot("9_2_1_trail_details.png")
    sleep(1)

    # Scroll using swipe
    print("\nScrolling using swipe...")
    screen_size = d.window_size()
    start_x = screen_size[0] * 0.5
    start_y = screen_size[1] * 0.8  # Start from 80% of screen height
    end_y = screen_size[1] * 0.2    # End at 20% of screen height
    
    for _ in range(3):  # Do multiple swipes
        d.swipe(start_x, start_y, start_x, end_y, duration=0.5)
        sleep(1)

    print("\nTaking screenshot of trail details visits...")
    d.screenshot("9_2_2_trail_details_visits.png")
    sleep(1)
