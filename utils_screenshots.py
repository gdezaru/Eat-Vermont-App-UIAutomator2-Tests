"""
Utility functions for screenshots management
"""
from datetime import datetime
import os
import pytest


class ScreenshotsManagement:
    def __init__(self, device):
        """
        Initialize ScreenshotsManagement with a device instance.

        Args:
            device: UIAutomator2 device instance
        """
        self.device = device

    @staticmethod
    def get_screenshots_dir():
        """
        Get the screenshots directory for the current test run.

        Returns:
            str: Path to the screenshots directory, or None if not found
        """
        # Get the current test run folder from the reporter
        from conftest import reporter
        if reporter and hasattr(reporter, 'screenshots_folder'):
            return reporter.screenshots_folder
        return None

    def take_screenshot(self, name):
        """
        Take a screenshot and save it with timestamp.

        Args:
            name: Base name for the screenshot file

        Returns:
            str: Path where the screenshot was saved
        """
        screenshots_dir = self.get_screenshots_dir()
        if screenshots_dir is None:
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f"{name}_{timestamp}.png"
        screenshot_path = os.path.join(screenshots_dir, screenshot_name)
        self.device.screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    def save_screenshot(self, filename: str, request) -> str:
        """
        Save a screenshot to the current test run's screenshots folder.

        Args:
            filename: The desired filename for the screenshot
            request: The pytest request fixture

        Returns:
            str: The path where the screenshot was saved
        """
        # Get the current test run folder from the reporter
        reporter = request.config.pluginmanager.get_plugin('excel_reporter')
        if not reporter:
            # Fallback to saving in the current directory if reporter not found
            return self.device.screenshot(filename)

        # Save screenshot in the test run's screenshots folder
        screenshot_path = os.path.join(reporter.screenshots_folder, filename)
        return self.device.screenshot(screenshot_path)