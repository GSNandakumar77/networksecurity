import sys
import logging
from networksecurity.logging import logger

'''
✅ Final-Tip

Always call super().__init__() when inheriting from built-in classes like Exception, BaseModel, etc., even if you're storing extra/custom fields. It's a best practice in Python.

'''
class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        super().__init__(error_message)
        self.error_message =error_message
        _,_,self.exc_tb=error_details.exc_info()

        self.lineno=self.exc_tb.tb_lineno
        self.filename=self.exc_tb.tb_frame.f_code.co_filename


    def __str__(self):
        return f"Error occurred in script [{0}] at line number [{1}] with message [{2}]".format(self.filename,self.exc_tb.tb_lineno,str(self.error_message))
    


# Entry point
if __name__=="__main__":
    try:
        logger.logging.info("enter the try block")
        a = 1 / 0  # This will raise a ZeroDivisionError
    except Exception as e:
        raise NetworkSecurityException(e, sys)    