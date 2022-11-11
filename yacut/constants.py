import string

VALID_SYMBOLS_SET = string.ascii_letters + string.digits
DEFAULT_LINK_LENGTH = 6
CUSTOM_LINK_LENGTH = 16
MAX_ORIGINAL_LINK_LENGTH = 2000
GENERATED_RANDOM_STRING_TRY_COUNT = 1000

_PREPARED_SYMBOLS = "".join(
    symbol if symbol.isalpha() or symbol.isdigit() else "\\" + symbol
    for symbol in VALID_SYMBOLS_SET
)
REGEXP_ID = fr'^[{_PREPARED_SYMBOLS}]+$'
# Хотел в одну строку, но это не сократить:
# REGEXP_ID = fr'^[{"".join(smb if smb.isalpha() or smb.isdigit() else chr(92) + smb for smb in VALID_SYMBOLS_SET)}]+$'
