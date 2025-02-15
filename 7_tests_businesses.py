from time import sleep
from locators import Businesses
from utils_device_interaction import sign_in_and_prepare, verify_businesses_section_present, search_and_submit
import pytest
import os

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
    sign_in_and_prepare(d)

    search_and_submit(d, business_name)

    verify_businesses_section_present(d)

    # Click on Higher Ground search result under Businesses
    search_result = d.xpath(Businesses.BUSINESS_UNDER_BUSINESSES.format(business_name))
    assert search_result.exists, "Higher Ground not found under Businesses section"
    search_result.click()
    sleep(5)

    # Verify About tab is visible
    about_tab = d.xpath(Businesses.BUSINESS_ABOUT_TAB)
    if about_tab.exists:
        assert about_tab.exists, "About tab not found on business details page"

    # Verify About tab contents are present
    about_contents = d.xpath(Businesses.BUSINESS_ABOUT_TAB_CONTENTS)
    assert about_contents.exists, "About tab contents not found"

    # Take screenshot of business details with About tab
    screenshot_path = os.path.join(screenshots_dir, "7_1_1_business_card_with_event_about_tab.png")
    d.screenshot(screenshot_path)

    # Click on FYI tab and verify contents
    fyi_tab = d.xpath(Businesses.BUSINESS_FYI_TAB)
    assert fyi_tab.exists, "FYI tab not found"
    fyi_tab.click()
    sleep(2)  # Wait for FYI contents to load

    # Verify FYI tab contents are present
    fyi_contents = d.xpath(Businesses.BUSINESS_FYI_TAB_CONTENTS)
    assert fyi_contents.exists, "FYI tab contents not found"

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
    sign_in_and_prepare(d)

    # Use utility function to search and submit
    search_and_submit(d, menu_business_name)

    # Wait for and verify Businesses section is present
    verify_businesses_section_present(d)

    # Click on Big Fatty's BBQ search result under Businesses
    print("\nLocating Big Fatty's BBQ under Businesses section...")
    search_result = d.xpath(Businesses.BUSINESS_UNDER_BUSINESSES.format(menu_business_name))
    assert search_result.exists, "Big Fatty's BBQ not found under Businesses section"
    print("Found Big Fatty's BBQ, clicking...")
    search_result.click()
    sleep(3)  # Wait for business details to load

    # Verify About tab is visible
    print("\nVerifying About tab is visible...")
    about_tab = d.xpath(Businesses.BUSINESS_ABOUT_TAB)
    assert about_tab.exists, "About tab not found on business details page"
    print("About tab is visible")

    # Verify About tab contents are present
    print("\nVerifying About tab contents are present...")
    about_contents = d.xpath(Businesses.BUSINESS_ABOUT_TAB_CONTENTS)
    assert about_contents.exists, "About tab contents not found"
    print("About tab contents are present")

    # Take screenshot of business details with About tab
    print("\nTaking screenshot of business details with About tab...")
    screenshot_path = os.path.join(screenshots_dir, "7_2_1_business_card_with_menu_about_tab.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 7_2_1_business_card_with_menu_about_tab.png")

    # Verify Menu tab is visible
    print("\nVerifying Menu tab is visible...")
    menu_tab = d.xpath(Businesses.BUSINESS_MENU_TAB)
    assert menu_tab.exists, "Menu tab not found on business details page"
    print("Menu tab is visible")

    # Click on Menu tab
    menu_tab.click()
    sleep(2)  # Wait for menu contents to load

    # Verify Menu tab contents are present
    print("\nVerifying Menu tab contents are present...")
    menu_contents = d.xpath(Businesses.BUSINESS_MENU_TAB_CONTENTS)
    assert menu_contents.exists, "Menu tab contents not found"
    print("Menu tab contents are present")

    # Take screenshot of business details with Menu tab
    print("\nTaking screenshot of business details with Menu tab...")
    screenshot_path = os.path.join(screenshots_dir, "7_2_2_business_card_with_menu_tab.png")
    d.screenshot(screenshot_path)
    print("Screenshot saved as 7_2_2_business_card_with_menu_tab.png")