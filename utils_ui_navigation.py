"""
Utility functions for UI verification.
"""
from time import sleep
from locators import HomeScreen, Events, Businesses, MyFavorites, SearchModule, Trails, BottomNavBar, VisitHistory
from utils_scrolling import ScreenSwipe, GeneralScrolling


class NavEvents:
    """Class for handling events navigation and interactions."""

    # Wait times
    LONG_WAIT = 10
    MEDIUM_WAIT = 7
    DEFAULT_WAIT = 2
    SWIPE_DURATION = 0.4
    RETRY_WAIT = 1.5

    # Retry settings
    MAX_CLICK_RETRIES = 3
    CLICK_TIMEOUT = 3.0

    def __init__(self, device):
        """
        Initialize NavEvents with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_see_all_events_home_screen(self):
        """
        Clicks the "See All" button on the Events carousel on the Home screen.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If 'See all' button is not found
        """
        see_all_events = self.device.xpath(HomeScreen.EVENTS_SEE_ALL)
        assert see_all_events.exists, "Could not find 'See all' for events"

        see_all_events.click()
        sleep(self.LONG_WAIT)
        return True

    def click_see_all_events_within_30(self):
        """
        Clicks the "See All" button on the Events within 30 minutes section.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If See All button is not found
        """
        see_all = self.device(text="See All")
        assert see_all.exists, "Could not find See All button for Events within 30 minutes"

        see_all.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def click_see_all_events_further_than_30(self):
        """
        Clicks the "See All" button on the Events further than 30 minutes section.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If See All button is not found
        """
        see_all = self.device(text="See All")
        assert see_all.exists, "Could not find See All button for Events further than 30 minutes"

        see_all.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def interact_with_events_carousel(self):
        """
        Locates and interacts with the Events carousel item.

        Returns:
            bool: True if interaction was successful

        Raises:
            AssertionError: If carousel item is not found
        """
        print("\nLocating Events carousel item...")
        sleep(5)

        # Do one scroll first using ScreenSwipe
        screen_swipe = ScreenSwipe(self.device)
        screen_swipe.calculate_swipe_coordinates()
        sleep(self.RETRY_WAIT)

        event_element = self.device.xpath('//android.view.ViewGroup[@content-desc]').get()
        if event_element:
            content_desc = event_element.attrib.get('content-desc')
            if content_desc:
                carousel_item = self.device.xpath(Events.CAROUSEL_ITEM.format(content_desc))
                assert carousel_item.exists, "Could not find Events carousel item"
                print("Events carousel item found, clicking...")
                carousel_item.click()
                sleep(self.MEDIUM_WAIT)
                return True

        assert False, "Could not find any event elements"

    def events_add_to_calendar(self):
        """
        Attempts to click the add to calendar button in the events card.

        Returns:
            bool: True if button was found and clicked, False otherwise
        """
        add_to_calendar = self.device.xpath(Events.ADD_TO_CALENDAR)
        if add_to_calendar.exists:
            add_to_calendar.click()
            sleep(self.DEFAULT_WAIT)
            return True
        return False

    def click_first_event_search_result(self):
        """
        Clicks on the first event search result in the list.

        Returns:
            bool: True if click was successful

        Raises:
            AssertionError: If no search result is found or if click fails
        """
        result = self.device.xpath(SearchModule.FIRST_SEARCH_RESULT)
        assert result.exists, "Could not find any search results"

        for attempt in range(self.MAX_CLICK_RETRIES):
            if result.click_exists(timeout=self.CLICK_TIMEOUT):
                sleep(self.DEFAULT_WAIT)
                return True
            sleep(1)  # Short wait between retries

        raise AssertionError("Failed to click the search result after multiple attempts")

    def find_and_click_more_info_tab(self):
        """
        Attempts to find and click the More Info tab within the event card.

        Returns:
            bool: True if tab was found and clicked, False otherwise
        """
        more_info_tab = self.device.xpath(Events.EVENT_CARD_MORE_INFO_TAB)
        if more_info_tab.exists:
            more_info_tab.click()
            sleep(self.DEFAULT_WAIT)
            return True
        return False

    def add_favorite_event(self):
        """
        Clicks the favorite icon on an event card.

        Returns:
            bool: True if favorite was added successfully

        Raises:
            AssertionError: If favorite icon is not found
        """
        favorite_icon = self.device.xpath(MyFavorites.FAVORITE_EVENTS_ADD_REMOVE)
        assert favorite_icon.exists, "Could not find favorite icon"

        favorite_icon.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def verify_and_remove_favorite_event(self):
        """
        Verifies that an event has been added to favorites, then removes it.

        Returns:
            bool: True if favorite was verified and removed successfully

        Raises:
            AssertionError: If favorited event is not found or not removed successfully
        """
        favorite_event = self.device.xpath(MyFavorites.ADDED_FAVORITE_EVENT)
        assert favorite_event.exists, "Could not find favorited event"

        favorite_event.click()
        sleep(self.DEFAULT_WAIT)

        assert not favorite_event.exists, "Event is still present in favorites"
        return True


class NavBusinesses:
    """Class for handling business navigation and interactions."""

    # Wait times
    LONG_WAIT = 5
    DEFAULT_WAIT = 3
    SHORT_WAIT = 2

    # Default business names
    DEFAULT_EVENT_BUSINESS = "Higher Ground"
    DEFAULT_MENU_BUSINESS = "Big Fatty's BBQ"

    def __init__(self, device):
        """
        Initialize NavBusinesses with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_business_with_event_search_result(self, business_name=None):
        """
        Clicks on the business containing event search result.

        Args:
            business_name (str, optional): Name of the business to click.
                                         Defaults to "Higher Ground"

        Returns:
            bool: True if business was found and clicked

        Raises:
            AssertionError: If business is not found under Businesses section
        """
        business_name = business_name or self.DEFAULT_EVENT_BUSINESS
        search_result = self.device.xpath(Businesses.BUSINESS_UNDER_BUSINESSES.format(business_name))
        assert search_result.exists, f"{business_name} not found under Businesses section"

        search_result.click()
        sleep(self.LONG_WAIT)
        return True

    def click_business_with_menu_search_result(self, menu_business_name=None):
        """
        Clicks on the business containing menu search result.

        Args:
            menu_business_name (str, optional): Name of the business to click.
                                              Defaults to "Big Fatty's BBQ"

        Returns:
            bool: True if business was found and clicked

        Raises:
            AssertionError: If business is not found under Businesses section
        """
        menu_business_name = menu_business_name or self.DEFAULT_MENU_BUSINESS
        search_result = self.device.xpath(Businesses.BUSINESS_UNDER_BUSINESSES.format(menu_business_name))
        assert search_result.exists, f"{menu_business_name} not found under Businesses section"

        search_result.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def verify_business_fyi_tab(self):
        """
        Verify FYI tab contents are present.

        Returns:
            bool: True if FYI tab contents exist

        Raises:
            AssertionError: If FYI tab contents are not found
        """
        fyi_contents = self.device.xpath(Businesses.BUSINESS_FYI_TAB_CONTENTS)
        assert fyi_contents.exists, "FYI tab contents not found"
        return True

    def click_first_business_search_result(self, menu_business_name=None):
        """
        Clicks on the first business search result in the list.

        Args:
            menu_business_name (str, optional): The business card containing menu tab.
                                              Defaults to "Big Fatty's BBQ"

        Returns:
            bool: True if business was found and clicked

        Raises:
            AssertionError: If business is not found or if click fails
        """
        menu_business_name = menu_business_name or self.DEFAULT_MENU_BUSINESS
        search_result = self.device.xpath(Businesses.BUSINESS_UNDER_BUSINESSES.format(menu_business_name))
        assert search_result.exists, f"{menu_business_name} not found under Businesses section"

        search_result.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def add_favorite_business(self):
        """
        Clicks the favorite icon on a business card.

        Returns:
            bool: True if favorite was added successfully

        Raises:
            AssertionError: If favorite icon is not found
        """
        favorite_icon = self.device.xpath(MyFavorites.FAVORITE_BUSINESS_ADD_REMOVE)
        assert favorite_icon.exists, "Could not find favorite icon"

        favorite_icon.click()
        sleep(self.SHORT_WAIT)
        return True

    def verify_and_remove_favorite_business(self):
        """
        Verifies that a business has been added to favorites, then removes it.

        Returns:
            bool: True if favorite was verified and removed successfully

        Raises:
            AssertionError: If favorited business is not found or not removed successfully
        """
        favorite_business = self.device.xpath(MyFavorites.ADDED_FAVORITE_BUSINESS)
        assert favorite_business.exists, "Could not find favorited business"

        favorite_business.click()
        sleep(self.SHORT_WAIT)

        assert not favorite_business.exists, "Business is still present in favorites"
        return True
    sleep(3)


class NavViewMap:
    """Class for handling map view navigation."""

    NAVIGATION_WAIT = 5  # Default wait time after clicking View Map

    def __init__(self, device):
        """
        Initialize NavViewMap with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_view_map(self):
        """
        Clicks the View Map button and verifies navigation.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If View Map button is not found
        """
        view_map = self.device.xpath(HomeScreen.VIEW_MAP)
        assert view_map.exists, "Could not find View Map button"

        view_map.click()
        sleep(self.NAVIGATION_WAIT)

        return True


class NavDayTripsTrails:
    """Class for handling Trails section navigation and interactions."""

    # Class constants
    TRAIL_START_TEXT = "Start a Trail!"
    DAY_TRIPS_TEXT = "Day Trips"

    # Wait times
    DEFAULT_WAIT = 2
    LONG_WAIT = 5
    SHORT_WAIT = 1

    # Scroll settings
    MAX_SCROLL_ATTEMPTS = 5
    MAX_SMALL_SCROLLS = 3
    SCROLL_DURATION = 1.0
    LONG_SCROLL_DURATION = 1.5

    def __init__(self, device):
        """
        Initialize NavTrails with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_trails_see_all(self):
        """
        Clicks the "See All" button for the Trails section.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If Trails 'See all' button is not found
        """
        trails_see_all = self.device.xpath(HomeScreen.TRAILS_SEE_ALL.format(self.TRAIL_START_TEXT))
        assert trails_see_all.exists, "Could not find Trails 'See all' button"

        trails_see_all.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def find_trails_text(self):
        """
        Find the Trails text and Read More button on the Home screen.

        Returns:
            UIElement: The Read More button element if found

        Raises:
            AssertionError: If Start a Trail! text or Read More button is not found
        """
        # Initialize screen swipe for coordinates
        screen_swipe = ScreenSwipe(self.device)
        start_x, start_y, end_y = screen_swipe.calculate_swipe_coordinates()
        general_scroll = GeneralScrolling(self.device)
        target_y = general_scroll.get_target_position_in_first_quarter()

        for attempt in range(self.MAX_SCROLL_ATTEMPTS):
            if self.device(text=self.TRAIL_START_TEXT).exists:
                day_trips_elem = self.device(text=self.TRAIL_START_TEXT)
                bounds = day_trips_elem.info['bounds']
                current_y = (bounds['top'] + bounds['bottom']) // 2

                if current_y <= target_y:
                    break

            self.device.swipe(start_x, start_y, start_x, end_y, duration=self.SCROLL_DURATION)
            sleep(self.DEFAULT_WAIT)

        assert self.device(text=self.DAY_TRIPS_TEXT).exists(timeout=self.LONG_WAIT), (
            "Start a Trail! text not found"
        )

        # Find Read More button
        read_more_button = self.device.xpath(Trails.READ_MORE_TRAILS)

        for i in range(self.MAX_SMALL_SCROLLS):
            if read_more_button.exists:
                break
            self.device.swipe(start_x, start_y, start_x, end_y, duration=self.LONG_SCROLL_DURATION)
            sleep(self.DEFAULT_WAIT)

        return read_more_button

    def find_trail_name(self):
        """
        Finds the text of the first trail, then the first Trails name.

        Returns:
            str: The found trail text

        Raises:
            AssertionError: If trail element is not found
        """
        trail_text = self.device(textContains="Trail").get_text()
        trail_element = self.device.xpath(Trails.TRAIL_NAME.format(trail_text))
        assert trail_element.wait(timeout=self.LONG_WAIT), f"Trail element not found"
        sleep(self.SHORT_WAIT)
        return trail_text

    def click_trails_button(self):
        """
        Finds and clicks the Trails button on the home screen.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If Trails button is not found
        """
        trails_button = self.device.xpath(HomeScreen.TRAILS_BUTTON)
        assert trails_button.wait(timeout=self.LONG_WAIT), "Trails button not found"

        print("\nClicking Trails button")
        trails_button.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def click_trails_read_more(self):
        """
        Clicks the Read More button of a Trail.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If Read More button is not found
        """
        read_more_button = self.device.xpath(Trails.READ_MORE_TRAILS)
        assert read_more_button.wait(timeout=self.LONG_WAIT), "Read More button not found"

        read_more_button.click()
        sleep(self.LONG_WAIT)
        return True

    def add_favorite_trail(self):
        """
        Clicks the favorite icon on the trail details screen.

        Returns:
            bool: True if favorite was added successfully

        Raises:
            AssertionError: If favorite icon is not found
        """
        favorite_icon = self.device.xpath(MyFavorites.FAVORITE_TRAILS_ADD_REMOVE)
        assert favorite_icon.exists, "Could not find favorite icon"

        favorite_icon.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def verify_and_remove_favorite_trail(self):
        """
        Verifies that a trail has been added to favorites, then removes it.

        Returns:
            bool: True if favorite was verified and removed successfully

        Raises:
            AssertionError: If favorited trail is not found or not removed successfully
        """
        favorite_trail = self.device.xpath(MyFavorites.ADDED_FAVORITE_TRAIL)
        assert favorite_trail.exists, "Could not find favorited trail"

        favorite_trail.click()
        sleep(self.DEFAULT_WAIT)

        assert not favorite_trail.exists, "Trail is still present in favorites"
        sleep(self.LONG_WAIT)
        return True


class NavAddInfo:
    """Class for handling Add Info section navigation."""

    NAVIGATION_WAIT = 5  # Default wait time after clicking Add Info button

    def __init__(self, device):
        """
        Initialize NavAddInfo with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_add_info_button(self):
        """
        Clicks the Add Info button on the Home screen and verifies navigation.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If Add Info button is not found
        """
        add_info_button = self.device.xpath(HomeScreen.ADD_INFO_BUTTON)
        assert add_info_button.exists, "Could not find Add Info button"

        add_info_button.click()
        sleep(self.NAVIGATION_WAIT)

        return True


class NavVideos:
    """Class for handling videos section navigation."""

    MAX_SMALL_SCROLLS = 3
    SCROLL_DURATION = 1.0
    SCROLL_WAIT = 1.5
    CLICK_WAIT = 5

    # Screen position multipliers
    START_Y_MULTIPLIER = 0.6  # 60% of screen height
    END_Y_MULTIPLIER = 0.4  # 40% of screen height

    def __init__(self, device):
        """
        Initialize NavVideos with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def find_and_click_see_all_videos(self, height, start_x):
        """
        Find and click the "See All" button for the Videos section using fine-tuned scrolling.

        Args:
            height (int): The screen height
            start_x (int): The starting x-coordinate for the swipe

        Returns:
            bool: True if button was found and clicked

        Raises:
            AssertionError: If Videos See All button is not found after maximum scroll attempts
        """
        videos_see_all = self.device.xpath(HomeScreen.VIDEOS_SEE_ALL)

        # Calculate scroll coordinates using screen height multipliers
        fine_tune_start_y = int(height * self.START_Y_MULTIPLIER)
        fine_tune_end_y = int(height * self.END_Y_MULTIPLIER)

        # Perform fine-tuned scrolls
        for attempt in range(self.MAX_SMALL_SCROLLS):
            if videos_see_all.exists:
                break

            self.device.swipe(
                start_x,
                fine_tune_start_y,
                start_x,
                fine_tune_end_y,
                duration=self.SCROLL_DURATION
            )
            sleep(self.SCROLL_WAIT)

        assert videos_see_all.exists, "Could not find Videos See All button after maximum scroll attempts"

        videos_see_all.click()
        sleep(self.CLICK_WAIT)

        return True


class NavFavoritesVisitHistory:
    """Class for handling favorites and visit history navigation."""

    NAVIGATION_WAIT = 2  # Default wait time after navigation
    FAVORITES_TEXT = "Favorites"  # Text to verify on favorites screen

    def __init__(self, device):
        """
        Initialize NavFavoritesVisitHistory with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_favorites_button(self):
        """
        Clicks the Favorites button in the bottom navigation bar and verifies navigation.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If Favorites button is not found or navigation verification fails
        """
        favorites_button = self.device.xpath(BottomNavBar.FAVORITES)
        assert favorites_button.exists, "Could not find Favorites button"
        favorites_button.click()
        sleep(self.NAVIGATION_WAIT)

        # Verify navigation
        assert self.device(text=self.FAVORITES_TEXT).exists, (
            f"{self.FAVORITES_TEXT} text not found on screen"
        )
        return True

    def click_visit_history(self):
        """
        Clicks the Visit History tab.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If Visit History tab is not found
        """
        visit_history_tab = self.device.xpath(VisitHistory.VISIT_HISTORY_TAB)
        assert visit_history_tab.exists, "Could not find Visit History tab"
        visit_history_tab.click()
        sleep(self.NAVIGATION_WAIT)
        return True


# UI navigation functions for Bottom Navigation Bar

class NavBottomNavBar:
    """Class for handling bottom navigation bar interactions."""

    NAVIGATION_WAIT = 5  # Default wait time after navigation
    EVENTS_TEXT = "Events"  # Text to verify on screens

    def __init__(self, device):
        """
        Initialize NavBottomNavBar with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_home_button(self):
        """
        Clicks the Home button in the bottom navigation bar and verifies navigation.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If Home button is not found or navigation verification fails
        """
        home_button = self.device.xpath(BottomNavBar.NAV_HOME_BUTTON)
        assert home_button.exists, "Could not find Home button"

        home_button.click()
        sleep(self.NAVIGATION_WAIT)

        # Verify navigation
        assert self.device(text=self.EVENTS_TEXT).exists, (
            f"{self.EVENTS_TEXT} text not found on home screen"
        )
        return True

    def click_events_button(self):
        """
        Clicks the Events button in the bottom navigation bar and verifies navigation.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If Events button is not found or navigation verification fails
        """
        events_button = self.device.xpath(BottomNavBar.EVENTS)
        assert events_button.exists, "Could not find Events button"

        events_button.click()
        sleep(self.NAVIGATION_WAIT)

        # Verify navigation
        assert self.device(text=self.EVENTS_TEXT).exists, (
            f"{self.EVENTS_TEXT} text not found on screen"
        )
        return True


# UI navigation for Guest Mode

class NavGuestMode:
    """Class for handling guest mode navigation interactions."""

    # Default wait times after clicks
    EVENTS_WAIT = 2
    SEARCH_WAIT = 5
    FAVORITES_WAIT = 3

    def __init__(self, device):
        """
        Initialize NavGuestMode with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_events_button(self):
        """
        Clicks the Events button in the bottom navigation bar in Guest Mode.

        Returns:
            bool: True if click was successful

        Raises:
            AssertionError: If Events tab is not found
        """
        events_tab = self.device.xpath(BottomNavBar.EVENTS)
        assert events_tab.exists, "Events tab not found"

        events_tab.click()
        sleep(self.EVENTS_WAIT)
        return True

    def click_search(self):
        """
        Clicks the Search button in Guest Mode.

        Returns:
            bool: True if click was successful

        Raises:
            AssertionError: If Search button is not found
        """
        search_button = self.device.xpath(BottomNavBar.SEARCH)
        assert search_button.exists, "Search button not found"

        search_button.click()
        sleep(self.SEARCH_WAIT)
        return True

    def click_favorites(self):
        """
        Clicks the Favorites button in Guest Mode.

        Returns:
            bool: True if click was successful

        Raises:
            AssertionError: If Favorites button is not found
        """
        favorites_button = self.device.xpath(BottomNavBar.FAVORITES)
        assert favorites_button.exists, "Favorites button not found in bottom navigation"

        favorites_button.click()
        sleep(self.FAVORITES_WAIT)
        return True
