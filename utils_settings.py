"""
Utility functions for Settings.
"""
from time import sleep
import random
import string

from locators import HomeScreen, SettingsScreen


class EditSaveProfile:
    def __init__(self, device):
        """
        Initialize EditSaveProfile with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_settings_save_button(self):
        """
        Clicks the save button in the Edit Profile screen.

        Returns:
            bool: True if save was successful
        """
        save_button = self.device.xpath(SettingsScreen.EDIT_PROFILE_SAVE_BUTTON)
        save_button.click()
        sleep(4)
        return True

    @staticmethod
    def generate_random_name():
        """
        Generate a random name starting with 'D'.

        Returns:
            str: A random name between 5 and 10 characters, starting with 'D'
        """
        name_length = random.randint(5, 10)  # Random length between 5 and 10
        random_chars = ''.join(random.choices(string.ascii_lowercase, k=name_length - 1))
        return 'D' + random_chars

    @staticmethod
    def generate_random_username():
        """
        Generate a random username.

        Returns:
            str: A random username between 8 and 15 characters
        """
        username_length = random.randint(8, 15)  # Random length between 8 and 15
        random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
        return random_chars


class Settings:
    def __init__(self, device):
        """
        Initialize SettingsScreen with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_settings_back_button(self):
        """
        Clicks the Settings back button.

        Returns:
            bool: True if back button was clicked successfully
        """
        back_button = self.device.xpath(SettingsScreen.BACK_BUTTON_SETTINGS)
        assert back_button.exists, "Could not find Back button"
        back_button.click()
        sleep(2)
        return True

    def click_settings_button(self):
        """
        Clicks the Settings button.

        Returns:
            bool: True if settings button was clicked successfully
        """
        settings_button = self.device.xpath(HomeScreen.SETTINGS_BUTTON)
        assert settings_button.exists, "Could not find Settings button"
        settings_button.click()
        sleep(2)
        return True

    def click_edit_profile(self):
        """
        Clicks the Edit Profile button.

        Returns:
            bool: True if edit profile button was clicked successfully
        """
        edit_profile = self.device.xpath(SettingsScreen.EDIT_PROFILE)
        assert edit_profile.exists, "Could not find Edit Profile option"
        edit_profile.click()
        sleep(2)
        return True

    def click_location_toggle(self):
        """
        Click the Settings location toggle.

        Returns:
            bool: True if location toggle was clicked successfully
        """
        location_toggle = self.device.xpath(SettingsScreen.LOCATION_TOGGLE)
        assert location_toggle.exists, "Could not find Location Toggle"
        location_toggle.click()
        sleep(1)
        return True

    def click_log_out(self):
        """
        Click the Logout button.

        Returns:
            bool: True if logout button was clicked successfully
        """
        log_out = self.device.xpath(SettingsScreen.LOG_OUT)
        assert log_out.exists, "Could not find Log Out button"
        log_out.click()
        sleep(2)
        return True

    def handle_allow_button(self):
        """
        Handles the location permission if it appears.

        Returns:
            bool: True if allow button was found and clicked, False if not found
        """
        location_allow = self.device.xpath(SettingsScreen.LOCATION_ALLOW)
        if location_allow.wait(timeout=2):
            location_allow.click()
            sleep(1)
            return True
        return False

    def click_dietary_preferences(self):
        """
        Clicks the Dietary Preferences option in Settings.

        Returns:
            bool: True if dietary preferences was clicked successfully
        """
        dietary_preferences = self.device.xpath(SettingsScreen.DIETARY_PREFERENCES)
        assert dietary_preferences.exists, "Could not find Dietary Preferences option"
        dietary_preferences.click()
        sleep(2)
        return True

    def set_dietary_preferences(self, preferences):
        """
        Enters text in the dietary preferences input box.

        Args:
            preferences: Text to enter the dietary preferences field

        Returns:
            bool: True if text was entered successfully
        """
        input_box = self.device.xpath(SettingsScreen.DIETARY_PREFERENCES_INPUT_BOX)
        assert input_box.exists, "Could not find Dietary Preferences input box"
        input_box.click()
        sleep(1)

        self.device.clear_text()
        sleep(1)

        self.device.send_keys(preferences)
        sleep(1)
        return True

    def save_dietary_preferences(self):
        """
        Clicks the Save button for dietary preferences.

        Returns:
            bool: True if save button was clicked successfully
        """
        save_button = self.device.xpath(SettingsScreen.DIETARY_PREFERENCES_SAVE_BUTTON)
        assert save_button.exists, "Could not find Save button for dietary preferences"
        save_button.click()
        sleep(2)
        return True
