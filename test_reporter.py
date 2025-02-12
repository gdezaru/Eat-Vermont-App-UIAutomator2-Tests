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
        print(f"\nExtracting steps from docstring:\n{docstring}")  # Debug print
        if not docstring:
            return []
            
        steps = []
        lines = [line.strip() for line in docstring.split('\n')]
        in_steps_section = False
        
        for line in lines:
            print(f"Processing line: '{line}'")  # Debug print
            
            # Start collecting steps when we see "Steps:"
            if 'steps:' in line.lower():
                print("Found steps section")  # Debug print
                in_steps_section = True
                continue
                
            # If we're in steps section and line starts with a number
            if in_steps_section and line and line[0].isdigit():
                print(f"Found step: {line}")  # Debug print
                steps.append(line)
            
            # Stop when we hit an empty line after collecting steps
            elif in_steps_section and not line and steps:
                break
        
        print(f"Extracted steps: {steps}")  # Debug print
        return steps

    def pytest_runtest_logstart(self, nodeid: str, location: tuple):
        """Called at the start of running the runtest protocol for a single test item."""
        self.current_test = {
            'test_name': nodeid,
            'start_time': datetime.now(),
            'status': 'running',
            'error_message': '',
            'traceback': '',
            'steps': ''
        }

    def add_step(self, nodeid: str, step: str):
        """Add a step to the current test"""
        if nodeid not in self.steps:
            self.steps[nodeid] = []
        self.steps[nodeid].append(step)

    def pytest_runtest_logreport(self, report: TestReport):
        """Called for test setup, call, and teardown."""
        if report.when == "call":  # Only process during the call phase
            if report.nodeid not in self.processed_tests:
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
                    
                # Get test function docstring
                try:
                    # Get the test function using the nodeid
                    module_name, test_name = report.nodeid.split("::")
                    module = __import__(module_name.replace("/", ".").replace(".py", ""))
                    test_function = getattr(module, test_name)
                    
                    print(f"\nProcessing test: {test_function.__name__}")  # Debug print
                    if test_function.__doc__:
                        # Extract and format steps
                        steps = self._extract_steps_from_docstring(test_function.__doc__)
                        if steps:
                            self.current_test['steps'] = '\n'.join(steps)
                            print(f"Set steps in current_test: {self.current_test['steps']}")  # Debug print
                        else:
                            print("No steps were extracted")  # Debug print
                    else:
                        print("No docstring found")  # Debug print
                except Exception as e:
                    print(f"Error getting test function: {e}")  # Debug print
                    
                self.current_test['end_time'] = datetime.now()
                self.current_test['duration'] = (self.current_test['end_time'] - self.current_test['start_time']).total_seconds()
                
                # Add the test result to our collection
                self.results.append(self.current_test.copy())
                print(f"Added test result with steps: {self.current_test['steps']}")  # Debug print

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
            'steps'
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
            
            # Set column widths first
            worksheet.set_column('A:A', 40)  # test_name
            worksheet.set_column('B:B', 25)  # start_time
            worksheet.set_column('C:C', 15)  # status
            worksheet.set_column('D:D', 40)  # error_message
            worksheet.set_column('E:E', 40)  # traceback
            worksheet.set_column('F:F', 50)  # steps
            worksheet.set_column('G:G', 25)  # end_time
            worksheet.set_column('H:H', 15)  # duration

            # Format header
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'vcenter',
                'align': 'center',
                'fg_color': '#E2EFDA',
                'border': 1,
                'border_color': '#D4D4D4',
                'font_size': 11
            })
            
            # Base format for all cells
            base_format = workbook.add_format({
                'text_wrap': True,
                'valign': 'vcenter',
                'align': 'center',
                'border': 1,
                'border_color': '#D4D4D4',
                'font_size': 11
            })
            
            pass_format = workbook.add_format({
                'text_wrap': True,
                'valign': 'vcenter',
                'align': 'center',
                'fg_color': '#C6EFCE',
                'border': 1,
                'border_color': '#D4D4D4',
                'font_size': 11
            })
            
            fail_format = workbook.add_format({
                'text_wrap': True,
                'valign': 'vcenter',
                'align': 'center',
                'fg_color': '#FFC7CE',
                'border': 1,
                'border_color': '#D4D4D4',
                'font_size': 11
            })

            # Steps format
            steps_format = workbook.add_format({
                'text_wrap': True,
                'valign': 'vcenter',
                'align': 'left',
                'border': 1,
                'border_color': '#D4D4D4',
                'font_size': 11
            })
            
            # Write headers with format
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Set default row height
            worksheet.set_default_row(45)  # Much taller rows for better readability
            
            # Write data with appropriate formats
            for row_num in range(1, len(df) + 1):
                row_height = 45  # Default minimum height
                
                for col_num, value in enumerate(df.iloc[row_num - 1]):
                    if pd.isna(value):
                        value = ''
                    
                    # Convert value to string and handle newlines
                    str_value = str(value).replace('\\n', '\n')
                    
                    # Calculate needed height based on content
                    num_lines = len(str_value.split('\n'))
                    needed_height = max(45, num_lines * 15)  # At least 45px, or more for multiline
                    row_height = max(row_height, needed_height)
                    
                    # Use appropriate format based on column
                    if df.columns[col_num] == 'status':
                        if value == 'passed':
                            worksheet.write(row_num, col_num, value, pass_format)
                        elif value == 'failed':
                            worksheet.write(row_num, col_num, value, fail_format)
                        else:
                            worksheet.write(row_num, col_num, value, base_format)
                    elif df.columns[col_num] == 'steps':
                        worksheet.write(row_num, col_num, str_value, steps_format)
                    else:
                        worksheet.write(row_num, col_num, str_value, base_format)
                
                # Set the calculated row height
                worksheet.set_row(row_num, row_height)
            
            # Set header row height
            worksheet.set_row(0, 45)  # Make header row same height
            
            # Enable text wrapping for the entire worksheet
            worksheet.set_column('A:H', None, None, {'text_wrap': True})
            
            # Freeze the header row
            worksheet.freeze_panes(1, 0)
            
            # Set print area
            worksheet.print_area(0, 0, len(df), len(df.columns) - 1)
            
            # Fit to page when printing
            worksheet.fit_to_pages(1, 0)
