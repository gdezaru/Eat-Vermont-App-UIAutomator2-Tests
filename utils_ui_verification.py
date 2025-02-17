""""
Utilities functions for UI verification
"""
import os
from time import sleep
from locators import Businesses, EventsScreen, HomeScreen, HomeScreenTiles, SettingsScreen, Trails
from utils_screenshots import take_screenshot

attempt = 1


# UI verification functions for Events

def find_and_click_current_day(d):
    """
    Find and click on the current day element in the events calendar screen.
    Returns:
        str: The current day in three-letter format (e.g., 'MON', 'TUE')
    """
    # Find the current selected day
    days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    current_day = None
    for day in days:
        day_element = d.xpath(EventsScreen.DAY_OF_WEEK.format(day, day))
        if day_element.exists:
            current_day = day
            print(f"\nFound current day: {day}")
            day_element.click()
            sleep(2)
            break

    assert current_day is not None, "Could not find any day of week element"
    return current_day


def find_event_within_30(d):
    """
    Find an event tile within 30 minutes.
    """
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    event_found = False
    for day in days_of_week:
        events_tile = d.xpath(HomeScreenTiles.EVENTS_WITHIN_30_TILE.format(day))
        if events_tile.exists:
            event_found = True
            break

    assert event_found, "Could not find any events with dates in Events within 30 minutes section"
    sleep(1)


def find_event_further_than_30(d):
    """
    Find an event tile further than 30 minutes.
    
    Args:
        d: UIAutomator2 device instance
        
    Raises:
        AssertionError: If no events are found after maximum scroll attempts
    """
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    event_found = False
    max_scroll_attempts = 3
    
    print("\nSearching for events further than 30 minutes...")
    
    for attempt in range(max_scroll_attempts):
        print(f"\nScroll attempt {attempt + 1}/{max_scroll_attempts}")
        
        for day in days_of_week:
            events_tile = d.xpath(HomeScreenTiles.EVENTS_MORE_THAN_30_TILE.format(day))
            if events_tile.exists:
                event_found = True
                event_text = events_tile.get_text()
                print(f"\nFound event further than 30 minutes: {event_text}")
                break
        
        if event_found:
            break
            
        # If no event found, scroll down and try again
        print("\nNo events found, scrolling down to check more...")
        d.swipe(0.5, 0.8, 0.5, 0.2, 0.5)
        sleep(2)

    if not event_found:
        # Take screenshot for debugging if no events found
        d.screenshot("debug_no_events_further_than_30.png")
        
    assert event_found, "Could not find any events further than 30 minutes after multiple scroll attempts"
    sleep(1)


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
    Verifies if FYI tab is visible.
    """
    # Click on FYI tab and verify contents
    fyi_tab = d.xpath(Businesses.BUSINESS_FYI_TAB)
    assert fyi_tab.exists, "FYI tab not found"
    fyi_tab.click()
    sleep(2)


def verify_business_fyi_tab_contents(d):

    fyi_contents = d.xpath(Businesses.BUSINESS_FYI_TAB_CONTENTS)
    assert fyi_contents.exists, "FYI tab contents not found"


def verify_and_click_business_menu_tab(d):
    """
    Verifies if Menu tab is visible.
    """
    menu_tab = d.xpath(Businesses.BUSINESS_MENU_TAB)
    assert menu_tab.exists, "Menu tab not found on business details page"
    menu_tab.click()
    sleep(2)


def verify_business_menu_tab_contents(d):
    """
    Verifies the contents of the business Menu tab.
    """
    menu_contents = d.xpath(Businesses.BUSINESS_MENU_TAB_CONTENTS)
    assert menu_contents.exists, "Menu tab contents not found"


# UI verification functions for View Map


# UI verification functions for Day Trips/Trails


def verify_trails_percentage_progress(d):
    """
    Verifies the percentage progress in the Trails module.
    """
    percentage_element = d.xpath(Trails.PERCENTAGE_PROGRESS)
    assert percentage_element.wait(timeout=5), "Percentage progress not found"
    percentage_element.get_text()


def verify_trails_visits(d):
    """
    Verifies the completed number of visits and the text in the Trails Details Screen.
    """
    visits_text = d.xpath(Trails.VISITS_COMPLETED_TEXT)
    assert visits_text.wait(timeout=5), "Visits completed text not found"

    visits_number = d.xpath(Trails.VISITS_COMPLETED_NUMBER)
    assert visits_number.wait(timeout=5), "Visits completed number not found"
    visits = visits_number.get_text()


def verify_trail_status(d):
    """
    Verifies the Trails statuses in the list of trails screen.
    """
    status_element = d.xpath(Trails.TRAILS_STATUS)
    assert status_element.wait(timeout=5), "Trail status not found"
    current_status = status_element.get_text()
    assert current_status in ["Not Started", "In Progress", "Complete"], f"Unexpected trail status: {current_status}"
    sleep(1)


# UI verification functions for Favorites/Visit History


# UI verification functions for Videos


def verify_videos_text_exists(d, start_x, start_y, end_y):
    """
    Verify that the Videos text is present on the screen.
    """
    videos_text = d.xpath(HomeScreen.VIDEOS_TEXT_HOME_SCREEN)
    max_scroll_attempts = 9

    for _ in range(max_scroll_attempts):
        if videos_text.exists:
            break
        d.swipe(start_x, start_y, start_x, end_y, duration=0.9)
        sleep(1.5)

    assert videos_text.exists, "Videos section not found"
    sleep(1)


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


# UI verification for Settings

def verify_settings_options(d):
    """
    Asserts the settings options.
    """
    manage_account = d.xpath(SettingsScreen.MANAGE_ACCOUNT)
    assert manage_account.exists, "Manage Account option not found"

    edit_profile = d.xpath(SettingsScreen.EDIT_PROFILE)
    assert edit_profile.exists, "Edit Profile option not found"

    share_location = d.xpath(SettingsScreen.SHARE_MY_LOCATION)
    assert share_location.exists, "Share My Location option not found"

    log_out = d.xpath(SettingsScreen.LOG_OUT)
    assert log_out.exists, "Log out option not found"


def verify_settings_changed_name(d, new_name):
    """
    Verifies if the inputted name is visible in the main Settings screen.
    """
    name_text = d(text=new_name)
    assert name_text.exists(timeout=5), f"Updated name '{new_name}' is not visible after saving changes"


def verify_save_button_exists(d):
    """
    Verifies if the Save button is present in the Edit Profile screen.
    """
    save_button = d.xpath(SettingsScreen.EDIT_PROFILE_SAVE_BUTTON)
    assert save_button.exists, "Save button is not present after editing name"


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
