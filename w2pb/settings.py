import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SERVICE_LOG_PATH = os.path.join(BASE_DIR, 'log/')
GHOSTDRIVER_LOG_PATH = os.path.join(SERVICE_LOG_PATH, 'ghostdriver.log')

AJAX_TIMEOUT = 10

try:
    os.stat(SERVICE_LOG_PATH)
except OSError:
    os.makedirs(SERVICE_LOG_PATH)

PHANTOM_DATA = {
    'service_args': ['--load-images=no'],
    'service_log_path': GHOSTDRIVER_LOG_PATH
}
