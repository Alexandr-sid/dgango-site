import time

from django.http import HttpRequest
from django.shortcuts import render


def set_useragent_on_request_middleware(get_response):
    print("initial call")

    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        request.ip_address = request.META["REMOTE_ADDR"]
        response = get_response(request)
        print("after get response")
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_time = {}
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        time_delay = 1
        if not self.request_time:
            print("This is the first request. The dictionary request time is empty.")
            self.request_time['time'] = 60 - time.localtime().tm_sec
            self.request_time['ip_address'] = request.META.get('REMOTE_ADDR')
        else:
            if abs((60 - time.localtime().tm_sec) - self.request_time['time']) < time_delay and \
                    self.request_time['ip_address'] == request.META.get('REMOTE_ADDR'):
                print(f"To much requests in {time_delay} seconds")
                return render(request, "requestdataapp/too-much-requests-error.html")

        self.request_time['time'] = 60 - time.localtime().tm_sec
        self.request_time['ip_address'] = request.META.get('REMOTE_ADDR')
        self.requests_count += 1
        print("Requests count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("Responses count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("Got", self.exceptions_count, "exceptions so far")
