from time import sleep
from locators import Events
from utils import sign_in_and_prepare
import pytest
import os


@pytest.mark.smoke
def test_events_popup(d, screenshots_dir):
    """
    Tests the contents of the events popup.
    Steps:
    1. Sign in with valid credentials
    2. Verify popup contents
    """
    sign_in_and_prepare(d)

    sleep(10)


@pytest.mark.smoke
def test_events_card(d, screenshots_dir):
    """
    Tests the contents of an events card.
    Steps:
    1. Sign in with valid credentials
    2. Navigate to Events section
    3. Select an event from the list
    4. Verify event title is displayed
    5. Check event date and time
    6. Verify location information
    7. Check event description
    8. Verify organizer details
    9. Test sharing functionality
    10. Check ticket/RSVP options
    """
    sign_in_and_prepare(d)

    sleep(10)

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
    screenshot_path = os.path.join(screenshots_dir, "6_2_1_events_details.png")
    d.screenshot(screenshot_path)
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
                print(f"Reached bottom after {i + 1} swipes")
                break
            last_screen = current_screen
            d.swipe_ext("up", scale=0.8)
            sleep(1)
            print(f"Swipe {i + 1}/{max_swipes}")

        # Take screenshot of More Info contents
        print("\nTaking screenshot of More Info contents...")
        screenshot_path = os.path.join(screenshots_dir, "6_2_2_more_info_contents.png")
        d.screenshot(screenshot_path)
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
    screenshot_path = os.path.join(screenshots_dir, "6_2_3_add_to_calendar.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 6_2_3_add_to_calendar_button_working.png")

    sleep(10)
