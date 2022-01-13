from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.get import getPodsUsage, getPodUsageFromNamespace, getPodUsageFromAppName
from ..utility.authenticated import checkToken


class kubernetesGetPodUsage(APIView):

    def get(self, request):
        checkToken(request=request)
        output = getPodsUsage()
        return Response(output)


class kubernetesGetPodUsageFromNamespace(APIView):

    def get(self, request, namespace):
        checkToken(request=request)
        output = getPodUsageFromNamespace(namespace=namespace)
        return Response(output)


class kubernetesGetPodUsageFromAppName(APIView):

    def get(self, request, name, namespace):
        checkToken(request=request)
        output = getPodUsageFromAppName(name=name, namespace=namespace)
        return Response(output)
