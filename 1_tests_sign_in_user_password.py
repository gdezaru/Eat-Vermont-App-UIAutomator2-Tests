import pytest
import os
from time import sleep
from config import TEST_USER
from utils_authentication import sign_in_and_prepare
from utils_device_interaction import handle_notification_permission, click_and_fill_forgot_password
from locators import LoginPage


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
    sign_in_and_prepare(d)

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
    handle_notification_permission(d)

    # Use utility function to click and fill forgot password
    click_and_fill_forgot_password(d, TEST_USER['email'])

    # Click Reset Password
    reset_button = d.xpath(LoginPage.RESET_PASSWORD_BUTTON)
    assert reset_button.wait(timeout=5), "Reset Password button not found"
    reset_button.click()
    sleep(5)

    # Check for success message
    success_message = d.xpath(LoginPage.VERIFY_EMAIL_MESSAGE)
    assert success_message.wait(timeout=5), "Success message not found"
    screenshot_path = os.path.join(screenshots_dir, "1_2_1_forgot_password.png")
    d.screenshot(screenshot_path)