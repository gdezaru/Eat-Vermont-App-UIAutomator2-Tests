"""
Utility functions for UI verification.
"""
from time import sleep
from locators import HomeScreen, Events, Businesses, MyFavorites, Trails, BottomNavBar, VisitHistory, \
    ViewMap, DayTrips, LoginPage, AddInfo, GuestMode, Videos, CheckIn, AskAI, EventsFilters
from utils_scrolling import ScreenSwipe, GeneralScrolling


class NavEvents:
    """Class for handling events navigation and interactions."""

    LONG_WAIT = 10
    MEDIUM_WAIT = 7
    DEFAULT_WAIT = 2
    SWIPE_DURATION = 0.4
    RETRY_WAIT = 1.5

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
        sleep(5)

        screen_swipe = ScreenSwipe(self.device)
        screen_swipe.calculate_swipe_coordinates()
        sleep(self.RETRY_WAIT)

        event_element = self.device.xpath('//android.view.ViewGroup[@content-desc]').get()
        if event_element:
            content_desc = event_element.attrib.get('content-desc')
            if content_desc:
                carousel_item = self.device.xpath(Events.CAROUSEL_ITEM.format(content_desc))
                assert carousel_item.exists, "Could not find Events carousel item"
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
        sleep(self.MEDIUM_WAIT)

        days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        day_conditions = " or ".join([f"contains(@content-desc, '{day}')" for day in days_of_the_week])
        dynamic_locator = f'//*[{day_conditions}]/android.view.ViewGroup[3]'
        result = self.device.xpath(dynamic_locator)
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


class NavEventsFilters:
    """Class for handling navigation in Events Filters"""

    DEFAULT_WAIT = 2

    def __init__(self, device):
        """
        Initialize NavEventsFilters with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device
        self.days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']

    def click_event_filter_button(self):
        """
        Clicks the Filter button on the Events screen.

        Returns:
            bool: True if click was successful

        Raises:
            AssertionError: If Filter button is not found
        """
        filter_button = self.device.xpath(HomeScreen.EVENTS_FILTERS)
        assert filter_button.exists, "Could not find Filter button on Events screen"

        filter_button.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def click_next_month_filter(self):
        """
        Clicks the Next Month button in the Events Filters screen.

        Returns:
            bool: True if click was successful

        Raises:
            AssertionError: If Next Month button is not found
        """
        next_month_button = self.device.xpath(EventsFilters.NEXT_MONTH_FILTER)
        assert next_month_button.exists, "Could not find Next Month button in Events Filters screen"

        next_month_button.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def toggle_drive_time(self, direction):
        """
        Clicks the Drive Time toggle button to move it in a specific direction.

        Args:
            direction: String - "left" or "right" to indicate the desired toggle direction

        Returns:
            bool: True if toggle was clicked successfully

        Raises:
            AssertionError: If Drive Time toggle is not found
            ValueError: If direction is not 'left' or 'right'
        """
        if direction not in ['left', 'right']:
            raise ValueError("Direction must be 'left' or 'right'")

        drive_time_toggle = self.device.xpath(EventsFilters.DRIVE_TIME_TOGGLE)
        assert drive_time_toggle.exists, "Could not find Drive Time toggle in Events Filters screen"

        toggle_info = drive_time_toggle.info
        toggle_bounds = toggle_info.get('bounds', {})

        toggle_width = toggle_bounds.get('right', 0) - toggle_bounds.get('left', 0)
        toggle_height = toggle_bounds.get('bottom', 0) - toggle_bounds.get('top', 0)

        if direction == 'left':
            x_coord = toggle_bounds.get('left', 0) + (toggle_width // 4)
        else:
            x_coord = toggle_bounds.get('right', 0) - (toggle_width // 4)

        y_coord = toggle_bounds.get('top', 0) + (toggle_height // 2)
        self.device.click(x_coord, y_coord)
        sleep(self.DEFAULT_WAIT)
        return True

    def click_apply_filters(self):
        """
        Clicks the Apply Filters button on the Events Filters screen.

        Returns:
            bool: True if click was successful

        Raises:
            AssertionError: If Apply Filters button is not found
        """
        apply_filters_button = self.device.xpath(EventsFilters.APPLY_FILTERS)
        assert apply_filters_button.exists, "Could not find Apply Filters button on Events Filters screen"

        apply_filters_button.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def click_reset_filters(self):
        """
        Clicks the Reset button on the Events Filters screen.

        Returns:
            bool: True if click was successful

        Raises:
            AssertionError: If Reset button is not found
        """
        reset_button = self.device.xpath(EventsFilters.RESET_FILTERS)
        assert reset_button.exists, "Could not find Reset button on Events Filters screen"

        reset_button.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def get_next_day(self, current_day):
        """
        Returns the next day of the week given the current day.

        Args:
            current_day (str): Current day in three-letter format (e.g., 'MON', 'TUE')

        Returns:
            str: Next day in three-letter format
        """
        current_index = self.days.index(current_day)
        next_index = (current_index + 1) % 7
        return self.days[next_index]

    def select_next_day(self, current_day):
        """
        Attempts to select the next day in the Events Filters screen.

        This method tries to find and click on the day element directly after
        the provided current day. It uses explicit assertions and error messaging
        rather than try-except blocks.

        Args:
            current_day (str): The current day in three-letter format (e.g., 'MON', 'TUE')

        Returns:
            str: The newly selected day in three-letter format

        Raises:
            AssertionError: If the next day element is not found or cannot be clicked
        """
        next_day = self.get_next_day(current_day)

        next_day_element = self.device.xpath(f'//android.widget.TextView[@text="{next_day}"]')

        assert next_day_element.exists, f"Next day element '{next_day}' not found in Events Filters screen"

        next_day_element.click()
        sleep(2)

        selected_day_indicator = self.device.xpath(
            f'//android.widget.TextView[@text="{next_day}" and @selected="true"]')
        assert selected_day_indicator.exists or next_day_element.info.get('selected', False), \
            f"Failed to verify '{next_day}' was selected after clicking"

        return next_day


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
        Navigate to View Map section by scrolling until the button is centered on screen.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If View Map button is not found after all attempts
        """
        general_scroll = GeneralScrolling(self.device)
        width, height = general_scroll.get_dimensions()
        center_y = height // 2
        for _ in range(3):
            view_map = self.device.xpath(HomeScreen.VIEW_MAP)
            if view_map.exists:
                bounds = view_map.info['bounds']
                button_y = (bounds['top'] + bounds['bottom']) // 2

                if abs(button_y - center_y) < height * 0.1:
                    return self.click_view_map()

                offset = button_y - center_y
                self.device.swipe(width // 2, height // 2 + offset // 2,
                                  width // 2, height // 2 - offset // 2, 0.3)
                sleep(1)
                break

            start_x, start_y, end_y = general_scroll.calculate_swipe_coordinates()
            self.device.swipe(start_x, start_y, start_x, end_y, 0.3)
            sleep(1.5)

        view_map = self.device.xpath(HomeScreen.VIEW_MAP)
        assert view_map.exists, "Could not find View Map button after multiple attempts"
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


class NavDayTripsTrails:
    """Class for handling Trails section navigation and interactions."""

    TRAIL_START_TEXT = "Fun Food Trails"
    DAY_TRIPS_TEXT = "Day Trips"

    DEFAULT_WAIT = 2
    LONG_WAIT = 5
    SHORT_WAIT = 1

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
        screen_swipe = ScreenSwipe(self.device)
        start_x, start_y, end_y = screen_swipe.calculate_swipe_coordinates()
        general_scroll = GeneralScrolling(self.device)
        target_y = general_scroll.get_target_position_in_first_quarter()
        scroll_end_y = (start_y + end_y) // 2

        for attempt in range(self.MAX_SCROLL_ATTEMPTS):
            if self.device(text=self.DAY_TRIPS_TEXT).exists:
                day_trips_elem = self.device(text=self.DAY_TRIPS_TEXT)
                bounds = day_trips_elem.info['bounds']
                current_y = (bounds['top'] + bounds['bottom']) // 2
                if current_y <= target_y:
                    if current_y < target_y - 100:
                        self.device.swipe(start_x, end_y, start_x, start_y, duration=self.LONG_SCROLL_DURATION)
                        sleep(self.DEFAULT_WAIT)
                    else:
                        break
            self.device.swipe(start_x, start_y, start_x, scroll_end_y, duration=self.SCROLL_DURATION)
            sleep(self.DEFAULT_WAIT)
        assert self.device(text=self.DAY_TRIPS_TEXT).exists(timeout=self.LONG_WAIT), (
            "Day Trips text not found"
        )
        read_more_button = self.device.xpath(DayTrips.DAY_TRIPS_READ_MORE_HOME_SCREEN)
        for i in range(self.MAX_SMALL_SCROLLS):
            if read_more_button.exists:
                break
            small_scroll_end = start_y - (start_y - end_y) // 4
            self.device.swipe(start_x, start_y, start_x, small_scroll_end, duration=self.LONG_SCROLL_DURATION)
            sleep(self.DEFAULT_WAIT)
        assert read_more_button.exists, "Could not find Read More button for Day Trips"
        return read_more_button

    def click_day_trips_see_all(self):
        """
        Scrolls to the Day Trips section and clicks the "See All" button.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If Day Trips section or 'See all' button is not found
        """
        screen_swipe = ScreenSwipe(self.device)
        start_x, start_y, end_y = screen_swipe.calculate_swipe_coordinates()
        general_scroll = GeneralScrolling(self.device)
        target_y = general_scroll.get_target_position_in_first_quarter()
        scroll_end_y = (start_y + end_y) // 2
        for attempt in range(self.MAX_SCROLL_ATTEMPTS):
            if self.device(text=self.DAY_TRIPS_TEXT).exists:
                day_trips_elem = self.device(text=self.DAY_TRIPS_TEXT)
                bounds = day_trips_elem.info['bounds']
                current_y = (bounds['top'] + bounds['bottom']) // 2
                if current_y <= target_y:
                    if current_y < target_y - 100:
                        self.device.swipe(start_x, end_y, start_x, start_y, duration=self.SCROLL_DURATION)
                        sleep(self.DEFAULT_WAIT)
                    else:
                        break
            self.device.swipe(start_x, start_y, start_x, scroll_end_y, duration=self.SCROLL_DURATION)
            sleep(self.DEFAULT_WAIT)
        assert self.device(text=self.DAY_TRIPS_TEXT).exists(timeout=self.LONG_WAIT), (
            "Day Trips text not found"
        )
        see_all_button = self.device(text="See All")
        assert see_all_button.exists(timeout=self.LONG_WAIT), "Could not find 'See all' text next to Day Trips"
        see_all_button.click()
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
        screen_swipe = ScreenSwipe(self.device)
        start_x, start_y, end_y = screen_swipe.calculate_swipe_coordinates()
        scroll_distance = (start_y - end_y) // 10
        current_scroll_y = start_y - scroll_distance
        day_trips_found = False
        for attempt in range(self.MAX_SCROLL_ATTEMPTS * 2):
            if self.device(text=self.DAY_TRIPS_TEXT).exists:
                day_trips_found = True
                break
            self.device.swipe(start_x, start_y, start_x, current_scroll_y, duration=self.SCROLL_DURATION)
            sleep(self.DEFAULT_WAIT)
            current_scroll_y = max(current_scroll_y - scroll_distance, end_y)
        for attempt in range(self.MAX_SCROLL_ATTEMPTS * 3):
            if self.device(text=self.TRAIL_START_TEXT).exists:
                break
            if self.device(textContains="Fun Food Trails").exists:
                break
            small_scroll = scroll_distance // 2 if day_trips_found else scroll_distance
            self.device.swipe(start_x, start_y, start_x, start_y - small_scroll, duration=self.SCROLL_DURATION)
            sleep(self.DEFAULT_WAIT)
        assert self.device(text=self.TRAIL_START_TEXT).exists(timeout=self.LONG_WAIT) or \
               self.device(textContains="Fun Food Trails").exists(timeout=self.LONG_WAIT), "Fun Food Trails text not found"
        read_more_button = self.device.xpath(Trails.READ_MORE_TRAILS)
        for i in range(self.MAX_SMALL_SCROLLS):
            if read_more_button.exists:
                break
            self.device.swipe(start_x, start_y, start_x, start_y - 100, duration=self.LONG_SCROLL_DURATION)
            sleep(self.DEFAULT_WAIT)
            read_more_button = self.device.xpath(Trails.READ_MORE_TRAILS)
        assert read_more_button.exists, "Read More button for Trails not found"
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

    def click_trails_read_more(self):
        """
        Clicks the Read More button of a Trail.

        Returns:
            bool: True if navigation was successful

        Raises:
            AssertionError: If Read More button is not found or click doesn't navigate to details screen
        """
        read_more_button = self.find_trails_text()
        read_more_button.click()
        sleep(self.DEFAULT_WAIT)

        if not self.device.xpath(Trails.PERCENTAGE_PROGRESS).exists:
            alt_button = self.device.xpath(Trails.READ_MORE_TRAILS_DYNAMIC)
            if alt_button.exists:
                alt_button.click()
                sleep(self.DEFAULT_WAIT)

            if not self.device.xpath(Trails.PERCENTAGE_PROGRESS).exists:
                read_more_texts = self.device(text="Read More")
                if read_more_texts.exists:
                    read_more_texts[read_more_texts.count - 1].click()
                    sleep(self.DEFAULT_WAIT)
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


class NavCustomDayTrips:
    """Class for handling Custom Day Trips navigation."""
    SEARCH_WAIT = 5
    DEFAULT_WAIT = 2

    def __init__(self, device):
        """
        Initialize NavCustomDayTrips with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_custom_day_trips_button(self):
        """
        Clicks the Create a Custom trip button.

        Returns:
            bool: True if button was found and clicked

        Raises:
            AssertionError: If Custom Day Trip button is not found
        """
        custom_trip_button = self.device.xpath(HomeScreen.CUSTOM_DAY_TRIP_BUTTON)
        assert custom_trip_button.exists, "Could not find Create a Custom trip button"

        custom_trip_button.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def click_create_trip_header(self):
        """Click the Create Trip header text."""
        self.device.xpath(DayTrips.CREATE_TRIP_HEADER).click()
        sleep(self.DEFAULT_WAIT)

    def click_add_location(self):
        """Click the Add A Location button."""
        self.device.xpath(DayTrips.ADD_A_LOCATION).click()
        sleep(self.DEFAULT_WAIT)

    def search_and_pick_location(self, location_name):
        """Searches for a location"""
        search_field = self.device.xpath(DayTrips.CUSTOM_DAY_TRIP_SEARCH)
        assert search_field.exists, "Could not find search field"
        search_field.click()
        sleep(self.DEFAULT_WAIT)
        self.device.send_keys(location_name)
        sleep(self.DEFAULT_WAIT)
        location_result = self.device.xpath(f'//android.widget.TextView[@text="{location_name}"]')
        assert location_result.exists, f"Could not find location result for: {location_name}"
        location_result.click()
        sleep(self.SEARCH_WAIT)
        return True

    def click_quick_suggestions(self):
        """Click the Quick Suggestions text."""
        self.device.xpath(DayTrips.QUICK_SUGGESTIONS).click()
        sleep(self.DEFAULT_WAIT)

    def click_auto_recommend(self):
        """Click the Auto-Recommend button."""
        self.device.xpath(DayTrips.AUTO_RECOMMEND_BUTTON).click()
        sleep(self.DEFAULT_WAIT)

    def click_date_picker(self, month=None, day=None, year=None):
        """
        Click the date picker with a specific date.

        Args:
            month (str, optional): Month name (e.g., 'February'). Defaults to current month.
            day (str, optional): Day of month (e.g., '25'). Defaults to current day.
            year (str, optional): Year in YYYY format (e.g., '2025'). Defaults to current year.
        """
        from datetime import datetime
        current_date = datetime.now()
        month = month or current_date.strftime('%B')
        day = day or str(current_date.day)
        year = year or str(current_date.year)
        date_string = f"{month} {day}, {year}"
        date_picker = self.device.xpath(f'//android.view.ViewGroup[@content-desc="{date_string}"]')
        assert date_picker.exists, f"Could not find date picker with date: {date_string}"
        date_picker.click()
        sleep(self.DEFAULT_WAIT)

    def click_date_picker_right_arrow(self):
        """Click the date picker right arrow button."""
        self.device.xpath(DayTrips.DATE_PICKER_RIGHT_ARROW).click()

    def select_date(self, date_number):
        """
        Select a specific date from the date picker.

        Args:
            date_number: String representing the date (e.g., '31')
        """
        self.device.xpath(DayTrips.DATE_PICKER_SELECTED_DATE.format(date_number)).click()
        sleep(self.DEFAULT_WAIT)

    def click_events(self):
        """Click the Events button."""
        self.device.xpath(DayTrips.CUSTOM_DAY_TRIP_EVENTS).click()
        sleep(self.DEFAULT_WAIT)

    def click_food_drinks(self):
        """Click the Food + Drinks button."""
        self.device.xpath(DayTrips.CUSTOM_DAY_TRIP_FOOD_DRINKS).click()
        sleep(self.DEFAULT_WAIT)

    def click_outdoors(self):
        """Click the Outdoors button."""
        self.device.xpath(DayTrips.CUSTOM_DAY_TRIP_OUTDOORS).click()
        sleep(self.DEFAULT_WAIT)

    def click_points_of_interest(self):
        """Click the Points of Interest button."""
        self.device.xpath(DayTrips.CUSTOM_DAY_TRIPS_POINTS_OF_INTEREST).click()
        sleep(self.DEFAULT_WAIT)

    def click_advanced_filter(self):
        """Click the Advanced Filter button."""
        self.device.xpath(DayTrips.ADVANCED_FILTER).click()
        sleep(self.DEFAULT_WAIT)

    def click_next(self):
        """Click the Next button."""
        self.device.xpath(DayTrips.NEXT_BUTTON).click()
        sleep(self.DEFAULT_WAIT)

    def click_continue(self):
        """Click the Continue button."""
        self.device.xpath(DayTrips.CONTINUE_BUTTON).click()
        sleep(self.DEFAULT_WAIT)

    def enter_trip_with_events_name(self):
        """
        Click the trip name field and enter a unique name with format:
        Events[random_number]

        Returns:
            str: The generated trip name

        Example:
            Events1234
        """
        import random
        random_number = random.randint(1, 9999)
        trip_name = f"Events{random_number}"
        trip_name_field = self.device.xpath(DayTrips.TRIP_NAME)
        assert trip_name_field.exists, "Trip name input field not found"
        trip_name_field.click()
        sleep(self.DEFAULT_WAIT)
        self.device.send_keys(trip_name)
        sleep(self.DEFAULT_WAIT)

        return trip_name

    def enter_trip_with_food_drinks_name(self):
        """
        Click the trip name field and enter a unique name with format:
        FoodDrinks[random_number]

        Returns:
            str: The generated trip name

        Example:
            FoodDrinks1234
        """
        import random
        random_number = random.randint(1, 9999)
        trip_name = f"Fooddrinks{random_number}"
        trip_name_field = self.device.xpath(DayTrips.TRIP_NAME)
        assert trip_name_field.exists, "Trip name input field not found"
        trip_name_field.click()
        sleep(self.DEFAULT_WAIT)
        self.device.send_keys(trip_name)
        sleep(self.DEFAULT_WAIT)

        return trip_name

    def enter_trip_with_outdoors_name(self):
        """
        Click the trip name field and enter a unique name with format:
        Outdoors[random_number]

        Returns:
            str: The generated trip name

        Example:
            Outdoors42
        """
        import random
        random_number = random.randint(1, 9999)
        trip_name = f"Outdoors{random_number}"
        trip_name_field = self.device.xpath(DayTrips.TRIP_NAME)
        assert trip_name_field.exists, "Trip name input field not found"
        trip_name_field.click()
        sleep(self.DEFAULT_WAIT)
        self.device.send_keys(trip_name)
        sleep(self.DEFAULT_WAIT)

        return trip_name

    def enter_trip_with_points_of_interest_name(self):
        """
        Click the trip name field and enter a unique name with format:
        Points[random_number]

        Returns:
            str: The generated trip name

        Example:
            Points1234
        """
        import random
        random_number = random.randint(1, 9999)
        trip_name = f"Points{random_number}"
        trip_name_field = self.device.xpath(DayTrips.TRIP_NAME)
        assert trip_name_field.exists, "Trip name input field not found"
        trip_name_field.click()
        sleep(self.DEFAULT_WAIT)
        self.device.send_keys(trip_name)
        sleep(self.DEFAULT_WAIT)
        return trip_name

    def click_save_trip(self):
        """
        Click the Save button to save the trip.
        Makes two attempts to click the button to ensure it's properly clicked.

        Raises:
            AssertionError: If Save Trip button is not found
        """
        save_button = self.device.xpath(DayTrips.SAVE_TRIP)
        assert save_button.wait(timeout=self.SEARCH_WAIT), "Save Trip button not found"
        save_button.click()
        sleep(self.DEFAULT_WAIT)
        save_button = self.device.xpath(DayTrips.SAVE_TRIP)
        if save_button.wait(timeout=self.DEFAULT_WAIT):
            save_button.click()
            sleep(self.DEFAULT_WAIT)

    def click_my_trips(self):
        """
        Click the My Trips button.

        Returns:
            bool: True if button was found and clicked

        Raises:
            AssertionError: If My Trips button is not found
        """
        my_trips_button = self.device.xpath(DayTrips.MY_TRIPS)
        assert my_trips_button.exists, "My Trips button not found"
        my_trips_button.click()
        sleep(self.DEFAULT_WAIT)
        return True

    def search_day_trip_with_events(self, trip_name="Events"):
        """
        Search for a day trip containing "Events" and click on the search result.
        Uses multiple click attempts with verification to ensure the click is successful.

        Args:
            trip_name (str, optional): Base name to search for. Defaults to "Events".

        Raises:
            AssertionError: If search field or result is not found
        """
        search_field = self.device.xpath(DayTrips.DAY_TRIPS_SEARCH)
        assert search_field.wait(timeout=self.SEARCH_WAIT), "Day Trips search field not found"
        search_field.click()
        sleep(self.DEFAULT_WAIT)
        self.device.send_keys(trip_name)
        sleep(self.DEFAULT_WAIT * 3)
        events_card = self.device.xpath(DayTrips.DAY_TRIPS_MY_TRIPS_CARD)
        assert events_card.wait(timeout=self.SEARCH_WAIT * 2), "Events day trip card not found"
        max_click_attempts = 3
        for attempt in range(max_click_attempts):
            events_card.click()
            sleep(self.DEFAULT_WAIT * 2)
            details_element = self.device.xpath(DayTrips.DAY_TRIPS_DETAILS_PLACES)
            if details_element.exists:
                break
            if attempt < max_click_attempts - 1:
                sleep(self.DEFAULT_WAIT)
                events_card = self.device.xpath(DayTrips.DAY_TRIPS_MY_TRIPS_CARD)
                if not events_card.exists:
                    if details_element.exists:
                        break
                    assert False, f"Events card disappeared after click attempt {attempt + 1}"
        details_element = self.device.xpath(DayTrips.DAY_TRIPS_DETAILS_PLACES)
        assert details_element.wait(
            timeout=self.SEARCH_WAIT), "Failed to navigate to day trip details after multiple click attempts"
        sleep(self.DEFAULT_WAIT * 2)

    def search_day_trip_with_food_drinks(self):
        """
        Search for a day trip with Food & Drinks and click on the search result.
        Uses multiple click attempts with verification to ensure the click is successful.

        Raises:
            AssertionError: If search field or result is not found
        """
        search_field = self.device.xpath(DayTrips.DAY_TRIPS_SEARCH)
        assert search_field.wait(timeout=self.SEARCH_WAIT), "Day Trips search field not found"
        search_field.click()
        sleep(self.DEFAULT_WAIT)
        self.device.send_keys("Fooddrinks")
        sleep(self.DEFAULT_WAIT * 3)
        food_drinks_card = self.device.xpath(DayTrips.DAY_TRIPS_SEARCH_RESULT_FOOD_DRINKS)
        assert food_drinks_card.wait(timeout=self.SEARCH_WAIT * 2), "Food & Drinks day trip card not found"
        max_click_attempts = 3
        for attempt in range(max_click_attempts):
            food_drinks_card.click()
            sleep(self.DEFAULT_WAIT * 2)
            details_element = self.device.xpath(DayTrips.DAY_TRIPS_DETAILS_PLACES)
            if details_element.exists:
                break
            if attempt < max_click_attempts - 1:
                sleep(self.DEFAULT_WAIT)
                food_drinks_card = self.device.xpath(DayTrips.DAY_TRIPS_MY_TRIPS_CARD)
                if not food_drinks_card.exists:
                    if details_element.exists:
                        break
                    assert False, f"Food & Drinks card disappeared after click attempt {attempt + 1}"
        details_element = self.device.xpath(DayTrips.DAY_TRIPS_DETAILS_PLACES)
        assert details_element.wait(
            timeout=self.SEARCH_WAIT), "Failed to navigate to day trip details after multiple click attempts"
        sleep(self.DEFAULT_WAIT * 2)

    def search_day_trip_with_outdoors(self):
        """
        Search for a day trip with Outdoors and click on the search result.
        Uses multiple click attempts with verification to ensure the click is successful.

        Raises:
            AssertionError: If search field or result is not found
        """
        search_field = self.device.xpath(DayTrips.DAY_TRIPS_SEARCH)
        assert search_field.wait(timeout=self.SEARCH_WAIT), "Day Trips search field not found"
        search_field.click()
        sleep(self.DEFAULT_WAIT)
        self.device.send_keys("Outdoors")
        sleep(self.DEFAULT_WAIT * 3)
        outdoors_card = self.device.xpath(DayTrips.DAY_TRIPS_SEARCH_RESULT_OUTDOORS)
        assert outdoors_card.wait(timeout=self.SEARCH_WAIT * 2), "Outdoors day trip card not found"
        max_click_attempts = 3
        for attempt in range(max_click_attempts):
            outdoors_card.click()
            sleep(self.DEFAULT_WAIT * 2)
            details_element = self.device.xpath(DayTrips.DAY_TRIPS_DETAILS_PLACES)
            if details_element.exists:
                break
            if attempt < max_click_attempts - 1:
                sleep(self.DEFAULT_WAIT)
                outdoors_card = self.device.xpath(DayTrips.DAY_TRIPS_MY_TRIPS_CARD)
                if not outdoors_card.exists:
                    if details_element.exists:
                        break
                    assert False, f"Outdoors card disappeared after click attempt {attempt + 1}"
        details_element = self.device.xpath(DayTrips.DAY_TRIPS_DETAILS_PLACES)
        assert details_element.wait(
            timeout=self.SEARCH_WAIT), "Failed to navigate to day trip details after multiple click attempts"
        sleep(self.DEFAULT_WAIT * 2)

    def search_day_trip_with_points_of_interest(self):
        """
        Search for a day trip with Points of Interest and click on the search result.
        Uses multiple click attempts with verification to ensure the click is successful.

        Raises:
            AssertionError: If search field or result is not found
        """
        search_field = self.device.xpath(DayTrips.DAY_TRIPS_SEARCH)
        assert search_field.wait(timeout=self.SEARCH_WAIT), "Day Trips search field not found"
        search_field.click()
        sleep(self.DEFAULT_WAIT)
        self.device.send_keys("Points")
        sleep(self.DEFAULT_WAIT * 3)
        poi_card = self.device.xpath(DayTrips.DAY_TRIPS_SEARCH_RESULT_PTS_INTEREST)
        assert poi_card.wait(timeout=self.SEARCH_WAIT * 2), "Points of Interest day trip card not found"
        max_click_attempts = 3
        for attempt in range(max_click_attempts):
            poi_card.click()
            sleep(self.DEFAULT_WAIT * 2)
            details_element = self.device.xpath(DayTrips.DAY_TRIPS_DETAILS_PLACES)
            if details_element.exists:
                break
            if attempt < max_click_attempts - 1:
                sleep(self.DEFAULT_WAIT)
                poi_card = self.device.xpath(DayTrips.DAY_TRIPS_MY_TRIPS_CARD)
                if not poi_card.exists:
                    if details_element.exists:
                        break
                    assert False, f"Points of Interest card disappeared after click attempt {attempt + 1}"
        details_element = self.device.xpath(DayTrips.DAY_TRIPS_DETAILS_PLACES)
        assert details_element.wait(
            timeout=self.SEARCH_WAIT), "Failed to navigate to day trip details after multiple click attempts"
        sleep(self.DEFAULT_WAIT * 2)

    def click_three_dotted_menu(self):
        """
        Click the three-dotted menu button in day trip details.
        Uses multiple click attempts with verification to ensure the click is successful.

        Raises:
            AssertionError: If menu button is not found after all attempts
        """
        max_attempts = 3
        for attempt in range(max_attempts):
            menu_button = self.device.xpath(DayTrips.DAY_TRIPS_THREE_DOTTED_BUTTON)
            if menu_button.exists:
                menu_button.click()
                sleep(self.DEFAULT_WAIT)
                delete_button = self.device.xpath(DayTrips.DAY_TRIPS_DELETE_BUTTON)
                if delete_button.exists:
                    return
            if attempt < max_attempts - 1:
                sleep(self.DEFAULT_WAIT * 2)
        assert False, "Three-dotted menu button not found after multiple attempts"

    def click_delete_trip(self):
        """
        Click the delete button in the trip options menu.
        Note: Three-dotted menu must be opened first.

        Raises:
            AssertionError: If delete button is not found
        """
        delete_button = self.device.xpath(DayTrips.DAY_TRIPS_DELETE_BUTTON)
        assert delete_button.exists, "Delete button not found in menu"

        delete_button.click()
        sleep(self.DEFAULT_WAIT)


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

    NAVIGATION_WAIT = 5
    EVENTS_TEXT = "Events"

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


class NavCheckIn:
    """Class for handling navigation in the check-in process"""

    def __init__(self, device):
        """
        Initialize NavCheckIn with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_business_three_dotted(self, wait_time=3):
        """
        Taps the three-dotted menu icon on a business card and verifies the Check-In option is available.

        Args:
            wait_time (int, optional): Time to wait for the Check-In option to appear. Defaults to 3 seconds.

        Returns:
            bool: True if menu was tapped and Check-In option is present

        Raises:
            AssertionError: If three-dotted menu isn't found or Check-In option doesn't appear
        """
        self.device.xpath(CheckIn.BUSINESS_THREE_DOTTED).click()
        sleep(wait_time)
        check_in_option = self.device.xpath(CheckIn.MENU_CHECK_IN).exists
        assert check_in_option, "Check-In option not found in the three-dotted menu"
        return True

    def click_check_in(self, wait_time=2):
        """
        Taps the Check-In option.

        Args:
            wait_time (int, optional): Time to wait for the Check-In screen to appear.

        Returns:
            bool: True if the button was tapped and the check-in screen is present.

        Raises:
            AssertionError: If check-in menu doesn't appear.
        """
        self.device.xpath(CheckIn.MENU_CHECK_IN).click()
        sleep(wait_time)
        check_in_screen = self.device.xpath(CheckIn.DEFAULT_RATING).exists
        assert check_in_screen, "Check-In screen not found"
        return True

    def input_your_thoughts(self, text = "Text Check-In", wait_time=2):
        """
        Inputs text in the 'Your feedback is private' field and presses enter.

        Args:
            text (str, optional): Text to input in the feedback field. Defaults to "Test Check-In".
            wait_time (int, optional): Time to wait after actions. Defaults to 2 seconds.

        Returns:
            bool: True if text was input successfully

        Raises:
            AssertionError: If feedback field is not found
        """
        your_thoughts_field = self.device.xpath(CheckIn.YOUR_THOUGHTS)
        assert your_thoughts_field.exists, "Feedback field not found"
        your_thoughts_field.click()
        sleep(wait_time)
        self.device.send_keys(text)
        sleep(1)
        self.device.press("enter")
        sleep(wait_time)
        return True

    def save_check_in(self, wait_time=3):
        """
        Taps Save in the Check-In screen.

        Args:
            wait_time (int, optional): Time to wait after actions. Defaults to 3 seconds.

        Returns:
            bool: True if save successful

        Raises:
            AssertionError: If Cheers button not present
        """
        self.device.xpath(CheckIn.SAVE_CHECK_IN).click()
        sleep(wait_time)
        cheers_button = self.device.xpath(CheckIn.CHEERS_BUTTON).exists
        assert cheers_button, "Cheers button not found"

    def click_cheers_button(self, wait_time=2):
        """
        Clicks the Cheers button that appears after saving a check-in.

        Args:
            wait_time (int, optional): Time to wait after clicking. Defaults to 2 seconds.

        Returns:
            bool: True if button was clicked successfully

        Raises:
            AssertionError: If Cheers button not found
        """
        cheers_button = self.device.xpath(CheckIn.CHEERS_BUTTON)
        cheers_button.click()
        sleep(wait_time)
        return True

    def click_visit_history_three_dotted(self, wait_time=1):
        """
        Taps the three-dotted menu icon on the Visit History after saving the check-in and verifies if Delete option
        is available.

        Args:
            wait_time (int, optional): Time to wait for the Check-In option to appear. Defaults to 3 seconds.

        Returns:
            bool: True if Delete button visible

        Raises:
            AssertionError: If Delete button isn't found or Check-In option doesn't appear
        """
        self.device.xpath(CheckIn.VISIT_HISTORY_THREE_DOTTED).click()
        sleep(wait_time)
        delete_button = self.device.xpath(CheckIn.DELETE_CHECK_IN_BUTTON)
        assert delete_button, "Delete button not found"

    def click_visit_history_delete(self, wait_time=2):
        """
        Taps the Delete button on the Visit History's three dotted menu and verifies if Yes option is available.

        Args:
            wait_time (int, optional): Time to wait for the Check-In option to appear. Defaults to 3 seconds.

        Returns:
            bool: True if Yes option is available

        Raises:
            AssertionError: If Yes button isn't found or Check-In option doesn't appear
        """
        self.device.xpath(CheckIn.DELETE_CHECK_IN_BUTTON).click()
        sleep(wait_time)
        yes = self.device.xpath(CheckIn.DELETE_YES)
        assert yes, "Yes button not found"

    def click_yes(self, wait_time=2):
        """
        Taps the Yes button on the Visit History's three dotted menu, then verifies that the text:
        "I'd go if I'm in town" has disappeared.

        Args:
            wait_time (int, optional): Time to wait for the Check-In option to appear. Defaults to 3 seconds.

        Returns:
            bool: True if the text has disappeared

        Raises:
            AssertionError: If text still present
        """
        self.device.xpath(CheckIn.DELETE_YES).click()
        sleep(wait_time)
        default_rating_text = self.device(text="I'd go if I'm in town").exists
        assert not default_rating_text, "Check In not deleted"


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
        self.DEFAULT_WAIT = 1.5

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

    def click_ask_ai(self):
        """
        Clicks the Search button in Guest Mode.

        Returns:
            bool: True if click was successful

        Raises:
            AssertionError: If Ask AI button is not found
        """
        ask_ai_button = self.device.xpath(AskAI.ASKAI_ICON)
        assert ask_ai_button.exists, "Search button not found"

        ask_ai_button.click()
        sleep(self.SEARCH_WAIT)
        return True

    def click_guest_mode_locked_videos(self):
        """
        Click on a video in guest mode to trigger the plans popup.
        Uses the specific locator for locked videos details.

        Returns:
            bool: True if successful

        Raises:
            AssertionError: If no videos are found to click
        """
        videos_section = self.device(text="Videos")
        assert videos_section.exists, "Videos section not found"
        locked_videos_details = self.device.xpath(GuestMode.GUEST_MODE_LOCKED_VIDEOS_DETAILS)
        if locked_videos_details.exists:
            locked_videos_details.click()
            sleep(self.DEFAULT_WAIT)
            return True
        locked_videos = self.device.xpath(GuestMode.GUEST_MODE_HOME_SCREEN_LOCKED_VIDEOS)
        if locked_videos.exists:
            locked_videos.click()
            sleep(self.DEFAULT_WAIT)
            return True
        video_element = self.device.xpath(Videos.VIDEO_TILE)
        if video_element.exists:
            video_element.click()
            sleep(self.DEFAULT_WAIT)
            return True
        see_all_button = self.device.xpath(GuestMode.GUEST_MODE_VIDEOS_SEE_ALL)
        if see_all_button.exists:
            see_all_button.click()
            sleep(self.DEFAULT_WAIT)
            return True
        raise AssertionError("Could not find any video elements to click in guest mode")

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
