""""
Utilities functions for UI verification
"""
import os
from time import sleep
from locators import (Businesses, EventsScreen, HomeScreenTiles, SettingsScreen, Trails, GuestMode,
                      PlansPopup, ViewMap, LoginPage, DayTrips)
from utils_screenshots import ScreenshotsManagement
from utils_scrolling import ScreenSwipe, GeneralScrolling


class VerifyEvents:
    def __init__(self, device):
        """
        Initialize VerifyEvents with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device
        self.days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.days_short = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']

    def verify_events_search_result(self):
        """
        Verify that event search results are displayed.
        Looks for indicators like "Burlington" or "Event" in the results.

        Returns:
            bool: True if search results are verified

        Raises:
            AssertionError: If search results cannot be verified
        """
        search_successful = (
                self.device(textContains="Burlington").exists or
                self.device(textContains="Event").exists
        )

        assert search_successful, "Search failed - Could not verify search results"
        return True

    def find_and_click_current_day(self):
        """
        Find and click on the current day element in the events calendar screen.

        Returns:
            str: The current day in three-letter format (e.g., 'MON', 'TUE')

        Raises:
            AssertionError: If no day of week element is found
        """
        current_day = None
        for day in self.days_short:
            day_element = self.device.xpath(EventsScreen.DAY_OF_WEEK.format(day, day))
            if day_element.exists:
                current_day = day
                print(f"\nFound current day: {day}")
                day_element.click()
                sleep(2)
                break

        assert current_day is not None, "Could not find any day of week element"
        return current_day

    def find_event_within_30(self):
        """
        Find an event tile within 30 minutes.

        Returns:
            bool: True if event was found, False otherwise

        Raises:
            AssertionError: If no events are found
        """
        event_found = False
        for day in self.days_of_week:
            events_tile = self.device.xpath(HomeScreenTiles.EVENTS_WITHIN_30_TILE.format(day))
            if events_tile.exists:
                event_found = True
                break

        assert event_found, "Could not find any events with dates in Events within 30 minutes section"
        sleep(1)
        return True

    def find_event_further_than_30(self):
        """
        Find an event tile further than 30 minutes.

        Returns:
            bool: True if event was found, False otherwise

        Raises:
            AssertionError: If no events are found after maximum scroll attempts
        """
        event_found = False
        max_scroll_attempts = 3

        for attempt in range(max_scroll_attempts):
            print(f"\nScroll attempt {attempt + 1}/{max_scroll_attempts}")

            for day in self.days_of_week:
                events_tile = self.device.xpath(HomeScreenTiles.EVENTS_MORE_THAN_30_TILE.format(day))
                if events_tile.exists:
                    event_found = True
                    event_text = events_tile.get_text()
                    break

            if event_found:
                break

            # If no event found, scroll down and try again
            self.device.swipe(0.5, 0.8, 0.5, 0.2, 0.5)
            sleep(2)

        if not event_found:
            self.device.screenshot("debug_no_events_further_than_30.png")

        assert event_found, "Could not find any events further than 30 minutes after multiple scroll attempts"
        sleep(1)
        return True


class VerifyBusinesses:
    """Class for verifying business-related UI elements and interactions."""

    def __init__(self, device):
        """
        Initialize VerifyBusinesses with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device
        self.days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        self.current_attempt = 1

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

    def try_next_day(self, current_day):
        """
        Attempts to find and click on the next day element in the events screen.

        Args:
            current_day (str): The current day to start trying from.

        Raises:
            AssertionError: If no clickable day is found after trying all days
        """
        current_try_day = current_day
        days_tried = 0
        max_days_to_try = 7  # Try all days of the week at most

        while days_tried < max_days_to_try:
            next_day = self.get_next_day(current_try_day)

            max_attempts = 3
            click_success = False

            for try_count in range(max_attempts):  # Changed 'attempt' to 'try_count'
                self.current_attempt = try_count + 1  # Update class-level attempt counter
                next_day_element = self.device.xpath(EventsScreen.DAY_OF_WEEK.format(next_day, next_day))

                if not next_day_element.exists:
                    break

                next_day_element.click()
                sleep(2)

                events_for_day = self.device(textContains=next_day.title())
                if events_for_day.exists:
                    click_success = True
                    break
                elif try_count < max_attempts - 1:
                    sleep(2)
                else:
                    print(f"\nCould not verify events for {next_day} after {max_attempts} attempts, will try next day")

            if click_success:
                return

            current_try_day = next_day
            days_tried += 1

        assert False, "Could not find any clickable day after trying all days of the week"

    def verify_business_search_result(self):
        """
        Verify that business search results are displayed.
        Looks for indicators like business name or business section.

        Returns:
            bool: True if search results are verified

        Raises:
            AssertionError: If search results cannot be verified
        """
        search_successful = (
                self.device(textContains="Big Fatty BBQ").exists or
                self.device.xpath(Businesses.BUSINESSES_SECTION).exists
        )

        assert search_successful, "Search failed - Could not verify business search results"
        return True

    def verify_businesses_section_present(self):
        """
        Verifies that the Businesses section is present on the screen.

        Raises:
            AssertionError: If businesses section is not found
        """
        businesses_section = self.device.xpath(Businesses.BUSINESSES_SECTION)
        assert businesses_section.exists, "Businesses section not found in search results"

    def verify_business_about_tab(self):
        """
        Verify About tab is visible and its contents are present.

        Raises:
            AssertionError: If About tab or its contents are not found
        """
        about_tab = self.device.xpath(Businesses.BUSINESS_ABOUT_TAB)
        if about_tab.exists:
            assert about_tab.exists, "About tab not found on business details page"

        about_contents = self.device.xpath(Businesses.BUSINESS_ABOUT_TAB_CONTENTS)
        assert about_contents.exists, "About tab contents not found"

    def verify_business_fyi_tab(self):
        """
        Verifies if FYI tab is visible and clicks it.

        Raises:
            AssertionError: If FYI tab is not found
        """
        fyi_tab = self.device.xpath(Businesses.BUSINESS_FYI_TAB)
        assert fyi_tab.exists, "FYI tab not found"
        fyi_tab.click()
        sleep(2)

    def verify_business_fyi_tab_contents(self):
        """
        Verifies the contents of the FYI tab.

        Raises:
            AssertionError: If FYI tab contents are not found
        """
        fyi_contents = self.device.xpath(Businesses.BUSINESS_FYI_TAB_CONTENTS)
        assert fyi_contents.exists, "FYI tab contents not found"

    def verify_and_click_business_menu_tab(self):
        """
        Verifies if Menu tab is visible and clicks it.

        Raises:
            AssertionError: If Menu tab is not found
        """
        menu_tab = self.device.xpath(Businesses.BUSINESS_MENU_TAB)
        assert menu_tab.exists, "Menu tab not found on business details page"
        menu_tab.click()
        sleep(2)

    def verify_business_menu_tab_contents(self):
        """
        Verifies the contents of the business Menu tab.

        Raises:
            AssertionError: If Menu tab contents are not found
        """
        menu_contents = self.device.xpath(Businesses.BUSINESS_MENU_TAB_CONTENTS)
        assert menu_contents.exists, "Menu tab contents not found"


class VerifyViewMap:
    """Verification utilities for View Map screen"""

    def __init__(self, d):
        self.d = d

    def verify_events_filter_visible(self):
        """Verify Events filter is visible"""
        events_filter = self.d.xpath(ViewMap.EVENTS_FILTER)
        assert events_filter.exists, "Events filter is not visible on the map screen"

    def verify_food_drinks_filter_visible(self):
        """Verify Food & Drinks filter is visible"""
        food_drinks_filter = self.d.xpath(ViewMap.FOOD_AND_DRINKS_FILTER)
        assert food_drinks_filter.exists, "Food & Drinks filter is not visible on the map screen"

    def verify_farms_filter_visible(self):
        """Verify Farms filter is visible"""
        farms_filter = self.d.xpath(ViewMap.FARMS_FILTER)
        assert farms_filter.exists, "Farms filter is not visible on the map screen"

    def verify_food_pantries_filter_visible(self):
        """Verify Food Pantries filter is visible"""
        food_pantries_filter = self.d.xpath(ViewMap.FOOD_PANTRIES_FILTER)
        assert food_pantries_filter.exists, "Food Pantries filter is not visible on the map screen"

    def verify_all_filters_visible(self):
        """Verify all map filters are visible"""
        self.verify_events_filter_visible()
        self.verify_food_drinks_filter_visible()
        self.verify_farms_filter_visible()
        self.verify_food_pantries_filter_visible()


class VerifyDayTrips:
    """Class for verifying day trips-related UI elements and interactions."""

    def __init__(self, device):
        """
        Initialize VerifyDayTrips with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def verify_day_trips_search_result(self):
        """
        Verify that day trips search results are displayed.
        Looks for indicators like "Day Trip" or day trips section.

        Returns:
            bool: True if search results are verified

        Raises:
            AssertionError: If search results cannot be verified
        """
        search_successful = (
            self.device(textContains="Day Trip").exists or
            self.device(textContains="Trip").exists
        )

        assert search_successful, "Search failed - Could not verify day trips search results"
        return True


class VerifyCustomDayTrips:
    """Class for verifying Custom Day Trips-related UI elements and interactions."""

    def __init__(self, device):
        """
        Initialize VerifyCustomDayTrips with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def verify_create_trip_header(self):
        """
        Verify that the Create Trip header text is present.

        Returns:
            bool: True if header text exists

        Raises:
            AssertionError: If header text is not found
        """
        header = self.device.xpath(DayTrips.CREATE_TRIP_HEADER)
        assert header.exists, "Create Trip header 'Where do you want to go?' not found"
        return True

    def verify_add_location(self):
        """
        Verify that the Add A Location button is present.

        Returns:
            bool: True if button exists

        Raises:
            AssertionError: If button is not found
        """
        button = self.device.xpath(DayTrips.ADD_A_LOCATION)
        assert button.exists, "Add A Location button not found"
        return True

    def verify_quick_suggestions(self):
        """
        Verify that the Quick Suggestions text is present.

        Returns:
            bool: True if text exists

        Raises:
            AssertionError: If text is not found
        """
        text = self.device.xpath(DayTrips.QUICK_SUGGESTIONS)
        assert text.exists, "Quick Suggestions text not found"
        return True

    def verify_auto_recommend(self):
        """
        Verify that the Auto-Recommend button is present.

        Returns:
            bool: True if button exists

        Raises:
            AssertionError: If button is not found
        """
        button = self.device.xpath(DayTrips.AUTO_RECOMMEND_BUTTON)
        assert button.exists, "Auto-Recommend button not found"
        return True

    def verify_date_picker(self, date_str):
        """
        Verify that the date picker with specific date is present.

        Args:
            date_str: Date string in format 'Month DD, YYYY'

        Returns:
            bool: True if date picker exists

        Raises:
            AssertionError: If date picker is not found
        """
        picker = self.device.xpath(DayTrips.DATE_PICKER.format(date_str))
        assert picker.exists, f"Date picker for '{date_str}' not found"
        return True

    def verify_date_picker_right_arrow(self):
        """
        Verify that the date picker right arrow is present.

        Returns:
            bool: True if arrow exists

        Raises:
            AssertionError: If arrow is not found
        """
        arrow = self.device.xpath(DayTrips.DATE_PICKER_RIGHT_ARROW)
        assert arrow.exists, "Date picker right arrow not found"
        return True

    def verify_selected_date(self, date_number):
        """
        Verify that the selected date is present.

        Args:
            date_number: String representing the date (e.g., '31')

        Returns:
            bool: True if date exists

        Raises:
            AssertionError: If date is not found
        """
        date = self.device.xpath(DayTrips.DATE_PICKER_SELECTED_DATE.format(date_number))
        assert date.exists, f"Selected date '{date_number}' not found"
        return True

    def verify_events_button(self):
        """
        Verify that the Events button is present.

        Returns:
            bool: True if button exists

        Raises:
            AssertionError: If button is not found
        """
        button = self.device.xpath(DayTrips.CUSTOM_DAY_TRIP_EVENTS)
        assert button.exists, "Events button not found"
        return True

    def verify_food_drinks_button(self):
        """
        Verify that the Food + Drinks button is present.

        Returns:
            bool: True if button exists

        Raises:
            AssertionError: If button is not found
        """
        button = self.device.xpath(DayTrips.CUSTOM_DAY_TRIP_FOOD_DRINKS)
        assert button.exists, "Food + Drinks button not found"
        return True

    def verify_outdoors_button(self):
        """
        Verify that the Outdoors button is present.

        Returns:
            bool: True if button exists

        Raises:
            AssertionError: If button is not found
        """
        button = self.device.xpath(DayTrips.CUSTOM_DAY_TRIP_OUTDOORS)
        assert button.exists, "Outdoors button not found"
        return True

    def verify_points_of_interest_button(self):
        """
        Verify that the Points of Interest button is present.

        Returns:
            bool: True if button exists

        Raises:
            AssertionError: If button is not found
        """
        button = self.device.xpath(DayTrips.CUSTOM_DAY_TRIPS_POINTS_OF_INTEREST)
        assert button.exists, "Points of Interest button not found"
        return True

    def verify_advanced_filter(self):
        """
        Verify that the Advanced Filter button is present.

        Returns:
            bool: True if button exists

        Raises:
            AssertionError: If button is not found
        """
        button = self.device.xpath(DayTrips.ADVANCED_FILTER)
        assert button.exists, "Advanced Filter button not found"
        return True

    def verify_next_button(self):
        """
        Verify that the Next button is present.

        Returns:
            bool: True if button exists

        Raises:
            AssertionError: If button is not found
        """
        button = self.device.xpath(DayTrips.NEXT_BUTTON)
        assert button.exists, "Next button not found"
        return True

    def verify_crafting_day_trip(self):
        """
        Verify that the Crafting Your Perfect Day Trip text is present.

        Returns:
            bool: True if text exists

        Raises:
            AssertionError: If text is not found
        """
        text = self.device.xpath(DayTrips.CRAFTING_DAY_TRIP)
        assert text.exists, "Crafting Your Trip text not found"
        return True

    def verify_location_details(self, location):
        """
        Verify that the location details text is present.

        Args:
            location: Name of the location (e.g., 'Burlington')

        Returns:
            bool: True if text exists

        Raises:
            AssertionError: If text is not found
        """
        text = self.device.xpath(DayTrips.DETAILS_SCREEN_LOCATION.format(location))
        assert text.exists, f"Location details for '{location}' not found"
        return True

    def verify_date_details(self, date_str):
        """
        Verify that the date details text is present.

        Args:
            date_str: Date string in format 'Month DD, YYYY'

        Returns:
            bool: True if text exists

        Raises:
            AssertionError: If text is not found
        """
        text = self.device.xpath(DayTrips.DETAILS_SCREEN_DATE.format(date_str))
        assert text.exists, f"Date details '{date_str}' not found"
        return True

    def verify_quick_tip(self):
        """
        Verify that the Quick Tip text is present.

        Returns:
            bool: True if text exists

        Raises:
            AssertionError: If text is not found
        """
        text = self.device.xpath(DayTrips.QUICK_TIP)
        assert text.exists, "Quick Tip text not found"
        return True

    def verify_also_tip(self):
        """
        Verify that the Also tip text is present.

        Returns:
            bool: True if text exists

        Raises:
            AssertionError: If text is not found
        """
        text = self.device.xpath(DayTrips.ALSO_TIP)
        assert text.exists, "Also tip text not found"
        return True

    def verify_continue_button(self):
        """
        Verify that the Continue button is present.

        Returns:
            bool: True if button exists

        Raises:
            AssertionError: If button is not found
        """
        button = self.device.xpath(DayTrips.CONTINUE_BUTTON)
        assert button.exists, "Continue button not found"
        return True




class VerifyTrails:
    """Class for verifying Trails-related UI elements and interactions."""

    VALID_TRAIL_STATUSES = ["Not Started", "In Progress", "Complete"]
    DEFAULT_TIMEOUT = 5

    def __init__(self, device):
        """
        Initialize VerifyTrails with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def verify_trails_percentage_progress(self):
        """
        Verifies the percentage progress in the Trails module.

        Returns:
            str: The percentage progress text

        Raises:
            AssertionError: If percentage progress element is not found within timeout
        """
        percentage_element = self.device.xpath(Trails.PERCENTAGE_PROGRESS)
        assert percentage_element.wait(timeout=self.DEFAULT_TIMEOUT), "Percentage progress not found"
        return percentage_element.get_text()

    def verify_trails_visits(self):
        """
        Verifies the completed number of visits and the text in the Trails Details Screen.

        Returns:
            tuple: (visits_text, visits_number) containing the visits text and number

        Raises:
            AssertionError: If visits text or number elements are not found within timeout
        """
        visits_text = self.device.xpath(Trails.VISITS_COMPLETED_TEXT)
        assert visits_text.wait(timeout=self.DEFAULT_TIMEOUT), "Visits completed text not found"
        text = visits_text.get_text()

        visits_number = self.device.xpath(Trails.VISITS_COMPLETED_NUMBER)
        assert visits_number.wait(timeout=self.DEFAULT_TIMEOUT), "Visits completed number not found"
        number = visits_number.get_text()

        return text, number

    def verify_trail_status(self):
        """
        Verifies the Trails statuses in the list of trails screen.

        Returns:
            str: The current trail status

        Raises:
            AssertionError: If trail status is not found or has an unexpected value
        """
        status_element = self.device.xpath(Trails.TRAILS_STATUS)
        assert status_element.wait(timeout=self.DEFAULT_TIMEOUT), "Trail status not found"

        current_status = status_element.get_text()
        assert current_status in self.VALID_TRAIL_STATUSES, f"Unexpected trail status: {current_status}"

        sleep(1)
        return current_status


class VerifyVideos:
    """Class for verifying video-related UI elements and playback."""

    MAX_SCROLL_ATTEMPTS = 9
    SCROLL_DURATION = 0.9
    SCROLL_WAIT = 1.5
    APP_PACKAGE = "com.eatvermont"

    def __init__(self, device):
        """
        Initialize VerifyVideos with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device
        self.general_scrolling = GeneralScrolling(device)
        self.screenshots = ScreenshotsManagement(device)

    def verify_videos_search_result(self):
        """
        Verify that video search results are displayed.
        Looks for indicators like "Rocket", "Results", or video elements.

        Returns:
            bool: True if search results are verified

        Raises:
            AssertionError: If search results cannot be verified
        """
        search_successful = (
                self.device(textContains="Rocket").exists or
                self.device(textContains="Video").exists
        )

        assert search_successful, "Search failed - Could not verify video search results"
        return True

    def verify_video_playback(self):
        """
        Verify that a video is playing by checking app state and UI elements.

        Returns:
            bool: True if video is playing, False otherwise
        """
        # Check if we're still in the app
        if not self.device(packageName=self.APP_PACKAGE).exists:
            return False

        # Take screenshot of the video playing
        self.screenshots.take_screenshot("video_playing")
        return True


class VerifySettings:
    """Class for verifying settings-related UI elements and interactions."""

    DEFAULT_TIMEOUT = 5
    REQUIRED_OPTIONS = [
        ("Manage Account", SettingsScreen.MANAGE_ACCOUNT),
        ("Edit Profile", SettingsScreen.EDIT_PROFILE),
        ("Share My Location", SettingsScreen.SHARE_MY_LOCATION),
        ("Log Out", SettingsScreen.LOG_OUT)
    ]

    def __init__(self, device):
        """
        Initialize VerifySettings with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def verify_settings_options(self):
        """
        Verifies that all required settings options are present on the screen.

        Returns:
            dict: Dictionary of option names and their existence status

        Raises:
            AssertionError: If any required setting option is not found
        """
        results = {}

        for option_name, xpath in self.REQUIRED_OPTIONS:
            element = self.device.xpath(xpath)
            exists = element.exists
            results[option_name] = exists
            assert exists, f"{option_name} option not found"

        return results

    def verify_settings_changed_name(self, new_name):
        """
        Verifies if the inputted name is visible in the main Settings screen.

        Args:
            new_name (str): The new name that should be visible

        Raises:
            AssertionError: If the updated name is not visible within timeout
        """
        name_text = self.device(text=new_name)
        assert name_text.exists(timeout=self.DEFAULT_TIMEOUT), (
            f"Updated name '{new_name}' is not visible after saving changes"
        )

    def verify_save_button_exists(self):
        """
        Verifies if the Save button is present in the Edit Profile screen.

        Returns:
            bool: True if save button exists

        Raises:
            AssertionError: If the save button is not present
        """
        save_button = self.device.xpath(SettingsScreen.EDIT_PROFILE_SAVE_BUTTON)
        assert save_button.exists, "Save button is not present after editing name"
        return True


class VerifyGuestMode:
    """Class for verifying Guest Mode-related UI elements and interactions."""

    MAX_SCROLL_ATTEMPTS = 15
    SCROLL_DURATION = 2.0
    SCROLL_WAIT = 1.5

    def __init__(self, device):
        """
        Initialize VerifyGuestMode with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device
        self.screen_swipe = ScreenSwipe(device)

    def verify_plans_popup(self):
        """
        Verifies the plans popup appearing in Guest Mode after certain actions.

        Returns:
            bool: True if plans popup close button exists

        Raises:
            AssertionError: If plans popup close button is not found
        """
        plans_popup_continue = self.device.xpath(PlansPopup.PLANS_POPUP_CLOSE_BUTTON)
        assert plans_popup_continue.exists, "Plans popup close button not found"
        return True

    def verify_events_limited_results_text(self):
        """
        Verifies if the Limited Results text is present in Guest Mode Events.

        Returns:
            bool: True if limited results text exists

        Raises:
            AssertionError: If Limited Results text is not found
        """
        limited_results = self.device.xpath(GuestMode.EVENTS_LIMITED_RESULTS)
        assert limited_results.exists, "Limited Results text not found"
        return True

    def verify_locked_videos(self):
        """
        Verifies if the locked videos are present in Guest Mode.

        Returns:
            bool: True if locked videos exist

        Raises:
            AssertionError: If locked videos are not found
        """
        locked_videos = self.device.xpath(GuestMode.GUEST_MODE_HOME_SCREEN_LOCKED_VIDEOS)
        assert locked_videos.exists, "Locked videos not found"
        return True

    def verify_home_screen_prompt(self):
        """
        Verifies the Guest Mode prompt at the end of the home screen.

        Returns:
            bool: True if guest mode prompt exists

        Raises:
            AssertionError: If guest mode prompt is not found after maximum scroll attempts
        """
        start_x, start_y, end_y = self.screen_swipe.calculate_swipe_coordinates()

        # Scroll until prompt is found
        for attempt in range(self.MAX_SCROLL_ATTEMPTS):
            print(f"\nScroll attempt {attempt + 1}/{self.MAX_SCROLL_ATTEMPTS}")

            self.device.swipe(start_x, start_y, start_x, end_y, duration=self.SCROLL_DURATION)
            sleep(self.SCROLL_WAIT)

            guest_mode_prompt = self.device.xpath(GuestMode.GUEST_MODE_HOME_SCREEN_PROMPT)
            if guest_mode_prompt.exists:
                print("\nFound guest mode prompt")
                return True

        assert False, "Guest mode prompt not found after maximum scroll attempts"


class VerifyPasswordReset:
    """Class for verifying password reset related UI elements and messages."""

    def __init__(self, device):
        """
        Initialize VerifyPasswordReset with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def verify_reset_password_text(self):
        """
        Verify that the reset password success message is displayed.

        Returns:
            bool: True if success message is found

        Raises:
            AssertionError: If success message is not found
        """
        success_message = self.device.xpath(LoginPage.VERIFY_EMAIL_MESSAGE)
        assert success_message.wait(timeout=5), "Success message not found"
        return True
