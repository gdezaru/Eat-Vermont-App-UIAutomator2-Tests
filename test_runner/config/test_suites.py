"""Test suite configuration"""

class TestSuites:
    """Test suite definitions"""
    
    SUITES = {
        'smoke': {
            'description': 'Critical path tests',
            'modules': ['1_tests_sign_in_user_password', '3_tests_home_screen'],
            'priority': 'high',
            'max_retries': 2,
            'parallel': True,
        },
        'regression': {
            'description': 'Full test suite',
            'modules': [
                '1_tests_sign_in_user_password',
                '2_tests_search_module',
                '3_tests_home_screen',
                '5_settings',
                '6_events',
                '7_businesses',
                '8_day_trips',
                '9_trails',
                '10_videos',
                '11_favorites',
                '12_visit_history',
                '13_view_map',
                '14_guest_mode'
            ],
            'priority': 'medium',
            'max_retries': 1,
            'parallel': True,
        },
        'guest': {
            'description': 'Guest mode features',
            'modules': ['14_guest_mode'],
            'priority': 'medium',
            'max_retries': 2,
            'parallel': False,
        },
        'core': {
            'description': 'Core functionality',
            'modules': [
                '1_tests_sign_in_user_password',
                '2_tests_search_module',
                '3_tests_home_screen'
            ],
            'priority': 'high',
            'max_retries': 2,
            'parallel': True,
        },
        'features': {
            'description': 'Feature-specific tests',
            'modules': [
                '6_events',
                '7_businesses',
                '8_day_trips',
                '9_trails',
                '10_videos'
            ],
            'priority': 'medium',
            'max_retries': 1,
            'parallel': True,
        }
    }
    
    @classmethod
    def get_suite(cls, suite_name):
        """Get suite configuration"""
        return cls.SUITES.get(suite_name, cls.SUITES['regression']).copy()
    
    @classmethod
    def get_module_list(cls, suite_name):
        """Get list of modules for a suite"""
        suite = cls.get_suite(suite_name)
        return [f"{module}.py" for module in suite['modules']]
    
    @classmethod
    def validate_suite(cls, suite_name):
        """Validate suite exists"""
        return suite_name in cls.SUITES
