# Eat Vermont App UIAutomator2 Tests

This project contains automated tests for the Eat Vermont mobile application using Python, pytest, and UIAutomator2.

## Features

- **Framework**: Python + pytest + UIAutomator2
- **Enhanced UI Interaction**: Robust element finding and scrolling mechanisms
- **Smart Scrolling**: Intelligent positioning of elements in viewport
- **Flexible Verification**: Non-assertive verification methods returning boolean results
- **Modular Structure**: Organized by functionality
- **Utilities**: Common functions and helpers
- **Locators**: Centralized XPath definitions
- **Configuration**: Flexible test configuration
- **Screenshot Documentation**: Comprehensive visual test documentation

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

## Project Structure

```
EatVermontAppAutomatedTests/
├── conftest.py                # Test fixtures and configuration
├── config.py                  # Test configuration and constants
├── locators.py               # UI element locators
├── utils_ui_navigation.py    # UI navigation utilities
├── utils_ui_verification.py  # UI verification utilities
├── utils_scrolling.py       # Scrolling and positioning utilities
├── utils_device_interaction.py # Device interaction utilities
├── utils_authentication.py   # Authentication utilities
└── tests/
    ├── 1_tests_sign_in_user_password.py  # Authentication tests
    ├── 2_tests_search_module.py          # Search functionality tests
    ├── 3_tests_home_screen.py           # Home screen tests
    ├── 4_tests_location_management.py   # Location management tests
    ├── 5_tests_settings.py             # Settings tests
    ├── 6_tests_events.py              # Events functionality tests
    ├── 7_tests_businesses.py         # Business listing tests
    ├── 8_tests_day_trips.py         # Day trips feature tests
    ├── 9_tests_trails.py           # Trails feature tests
    ├── 10_tests_videos.py         # Video content tests
    ├── 11_tests_favorites.py     # Favorites functionality tests
    ├── 12_tests_visit_history.py # Visit history tests
    ├── 13_tests_view_map.py    # Map view tests
    └── 14_tests_guest_mode.py  # Guest mode tests
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Smoke Tests Only
```bash
pytest -v -m smoke
```

### Run Specific Test File
```bash
pytest -v <test_file.py>
```

### Run Specific Test
```bash
pytest -v <test_file.py>::<test_name>
```

## Key Features and Improvements

### Smart UI Interaction
- Enhanced scrolling mechanisms that ensure elements are properly positioned in viewport
- Intelligent positioning of elements in first quarter of screen for better interaction
- Non-assertive verification methods that return boolean results for better flow control

### Modular Utilities
- **utils_ui_navigation.py**: Functions for navigating through the app
- **utils_ui_verification.py**: Functions for verifying UI elements and states
- **utils_scrolling.py**: Smart scrolling and element positioning
- **utils_device_interaction.py**: Device-level interactions
- **utils_authentication.py**: Authentication and user management

### Robust Locators
- Centralized XPath definitions in locators.py
- Carefully crafted selectors for reliability
- Organized by functional area (Events, Businesses, Trails, etc.)

### Screenshot Documentation
- Automatic screenshot capture at key points
- Organized by test case and step
- Stored in screenshots directory with clear naming convention

## Test Reporting

The framework includes comprehensive test reporting functionality:

### Report Generation
- Reports are automatically generated after each test run
- Located in the `reports` directory with timestamp: `reports/test_run_YYYYMMDD_HHMMSS/`
- Each test run gets its own directory to prevent overwriting

### Report Contents
1. **Test Summary**
   - Total tests run
   - Pass/fail statistics
   - Test duration
   - Environment details

2. **Detailed Test Results**
   - Individual test status
   - Test execution time
   - Error messages and stack traces for failures
   - Links to associated screenshots

3. **Screenshot Integration**
   - Screenshots are organized in the `screenshots` subdirectory
   - Named with clear convention: `<test_number>_<step>_<description>.png`
   - Referenced in the report with clickable links
   - Captured automatically on test failures

### Report Format
```
reports/
└── test_run_YYYYMMDD_HHMMSS/
    ├── test_report.html       # Main test report
    └── screenshots/           # Test screenshots
        ├── 7_1_1_business_card_with_event.png
        ├── 7_1_2_business_card_with_menu.png
        └── ...
```

### Viewing Reports
- Open the HTML report in any web browser
- Navigate through test results using the interactive interface
- Filter and search test results
- View screenshots directly from the report

## Best Practices

1. **Element Location**
   - Use flexible XPath selectors
   - Prefer text-based location when possible
   - Include timeouts for dynamic elements

2. **Scrolling and Positioning**
   - Use smart scrolling utilities
   - Ensure elements are properly positioned before interaction
   - Include appropriate waits after scrolling

3. **Verification**
   - Use non-assertive verification when appropriate
   - Include clear error messages
   - Capture screenshots for verification failures

4. **Test Organization**
   - Follow naming convention for test files
   - Group related tests together
   - Use appropriate markers (e.g., @pytest.mark.smoke)

## Maintenance

- Keep locators updated as app UI changes
- Review and update screenshot references
- Maintain clear documentation of changes
- Regular review of test stability and performance

## Contributing

1. Follow the existing code structure
2. Update documentation for significant changes
3. Test thoroughly before submitting changes
4. Include relevant screenshots or examples

## Support

For issues or questions, please contact the test automation team.
