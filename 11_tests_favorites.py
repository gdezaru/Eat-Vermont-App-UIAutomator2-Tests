import pytest

from utils_authentication import SignInPrepare
from utils_device_interaction import SearchSubmit
from utils_ui_navigation import NavFavoritesVisitHistory, NavBusinesses, NavDayTripsTrails, NavEvents
from utils_screenshots import ScreenshotsManagement
from utils_ui_verification import VerifyBusinesses

# Initialize business names at module level
business_name = "Higher Ground"
menu_business_name = "Big Fatty's BBQ"


@pytest.mark.smoke
def test_add_favorite_events(d, screenshots_dir):
    """
    Tests the ability to add events to My Favorites.
    Steps:
    1. Sign in using the utility method
    2. Handle events popup using the utility method
    3. Interact with Events carousel item
    4. Find and click the favorite icon
    5. Take screenshot
    """
    sign_in = SignInPrepare(d)
    search = SearchSubmit(d)
    nav_events = NavEvents(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    search_term = "Burlington"
    search.search_and_submit(search_term)

    nav_events.click_first_event_search_result()

    nav_events.add_favorite_event()

    screenshots.take_screenshot("11_1_1_event_favorited.png")


@pytest.mark.smoke
def test_add_favorite_businesses(d, screenshots_dir):
    """
    Tests the ability to add businesses to My Favorites.
    Steps:
    1. Sign in using the utility method
    2. Handle events popup using the utility method
    3. Find and click Search in bottom navigation
    4. Find and click search field
    5. Enter search term and submit
    6. Wait for and verify Businesses section is present
    7. Click on Big Fatty's BBQ search result under Businesses
    8. Find and click the favorite icon
    9. Take screenshot of favorited business
    """
    sign_in = SignInPrepare(d)
    search = SearchSubmit(d)
    nav_business = NavBusinesses(d)
    verify_business = VerifyBusinesses(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    search.search_and_submit(menu_business_name)

    verify_business.verify_businesses_section_present()

    nav_business.click_first_business_search_result(menu_business_name)

    nav_business.add_favorite_business()

    screenshots.take_screenshot("11_2_1_business_favorited.png")


@pytest.mark.smoke
def test_add_favorite_trails(d, screenshots_dir):
    """
    Tests the ability to add trails to My Favorites.
    Steps:
    1. Sign in using the utility method
    2. Handle events popup using the utility method
    3. Click on Trails button
    4. Find and click the favorite icon
    5. Take screenshot of favorited trail
    """
    sign_in = SignInPrepare(d)
    nav_trails = NavDayTripsTrails(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_trails.find_trails_text()

    nav_trails.click_trails_read_more()

    nav_trails.add_favorite_trail()

    screenshots.take_screenshot("11_4_1_trail_favorited.png")


@pytest.mark.smoke
def test_remove_favorite_events(d, screenshots_dir):
    """
    Tests the ability to remove events from My Favorites.
    Steps:
    1. Sign in using the utility method
    2. Handle events popup using the utility method
    3. Click on Favorites button in bottom navigation
    4. Verify favorited event is present and take screenshot
    5. Click on favorite icon to remove from favorites
    6. Verify event is no longer in favorites
    """
    sign_in = SignInPrepare(d)
    nav_favorites = NavFavoritesVisitHistory(d)
    nav_events = NavEvents(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_favorites.click_favorites_button()

    screenshots.take_screenshot("11_5_1_favorited_event_before_removal.png")

    nav_events.verify_and_remove_favorite_event()

    screenshots.take_screenshot("11_5_2_favorites_after_removal.png")


@pytest.mark.smoke
def test_remove_favorite_businesses(d, screenshots_dir):
    """
    Tests the ability to remove businesses from My Favorites.
    Steps:
    1. Sign in using the utility method
    2. Handle events popup using the utility method
    3. Click on Favorites button in bottom navigation
    4. Verify favorited business is present and take screenshot
    5. Click on favorite icon to remove from favorites
    6. Verify business is no longer in favorites
    """
    sign_in = SignInPrepare(d)
    nav_favorites = NavFavoritesVisitHistory(d)
    nav_business = NavBusinesses(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_favorites.click_favorites_button()

    screenshots.take_screenshot("11_6_1_favorited_business_before_removal.png")

    nav_business.verify_and_remove_favorite_business()

    screenshots.take_screenshot("11_6_2_favorites_after_removal.png")


@pytest.mark.smoke
def test_remove_favorite_trails(d, screenshots_dir):
    """
    Tests the ability to remove trails from My Favorites.
    Steps:
    1. Sign in using the utility method
    2. Handle events popup using the utility method
    3. Click on Favorites button in bottom navigation
    4. Verify favorited trail is present and take screenshot
    5. Click on favorite icon to remove from favorites
    6. Verify trail is no longer in favorites
    """
    sign_in = SignInPrepare(d)
    nav_favorites = NavFavoritesVisitHistory(d)
    nav_trails = NavDayTripsTrails(d)
    screenshots = ScreenshotsManagement(d)

    sign_in.sign_in_and_prepare()

    nav_favorites.click_favorites_button()

    screenshots.take_screenshot("11_8_1_favorited_trail_before_removal.png")

    nav_trails.verify_and_remove_favorite_trail()

    screenshots.take_screenshot("11_8_2_favorites_after_removal.png")
