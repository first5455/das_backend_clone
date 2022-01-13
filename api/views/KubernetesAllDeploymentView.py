from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.getAll import getAllDeployment, getAllDeploymentFromNameSpace
from ..utility.authenticated import checkToken


class kubernetesAllDeployment(APIView):

    def get(self, request):
        checkToken(request=request)
        output = getAllDeployment().data
        return Response(output)


class kubernetesAllDeploymentFromNameSpace(APIView):

    def get(self, request, namespace):
        checkToken(request=request)
        output = getAllDeploymentFromNameSpace(namespace=namespace).data
        return Response(output)
