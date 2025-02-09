import time
from time import sleep
from config import TEST_USER
from locators import Businesses, Events
from utils import handle_notification_permission
import pytest

# Initialize business names at module level
business_name = "Higher Ground"
menu_business_name = "Big Fatty's BBQ"


@pytest.mark.smoke
def test_business_card_with_event(d):
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
    d.send_keys(business_name)
    sleep(1)
    d.press("enter")
    sleep(10)

    # Wait for and verify Businesses section is present
    print("\nVerifying Businesses section is present...")
    businesses_section = d.xpath(Businesses.BUSINESSES_SECTION)
    assert businesses_section.exists, "Businesses section not found in search results"
    print("Found Businesses section")

    # Click on Higher Ground search result under Businesses
    print("\nLocating Higher Ground under Businesses section...")
    search_result = d.xpath(Businesses.BUSINESS_UNDER_BUSINESSES.format(business_name))
    assert search_result.exists, "Higher Ground not found under Businesses section"
    print("Found Higher Ground, clicking...")
    search_result.click()
    sleep(3)  # Wait for business details to load

    # Verify About tab is visible
    print("\nVerifying About tab is visible...")
    about_tab = d.xpath(Businesses.BUSINESS_ABOUT_TAB)
    assert about_tab.exists, "About tab not found on business details page"
    print("About tab is visible")

    # Verify About tab contents are present
    print("\nVerifying About tab contents are present...")
    about_contents = d.xpath(Businesses.BUSINESS_ABOUT_TAB_CONTENTS)
    assert about_contents.exists, "About tab contents not found"
    print("About tab contents are present")

    # Take screenshot of business details with About tab
    print("\nTaking screenshot of business details with About tab...")
    d.screenshot("7_1_1_business_card_with_event_about_tab.png")
    print("Screenshot saved as 7_1_1_business_card_with_event_about_tab.png")

    # Click on FYI tab and verify contents
    print("\nLocating and clicking FYI tab...")
    fyi_tab = d.xpath(Businesses.BUSINESS_FYI_TAB)
    assert fyi_tab.exists, "FYI tab not found"
    fyi_tab.click()
    sleep(2)  # Wait for FYI contents to load
    print("FYI tab clicked")

    # Verify FYI tab contents are present
    print("\nVerifying FYI tab contents are present...")
    fyi_contents = d.xpath(Businesses.BUSINESS_FYI_TAB_CONTENTS)
    assert fyi_contents.exists, "FYI tab contents not found"
    print("FYI tab contents are present")

    # Take screenshot of FYI tab contents
    print("\nTaking screenshot of FYI tab contents...")
    d.screenshot("7_1_2_business_card_with_event_fyi_tab.png")
    print("Screenshot saved as 7_1_2_business_card_with_event_fyi_tab.png")


@pytest.mark.smoke
def test_business_card_with_menu(d):
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
        d.send_keys(menu_business_name)
        sleep(1)
        d.press("enter")
        sleep(10)

        # Wait for and verify Businesses section is present
        print("\nVerifying Businesses section is present...")
        businesses_section = d.xpath(Businesses.BUSINESSES_SECTION)
        assert businesses_section.exists, "Businesses section not found in search results"
        print("Found Businesses section")

        # Click on Big Fatty's BBQ search result under Businesses
        print("\nLocating Big Fatty's BBQ under Businesses section...")
        search_result = d.xpath(Businesses.BUSINESS_UNDER_BUSINESSES.format(menu_business_name))
        assert search_result.exists, "Big Fatty's BBQ not found under Businesses section"
        print("Found Big Fatty's BBQ, clicking...")
        search_result.click()
        sleep(3)  # Wait for business details to load

        # Verify About tab is visible
        print("\nVerifying About tab is visible...")
        about_tab = d.xpath(Businesses.BUSINESS_ABOUT_TAB)
        assert about_tab.exists, "About tab not found on business details page"
        print("About tab is visible")

        # Verify About tab contents are present
        print("\nVerifying About tab contents are present...")
        about_contents = d.xpath(Businesses.BUSINESS_ABOUT_TAB_CONTENTS)
        assert about_contents.exists, "About tab contents not found"
        print("About tab contents are present")

        # Take screenshot of business details with About tab
        print("\nTaking screenshot of business details with About tab...")
        d.screenshot("7_2_1_business_card_with_menu_about_tab.png")
        print("Screenshot saved as 7_2_1_business_card_with_menu_about_tab.png")

        # Verify Menu tab is visible
        print("\nVerifying Menu tab is visible...")
        menu_tab = d.xpath(Businesses.BUSINESS_MENU_TAB)
        assert menu_tab.exists, "Menu tab not found on business details page"
        print("Menu tab is visible")

        # Click on Menu tab
        menu_tab.click()
        sleep(2)  # Wait for menu contents to load

        # Verify Menu tab contents are present
        print("\nVerifying Menu tab contents are present...")
        menu_contents = d.xpath(Businesses.BUSINESS_MENU_TAB_CONTENTS)
        assert menu_contents.exists, "Menu tab contents not found"
        print("Menu tab contents are present")

        # Take screenshot of business details with Menu tab
        print("\nTaking screenshot of business details with Menu tab...")
        d.screenshot("7_2_1_business_card_with_menu_tab.png")
        print("Screenshot saved as 7_2_2_business_card_with_menu_tab.png")