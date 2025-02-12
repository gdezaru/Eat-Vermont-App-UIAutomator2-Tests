import os
from datetime import datetime
import pandas as pd
from typing import Dict, List, Any
import pytest
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
import traceback
import inspect
import shutil


class ExcelReporter:
    def __init__(self):
        self.results = []
        self.current_test = {}
        self.screenshots = {}
        self.steps = {}
        self.processed_tests = set()
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Create the base reports directory if it doesn't exist
        self.base_report_dir = os.path.join(os.getcwd(), 'reports')
        os.makedirs(self.base_report_dir, exist_ok=True)
        # Create a dedicated folder for this test run
        self.run_folder = os.path.join(
            self.base_report_dir,
            f'Eat_Vermont_Test_Run_{self.timestamp}'
        )
        os.makedirs(self.run_folder, exist_ok=True)
        # Create a screenshots subfolder
        self.screenshots_folder = os.path.join(self.run_folder, 'screenshots')
        os.makedirs(self.screenshots_folder, exist_ok=True)

    def _extract_steps_from_docstring(self, docstring: str) -> List[str]:
        """Extract steps from docstring in a clean format."""
        if not docstring:
            return []
            
        steps = []
        lines = docstring.split('\n')
        in_steps_section = False
        
        for line in lines:
            line = line.strip()
            if line.lower().startswith('steps:'):
                in_steps_section = True
                continue
            elif in_steps_section and line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                # Remove the number and clean up the step
                step = line.split('.', 1)[1].strip()
                steps.append(step)
            elif in_steps_section and not line:  # Empty line after steps section
                break
                
        return steps

    def pytest_runtest_logstart(self, nodeid: str, location: tuple):
        """Called at the start of running the runtest protocol for a single test item."""
        self.current_test = {
            'test_name': nodeid,
            'start_time': datetime.now(),
            'status': 'running',
            'error_message': '',
            'traceback': '',
            'screenshots': [],
            'steps_to_reproduce': ''  # Initialize as empty string
        }

    def add_step(self, nodeid: str, step: str):
        """Add a step to the current test"""
        if nodeid not in self.steps:
            self.steps[nodeid] = []
        self.steps[nodeid].append(step)

    def pytest_runtest_logreport(self, report: TestReport):
        """Called for test setup, call, and teardown."""
        if report.when == "call" and report.nodeid not in self.processed_tests:
            self.processed_tests.add(report.nodeid)  # Mark this test as processed
            
            if report.passed:
                self.current_test['status'] = 'passed'
            elif report.failed:
                self.current_test['status'] = 'failed'
                if hasattr(report, 'longrepr'):
                    self.current_test['error_message'] = str(report.longrepr)
                    if hasattr(report.longrepr, 'traceback'):
                        self.current_test['traceback'] = ''.join(traceback.format_tb(report.longrepr.traceback[-1].frame.tb))
            elif report.skipped:
                self.current_test['status'] = 'skipped'
                
            # Get test function from the report item directly
            test_function = getattr(report, 'item', None)
            if test_function:
                test_function = test_function.function
            
            # Extract steps from docstring for all tests
            if test_function and test_function.__doc__:
                steps = self._extract_steps_from_docstring(test_function.__doc__)
                if steps:
                    self.current_test['steps_to_reproduce'] = '\n'.join([f"{i+1}. {step}" for i, step in enumerate(steps)])
                
            self.current_test['end_time'] = datetime.now()
            self.current_test['duration'] = (self.current_test['end_time'] - self.current_test['start_time']).total_seconds()
            
            # Add the test result to our collection
            self.results.append(self.current_test.copy())
            
    def pytest_sessionfinish(self, session: pytest.Session, exitstatus: int):
        """Called after whole test run finished, right before returning the exit status to the system."""
        # Move screenshots from root screenshots folder to test run folder
        root_screenshots_dir = os.path.join(os.getcwd(), 'screenshots')
        if os.path.exists(root_screenshots_dir):
            for screenshot in os.listdir(root_screenshots_dir):
                src = os.path.join(root_screenshots_dir, screenshot)
                dst = os.path.join(self.screenshots_folder, screenshot)
                shutil.move(src, dst)
                print(f"Moved screenshot {screenshot} to test run folder")

        # Create summary file
        summary_file = os.path.join(self.run_folder, 'test_run_summary.txt')
        with open(summary_file, 'w') as f:
            f.write("Test Run Summary\n")
            f.write("===============\n\n")
            f.write(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Count test results
            total_tests = len(self.results)
            passed_tests = len([r for r in self.results if r['status'] == 'passed'])
            failed_tests = len([r for r in self.results if r['status'] == 'failed'])
            skipped_tests = len([r for r in self.results if r['status'] == 'skipped'])
            
            f.write(f"Total Tests: {total_tests}\n")
            f.write(f"Passed: {passed_tests}\n")
            f.write(f"Failed: {failed_tests}\n")
            f.write(f"Skipped: {skipped_tests}\n\n")
            
            # Add report file info
            report_file = f"test_report_{self.timestamp}.xlsx"
            f.write(f"Test Report: {report_file}\n")
            
            # Add screenshots info
            screenshots = os.listdir(self.screenshots_folder)
            f.write(f"Screenshots: {len(screenshots)} files in screenshots/\n")

        # Create Excel report
        df = pd.DataFrame(self.results)
        excel_file = os.path.join(self.run_folder, f"test_report_{self.timestamp}.xlsx")
        
        # Ensure all columns exist with default values
        required_columns = [
            'test_name',
            'status',
            'start_time',
            'end_time',
            'duration',
            'error_message',
            'traceback',
            'screenshots',
            'steps_to_reproduce'
        ]
        
        for col in required_columns:
            if col not in df.columns:
                df[col] = ''
                
        # Convert all columns to string to avoid Excel formatting issues
        for col in df.columns:
            df[col] = df[col].astype(str)
            
        # Create Excel writer object
        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            # Write the main results sheet
            df.to_excel(writer, sheet_name='Test Results', index=False)
            
            # Get the xlsxwriter workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Test Results']
            
            # Add column auto-filter
            worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
            
            # Define formats
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            pass_format = workbook.add_format({
                'fg_color': '#C6EFCE',
                'font_color': '#006100'
            })
            
            fail_format = workbook.add_format({
                'fg_color': '#FFC7CE',
                'font_color': '#9C0006'
            })

            # Add text wrapping format for steps
            steps_format = workbook.add_format({
                'text_wrap': True,
                'valign': 'top',
                'align': 'left'
            })
            
            # Write headers with format
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Format the status column
            status_col = df.columns.get_loc('status')
            for row_num, status in enumerate(df['status'], start=1):
                if status == 'passed':
                    worksheet.write(row_num, status_col, status, pass_format)
                elif status == 'failed':
                    worksheet.write(row_num, status_col, status, fail_format)
                else:
                    worksheet.write(row_num, status_col, status)

            # Format the steps column with text wrapping
            steps_col = df.columns.get_loc('steps_to_reproduce')
            for row_num, steps in enumerate(df['steps_to_reproduce'], start=1):
                worksheet.write(row_num, steps_col, steps, steps_format)
            
            # Set column widths
            worksheet.set_column('A:A', 50)  # test_name
            worksheet.set_column('B:B', 10)  # status
            worksheet.set_column('C:D', 20)  # start_time, end_time
            worksheet.set_column('E:E', 10)  # duration
            worksheet.set_column('F:F', 50)  # error_message
            worksheet.set_column('G:G', 50)  # traceback
            worksheet.set_column('H:H', 30)  # screenshots
            worksheet.set_column('I:I', 50)  # steps_to_reproduce

            # Set row height to accommodate wrapped text
            worksheet.set_default_row(30)
