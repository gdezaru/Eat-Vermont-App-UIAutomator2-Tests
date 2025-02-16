"""
Utility functions for Settings.
"""
from time import sleep
import random
import string

from locators import HomeScreen, SettingsScreen


# UI interaction with Edit Profile screen


def click_settings_save_button(d):
    """
    Clicks the save button in the Edit Profile screen.
    """
    save_button = d.xpath(SettingsScreen.EDIT_PROFILE_SAVE_BUTTON)
    save_button.click()
    sleep(4)


def generate_random_name():
    """
    Generate a random name starting with 'D'.
    """
    name_length = random.randint(5, 10)  # Random length between 5 and 10
    random_chars = ''.join(random.choices(string.ascii_lowercase, k=name_length - 1))
    return 'D' + random_chars


def generate_random_username():
    """
    Generate a random username.
    """
    username_length = random.randint(8, 15)  # Random length between 8 and 15
    random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
    return random_chars


# UI interaction with settings screen
def click_settings_back_button(d):
    """
    Clicks the Settings back button.
    """
    back_button = d.xpath(SettingsScreen.BACK_BUTTON_SETTINGS)
    assert back_button.exists, "Could not find Back button"
    back_button.click()
    sleep(2)


def click_settings_button(d):
    """
    Clicks the Settings button.
    """
    settings_button = d.xpath(HomeScreen.SETTINGS_BUTTON)
    assert settings_button.exists, "Could not find Settings button"
    settings_button.click()
    sleep(2)


def click_edit_profile(d):
    """
    Clicks the Edit Profile button.
    """
    edit_profile = d.xpath(SettingsScreen.EDIT_PROFILE)
    assert edit_profile.exists, "Could not find Edit Profile option"
    edit_profile.click()
    sleep(2)


def click_location_toggle(d):
    """
    Click the Settings location toggle.
    """
    location_toggle = d.xpath(SettingsScreen.LOCATION_TOGGLE)
    assert location_toggle.exists, "Could not find Location Toggle"
    location_toggle.click()
    sleep(1)


def click_log_out(d):
    """
    Click the Logout button.
    """
    log_out = d.xpath(SettingsScreen.LOG_OUT)
    assert log_out.exists, "Could not find Log Out button"
    log_out.click()
    sleep(2)


def handle_allow_button(d):
    """
    Handles the location permission if it appears.
    """
    location_allow = d.xpath(SettingsScreen.LOCATION_ALLOW)
    if location_allow.wait(timeout=2):
        location_allow.click()
        sleep(1)