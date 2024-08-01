from .models import ClientStatus

class ClientStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        client_status = ClientStatus.objects.filter().first()
        request.client_status = client_status
        response = self.get_response(request)
        return response