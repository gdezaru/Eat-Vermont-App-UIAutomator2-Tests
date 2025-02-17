"""
Utility functions for UI verification.
"""
from time import sleep
from locators import Events, Businesses, HomeScreen, BottomNavBar, VisitHistory, DayTrips, SearchModule, Trails, \
    MyFavorites
from utils_scrolling import calculate_swipe_coordinates, get_screen_dimensions, get_target_position_in_first_quarter


# UI navigation functions for Events
def click_see_all_events_home_screen(d):
    """
    Clicks the "See All" button on the Events carousel on the Home screen.

    :param d: The UIAutomator2 device instance.
    """
    # Find and click 'See all' next to events
    see_all_events = d.xpath(HomeScreen.EVENTS_SEE_ALL)
    assert see_all_events.exists, "Could not find 'See all' for events"
    see_all_events.click()
    sleep(10)


def click_see_all_events_within_30(d):
    """
    Clicks the "See All" button on the Events within 30 minutes section on the Home screen.
    """
    see_all = d(text="See All")
    assert see_all.exists, "Could not find See All button for Events within 30 minutes"
    see_all.click()
    sleep(2)


def click_see_all_events_further_than_30(d):
    """
    Clicks the "See All" button on the Events further than 30 minutes section on the Home screen.
    """
    see_all = d(text="See All")
    assert see_all.exists, "Could not find See All button for Events within 30 minutes"
    see_all.click()
    sleep(2)


def interact_with_events_carousel(d):
    """
    Locates and interacts with the Events carousel item.
    """
    print("\nLocating Events carousel item...")
    sleep(5)

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


def events_add_to_calendar(d):
    """
    Attempts to click the add to calendar button in the events card if it exists.
    Returns True if button was found and clicked, False otherwise.
    """
    add_to_calendar = d.xpath(Events.ADD_TO_CALENDAR)
    if add_to_calendar.exists:
        add_to_calendar.click()
        sleep(2)
        return True
    return False


def click_first_event_search_result(d):
    """
    Clicks on the first event search result in the list.

    Args:
        d: UIAutomator2 device instance

    Raises:
        AssertionError: If no search result is found or if click fails
    """
    result = d.xpath(SearchModule.FIRST_SEARCH_RESULT)
    assert result.exists, "Could not find any search results"
    
    # Try to click with retries
    max_retries = 3
    for attempt in range(max_retries):
        if result.click_exists(timeout=3.0):
            break
        sleep(1)  # Short wait between retries
    else:
        raise AssertionError("Failed to click the search result after multiple attempts")
    
    sleep(2)


def find_and_click_more_info_tab(d):
    """
    Attempts to find and click the More Info tab within the event card.
    Returns True if tab was found and clicked, False otherwise.
    """
    more_info_tab = d.xpath(Events.EVENT_CARD_MORE_INFO_TAB)
    if more_info_tab.exists:
        more_info_tab.click()
        sleep(2)
        return True
    return False


def add_favorite_event(d):
    """
    Clicks the favorite icon on an event card.
    """
    favorite_icon = d.xpath(MyFavorites.FAVORITE_EVENTS_ADD_REMOVE)
    assert favorite_icon.exists, "Could not find favorite icon"
    favorite_icon.click()
    sleep(2)


def verify_and_remove_favorite_event(d):
    """
    Verifies that an event has been added to favorites, then removes it.
    """
    favorite_event = d.xpath(MyFavorites.ADDED_FAVORITE_EVENT)
    assert favorite_event.exists, "Could not find favorited event"
    favorite_event.click()
    sleep(2)
    assert not favorite_event.exists, "Event is still present in favorites"


# UI navigation functions for Businesses
def click_business_with_event_search_result(d, business_name):
    """
    Clicks on the business containing event search result.
    """
    search_result = d.xpath(Businesses.BUSINESS_UNDER_BUSINESSES.format(business_name))
    assert search_result.exists, "Higher Ground not found under Businesses section"
    search_result.click()
    sleep(5)


def click_business_with_menu_search_result(d, menu_business_name):
    """
    Clicks on the business containing menu search result.
    """
    search_result = d.xpath(Businesses.BUSINESS_UNDER_BUSINESSES.format(menu_business_name))
    assert search_result.exists, "Big Fatty's BBQ not found under Businesses section"
    search_result.click()
    sleep(3)


def click_business_fyi_tab(d):
    """
    Click on FYI tab and verify contents
    """
    # Verify FYI tab contents are present
    fyi_contents = d.xpath(Businesses.BUSINESS_FYI_TAB_CONTENTS)
    assert fyi_contents.exists, "FYI tab contents not found"


def click_first_business_search_result(d, menu_business_name):
    """
    Clicks on the first business search result in the list.

    Args:
        d: UIAutomator2 device instance
        menu_business_name: The business card containing menu tab.

    Raises:
        AssertionError: If no search result is found or if click fails
    """
    search_result = d.xpath(Businesses.BUSINESS_UNDER_BUSINESSES.format(menu_business_name))
    assert search_result.exists, "Big Fatty's BBQ not found under Businesses section"
    search_result.click()
    sleep(3)


def add_favorite_business(d):
    """
    Clicks the favorite icon on a business card.
    """
    favorite_icon = d.xpath(MyFavorites.FAVORITE_BUSINESS_ADD_REMOVE)
    assert favorite_icon.exists, "Could not find favorite icon"
    favorite_icon.click()
    sleep(2)


def verify_and_remove_favorite_business(d):
    """
    Verifies that a business has been added to favorites, then removes it.
    """
    # Verify favorited business is present and take screenshot
    favorite_business = d.xpath(MyFavorites.ADDED_FAVORITE_BUSINESS)
    assert favorite_business.exists, "Could not find favorited business"
    favorite_business.click()
    sleep(2)
    assert not favorite_business.exists, "Business is still present in favorites"
    sleep(3)


# UI navigation functions for View Map

def click_view_map(d):
    """
    Clicks the View Map button.

    :param d: The UIAutomator2 device instance.
    """
    view_map = d.xpath(HomeScreen.VIEW_MAP)
    assert view_map.exists, "Could not find View Map button"
    view_map.click()
    sleep(5)


# UI navigation functions for Day Trips

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
                break

        d.swipe(start_x, start_y, start_x, end_y, duration=1.0)
        sleep(2)

    assert d(text="Day Trips").exists(timeout=5), "Day Trips text not found"

    # Now look for the Read More button within the Day Trips section
    read_more_button = d.xpath(DayTrips.DAY_TRIPS_READ_MORE_HOME_SCREEN)
    max_small_scrolls = 3

    for i in range(max_small_scrolls):
        if read_more_button.exists:
            break
        d.swipe(start_x, start_y, start_x, end_y, duration=1.5)
        sleep(2)

    return read_more_button


def click_day_trips_see_all(d):
    """
    Clicks the "See All" button for the Day Trips section.

    :param d: The device instance.
    """
    day_trips_see_all = d.xpath(HomeScreen.DAY_TRIPS_SEE_ALL.format("Day Trip"))
    assert day_trips_see_all.exists, "Could not find Day Trip 'See all' button"
    day_trips_see_all.click()
    sleep(2)


def click_day_trips_read_more(d, read_more_button):
    """
    Clicks the Read More button of a Day Trip.
    """
    assert read_more_button.exists, "Read More button not found"
    read_more_button.click()
    sleep(5)


# UI navigation functions for Trails
def click_trails_see_all(d):
    """
    Clicks the "See All" button for the Day Trips section.

    :param d: The device instance.
    """
    trails_see_all = d.xpath(HomeScreen.TRAILS_SEE_ALL.format("Start a Trail!"))
    assert trails_see_all.exists, "Could not find Trails 'See all' button"
    trails_see_all.click()
    sleep(2)


def find_trails_text(d):
    """
    Find the Trails text and Read More button on the Home screen.

    :param d: The device instance.
    :return: The Read More button element
    """

    # Get screen dimensions and target position
    width, height = get_screen_dimensions(d)
    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)
    target_y = get_target_position_in_first_quarter(d)

    max_attempts = 5
    for attempt in range(max_attempts):
        if d(text="Start a Trail!").exists:
            # Get the position of Day Trips text
            day_trips_elem = d(text="Start a Trail!")
            bounds = day_trips_elem.info['bounds']
            current_y = (bounds['top'] + bounds['bottom']) // 2

            if current_y <= target_y:
                break

        d.swipe(start_x, start_y, start_x, end_y, duration=1.0)
        sleep(2)

    assert d(text="Day Trips").exists(timeout=5), "Start a Trail! text not found"

    # Now look for the Read More button within the Day Trips section
    read_more_button = d.xpath(Trails.READ_MORE_TRAILS)
    max_small_scrolls = 3

    for i in range(max_small_scrolls):
        if read_more_button.exists:
            break
        d.swipe(start_x, start_y, start_x, end_y, duration=1.5)
        sleep(2)

    return read_more_button


def find_trail_name(d):
    """
    Finds the text of the first trail, then the first Trails name.
    """
    trail_text = d(textContains="Trail").get_text()
    trail_element = d.xpath(Trails.TRAIL_NAME.format(trail_text))
    assert trail_element.wait(timeout=5), f"Trail element not found"
    sleep(1)


def click_trails_button(d):
    """
    Finds and clicks the Trails button on the home screen.

    :param d: The device instance.
    """
    trails_button = d.xpath(HomeScreen.TRAILS_BUTTON)
    assert trails_button.wait(timeout=5), "Trails button not found"
    trails_button.click()
    sleep(2)


def click_trails_read_more(d):
    """
    Clicks the Read More button of a Day Trip.
    """
    read_more_button = d.xpath(Trails.READ_MORE_TRAILS)
    assert read_more_button.wait(timeout=5), "Read More button not found"
    read_more_button.click()
    sleep(5)


def add_favorite_trail(d):
    """
    Clicks the favorite icon on the trail details screen.
    """
    favorite_icon = d.xpath(MyFavorites.FAVORITE_TRAILS_ADD_REMOVE)
    assert favorite_icon.exists, "Could not find favorite icon"
    favorite_icon.click()
    sleep(2)


def verify_and_remove_favorite_trail(d):
    """
    Verifies that a trail has been added to favorites, then removes it.
    """
    favorite_trail = d.xpath(MyFavorites.ADDED_FAVORITE_TRAIL)
    assert favorite_trail.exists, "Could not find favorited trail"
    favorite_trail.click()
    sleep(2)
    assert not favorite_trail.exists, "Trail is still present in favorites"
    sleep(5)


# UI navigation functions for Add Info

def click_add_info_button(d):
    """
    Clicks the Add Info button on the Home screen.

    :param d: The UIAutomator2 device instance.
    """
    add_info_button = d.xpath(HomeScreen.ADD_INFO_BUTTON)
    assert add_info_button.exists, "Could not find Add Info button"
    add_info_button.click()
    sleep(5)


# UI navigation functions for Videos

def find_and_click_see_all_videos(d, height, start_x):
    """
    Find and click the "See All" button for the Videos section.

    :param d: The UIAutomator2 device instance.
    :param height: The screen height.
    :param start_x: The starting x-coordinate for the swipe.
    """
    # Now do smaller scrolls to find See All
    max_small_scrolls = 3
    videos_see_all = d.xpath(HomeScreen.VIDEOS_SEE_ALL)

    # Smaller swipes for fine-tuning
    fine_tune_start_y = (height * 3) // 5  # Start from 60%
    fine_tune_end_y = (height * 2) // 5  # End at 40%

    for _ in range(max_small_scrolls):
        if videos_see_all.exists:
            break
        d.swipe(start_x, fine_tune_start_y, start_x, fine_tune_end_y, duration=1.0)
        sleep(1.5)

    assert videos_see_all.exists, "Could not find Videos See All button"
    videos_see_all.click()
    sleep(5)


# UI navigation functions for Favorites/Visit History

def click_favorites_button(d):
    """
    Clicks the Favorites button in the bottom navigation bar.

    :param d: The UIAutomator2 device instance.
    """
    favorites_button = d.xpath(BottomNavBar.FAVORITES)
    assert favorites_button.exists, "Could not find Favorites button"
    favorites_button.click()
    sleep(2)
    assert d(text="Favorites").exists, "Favorites text not found on screen"


def click_visit_history(d):
    """
    Clicks the Visit History tab.

    :param d: The UIAutomator2 device instance.
    """
    visit_history_tab = d.xpath(VisitHistory.VISIT_HISTORY_TAB)
    assert visit_history_tab.exists, "Could not find Visit History tab"
    visit_history_tab.click()
    sleep(2)


# UI navigation functions for Bottom Navigation Bar

def click_home_button(d):
    """
    Clicks the Home button in the bottom navigation bar.

    :param d: The UIAutomator2 device instance.
    """
    home_button = d.xpath(BottomNavBar.NAV_HOME_BUTTON)
    assert home_button.exists, "Could not find Home button"
    home_button.click()
    sleep(5)
    assert d(text="Events").exists, "Events text not found on home screen"


def click_events_button(d):
    """
    Clicks the Events button in the bottom navigation bar.

    :param d: The UIAutomator2 device instance.
    """
    events_button = d.xpath(BottomNavBar.EVENTS)
    assert events_button.exists, "Could not find Events button"
    events_button.click()
    sleep(5)
    assert d(text="Events").exists, "Events text not found on screen"
