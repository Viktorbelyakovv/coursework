def token_expired(get_response):

    def process_exception(request):
        response = get_response(request)
        if response.status_code == 401:
            print("Token expired exception")
        return response
    return process_exception
