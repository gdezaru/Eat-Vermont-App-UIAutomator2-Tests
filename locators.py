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
    EVENTS_TEXT = '//android.widget.TextView[contains(@text, "Events Near You")]'
    EVENTS_SEE_ALL = '//android.widget.TextView[@text="See All"]'
    VIDEOS_SEE_ALL = ('//android.widget.TextView[@text="Videos"]/following-sibling::*'
                      '//android.widget.TextView[@text="See All"]')
    VIDEOS_TEXT_HOME_SCREEN = '//android.widget.TextView[@text="Videos" and ./parent::android.view.ViewGroup]'
    DAY_TRIPS_SEE_ALL = ('//android.widget.TextView[@text="Day Trips"]/following-sibling::*'
                         '//android.widget.TextView[@text="See All"]')
    TRAILS_SEE_ALL = ('//android.widget.TextView[@text="Start a Trail!"]/following-sibling::*'
                      '//android.widget.TextView[@text="See All"]')
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
    CUSTOM_DAY_TRIP_BUTTON = '//android.widget.TextView[@text="Create a Custom trip"]'


class HomeScreenTiles:
    """Locators for Home Screen Tiles"""
    EVENTS_TILE = '//android.view.ViewGroup[contains(@content-desc, "{}")]'
    VIDEOS_TILE = ('//android.widget.HorizontalScrollView/android.view.ViewGroup[1]'
                   '/android.view.ViewGroup[1]/android.view.ViewGroup[1]')
    VIDEOS_TILE_TITLE = '//android.widget.ScrollView//android.view.ViewGroup[contains(@content-desc, "Rocket")]'
    DAY_TRIPS_TILE = ('//android.view.ViewGroup[contains(@content-desc, "{}")]//android.widget.TextView'
                      '[@text="Read More"]')
    EVENTS_WITHIN_30_TILE = '//android.widget.TextView[contains(@text, "{}, ")]'
    EVENTS_MORE_THAN_30_TILE = '//android.widget.TextView[contains(@text, "{}, ")]'


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
    FIRST_SEARCH_RESULT = '//*[contains(@content-desc, "Burlington")]/android.view.ViewGroup[3]'

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
    ADD_UPDATE_INFO_FIELD = ('//*[@content-desc="Add Info"]/android.view.ViewGroup[1]/android.widget.ScrollView[1]'
                             '/android.view.ViewGroup[1]/android.view.ViewGroup[2]')
    SUBMIT_INFO_BUTTON = '//android.widget.TextView[@text="Submit"]'
    CHEERS_BUTTON = '//android.widget.TextView[@text="Cheers"]'


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
    EVENTS_POPUP_BASE = ('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                         '/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[2]'
                         '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]')
    EVENTS_POPUP_MAIN = EVENTS_POPUP_BASE + '/android.view.ViewGroup[1]'
    EVENTS_POPUP_CLOSE_BUTTON = ('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                                 '/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[2]'
                                 '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                 '/android.view.ViewGroup[1]/com.horcrux.svg.SvgView[1]/com.horcrux.svg.GroupView[1]')
    CAROUSEL_ITEM = '//*[@content-desc="{}"]/android.view.ViewGroup[3]/android.widget.TextView[3]'
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
                                 '[descendant::*[@text="FYI 🎉"]]]')
    BUSINESS_NAME_EVENT_CARD = ('//android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/'
                                'android.widget.ScrollView/android.view.ViewGroup'
                                '/android.view.ViewGroup[5]')
    BUSINESSES_BACK_BUTTON = ('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                              '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                              '/android.widget.ScrollView[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/'
                              'android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                              '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/com.horcrux.svg.SvgView[1]'
                              '/com.horcrux.svg.GroupView[1]')


class DayTrips:
    """Locators for Day Trips and Custom Day Trips builder"""
    DAY_TRIPS_READ_MORE_HOME_SCREEN = ('//android.widget.TextView[@text="Read More"]'
                                       '[ancestor::android.view.ViewGroup[.//android.widget.TextView[contains'
                                       '(@text, "Day Trips")]]]'
                                       '[1]')
    MY_TRIPS = '//android.widget.TextView[@text="My Trips"]'
    DAY_TRIPS_SEARCH = '//android.widget.EditText[@text="Search"]'
    DAY_TRIPS_SEARCH_RESULT_EVENTS = '//android.widget.TextView[contains(@text, "Events")]'
    DAY_TRIPS_MY_TRIPS_CARD = '//android.widget.TextView[contains(@text, "day trip") and contains(@text, "Burlington")]'
    DAY_TRIPS_SEARCH_RESULT_FOOD_DRINKS = '//android.widget.TextView[contains(@text, "Fooddrinks")]'
    DAY_TRIPS_SEARCH_RESULT_OUTDOORS = '//android.widget.TextView[contains(@text, "Outdoors")]'
    DAY_TRIPS_SEARCH_RESULT_PTS_INTEREST = '//android.widget.TextView[contains(@text, "Points")]'
    DAY_TRIP_DETAILS_DATE = '//android.widget.TextView[contains(@text, "{}")]'
    DAY_TRIPS_DETAILS_PLACES = '//android.widget.TextView[contains(@text, " Places")]'
    DAY_TRIPS_THREE_DOTTED_BUTTON = (
        '//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]'
        '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.widget.ScrollView[1]/android.view.ViewGroup[1]'
        '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
        '/android.view.ViewGroup[5]/android.view.ViewGroup[1]')
    DAY_TRIPS_DELETE_BUTTON = '//android.widget.TextView[@text="Delete"]'
    # Locators for automatic custom Day Trips builder
    CUSTOM_DAY_TRIPS_BUTTON = '//android.widget.TextView[@text="Create a Custom trip"]'
    CREATE_TRIP_HEADER = '//android.widget.TextView[@text="Where do you want to go?"]'
    ADD_A_LOCATION = '//android.widget.TextView[@text="Add A Location"]'
    CUSTOM_DAY_TRIP_SEARCH = '//android.widget.EditText[@text="Search here"]'
    QUICK_SUGGESTIONS = '//android.widget.TextView[@text="Quick Suggestions"]'
    DATE_PICKER = '//android.view.ViewGroup[@content-desc="{}"]'
    DATE_PICKER_RIGHT_ARROW = ('//*[@resource-id="undefined.header.rightArrow"]/com.horcrux.svg.SvgView[1]'
                               '/com.horcrux.svg.GroupView[1]')
    DATE_PICKER_SELECTED_DATE = '//android.widget.TextView[@text="{}"]'
    AUTO_RECOMMEND_BUTTON = '//android.widget.TextView[@text="Auto-Recommend"]'
    CUSTOM_DAY_TRIP_EVENTS = '//android.widget.TextView[@text="Events"]'
    CUSTOM_DAY_TRIP_FOOD_DRINKS = '//android.widget.TextView[@text="Food + Drinks"]'
    CUSTOM_DAY_TRIP_OUTDOORS = '//android.widget.TextView[@text="Outdoors"]'
    CUSTOM_DAY_TRIPS_POINTS_OF_INTEREST = '//android.widget.TextView[@text="Points of Interest"]'
    ADVANCED_FILTER = '//android.widget.TextView[@text=" Advanced Filter"]'
    NEXT_BUTTON = '//android.widget.TextView[@text="Next"]'
    CRAFTING_DAY_TRIP = '//android.widget.TextView[@text="Crafting Your Trip"]'
    DETAILS_SCREEN_LOCATION = '//android.widget.TextView[contains(@text, "{}")]'
    DETAILS_SCREEN_DATE = '//android.widget.TextView[@text="{}"]'
    QUICK_TIP = '//android.widget.TextView[@text="Quick Tip: Drag and drop to change order."]'
    ALSO_TIP = '//android.widget.TextView[@text="Also: Swipe side-to-side for more."]'
    CONTINUE_BUTTON = '//android.widget.TextView[@text="Continue"]'
    TRIP_NAME = '//android.widget.EditText[@text="Enter Trip name"]'
    SAVE_TRIP = '//android.widget.TextView[@text="Save"]'
    # Locators for manual Day Trips builder


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
    FAVORITE_BUSINESS_ADD_REMOVE = ('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                                    '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                    '/android.widget.ScrollView[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                    '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                    '/android.view.ViewGroup[1]/android.view.ViewGroup[3]/com.horcrux.svg.SvgView[1]'
                                    '/com.horcrux.svg.GroupView[1]')
    FAVORITE_BUSINESS_DETAILS_REMOVE = ('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                                        '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                        '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                        '/android.view.ViewGroup[2]/com.horcrux.svg.SvgView[1]')
    FAVORITE_VIDEOS_ADD_REMOVE = ('//android.widget.HorizontalScrollView'
                                  '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                  '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                  '/android.view.ViewGroup[3]/com.horcrux.svg.SvgView[1]')
    FAVORITE_TRAILS_ADD_REMOVE = ('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]'
                                  '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                  '/android.widget.ScrollView[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                  '/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                  '/android.view.ViewGroup[1]/android.view.ViewGroup[2]/com.horcrux.svg.SvgView[1]'
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
    ADDED_FAVORITE_BUSINESS = f'//*[contains(@content-desc, "Big Fatty\'s BBQ")]'
    ADDED_FAVORITE_TRAIL = ('//*[contains(translate(@content-desc, "TRAIL", "trail"), "trail")]'
                            '/android.view.ViewGroup[2]')
    ADDED_FAVORITE_VIDEO = ('//*[@content-desc]'
                            '/android.view.ViewGroup[3]/com.horcrux.svg.SvgView[1]')


class VisitHistory:
    """Locators for Visit History"""
    VISIT_HISTORY_TAB = '//android.widget.TextView[@text="Visit History"]'


class GuestMode:
    """Locators for Guest Mode module"""
    CONTINUE_AS_GUEST_BUTTON = '//android.widget.TextView[@text="Try for Free – Guest Access"]'
    #    GUEST_MODE_SIGN_IN_BUTTON = *need button id because other locators don't work*'
    EVENTS_LIMITED_RESULTS = '//android.widget.TextView[@text="Limited Results"]'
    GUEST_MODE_HOME_SCREEN_PROMPT = '//android.widget.TextView[@text="Limited Results"]'
    GUEST_MODE_ADD_INFO = '//android.widget.TextView[@text="Add Info"]'
    GUEST_MODE_VIDEOS_SEE_ALL = '//android.view.ViewGroup[@content-desc="See All"]'
    GUEST_MODE_HOME_SCREEN_LOCKED_VIDEOS = ('//android.widget.HorizontalScrollView'
                                            '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                            '/android.view.ViewGroup[1]/android.view.ViewGroup[1]'
                                            '/android.view.ViewGroup[3]/android.view.ViewGroup[1]')


class PlansPopup:
    """Locators for Plans Popup"""
    PLANS_POPUP_CLOSE_BUTTON = ('//*[@resource-id="android:id/content"]'
                                '/android.widget.FrameLayout[1]'
                                '/android.view.ViewGroup[1]'
                                '/android.view.ViewGroup[2]'
                                '/android.view.ViewGroup[2]'
                                '/android.view.ViewGroup[1]'
                                '/android.view.ViewGroup[1]'
                                '/android.view.ViewGroup[1]'
                                '/android.view.ViewGroup[2]'
                                '/com.horcrux.svg.SvgView[1]')
