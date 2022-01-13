from rest_framework.response import Response
from rest_framework.views import APIView

from ..kubernetes.start import startDeployment
from ..utility.authenticated import checkToken


class kubernetesStartDeployment(APIView):

    def patch(self, request, name, namespace):
        checkToken(request=request)
        output = startDeployment(name=name, namespace=namespace)
        return Response({
            "message": output
        })
