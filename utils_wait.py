import time


class WaitUtils:
    def __init__(self, device, default_timeout=10):
        self.device = device
        self.default_timeout = default_timeout

    def wait_for_element(self, selector, timeout=None):
        """Wait for element to be present and visible"""
        timeout = timeout or self.default_timeout
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.device(selector).exists:
                return True
            time.sleep(0.5)
        return False

    def wait_for_element_to_disappear(self, selector, timeout=None):
        """Wait for element to disappear"""
        timeout = timeout or self.default_timeout
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self.device(selector).exists:
                return True
            time.sleep(0.5)
        return False

    def wait_for_condition(self, condition_func, timeout=None, message=None):
        """Wait for custom condition function to return True"""
        timeout = timeout or self.default_timeout
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(0.5)
        if message:
            print(f"Timeout waiting for condition: {message}")
        return False
