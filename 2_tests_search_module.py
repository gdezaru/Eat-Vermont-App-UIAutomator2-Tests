import pytest
import os
from time import sleep
from utils import handle_notification_permission, sign_in_and_prepare


@pytest.mark.smoke
def test_search_events(d, screenshots_dir):
    """
    Test searching for events functionality
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Click Search in bottom navigation
    5. Click search field
    6. Enter search term 'Burlington'
    7. Submit search
    8. Verify search results are displayed
    9. Verify results contain events
    """
    sign_in_and_prepare(d)

    # Find and click Search in bottom navigation
    search_button = None
    if d(description="Search").exists(timeout=5):
        search_button = d(description="Search")
    elif d(text="Search").exists(timeout=5):
        search_button = d(text="Search")
    elif d(resourceId="Search").exists(timeout=5):
        search_button = d(resourceId="Search")

    assert search_button is not None, "Could not find Search button"
    search_button.click()
    sleep(2)

    # Find and click search field
    search_field = None
    search_selectors = [
        lambda: d(description="Search"),
        lambda: d(text="Search"),
        lambda: d(resourceId="search-input"),
        lambda: d(className="android.widget.EditText")
    ]

    for selector in search_selectors:
        if selector().exists(timeout=3):
            search_field = selector()
            break

    assert search_field is not None, "Could not find search field"
    search_field.click()
    sleep(1)

    # Enter search term and submit
    d.send_keys("Burlington")
    sleep(1)
    d.press("enter")
    sleep(2)

    # Verify search results
    verify_attempts = 3
    for _ in range(verify_attempts):
        if (d(textContains="Burlington").exists(timeout=5) or
                d(textContains="Results").exists(timeout=5) or
                d(textContains="Event").exists(timeout=5)):
            sleep(10)
            screenshot_path = os.path.join(screenshots_dir, "2_1_search_events.png")
            d.screenshot(screenshot_path)
            return
        sleep(10)

    assert False, "Search failed - Could not verify search results"


@pytest.mark.smoke
def test_search_businesses(d, screenshots_dir):
    """
    Test searching for businesses functionality
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Click Search in bottom navigation
    5. Click search field
    6. Enter search term 'Big Fatty BBQ'
    7. Submit search
    8. Verify search results are displayed
    9. Verify results contain businesses
    """
    sign_in_and_prepare(d)

    # Find and click Search in bottom navigation
    search_button = None
    if d(description="Search").exists(timeout=5):
        search_button = d(description="Search")
    elif d(text="Search").exists(timeout=5):
        search_button = d(text="Search")
    elif d(resourceId="Search").exists(timeout=5):
        search_button = d(resourceId="Search")

    assert search_button is not None, "Could not find Search button"
    search_button.click()
    sleep(2)

    # Find and click search field
    search_field = None
    search_selectors = [
        lambda: d(description="Search"),
        lambda: d(text="Search"),
        lambda: d(resourceId="search-input"),
        lambda: d(className="android.widget.EditText")
    ]

    for selector in search_selectors:
        if selector().exists(timeout=3):
            search_field = selector()
            break

    assert search_field is not None, "Could not find search field"
    search_field.click()
    sleep(1)

    # Enter search term and submit
    d.send_keys("Big Fatty BBQ")
    sleep(1)
    d.press("enter")
    sleep(2)

    # Verify search results
    verify_attempts = 3
    for _ in range(verify_attempts):
        if (d(textContains="Big Fatty BBQ").exists(timeout=5) or
                d(textContains="Results").exists(timeout=5) or
                d(textContains="Big Fatty BBQ").exists(timeout=5)):
            sleep(10)
            screenshot_path = os.path.join(screenshots_dir, "2_2_search_business.png")
            d.screenshot(screenshot_path)
            return
        sleep(10)

    assert False, "Search failed - Could not verify search results"


@pytest.mark.smoke
def test_search_day_trips(d, screenshots_dir):
    """
    Test searching for day trips functionality
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Click Search in bottom navigation
    5. Click search field
    6. Enter search term 'Day Trip'
    7. Submit search
    8. Verify search results are displayed
    9. Verify results contain day trips
    """
    sign_in_and_prepare(d)

    # Find and click Search in bottom navigation
    search_button = None
    if d(description="Search").exists(timeout=5):
        search_button = d(description="Search")
    elif d(text="Search").exists(timeout=5):
        search_button = d(text="Search")
    elif d(resourceId="Search").exists(timeout=5):
        search_button = d(resourceId="Search")

    assert search_button is not None, "Could not find Search button"
    search_button.click()
    sleep(2)

    # Find and click search field
    search_field = None
    search_selectors = [
        lambda: d(description="Search"),
        lambda: d(text="Search"),
        lambda: d(resourceId="search-input"),
        lambda: d(className="android.widget.EditText")
    ]

    for selector in search_selectors:
        if selector().exists(timeout=3):
            search_field = selector()
            break

    assert search_field is not None, "Could not find search field"
    search_field.click()
    sleep(1)

    # Enter search term and submit
    d.send_keys("Day Trip")
    sleep(1)
    d.press("enter")
    sleep(2)

    # Verify search results
    verify_attempts = 3
    for _ in range(verify_attempts):
        if (d(textContains="Day Trip").exists(timeout=5) or
                d(textContains="Results").exists(timeout=5) or
                d(textContains="Day Trip").exists(timeout=5)):
            # Scroll to bottom of results
            screen_size = d.window_size()
            for _ in range(3):  # Scroll 3 times to ensure we reach bottom
                d.swipe(screen_size[0] * 0.5, screen_size[1] * 0.8,
                        screen_size[0] * 0.5, screen_size[1] * 0.2,
                        duration=0.5)
                sleep(2)  # Wait for content to load
            sleep(10)
            screenshot_path = os.path.join(screenshots_dir, "2_3_search_day_trips.png")
            d.screenshot(screenshot_path)
            return
        sleep(10)

    assert False, "Search failed - Could not verify search results"


@pytest.mark.smoke
def test_search_videos(d, screenshots_dir):
    """
    Test searching for videos functionality
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Click Search in bottom navigation
    5. Click search field
    6. Enter search term 'Rocket'
    7. Submit search
    8. Verify search results are displayed
    9. Verify results contain videos
    """
    sign_in_and_prepare(d)

    # Find and click Search in bottom navigation
    search_button = None
    if d(description="Search").exists(timeout=5):
        search_button = d(description="Search")
    elif d(text="Search").exists(timeout=5):
        search_button = d(text="Search")
    elif d(resourceId="Search").exists(timeout=5):
        search_button = d(resourceId="Search")

    assert search_button is not None, "Could not find Search button"
    search_button.click()
    sleep(2)

    # Find and click search field
    search_field = None
    search_selectors = [
        lambda: d(description="Search"),
        lambda: d(text="Search"),
        lambda: d(resourceId="search-input"),
        lambda: d(className="android.widget.EditText")
    ]

    for selector in search_selectors:
        if selector().exists(timeout=3):
            search_field = selector()
            break

    assert search_field is not None, "Could not find search field"
    search_field.click()
    sleep(1)

    # Enter search term and submit
    d.send_keys("Rocket")
    sleep(1)
    d.press("enter")
    sleep(2)

    # Verify search results
    verify_attempts = 3
    for _ in range(verify_attempts):
        if (d(textContains="Rocket").exists(timeout=5) or
                d(textContains="Results").exists(timeout=5) or
                d(textContains="Rocket").exists(timeout=5)):
            # Scroll to bottom of results
            screen_size = d.window_size()
            for _ in range(3):  # Scroll 3 times to ensure we reach bottom
                d.swipe(screen_size[0] * 0.5, screen_size[1] * 0.8,
                        screen_size[0] * 0.5, screen_size[1] * 0.2,
                        duration=0.5)
                sleep(2)  # Wait for content to load
            sleep(10)
            screenshot_path = os.path.join(screenshots_dir, "2_4_search_videos.png")
            d.screenshot(screenshot_path)
            return
        sleep(10)

    assert False, "Search failed - Could not verify search results"
