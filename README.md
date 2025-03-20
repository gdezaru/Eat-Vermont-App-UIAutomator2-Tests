# Eat Vermont App UIAutomator2 Tests

A comprehensive test automation framework for the Eat Vermont mobile application using Python, pytest, and UIAutomator2.

## Overview

This framework provides automated testing capabilities for the Eat Vermont mobile application, covering various functionalities from authentication to content exploration. Built with maintainability, reliability, and extensibility in mind.

## Key Features

- **Modular Architecture**: Well-organized utility classes for different functionalities
- **Smart UI Interaction**: Robust element handling and intelligent scrolling
- **Comprehensive Test Coverage**: Tests for all major app features
- **Detailed Reporting**: Screenshots and HTML reports for test runs
- **Maintainable Structure**: Clear separation of concerns and reusable components

## Prerequisites

- Python 3.9+
- Android device with USB debugging enabled
- Eat Vermont app installed on the device
- ADB (Android Debug Bridge) installed and in PATH

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd EatVermontAppAutomatedTests
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Connect your Android device and verify ADB connection:
```bash
adb devices
```

## Framework Structure

### Core Components

```
EatVermontAppAutomatedTests/
├── conftest.py                # Test fixtures and configuration
├── config.py                  # Test configuration and constants
├── locators.py                # UI element locators
├── utils_ui_navigation.py     # UI navigation utilities
├── utils_ui_verification.py   # UI verification utilities
├── utils_scrolling.py         # Scrolling utilities
├── utils_device_interaction.py # Device interaction utilities
├── utils_authentication.py    # Authentication utilities
├── utils_cache_management.py  # Cache cleanup utilities
├── utils_screenshots.py       # Screenshot utilities
├── utils_settings.py          # Settings management utilities
├── utils_wait.py              # Wait utilities
├── 1_tests_sign_in_user_password.py # Test modules (numbered for execution order)
├── 2_tests_ask_ai.py
├── ...
└── EatVermontAutomatedTestsSpares/ # Archived tests for future reference
```

### Test Modules

1. **Authentication (1_tests_sign_in_user_password.py)**
   - Sign in with valid credentials
   - Password reset functionality
   - Error handling

2. **Ask AI (2_tests_ask_ai.py)**
   - AI search functionality
   - Result verification

3. **Home Screen (3_tests_home_screen.py)**
   - Video section navigation
   - Content scrolling
   - UI element verification

4. **Settings (4_tests_settings.py)**
   - User preferences
   - Profile management
   - Dietary preferences

5. **Content Features**
   - Events (5_tests_events.py)
   - Businesses (6_tests_businesses.py)
   - Day Trips (7_tests_day_trips.py)
   - Trails (8_tests_trails.py)

6. **User Features**
   - Favorites (10_tests_favorites.py)
   - Visit History (11_tests_check_in_visit_history.py)
   - Map View (12_tests_view_map.py)
   - Guest Mode (13_tests_guest_mode.py)

## Utility Classes

### Navigation (utils_ui_navigation.py)
- **NavEvents**: Event section navigation
- **NavBusinesses**: Business section navigation
- **NavDayTripsTrails**: Day trips and trails navigation
- **NavFavoritesVisitHistory**: Favorites and visit history navigation
- **NavViewMap**: Map view navigation

### Verification (utils_ui_verification.py)
- **VerifyEvents**: Event search result verification
- **VerifyBusinesses**: Business search result verification
- **VerifyEventsFilters**: Event filter verification

### Scrolling (utils_scrolling.py)
- **GeneralScrolling**: Generic scrolling functionality
- **EventsScrolling**: Events section scrolling

### Device Interaction (utils_device_interaction.py)
- **LaunchApp**: App launch and permissions
- **SearchSubmit**: Search functionality
- **SearchAI**: AI search functionality
- **ForgotPassword**: Password reset flow
- **EditProfile**: Profile management

### Authentication (utils_authentication.py)
- **SignInPrepare**: Authentication preparation and handling
- **GuestModeAuth**: Guest mode authentication

### Cache Management (utils_cache_management.py)
- **clear_python_cache**: Removes Python bytecode cache folders
- **clear_screenshot_cache**: Cleans up old screenshots
- **clear_old_reports**: Removes old test reports

### Screenshots (utils_screenshots.py)
- **ScreenshotsManagement**: Screenshot capture and organization

## Running Tests

### Device Configuration

The test framework supports running tests on any Android device. You can specify your device in two ways:

1. **Using Device ID**
```bash
pytest --device-id=your_device_id
```

2. **Automatic Device Detection**
If you don't specify a device ID, the framework will automatically use the first connected Android device. Simply connect your device via USB and run:
```bash
pytest
```

3. **Custom App Package**
If you're testing a different build of the app (e.g., debug version), you can specify the package name:
```bash
pytest --app-package=com.eatvermont.debug
```

### Required Device Setup
1. Enable USB debugging on your Android device
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times to enable Developer Options
   - Go to Settings > Developer Options
   - Enable "USB Debugging"
2. Connect your device via USB
3. Accept the USB debugging prompt on your device
4. Verify connection by running:
```bash
adb devices
```

### Running Specific Tests

1. **Run All Tests**
```bash
pytest
```

2. **Run Smoke Tests**
```bash
pytest -v -m smoke
```

3. **Run a Specific Test File**
```bash
pytest -v <test_file.py>
```

4. **Run a Specific Test**
```bash
pytest -v -k "test_name"
```

Example:
```bash
pytest -v -k "test_forgot_password" 1_tests_sign_in_user_password.py
```

### Test Reports

#### Structure
```
reports/
└── Eat_Vermont_Test_Run_YYYYMMDD_HHMMSS/
    ├── test_run_summary.txt
    ├── test_report.xlsx
    └── screenshots/
        ├── fail_test_name_timestamp.png
        └── ...
```

#### Report Contents
- Test execution timestamps
- Test status (pass/fail)
- Test steps from docstrings
- Screenshots of failures
- Test execution statistics
- Detailed error messages

## Recent Framework Changes

The framework has undergone several important improvements:

1. **Cache Management**: Added automatic cleanup of unnecessary cache including:
   - Python bytecode cache (__pycache__ directories)
   - Old screenshots (configurable retention period)
   - Old test reports (configurable retention period)

2. **Improved Error Handling**: Removed try-except blocks from test code for better error visibility and debugging.

3. **Test Structure Reorganization**: 
   - Current active tests are maintained in the main directory
   - Legacy tests have been archived in the EatVermontAutomatedTestsSpares folder for future reference

4. **Optimized Screenshot Handling**:
   - Improved screenshot capture during test failures
   - Better organization of screenshots in test reports

5. **Enhanced Logging**:
   - More detailed logs for test execution
   - Clear error messages for test failures

## Legacy Tests

Tests for features that are currently not active in the app have been moved to the EatVermontAutomatedTestsSpares folder. These tests are preserved for reference and can be reactivated if the corresponding features are restored in the app.

To use a test from the spares folder:
1. Copy the test file to the main directory
2. Ensure all required utilities and dependencies are available
3. Update the test if necessary to match the current framework structure
4. Run the test using the standard test commands

## Best Practices

### Element Location
- Use unique identifiers wherever possible (resourceId, contentDesc)
- Fall back to XPath selectors when necessary
- Define all selectors in locators.py for maintainability

### Test Structure
- Keep tests independent
- Clean state before each test
- Follow Arrange-Act-Assert pattern
- Document test steps in docstrings
- Include detailed assertions with clear error messages

### Error Handling
- Do not use try-except blocks in test code
- Let test failures surface with clear error messages
- Use proper waits and verification steps
- Add descriptive assertions that clearly indicate what failed

### Screenshots
- Take screenshots at key verification points
- Name screenshots descriptively
- Include timestamp in filename
- Always take screenshots on test failures

## Contributing

1. Follow the existing code structure and patterns
2. Update documentation when adding new features
3. Add appropriate docstrings for new functions
4. Ensure tests run independently
5. Add smoke tests for critical functionality

## Troubleshooting

### Common Issues

1. **ADB Connection Issues**
   - Ensure USB debugging is enabled
   - Check USB cable connection
   - Restart ADB server: `adb kill-server && adb start-server`
   - Accept USB debugging prompt on device

2. **Element Not Found Errors**
   - Check if the app UI has changed
   - Update selectors in locators.py
   - Add appropriate wait conditions
   - Verify screen state with screenshots

3. **Test Timeouts**
   - Check for slow network conditions
   - Increase wait timeouts if necessary
   - Verify app is responding properly

4. **App State Issues**
   - Ensure app is properly cleared between tests
   - Check app permissions are granted
   - Verify notification handling
