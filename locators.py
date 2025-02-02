"""
Locators for the EatVermont app UI elements
"""

class LoginPageLocators:
    """Locators for login flow"""
    # Buttons
    SIGN_IN_BUTTON = '//android.widget.TextView[@text="Sign In"]'
    LOG_IN_BUTTON = '//android.widget.TextView[@text="Log in"]'
    
    # Input fields
    EMAIL_FIELD = '//android.widget.EditText[@text="Email"]'
    PASSWORD_FIELD = '//android.widget.EditText[@text="Password" or @password="true"]'
    
class HomeScreenLocators:
    """Locators for Home Screen UI Elements"""
    EVENTS_TEXT = '//android.widget.TextView[@text="Events"]'
