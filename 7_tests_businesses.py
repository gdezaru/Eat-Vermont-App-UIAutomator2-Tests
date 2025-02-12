from time import sleep
from locators import Businesses
from utils import handle_notification_permission, handle_events_popup, sign_in_user
import pytest
from retry_decorator import retry

# Initialize business names at module level
business_name = "Higher Ground"
menu_business_name = "Big Fatty's BBQ"


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_business_card_with_event(d):
    """Tests the contents of a business card with event."""
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
    d.send_keys(business_name)
    sleep(1)
    d.press("enter")
    sleep(10)

    # Wait for and verify Businesses section is present
    print("\nVerifying Businesses section is present...")
    businesses_section = d.xpath(Businesses.BUSINESSES_SECTION)
    assert businesses_section.exists, "Businesses section not found in search results"
    print("Found Businesses section")

    # Click on Higher Ground search result under Businesses
    print("\nLocating Higher Ground under Businesses section...")
    search_result = d.xpath(Businesses.BUSINESS_UNDER_BUSINESSES.format(business_name))
    assert search_result.exists, "Higher Ground not found under Businesses section"
    print("Found Higher Ground, clicking...")
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
    d.screenshot("7_1_1_business_card_with_event_about_tab.png")
    print("Screenshot saved as 7_1_1_business_card_with_event_about_tab.png")

    # Click on FYI tab and verify contents
    print("\nLocating and clicking FYI tab...")
    fyi_tab = d.xpath(Businesses.BUSINESS_FYI_TAB)
    assert fyi_tab.exists, "FYI tab not found"
    fyi_tab.click()
    sleep(2)  # Wait for FYI contents to load
    print("FYI tab clicked")

    # Verify FYI tab contents are present
    print("\nVerifying FYI tab contents are present...")
    fyi_contents = d.xpath(Businesses.BUSINESS_FYI_TAB_CONTENTS)
    assert fyi_contents.exists, "FYI tab contents not found"
    print("FYI tab contents are present")

    # Take screenshot of FYI tab contents
    print("\nTaking screenshot of FYI tab contents...")
    d.screenshot("7_1_2_business_card_with_event_fyi_tab.png")
    print("Screenshot saved as 7_1_2_business_card_with_event_fyi_tab.png")


@pytest.mark.smoke
@retry(retries=2, delay=1, exceptions=(AssertionError, TimeoutError))
def test_business_card_with_menu(d):
    """Tests the contents of a business card with menu."""
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
    d.send_keys(menu_business_name)
    sleep(1)
    d.press("enter")
    sleep(10)

    # Wait for and verify Businesses section is present
    print("\nVerifying Businesses section is present...")
    businesses_section = d.xpath(Businesses.BUSINESSES_SECTION)
    assert businesses_section.exists, "Businesses section not found in search results"
    print("Found Businesses section")

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
    d.screenshot("7_2_1_business_card_with_menu_about_tab.png")
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
    d.screenshot("7_2_1_business_card_with_menu_tab.png")
    print("Screenshot saved as 7_2_2_business_card_with_menu_tab.png")