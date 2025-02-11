"""Device configuration for test execution"""

class DeviceConfig:
    """Device configuration settings"""
    
    CONFIGURATIONS = {
        'default': {
            'platformName': 'Android',
            'automationName': 'UiAutomator2',
            'deviceName': None,  # Will be set from command line
            'appPackage': 'com.eatvermont',
            'noReset': False,
            'fullReset': False,
            'autoGrantPermissions': True,
            'newCommandTimeout': 300,
            'systemPort': 8200,
        },
        'emulator': {
            'platformName': 'Android',
            'automationName': 'UiAutomator2',
            'deviceName': 'emulator-5554',
            'appPackage': 'com.eatvermont',
            'avd': 'Pixel_4_API_30',
            'noReset': False,
            'systemPort': 8201,
        },
        'real_device': {
            'platformName': 'Android',
            'automationName': 'UiAutomator2',
            'deviceName': None,
            'appPackage': 'com.eatvermont',
            'noReset': True,
            'systemPort': 8202,
        }
    }
    
    @classmethod
    def get_config(cls, device_type='default', device_id=None):
        """Get device configuration"""
        config = cls.CONFIGURATIONS.get(device_type, cls.CONFIGURATIONS['default']).copy()
        if device_id:
            config['deviceName'] = device_id
        return config
    
    @classmethod
    def validate_device(cls, device_id):
        """Validate device connection"""
        import subprocess
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            return device_id in result.stdout
        except Exception:
            return False
