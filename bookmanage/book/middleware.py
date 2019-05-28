

def my(get_response):
    print('init被调用')
    def middleware(request):
        print('before request被调用')
        response = get_response(request)
        print('after response被调用')
        return response
    return middleware