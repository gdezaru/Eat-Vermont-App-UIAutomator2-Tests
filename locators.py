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
    RESET_PASSWORD_EMAIL_FIELD = '//android.widget.EditText[@text="Email"]'
    RESET_PASSWORD_BUTTON = '//android.widget.TextView[@text="Reset Password"]'
    VERIFY_EMAIL_MESSAGE = '//android.widget.TextView[@text="Check Email"]'


class Permissions:
    """Locators for permission dialogs"""
    ALLOW_BUTTON = '//android.widget.Button[@text="Allow"]'


class HomeScreen:
    """Locators for Home Screen UI Elements"""
    EVENTS_TEXT = '//android.widget.TextView[contains(@text, "Events")]'
    EVENTS_SEE_ALL = ('//android.view.ViewGroup[.//android.widget.TextView[contains(@text, "Events")]]'
                      '//android.widget.TextView[@text="See All"]')
    VIDEOS_SEE_ALL = '//android.widget.TextView[@text="See All"]'
    VIEW_MAP = '//android.widget.TextView[@text="View Map"]'
    DAY_TRIPS_SEE_ALL = '//*[contains(@text, "{}")]/following-sibling::*//android.widget.TextView[@text="See All"]'
    EVENTS_WITHIN_30_SEE_ALL = ('//*[contains(@text, "{}")]/following-sibling::*//android.widget.TextView'
                                '[@text="See All"]')
    EVENTS_FURTHER_THAN_30_SEE_ALL = ('//*[contains(@text, "Events Further Than ~30min")]'
                                      '/following-sibling::*//android.widget.TextView[@text="See All"]')
    ADD_INFO_BUTTON = '//android.widget.TextView[@text="Add Info"]'
    SETTINGS_BUTTON = '//android.widget.TextView[@text="D" and @package="com.eatvermont"]'


#    LOCATION_PICKER_HOME_SCREEN = *need button id because other locators don't work*'


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
    SEARCH = '//android.view.ViewGroup[@content-desc="Search"]'
    EVENTS = '//android.widget.TextView[@text="Events"]'
    FAVORITES = '//android.widget.TextView[@text="Favorites"]'
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
    DAY_OF_WEEK = (
        '//android.view.ViewGroup[@clickable="true" and .//android.widget.TextView[@text="{}"]]'
        '//android.widget.TextView[@text="{}"]')  # The day text itself
    EVENTS_SCREEN_TILE_1 = '//android.widget.TextView[@text and @index="2"]'
    EVENTS_SCREEN_NO_EVENTS = '//android.widget.TextView[@text="No Events"]'
    EVENT_TITLE = '//android.widget.TextView[contains(@text, "{}")]'


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


class LocationManagement:
    """Locators for Location Management"""
    LOCATION_SEARCH_INPUT = '//android.widget.EditText[@package="com.eatvermont"]'
    USE_MY_CURRENT_LOCATION = '//android.widget.TextView[@text="Use My Current Location" and @package="com.eatvermont"]'
    LOCATION_SEARCH_RESULT = '//android.widget.TextView[@text="{}" and @package="com.eatvermont"]'


class SettingsScreen:
    BACK_BUTTON_SETTINGS = '//android.view.ViewGroup[@content-desc="My Profile" and @package="com.eatvermont"]'
    MANAGE_ACCOUNT = '//android.view.ViewGroup[@content-desc="Manage Account" and @package="com.eatvermont"]'
    EDIT_PROFILE = '//android.view.ViewGroup[@content-desc="Edit Profile" and @package="com.eatvermont"]'
    EDIT_NAME = '//android.widget.EditText[@package="com.eatvermont" and @index="1"]'
    EDIT_USERNAME = '//android.view.ViewGroup[@index="5" and @package="com.eatvermont"]//android.widget.EditText'
    BIRTH_DATE = '//android.view.ViewGroup[@resource-id="edit-profile-birth-date" and @package="com.eatvermont"]'
    EDIT_PROFILE_SAVE_BUTTON = '//android.view.ViewGroup[@content-desc="Save" and @package="com.eatvermont"]'
    SHARE_MY_LOCATION = '//android.widget.TextView[@text="Share My Location" and @package="com.eatvermont"]'
    LOCATION_TOGGLE = '//com.horcrux.svg.CircleView[@package="com.eatvermont" and @index="1"]'
    LOCATION_ALLOW = '//android.widget.TextView[@text="Allow" and @package="com.eatvermont"]'
    LOG_OUT = '//android.view.ViewGroup[@content-desc="Log out" and @package="com.eatvermont"]'


class Events:
    """Locators for Events and Events Popup"""
    EVENT_CARD_DETAILS_TAB = '//android.view.ViewGroup[@content-desc="Details" and @package="com.eatvermont"]'
    EVENT_CARD_MORE_INFO_TAB = '//android.view.ViewGroup[@content-desc="More Info" and @package="com.eatvermont"]'
    EVENTS_POPUP_MAIN = '//android.view.ViewGroup[./*[@text="Events For You"]]'
    EVENTS_POPUP_CLOSE_BUTTON = ('//android.view.ViewGroup[./*[@text="Events For You"]]'
                                 '/android.view.ViewGroup/com.horcrux.svg.SvgView')
    CAROUSEL_ITEM = '//android.view.ViewGroup[.//android.widget.ImageView and .//android.widget.TextView]'
    EVENT_DETAILS_TEXT = ('//android.widget.TextView[contains(@text, "Date") or contains(@text, "Time") '
                          'or contains(@text, "Where")]')
    ADD_TO_CALENDAR = '//android.widget.TextView[@text="Add to Calendar"]'


class Businesses:
    """Locators for Businesses"""
    BUSINESSES_SECTION = '//android.widget.TextView[@text="Businesses"]'
    BUSINESS_UNDER_BUSINESSES = ('//android.widget.TextView[@text="Businesses"]/'
                                 'following::android.widget.TextView[@text="{}"]')
    BUSINESS_ABOUT_TAB = '//android.view.ViewGroup[contains(@content-desc, "About")]'
    BUSINESS_ABOUT_TAB_CONTENTS = ('//android.widget.TextView[ancestor::android.view.ViewGroup'
                                   '[descendant::android.view.ViewGroup[contains(@content-desc,'
                                   ' "About")]]]')
    BUSINESS_MENU_TAB = '//android.view.ViewGroup[contains(@content-desc, "Menu")]'
    BUSINESS_MENU_TAB_CONTENTS = ('//android.widget.TextView[ancestor::android.view.ViewGroup'
                                  '[descendant::android.view.ViewGroup[contains(@content-desc,'
                                  ' "Menu")]]]')
    BUSINESS_FYI_TAB = '//android.view.ViewGroup[contains(@content-desc, "FYI")]'
    BUSINESS_FYI_TAB_CONTENTS = ('//android.widget.TextView[ancestor::android.view.ViewGroup'
                                 '[descendant::android.view.ViewGroup[contains(@content-desc,'
                                 ' "FYI")]]]')
    BUSINESS_NAME_EVENT_CARD = ('//android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/'
                                'android.widget.ScrollView/android.view.ViewGroup'
                                '/android.view.ViewGroup[5]')


class DayTrips:
    """Locators for Day Trips"""
    READ_MORE_HOME_SCREEN = ('//android.widget.TextView[@text="Read More"]'
                             '[ancestor::android.view.ViewGroup[.//android.widget.TextView[contains(@text, "Day Trip")]]]'
                             '[1]')


class Trails:
    """Locators for Trails"""
    TRAILS_BUTTON = '//android.widget.TextView[@text="Trails"]'
