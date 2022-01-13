from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.delete import deleteService
from ..utility.authenticated import checkToken

class kubernetesDeleteService(APIView):

    def delete(self, request, name, namespace):
        checkToken(request=request)
        output = deleteService(name=name, namespace=namespace)
        return Response(output)