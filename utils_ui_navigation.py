"""
Utility functions for UI verification.
"""
from datetime import datetime
import os
from time import sleep
import time
from config import TEST_USER
import random
import string
from locators import Events, Businesses, HomeScreen, BottomNavBar, VisitHistory, DayTrips
from utils_scrolling import calculate_swipe_coordinates, get_screen_dimensions, get_target_position_in_first_quarter


# UI navigation functions for Events

def interact_with_events_carousel(d):
    """
    Locates and interacts with the Events carousel item.
    """
    print("\nLocating Events carousel item...")
    sleep(5)  # Wait for UI to load

    # Do one scroll first
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']
    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)
    d.swipe(start_x, start_y, start_x, end_y, duration=0.4)
    sleep(1.5)

    # First find any event element
    event_element = d.xpath('//android.view.ViewGroup[@content-desc]').get()
    if event_element:
        content_desc = event_element.attrib.get('content-desc')
        if content_desc:
            carousel_item = d.xpath(Events.CAROUSEL_ITEM.format(content_desc))
            assert carousel_item.exists, "Could not find Events carousel item"
            print("Events carousel item found, clicking...")
            carousel_item.click()
            sleep(7)
    else:
        assert False, "Could not find any event elements"


# UI navigation functions for Businesses
def click_business_fyi_tab(d):
    """
    Click on FYI tab and verify contents
    """
    # Verify FYI tab contents are present
    fyi_contents = d.xpath(Businesses.BUSINESS_FYI_TAB_CONTENTS)
    assert fyi_contents.exists, "FYI tab contents not found"


# UI navigation functions for View Map/Videos

def click_view_map(d):
    """
    Clicks the View Map button.

    :param d: The UIAutomator2 device instance.
    """
    print("\nClicking on View Map button...")
    view_map = d.xpath(HomeScreen.VIEW_MAP)
    assert view_map.exists, "Could not find View Map button"
    print("Found View Map button, clicking...")
    view_map.click()
    sleep(5)


# UI navigation functions for Day Trips/Trails

def find_day_trips_text(d):
    """
    Find the Day Trips text and Read More button on the Home screen.

    :param d: The device instance.
    :return: The Read More button element
    """

    # Get screen dimensions and target position
    width, height = get_screen_dimensions(d)
    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)
    target_y = get_target_position_in_first_quarter(d)

    max_attempts = 5
    for attempt in range(max_attempts):
        if d(text="Day Trips").exists:
            # Get the position of Day Trips text
            day_trips_elem = d(text="Day Trips")
            bounds = day_trips_elem.info['bounds']
            current_y = (bounds['top'] + bounds['bottom']) // 2

            if current_y <= target_y:
                print(f"\nDay Trips text found in correct position (y={current_y})")
                break

        print(f"\nAttempt {attempt + 1}: Scrolling for Day Trips text")
        d.swipe(start_x, start_y, start_x, end_y, duration=1.0)
        sleep(2)

    assert d(text="Day Trips").exists(timeout=5), "Day Trips text not found"

    # Now look for the Read More button within the Day Trips section
    read_more_button = d.xpath(DayTrips.DAY_TRIPS_READ_MORE_HOME_SCREEN)
    max_small_scrolls = 3

    for i in range(max_small_scrolls):
        if read_more_button.exists:
            break
        print(f"\nSmall scroll attempt {i + 1} for Read More button")
        d.swipe(start_x, start_y, start_x, end_y, duration=1.5)
        sleep(2)

    return read_more_button


def click_trails_button(d):
    """
    Finds and clicks the Trails button on the home screen.

    :param d: The device instance.
    """
    print("\nClicking on Trails button...")
    trails_button = d.xpath(HomeScreen.TRAILS_BUTTON)
    assert trails_button.wait(timeout=5), "Trails button not found"
    trails_button.click()
    sleep(2)


# UI navigation functions for Favorites/Visit History

def click_favorites_button(d):
    """
    Clicks the Favorites button in the bottom navigation bar.

    :param d: The UIAutomator2 device instance.
    """
    print("\nClicking on Favorites button...")
    favorites_button = d.xpath(BottomNavBar.FAVORITES)
    assert favorites_button.exists, "Could not find Favorites button"
    print("Found Favorites button, clicking...")
    favorites_button.click()
    sleep(2)  # Wait for favorites page to load

    # Verify that "Favorites" text is present
    assert d(text="Favorites").exists, "Favorites text not found on screen"


def click_visit_history(d):
    """
    Clicks the Visit History tab.

    :param d: The UIAutomator2 device instance.
    """
    print("\nClicking on Visit History tab...")
    visit_history_tab = d.xpath(VisitHistory.VISIT_HISTORY_TAB)
    assert visit_history_tab.exists, "Could not find Visit History tab"
    print("Found Visit History tab, clicking...")
    visit_history_tab.click()
    sleep(2)
