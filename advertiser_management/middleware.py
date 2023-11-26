class IPAddress:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip = ip_address.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.user.ip = ip
        response = self.get_response(request)
        return response
