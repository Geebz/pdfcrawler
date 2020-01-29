from django.utils.deprecation import MiddlewareMixin, RemovedInDjango21Warning

from django.http import JsonResponse


class BrokenURLChecker(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code != 200:
            return JsonResponse({'status': False}, safe=False)

        return response