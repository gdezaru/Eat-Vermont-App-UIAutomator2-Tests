"""Test report generation utilities"""
import os
import pandas as pd
from datetime import datetime
from pathlib import Path

class ReportGenerator:
    """Generate test execution reports"""
    
    def __init__(self, metrics, output_dir):
        self.metrics = metrics
        self.output_dir = Path(output_dir)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def generate_excel_report(self):
        """Generate Excel report with multiple sheets"""
        excel_path = self.output_dir / f'test_report_{self.timestamp}.xlsx'
        
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            self._create_summary_sheet(writer)
            self._create_test_details_sheet(writer)
            self._create_error_analysis_sheet(writer)
            self._create_device_stats_sheet(writer)
            self._create_time_analysis_sheet(writer)
        
        return excel_path
    
    def _create_summary_sheet(self, writer):
        """Create summary sheet with overall metrics"""
        summary_data = {
            'Metric': [
                'Total Tests',
                'Passed Tests',
                'Failed Tests',
                'Skipped Tests',
                'Total Duration (s)',
                'Average Duration (s)',
                'Flaky Tests',
                'Stable Tests',
                'Flaky Rate (%)',
                'Start Time',
                'End Time'
            ],
            'Value': [
                self.metrics['test_execution']['total_tests'],
                self.metrics['test_execution']['passed_tests'],
                self.metrics['test_execution']['failed_tests'],
                self.metrics['test_execution']['skipped_tests'],
                round(self.metrics['test_execution']['total_duration'], 2),
                round(self.metrics['test_execution']['average_duration'], 2),
                len(self.metrics['error_analysis']['flaky_tests']),
                self.metrics['test_stability']['stable_tests'],
                round(self.metrics['test_stability']['flaky_rate'], 2),
                self.metrics['time_analysis']['start_time'].strftime('%Y-%m-%d %H:%M:%S'),
                self.metrics['time_analysis']['end_time'].strftime('%Y-%m-%d %H:%M:%S')
            ]
        }
        
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
        
        # Auto-adjust column width
        worksheet = writer.sheets['Summary']
        for column in worksheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
    
    def _create_test_details_sheet(self, writer):
        """Create detailed test results sheet"""
        test_details = []
        for test_name, duration in self.metrics['test_execution']['slowest_tests']:
            test_details.append({
                'Test Name': test_name,
                'Duration (s)': round(duration, 2),
                'Status': 'Failed' if test_name in self.metrics['test_execution']['most_failed_tests'] else 'Passed',
                'Retry Count': self.metrics['test_stability']['retry_count'] if test_name in self.metrics['error_analysis']['flaky_tests'] else 0
            })
        
        df_details = pd.DataFrame(test_details)
        df_details.to_excel(writer, sheet_name='Test Details', index=False)
    
    def _create_error_analysis_sheet(self, writer):
        """Create error analysis sheet"""
        error_data = {
            'Error Type': list(self.metrics['error_analysis']['error_types'].keys()),
            'Count': list(self.metrics['error_analysis']['error_types'].values()),
            'Error Message': list(self.metrics['error_analysis']['error_messages'].keys())
        }
        
        df_errors = pd.DataFrame(error_data)
        df_errors.to_excel(writer, sheet_name='Error Analysis', index=False)
    
    def _create_device_stats_sheet(self, writer):
        """Create device statistics sheet"""
        device_data = {
            'Metric': [
                'Device ID',
                'Android Version',
                'Screen Resolution',
                'Average Memory Usage (%)',
                'Average CPU Usage (%)'
            ],
            'Value': [
                self.metrics['device_stats']['device_id'],
                self.metrics['device_stats']['android_version'],
                self.metrics['device_stats']['screen_resolution'],
                round(sum(m[1] for m in self.metrics['device_stats']['memory_usage']) / 
                      len(self.metrics['device_stats']['memory_usage']), 2),
                round(sum(c[1] for c in self.metrics['device_stats']['cpu_usage']) / 
                      len(self.metrics['device_stats']['cpu_usage']), 2)
            ]
        }
        
        df_device = pd.DataFrame(device_data)
        df_device.to_excel(writer, sheet_name='Device Stats', index=False)
    
    def _create_time_analysis_sheet(self, writer):
        """Create time analysis sheet"""
        time_data = {
            'Hour': list(self.metrics['time_analysis']['peak_hours'].keys()),
            'Failures': list(self.metrics['time_analysis']['peak_hours'].values()),
            'Tests per Module': list(self.metrics['time_analysis']['test_distribution'].items())
        }
        
        df_time = pd.DataFrame(time_data)
        df_time.to_excel(writer, sheet_name='Time Analysis', index=False)
