from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.getAll import getAllHorizontalAutoScalerPodAll, getAllHorizontalAutoScalerPodAllFromNamespace
from ..utility.authenticated import checkToken


class kubernetesAllHorizontal(APIView):

    def get(self, request):
        checkToken(request)
        output = getAllHorizontalAutoScalerPodAll().data
        return Response(output)

class kubernetesAllHorizontalFromNamespace(APIView):

    def get(self, request, namespace):
        checkToken(request)
        output = getAllHorizontalAutoScalerPodAllFromNamespace(namespace=namespace).data
        return Response(output)
