"""
Utility functions for screenshots management
"""
from datetime import datetime
import os


def get_screenshots_dir():
    """Get the screenshots directory for the current test run"""
    # Get the current test run folder from the reporter
    import pytest
    reporter = next((plugin for plugin in pytest.get_platform().pluginmanager.get_plugins()
                     if hasattr(plugin, 'screenshots_folder')), None)
    if reporter:
        return reporter.screenshots_folder
    return None


def take_screenshot(d, name):
    """Take a screenshot and save it with timestamp"""
    screenshots_dir = get_screenshots_dir()
    if screenshots_dir is None:
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_name = f"{name}_{timestamp}.png"
    screenshot_path = os.path.join(screenshots_dir, screenshot_name)
    d.screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")


def save_screenshot(d, filename: str, request) -> str:
    """
    Save a screenshot to the current test run's screenshots folder.

    Args:
        d: The UI Automator device instance
        filename: The desired filename for the screenshot
        request: The pytest request fixture

    Returns:
        str: The path where the screenshot was saved
    """
    # Get the current test run folder from the reporter
    reporter = request.config.pluginmanager.get_plugin('excel_reporter')
    if not reporter:
        # Fallback to saving in the current directory if reporter not found
        return d.screenshot(filename)

    # Save screenshot in the test run's screenshots folder
    screenshot_path = os.path.join(reporter.screenshots_folder, filename)
    return d.screenshot(screenshot_path)