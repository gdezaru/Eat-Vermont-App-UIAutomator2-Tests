import pytest
import os
from time import sleep
from config import TEST_USER
from utils_authentication import SignInPrepare
from utils_device_interaction import ForgotPassword, LaunchApp
from utils_screenshots import ScreenshotsManagement
from utils_ui_navigation import NavForgotPassword
from utils_ui_verification import VerifyPasswordReset


@pytest.mark.smoke
def test_sign_in_with_valid_credentials(d, screenshots_dir):
    """
    Test sign in with valid user and password.

    Steps:
    1. Handle notification permission if it appears
    2. Click Sign In button
    3. Enter valid username
    4. Enter valid password
    5. Click Log In button
    6. Wait for successful sign in
    7. Take screenshot of successful sign in
    8. Verify user is logged in successfully
    """
    sign_in = SignInPrepare(d)
    sign_in.sign_in_and_prepare()

    # Check for success message
    screenshot_path = os.path.join(screenshots_dir, "1_1_1_successful_sign_in_user_password.png")
    d.screenshot(screenshot_path)


@pytest.mark.smoke
def test_forgot_password(d, screenshots_dir):
    """
    Test forgot password functionality.

    Steps:
    1. Handle notification permission if it appears
    2. Click Sign In button
    3. Click Forgot Password link
    4. Enter registered email address
    5. Click Send Reset Link button
    6. Take screenshot of confirmation screen
    7. Verify success message is displayed
    """
    launch_app = LaunchApp(d)
    forgot_password = ForgotPassword(d)
    nav_forgot_password = NavForgotPassword(d)
    verify_password_reset = VerifyPasswordReset(d)
    screenshots = ScreenshotsManagement(d)

    launch_app.handle_notification_permission()

    forgot_password.click_and_fill_forgot_password(TEST_USER['email'])

    nav_forgot_password.click_reset_password()

    verify_password_reset.verify_reset_password_text()

    screenshots.take_screenshot("1_2_1_forgot_password")