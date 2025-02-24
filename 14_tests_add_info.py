import pytest

from utils_authentication import SignInPrepare
from utils_screenshots import ScreenshotsManagement
from utils_scrolling import ScrollAddInfo
from utils_ui_navigation import NavAddInfo, AddInfoActions


@pytest.mark.smoke
def test_add_info_without_photo(d, screenshots_dir):
    """
    Test home screen add info module functionality
    Steps:
    1. Sign in with valid credentials and prepare
    2. Find and click Add Info
    3. Fill in business name
    4. Fill in information
    5. Tap Submit
    6. Assert that the confirmation popup is present
    7. Taps the Cheers button
    8. Asserts that the confirmation popup has been closed
    """
    sign_in = SignInPrepare(d)
    nav_add_info = NavAddInfo(d)
    scroll_add_info = ScrollAddInfo(d)
    screenshots = ScreenshotsManagement(d)
    add_info = AddInfoActions(d)

    sign_in.sign_in_and_prepare()

    scroll_add_info.scroll_to_add_info()

    nav_add_info.click_add_info_button()

    add_info.input_business_name("Test Business")

    screenshots.take_screenshot("14_1_1_add_info_business_name_filled")

    add_info.input_update_info("New test update info")

    screenshots.take_screenshot("14_2_1_add_info_details_filled")

    add_info.click_submit_button()

    screenshots.take_screenshot("14_3_1_add_info_confirmation_popup_visible")

    add_info.click_cheers_button()

    screenshots.take_screenshot("14_4_1_add_info_confirmation_popup_closed")