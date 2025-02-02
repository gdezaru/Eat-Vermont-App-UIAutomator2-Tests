# Eat Vermont App Automated Tests

This project contains automated tests for the Eat Vermont mobile application using Python, Appium, and pytest.

## Setup

1. Install required packages:
```bash
pip install Appium-Python-Client pytest selenium
```

2. Start Appium server:
```bash
appium
```

3. Connect your Android device with USB debugging enabled

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

- `conftest.py`: Contains test fixtures and Appium configuration
- `test_login.py`: Test cases for login functionality
- More test files will be added for other features

## Notes

- Make sure Appium server is running before executing tests
- Device should be connected and USB debugging enabled
- App should be installed on the device
