from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ..kubernetes.create import createDeployment, createDeploymentObject, createService, createServiceObject, \
    createNamespace, createSecret, createHorizontalPodAutoScaleObj, createHorizontalPodAutoScale
from ..models.App import Port
from ..models.Kubernetes import KubernetesCreateOutput
from ..serializers.AppSerializer import PortSerializer, EnvSerializer
from ..serializers.KubernetesSerializer import KubernetesCreateOutputSerializer
from ..utility.authenticated import checkToken


class kubernetesCreateDeployment(GenericAPIView):
    serializer_class = EnvSerializer
    permission_classes = ()

    def post(self, request, name, namespace, portdocker, *args, **kwargs):
        portApp = None
        checkToken(request)
        createNamespace(namespace=namespace)
        envSerializerClass = self.get_serializer_class()
        envSerializer = envSerializerClass(data=request.data, context={'request': request}, many=True)
        envSerializer.is_valid(raise_exception=True)
        envData = envSerializer.data

        deploymentObj = createDeploymentObject(name=name, namespace=namespace, port=int(portdocker), envData=envData)
        try:
            portAppCheck = Port.objects.get(
                appName=name + "-service",
                namespace=namespace
            )
        except:
            portAppCheck = None
        if portAppCheck is not None:
            portApp = {
                "port": portAppCheck.port,
                "appName": portAppCheck.appName,
                "namespace": portAppCheck.namespace
            }
        else:
            for i in range(30000, 32767):
                portDb = Port.objects.filter(port=i).first()
                if portDb is None:
                    portApp = {
                        "port": i,
                        "appName": name + "-service",
                        "namespace": namespace
                    }
                    portAppSerializer = PortSerializer(data=portApp)
                    portAppSerializer.is_valid(raise_exception=True)
                    portAppSerializer.save()
                    break
            if portApp is None:
                raise Response({"detail": "No ports Available"})
        serviceObj = createServiceObject(name=name, appPort=portApp.get("port"), containerPort=int(portdocker))
        createSecret(namespace=namespace)
        service = createService(service=serviceObj, namespace=namespace)
        deployment = createDeployment(deployment=deploymentObj, namespace=namespace)
        horizonPodAutoscaleObj = createHorizontalPodAutoScaleObj(name=name, namespace=namespace)
        horizonPodAutoscale = createHorizontalPodAutoScale(name=name ,namespace=namespace, horizonPod=horizonPodAutoscaleObj)
        output = KubernetesCreateOutput(
            deploymentName=deployment.data.get('name'),
            serviceName=service.data.get('servicename'),
            nameSpace=namespace,
            name=name,
            port=service.data.get('port')
        )
        outputSerializer = KubernetesCreateOutputSerializer(output).data
        return Response(outputSerializer)
