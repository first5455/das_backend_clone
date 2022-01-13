from rest_framework.response import Response
from rest_framework.views import APIView

from ..utility.authenticated import checkToken
from ..utility.rollback import rollbackImage


class kubernetesRollback(APIView):

    def patch(self, request, name, namespace):
        checkToken(request=request)
        output = rollbackImage(appName=name, namespace=namespace)
        return Response({
            "message": output
        })
