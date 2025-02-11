"""Main test runner script"""
import os
import sys
import pytest
import logging
import argparse
from datetime import datetime
from pathlib import Path

# Add test_runner to Python path
sys.path.append(str(Path(__file__).parent))

from config.device_config import DeviceConfig
from config.env_config import EnvironmentConfig
from config.test_suites import TestSuites
from utils.metrics import TestMetrics
from utils.report_generator import ReportGenerator

class TestRunner:
    """Main test runner class"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.results_dir = Path('reports') / self.timestamp
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.metrics = TestMetrics()
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_file = self.results_dir / 'test_run.log'
        logging.basicConfig(
            filename=str(log_file),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        # Also log to console
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logging.getLogger('').addHandler(console)
    
    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(description='Test Runner')
        parser.add_argument('--suite', choices=list(TestSuites.SUITES.keys()), default='regression',
                          help='Test suite to run')
        parser.add_argument('--modules', help='Comma-separated list of module numbers')
        parser.add_argument('--parallel', type=int, help='Number of parallel processes')
        parser.add_argument('--device', help='Device serial number')
        parser.add_argument('--device-type', choices=['default', 'emulator', 'real_device'],
                          default='default', help='Device type configuration')
        parser.add_argument('--env', choices=list(EnvironmentConfig.ENVIRONMENTS.keys()),
                          default='dev', help='Test environment')
        parser.add_argument('--reruns', type=int, help='Number of times to retry failed tests')
        return parser.parse_args()
    
    def get_test_modules(self, args):
        """Get list of test modules to run"""
        if args.modules:
            return [f"{num}_*.py" for num in args.modules.split(',')]
        return TestSuites.get_module_list(args.suite)
    
    def run(self):
        """Run the test suite"""
        args = self.parse_arguments()
        self.setup_logging()
        
        logging.info(f"Starting test execution - {self.timestamp}")
        
        # Validate environment
        if not EnvironmentConfig.validate_env(args.env):
            logging.error(f"Invalid environment: {args.env}")
            return 1
        
        # Validate device if specified
        if args.device and not DeviceConfig.validate_device(args.device):
            logging.error(f"Device not found: {args.device}")
            return 1
        
        # Get device configuration
        device_config = DeviceConfig.get_config(args.device_type, args.device)
        
        # Update metrics with device info
        self.metrics.update_device_stats(
            device_id=device_config['deviceName'],
            android_version='Unknown',  # This should be fetched from actual device
            screen_resolution='Unknown'  # This should be fetched from actual device
        )
        
        # Setup pytest arguments
        pytest_args = [
            '-v',
            f'--html={self.results_dir}/report.html',
            '--capture=tee-sys'
        ]
        
        # Add parallel execution if specified
        if args.parallel:
            pytest_args.extend(['-n', str(args.parallel)])
        
        # Add rerun if specified
        if args.reruns:
            pytest_args.extend(['--reruns', str(args.reruns)])
        
        # Add test modules
        pytest_args.extend(self.get_test_modules(args))
        
        try:
            # Run tests
            logging.info("Running tests with arguments: %s", ' '.join(pytest_args))
            exit_code = pytest.main(pytest_args)
            
            # Generate reports
            logging.info("Generating reports...")
            self.metrics.finalize_metrics()
            report_gen = ReportGenerator(self.metrics.metrics, self.results_dir)
            excel_report = report_gen.generate_excel_report()
            logging.info(f"Excel report generated: {excel_report}")
            
            logging.info(f"Test execution completed with exit code: {exit_code}")
            return exit_code
            
        except Exception as e:
            logging.error(f"Test execution failed: {str(e)}", exc_info=True)
            return 1

if __name__ == "__main__":
    runner = TestRunner()
    exit_code = runner.run()
    sys.exit(exit_code)
