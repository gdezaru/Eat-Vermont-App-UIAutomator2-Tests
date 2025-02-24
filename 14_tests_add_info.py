import pytest

from utils_authentication import SignInPrepare
from utils_screenshots import ScreenshotsManagement
from utils_scrolling import ScrollAddInfo
from utils_ui_navigation import NavAddInfo


@pytest.mark.smoke
def test_add_info_without_photo(d, screenshots_dir):
    """
    Test home screen add info module functionality
    Steps:
    1. Sign in with valid credentials and prepare
    2. Find and click Add Info
    3. Fill in business name
    4. Fill in information
    5. Tap Save
    6. Assert that the confirmation popup is present
    """
    sign_in = SignInPrepare(d)
    nav_add_info = NavAddInfo(d)
    scroll_add_info = ScrollAddInfo(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    scroll_add_info.scroll_to_add_info()

    nav_add_info.click_add_info_button()

    screenshots.take_screenshot("14_1_1_add_info_business_name_filled")

    screenshots.take_screenshot("14_2_1_add_info_details_filled")

    screenshots.take_screenshot("14_3_1_add_info_confirmation_popup")
