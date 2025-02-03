"""
Locators for the EatVermont app UI elements
"""

class LoginPageLocators:
    """Locators for login flow"""
    # Buttons
    SIGN_IN_BUTTON = '//android.widget.TextView[@text="Sign In"]'
    LOG_IN_BUTTON = '//android.widget.TextView[@text="Log in"]'  # Updated to match exact text
    
    # Input fields
    EMAIL_FIELD = '//android.widget.EditText[@text="Email"]'
    PASSWORD_FIELD = '//android.widget.EditText[@text="Password" or @password="true"]'

    #Forgot Password
    FORGOT_PASSWORD = '//android.view.ViewGroup[@content-desc="Forgot Password?"]'

class PermissionDialogLocators:
    """Locators for permission dialogs"""
    ALLOW_BUTTON = '//android.widget.Button[@text="Allow"]'

class HomeScreenLocators:
    """Locators for Home Screen UI Elements"""
    EVENTS_TEXT = '//android.widget.TextView[@text="Events"]'
    EVENTS_SEE_ALL =
    VIDEOS_SEE_ALL =
    VIEW_MAP =
    DAY_TRIPS_SEE_ALL =
    EVENTS_WITHIN_30_SEE_ALL =
    EVENTS_MORE_THAN_30_SEE_ALL =
    PROFILE_PHOTO_BUTTON =
    ADD_INFO_BUTTON =
    HOME_SCREEN_LOCATION_PICKER =

class HomeScreenTiles:
    """Locators for Home Screen Tiles"""
    EVENTS_TILE =
    VIDEOS_TILE =
    DAY_TRIPS_TILE =
    EVENTS_WITHIN_30_TILE =
    EVENTS_MORE_THAN_30_TILE =

class BottomNavBarLocators:
    """Locators for Bottom Navigation Bar"""
    HOME_BOTTOM_NAV_BAR =
    SEARCH_BOTTOM_NAV_BAR =
    TRAILS_BOTTOM_NAV_BAR =
    FAVORITES_BOTTOM_NAV_BAR =
    EV_BUTTON_BOTTOM_NAV_BAR =

class SettingsLocators:
    """Locators for Settings Screen"""
    MANAGE_ACCOUNT =
    EDIT_PROFILE =
    SHARE_MY_LOCATION_TOGGLE =
    LOG_OUT =
    SETTINGS_BACK_BUTTON =

class EditProfileLocators:
    """Locators for Edit Profile Screen"""
    FIRST_LAST_NAME =
    USERNAME =
    EMAIL =
    PHONE_NUMBER =
    EDIT_PROFILE_BACK_BUTTON =
    EDIT_PROFILE_SAVE_BUTTON =