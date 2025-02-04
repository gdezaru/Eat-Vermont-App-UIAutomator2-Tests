# Eat Vermont App UIAutomator2 Tests

This project contains automated tests for the Eat Vermont mobile application using Python and uiautomator2.

## Setup

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Connect your Android device with USB debugging enabled

## Running Tests

To run all tests:
```bash
pytest
```

To run a specific test file:
```bash
pytest test_login.py
```

## Project Structure

- `conftest.py`: Contains test fixtures and device configuration
- `locators.py`: Contains XPath locators for UI elements
- `utils.py`: Utility functions for screenshots and app state management
- `1_test_sign_in_user_password.py`: Test cases for login functionality
- `2_test_search_module.py`: Test cases for search functionality

## Notes

- Device should be connected and USB debugging enabled
- App should be installed on the device
- No Appium server needed - using uiautomator2 for direct device communication
