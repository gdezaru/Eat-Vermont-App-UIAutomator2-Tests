import pytest
from time import sleep
from config import TEST_USER
from locators import HomeScreen, EventsScreen
from utils import get_next_day


def test_home_screen_events(d):
    """Tests the navigation to the home screen and the events displayed."""
    # Handle notification permission if it appears
    if d(text="Allow").exists:
        d(text="Allow").click()
        sleep(1)

    # Find and click Sign In button
    sign_in = None
    if d(description="Sign In").exists(timeout=5):
        sign_in = d(description="Sign In")
    elif d(text="Sign In").exists(timeout=5):
        sign_in = d(text="Sign In")

    assert sign_in is not None, "Could not find Sign In button"
    sign_in.click()
    sleep(2)

    # Enter email
    email_field = d(text="Email")
    assert email_field.exists(timeout=5), "Email field not found"
    email_field.click()
    d.send_keys(TEST_USER['email'])
    sleep(1)

    # Enter password
    password_field = d(text="Password")
    assert password_field.exists(timeout=5), "Password field not found"
    password_field.click()
    d.send_keys(TEST_USER['password'])
    sleep(1)

    # Click Log in and verify
    login_attempts = 2
    for attempt in range(login_attempts):
        # Find and click login button
        login_button = d(text="Log in")
        assert login_button.exists(timeout=5), "Log in button not found"
        login_button.click()
        sleep(5)  # Wait for login process

        # Check for error messages
        error_messages = [
            "Invalid email or password",
            "Login failed",
            "Error",
            "Something went wrong",
            "No internet connection"
        ]

        error_found = False
        for error_msg in error_messages:
            if d(textContains=error_msg).exists(timeout=2):
                error_found = True
                break

        if error_found and attempt < login_attempts - 1:
            continue

        # Verify successful login by checking for common elements
        success_indicators = ["Events", "Home", "Profile", "Search"]
        for indicator in success_indicators:
            if d(text=indicator).exists(timeout=5):
                break
        else:
            if attempt < login_attempts - 1:
                # Try to go back if needed
                if d(text="Back").exists():
                    d(text="Back").click()
                    sleep(1)
                continue
            assert False, "Login failed - Could not verify successful login"

    # Click "See all" next to events
    events_see_all = d.xpath(HomeScreen.EVENTS_SEE_ALL)
    assert events_see_all.exists, "Could not find Events 'See all' button"
    events_see_all.click()
    sleep(15)  # Wait for events page to load
    
    # Take screenshot of events page
    d.screenshot("3_1_1_home_screen_events.png")
    
    # Find the current selected day
    days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    current_day = None
    for day in days:
        day_element = d.xpath(EventsScreen.DAY_OF_WEEK.format(day, day))  
        if day_element.exists:
            current_day = day
            print(f"\nFound current day: {day}")  
            break
    
    assert current_day is not None, "Could not find any day of week element"
    
    # Try clicking each subsequent day until one works
    current_try_day = current_day
    days_tried = 0
    max_days_to_try = 7  # Try all days of the week at most
    
    while days_tried < max_days_to_try:
        # Get the next day to try
        next_day = get_next_day(current_try_day)
        print(f"\nTrying to click on: {next_day}")
        
        # Try clicking this day multiple times
        max_attempts = 3
        click_success = False
        
        for attempt in range(max_attempts):
            next_day_element = d.xpath(EventsScreen.DAY_OF_WEEK.format(next_day, next_day))
            print(f"\nAttempt {attempt + 1}: Next day element exists: {next_day_element.exists}")
            
            if not next_day_element.exists:
                print(f"\n{next_day} not found, will try next day")
                break
            
            next_day_element.click()
            print(f"\nClicked on {next_day}")
            sleep(2)  # Wait for next day's events to load
            
            # Verify if we're now on this day by checking the events list
            events_for_day = d(textContains=next_day.title())  # e.g., "Mon" instead of "MON"
            if events_for_day.exists:
                print(f"\nSuccess! Found events for {next_day}")
                click_success = True
                break
            elif attempt < max_attempts - 1:
                print(f"\nClick might not have worked (no events found for {next_day}), trying again...")
                sleep(2)  # Wait before next attempt
            else:
                print(f"\nCould not verify events for {next_day} after {max_attempts} attempts, will try next day")
        
        if click_success:
            break
            
        # Move to next day if this one didn't work
        current_try_day = next_day
        days_tried += 1
        
        if days_tried == max_days_to_try:
            assert False, "Could not find any clickable day after trying all days of the week"
    
    # Verify that either there's an event or "No Events" message is shown
    first_event = d.xpath(EventsScreen.EVENTS_SCREEN_TILE_1)
    no_events_message = d.xpath(EventsScreen.EVENTS_SCREEN_NO_EVENTS)
    
    assert first_event.exists or no_events_message.exists, "Neither events nor 'No Events' message found"
    if first_event.exists:
        print(f"\nFound at least one event for {next_day}")
    else:
        print(f"\nNo events found for {next_day}")
    
    # Take screenshot of the successful day's events
    d.screenshot(f"3_1_2_home_screen_events_{next_day.lower()}.png")
    
    # If no event was found initially, scroll to try to find one
    if not first_event.exists and not no_events_message.exists:
        print("\nNo event visible initially, scrolling to find events...")
        max_scroll_attempts = 3
        found_event = False
        
        for scroll_attempt in range(max_scroll_attempts):
            # Scroll down
            d.swipe(0.5, 0.8, 0.5, 0.2, 0.5)  # Scroll from bottom to top
            sleep(2)  # Wait for scroll to complete
            
            # Check if we can now see an event
            first_event = d.xpath(EventsScreen.EVENTS_SCREEN_TILE_1)
            if first_event.exists:
                print(f"\nFound an event after {scroll_attempt + 1} scroll(s)")
                found_event = True
                # Take a screenshot after finding the event
                d.screenshot(f"3_1_2_home_screen_events_{next_day.lower()}_after_scroll.png")
                break
        
        if not found_event:
            print(f"\nNo events found even after {max_scroll_attempts} scrolls")
            assert no_events_message.exists, "No events found and 'No Events' message is not displayed"
    
    # Click on the first event tile if it exists
    if first_event.exists:
        print("\nClicking on the first event tile...")
        # Get the event title before clicking
        event_title = first_event.get_text()
        print(f"Event title: {event_title}")
        
        # Click the event title and wait for details to load
        first_event.click()
        sleep(2)  # Wait for event details to load
        
        # Verify we're in the event details view by checking for the event title
        event_title_in_details = d.xpath(EventsScreen.EVENT_TITLE.format(event_title))
        assert event_title_in_details.exists, f"Failed to open event details for '{event_title}'"
        
        print("\nSuccessfully opened event details")
        # Take screenshot of the event details
        d.screenshot(f"3_1_4_home_screen_event_details_{next_day.lower()}.png")
        print("\nEvent details page loaded and screenshot taken")