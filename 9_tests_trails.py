from time import sleep
from locators import HomeScreen, Trails
from utils import sign_in_user, handle_events_popup, handle_notification_permission
import pytest
from retry_decorator import retry


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_trails_screen(d):
    """
    Test the Trails functionality
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Navigate to Trails section
    5. Find and verify any trail name
    6. Verify trail status
    7. Take screenshot of trails main screen
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

    # Click on Trails button
    print("\nClicking on Trails button...")
    trails_button = d.xpath(HomeScreen.TRAILS_BUTTON)
    assert trails_button.wait(timeout=5), "Trails button not found"
    trails_button.click()
    sleep(2)

    # Find and verify any trail name
    print("\nFinding trail name...")
    # First find any TextView containing "Trail" to get its text
    trail_text = d(textContains="Trail").get_text()
    print(f"Found trail: {trail_text}")

    # Now use that text with our TRAIL_NAME locator
    trail_element = d.xpath(Trails.TRAIL_NAME.format(trail_text))
    assert trail_element.wait(timeout=5), f"Trail element not found"
    sleep(1)

    # Verify trail status
    print("\nChecking trail status...")
    status_element = d.xpath(Trails.TRAILS_STATUS)
    assert status_element.wait(timeout=5), "Trail status not found"
    current_status = status_element.get_text()
    print(f"Trail status is: {current_status}")
    assert current_status in ["Not Started", "In Progress", "Complete"], f"Unexpected trail status: {current_status}"
    sleep(1)

    # Take screenshot of trails main screen
    print("\nTaking screenshot of trails main screen...")
    d.screenshot("9_1_1_trails_main_screen.png")
    sleep(1)


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_trails_details(d):
    """
    Test the Trails details screen
    Steps:
    1. Handle notification permissions
    2. Sign in with valid credentials
    3. Handle events popup
    4. Navigate to Trails section
    5. Click Read More button
    6. Verify percentage progress
    7. Verify visits completed text and number
    8. Take screenshot of trail details
    9. Scroll using swipe
    10. Take screenshot of trail details visits
    """
    handle_notification_permission(d)
    # Sign in using the utility method
    sign_in_user(d)

    # Handle events popup using the utility method
    handle_events_popup(d)
    sleep(10)

    # Click on Trails button
    print("\nClicking on Trails button...")
    trails_button = d.xpath(HomeScreen.TRAILS_BUTTON)
    assert trails_button.wait(timeout=5), "Trails button not found"
    trails_button.click()
    sleep(2)

    # Click Read More button
    print("\nClicking Read More button...")
    read_more_button = d.xpath(Trails.READ_MORE_TRAILS)
    assert read_more_button.wait(timeout=5), "Read More button not found"
    read_more_button.click()
    sleep(5)  # Increased wait time

    # Verify percentage progress
    print("\nVerifying percentage progress...")
    percentage_element = d.xpath(Trails.PERCENTAGE_PROGRESS)
    assert percentage_element.wait(timeout=5), "Percentage progress not found"
    percentage = percentage_element.get_text()
    print(f"Trail progress: {percentage}")

    # Verify visits completed text and number
    print("\nVerifying visits completed...")
    visits_text = d.xpath(Trails.VISITS_COMPLETED_TEXT)
    assert visits_text.wait(timeout=5), "Visits completed text not found"

    visits_number = d.xpath(Trails.VISITS_COMPLETED_NUMBER)
    assert visits_number.wait(timeout=5), "Visits completed number not found"
    visits = visits_number.get_text()
    print(f"Visits completed: {visits}")

    # Take screenshot of trail details
    print("\nTaking screenshot of trail details...")
    d.screenshot("9_2_1_trail_details.png")
    sleep(1)

    # Scroll using swipe
    print("\nScrolling using swipe...")
    screen_size = d.window_size()
    start_x = screen_size[0] * 0.5
    start_y = screen_size[1] * 0.8  # Start from 80% of screen height
    end_y = screen_size[1] * 0.2  # End at 20% of screen height

    for _ in range(3):  # Do multiple swipes
        d.swipe(start_x, start_y, start_x, end_y, duration=0.5)
        sleep(1)

    print("\nTaking screenshot of trail details visits...")
    d.screenshot("9_2_2_trail_details_visits.png")
    sleep(1)
