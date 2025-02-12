# Eat Vermont App UIAutomator2 Tests

This project contains automated tests for the Eat Vermont mobile application using Python, pytest, and UIAutomator2.

## Features

- **Framework**: Python + pytest + UIAutomator2
- **Retry Mechanism**: Automatic retry for flaky tests
- **Excel Reporting**: Detailed test results with failure analysis
- **Modular Structure**: Organized by functionality
- **Utilities**: Common functions and helpers
- **Locators**: Centralized XPath definitions
- **Configuration**: Flexible test configuration

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
├── conftest.py              # Test fixtures and configuration
├── config.py               # Test configuration and constants
├── locators.py            # UI element locators
├── utils.py               # Utility functions
├── retry_decorator.py     # Retry mechanism for flaky tests
├── requirements.txt       # Project dependencies
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
To run all tests:
```bash
pytest
```

### Run Specific Test File
```bash
pytest 1_tests_sign_in_user_password.py
```

### Run Specific Test
```bash
pytest 1_tests_sign_in_user_password.py::test_sign_in_user_password
```

### Run with Verbose Output
```bash
pytest -v
```

### Run Tests in Parallel
```bash
pytest -n auto  # Runs tests in parallel using available CPU cores
```

### Run Smoke Tests
To run smoke tests:
```bash
pytest -m smoke
```

### Run Tests in Numerical Order
The test files are numbered from 1 to 14 (e.g., `1_tests_sign_in_user_password.py`, `2_tests_search_module.py`, etc.). To run smoke tests in numerical order, use:
```bash
python run_ordered_tests.py
```

This script will:
1. Find all test files that start with a number
2. Sort them in natural numerical order (1, 2, 3... instead of 1, 10, 11...)
3. Run only the smoke tests from these files in sequence
4. Generate a test report in the `reports` directory

## Retry Mechanism

The framework includes an automatic retry mechanism for handling flaky tests:

- Default configuration: 2 retries with 1-second delay
- Retries on AssertionError and TimeoutError
- Can be customized per test using decorators:

```python
@retry(retries=3, delay=2, backoff=2, exceptions=(AssertionError, TimeoutError))
def test_flaky_feature():
    # Test code here
```

## Screenshot Management

The framework includes a robust screenshot management system:

### Screenshot Organization
- Screenshots are initially saved to a root `screenshots` directory
- After each test run completes, screenshots are automatically moved to a test-specific folder within the `reports` directory
- Each test run gets its own timestamped folder to prevent overwriting

### Screenshot Naming Convention
- Screenshots follow a consistent naming pattern:
  - `<test_number>_<test_part>_<description>.png`
  - Example: `7_1_1_business_card_with_event.png`

### Screenshot Locations
1. **During Test Execution**
   - Temporarily stored in: `screenshots/`
   - Managed by the `screenshots_dir` fixture

2. **After Test Completion**
   - Moved to: `reports/test_run_YYYYMMDD_HHMMSS/screenshots/`
   - Organized alongside the test report

### Screenshot Usage
- Screenshots are taken at key points in tests to document UI state
- Additional screenshots are automatically captured on test failures
- All screenshots are referenced in the Excel report with clickable links

## Test Reports

The framework generates comprehensive Excel reports after each test run:

### Report Structure
1. **Test Run Directory**
   ```
   reports/
   └── test_run_YYYYMMDD_HHMMSS/
       ├── test_report.xlsx
       └── screenshots/
           ├── 7_1_1_business_card_with_event.png
           ├── 7_1_2_business_card_with_menu.png
           └── ...
   ```

2. **Excel Report Contents**
   - Test execution summary
   - Detailed test results
   - Screenshot references
   - Error logs and stack traces
   - Test retry information

### Report Features
- **Screenshot Integration**: Direct links to screenshots
- **Failure Analysis**: Detailed error information
- **Test Statistics**: Pass/fail rates and durations
- **Filtering**: Sortable and filterable columns
- **Color Coding**: Visual status indicators

### Example Usage
```bash
# Run tests and generate report
pytest

# Report and screenshots will be in:
# reports/test_run_YYYYMMDD_HHMMSS/
```

## Key Components

### conftest.py
- Test fixtures
- Device setup and teardown
- Screenshot capture on failure
- Test reporting configuration

### locators.py
- XPath and UI element selectors
- Organized by screen/feature
- Maintainable centralized locators

### utils.py
- Common test utilities
- Helper functions
- State management

### retry_decorator.py
- Retry mechanism implementation
- Configurable retry settings
- Logging for retry attempts

## Best Practices

1. **Test Independence**
   - Each test should be independent
   - Clean up any test data
   - Reset app state when needed

2. **Locator Management**
   - Keep locators in `locators.py`
   - Use meaningful names
   - Comment complex XPaths

3. **Error Handling**
   - Use appropriate assertions
   - Include meaningful error messages
   - Handle timeouts properly

4. **Test Data**
   - Use configuration files
   - Avoid hardcoding test data
   - Use meaningful test data

## Troubleshooting

### Common Issues

1. **Device Not Found**
   - Ensure USB debugging is enabled
   - Check USB connection
   - Verify ADB device list

2. **Element Not Found**
   - Check locator definitions
   - Verify app state
   - Add appropriate waits

3. **Test Flakiness**
   - Increase wait times
   - Add retry mechanism
   - Check for race conditions

### Debug Tips

1. Use verbose mode for more details:
```bash
pytest -v
```

2. Enable debug logging:
```bash
pytest --log-cli-level=DEBUG
```

3. Generate HTML report:
```bash
pytest --html=report.html
```

## Contributing

1. Follow the existing code structure
2. Add appropriate tests for new features
3. Update documentation as needed
4. Use meaningful commit messages

## License

[Your License Information]

## Contact

[Your Contact Information]
