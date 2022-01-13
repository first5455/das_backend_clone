from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.delete import deleteHorizontalScale
from ..utility.authenticated import checkToken


class kubernetesDeleteHorizontalAutoScaler(APIView):

    def delete(self, request, name, namespace):
        checkToken(request=request)
        output = deleteHorizontalScale(name=name, namespace=namespace)
        return Response(output)
