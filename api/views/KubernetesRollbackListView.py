from rest_framework.response import Response
from rest_framework.views import APIView

from ..utility.authenticated import checkToken
from ..utility.rollback import rollbackList


class kubernetesRollbackList(APIView):

    def get(self, request, name, namespace):
        checkToken(request=request)
        output = rollbackList(appName=name, namespace=namespace)
        return Response(output)
