import pytest
from time import sleep
from config import TEST_USER
from locators import HomeScreen, EventsScreen, ViewMap, HomeScreenTiles, BottomNavBar
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
                d.screenshot(f"3_1_3_home_screen_events_{next_day.lower()}_after_scroll.png")
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


def test_home_screen_view_map(d):
    """Tests the navigation to the home screen View Map module."""
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

        # Single scroll to show View Map
        d.swipe(0.5, 0.8, 0.5, 0.4, 0.5)
        sleep(1)

        # Click "View Map" button
        view_map = d.xpath(HomeScreen.VIEW_MAP)
        assert view_map.exists, "Could not find View Map button"
        view_map.click()
        sleep(5)
        
        # Assert that Events filter is visible
        events_filter = d.xpath(ViewMap.EVENTS_FILTER)
        assert events_filter.exists, "Events filter is not visible on the map screen"
        
        # Take screenshot of the map screen with filters
        d.screenshot("3_2_1_home_screen_view_map_opened.png")


def test_home_screen_videos(d):
    """
    Tests the navigation to the home screen Videos module.
    """
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

    # Single scroll to show Videos
    d.swipe(0.5, 0.8, 0.5, 0.4, 0.5)
    sleep(1)

    # Click "See All" in Videos section
    videos_see_all = d.xpath(HomeScreen.VIDEOS_SEE_ALL)
    assert videos_see_all.exists, "Could not find Videos See All button"
    videos_see_all.click()
    sleep(2)  # Wait for videos page to load

    # Take screenshot of the videos page
    d.screenshot("3_3_1_home_screen_videos_opened.png")


def test_home_screen_add_info(d):
    """
    Tests the navigation to the home screen Add Info module.
    """
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

        # Scroll until Add Info button is visible
        d(scrollable=True).scroll.to(text="Add Info")
        assert d(text="Add Info").exists(timeout=5), "Add Info button not found"
        sleep(1)

        # Click on Add Info button
        add_info_button = d.xpath(HomeScreen.ADD_INFO_BUTTON)
        assert add_info_button.exists, "Add Info button not found"
        add_info_button.click()
        sleep(5)

        # Take screenshot of the Add Info page
        d.screenshot("3_4_1_home_screen_add_info_opened.png")
        print("\nAdd Info page loaded and screenshot taken")


def test_home_screen_day_trips(d):
    """
    Tests the navigation to the home screen to the Day Trips module.
    """
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

    # Single scroll to show Day Trips
    d(scrollable=True).scroll.to(text="Day Trip")
    assert d(text="Day Trip").exists(timeout=5), "Day Trip text not found"
    sleep(1)

    # Click "See all" next to Day Trips
    day_trips_see_all = d.xpath(HomeScreen.DAY_TRIPS_SEE_ALL.format("Day Trip"))
    assert day_trips_see_all.exists, "Could not find Day Trip 'See all' button"
    day_trips_see_all.click()
    sleep(2)

    # Take screenshot of the Day Trips page
    d.screenshot("3_5_1_home_screen_day_trips_opened.png")
    print("\nDay Trips page loaded and screenshot taken")


def test_home_screen_events_within(d):
    """
    Tests the navigation to the home screen to the Events within ~30 minutes module.
    """
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

    # Single scroll to show Events within ~30 minutes
    d(scrollable=True).scroll.to(text="Events Within ~30min")
    assert d(text="Events Within ~30min").exists(timeout=5), "Events Within ~30min text not found"
    sleep(1)

    # Check for content in Events within 30 minutes tile
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    event_found = False
    for day in days_of_week:
        events_tile = d.xpath(HomeScreenTiles.EVENTS_WITHIN_30_TILE.format(day))
        if events_tile.exists:
            event_found = True
            break
    
    assert event_found, "Could not find any events with dates in Events within 30 minutes section"
    sleep(1)

    # Take screenshot of the Events within 30 minutes section
    d.screenshot("3_6_1_home_screen_events_within.png")
    sleep(1)

    # Click See All for Events within 30 minutes
    see_all = d(text="See All")
    assert see_all.exists, "Could not find See All button for Events within 30 minutes"
    see_all.click()
    sleep(2)  # Extra time for page transition

    # Take screenshot of the Events within 30 minutes list view
    d.screenshot("3_6_2_home_screen_events_within_list.png")
    sleep(1)


def test_home_screen_events_further_than(d):
    """
    Tests the navigation to the home screen to the Events Further Than ~30 minutes module.
    """
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

        # Single scroll to show Events within ~30 minutes
        d(scrollable=True).scroll.to(text="Events Further Than ~30min")
        assert d(text="Events Further Than ~30min").exists(timeout=5), "Events Within ~30min text not found"
        sleep(1)

        # Check for content in Events within 30 minutes tile
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        event_found = False
        for day in days_of_week:
            events_tile = d.xpath(HomeScreenTiles.EVENTS_WITHIN_30_TILE.format(day))
            if events_tile.exists:
                event_found = True
                break

        assert event_found, "Could not find any events with dates in Events within 30 minutes section"
        sleep(1)

        # Take screenshot of the Events within 30 minutes section
        d.screenshot("3_7_1_home_screen_events_further_than.png")
        sleep(1)

        # Click See All for Events within 30 minutes
        see_all = d(text="See All")
        assert see_all.exists, "Could not find See All button for Events within 30 minutes"
        see_all.click()
        sleep(2)  # Extra time for page transition

        # Take screenshot of the Events within 30 minutes list view
        d.screenshot("3_7_2_home_screen_events_more_than_list.png")
        sleep(1)


def test_home_screen_bottom_nav_bar(d):
    """
    Tests the navigation to the home screen to the bottom navigation bar.
    """
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

    # Click Favorites button
    favorites_button = d.xpath(BottomNavBar.FAVORITES)
    assert favorites_button.exists, "Could not find Favorites button"
    favorites_button.click()
    sleep(2)  # Wait for favorites page to load

    # Assert that "Favorites" text is present
    assert d(text="Favorites").exists, "Favorites text not found on screen"

    # Take screenshot
    d.screenshot("3_8_1_bottom_nav_favorites_screen.png")

    # Click Events button
    events_button = d.xpath(BottomNavBar.EVENTS)
    assert events_button.exists, "Could not find Events button"
    events_button.click()
    sleep(5)  # Wait for events page to load

    # Assert that "Events" text is present
    assert d(text="Events").exists, "Events text not found on screen"

    # Take screenshot
    d.screenshot("3_8_2_bottom_nav_events_screen.png")

    # Click Home button
    home_button = d.xpath(BottomNavBar.NAV_HOME_BUTTON)
    assert home_button.exists, "Could not find Home button"
    home_button.click()
    sleep(5)  # Wait for home page to load

    # Assert that "Eat Vermont" text is present
    assert d(text="Eat Vermont").exists, "Eat Vermont text not found on screen"

    # Take screenshot
    d.screenshot("3_8_3_bottom_nav_home_screen.png")

    # Click EAT VERMONT button
    eat_vermont_button = d.xpath(BottomNavBar.EAT_VERMONT_BUTTON)
    assert eat_vermont_button.exists, "Could not find EAT VERMONT button"
    eat_vermont_button.click()
    sleep(2)  # Wait for menu to appear

    # Assert that Check In button is visible
    check_in_button = d.xpath(BottomNavBar.CHECK_IN_BUTTON)
    assert check_in_button.exists, "Check In button not found on screen"

    # Take screenshot
    d.screenshot("3_8_4_eat_vermont_button_home_screen.png")
