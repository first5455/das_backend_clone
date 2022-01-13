from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.getlogs import getPodLog
from ..utility.authenticated import checkToken


class kubernetesGetPogLog(APIView):

    def get(self, request, name, namespace):
        checkToken(request=request)
        output = getPodLog(name, namespace)
        return Response(output)
