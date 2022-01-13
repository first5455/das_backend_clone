from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ..kubernetes.update import updateReplicaSet
from ..serializers.AppSerializer import UpdateReplica
from ..utility.authenticated import checkToken


class kubernetesUpdateReplicaSet(GenericAPIView):
    serializer_class = UpdateReplica

    def post(self, request, name, namespace):
        checkToken(request=request)
        replicaSerializer = UpdateReplica(data=request.data, context={'request': request})
        replicaSerializer.is_valid()
        replicas = replicaSerializer.data.get("replicas")
        output = updateReplicaSet(name=name, namespace=namespace, replicas=int(replicas))
        return Response({
            "message": output
        })
