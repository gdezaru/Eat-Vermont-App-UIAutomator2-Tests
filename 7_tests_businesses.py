import pytest

from utils_authentication import SignInPrepare
from utils_ui_navigation import NavBusinesses
from utils_ui_verification import VerifyBusinesses
from utils_screenshots import ScreenshotsManagement
from utils_device_interaction import SearchSubmit

# Initialize business names at module level
business_name = "Higher Ground"
menu_business_name = "Big Fatty's BBQ"


@pytest.mark.smoke
def test_business_card_with_event(d, screenshots_dir):
    """
    Test business card functionality with event details.
    
    Steps:
    1. Sign in with test user credentials and prepare
    2. Handle events popup if it appears
    3. Searches for business with menu (Higher Ground)
    4. Clicks on the search result to open the business card
    5. Verifies the contents of the About tab
    6. Switches to the FYI tab
    7. Verifies the contents of the FYI tab
    """
    sign_in = SignInPrepare(d)
    nav_businesses = NavBusinesses(d)
    verify_businesses = VerifyBusinesses(d)
    screenshots = ScreenshotsManagement(d)
    search = SearchSubmit(d)

    sign_in.sign_in_and_prepare()

    search.search_and_submit(business_name)
    verify_businesses.verify_businesses_section_present()
    nav_businesses.click_business_with_event_search_result(business_name)

    verify_businesses.verify_business_about_tab()

    screenshots.take_screenshot("7_1_1_business_card_with_event_about_tab")

    verify_businesses.verify_and_click_business_fyi_tab()
    verify_businesses.verify_business_fyi_tab_contents()

    screenshots.take_screenshot("7_1_2_business_card_with_event_fyi_tab")


@pytest.mark.smoke
def test_business_card_with_menu(d, screenshots_dir):
    """
    Test business card functionality with menu details.
    
    Steps:
    1. Sign in with test user credentials and prepare
    2. Handle events popup if it appears
    3. Searches for business with menu (Big Fatty's BBQ)
    4. Clicks on the search result to open the business card
    5. Verifies the contents of the About tab
    6. Switches to the Menu tab
    7. Verifies the contents of the Menu tab
    """
    sign_in = SignInPrepare(d)
    nav_businesses = NavBusinesses(d)
    verify_businesses = VerifyBusinesses(d)
    screenshots = ScreenshotsManagement(d)
    search = SearchSubmit(d)

    sign_in.sign_in_and_prepare()

    search.search_and_submit(menu_business_name)
    verify_businesses.verify_businesses_section_present()
    nav_businesses.click_business_with_menu_search_result(menu_business_name)

    verify_businesses.verify_business_about_tab()

    screenshots.take_screenshot("7_2_1_business_card_with_menu_about_tab")

    verify_businesses.verify_and_click_business_menu_tab()
    verify_businesses.verify_business_menu_tab_contents()

    screenshots.take_screenshot("7_2_2_business_card_with_menu_tab")