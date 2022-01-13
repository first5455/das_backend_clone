import datetime

import jwt
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.models.App import Port
from api.models.User import User
from api.serializers.UserSerializer import UserSerializer, LoginSerializer
from api.utility.authenticated import checkToken
from ..kubernetes.delete import deleteNamespace
from ..kubernetes.create import createNamespace


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        seriallizer = UserSerializer(data=request.data)
        seriallizer.is_valid(raise_exception=True)
        seriallizer.save()
        createNamespace(request.data["namespace"])
        return Response(seriallizer.data)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.get(email=email)

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='Authorization', value=token, httponly=False, samesite='None', secure=False)
        response.data = {
            'user': user.id,
            'token': token
        }
        return response


class UserView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, id):
        checkToken(request)
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({
                'detail': 'This User does not exist'
            }, status=400)
        userSerializer = UserSerializer(user)
        return Response(userSerializer.data)

    def put(self, request, id=None):
        checkToken(request)
        try:
            userData = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({
                'detail': 'This User does not exist'
            }, status=400)
        if userData.check_password(request.data['passwordOld']):
            updateSerializer = UserSerializer(userData, data=request.data)
            if updateSerializer.is_valid():
                updateObject = updateSerializer.save()
                responseSerializer = UserSerializer(updateObject)
                return Response(responseSerializer.data, status=200)
        return Response({"detail": "Wrong Old Password"}, status=400)

    def delete(self, request, id):
        loginUser = checkToken(request)
        if loginUser.role == "admin":
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response({
                    'detail': 'This User does not exist'
                }, status=400)
            try:
                deleteNamespace(user.namespace)
            except:
                pass
            ports = Port.objects.filter(namespace=user.namespace)
            ports.delete()
            user.delete()
            return Response({"message": "Deleted " + user.name})
        else:
            raise NotAuthenticated("Access Denied")


class UserAllView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        loginUser = checkToken(request)
        if loginUser.role == "admin":
            users = User.objects.all()
            userSerializer = UserSerializer(users, many=True)
            return Response(userSerializer.data)
        else:
            raise NotAuthenticated("Access Denied")


class LogoutView(GenericAPIView):
    def delete(self, request):
        response = Response()
        response.delete_cookie('Authorization')
        response.data = {
            'message': 'logout sucess'
        }
        return response
