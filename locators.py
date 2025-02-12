"""
Locators for the EatVermont app UI elements using XPath selectors
"""


class LoginPage:
    """Locators for login flow"""
    # Buttons
    GET_STARTED = '//android.widget.TextView[@text="Get Started"]'
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
    EVENTS_SEE_ALL = '//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[3]'
    VIDEOS_SEE_ALL = ('//android.widget.ScrollView/android.view.ViewGroup[1]/'
                      'android.view.ViewGroup[6]/android.widget.TextView[1]')
    VIDEOS_TEXT_HOME_SCREEN = '//android.widget.TextView[@text="Videos" and ./parent::android.view.ViewGroup]'
    DAY_TRIPS_SEE_ALL = (
        '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]'
        '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
        '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
        '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
        '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
        '/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
        '/android.view.ViewGroup[1]/android.widget.ScrollView[1]/android.view.ViewGroup[1]'
        '/android.view.ViewGroup[2]/android.view.ViewGroup[1]')
    EVENTS_WITHIN_30_SEE_ALL = ('//*[contains(@text, "{}")]/following-sibling::'
                                '*//android.widget.TextView[@text="See All"]')
    EVENTS_FURTHER_THAN_30_SEE_ALL = ('//*[contains(@text, "Events Further Than ~30min")]'
                                      '/following-sibling::*//android.widget.TextView[@text="See All"]')
    EVENTS_WITHIN_30_TILE = ('//*[contains(@content-desc, "{}")]/android.view.ViewGroup[4]'
                             '/android.widget.TextView[1]')
    EVENTS_MORE_THAN_30_MIN = ('//*[contains(@content-desc, "{}")]/android.view.ViewGroup[4]'
                               '/android.widget.TextView[1]')
    VIEW_MAP = '//android.widget.TextView[@text="View Map"]'
    ADD_INFO_BUTTON = '//android.widget.TextView[@text="Add Info"]'
    SETTINGS_BUTTON = '//android.widget.TextView[@text="D" and @package="com.eatvermont"]'
    TRAILS_BUTTON = '//android.view.ViewGroup[@content-desc="Trail"]'


#    LOCATION_PICKER_HOME_SCREEN = *need button id because other locators don't work*'


class HomeScreenTiles:
    """Locators for Home Screen Tiles"""
    EVENTS_TILE = '//android.view.ViewGroup[contains(@content-desc, "{}")]'
    VIDEOS_TILE = ('//android.widget.HorizontalScrollView/android.view.ViewGroup[1]'
                   '/android.view.ViewGroup[1]/android.view.ViewGroup[1]')
    VIDEOS_TILE_TITLE = '//android.widget.ScrollView//android.view.ViewGroup[contains(@content-desc, "Rocket")]'
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
    FAVORITES = '//*[@content-desc="Favorites"]/com.horcrux.svg.SvgView[1]'
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
    EVENTS_FILTER = '//android.widget.TextView[@text="Events"]'
    FOOD_AND_DRINKS_FILTER = '//android.widget.TextView[@text="Food & Drinks"]'
    FARMS_FILTER = '//android.widget.TextView[@text="Farms"]'
    FOOD_PANTRIES_FILTER = '//android.widget.TextView[@text="Food Pantries"]'
    FILTERS_HEADER = ('//android.view.ViewGroup[.//android.widget.TextView[@text="Events" or '
                      '@text="Food & Drinks" or @text="Farms" or @text="Food Pantries"]]')


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
    BUSINESS_ABOUT_TAB = '//*[@content-desc="About"]/android.widget.TextView[1]'
    BUSINESS_ABOUT_TAB_CONTENTS = ('//android.widget.TextView[ancestor::android.view.ViewGroup'
                                   '[descendant::android.view.ViewGroup[contains(@content-desc,'
                                   ' "About")]]]')
    BUSINESS_MENU_TAB = '//android.view.ViewGroup[contains(@content-desc, "Menu")]'
    BUSINESS_MENU_TAB_CONTENTS = ('//android.widget.TextView[ancestor::android.view.ViewGroup'
                                  '[descendant::android.view.ViewGroup[contains(@content-desc,'
                                  ' "Menu")]]]')
    BUSINESS_FYI_TAB = '//*[@text="FYI 🎉"]'
    BUSINESS_FYI_TAB_CONTENTS = ('//android.widget.TextView[ancestor::android.view.ViewGroup'
                                 '[descendant::android.view.ViewGroup[@text="FYI 🎉"]]]')
    BUSINESS_NAME_EVENT_CARD = ('//android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/'
                                'android.widget.ScrollView/android.view.ViewGroup'
                                '/android.view.ViewGroup[5]')


class DayTrips:
    """Locators for Day Trips"""
    READ_MORE_HOME_SCREEN = ('//android.widget.TextView[@text="Read More"]'
                             '[ancestor::android.view.ViewGroup[.//android.widget.TextView[contains'
                             '(@text, "Day Trip")]]]'
                             '[1]')


class Trails:
    """Locators for Trails"""
    READ_MORE_TRAILS = ('//android.widget.TextView[@text="Read More"]'
                        '[ancestor::android.view.ViewGroup[.//android.widget.TextView[contains(@text, "Trail")]]]'
                        '[1]')
    TRAIL_NAME = '//android.widget.TextView[@text="{}"]'
    TRAILS_SEARCH = '//android.widget.EditText[@text="Search"]'
    TRAILS_STATUS = '//android.widget.TextView[@text="Not Started" or @text="In Progress" or @text="Complete"]'
    PERCENTAGE_PROGRESS = '//android.widget.TextView[contains(@text, "%")]'
    VISITS_COMPLETED_TEXT = ('//android.widget.TextView[contains(translate(@text, "ABCDEFGHIJKLMNOPQRSTUVWXYZ",'
                             ' "abcdefghijklmnopqrstuvwxyz"), "visits completed")]')
    VISITS_COMPLETED_NUMBER = '//android.widget.TextView[contains(@text, "/") and string-length(@text) <= 5]'
    TRAILS_SECTION = '//android.view.ViewGroup[.//android.widget.TextView[@package="com.eatvermont"]]'
    TRAILS_SECTION_TEXT = '//android.widget.TextView[@text="{}"]'


class Videos:
    """Locators for Videos screen UI Elements"""
    VIDEO_TILE = ('//android.widget.ScrollView//android.view.ViewGroup[.//android.widget.ImageView and'
                  ' .//android.widget.TextView]')
    VIDEO_PLAYER = '//android.widget.FrameLayout[./android.widget.FrameLayout and ./android.view.ViewGroup]'


class MyFavorites:
    """Locators for My Favorites"""
    FAVORITE_EVENTS_ADD_REMOVE = ('//*[@resource-id="android:id/content"]'
                                  '/android.widget.FrameLayout[1]/android.view.ViewGroup[1]'
                                  '/android.view.ViewGroup[2]/android.view.ViewGroup[2]'
                                  '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                  '/android.view.ViewGroup[1]/android.widget.ScrollView[1]'
                                  '/android.view.ViewGroup[1]/android.view.ViewGroup[2]'
                                  '/com.horcrux.svg.SvgView[1]')
    FAVORITE_BUSINESS_ADD_REMOVE = ('//*[@resource-id="android:id/content"]'
                                    '/android.widget.FrameLayout[1]/android.view.ViewGroup[1]'
                                    '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                    '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                    '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                    '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                    '/android.view.ViewGroup[1]/android.view.ViewGroup[3]'
                                    '/com.horcrux.svg.SvgView[1]')
    FAVORITE_VIDEOS_ADD_REMOVE = ('//android.widget.HorizontalScrollView'
                                  '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                  '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                  '/android.view.ViewGroup[3]/com.horcrux.svg.SvgView[1]')
    FAVORITE_TRAILS_ADD_REMOVE = ('//*[contains(@content-desc, "Trail") and contains(@content-desc, "Read More")]'
                                  '/android.view.ViewGroup[2]/com.horcrux.svg.SvgView[1]'
                                  '/com.horcrux.svg.GroupView[1]')
    ADDED_FAVORITE_EVENT = ('//*[contains(@content-desc, ", ") and ('
                            'contains(@content-desc, "Monday") or '
                            'contains(@content-desc, "Tuesday") or '
                            'contains(@content-desc, "Wednesday") or '
                            'contains(@content-desc, "Thursday") or '
                            'contains(@content-desc, "Friday") or '
                            'contains(@content-desc, "Saturday") or '
                            'contains(@content-desc, "Sunday"))]'
                            '/android.view.ViewGroup[2]/com.horcrux.svg.SvgView[1]')
    ADDED_FAVORITE_BUSINESS = ('//*[contains(@content-desc, ", ") and ('
                               'contains(@content-desc, "Open Now") or '
                               'contains(@content-desc, "Closed") or '
                               'contains(@content-desc, "Opening") or '
                               'contains(@content-desc, "Closing"))]'
                               '/android.view.ViewGroup[2]/com.horcrux.svg.SvgView[1]')
    ADDED_FAVORITE_TRAIL = ('//*[contains(translate(@content-desc, "TRAIL", "trail"), "trail")]'
                            '/android.view.ViewGroup[2]')
    ADDED_FAVORITE_VIDEO = ('//*[@content-desc]'
                            '/android.view.ViewGroup[3]/com.horcrux.svg.SvgView[1]')


class VisitHistory:
    """Locators for Visit History"""
    VISIT_HISTORY_TAB = '//android.widget.TextView[@text="Visit History"]'


class GuestMode:
    """Locators for Guest Mode module"""
    CONTINUE_AS_GUEST_BUTTON = '//android.widget.TextView[@text="Continue as a guest."]'
    #    GUEST_MODE_SIGN_IN_BUTTON = *need button id because other locators don't work*'
    EVENTS_LIMITED_RESULTS = '//android.widget.TextView[@text="Limited Results"]'
    GUEST_MODE_HOME_SCREEN_PROMPT = '//android.widget.TextView[@text="Limited Results"]'
    GUEST_MODE_HOME_SCREEN_LOCKED_VIDEOS = ('//android.widget.HorizontalScrollView'
                                            '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                            '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                            '/android.view.ViewGroup[3]/android.view.ViewGroup[1]'
                                            '/com.horcrux.svg.SvgView[1]/com.horcrux.svg.GroupView[1]')
    GUEST_MODE_ADD_INFO = '//android.widget.TextView[@text="Add Info"]'
    GUEST_MODE_VIDEOS_SEE_ALL = '//android.view.ViewGroup[@content-desc="See All"]'


class PlansPopup:
    """Locators for Plans Popup"""
    PLANS_POPUP_CONTINUE_BUTTON = ('//android.widget.TextView[@text="Continue as a guest."]'
                                   ' | //android.view.ViewGroup[@content-desc="Continue as a guest."]')
