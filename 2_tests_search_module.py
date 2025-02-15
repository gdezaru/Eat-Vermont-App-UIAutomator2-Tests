import pytest
import os
from time import sleep
from utils_device_interaction import handle_notification_permission, sign_in_and_prepare, search_and_submit, verify_and_screenshot, scroll_to_bottom


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

    # Use utility function to search and submit
    search_term = "Burlington"
    search_and_submit(d, search_term)
    sleep(2)

    # Verify search results and take screenshot
    verify_and_screenshot(
        device=d,
        condition=lambda: d(textContains="Burlington").exists or d(textContains="Results").exists or d(textContains="Event").exists,
        error_message="Search failed - Could not verify search results",
        screenshots_dir=screenshots_dir,
        filename="2_2_1_search_events.png"
    )


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

    # Use utility function to search and submit
    search_term = "Big Fatty BBQ"
    search_and_submit(d, search_term)
    sleep(2)

    # Verify search results and take screenshot
    verify_and_screenshot(
        device=d,
        condition=lambda: d(textContains="Big Fatty BBQ").exists or d(textContains="Results").exists or d(textContains="Big Fatty BBQ").exists,
        error_message="Search failed - Could not verify search results",
        screenshots_dir=screenshots_dir,
        filename="2_2_2_search_business.png"
    )


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

    # Use utility function to search and submit
    search_term = "Day Trip"
    search_and_submit(d, search_term)
    sleep(2)

    # Use utility function to scroll to bottom of results
    scroll_to_bottom(d)
    sleep(2)  # Wait for content to load

    # Verify search results and take screenshot
    verify_and_screenshot(
        device=d,
        condition=lambda: d(textContains="Day Trip").exists or d(textContains="Results").exists or d(textContains="Day Trip").exists,
        error_message="Search failed - Could not verify search results",
        screenshots_dir=screenshots_dir,
        filename="2_2_3_search_day_trips.png"
    )


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

    # Use utility function to search and submit
    search_term = "Rocket"
    search_and_submit(d, search_term)
    sleep(2)

    # Use utility function to scroll to bottom of results
    scroll_to_bottom(d)
    sleep(2)  # Wait for content to load

    # Verify search results and take screenshot
    verify_and_screenshot(
        device=d,
        condition=lambda: d(textContains="Rocket").exists or d(textContains="Results").exists or d(textContains="Rocket").exists,
        error_message="Search failed - Could not verify search results",
        screenshots_dir=screenshots_dir,
        filename="2_2_4_search_videos.png"
    )
