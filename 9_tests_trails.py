from time import sleep
from locators import HomeScreen, Trails
from utils import sign_in_and_prepare, click_trails_button, scroll_to_bottom
import pytest
import os


@pytest.mark.smoke
def test_trails_screen(d, screenshots_dir):
    """
    Test the Trails functionality
    Steps:
    1. Sign in and prepare
    2. Navigate to Trails section
    3. Find and verify any trail name
    4. Verify trail status
    5. Take screenshot of trails main screen
    """
    sign_in_and_prepare(d)

    # Use utility function to click Trails button
    click_trails_button(d)
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
    screenshot_path = os.path.join(screenshots_dir, "9_1_1_trails_main_screen.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 9_1_1_trails_main_screen.png")
    sleep(1)


@pytest.mark.smoke
def test_trails_details(d, screenshots_dir):
    """
    Test the Trails details screen
    Steps:
    1. Sign in and prepare
    2. Navigate to Trails section
    3. Click Read More button
    4. Verify percentage progress
    5. Verify visits completed text and number
    6. Take screenshot of trail details
    7. Scroll using swipe
    8. Take screenshot of trail details visits
    """
    sign_in_and_prepare(d)

    # Use utility function to click Trails button
    click_trails_button(d)
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
    screenshot_path = os.path.join(screenshots_dir, "9_2_1_trail_details.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 9_2_1_trail_details.png")
    sleep(1)

    # Use utility function to scroll to bottom of results
    scroll_to_bottom(d)

    print("\nTaking screenshot of trail details visits...")
    screenshot_path = os.path.join(screenshots_dir, "9_2_2_trail_details_visits.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 9_2_2_trail_details_visits.png")
    sleep(1)
