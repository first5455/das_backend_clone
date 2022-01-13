from os import environ

from dotenv import load_dotenv
from kubernetes import client
from kubernetes.client import ApiClient, configuration
from kubernetes.client.exceptions import ApiException

from ..serializers.AppSerializer import LogSerializer

load_dotenv()
configuration = configuration.Configuration()
configuration.host = environ['KUBERNETES_HOST']
configuration.api_key["authorization"] = environ['KUBERNETES_KEY']
api_client = ApiClient(configuration=configuration)
v1 = client.CoreV1Api(api_client=api_client)
appApi = client.AppsV1Api(api_client=api_client)
autoScalev1 = client.AutoscalingV1Api(api_client=api_client)


def getPodLog(podname, namespace):
    try:
        response = v1.read_namespaced_pod_log(
            name=podname,
            namespace=namespace
        )
        print(response)
        data = {
            "podname": podname,
            "logs": response
        }
        serializer = LogSerializer(
            data=data
        )
        serializer.is_valid(raise_exception=True)
        return serializer.data
    except ApiException as err:
        raise err
