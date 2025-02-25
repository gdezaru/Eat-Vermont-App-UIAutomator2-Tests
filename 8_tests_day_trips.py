import pytest

from utils_authentication import SignInPrepare
from utils_screenshots import ScreenshotsManagement
from utils_scrolling import ScrollToCustomDayTrips
from utils_ui_navigation import NavDayTripsTrails, NavCustomDayTrips
from utils_ui_verification import VerifyCustomDayTrips


@pytest.mark.smoke
def test_day_trip_card(d, screenshots_dir):
    """
    Test the Day Trip card on the Home screen
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Scroll to center the Day Trip section
    4. Verify Day Trip text is displayed
    5. Scroll to find Read More button
    6. Verify Read More button is displayed
    7. Tap Read More button
    8. Verify day trip details screen
    """
    sign_in = SignInPrepare(d)
    nav_trips = NavDayTripsTrails(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()
    read_more_button = nav_trips.find_day_trips_text()
    nav_trips.click_day_trips_read_more(read_more_button)

    screenshots.take_screenshot("8_1_1_day_trips_details")


@pytest.mark.smoke
def test_custom_day_trip_create_trip_screem(d, screenshots_dir):
    """
    Tests if the Custom Day Trips builder can be accessed from the home screen.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Scroll to center the Custom Day Trip section
    4. Tap Create a Custom trip
    5. Checks the contents of the "Create Trip" screen (header, Add A Location button and Quick Suggestions)
    """
    sign_in = SignInPrepare(d)
    scroll_custom_trips = ScrollToCustomDayTrips(d)
    nav_custom_trips = NavCustomDayTrips(d)
    screenshots = ScreenshotsManagement(d)
    verify_custom_trips = VerifyCustomDayTrips(d)

    sign_in.sign_in_and_prepare()

    scroll_custom_trips.scroll_to_custom_day_trips()

    nav_custom_trips.click_custom_day_trips_button()

    verify_custom_trips.verify_create_trip_header()

    verify_custom_trips.verify_add_location()

    verify_custom_trips.verify_quick_suggestions()

    screenshots.take_screenshot("8_2_1_custom_day_trips_create_trip_screen")


def test_auto_generated_day_trip_events(d, screenshots_dir):
    """
    Tests the auto generation of a Day Trip in Custom Day Trips module.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Scroll to center the Custom Day Trip section
    4. Tap Create a Custom trip
    5. Searches for a location
    6. Confirms the location
    7. Selects a date from the calendar
    8. Taps Auto-Recommend
    9. Selects Events
    10. Asserts that Advanced Filter button is present
    11. Taps Next
    12. Asserts that the Crafting Your Perfect Day Trip popup is visible
    13. Waits for the Day Trips details to load
    14. Asserts that the Location is visible
    15. Asserts that the Date is visible
    16. Asserts that the Quick Tip and Also are visible
    17. Taps the Continue button
    18. Asserts that the user is back on the home screen
    """
    sign_in = SignInPrepare(d)
    scroll_custom_trips = ScrollToCustomDayTrips(d)
    nav_custom_trips = NavCustomDayTrips(d)
    verify_custom_trips = VerifyCustomDayTrips(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    scroll_custom_trips.scroll_to_custom_day_trips()

    nav_custom_trips.click_custom_day_trips_button()

    nav_custom_trips.click_add_location()

    nav_custom_trips.search_and_pick_location("Burlington")

    nav_custom_trips.click_date_picker()

    nav_custom_trips.click_date_picker_right_arrow()

    nav_custom_trips.select_date("1")

    screenshots.take_screenshot("8_3_1_custom_day_trips_events_location_and_date_added")

    nav_custom_trips.click_auto_recommend()

    verify_custom_trips.verify_advanced_filter()

    nav_custom_trips.click_events()

    verify_custom_trips.verify_next_button()

    nav_custom_trips.click_next()

    verify_custom_trips.verify_crafting_day_trip()

    verify_custom_trips.wait_for_crafting_popup_to_disappear()

    verify_custom_trips.verify_location_details("Burlington")

    verify_custom_trips.verify_quick_tip()

    verify_custom_trips.verify_also_tip()

    verify_custom_trips.verify_continue_button()

    screenshots.take_screenshot("8_3_2_custom_day_trips_events_day_trips_details")

    nav_custom_trips.click_continue()

    nav_custom_trips.enter_trip_with_events_name()

    screenshots.take_screenshot("8_3_3_custom_day_trips_events_trip_name")

    nav_custom_trips.click_save_trip()


def test_auto_generated_day_trip_food_and_drinks(d, screenshots_dir):
    """
    Tests the auto generation of a Day Trip in Custom Day Trips module.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Scroll to center the Custom Day Trip section
    4. Tap Create a Custom trip
    5. Searches for a location
    6. Confirms the location
    7. Selects a date from the calendar
    8. Taps Auto-Recommend
    9. Selects Food + Drinks
    10. Asserts that Advanced Filter button is present
    11. Taps Next
    12. Asserts that the Crafting Your Perfect Day Trip popup is visible
    13. Waits for the Day Trips details to load
    14. Asserts that the Location is visible
    15. Asserts that the Date is visible
    16. Asserts that the Quick Tip and Also are visible
    17. Taps the Continue button
    18. Asserts that the user is back on the home screen
    """
    sign_in = SignInPrepare(d)
    scroll_custom_trips = ScrollToCustomDayTrips(d)
    nav_custom_trips = NavCustomDayTrips(d)
    verify_custom_trips = VerifyCustomDayTrips(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    scroll_custom_trips.scroll_to_custom_day_trips()

    nav_custom_trips.click_custom_day_trips_button()

    nav_custom_trips.click_add_location()

    nav_custom_trips.search_and_pick_location("Burlington")

    nav_custom_trips.click_date_picker()

    nav_custom_trips.click_date_picker_right_arrow()

    nav_custom_trips.select_date("1")

    screenshots.take_screenshot("8_4_1_custom_day_trips_events_location_and_date_added")

    nav_custom_trips.click_auto_recommend()

    verify_custom_trips.verify_advanced_filter()

    nav_custom_trips.click_food_drinks()

    verify_custom_trips.verify_next_button()

    nav_custom_trips.click_next()

    verify_custom_trips.verify_crafting_day_trip()

    verify_custom_trips.wait_for_crafting_popup_to_disappear()

    verify_custom_trips.verify_location_details("Burlington")

    verify_custom_trips.verify_quick_tip()

    verify_custom_trips.verify_also_tip()

    verify_custom_trips.verify_continue_button()

    screenshots.take_screenshot("8_4_2_custom_day_trips_food_drinks_day_trips_details")

    nav_custom_trips.click_continue()

    nav_custom_trips.enter_trip_with_food_drinks_name()

    screenshots.take_screenshot("8_4_3_custom_day_trips_food_and_drinks_trip_name")

    nav_custom_trips.click_save_trip()


def test_auto_generated_day_trip_outdoors(d, screenshots_dir):
    """
    Tests the auto generation of a Day Trip in Custom Day Trips module.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Scroll to center the Custom Day Trip section
    4. Tap Create a Custom trip
    5. Searches for a location
    6. Confirms the location
    7. Selects a date from the calendar
    8. Taps Auto-Recommend
    9. Selects Outdoors
    10. Asserts that Advanced Filter button is present
    11. Taps Next
    12. Asserts that the Crafting Your Perfect Day Trip popup is visible
    13. Waits for the Day Trips details to load
    14. Asserts that the Location is visible
    15. Asserts that the Date is visible
    16. Asserts that the Quick Tip and Also are visible
    17. Taps the Continue button
    18. Asserts that the user is back on the home screen
    """
    sign_in = SignInPrepare(d)
    scroll_custom_trips = ScrollToCustomDayTrips(d)
    nav_custom_trips = NavCustomDayTrips(d)
    verify_custom_trips = VerifyCustomDayTrips(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    scroll_custom_trips.scroll_to_custom_day_trips()

    nav_custom_trips.click_custom_day_trips_button()

    nav_custom_trips.click_add_location()

    nav_custom_trips.search_and_pick_location("Burlington")

    nav_custom_trips.click_date_picker()

    nav_custom_trips.click_date_picker_right_arrow()

    nav_custom_trips.select_date("1")

    screenshots.take_screenshot("8_5_1_custom_day_trips_events_location_and_date_added")

    nav_custom_trips.click_auto_recommend()

    verify_custom_trips.verify_advanced_filter()

    nav_custom_trips.click_outdoors()

    verify_custom_trips.verify_next_button()

    nav_custom_trips.click_next()

    verify_custom_trips.verify_crafting_day_trip()

    verify_custom_trips.wait_for_crafting_popup_to_disappear()

    verify_custom_trips.verify_location_details("Burlington")

    verify_custom_trips.verify_quick_tip()

    verify_custom_trips.verify_also_tip()

    verify_custom_trips.verify_continue_button()

    screenshots.take_screenshot("8_5_2_custom_day_trips_outdoors_day_trips_details")

    nav_custom_trips.click_continue()

    nav_custom_trips.enter_trip_with_outdoors_name()

    screenshots.take_screenshot("8_5_3_custom_day_trips_outdoors_trip_name")

    nav_custom_trips.click_save_trip()


def test_auto_generated_day_trip_points_of_interest(d, screenshots_dir):
    """
    Tests the auto generation of a Day Trip in Custom Day Trips module.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Scroll to center the Custom Day Trip section
    4. Tap Create a Custom trip
    5. Searches for a location
    6. Confirms the location
    7. Selects a date from the calendar
    8. Taps Auto-Recommend
    9. Selects Points of Interest
    10. Asserts that Advanced Filter button is present
    11. Taps Next
    12. Asserts that the Crafting Your Perfect Day Trip popup is visible
    13. Waits for the Day Trips details to load
    14. Asserts that the Location is visible
    15. Asserts that the Date is visible
    16. Asserts that the Quick Tip and Also are visible
    17. Taps the Continue button
    18. Asserts that the user is back on the home screen
    """
    sign_in = SignInPrepare(d)
    scroll_custom_trips = ScrollToCustomDayTrips(d)
    nav_custom_trips = NavCustomDayTrips(d)
    verify_custom_trips = VerifyCustomDayTrips(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    scroll_custom_trips.scroll_to_custom_day_trips()

    nav_custom_trips.click_custom_day_trips_button()

    nav_custom_trips.click_add_location()

    nav_custom_trips.search_and_pick_location("Burlington")

    nav_custom_trips.click_date_picker()

    nav_custom_trips.click_date_picker_right_arrow()

    nav_custom_trips.select_date("1")

    screenshots.take_screenshot("8_6_1_custom_day_trips_events_location_and_date_added")

    nav_custom_trips.click_auto_recommend()

    verify_custom_trips.verify_advanced_filter()

    nav_custom_trips.click_points_of_interest()

    verify_custom_trips.verify_next_button()

    nav_custom_trips.click_next()

    verify_custom_trips.verify_crafting_day_trip()

    verify_custom_trips.wait_for_crafting_popup_to_disappear()

    verify_custom_trips.verify_location_details("Burlington")

    verify_custom_trips.verify_quick_tip()

    verify_custom_trips.verify_also_tip()

    verify_custom_trips.verify_continue_button()

    screenshots.take_screenshot("8_6_2_custom_day_trips_points_interest_day_trips_details")

    nav_custom_trips.click_continue()

    nav_custom_trips.enter_trip_with_points_of_interest_name()

    screenshots.take_screenshot("8_6_3_custom_day_trips_points_of_interest_trip_name")

    nav_custom_trips.click_save_trip()


def test_auto_generated_day_trip_events_details(d, screenshots_dir):
    """
    Test goes to My Trips tab and checks the contents of the previously generated day trip.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Scroll to center the Custom Day Trip section
    4. Taps See All
    5. Taps My Trips tab
    6. Opens the details of the Day Trip Containing Events
    7. Asserts that a date is present
    8. Asserts that the number of places section is present
    9. Scrolls to the bottom of the page
    10. Asserts that the number of the last item matches the number of places
    11. Deletes the Day Trip
    """
    sign_in = SignInPrepare(d)
    nav_trips = NavDayTripsTrails(d)
    nav_custom_trips = NavCustomDayTrips(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_trips.find_day_trips_text()

    nav_trips.click_day_trips_see_all()

    nav_custom_trips.click_my_trips()

    screenshots.take_screenshot("8_7_1_custom_day_trips_my_trips")


def test_auto_generated_day_trip_food_and_drinks_details(d, screenshots_dir):
    """
    Test goes to My Trips tab and checks the contents of the previously generated day trip.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Scroll to center the Custom Day Trip section
    4. Taps See All
    5. Taps My Trips tab
    6. Opens the details of the Day Trip Containing Food + Drinks
    7. Asserts that a date is present
    8. Asserts that the number of places section is present
    9. Scrolls to the bottom of the page
    10. Asserts that the number of the last item matches the number of places
    11. Deletes the Day Trip
    """
    sign_in = SignInPrepare(d)
    nav_trips = NavDayTripsTrails(d)
    nav_custom_trips = NavCustomDayTrips(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_trips.find_day_trips_text()

    nav_trips.click_day_trips_see_all()

    nav_custom_trips.click_my_trips()

    screenshots.take_screenshot("8_8_1_custom_day_trips_my_trips")


def test_auto_generated_day_trip_outdoors_details(d, screenshots_dir):
    """
    Test goes to My Trips tab and checks the contents of the previously generated day trip.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Scroll to center the Custom Day Trip section
    4. Taps See All
    5. Taps My Trips tab
    6. Opens the details of the Day Trip Containing Outdoors
    7. Asserts that a date is present
    8. Asserts that the number of places section is present
    9. Scrolls to the bottom of the page
    10. Asserts that the number of the last item matches the number of places
    11. Deletes the Day Trip
    """
    sign_in = SignInPrepare(d)
    nav_trips = NavDayTripsTrails(d)
    nav_custom_trips = NavCustomDayTrips(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_trips.find_day_trips_text()

    nav_trips.click_day_trips_see_all()

    nav_custom_trips.click_my_trips()

    screenshots.take_screenshot("8_9_1_custom_day_trips_my_trips")


def test_auto_generated_day_trip_points_of_interest_details(d, screenshots_dir):
    """
    Test goes to My Trips tab and checks the contents of the previously generated day trip.
    Steps:
    1. Sign in with valid credentials
    2. Handle events popup
    3. Scroll to center the Custom Day Trip section
    4. Taps See All
    5. Taps My Trips tab
    6. Opens the details of the Day Trip Containing Points of Interest
    7. Asserts that a date is present
    8. Asserts that the number of places section is present
    9. Scrolls to the bottom of the page
    10. Asserts that the number of the last item matches the number of places
    11. Deletes the Day Trip
    """
    sign_in = SignInPrepare(d)
    nav_trips = NavDayTripsTrails(d)
    nav_custom_trips = NavCustomDayTrips(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_trips.find_day_trips_text()

    nav_trips.click_day_trips_see_all()

    nav_custom_trips.click_my_trips()

    screenshots.take_screenshot("8_10_1_custom_day_trips_my_trips")