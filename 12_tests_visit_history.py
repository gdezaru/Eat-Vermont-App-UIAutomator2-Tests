import pytest

from utils_authentication import SignInPrepare
from utils_screenshots import ScreenshotsManagement
from utils_ui_navigation import NavFavoritesVisitHistory


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
