import pytest

from utils_authentication import SignInPrepare
from utils_device_interaction import SearchAI
from utils_screenshots import ScreenshotsManagement
from utils_ui_navigation import NavFavoritesVisitHistory, NavBusinesses, NavCheckIn
from utils_ui_verification import VerifyBusinesses, VerifyCheckIn

# Initialize check in business name at module level
check_in_business_name = "Higher Ground"


@pytest.mark.smoke
def test_check_in_without_feedback_from_business(d, screenshots_dir):
    """
    Tests the check-in feature from a business card
    Steps:
    1. Sign in and prepare
    2. Handle events popup
    3. Searches for business via AI search
    4. Opens business card
    5. Taps the three dotted button
    6. Taps Check-In
    7. Taps Save
    8. Deletes the check-in
    """

    sign_in = SignInPrepare(d)
    nav_businesses = NavBusinesses(d)
    verify_businesses = VerifyBusinesses(d)
    click_business_menu, select_check_in, input_your_thoughts, save, tap_visit_menu, delete, yes = NavCheckIn(d)
    verify_rating = VerifyCheckIn(d)
    screenshots = ScreenshotsManagement(d)
    search_ai = SearchAI(d)

    sign_in.sign_in_and_prepare()

    search_ai.search_and_submit_ai(check_in_business_name)

    verify_businesses.verify_businesses_section_present()

    nav_businesses.click_business_with_event_search_result(check_in_business_name)

    click_business_menu.click_business_three_dotted()

    screenshots.take_screenshot("12_1_1_check_in_option_visible")

    select_check_in.click_check_in()

    input_your_thoughts.input_your_thoughts()

    save.save_check_in()

    verify_rating.verify_rating_text()

    tap_visit_menu.click_visit_history_three_dotted()

    delete.click_visit_history_delete()

    yes.click_yes()


@pytest.mark.smoke
def test_check_in_with_feedback_from_business(d, screenshots_dir):
    """
    Tests the check-in feature from a business card
    Steps:
    1. Sign in and prepare
    2. Handle events popup
    3. Searches for business via AI search
    4. Opens business card
    5. Taps the three dotted button
    6. Taps Check-In
    7. Writes a feedback in Your Thoughts text input field
    8. Taps Save
    9. Deletes the check-in
    """

    sign_in = SignInPrepare(d)
    nav_businesses = NavBusinesses(d)
    verify_businesses = VerifyBusinesses(d)
    tap_business_menu, select_check_in, input_your_thoughts, save, tap_visit_menu, delete, yes = NavCheckIn(d)
    verify_rating = VerifyCheckIn(d)
    screenshots = ScreenshotsManagement(d)
    search_ai = SearchAI(d)

    sign_in.sign_in_and_prepare()

    search_ai.search_and_submit_ai(check_in_business_name)

    verify_businesses.verify_businesses_section_present()

    nav_businesses.click_business_with_event_search_result(check_in_business_name)

    tap_business_menu.click_business_three_dotted()

    screenshots.take_screenshot("12_1_1_check_in_option_visible")

    select_check_in.click_check_in()

    screenshots.take_screenshot("12_2_1_check_in_screen_contents")

    input_your_thoughts.input_your_thoughts()

    save.save_check_in()

    verify_rating.verify_rating_text()

    screenshots.take_screenshot("12_3_1_check_in_history_contents")

    tap_visit_menu.click_visit_history_three_dotted()

    screenshots.take_screenshot("12_4_1_check_in_screen_contents")

    delete.click_visit_history_delete()

    screenshots.take_screenshot("12_5_1_check_in_deletion_popup")

    yes.click_yes()


@pytest.mark.smoke
def test_visit_history_screen(d, screenshots_dir):
    """
    Test visit history screen functionality
    Steps:
    1. Sign in and prepare
    2. Handle events popup
    3. Navigate to Favorites section
    4. Open Visit History tab
    5. Verify Visit History screen loads
    6. Take confirmation screenshot
    """
    sign_in = SignInPrepare(d)
    nav_favorites = NavFavoritesVisitHistory(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_favorites.click_favorites_button()

    nav_favorites.click_visit_history()

    screenshots.take_screenshot("12_1_1_visit_history_screen")
