from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.getAll import getAllSecret, getAllSecretFromNameSpace
from ..utility.authenticated import checkToken


class kubernetesAllSecretView(APIView):
    def get(self, request):
        checkToken(request=request)
        output = getAllSecret()
        return Response(output)


class kubernetesAllSecretViewFromNamespace(APIView):
    def get(self, request, namespace):
        checkToken(request=request)
        output = getAllSecretFromNameSpace(namespace=namespace)
        return Response(output)
