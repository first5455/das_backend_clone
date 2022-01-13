from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.stop import stopDeployment
from ..utility.authenticated import checkToken


class kubernetesStopDeployment(APIView):

    def patch(self, request, name, namespace):
        checkToken(request=request)
        output = stopDeployment(name=name, namespace=namespace)
        return Response({
            "message": output
        })
