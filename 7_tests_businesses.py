from time import sleep
import pytest
import os

from utils_authentication import sign_in_and_prepare, SignInPrepare
from utils_device_interaction import search_and_submit
from utils_ui_navigation import click_business_with_event_search_result, click_business_fyi_tab, \
    click_business_with_menu_search_result
from utils_ui_verification import verify_businesses_section_present, verify_business_about_tab, \
    verify_business_fyi_tab_contents, verify_and_click_business_menu_tab, verify_business_menu_tab_contents

# Initialize business names at module level
business_name = "Higher Ground"
menu_business_name = "Big Fatty's BBQ"


@pytest.mark.smoke
def test_business_card_with_event(d, screenshots_dir):
    """
    Test business card functionality with event details.
    
    Steps:
    1. Sign in with test user credentials and prepare
    2. Handle events popup if it appears
    3. Navigate to the About tab
    4. Take screenshot of About tab contents
    5. Navigate to the FYI tab
    6. Take screenshot of FYI tab contents
    7. Verify all business card elements are present
    8. Verify business card navigation works correctly
    """
    sign_in = SignInPrepare(d)
    sign_in.sign_in_and_prepare()

    search_and_submit(d, business_name)

    verify_businesses_section_present(d)

    click_business_with_event_search_result(d, business_name)

    verify_business_about_tab(d)

    # Take screenshot of business details with About tab
    screenshot_path = os.path.join(screenshots_dir, "7_1_1_business_card_with_event_about_tab.png")
    d.screenshot(screenshot_path)

    click_business_fyi_tab(d)

    verify_business_fyi_tab_contents(d)

    # Take screenshot of FYI tab contents
    screenshot_path = os.path.join(screenshots_dir, "7_1_2_business_card_with_event_fyi_tab.png")
    d.screenshot(screenshot_path)


@pytest.mark.smoke
def test_business_card_with_menu(d, screenshots_dir):
    """
    Test business card functionality with menu details.
    
    Steps:
    1. Sign in with test user credentials and prepare
    2. Handle events popup if it appears
    3. Navigate to the Menu tab
    4. Take screenshot of Menu tab contents
    5. Navigate to the About tab
    6. Take screenshot of About tab contents
    7. Navigate to the FYI tab
    8. Take screenshot of FYI tab contents
    9. Verify all menu items are displayed correctly
    10. Verify business card navigation works correctly
    """
    sign_in = SignInPrepare(d)
    sign_in.sign_in_and_prepare()

    search_and_submit(d, menu_business_name)

    verify_businesses_section_present(d)

    click_business_with_menu_search_result(d, menu_business_name)

    verify_business_about_tab(d)

    # Take screenshot of business details with About tab
    screenshot_path = os.path.join(screenshots_dir, "7_2_1_business_card_with_menu_about_tab.png")
    d.screenshot(screenshot_path)

    verify_and_click_business_menu_tab(d)

    verify_business_menu_tab_contents(d)

    # Take screenshot of business details with Menu tab
    screenshot_path = os.path.join(screenshots_dir, "7_2_2_business_card_with_menu_tab.png")
    d.screenshot(screenshot_path)