"""
    Returns any synapse error with `Error.error(<error_code>, <extra_info>)`
"""


class Error:
    error_codes = {
        "SYN_001": "Invalid file format error: ",
        "SYN_002": "File not found error: ",
        "SYN_003": "Syntax error: ",
        "SYN_004": "Unknow type error: ",
        "SYN_005": "Type mismatch error: ",
        "SYN_006": "Unknow method error: ",
        "SYN_007": "Undeclared variable error: ",
    }

    @staticmethod
    def error(error_code, extra_info=""):
        if error_code in Error.error_codes:
            message = f"{error_code} - {Error.error_codes[error_code]}{extra_info}"
            print(f"\033[1;31m Error: {message}\033[0m")
            return message
        else:
            unknown_error = f"UNKNOWN_ERROR - Unknown error code: {error_code}"
            print(f"\033[1;33m{unknown_error}\033[0m")
            return unknown_error

    @staticmethod
    def list_errors():
        """List all available error codes"""
        print("Available error codes:")
        for code, description in Error.error_codes.items():
            print(f"  {code}: {description}")
