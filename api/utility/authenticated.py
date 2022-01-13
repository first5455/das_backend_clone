import jwt
from rest_framework.exceptions import AuthenticationFailed

from api.models.User import User


def checkToken(request):
    token = request.COOKIES.get('Authorization')

    if not token:
        try:
            token = request.headers['Authorization']
        except:
            raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token Expired')
    user = User.objects.get(id=payload['id'])

    return user
