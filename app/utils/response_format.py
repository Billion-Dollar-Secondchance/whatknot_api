def success_response(message: str = "", data=None):
    return {
        "status": "success",
        "message": message,
        "data": data
    }

def failure_response(message: str = "", data=None):
    return {
        "status": "failure",
        "message": message,
        "data": data
    }
