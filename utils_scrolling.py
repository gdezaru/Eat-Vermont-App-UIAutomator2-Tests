"""
Utility functions for scrolling.
"""
import os
from time import sleep

from conftest import screenshots_dir
from locators import EventsScreen, Events, GuestMode


def get_screen_dimensions(d):
    """
    Returns the screen width and height.

    :param d: The device instance.
    :return: A tuple containing (width, height)
    """
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']
    return width, height


def get_target_position_in_first_quarter(d):
    """
    Calculate the target position in the first quarter of the screen.

    :param d: The device instance.
    :return: The y-coordinate target position
    """
    width, height = get_screen_dimensions(d)
    return height // 4


def click_and_verify_element(d, element_locator, description):
    """
    Clicks an element and verifies its presence.

    :param d: The device instance.
    :param element_locator: The XPath locator for the element.
    :param description: A description of the element for logging.
    """
    print(f"\nClicking and verifying {description}...")
    element = d.xpath(element_locator)
    assert element.exists, f"{description} not found"
    element.click()
    print(f"{description} clicked and verified.")


def scroll_to_find_text(d, text, max_attempts=5):
    """
    Scroll the screen until text is found

    Args:
        d: UIAutomator2 device instance
        text: Text to find
        max_attempts: Maximum number of scroll attempts

    Returns:
        bool: True if text was found, False otherwise
    """
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']

    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)

    for _ in range(max_attempts):
        if d(text=text).exists:
            return True
        d.swipe(start_x, start_y, start_x, end_y, duration=0.8)
        sleep(1.5)

    return d(text=text).exists


def scroll_until_element_is_visible(d, locator, max_attempts=5):
    """
    Scroll the screen until the element with the given locator is visible

    Args:
        d: UIAutomator2 device instance
        locator: XPath locator string
        max_attempts: Maximum number of scroll attempts

    Returns:
        bool: True if element was found, False otherwise
    """
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']

    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)

    for _ in range(max_attempts):
        element = d.xpath(locator)
        if element.exists:
            return True
        d.swipe(start_x, start_y, start_x, end_y, duration=0.8)
        sleep(1.5)

    return d.xpath(locator).exists


def calculate_swipe_coordinates(width, height):
    """
    Calculates swipe coordinates for scrolling.

    :param width: Screen width.
    :param height: Screen height.
    :return: A tuple containing (start_x, start_y, end_y)
    """
    start_x = width // 2
    start_y = (height * 3) // 4
    end_y = height // 4
    return start_x, start_y, end_y


def scroll_to_bottom(d, scroll_times=3, duration=0.5):
    """
    Scrolls to the bottom of the results on the screen.

    :param d: The device instance.
    :param scroll_times: Number of times to scroll to ensure reaching the bottom.
    :param duration: Duration of each swipe.
    """
    screen_size = d.window_size()
    for _ in range(scroll_times):
        d.swipe(
            screen_size[0] * 0.5, screen_size[1] * 0.8,
            screen_size[0] * 0.5, screen_size[1] * 0.2,
            duration=duration
        )
        sleep(2)


def scroll_to_event_and_click(d, screenshots_dir, current_day=None):
    """
    Scroll to the first event in the calendar.
    """
    # Verify that either there's an event or "No Events" message is shown
    first_event = d.xpath(EventsScreen.EVENTS_SCREEN_TILE_1)
    no_events_message = d.xpath(EventsScreen.EVENTS_SCREEN_NO_EVENTS)

    assert first_event.exists or no_events_message.exists, "Neither events nor 'No Events' message found"

    # If no event was found initially, scroll to try to find one
    if not first_event.exists and not no_events_message.exists:
        max_scroll_attempts = 3
        found_event = False

        for scroll_attempt in range(max_scroll_attempts):
            # Scroll down
            d.swipe(0.5, 0.8, 0.5, 0.2, 0.5)  # Scroll from bottom to top
            sleep(2)  # Wait for scroll to complete

            # Check if we can now see an event
            first_event = d.xpath(EventsScreen.EVENTS_SCREEN_TILE_1)
            if first_event.exists:
                found_event = True
                # Take a screenshot after finding the event
                screenshot_path = os.path.join(screenshots_dir, f"3_1_3_home_screen_events_{current_day.lower()}"
                                                                f"_after_scroll.png")
                d.screenshot(screenshot_path)
                break

        if not found_event:
            assert no_events_message.exists, "No events found and 'No Events' message is not displayed"

    # Click on the first event tile if it exists
    if first_event.exists:
        # Get the event title before clicking
        event_title = first_event.get_text()

        # Click the event title and wait for details to load
        first_event.click()
        sleep(2)  # Wait for event details to load

        # Verify we're in the event details view by checking for the event title
        event_title_in_details = d.xpath(EventsScreen.EVENT_TITLE.format(event_title))
        assert event_title_in_details.exists, f"Failed to open event details for '{event_title}'"


def scroll_to_events_within_30(d):
    """
    Scroll to the events within 30 minutes and ensure the text is in the first quarter of the screen.

    Args:
        d: UIAutomator2 device instance
    Returns:
        bool: True if the text was found and positioned correctly, False otherwise
    """
    width, height = get_screen_dimensions(d)
    target_y = get_target_position_in_first_quarter(d)
    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)

    d(scrollable=True).scroll.to(text="Events Within ~30min")
    if not d(text="Events Within ~30min").exists(timeout=5):
        print("Warning: Events Within ~30min text not found")
        return False

    events_elem = d(text="Events Within ~30min")
    bounds = events_elem.info['bounds']
    current_y = (bounds['top'] + bounds['bottom']) // 2

    max_adjustment_attempts = 3
    for attempt in range(max_adjustment_attempts):
        if current_y <= target_y:
            break

        scroll_distance = (current_y - target_y) // 2
        d.swipe(start_x, start_y, start_x, start_y - scroll_distance, duration=0.5)
        sleep(1)

        bounds = events_elem.info['bounds']
        current_y = (bounds['top'] + bounds['bottom']) // 2

    sleep(1)
    return True


def scroll_to_events_further_than_30(d):
    """
    Scroll to the events further than 30 minutes and ensure the text is in the first quarter of the screen.

    Args:
        d: UIAutomator2 device instance
    Returns:
        bool: True if the text was found and positioned correctly, False otherwise
    """
    width, height = get_screen_dimensions(d)
    target_y = get_target_position_in_first_quarter(d)
    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)

    d(scrollable=True).scroll.to(text="Events Further Than ~30min")
    if not d(text="Events Further Than ~30min").exists(timeout=5):
        print("Warning: Events Further Than ~30min text not found")
        return False

    events_elem = d(text="Events Further Than ~30min")
    bounds = events_elem.info['bounds']
    current_y = (bounds['top'] + bounds['bottom']) // 2

    max_adjustment_attempts = 3
    for attempt in range(max_adjustment_attempts):
        if current_y <= target_y:
            break

        scroll_distance = (current_y - target_y) // 2
        d.swipe(start_x, start_y, start_x, start_y - scroll_distance, duration=0.5)
        sleep(1)

        bounds = events_elem.info['bounds']
        current_y = (bounds['top'] + bounds['bottom']) // 2

    sleep(1)
    return True


def scroll_event_card(d):
    """
    Attempts to scroll to the bottom of the event card to see its details.
    Returns True if event details were found, False otherwise.
    """
    max_swipes = 5
    found = False
    for i in range(max_swipes):
        if d.xpath(Events.EVENT_DETAILS_TEXT).exists:
            found = True
            break
        d.swipe_ext("up", scale=0.8)
        sleep(1)
    
    return found


def scroll_to_add_info(d):
    """
    Scroll to the Add Info button.
    """
    d(scrollable=True).scroll.to(text="Add Info")
    assert d(text="Add Info").exists(timeout=5), "Add Info button not found"
    sleep(1)


def guest_mode_scroll_to_videos(d):
    """
    Scrolls to videos section in Guest Mode.
    """
    width, height = get_screen_dimensions(d)
    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)
    locked_videos = d.xpath(GuestMode.GUEST_MODE_HOME_SCREEN_LOCKED_VIDEOS)
    max_scroll_attempts = 9
    for _ in range(max_scroll_attempts):
        if locked_videos.exists:
            break
        d.swipe(start_x, start_y, start_x, end_y, duration=0.9)
        sleep(1.5)
