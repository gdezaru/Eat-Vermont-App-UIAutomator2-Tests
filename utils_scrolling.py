"""
Utility functions for scrolling.
"""
import os
from time import sleep

from conftest import screenshots_dir
from locators import EventsScreen, Events, GuestMode, HomeScreen, DayTrips


class ScreenSwipe:
    def __init__(self, device):
        """
        Initialize ScreenSwipe with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device
        self.width, self.height = self._get_screen_dimensions()

    def _get_screen_dimensions(self):
        """
        Returns the screen width and height.

        Returns:
            tuple: A tuple containing (width, height)
        """
        screen_info = self.device.info
        width = screen_info['displayWidth']
        height = screen_info['displayHeight']
        return width, height

    def calculate_swipe_coordinates(self):
        """
        Calculates swipe coordinates for scrolling based on the screen dimensions.

        Returns:
            tuple: A tuple containing (start_x, start_y, end_y) where:
                  - start_x is the horizontal position (middle of screen)
                  - start_y is the starting vertical position (3/4 down the screen)
                  - end_y is the ending vertical position (1/4 down the screen)
        """
        start_x = self.width // 2
        start_y = (self.height * 3) // 4
        end_y = self.height // 4
        return start_x, start_y, end_y

    def get_dimensions(self):
        """
        Get the current screen dimensions.

        Returns:
            tuple: A tuple containing (width, height)
        """
        return self.width, self.height


class GeneralScrolling(ScreenSwipe):
    def __init__(self, device):
        """
        Initialize GeneralScrolling with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        super().__init__(device)

    def get_target_position_in_first_quarter(self):
        """
        Calculate the target position in the first quarter of the screen.

        Returns:
            int: The y-coordinate target position
        """
        return self.height // 4

    def scroll_to_bottom(self, scroll_times=3, duration=0.5):
        """
        Scrolls to the bottom of the results on the screen.

        Args:
            scroll_times: Number of times to scroll to ensure reaching the bottom.
            duration: Duration of each swipe in seconds.
        """
        screen_size = self.device.window_size()
        for _ in range(scroll_times):
            self.device.swipe(
                screen_size[0] * 0.5,  # start x: middle of screen
                screen_size[1] * 0.8,  # start y: 80% down
                screen_size[0] * 0.5,  # end x: middle of screen
                screen_size[1] * 0.2,  # end y: 20% down
                duration=duration
            )
            sleep(2)


class EventsScrolling(GeneralScrolling):
    def __init__(self, device):
        """
        Initialize EventsScrolling with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        super().__init__(device)

    def scroll_to_event_and_click(self, screenshots_dir, current_day=None):
        """
        Scroll to the first event in the calendar and click it.

        Args:
            screenshots_dir: Directory to save screenshots
            current_day: Current day for screenshot naming

        Returns:
            bool: True if event was found and clicked, False if no events found

        Raises:
            AssertionError: If neither events nor 'No Events' message is found
        """
        # Verify that either there's an event or "No Events" message is shown
        first_event = self.device.xpath(EventsScreen.EVENTS_SCREEN_TILE_1)
        no_events_message = self.device.xpath(EventsScreen.EVENTS_SCREEN_NO_EVENTS)

        assert first_event.exists or no_events_message.exists, "Neither events nor 'No Events' message found"

        # If no event was found initially, scroll to try to find one
        if not first_event.exists and not no_events_message.exists:
            max_scroll_attempts = 3
            found_event = False

            for scroll_attempt in range(max_scroll_attempts):
                # Scroll down using parent class method
                self.scroll_to_bottom(scroll_times=1, duration=0.5)

                # Check if we can now see an event
                first_event = self.device.xpath(EventsScreen.EVENTS_SCREEN_TILE_1)
                if first_event.exists:
                    found_event = True
                    # Take a screenshot after finding the event
                    if current_day:
                        screenshot_path = os.path.join(screenshots_dir,
                                                       f"3_1_3_home_screen_events_{current_day.lower()}_after_scroll.png")
                        self.device.screenshot(screenshot_path)
                    break

            if not found_event:
                assert no_events_message.exists, "No events found and 'No Events' message is not displayed"
                return False

        # Click on the first event tile if it exists
        if first_event.exists:
            # Get the event title before clicking
            event_title = first_event.get_text()

            # Click the event title and wait for details to load
            first_event.click()
            sleep(2)  # Wait for event details to load

            # Verify we're in the event details view by checking for the event title
            event_title_in_details = self.device.xpath(EventsScreen.EVENT_TITLE.format(event_title))
            assert event_title_in_details.exists, f"Failed to open event details for '{event_title}'"
            return True

        return False

    def scroll_to_events_within_30(self):
        """
        Scroll to the events within 30 minutes and ensure the text is in the first quarter of the screen.

        Returns:
            bool: True if the text was found and positioned correctly, False otherwise
        """
        target_y = self.get_target_position_in_first_quarter()
        start_x, start_y, end_y = self.calculate_swipe_coordinates()

        self.device(scrollable=True).scroll.to(text="Events Within ~30min")
        if not self.device(text="Events Within ~30min").exists(timeout=5):
            print("Warning: Events Within ~30min text not found")
            return False

        events_elem = self.device(text="Events Within ~30min")
        bounds = events_elem.info['bounds']
        current_y = (bounds['top'] + bounds['bottom']) // 2

        max_adjustment_attempts = 3
        for attempt in range(max_adjustment_attempts):
            if current_y <= target_y:
                break

            scroll_distance = (current_y - target_y) // 2
            self.device.swipe(start_x, start_y, start_x, start_y - scroll_distance, duration=0.5)
            sleep(1)

            bounds = events_elem.info['bounds']
            current_y = (bounds['top'] + bounds['bottom']) // 2

        sleep(1)
        return True

    def scroll_to_events_further_than_30(self):
        """
        Scroll to the events further than 30 minutes and ensure the text is in the first quarter of the screen.

        Returns:
            bool: True if the text was found and positioned correctly, False otherwise
        """
        target_y = self.get_target_position_in_first_quarter()
        start_x, start_y, end_y = self.calculate_swipe_coordinates()

        self.device(scrollable=True).scroll.to(text="Events Further Than ~30min")
        if not self.device(text="Events Further Than ~30min").exists(timeout=5):
            print("Warning: Events Further Than ~30min text not found")
            return False

        events_elem = self.device(text="Events Further Than ~30min")
        bounds = events_elem.info['bounds']
        current_y = (bounds['top'] + bounds['bottom']) // 2

        max_adjustment_attempts = 3
        for attempt in range(max_adjustment_attempts):
            if current_y <= target_y:
                break

            scroll_distance = (current_y - target_y) // 2
            self.device.swipe(start_x, start_y, start_x, start_y - scroll_distance, duration=0.5)
            sleep(1)

            bounds = events_elem.info['bounds']
            current_y = (bounds['top'] + bounds['bottom']) // 2

        sleep(1)
        return True

    def scroll_event_card(self):
        """
        Attempts to scroll to the bottom of the event card to see its details.

        Returns:
            bool: True if event details were found, False otherwise
        """
        max_swipes = 5
        found = False
        for i in range(max_swipes):
            if self.device.xpath(Events.EVENT_DETAILS_TEXT).exists:
                found = True
                break
            self.device.swipe_ext("up", scale=0.8)
            sleep(1)

        return found


class ScrollAddInfo(GeneralScrolling):
    def __init__(self, device):
        """
        Initialize ScrollAddInfo with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        super().__init__(device)

    def scroll_to_add_info(self):
        """
        Scroll to the Add Info button.

        Returns:
            bool: True if Add Info button was found, False otherwise

        Raises:
            AssertionError: If Add Info button is not found after scrolling
        """
        try:
            self.device(scrollable=True).scroll.to(text="Add Info")
            assert self.device(text="Add Info").exists(timeout=5), "Add Info button not found"
            sleep(1)
            return True
        except Exception as e:
            print(f"Error scrolling to Add Info button: {str(e)}")
            return False


class ScrollToCustomDayTrips:
    """Class for handling Custom Day Trips navigation."""

    # Class constants
    DAY_TRIPS_TEXT = "Day Trips"
    CUSTOM_TRIP_TEXT = "Create a Custom trip"

    # Scroll settings
    MAX_SCROLL_ATTEMPTS = 5
    SCROLL_DURATION = 0.3
    DEFAULT_WAIT = 2
    LONG_WAIT = 5

    def __init__(self, device):
        """
        Initialize NavCustomDayTrips with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device
        self.general_scroll = GeneralScrolling(device)

    def scroll_to_custom_day_trips(self, max_attempts=5):
        """
        Scroll until Day Trips section is found and centered.

        Args:
            max_attempts: Maximum number of scroll attempts (default: 5)

        Returns:
            bool: True if Day Trips section was found and centered

        Raises:
            AssertionError: If Day Trips section is not found after max attempts
        """
        screen_swipe = ScreenSwipe(self.device)
        start_x, start_y, end_y = screen_swipe.calculate_swipe_coordinates()
        target_y = self.general_scroll.get_target_position_in_first_quarter()
        scroll_end_y = (start_y + end_y) // 2
        for attempt in range(max_attempts):
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
        custom_trip_button = self.device(text=self.CUSTOM_TRIP_TEXT)
        assert custom_trip_button.exists(timeout=self.LONG_WAIT), (
            "Custom Day Trip button not found"
        )

        return True


class ScrollVideos(GeneralScrolling):
    def __init__(self, device):
        """
        Initialize ScrollVideos with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        super().__init__(device)

    def guest_mode_scroll_to_videos(self):
        """
        Scrolls to videos section in Guest Mode.
        Uses multiple scroll strategies and improved positioning
        similar to the regular scroll_to_videos method.

        Returns:
            bool: True if locked videos section was found

        Raises:
            AssertionError: If locked videos section is not found after max attempts
        """
        start_x = self.width // 2
        locked_videos = self.device.xpath(GuestMode.GUEST_MODE_HOME_SCREEN_LOCKED_VIDEOS)
        scrollable = self.device(scrollable=True)
        if scrollable.exists:
            scrollable.scroll.to(text="Videos")
            sleep(1.5)
            if locked_videos.exists:
                return True
        max_scroll_attempts = 15
        for attempt in range(max_scroll_attempts):
            if locked_videos.exists:
                return True
            if attempt < 5:
                start_y_percent = 0.7
                end_y_percent = 0.3
            elif attempt < 10:
                start_y_percent = 0.8
                end_y_percent = 0.2
            else:
                start_y_percent = 0.9
                end_y_percent = 0.1
            self.device.swipe(
                start_x,
                int(self.height * start_y_percent),
                start_x,
                int(self.height * end_y_percent),
                duration=0.9
            )
            sleep(1.5)
            if attempt > 5 and self.device(text="Videos").exists:
                return True
        for i in range(3):
            self.device.swipe(
                start_x,
                int(self.height * 0.9),
                start_x,
                int(self.height * 0.1),
                duration=1.2
            )
            sleep(2)
            if locked_videos.exists or self.device(text="Videos").exists:
                return True

        raise AssertionError("Failed to find locked videos section after maximum scroll attempts")

    def guest_mode_scroll_to_videos(self):
        """
        Scrolls to videos section in Guest Mode.

        Returns:
            bool: True if locked videos section was found, False if not found after max attempts
        """
        start_x, start_y, end_y = self.calculate_swipe_coordinates()
        locked_videos = self.device.xpath(GuestMode.GUEST_MODE_HOME_SCREEN_LOCKED_VIDEOS)

        max_scroll_attempts = 9
        for attempt in range(max_scroll_attempts):
            if locked_videos.exists:
                return True

            self.device.swipe(start_x, start_y, start_x, end_y, duration=0.9)
            sleep(1.5)

        print("Failed to find locked videos section after maximum scroll attempts")
        return False
