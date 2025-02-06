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
    VIDEOS_SEE_ALL = '//android.widget.TextView[@text="See All"]'
    VIEW_MAP = '//android.widget.TextView[@text="View Map"]'
    DAY_TRIPS_SEE_ALL = '//*[contains(@text, "{}")]/following-sibling::*//android.widget.TextView[@text="See All"]'
    EVENTS_WITHIN_30_SEE_ALL = ('//*[contains(@text, "{}")]/following-sibling::*//android.widget.TextView'
                                '[@text="See All"]')
    EVENTS_FURTHER_THAN_30_SEE_ALL = ('//*[contains(@text, "Events Further Than ~30min")]'
                                      '/following-sibling::*//android.widget.TextView[@text="See All"]')
    ADD_INFO_BUTTON = '//android.widget.TextView[@text="Add Info"]'
    LOCATION_PICKER_HOME_SCREEN = '//android.widget.TextView[@text="Pick Your Location"]'


class HomeScreenTiles:
    """Locators for Home Screen Tiles"""
    EVENTS_TILE = '//android.view.ViewGroup[contains(@content-desc, "{}")]'
    VIDEOS_TILE = ('//android.widget.HorizontalScrollView/android.view.ViewGroup[1]'
                   '/android.view.ViewGroup[1]/android.view.ViewGroup[1]')
    DAY_TRIPS_TILE = ('//android.view.ViewGroup[contains(@content-desc, "{}")]//android.widget.TextView'
                      '[@text="Read More"]')
    EVENTS_WITHIN_30_TILE = '//android.widget.TextView[contains(@text, "{}, ")]'
    EVENTS_MORE_THAN_30_TILE = ('//android.widget.ScrollView[1]/android.view.ViewGroup[1]'
                                '/android.view.ViewGroup[5]/android.view.ViewGroup[contains(@content-desc, "{}")]')


class BottomNavBar:
    """Locators for Bottom Navigation Bar"""
    NAV_HOME_BUTTON = '//android.widget.TextView[@text="Home"]'
    SEARCH = '//android.widget.TextView[@text="Search"]'
    EVENTS = '//android.widget.TextView[@text="Events"]'
    FAVORITES = '//android.widget.TextView[@text="Favorites"]'
    EAT_VERMONT_BUTTON = ('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/'
                          'android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                          '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                          '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                          '/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.View[1]'
                          '/android.view.ViewGroup[1]/android.view.View[1]')
    DAY_TRIPS_BUTTON = '//android.widget.TextView[@text="Day Trips"]'
    CHECK_IN_BUTTON = '//android.widget.TextView[@text="Check In"]'
    TRAILS_BUTTON = '//android.widget.TextView[@text="Trails"]'


class SearchModule:
    """Locators for Search Module"""
    SEARCH_ICON = '//*[@content-desc="Search"]'
    SEARCH_INPUT = '//android.widget.EditText'

    @staticmethod
    def search_result(text):
        """Get XPath for a search result containing specific text"""
        return f'//android.view.ViewGroup[contains(@content-desc, "{text}")]'


class EventsScreen:
    """Locators for Events Screen UI Elements"""
    DAY_OF_WEEK = ('//android.view.ViewGroup[@clickable="true" and .//android.widget.TextView[@text="{}"]]'  # The clickable container
                   '//android.widget.TextView[@text="{}"]')  # The day text itself
    EVENTS_SCREEN_TILE_1 = '//android.widget.TextView[@text and @index="2"]'  # First event title text (index 2 from screenshot)
    EVENTS_SCREEN_NO_EVENTS = '//android.widget.TextView[@text="No Events"]'  # Text shown when no events are available
    EVENT_TITLE = '//android.widget.TextView[contains(@text, "{}")]'  # Event title in the details view


class ViewMap:
    EVENTS_FILTER = '//android.widget.TextView[@text="Events" and @index="1"]'
    FOOD_AND_DRINKS_FILTER = '//android.widget.TextView[@text="Food & Drinks" and @index="2"]'
    FARMS_FILTER = '//android.widget.TextView[@text="Farms" and @index="3"]'
    FOOD_PANTRIES_FILTER = '//android.widget.TextView[@text="Food Pantries" and @index="4"]'


class AddInfo:
    """Locators for Add Info Screen"""
    BUSINESS_NAME = '//android.widget.EditText[@text="Type here."]'
    ADD_UPDATE_INFO_FIELD = ('//android.widget.EditText[@text="e.g. '
                             '\"New hours: 9am-6pm daily.\" or \"New menu!\" (then attach an image)"]')
    SUBMIT_INFO_BUTTON = '//android.widget.TextView[@text="Submit"]'

#class DayTripsScreen: