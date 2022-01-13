from os import environ

from dotenv import load_dotenv
from kubernetes import client
from kubernetes.client import ApiClient, configuration, ApiException
from rest_framework.exceptions import NotFound

load_dotenv()
configuration = configuration.Configuration()
configuration.host = environ['KUBERNETES_HOST']
configuration.api_key["authorization"] = environ['KUBERNETES_KEY']
api_client = ApiClient(configuration=configuration)
v1 = client.CoreV1Api(api_client=api_client)
appApi = client.AppsV1Api(api_client=api_client)
autoScalev1 = client.AutoscalingV1Api(api_client=api_client)
customv1 = client.CustomObjectsApi(api_client=api_client)


def getDeployment(name, namespace):
    try:
        response = appApi.read_namespaced_deployment(
            name=name,
            namespace=namespace
        )
        return response
    except ApiException as err:
        if err.status == 404:
            raise NotFound("No Deployment Found")
        else:
            raise err


def getAppsDetail(appname, namespace):
    try:
        deploymentData = appApi.read_namespaced_deployment(
            name=appname + "-deployment",
            namespace=namespace
        )
    except ApiException as err:
        if err.status == 404:
            raise NotFound("No Deployment Found")
        else:
            raise err
    try:
        serviceData = v1.read_namespaced_service(
            name=appname + "-service",
            namespace=namespace
        )
    except ApiException as err:
        if err.status == 404:
            raise NotFound("No Service Found")
        else:
            raise err
    try:
        podData = v1.list_namespaced_pod(namespace=namespace)
        podList = []
        for data in podData.items:
            if appname in data.metadata.name:
                podList.append({
                    "podName": data.metadata.name,
                    "podStatus": data.status.phase
                })
    except ApiException as err:
        if err.status == 404:
            raise NotFound("No Pod Found")
        else:
            raise err
    try:
        autoScalerData = autoScalev1.read_namespaced_horizontal_pod_autoscaler(
            name=appname + "-podautoscaler",
            namespace=namespace
        )
    except ApiException as err:
        if err.status == 404:
            raise NotFound("No AutoScaler Found")
        else:
            raise err
    output = {
        "deploymentName": deploymentData.metadata.name,
        "deploymentImage": deploymentData.spec.template.spec.containers[0].image,
        "readyReplicas": deploymentData.status.ready_replicas,
        "availableReplicas": deploymentData.status.available_replicas,
        "updatedReplicas": deploymentData.status.updated_replicas,
        "serviceName": serviceData.metadata.name,
        "servicePorts": serviceData.spec.ports[0].port,
        "pods": podList,
        "autoScalerPodName": autoScalerData.metadata.name,
        "autoScalerPodTargetCPU": autoScalerData.spec.target_cpu_utilization_percentage,
        "autoScalerPodCurrentCPU": autoScalerData.status.current_cpu_utilization_percentage,
        "autoScalerMinPod": autoScalerData.spec.min_replicas,
        "autoScalerMaxPod": autoScalerData.spec.max_replicas,
        "autoScalerCurrentPod": autoScalerData.status.current_replicas,
    }
    return output


def getPodsUsage():
    try:
        response = customv1.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "pods")
        output = []
        for i in response.get("items"):
            for j in i.get("containers"):
                data = {
                    "podname": i.get("metadata")["name"],
                    "podusage": j.get("usage"),
                    "namespace": i.get("metadata").get("namespace")
                }
                output.append(data)
        return output
    except ApiException as err:
        raise err


def getPodUsageFromNamespace(namespace):
    try:
        response = customv1.list_namespaced_custom_object(group="metrics.k8s.io", version="v1beta1",
                                                          namespace=namespace, plural="pods")
        output = []
        for i in response.get("items"):
            for j in i.get("containers"):
                data = {
                    "podname": i.get("metadata")["name"],
                    "podusage": j.get("usage"),
                    "namespace": i.get("metadata").get("namespace")
                }
                output.append(data)
        return output
    except ApiException as err:
        raise err


def getPodUsageFromAppName(name, namespace):
    try:
        response = customv1.list_namespaced_custom_object(group="metrics.k8s.io", version="v1beta1",
                                                          namespace=namespace, plural="pods")
        output = []
        for i in response.get("items"):
            for j in i.get("containers"):
                if name in j.get("name"):
                    data = {
                        "podname": j.get("name"),
                        "podusage": j.get("usage"),
                        "namespace": i.get("metadata").get("namespace")
                    }
                    output.append(data)
        return output
    except ApiException as err:
        raise err


def getNodeUsage():
    try:
        response = customv1.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
        output = []
        for i in response.get("items"):
            data = {
                "nodename": i.get("metadata").get("name"),
                "nodeusage": i.get("usage")
            }
            output.append(data)
        return output
    except ApiException as err:
        raise err
