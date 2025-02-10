import pytest
from time import sleep
from locators import Events, GuestMode, LoginPage, PlansPopup
from utils import handle_notification_permission


@pytest.mark.smoke
def test_guest_mode_button(d):
    """Test the Guest Mode Home screen"""
    handle_notification_permission(d)

    # Find and click Guest Mode button
    d.xpath(LoginPage.GET_STARTED).click()
    sleep(3)
    
    guest_mode_button = d.xpath(GuestMode.CONTINUE_AS_GUEST_BUTTON)
    assert guest_mode_button.exists, "Continue as guest button not found"
    guest_mode_button.click()

    # Handle plans popup if present
    plans_popup_close = d.xpath(PlansPopup.PLANS_POPUP_CLOSE_BUTTON)
    if plans_popup_close.exists:
        print("\nPlans popup is visible, closing it...")
        plans_popup_close.click()
    else:
        print("\nNo plans popup found, continuing with test...")

    events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
    if events_popup.exists:
        print("\nEvents popup is visible, closing it...")
        sleep(3)
        close_button = d.xpath(Events.EVENTS_POPUP_CLOSE_BUTTON)
        print("\nChecking close button...")
        print(f"Close button exists: {close_button.exists}")
        if close_button.exists:
            print(f"Close button info: {close_button.info}")
        assert close_button.exists, "Close button not found on events popup"
        print("\nAttempting to click close button...")
        close_button.click()
        print("\nClose button clicked")
        sleep(3)

        # Verify popup is closed
        print("\nVerifying popup is closed...")
        events_popup = d.xpath(Events.EVENTS_POPUP_MAIN)
        assert not events_popup.exists, "Events popup is still visible after clicking close button"
        print("Events popup successfully closed")
    else:
        print("\nNo events popup found, continuing with next steps...")


