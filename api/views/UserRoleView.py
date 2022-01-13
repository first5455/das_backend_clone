from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ..models import User
from ..serializers.UserSerializer import UserSerializer, RoleSerilizer
from ..utility.authenticated import checkToken


class UserRoleView(GenericAPIView):
    serializer_class = RoleSerilizer

    def put(self, request, id=None):
        loginUser = checkToken(request)
        if loginUser.role == "admin":
            try:
                userData = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response({
                    'detail': 'This User does not exist'
                }, status=400)
            updateSerilizer = RoleSerilizer(userData, data=request.data)
            if updateSerilizer.is_valid(raise_exception=True):
                updateObject = updateSerilizer.save()
                responseSerilizer = UserSerializer(updateObject)
                return Response(responseSerilizer.data, status=200)
            else:
                return Response("Error")
        else:
            raise NotAuthenticated("Access Denied")
