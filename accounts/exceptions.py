from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # your custom logic
    response = exception_handler(exc, context)
    # modify response if needed
    return response