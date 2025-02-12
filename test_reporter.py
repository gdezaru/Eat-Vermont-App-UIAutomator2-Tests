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


class ExcelReporter:
    def __init__(self):
        self.results = []
        self.current_test = {}
        self.screenshots = {}
        self.steps = {}  # Add steps dictionary back
        
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
        if report.when == "call":
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
                
            # Get test function and extract steps for all tests
            test_function = None
            for item in pytest.test_items:
                if item.nodeid == self.current_test['test_name']:
                    test_function = item.function
                    break
            
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
        # Create the report directory if it doesn't exist
        report_dir = os.path.join(os.getcwd(), 'reports')
        os.makedirs(report_dir, exist_ok=True)
        
        # Create the Excel report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(report_dir, f'test_report_{timestamp}.xlsx')
        
        # Convert results to DataFrame
        df = pd.DataFrame(self.results)
        
        # Ensure all columns exist with default values
        required_columns = [
            'test_name', 'status', 'start_time', 'end_time', 'duration', 
            'error_message', 'traceback', 'screenshots', 'steps_to_reproduce'
        ]
        
        for col in required_columns:
            if col not in df.columns:
                df[col] = ''
                
        # Reorder and rename columns for better readability
        columns = {
            'test_name': 'Test Name',
            'status': 'Status',
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'duration': 'Duration (s)',
            'error_message': 'Error Message',
            'traceback': 'Stack Trace',
            'screenshots': 'Screenshots',
            'steps_to_reproduce': 'Steps to Reproduce'
        }
        
        df = df.rename(columns=columns)
        
        # Convert all columns to string type to avoid Excel formatting issues
        for col in df.columns:
            df[col] = df[col].astype(str)
            
        # Create Excel writer object
        with pd.ExcelWriter(report_path, engine='xlsxwriter') as writer:
            # Write the main results sheet
            df.to_excel(writer, sheet_name='Test Results', index=False)
            
            # Get workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Test Results']
            
            # Define formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#D8E4BC',
                'border': 1,
                'text_wrap': True,
                'valign': 'vcenter'
            })
            
            pass_format = workbook.add_format({
                'bg_color': '#C6EFCE',
                'font_color': '#006100',
                'text_wrap': True
            })
            
            fail_format = workbook.add_format({
                'bg_color': '#FFC7CE',
                'font_color': '#9C0006',
                'text_wrap': True
            })
            
            wrap_format = workbook.add_format({
                'text_wrap': True,
                'valign': 'top'
            })
            
            # Apply formats
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
            # Set column widths
            worksheet.set_column('A:A', 50)  # Test Name
            worksheet.set_column('B:B', 15)  # Status
            worksheet.set_column('C:D', 20)  # Start/End Time
            worksheet.set_column('E:E', 15)  # Duration
            worksheet.set_column('F:F', 50)  # Error Message
            worksheet.set_column('G:G', 50)  # Stack Trace
            worksheet.set_column('H:H', 50)  # Screenshots
            worksheet.set_column('I:I', 40)  # Steps to Reproduce
            
            # Apply text wrapping to all data cells
            for col in range(len(df.columns)):
                worksheet.set_column(col, col, None, wrap_format)
            
            # Apply conditional formatting for status column
            worksheet.conditional_format('B2:B1048576', {
                'type': 'cell',
                'criteria': 'equal to',
                'value': '"passed"',
                'format': pass_format
            })
            
            worksheet.conditional_format('B2:B1048576', {
                'type': 'cell',
                'criteria': 'equal to',
                'value': '"failed"',
                'format': fail_format
            })
            
        print(f"\nTest report generated: {report_path}")
        
    def add_screenshot(self, nodeid: str, screenshot_path: str):
        """Add a screenshot path to the current test"""
        self.current_test['screenshots'].append(screenshot_path)
