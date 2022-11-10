import string


VALID_SYMBOLS_SET = string.ascii_letters + string.digits
DEFAULT_LINK_LENGTH = 6
CUSTOM_LINK_LENGTH = 16
MAX_ORIGINAL_LINK_LENGTH = 2000
GENERATED_RANDOM_STRING_TRY_COUNT = 1000

# REGEXP_ID = fr'^[{VALID_SYMBOLS_SET}]+$'
REGEXP_ID = r'^[a-zA-Z0-9]+$'
REGEXP_URL = (
    r'^[a-z]+://'
    r'(?P<host>[^\/\?:]+)'
    r'(?P<port>:[0-9]+)?'
    r'(?P<query>\?.*)?$'
)
