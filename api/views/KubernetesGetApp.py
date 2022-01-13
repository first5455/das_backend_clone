from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.get import getAppsDetail
from ..utility.authenticated import checkToken


class kubernetesGetApp(APIView):

    def get(self, request, name, namespace):
        checkToken(request=request)
        output = getAppsDetail(appname=name, namespace=namespace)
        return Response(output)
