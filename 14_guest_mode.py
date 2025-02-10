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
    sleep(5)  # Wait longer for popup to appear

    # Check for plans popup
    plans_popup_continue = d.xpath(PlansPopup.PLANS_POPUP_CONTINUE_BUTTON)
    if plans_popup_continue.exists:
        print("\nPlans popup is visible, clicking continue...")
        sleep(3)
        plans_popup_continue.click()
        print("Clicked continue on plans popup")
    else:
        print("\nNo plans popup found, continuing with test...")
        sleep(5)

    # Handle events popup if present
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

    # Take a confirmation screenshot
    print("\nTaking confirmation screenshot...")
    d.screenshot("14_1_1_guest_mode_button.png")


@pytest.mark.smoke
def test_guest_mode_events(d):
    """Test the Guest Mode Home screen"""
    handle_notification_permission(d)

    # Find and click Guest Mode button
    d.xpath(LoginPage.GET_STARTED).click()
    sleep(3)

    guest_mode_button = d.xpath(GuestMode.CONTINUE_AS_GUEST_BUTTON)
    assert guest_mode_button.exists, "Continue as guest button not found"
    guest_mode_button.click()
    sleep(5)  # Wait longer for popup to appear

    # Check for plans popup
    plans_popup_continue = d.xpath(PlansPopup.PLANS_POPUP_CONTINUE_BUTTON)
    if plans_popup_continue.exists:
        print("\nPlans popup is visible, clicking continue...")
        sleep(3)
        plans_popup_continue.click()
        print("Clicked continue on plans popup")
    else:
        print("\nNo plans popup found, continuing with test...")
        sleep(5)

    # Handle events popup if present
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

    # Click on Events carousel item
    print("\nLocating Events carousel item...")
    carousel_item = d.xpath(Events.CAROUSEL_ITEM)
    assert carousel_item.exists, "Could not find Events carousel item"
    print("Events carousel item found, clicking...")
    carousel_item.click()
    sleep(7)

    # Verify Limited Results text is present
    print("\nVerifying Limited Results text...")
    limited_results = d.xpath(GuestMode.EVENTS_LIMITED_RESULTS)
    assert limited_results.exists, "Limited Results text not found"
    print("Limited Results text is present")

    # Take a confirmation screenshot
    print("\nTaking confirmation screenshot...")
    d.screenshot("14_2_1_guest_mode_events.png")
