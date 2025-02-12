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

## Test Reports

The framework automatically generates detailed Excel reports after each test run. Reports include:

### Report Location
- Reports are saved in the `reports` directory
- Format: `test_report_YYYYMMDD_HHMMSS.xlsx`

### Report Contents
1. **Test Information**
   - Test name and status
   - Start and end times
   - Test duration

2. **Failure Analysis**
   - Error messages
   - Stack traces
   - Steps to reproduce
   - Screenshot locations

3. **Retry Information**
   - Number of retry attempts
   - Failure reason for each attempt
   - Final test status

### Viewing Reports
The Excel report includes:
- Color-coded test status (Green for pass, Red for fail)
- Filterable columns
- Detailed error information
- Links to failure screenshots

### Screenshots
- Automatically captured on test failure
- Saved in the `screenshots` directory
- Named with test name and timestamp
- Referenced in the Excel report

### Example Usage
```bash
# Run tests and generate report
pytest

# Report will be generated at:
# reports/test_report_YYYYMMDD_HHMMSS.xlsx
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
