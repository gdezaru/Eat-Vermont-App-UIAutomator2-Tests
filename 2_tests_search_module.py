import pytest
from time import sleep
from config import TEST_USER
from locators import Events
from utils import handle_notification_permission, sign_in_user, handle_events_popup
from retry_decorator import retry

@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_search_events(d):
    """Test searching for events"""
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

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
            d.screenshot("2_1_search_events.png")
            return
        sleep(10)

    assert False, "Search failed - Could not verify search results"


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_search_businesses(d):
    """Test searching for businesses"""
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

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
            d.screenshot("2_2_search_business.png")
            return
        sleep(10)

    assert False, "Search failed - Could not verify search results"


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_search_day_trips(d):
    """Test searching for day trips"""
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

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
            d.screenshot("2_3_search_day_trips.png")
            return
        sleep(10)

    assert False, "Search failed - Could not verify search results"


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_search_videos(d):
    """Test searching for videos"""
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

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
            d.screenshot("2_4_search_videos.png")
            return
        sleep(10)

    assert False, "Search failed - Could not verify search results"
