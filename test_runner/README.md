# Eat Vermont App Test Automation Framework

This test automation framework provides a comprehensive solution for running and managing automated tests for the Eat Vermont App.

## Features

- Test Suite Selection
- Parallel Test Execution
- HTML Report Generation
- Test Retry Mechanism
- Device Configuration
- Environment Management
- Detailed Test Reports (Excel)
- Screenshot Collection for Failed Tests

## Directory Structure

```
test_runner/
├── config/
│   ├── device_config.py
│   ├── env_config.py
│   └── test_suites.py
├── utils/
│   ├── metrics.py
│   ├── report_generator.py
│   └── test_utils.py
├── reports/
│   └── README.md
├── requirements.txt
└── run_tests.py
```

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Configure your test environment in `config/env_config.py`

3. Set up device configurations in `config/device_config.py`

## Usage

### Basic Usage

Run all tests:
```bash
python run_tests.py
```

### Advanced Usage

1. Run specific test suite:
```bash
python run_tests.py --suite smoke
```

2. Run specific modules:
```bash
python run_tests.py --modules 1,2,3
```

3. Run tests in parallel:
```bash
python run_tests.py --parallel 4
```

4. Specify device:
```bash
python run_tests.py --device emulator-5554
```

5. Choose environment:
```bash
python run_tests.py --env staging
```

### Test Suites

- `smoke`: Critical path tests
- `regression`: Full test suite
- `guest`: Guest mode features
- `core`: Core functionality
- `features`: Feature-specific tests

### Reports

After test execution, you can find:
- HTML report in `reports/html/`
- Excel report in `reports/excel/`
- Screenshots in `reports/screenshots/`
- Logs in `reports/logs/`

## Report Details

### Excel Report Sheets

1. **Summary**
   - Overall test execution statistics
   - Pass/Fail rates
   - Duration metrics

2. **Detailed Results**
   - Test-by-test breakdown
   - Execution time
   - Error messages
   - Screenshots (if failed)

3. **Error Analysis**
   - Common error patterns
   - Flaky tests
   - Retry statistics

4. **Device Stats**
   - Device information
   - Performance metrics
   - Resource usage

5. **Time Analysis**
   - Test execution timeline
   - Peak failure times
   - Module execution distribution

## Detailed Usage Guide

### Prerequisites

1. Python 3.8 or higher
2. Android SDK and ADB tools installed
3. A connected Android device or emulator
4. The Eat Vermont App installed on the test device

### Initial Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd EatVermontAppAutomatedTests
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r test_runner/requirements.txt
```

### Running Tests

#### Basic Usage

1. Run all regression tests:
```bash
python test_runner/run_tests.py
```

2. Run a specific test suite:
```bash
python test_runner/run_tests.py --suite smoke
```

#### Advanced Usage

1. Run specific test modules:
```bash
# Run modules 1, 2, and 3
python test_runner/run_tests.py --modules 1,2,3
```

2. Run tests in parallel:
```bash
# Run with 4 parallel processes
python test_runner/run_tests.py --parallel 4
```

3. Run tests on a specific device:
```bash
# Using device serial number
python test_runner/run_tests.py --device emulator-5554

# Using device type
python test_runner/run_tests.py --device-type emulator
```

4. Run tests in a specific environment:
```bash
python test_runner/run_tests.py --env staging
```

5. Configure test retries:
```bash
# Retry failed tests up to 3 times
python test_runner/run_tests.py --reruns 3
```

6. Combine multiple options:
```bash
python test_runner/run_tests.py --suite smoke --parallel 4 --env staging --reruns 2
```

### Test Suites

The framework includes predefined test suites:

1. `smoke`: Critical path tests
   ```bash
   python test_runner/run_tests.py --suite smoke
   ```

2. `regression`: Full test suite
   ```bash
   python test_runner/run_tests.py --suite regression
   ```

3. `guest`: Guest mode features
   ```bash
   python test_runner/run_tests.py --suite guest
   ```

4. `core`: Core functionality
   ```bash
   python test_runner/run_tests.py --suite core
   ```

5. `features`: Feature-specific tests
   ```bash
   python test_runner/run_tests.py --suite features
   ```

### Reports and Results

After test execution, you can find the following in the `reports` directory:

1. Excel Report (`test_report_TIMESTAMP.xlsx`):
   - Summary sheet: Overall test statistics
   - Test Details: Individual test results
   - Error Analysis: Failure patterns and types
   - Device Stats: Device performance metrics
   - Time Analysis: Execution timeline and patterns

2. HTML Report (`report.html`):
   - Interactive test results
   - Test execution details
   - Failure screenshots
   - Error messages and tracebacks

3. Log File (`test_run.log`):
   - Detailed execution logs
   - Debug information
   - Error traces

### Understanding Test Results

#### Excel Report Sheets

1. **Summary Sheet**
   - Total number of tests
   - Pass/fail rates
   - Total and average duration
   - Flaky test statistics

2. **Test Details Sheet**
   - Individual test results
   - Execution time per test
   - Retry attempts
   - Failure messages

3. **Error Analysis Sheet**
   - Common error patterns
   - Error frequency
   - Error messages and stack traces

4. **Device Stats Sheet**
   - Device information
   - Resource usage (CPU, memory)
   - Performance metrics

5. **Time Analysis Sheet**
   - Test execution timeline
   - Peak failure times
   - Module execution distribution

### Customization

#### Adding New Test Suites

1. Edit `config/test_suites.py`:
```python
SUITES = {
    'your_suite': {
        'description': 'Your suite description',
        'modules': ['module1', 'module2'],
        'priority': 'high',
        'max_retries': 2,
        'parallel': True,
    }
}
```

#### Modifying Environment Settings

1. Edit `config/env_config.py`:
```python
ENVIRONMENTS = {
    'your_env': {
        'app_url': 'https://your-url.com',
        'timeout': 15,
        'retry_attempts': 2,
        # Add other settings
    }
}
```

#### Configuring Device Settings

1. Edit `config/device_config.py`:
```python
CONFIGURATIONS = {
    'your_device': {
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'deviceName': 'your-device-id',
        # Add other capabilities
    }
}
```

### Best Practices

1. **Test Organization**
   - Group related tests in modules
   - Use meaningful test names
   - Add proper docstrings and comments

2. **Device Management**
   - Ensure device is properly connected
   - Clear app data between test runs
   - Monitor device performance

3. **Error Handling**
   - Add appropriate wait times
   - Handle expected exceptions
   - Add retry mechanisms for flaky tests

4. **Reporting**
   - Review all report sheets
   - Monitor trends over time
   - Address recurring failures

## Contributing

1. Follow the existing code structure
2. Add appropriate tests for new features
3. Update documentation as needed
4. Ensure all tests pass before submitting changes

## Troubleshooting

### Common Issues

1. Device not found:
   - Check device connection
   - Verify ADB is running
   - Ensure device ID is correct

2. Test failures:
   - Check test environment configuration
   - Verify app state
   - Review error logs

3. Report generation issues:
   - Ensure write permissions
   - Check disk space
   - Verify required packages are installed

### Support

For additional support:
1. Check the logs in `reports/logs/`
2. Review error messages in the Excel report
3. Check screenshot evidence for failed tests
