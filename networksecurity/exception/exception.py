import sys
import logging
from networksecurity.logging import logger

'''
✅ Final-Tip

Always call super().__init__() when inheriting from built-in classes like Exception, BaseModel, etc., even if you're storing extra/custom fields. It's a best practice in Python.

'''
class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    def get_detailed_error_message(self, error_message, error_detail):
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        return f"Error occurred in script [{file_name}] at line number [{line_number}] with message [{error_message}]"

    def __str__(self):
        return self.error_message


# Entry point
if __name__=="__main__":
    try:
        logger.logging.info("enter the try block")
        a = 1 / 0  # This will raise a ZeroDivisionError
    except Exception as e:
        raise NetworkSecurityException(e, sys)    