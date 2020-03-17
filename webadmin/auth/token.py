import time
import jwt
from jwt import exceptions
from LinuxSecurity import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render

class checkTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            token = request.COOKIES['token']
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, True)
                request.user = payload['username']
            except :
                if not 'login' in request.path:
                    return render(request, 'login.html')
        except KeyError:
            if not 'login' in request.path:
                return render(request,'login.html')

def create_token(payload,timeout=60):
    header = {
        "typ":"JWT",
        "alg":"HS256"
    }
    payload['exp'] = int(time.time())+timeout
    token = jwt.encode(payload=payload,key=settings.SECRET_KEY,algorithm='HS256',headers=header)
    return token