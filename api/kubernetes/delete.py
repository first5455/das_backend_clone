from os import environ

from dotenv import load_dotenv
from kubernetes.client import AppsV1Api, configuration, ApiClient, CoreV1Api, ApiException, AutoscalingV1Api
from rest_framework.exceptions import NotFound

from ..models.App import Port
from ..models.Kubernetes import KubernetesDeployment, KubernetesService, KubernetesHorizontal
from ..serializers.KubernetesSerializer import KubernetesDeploymentSerializer, KubernetesServiceSerializer, \
    KubernetesHorizontalAutoscalerSerializer
from ..utility.deleteImageRepository import deleteImageRepository

load_dotenv()
configuration = configuration.Configuration()
configuration.host = environ['KUBERNETES_HOST']
configuration.api_key["authorization"] = environ['KUBERNETES_KEY']
api_client = ApiClient(configuration=configuration)
appV1Api = AppsV1Api(api_client=api_client)
v1Api = CoreV1Api(api_client=api_client)
autoscaleApiv1 = AutoscalingV1Api(api_client=api_client)


def deleteDeployment(name, namespace):
    try:
        response = appV1Api.delete_namespaced_deployment(
            name=name,
            namespace=namespace
        )
        deleteImageRepository(str(namespace + "-" + name).replace("-deployment", ""))
    except ApiException as err:
        if err.status == 404:
            raise NotFound("No Deployment found")
        else:
            raise err
    deploymentObject = KubernetesDeployment(
        name=response.details.name,
        namespace=namespace,
    )
    deploymentSerializer = KubernetesDeploymentSerializer(deploymentObject)
    return deploymentSerializer.data


def deleteService(name, namespace):
    try:
        response = v1Api.delete_namespaced_service(
            name=name,
            namespace=namespace
        )
    except ApiException as err:
        if err.status == 404:
            raise NotFound("No Services Found")
        else:
            raise err
    portDB = Port.objects.filter(
        appName=name,
        namespace=namespace
    ).first()
    port = portDB.port
    portDB.delete()
    serviceObj = KubernetesService(
        servicename=response.details.name,
        namespace=namespace,
        port=port,
    )
    serviceSerializer = KubernetesServiceSerializer(serviceObj)
    return serviceSerializer.data


def deleteHorizontalScale(name, namespace):
    try:
        response = autoscaleApiv1.delete_namespaced_horizontal_pod_autoscaler(
            name=name,
            namespace=namespace
        )
        horizontalObj = KubernetesHorizontal(
            name=response.details.name,
            namespace=namespace,
            deploymentTarget=name + "-deployment",
            targetcpu="",
            currentcpu="",
            minpod="",
            maxpod="",
            currentpod=""
        )
        horizontalSerializer = KubernetesHorizontalAutoscalerSerializer(horizontalObj)
        return horizontalSerializer.data
    except ApiException as err:
        if err.status == 404:
            raise NotFound("No HorizontalAutoScalerPodFound")
        else:
            raise err


def deleteNamespace(namespace):
    try:
        v1Api.delete_namespace(
            name=namespace
        )
        dbPort = Port.objects.filter(namespace=namespace).all()
        for i in dbPort:
            deleteImageRepository(str(i.namespace + "-" + i.appName).replace("-service", ""))
            i.delete()
        return {
            "detail": "Deleted " + namespace
        }
    except ApiException as err:
        if err.status == 404:
            raise NotFound("No Namespace Found")
        raise err
