"""
Utility functions for authentication
"""
from time import sleep
from locators import Events, PlansPopup, LoginPage, GuestMode
from utils_device_interaction import LaunchApp


class SignInPrepare:
    def __init__(self, device):
        """
        Initialize SignInPrepare with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    def sign_in_and_prepare(self):
        """Sign in and handle initial popups"""
        launch_app = LaunchApp(self.device)
        launch_app.handle_notification_permission()
        self.sign_in_user()
        self.handle_events_popup()
        sleep(5)

    def sign_in_user(self):
        """
        Sign in to the app using test user credentials.
        """
        from config import TEST_USER
        launch_app = LaunchApp(self.device)
        launch_app.handle_notification_permission()
        sleep(5)
        if self.device(description="Search").exists(timeout=2) or self.device(text="Search").exists(timeout=2):
            return
        get_started = None
        if self.device(description="Get Started").exists(timeout=5):
            get_started = self.device(description="Get Started")
        elif self.device(text="Get Started").exists(timeout=5):
            get_started = self.device(text="Get Started")
        assert get_started is not None, "Could not find Get Started button"
        get_started.click()
        sleep(2)
        email_field = self.device(text="Email")
        assert email_field.exists(timeout=5), "Email field not found"
        email_field.click()
        sleep(1)
        self.device.send_keys(TEST_USER['email'])
        sleep(1)
        password_field = self.device(text="Password")
        assert password_field.exists(timeout=5), "Password field not found"
        password_field.click()
        sleep(1)
        self.device.send_keys(TEST_USER['password'])
        sleep(1)
        login_attempts = 2
        for attempt in range(login_attempts):
            log_in_button = None
            if self.device(description="Log in").exists(timeout=5):
                log_in_button = self.device(description="Log in")
            elif self.device(text="Log in").exists(timeout=5):
                log_in_button = self.device(text="Log in")

            assert log_in_button is not None, "Could not find Log in button"
            log_in_button.click()
            sleep(5)  # Wait for login process

            # Verify successful login by checking for common elements
            success_indicators = ["Events", "Home", "Profile", "Search"]
            for indicator in success_indicators:
                if self.device(text=indicator).exists(timeout=5):
                    return  # Login successful

            if attempt < login_attempts - 1:
                # Try to go back if needed
                if self.device(text="Back").exists():
                    self.device(text="Back").click()
                    sleep(1)
                continue

            # If we get here on the last attempt, login failed
            assert False, "Login failed - Could not verify successful login"

    def handle_events_popup(self):
        """
        Handle events popup if it appears.
        """
        close_button = self.device.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
        if close_button.exists:
            close_button.click()
            sleep(2)
            return True

        events_popup = self.device.xpath(Events.EVENTS_POPUP_MAIN)
        if events_popup.exists:
            close_button = self.device.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
            if close_button.exists:
                close_button.click()
                sleep(2)
                return True
            else:
                return False

        return True


class GuestModeAuth(SignInPrepare):
    def handle_guest_mode_plans_popup(self):
        """
        Handles the plans popup in guest mode.
        """
        plans_popup_close = self.device.xpath(PlansPopup.PLANS_POPUP_CLOSE_BUTTON)
        if plans_popup_close.exists:
            sleep(2)
            plans_popup_close.click()
        else:
            sleep(2)

    def enter_guest_mode_and_handle_popups(self):
        """Enter guest mode and handle all necessary popups."""
        launch_app = LaunchApp(self.device)
        launch_app.handle_notification_permission()

        # Click Get Started
        get_started = self.device.xpath(LoginPage.GET_STARTED)
        assert get_started.exists, "Get Started button not found"
        get_started.click()
        sleep(2)

        # Click Continue as Guest
        guest_button = self.device.xpath(GuestMode.CONTINUE_AS_GUEST_BUTTON)
        assert guest_button.exists, "Continue as Guest button not found"
        guest_button.click()
        sleep(2)

        # Handle events popup if it appears
        self.handle_events_popup()

    def handle_plans_events_popups(self):
        """Handle plans popup if present."""
        guest_button = self.device.xpath(GuestMode.CONTINUE_AS_GUEST_BUTTON)
        assert guest_button.exists, "Continue as Guest button not found"
        guest_button.click()
        sleep(2)
        self.handle_guest_mode_plans_popup()
        self.handle_events_popup()
        sleep(3)
