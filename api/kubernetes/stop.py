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


def stopDeployment(name, namespace):
    try:
        readData = appV1Api.read_namespaced_deployment_scale(name=name, namespace=namespace)
        readData.spec = {"replicas": 0}
        appV1Api.patch_namespaced_deployment_scale(
            name=name,
            namespace=namespace,
            body=readData
        )
        return "Stopped " + name
    except ApiException as err:
        if err.status == 404:
            raise NotFound("No deployment found")
        else:
            raise err
