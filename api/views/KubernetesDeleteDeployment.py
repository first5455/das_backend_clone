from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.delete import deleteDeployment
from ..utility.authenticated import checkToken


class kubernetesDeleteDeployment(APIView):

    def delete(self, request, name, namespace):
        checkToken(request=request)
        output = deleteDeployment(name=name, namespace=namespace)
        return Response(output)
