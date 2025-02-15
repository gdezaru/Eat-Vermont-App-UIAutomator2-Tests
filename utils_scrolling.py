"""
Utility functions for scrolling.
"""
from time import sleep


def get_screen_dimensions(d):
    """
    Returns the screen width and height.

    :param d: The device instance.
    :return: A tuple containing (width, height)
    """
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']
    return width, height


def get_target_position_in_first_quarter(d):
    """
    Calculate the target position in the first quarter of the screen.

    :param d: The device instance.
    :return: The y-coordinate target position
    """
    width, height = get_screen_dimensions(d)
    return height // 4


def click_and_verify_element(d, element_locator, description):
    """
    Clicks an element and verifies its presence.

    :param d: The device instance.
    :param element_locator: The XPath locator for the element.
    :param description: A description of the element for logging.
    """
    print(f"\nClicking and verifying {description}...")
    element = d.xpath(element_locator)
    assert element.exists, f"{description} not found"
    element.click()
    print(f"{description} clicked and verified.")


def scroll_to_find_text(d, text, max_attempts=5):
    """
    Scroll the screen until text is found

    Args:
        d: UIAutomator2 device instance
        text: Text to find
        max_attempts: Maximum number of scroll attempts

    Returns:
        bool: True if text was found, False otherwise
    """
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']

    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)

    for _ in range(max_attempts):
        if d(text=text).exists:
            return True
        d.swipe(start_x, start_y, start_x, end_y, duration=0.8)
        sleep(1.5)

    return d(text=text).exists


def scroll_until_element_is_visible(d, locator, max_attempts=5):
    """
    Scroll the screen until the element with the given locator is visible

    Args:
        d: UIAutomator2 device instance
        locator: XPath locator string
        max_attempts: Maximum number of scroll attempts

    Returns:
        bool: True if element was found, False otherwise
    """
    screen_info = d.info
    width = screen_info['displayWidth']
    height = screen_info['displayHeight']

    start_x, start_y, end_y = calculate_swipe_coordinates(width, height)

    for _ in range(max_attempts):
        element = d.xpath(locator)
        if element.exists:
            return True
        d.swipe(start_x, start_y, start_x, end_y, duration=0.8)
        sleep(1.5)

    return d.xpath(locator).exists


def calculate_swipe_coordinates(width, height):
    """
    Calculates swipe coordinates for scrolling.

    :param width: Screen width.
    :param height: Screen height.
    :return: A tuple containing (start_x, start_y, end_y)
    """
    start_x = width // 2
    start_y = (height * 3) // 4
    end_y = height // 4
    return start_x, start_y, end_y


def scroll_to_bottom(d, scroll_times=3, duration=0.5):
    """
    Scrolls to the bottom of the results on the screen.

    :param d: The device instance.
    :param scroll_times: Number of times to scroll to ensure reaching the bottom.
    :param duration: Duration of each swipe.
    """
    screen_size = d.window_size()
    for _ in range(scroll_times):
        d.swipe(
            screen_size[0] * 0.5, screen_size[1] * 0.8,
            screen_size[0] * 0.5, screen_size[1] * 0.2,
            duration=duration
        )
        sleep(2)