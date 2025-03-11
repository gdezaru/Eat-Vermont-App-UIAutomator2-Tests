"""
Utility functions for device interaction
"""
from time import sleep
import time
from locators import LoginPage, SettingsScreen, AskAI


class LaunchApp:
    def __init__(self, device):
        """
        Initialize LaunchApp with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device
        self.app_id = 'com.eatvermont'

    def clear_app_state(self):
        """Clear app data and restart the app"""
        print("Clearing app state...")
        self.device.app_stop(self.app_id)
        self.device.app_clear(self.app_id)
        self.device.app_start(self.app_id)
        print("App state cleared and restarted")

    def handle_notification_permission(self):
        """Handle notification permission dialogs if they appear."""
        if self.device(text="Allow").exists:
            self.device(text="Allow").click()
            sleep(1)
            if self.device(text="Allow").exists:
                self.device(text="Allow").click()
                sleep(1)


class SearchSubmit:
    def __init__(self, device):
        """
        Initialize SearchSubmit with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device
        self.search_selectors = [
            lambda: self.device(description="Search"),
            lambda: self.device(text="Search"),
            lambda: self.device(resourceId="search-input"),
            lambda: self.device(className="android.widget.EditText")
        ]

    def search_and_submit(self, search_term):
        """
        Finds the search button and field, enters a search term, and submits it.

        Args:
            search_term: The term to search for.
        """
        search_button = None
        if self.device(description="Search").exists(timeout=5):
            search_button = self.device(description="Search")
        elif self.device(text="Search").exists(timeout=5):
            search_button = self.device(text="Search")
        elif self.device(resourceId="Search").exists(timeout=5):
            search_button = self.device(resourceId="Search")
        assert search_button is not None, "Could not find Search button"
        search_button.click()
        sleep(5)
        search_field = None
        for selector in self.search_selectors:
            if selector().exists(timeout=3):
                search_field = selector()
                break
        assert search_field is not None, "Could not find search field"
        search_field.click()
        sleep(1)
        self.device.send_keys(search_term)
        sleep(1)
        self.device.press("enter")
        sleep(5)


class SearchAI:
    def __init__(self, device):
        """
        Initialize SearchAI with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device
        self.WAIT_TIME_AFTER_CLICK = 2
        self.WAIT_TIME_AFTER_TYPING = 1
        self.WAIT_TIME_FOR_AI_RESPONSE = 15

    def search_and_submit_ai(self, search_term):
        """
        Finds the Ask AI button, clicks it, enters a search term, and submits it.

        Args:
            search_term: The term to search for.
        """
        ask_ai_button = self.device.xpath(AskAI.ASKAI_ICON)
        assert ask_ai_button.exists(timeout=5), "Could not find Ask AI button"
        ask_ai_button.click()
        sleep(self.WAIT_TIME_AFTER_CLICK)
        chat_input = self.device.xpath(AskAI.CHAT_INPUT)
        assert chat_input.exists(timeout=5), "Could not find Ask Anything input field"
        chat_input.click()
        sleep(self.WAIT_TIME_AFTER_TYPING)
        self.device.send_keys(search_term)
        sleep(self.WAIT_TIME_AFTER_TYPING)
        self.device.press("enter")
        sleep(self.WAIT_TIME_FOR_AI_RESPONSE)
        assert self.device.xpath(AskAI.TEXT_AREA).exists(timeout=5), "AI did not provide a response"


class ForgotPassword:
    def __init__(self, device):
        """
        Initialize ForgotPassword with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def click_and_fill_forgot_password(self, email):
        """
        Finds and clicks the Get Started button, navigates to Forgot Password,
        and enters the email for password reset.

        Args:
            email: The email address to enter for password reset.
        """
        get_started = None
        if self.device(description="Get Started").exists(timeout=5):
            get_started = self.device(description="Get Started")
        elif self.device(text="Get Started").exists(timeout=5):
            get_started = self.device(text="Get Started")
        assert get_started is not None, "Could not find Get Started button"
        get_started.click()
        time.sleep(2)
        forgot_password = self.device.xpath(LoginPage.FORGOT_PASSWORD)
        assert forgot_password.wait(timeout=5), "Forgot Password button not found"
        forgot_password.click()
        sleep(2)
        email_field = self.device.xpath(LoginPage.RESET_PASSWORD_EMAIL_FIELD)
        assert email_field.wait(timeout=5), "Email field not found"
        email_field.click()
        self.device.send_keys(email)
        sleep(1)


class EditProfile:
    def __init__(self, device):
        """
        Initialize EditProfile with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def change_username_profile_settings(self, generate_random_username):
        """
        Changes the username in the Edit Profile screen.

        Args:
            generate_random_username: Function that generates a random username

        Returns:
            str: The new username that was set
        """
        edit_username = self.device.xpath(SettingsScreen.EDIT_USERNAME)
        assert edit_username.exists, "Could not find Username field"
        edit_username.click()
        self.device.clear_text()
        new_username = generate_random_username()
        self.device.send_keys(new_username)
        sleep(1)
        assert edit_username.get_text() == new_username, (
            f"Username was not updated correctly. Expected: {new_username},"
            f" Got: {edit_username.get_text()}")
        return new_username

    def change_name_profile_settings(self, generate_random_name):
        """
        Changes the name in the Edit Profile screen.

        Args:
            generate_random_name: Function that generates a random name

        Returns:
            str: The new name that was set
        """
        edit_name = self.device.xpath(SettingsScreen.EDIT_NAME)
        assert edit_name.exists, "Could not find Name field"
        edit_name.click()
        self.device.clear_text()
        new_name = generate_random_name()
        self.device.send_keys(new_name)
        sleep(3)
        assert edit_name.get_text() == new_name, f"Name was not updated correctly. Expected: {new_name}, Got: {edit_name.get_text()}"
        return new_name
