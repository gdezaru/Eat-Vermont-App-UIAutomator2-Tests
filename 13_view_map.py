import pytest
from time import sleep
from config import TEST_USER
from locators import HomeScreen, ViewMap, Events
from utils import handle_notification_permission


@pytest.mark.smoke
def test_view_map_filters(d):
    """Test the View Map filters"""
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

        # Single scroll to show View Map
        d.swipe(0.5, 0.8, 0.5, 0.4, 0.5)
        sleep(1)

        # Click "View Map" button
        view_map = d.xpath(HomeScreen.VIEW_MAP)
        assert view_map.exists, "Could not find View Map button"
        view_map.click()
        sleep(5)

        # Assert that Events filter is visible
        events_filter = d.xpath(ViewMap.EVENTS_FILTER)
        assert events_filter.exists, "Events filter is not visible on the map screen"

        # Assert that Food & Drinks filter is visible
        food_drinks_filter = d.xpath(ViewMap.FOOD_AND_DRINKS_FILTER)
        assert food_drinks_filter.exists, "Food & Drinks filter is not visible on the map screen"

        # Assert that Farms filter is visible
        farms_filter = d.xpath(ViewMap.FARMS_FILTER)
        assert farms_filter.exists, "Farms filter is not visible on the map screen"

        # Assert that Food Pantries filter is visible
        food_pantries_filter = d.xpath(ViewMap.FOOD_PANTRIES_FILTER)
        assert food_pantries_filter.exists, "Food Pantries filter is not visible on the map screen"

        # Take screenshot of all filters
        print("\nTook screenshot: 13_1_1_map_filters_present.png")
        d.screenshot("13_1_1_map_filters_present.png")

        # Click Events filter and take screenshot
        print("\nClicking Events filter...")
        events_filter.click()
        sleep(2)
        print("\nTook screenshot: 13_1_2_events_filter_active.png")
        d.screenshot("13_1_2_events_filter_active.png")

        # Click Food & Drinks filter and take screenshot
        print("\nClicking Food & Drinks filter...")
        food_drinks_filter.click()
        sleep(2)
        print("\nTook screenshot: 13_1_3_food_drinks_filter_active.png")
        d.screenshot("13_1_3_food_drinks_filter_active.png")

        # Click Farms filter and take screenshot
        print("\nClicking Farms filter...")
        farms_filter.click()
        sleep(2)
        print("\nTook screenshot: 13_1_4_farms_filter_active.png")
        d.screenshot("13_1_4_farms_filter_active.png")

        # Scroll right on filters header
        print("\nScrolling right on filters header...")
        filters_header = d.xpath(ViewMap.FILTERS_HEADER)
        assert filters_header.exists, "Could not find filters header"
        filters_header.swipe("left", steps=10)
        sleep(2)

        # Click Food Pantries filter and take screenshot
        print("\nClicking Food Pantries filter...")
        food_pantries_filter.click()
        sleep(2)
        print("\nTook screenshot: 13_1_5_food_pantries_filter_active.png")
        d.screenshot("13_1_5_food_pantries_filter_active.png")
