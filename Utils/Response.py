def success_response(message, data=None, status_code=200):
    return{
        "succes":True,
        "message":message,
        "data":data,
        "error":None
    }, status_code
    
def error_response(message, status_code=400, error_code=None):
    return{
        "succes":False,
        "message":message,
        "data":None,
        "error":error_code or "API Error"
    }, status_code