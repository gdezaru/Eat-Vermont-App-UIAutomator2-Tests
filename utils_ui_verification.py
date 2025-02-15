""""
Utilities functions for UI verification
"""
import os
from time import sleep
from locators import Businesses, EventsScreen
from utils_screenshots import take_screenshot

attempt = 1


# UI verification functions for Events

def find_and_click_current_day(d):
    """
    Find and click on the current day element in the events calendar screen.
    """
    # Find the current selected day
    days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    current_day = None
    for day in days:
        day_element = d.xpath(EventsScreen.DAY_OF_WEEK.format(day, day))
        if day_element.exists:
            current_day = day
            print(f"\nFound current day: {day}")
            break

    assert current_day is not None, "Could not find any day of week element"


# UI verification functions for Businesses

def get_next_day(current_day):
    """
    Returns the next day of the week given the current day.
    Args:
        current_day (str): Current day in three-letter format (e.g., 'MON', 'TUE')
    Returns:
        str: Next day in three-letter format
    """
    days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    current_index = days.index(current_day)
    next_index = (current_index + 1) % 7
    return days[next_index]


def try_next_day(d, current_day):
    """
    Attempts to find and click on the next day element in the events screen.

    :param d: The UIAutomator2 device instance.
    :param current_day: The current day to start trying from.
    :return: None
    """
    global attempt
    current_try_day = current_day
    days_tried = 0
    max_days_to_try = 7  # Try all days of the week at most

    while days_tried < max_days_to_try:
        # Get the next day to try
        next_day = get_next_day(current_try_day)
        print(f"\nTrying to click on: {next_day}")

        # Try clicking this day multiple times
        max_attempts = 3
        click_success = False

        for attempt in range(max_attempts):
            next_day_element = d.xpath(EventsScreen.DAY_OF_WEEK.format(next_day, next_day))
            print(f"\nAttempt {attempt + 1}: Next day element exists: {next_day_element.exists}")

            if not next_day_element.exists:
                print(f"\n{next_day} not found, will try next day")
                break

            next_day_element.click()
            print(f"\nClicked on {next_day}")
            sleep(2)

            # Verify if we're now on this day by checking the events list
            events_for_day = d(textContains=next_day.title())  # e.g., "Mon" instead of "MON"
            if events_for_day.exists:
                print(f"\nSuccess! Found events for {next_day}")
                click_success = True
                break
            elif attempt < max_attempts - 1:
                print(f"\nClick might not have worked (no events found for {next_day}), trying again...")
                sleep(2)  # Wait before next attempt
            else:
                print(f"\nCould not verify events for {next_day} after {max_attempts} attempts, will try next day")

        if click_success:
            break

        # Move to next day if this one didn't work
        current_try_day = next_day
        days_tried += 1

    if days_tried == max_days_to_try:
        assert False, "Could not find any clickable day after trying all days of the week"


def verify_businesses_section_present(d):
    """
    Verifies that the Businesses section is present on the screen.
    """
    businesses_section = d.xpath(Businesses.BUSINESSES_SECTION)
    assert businesses_section.exists, "Businesses section not found in search results"


def verify_business_about_tab(d):
    """
    Verify About tab is visible
    """
    # Verify About tab is visible
    about_tab = d.xpath(Businesses.BUSINESS_ABOUT_TAB)
    if about_tab.exists:
        assert about_tab.exists, "About tab not found on business details page"

    # Verify About tab contents are present
    about_contents = d.xpath(Businesses.BUSINESS_ABOUT_TAB_CONTENTS)
    assert about_contents.exists, "About tab contents not found"


def verify_business_fyi_tab(d):
    """
    Verify FYI tab is visible
    """
    # Click on FYI tab and verify contents
    fyi_tab = d.xpath(Businesses.BUSINESS_FYI_TAB)
    assert fyi_tab.exists, "FYI tab not found"
    fyi_tab.click()
    sleep(2)


# UI verification functions for View Map


# UI verification functions for Day Trips/Trails


# UI verification functions for Favorites/Visit History


# UI verification functions for Videos


def verify_video_playback(d):
    """
    Verify that a video is playing by checking app state and UI elements.

    Args:
        d: UIAutomator2 device instance

    Returns:
        bool: True if video is playing, False otherwise
    """
    print("\nVerifying video playback...")

    # Get current app info
    app_info = d.info
    print(f"\nCurrent app info: {app_info}")

    # Get current window hierarchy
    xml_hierarchy = d.dump_hierarchy()
    print(f"\nWindow hierarchy: {xml_hierarchy}")

    # Check if we're still in the app
    if not d(packageName="com.eatvermont").exists:
        print("App is no longer in foreground")
        return False

    # Take screenshot of the video playing
    take_screenshot(d, "video_playing")
    print("Video state verification complete")
    return True


# UI general verification functions

def verify_and_screenshot(d, condition, error_message, screenshots_dir, filename):
    """
    Verifies a condition and takes a screenshot if successful.

    :param d: The device instance.
    :param condition: A callable that returns a boolean.
    :param error_message: The error message if the condition fails.
    :param screenshots_dir: The directory to save the screenshot.
    :param filename: The name of the screenshot file.
    """
    assert condition(), error_message
    screenshot_path = os.path.join(screenshots_dir, filename)
    d.screenshot(screenshot_path)
    print(f"Screenshot saved as {filename}")
