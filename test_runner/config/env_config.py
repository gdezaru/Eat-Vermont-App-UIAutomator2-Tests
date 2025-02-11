"""Environment configuration for test execution"""

class EnvironmentConfig:
    """Environment configuration settings"""
    
    ENVIRONMENTS = {
        'dev': {
            'app_url': 'https://dev.eatvermont.com',
            'api_url': 'https://api.dev.eatvermont.com',
            'timeout': 10,
            'retry_attempts': 3,
            'log_level': 'DEBUG',
            'screenshot_on_failure': True,
            'clear_app_data': True,
            'implicit_wait': 10,
            'explicit_wait': 20,
        },
        'staging': {
            'app_url': 'https://staging.eatvermont.com',
            'api_url': 'https://api.staging.eatvermont.com',
            'timeout': 15,
            'retry_attempts': 2,
            'log_level': 'INFO',
            'screenshot_on_failure': True,
            'clear_app_data': True,
            'implicit_wait': 15,
            'explicit_wait': 25,
        },
        'prod': {
            'app_url': 'https://eatvermont.com',
            'api_url': 'https://api.eatvermont.com',
            'timeout': 20,
            'retry_attempts': 1,
            'log_level': 'WARNING',
            'screenshot_on_failure': True,
            'clear_app_data': False,
            'implicit_wait': 20,
            'explicit_wait': 30,
        }
    }
    
    @classmethod
    def get_config(cls, env='dev'):
        """Get environment configuration"""
        return cls.ENVIRONMENTS.get(env, cls.ENVIRONMENTS['dev']).copy()
    
    @classmethod
    def validate_env(cls, env):
        """Validate environment"""
        return env in cls.ENVIRONMENTS
