from os import environ

from dotenv import load_dotenv
from kubernetes.client import AppsV1Api, configuration, ApiClient, CoreV1Api, AutoscalingV1Api, ApiException
from rest_framework.exceptions import NotFound

load_dotenv()
configuration = configuration.Configuration()
configuration.host = environ['KUBERNETES_HOST']
configuration.api_key["authorization"] = environ['KUBERNETES_KEY']
api_client = ApiClient(configuration=configuration)
appV1Api = AppsV1Api(api_client=api_client)
v1Api = CoreV1Api(api_client=api_client)
dockerConfigJson = environ['DOCKER_CONFIG_JSON']
imageRegistry = environ['IMAGE_REGISTRY']
kubernetesIp = environ['KUBERNETES_IP']
autoscaleV1 = AutoscalingV1Api(api_client=api_client)


def updateReplicaSet(name, namespace, replicas):
    try:
        readData = appV1Api.read_namespaced_deployment_scale(name=name, namespace=namespace)
        readData.spec = {"replicas": replicas}
        appV1Api.patch_namespaced_deployment_scale(
            name=name,
            namespace=namespace,
            body=readData
        )
        return "Set " + name + " replicas to " + str(replicas)
    except ApiException as err:
        if err.status == 404:
            raise NotFound("No deployment found")
        else:
            raise err


def updateLimitAutoscale(name, namespace, maxLimit, minLimt, cpuLimit):
    try:
        readData = autoscaleV1.read_namespaced_horizontal_pod_autoscaler(
            name=name,
            namespace=namespace
        )
        readData.spec.max_replicas = maxLimit or readData.spec.max_replicas
        readData.spec.min_replicas = minLimt or readData.spec.min_replicas
        readData.spec.target_cpu_utilization_percentage = cpuLimit or readData.spec.target_cpu_utilization_percentage
        autoscaleV1.patch_namespaced_horizontal_pod_autoscaler(
            name=name,
            namespace=namespace,
            body=readData
        )
        return "Set " + name + " min: " + str(minLimt) + " max: " + str(maxLimit) + " cpu: " + str(cpuLimit) + "%"
    except ApiException as err:
        if err.status == 404:
            raise NotFound("No Autoscaler found")
        else:
            raise err
