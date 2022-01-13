from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.getAll import getAllPods, getAllPodsFromNameSpace
from ..utility.authenticated import checkToken


class kubernetesAllPodView(APIView):
    def get(self, request):
        checkToken(request=request)
        output = getAllPods().data
        return Response(output)


class kubernetesAllPodViewFromNamespace(APIView):
    def get(self, request, namespace):
        checkToken(request=request)
        output = getAllPodsFromNameSpace(namespace=namespace).data
        return Response(output)
