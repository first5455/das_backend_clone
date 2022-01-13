from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ..kubernetes.update import updateLimitAutoscale
from ..serializers.AppSerializer import UpdateLimitAutoscaler
from ..utility.authenticated import checkToken


class kubernetesUpdateLimitAutoScaler(GenericAPIView):
    serializer_class = UpdateLimitAutoscaler

    def post(self, request, name, namespace):
        checkToken(request=request)
        updateSerializer = UpdateLimitAutoscaler(data=request.data, context={'request': request})
        updateSerializer.is_valid(raise_exception=True)
        minLimit = updateSerializer.data.get("min")
        maxLimit = updateSerializer.data.get("max")
        cpuLimit = updateSerializer.data.get("cpu")
        output = updateLimitAutoscale(name=name, namespace=namespace, minLimt=minLimit, maxLimit=maxLimit, cpuLimit=cpuLimit)
        return Response({
            "message": output
        })