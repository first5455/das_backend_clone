from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.delete import deleteNamespace
from ..utility.authenticated import checkToken


class kubernetesDeleteNamespace(APIView):

    def delete(self, request, namespace):
        checkToken(request=request)
        output = deleteNamespace(namespace=namespace)
        return Response(output, status=200)
