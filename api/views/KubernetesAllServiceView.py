from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.getAll import getAllServices, getAllServicesFromNameSpace
from ..utility.authenticated import checkToken


class kubernetesAllServiceView(APIView):
    def get(self, request):
        checkToken(request=request)
        output = getAllServices().data
        return Response(output)


class kubernetesAllServiceViewFromNamespace(APIView):
    def get(self, request, namespace):
        checkToken(request=request)
        output = getAllServicesFromNameSpace(namespace=namespace).data
        return Response(output)
