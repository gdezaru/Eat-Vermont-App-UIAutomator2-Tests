import pytest
import os
from time import sleep
from config import TEST_USER
from utils import handle_notification_permission, sign_in_user, handle_events_popup
from locators import LoginPage


@pytest.mark.smoke
def test_sign_in_user_password(d, screenshots_dir):
    """
    Test sign in with valid user and password
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Verify successful login
    4. Handle events popup
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

    # Check for success message
    screenshot_path = os.path.join(screenshots_dir, "1_1_1_successful_sign_in_user_password.png")
    d.screenshot(screenshot_path)


@pytest.mark.smoke
def test_forgot_password(d, screenshots_dir):
    """
    Test forgot password functionality
    Steps:
    1. Handle notification permissions
    2. Click Sign In button
    3. Click Forgot Password link
    4. Enter email address
    5. Click Reset Password button
    6. Verify confirmation message
    """
    handle_notification_permission(d)

    # Find and click Sign In button
    sign_in = None
    if d(description="Sign In").exists(timeout=5):
        sign_in = d(description="Sign In")
    elif d(text="Sign In").exists(timeout=5):
        sign_in = d(text="Sign In")

    assert sign_in is not None, "Could not find Sign In button"
    sign_in.click()
    sleep(2)

    # Click Forgot Password
    forgot_password = d.xpath(LoginPage.FORGOT_PASSWORD)
    assert forgot_password.wait(timeout=5), "Forgot Password button not found"
    forgot_password.click()
    sleep(2)

    # Enter email
    email_field = d.xpath(LoginPage.RESET_PASSWORD_EMAIL_FIELD)
    assert email_field.wait(timeout=5), "Email field not found"
    email_field.click()
    d.send_keys(TEST_USER['email'])
    sleep(1)

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