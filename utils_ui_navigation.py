"""
Utility functions for UI verification.
"""
from time import sleep
from locators import HomeScreen, Events, Businesses, MyFavorites, SearchModule, Trails, BottomNavBar, VisitHistory, \
    ViewMap, DayTrips, LoginPage, AddInfo
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
        # Wait for search results to load
        sleep(self.MEDIUM_WAIT)

        result = self.device.xpath(SearchModule.FIRST_SEARCH_RESULT)
        assert result.exists, "Could not find any event search results"

        for attempt in range(self.MAX_CLICK_RETRIES):
            if result.click_exists(timeout=self.CLICK_TIMEOUT):
                sleep(self.LONG_WAIT)
                return True

            if attempt < self.MAX_CLICK_RETRIES - 1:
                sleep(self.RETRY_WAIT)

        raise AssertionError("Failed to click the event search result after multiple attempts")

    def click_out_of_events_details(self):
        """
        Clicks in the first quarter of the screen to exit event details.

        Returns:
            bool: True if click was successful
        """
        screen_swipe = ScreenSwipe(self.device)
        width, height = screen_swipe.get_dimensions()

        click_x = width // 4
        click_y = height // 4

        self.device.click(click_x, click_y)
        sleep(self.DEFAULT_WAIT)
        return True

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
            bool: True if favorite was added/removed successfully

        Raises:
            AssertionError: If favorite icon is not found or click fails
        """
        sleep(self.MEDIUM_WAIT)

        for attempt in range(self.MAX_CLICK_RETRIES):
            favorite_icon = self.device.xpath(MyFavorites.FAVORITE_EVENTS_ADD_REMOVE)
            if not favorite_icon.exists:
                if attempt < self.MAX_CLICK_RETRIES - 1:
                    sleep(self.RETRY_WAIT)
                    continue
                raise AssertionError("Could not find favorite icon")

            if favorite_icon.click_exists(timeout=self.CLICK_TIMEOUT):
                sleep(self.LONG_WAIT)
                return True

            if attempt < self.MAX_CLICK_RETRIES - 1:
                sleep(self.RETRY_WAIT)

        raise AssertionError("Could not click favorite icon after multiple attempts")

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
        # First verify the business exists in favorites
        sleep(self.DEFAULT_WAIT)
        favorite_business = self.device.xpath(MyFavorites.ADDED_FAVORITE_BUSINESS)
        assert favorite_business.exists, f"Could not find favorited business. Looking for: {self.DEFAULT_MENU_BUSINESS}"

        # Click the business to open its details
        favorite_business.click()
        sleep(self.LONG_WAIT)

        # Try to find the favorite button with retries
        max_retries = 3
        for i in range(max_retries):
            favorite_icon = self.device.xpath(MyFavorites.FAVORITE_BUSINESS_DETAILS_REMOVE)
            if favorite_icon.exists:
                favorite_icon.click()
                sleep(self.LONG_WAIT)
                break
            elif i < max_retries - 1:
                sleep(self.DEFAULT_WAIT)
        else:
            assert False, "Could not find favorite remove button after multiple attempts"

        # Go back to favorites list
        self.device.press("back")
        sleep(self.DEFAULT_WAIT)

        # Verify business is removed from favorites
        favorite_business = self.device.xpath(MyFavorites.ADDED_FAVORITE_BUSINESS)
        assert not favorite_business.exists, "Business is still present in favorites"
        return True

    def click_back_from_business_details(self):
        """
        Clicks the back button from business details view.

        Returns:
            bool: True if back button was clicked successfully

        Raises:
            AssertionError: If back button is not found
        """
        back_button = self.device.xpath(Businesses.BUSINESSES_BACK_BUTTON)
        assert back_button.exists, "Could not find back button in business details"
        back_button.click()
        sleep(self.DEFAULT_WAIT)
        return True


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

    def navigate_to_view_map(self):
        """
        Navigate to View Map section by scrolling and clicking.
        Uses multiple scroll attempts and better error handling.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If View Map button is not found after all attempts
        """
        max_scroll_attempts = 3
        for attempt in range(max_scroll_attempts):
            view_map = self.device.xpath(HomeScreen.VIEW_MAP)
            if view_map.exists:
                return self.click_view_map()

            self.device.swipe(0.5, 0.8, 0.5, 0.2, 0.5)
            sleep(1.5)

        view_map = self.device.xpath(HomeScreen.VIEW_MAP)
        assert view_map.exists, f"Could not find View Map button after {max_scroll_attempts} scroll attempts"
        return self.click_view_map()

    def click_events_filter(self):
        """
        Click Events filter on map.

        Returns:
            bool: True if click was successful

        Raises:
            AssertionError: If Events filter is not found
        """
        events_filter = self.device.xpath(ViewMap.EVENTS_FILTER)
        assert events_filter.exists, "Events filter is not visible on the map screen"
        events_filter.click()
        sleep(1)
        return True

    def click_food_drinks_filter(self):
        """
        Click Food & Drinks filter on map.

        Returns:
            bool: True if click was successful

        Raises:
            AssertionError: If Food & Drinks filter is not found
        """
        food_drinks_filter = self.device.xpath(ViewMap.FOOD_AND_DRINKS_FILTER)
        assert food_drinks_filter.exists, "Food & Drinks filter is not visible on the map screen"
        food_drinks_filter.click()
        sleep(1)
        return True

    def click_farms_filter(self):
        """
        Click Farms filter on map.

        Returns:
            bool: True if click was successful

        Raises:
            AssertionError: If Farms filter is not found
        """
        farms_filter = self.device.xpath(ViewMap.FARMS_FILTER)
        assert farms_filter.exists, "Farms filter is not visible on the map screen"
        farms_filter.click()
        sleep(1)
        return True

    def click_food_pantries_filter(self):
        """
        Click Food Pantries filter on map.

        Returns:
            bool: True if click was successful

        Raises:
            AssertionError: If Food Pantries filter is not found
        """
        food_pantries_filter = self.device.xpath(ViewMap.FOOD_PANTRIES_FILTER)
        assert food_pantries_filter.exists, "Food Pantries filter is not visible on the map screen"
        food_pantries_filter.click()
        sleep(1)
        return True


class AddInfoActions:
    """Class for handling Add Info actions"""

    def __init__(self, device):
        """
        Initialize AddInfoActions with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def input_business_name(self, text):
        """
        Click business name field and input text.

        Args:
            text: Text to input in the business name field

        Returns:
            bool: True if text was input successfully

        Raises:
            AssertionError: If business name field is not found
        """
        business_name_field = self.device.xpath(AddInfo.BUSINESS_NAME)
        assert business_name_field.exists, "Business name field not found"
        business_name_field.click()
        self.device.send_keys(text)
        return True

    def input_update_info(self, text):
        """
        Click update info field and input text.

        Args:
            text: Text to input in the update info field

        Returns:
            bool: True if text was input successfully

        Raises:
            AssertionError: If update info field is not found
        """
        update_info_field = self.device.xpath(AddInfo.ADD_UPDATE_INFO_FIELD)
        assert update_info_field.exists, "Update info field not found"
        update_info_field.click()
        self.device.send_keys(text)
        return True

    def click_submit_button(self, wait_time=3):
        """
        Click the submit button with multiple attempts and verify the Cheers confirmation.

        Args:
            wait_time: Time to wait for Cheers button to appear (default: 3 seconds)

        Returns:
            bool: True if button was clicked successfully and Cheers confirmation appeared

        Raises:
            AssertionError: If submit button is not found or if Cheers confirmation is not visible
        """
        self.device(text="Submit").click()
        sleep(wait_time)

        cheers_button = self.device.xpath(AddInfo.CHEERS_BUTTON)
        assert cheers_button.exists, "Cheers button not visible after submission"

        return True

    def click_cheers_button(self, wait_time=2):
        """
        Click the Cheers button and verify it disappears.

        Returns:
            bool: True if button was clicked and disappeared successfully

        Raises:
            AssertionError: If Cheers button is not found initially or if it remains visible after clicking
        """
        cheers_button = self.device.xpath(AddInfo.CHEERS_BUTTON)
        assert cheers_button.exists, "Cheers button not found"

        cheers_button.click()
        sleep(wait_time)

        assert not cheers_button.exists, "Cheers button still visible after clicking"

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

    def find_day_trips_text(self):
        """
        Find the Day Trips text and Read More button on the Home screen.

        Returns:
            UIElement: The Read More button element if found

        Raises:
            AssertionError: If Day Trips text or Read More button is not found
        """
        # Initialize screen swipe for coordinates
        screen_swipe = ScreenSwipe(self.device)
        start_x, start_y, end_y = screen_swipe.calculate_swipe_coordinates()
        general_scroll = GeneralScrolling(self.device)
        target_y = general_scroll.get_target_position_in_first_quarter()

        for attempt in range(self.MAX_SCROLL_ATTEMPTS):
            if self.device(text=self.DAY_TRIPS_TEXT).exists:
                day_trips_elem = self.device(text=self.DAY_TRIPS_TEXT)
                bounds = day_trips_elem.info['bounds']
                current_y = (bounds['top'] + bounds['bottom']) // 2

                if current_y <= target_y:
                    break

            self.device.swipe(start_x, start_y, start_x, end_y, duration=self.SCROLL_DURATION)
            sleep(self.DEFAULT_WAIT)

        assert self.device(text=self.DAY_TRIPS_TEXT).exists(timeout=self.LONG_WAIT), (
            "Day Trips text not found"
        )

        # Find Read More button
        read_more_button = self.device.xpath(DayTrips.DAY_TRIPS_READ_MORE_HOME_SCREEN)

        for i in range(self.MAX_SMALL_SCROLLS):
            if read_more_button.exists:
                break
            self.device.swipe(start_x, start_y, start_x, end_y, duration=self.LONG_SCROLL_DURATION)
            sleep(self.DEFAULT_WAIT)

        assert read_more_button.exists, "Could not find Read More button for Day Trips"
        return read_more_button


    def click_day_trips_see_all(self):
        """
        Clicks the "See All" button for the Day Trips section.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If Day Trips 'See all' button is not found
        """
        day_trips_see_all = self.device.xpath(HomeScreen.DAY_TRIPS_SEE_ALL)
        assert day_trips_see_all.exists, "Could not find Day Trips 'See all' button"

        day_trips_see_all.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def click_day_trips_read_more(self, read_more_button=None):
        """
        Clicks the Read More button of a Day Trip.

        Args:
            read_more_button (UIElement, optional): The Read More button element.
                                                If None, will try to find it.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If Read More button is not found
        """
        if read_more_button is None:
            read_more_button = self.find_day_trips_text()

        read_more_button.click()
        sleep(self.DEFAULT_WAIT)
        return True

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

    CLICK_WAIT = 5

    def __init__(self, device):
        """
        Initialize NavVideos with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def find_and_click_see_all_videos(self):
        """
        Find and click the "See All" button for the Videos section.
        The screen should already be scrolled to where the videos section is visible.

        Returns:
            bool: True if button was found and clicked

        Raises:
            AssertionError: If Videos See All button is not found
        """
        videos_see_all = self.device.xpath(HomeScreen.VIDEOS_SEE_ALL)
        assert videos_see_all.exists, "Could not find Videos See All button"

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


class NavForgotPassword:
    """Class for handling forgot password navigation interactions."""

    RESET_WAIT = 5

    def __init__(self, device):
        """
        Initialize NavForgotPassword with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_reset_password(self):
        """
        Click the Reset Password button and wait for navigation.

        Returns:
            bool: True if button was found and clicked

        Raises:
            AssertionError: If Reset Password button is not found
        """
        reset_button = self.device.xpath(LoginPage.RESET_PASSWORD_BUTTON)
        assert reset_button.wait(timeout=5), "Reset Password button not found"

        reset_button.click()
        sleep(self.RESET_WAIT)

        return True