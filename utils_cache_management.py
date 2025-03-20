import os
import time
import shutil


def clear_python_cache():
    """
    Remove Python bytecode cache folders (__pycache__).
    These are safe to delete as they will be regenerated when needed.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "__pycache__" in dirnames:
            pycache_path = os.path.join(dirpath, "__pycache__")
            shutil.rmtree(pycache_path)


def clear_screenshot_cache(days_old=7):
    """
    Remove screenshots older than specified days.

    Args:
        days_old: Number of days, screenshots older than this will be removed
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    screenshot_dir = os.path.join(root_dir, "screenshots")

    if not os.path.exists(screenshot_dir):
        return

    cutoff_time = time.time() - (days_old * 86400)

    removed_count = 0
    for filename in os.listdir(screenshot_dir):
        file_path = os.path.join(screenshot_dir, filename)
        if os.path.isfile(file_path) and os.path.getmtime(file_path) < cutoff_time:
            os.remove(file_path)
            removed_count += 1



def clear_old_reports(days_old=30):
    """
    Remove test reports older than specified days.

    Args:
        days_old: Number of days, reports older than this will be removed
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(root_dir, "reports")

    if not os.path.exists(reports_dir):
        return

    cutoff_time = time.time() - (days_old * 86400)

    removed_files = 0
    removed_dirs = 0

    for item in os.listdir(reports_dir):
        item_path = os.path.join(reports_dir, item)

        # Skip if it's a recent file
        if os.path.getmtime(item_path) >= cutoff_time:
            continue

        if os.path.isfile(item_path):
            os.remove(item_path)
            removed_files += 1
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            removed_dirs += 1