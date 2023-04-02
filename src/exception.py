import sys 
sys.path.append('.') # to let python know src module is in this directory 
from src.logger import logging



def error_msg_detail(error,error_detail:sys): # error details
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error in python script name [{0}], line number [{1}], filename [{2}]".format(file_name,exc_tb.tb_lineno,str(error))
    return error_message

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message) #inheriting from exception
        self.error_message = error_msg_detail(error_message,error_detail)

    def __str__(self): # return error message 
        return self.error_message
    

# if __name__ == "__main__":
#     try:
#         check = 1/0
#     except Exception as e:
#         logging.info("Divide by zero")
#         raise CustomException(e,sys)