from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.getAll import getAllNode
from ..utility.authenticated import checkToken


class kubernetesAllNodesView(APIView):
    def get(self, request):
        checkToken(request=request)
        output = getAllNode().data
        return Response(output)
