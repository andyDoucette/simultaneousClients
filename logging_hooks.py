from app import app
from flask import request

@app.before_request
def log_request_info():
    message=f'''
↓↓↓↓↓↓↓↓↓↓↓↓↓
↓↓ {request.method} request from {request.remote_addr} for {request.url}

Request Headers: 
{request.headers}Request Body: 
{request.get_data()}

======'''

    app.logger.debug(message)

@app.after_request
def log_response_info(response):
    message=f'''
======
Response Summary:
{str(response)}

Response Headers:
{str(response.headers)}'''
    #Only log details for responses that aren't pass-through (static files are pass-through, for example):
    try:
        if not response.direct_passthrough:
            message +=f'Response Body: \n{response.get_data().decode("utf-8")}'
    except: pass
    
    message+='\n↑↑\n↑↑↑↑↑↑↑↑↑↑↑↑↑↑'
    
    app.logger.debug(message)

    return response
