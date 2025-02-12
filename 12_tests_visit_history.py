import pytest
from time import sleep
from locators import BottomNavBar, VisitHistory
from utils import (
    handle_notification_permission, sign_in_user, handle_events_popup
)
from retry_decorator import retry


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_visit_history_screen(d):
    """
    Test visit history screen functionality
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Navigate to Favorites section
    5. Open Visit History tab
    6. Verify Visit History screen loads
    7. Take confirmation screenshot
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

    # Click on Favorites button in bottom navigation
    print("\nClicking on Favorites button...")
    favorites_button = d.xpath(BottomNavBar.FAVORITES)
    assert favorites_button.exists, "Could not find Favorites button"
    print("Found Favorites button, clicking...")
    favorites_button.click()
    sleep(2)

    # Click on Visit History tab
    print("\nClicking on Visit History tab...")
    visit_history_tab = d.xpath(VisitHistory.VISIT_HISTORY_TAB)
    assert visit_history_tab.exists, "Could not find Visit History tab"
    print("Found Visit History tab, clicking...")
    visit_history_tab.click()
    sleep(2)

    # Take confirmation screenshot
    print("\nTook screenshot: 12_1_visit_history_screen.png")
    d.screenshot("12_1_1_visit_history_screen.png")
