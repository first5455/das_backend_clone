from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.get import getNodeUsage
from ..utility.authenticated import checkToken


class kubernetesGetNodeUsage(APIView):

    def get(self, request):
        checkToken(request=request)
        output = getNodeUsage()
        return Response(output)
