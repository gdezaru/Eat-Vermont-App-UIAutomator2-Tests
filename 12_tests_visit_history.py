from time import sleep
import pytest
import os
from locators import BottomNavBar, VisitHistory
from utils import (
    sign_in_and_prepare,
    click_favorites_button
)


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
    sign_in_and_prepare(d)

    # Click on Favorites button in bottom navigation
    click_favorites_button(d)
    sleep(2)

    # Click on Visit History tab
    print("\nClicking on Visit History tab...")
    visit_history_tab = d.xpath(VisitHistory.VISIT_HISTORY_TAB)
    assert visit_history_tab.exists, "Could not find Visit History tab"
    print("Found Visit History tab, clicking...")
    visit_history_tab.click()
    sleep(2)

    # Take screenshot of visit history screen
    print("\nTaking screenshot of visit history screen...")
    screenshot_path = os.path.join(screenshots_dir, "12_1_1_visit_history_screen.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 12_1_1_visit_history_screen.png")
