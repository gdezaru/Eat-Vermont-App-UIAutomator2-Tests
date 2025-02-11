"""Test metrics collection and analysis"""
import time
import psutil
from datetime import datetime
from collections import defaultdict

class TestMetrics:
    """Test metrics collection and analysis"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.metrics = {
            'test_execution': {
                'total_tests': 0,
                'passed_tests': 0,
                'failed_tests': 0,
                'skipped_tests': 0,
                'total_duration': 0,
                'average_duration': 0,
                'slowest_tests': [],  # (test_name, duration)
                'most_failed_tests': defaultdict(int),  # test_name: fail_count
            },
            'error_analysis': {
                'error_types': defaultdict(int),  # error_type: count
                'error_messages': defaultdict(int),  # error_msg: count
                'flaky_tests': [],  # tests that passed after retries
            },
            'coverage': {
                'modules_covered': set(),
                'total_test_cases': 0,
                'smoke_tests': 0,
                'regression_tests': 0,
            },
            'device_stats': {
                'device_id': '',
                'android_version': '',
                'screen_resolution': '',
                'memory_usage': [],  # [(timestamp, usage)]
                'cpu_usage': [],  # [(timestamp, usage)]
            },
            'test_stability': {
                'retry_count': 0,
                'flaky_rate': 0,
                'stable_tests': 0,
            },
            'time_analysis': {
                'start_time': self.start_time,
                'end_time': None,
                'peak_hours': defaultdict(int),  # hour: failure_count
                'test_distribution': defaultdict(int),  # module: test_count
            }
        }
    
    def record_test_result(self, test_name, outcome, duration, error=None, retry_count=0):
        """Record individual test result"""
        self.metrics['test_execution']['total_tests'] += 1
        self.metrics['test_execution']['total_duration'] += duration
        
        if outcome == 'passed':
            self.metrics['test_execution']['passed_tests'] += 1
            if retry_count > 0:
                self.metrics['error_analysis']['flaky_tests'].append(test_name)
        elif outcome == 'failed':
            self.metrics['test_execution']['failed_tests'] += 1
            self.metrics['test_execution']['most_failed_tests'][test_name] += 1
            if error:
                error_type = error.__class__.__name__
                self.metrics['error_analysis']['error_types'][error_type] += 1
                self.metrics['error_analysis']['error_messages'][str(error)] += 1
        else:  # skipped
            self.metrics['test_execution']['skipped_tests'] += 1
        
        # Record for time analysis
        hour = datetime.now().hour
        if outcome == 'failed':
            self.metrics['time_analysis']['peak_hours'][hour] += 1
        
        # Update slowest tests
        self.metrics['test_execution']['slowest_tests'].append((test_name, duration))
        self.metrics['test_execution']['slowest_tests'].sort(key=lambda x: x[1], reverse=True)
        self.metrics['test_execution']['slowest_tests'] = self.metrics['test_execution']['slowest_tests'][:5]
    
    def update_device_stats(self, device_id=None, android_version=None, screen_resolution=None):
        """Update device statistics"""
        if device_id:
            self.metrics['device_stats']['device_id'] = device_id
        if android_version:
            self.metrics['device_stats']['android_version'] = android_version
        if screen_resolution:
            self.metrics['device_stats']['screen_resolution'] = screen_resolution
        
        # Record current resource usage
        timestamp = datetime.now()
        self.metrics['device_stats']['memory_usage'].append(
            (timestamp, psutil.virtual_memory().percent)
        )
        self.metrics['device_stats']['cpu_usage'].append(
            (timestamp, psutil.cpu_percent())
        )
    
    def finalize_metrics(self):
        """Calculate final metrics"""
        self.metrics['time_analysis']['end_time'] = datetime.now()
        total_duration = self.metrics['test_execution']['total_duration']
        total_tests = self.metrics['test_execution']['total_tests']
        
        if total_tests > 0:
            self.metrics['test_execution']['average_duration'] = total_duration / total_tests
            self.metrics['test_stability']['flaky_rate'] = (
                len(self.metrics['error_analysis']['flaky_tests']) / total_tests * 100
            )
            self.metrics['test_stability']['stable_tests'] = (
                self.metrics['test_execution']['passed_tests'] -
                len(self.metrics['error_analysis']['flaky_tests'])
            )
        
        return self.metrics
