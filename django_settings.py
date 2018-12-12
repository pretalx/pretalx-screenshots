from pretalx.common.settings.test_settings import *

LOCALE_PATHS = list(LOCALE_PATHS) + [os.path.join(os.path.dirname(__file__), 'locale')]
