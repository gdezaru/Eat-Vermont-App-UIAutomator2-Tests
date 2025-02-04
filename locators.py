"""
Locators for the EatVermont app UI elements using XPath selectors
"""


class LoginPage:
    """Locators for login flow"""
    # Buttons
    SIGN_IN_BUTTON = '//android.widget.TextView[@text="Sign In"]'
    LOG_IN_BUTTON = '//android.widget.TextView[@text="Log in"]'

    # Input fields
    EMAIL_FIELD = '//android.widget.EditText[@text="Email"]'
    PASSWORD_FIELD = '//android.widget.EditText[@text="Password" or @password="true"]'

    # Forgot Password
    FORGOT_PASSWORD = '//android.view.ViewGroup[@content-desc="Forgot Password?"]'


class Permissions:
    """Locators for permission dialogs"""
    ALLOW_BUTTON = '//android.widget.Button[@text="Allow"]'


class HomeScreen:
    """Locators for Home Screen UI Elements"""
    EVENTS_TEXT = '//android.widget.TextView[contains(@text, "Events")]'
    EVENTS_SEE_ALL = '//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[2]'
    VIDEOS_SEE_ALL = ('//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[5]'
                      '/android.widget.TextView[1]')
    VIEW_MAP = '//android.widget.TextView[@text="View Map"]'
    DAY_TRIPS_SEE_ALL = '//*[contains(@text, "{}")]/following-sibling::*//android.widget.TextView[@text="See All"]'
    EVENTS_WITHIN_30_SEE_ALL = ('//*[contains(@text, "{}")]/following-sibling::*//android.widget.TextView'
                                '[@text="See All"]')
    ADD_INFO_BUTTON = '//android.widget.TextView[@text="Add Info"]'


class HomeScreenTiles:
    """Locators for Home Screen Tiles"""
    EVENTS_TILE = '//android.view.ViewGroup[contains(@content-desc, "{}")]'
    VIDEOS_TILE = ('//android.widget.HorizontalScrollView/android.view.ViewGroup[1]'
                   '/android.view.ViewGroup[1]/android.view.ViewGroup[1]')
    DAY_TRIPS_TILE = ('//android.view.ViewGroup[contains(@content-desc, "{}")]//android.widget.TextView'
                      '[@text="Read More"]')
    EVENTS_WITHIN_30_TILE = ('//android.widget.ScrollView[1]/android.view.ViewGroup[1]'
                             '/android.view.ViewGroup[4]/android.view.ViewGroup[contains(@content-desc, "{}")]')
    EVENTS_MORE_THAN_30_TILE = ('//android.widget.ScrollView[1]/android.view.ViewGroup[1]'
                                '/android.view.ViewGroup[5]/android.view.ViewGroup[contains(@content-desc, "{}")]')


class BottomNavBar:
    """Locators for Bottom Navigation Bar"""
    SEARCH = '//android.widget.TextView[@text="Search"]'
    EVENTS = '//android.widget.TextView[@content-desc="Events"]/android.widget.TextView[1]'
    FAVORITES = '//android.widget.TextView[@text="Favorites"]'


class SearchModule:
    """Locators for Search Module"""
    SEARCH_ICON = '//*[@content-desc="Search"]'
    SEARCH_INPUT = '//android.widget.EditText'

    @staticmethod
    def search_result(text):
        """Get XPath for a search result containing specific text"""
        return f'//android.view.ViewGroup[contains(@content-desc, "{text}")]'