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
├── locators.py               # UI element locators
├── utils_ui_navigation.py    # UI navigation utilities
├── utils_ui_verification.py  # UI verification utilities
├── utils_scrolling.py        # Scrolling utilities
├── utils_device_interaction.py # Device interaction utilities
├── utils_authentication.py    # Authentication utilities
└── tests/                    # Test modules
```

### Test Modules

1. **Authentication (1_tests_sign_in_user_password.py)**
   - Sign in with valid credentials
   - Password reset functionality
   - Error handling

2. **Search Module (2_tests_search_module.py)**
   - Search for events
   - Search for businesses
   - Search for day trips
   - Search for videos

3. **Home Screen (3_tests_home_screen.py)**
   - Video section navigation
   - Content scrolling
   - UI element verification

4. **Location Management (4_tests_location_management.py)**
   - Location services
   - Permission handling

5. **Settings (5_tests_settings.py)**
   - User preferences
   - Profile management

6. **Content Features**
   - Events (6_tests_events.py)
   - Businesses (7_tests_businesses.py)
   - Day Trips (8_tests_day_trips.py)
   - Trails (9_tests_trails.py)
   - Videos (10_tests_videos.py)

7. **User Features**
   - Favorites (11_tests_favorites.py)
   - Visit History (12_tests_visit_history.py)
   - Map View (13_tests_view_map.py)
   - Guest Mode (14_tests_guest_mode.py)

## Utility Classes

### Navigation (utils_ui_navigation.py)
- **NavForgotPassword**: Password reset navigation
- **NavVideos**: Video section navigation
- **NavSignIn**: Sign-in flow navigation

### Verification (utils_ui_verification.py)
- **VerifyEvents**: Event search result verification
- **VerifyBusinesses**: Business search result verification
- **VerifyDayTrips**: Day trip search result verification
- **VerifyPasswordReset**: Password reset verification
- **VerifyVideos**: Video playback verification

### Scrolling (utils_scrolling.py)
- **GeneralScrolling**: Generic scrolling functionality
- **ScrollVideos**: Video section scrolling

### Device Interaction (utils_device_interaction.py)
- **LaunchApp**: App launch and permissions
- **SearchSubmit**: Search functionality
- **ForgotPassword**: Password reset flow
- **EditProfile**: Profile management

### Authentication (utils_authentication.py)
- **SignInPrepare**: Authentication preparation and handling

## Running Tests

### All Tests
```bash
pytest
```

### Smoke Tests
```bash
pytest -v -m smoke
```

### Specific Test File
```bash
pytest -v <test_file.py>
```

### Specific Test
```bash
pytest -v <test_file.py>::<test_name>
```

## Test Reports

### Structure
```
reports/
└── test_run_YYYYMMDD_HHMMSS/
    ├── test_report.html
    └── screenshots/
        ├── <test_number>_<step>_<description>.png
        └── ...
```

### Features
- Automatic HTML report generation
- Screenshot capture at key points
- Failure screenshots
- Test execution statistics
- Detailed error messages

## Best Practices

### Element Location
- Use flexible XPath selectors
- Prefer text-based location
- Include appropriate timeouts
- Handle dynamic elements

### UI Interaction
- Use utility classes for common operations
- Implement smart scrolling
- Handle permissions and popups
- Verify element state before interaction

### Test Organization
- Group related tests together
- Use descriptive test names
- Add proper documentation
- Implement smoke tests for critical paths

### Verification
- Use non-assertive methods when appropriate
- Include clear error messages
- Take screenshots for verification
- Handle timeouts properly

## Maintenance

### Regular Tasks
- Update locators for UI changes
- Review and update screenshots
- Check test stability
- Update documentation

### Code Standards
- Follow Python PEP 8
- Use clear naming conventions
- Add proper docstrings
- Keep methods focused and simple

## Contributing

1. Follow existing code structure
2. Add proper documentation
3. Include test cases
4. Update README for new features

## Troubleshooting

### Common Issues
1. Device Connection
   - Check ADB connection
   - Verify USB debugging
   - Restart ADB server if needed

2. Test Failures
   - Check app state
   - Verify locators
   - Review screenshots
   - Check error messages

3. Performance
   - Monitor device resources
   - Review wait times
   - Check for memory leaks

## Support

For issues and questions:
1. Check documentation
2. Review existing issues
3. Contact development team
