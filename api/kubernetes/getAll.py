from os import environ

from dotenv import load_dotenv
from kubernetes import client
from kubernetes.client import ApiClient, configuration

from ..models.Kubernetes import KubernetesPod, KubernetesService, KubernetesNode, KubernetesDeployment, \
    KubernetesHorizontal
from ..serializers.KubernetesSerializer import KubernetesPodSerializer, KubernetesServiceSerializer, \
    KubernetesNodeSerializer, KubernetesDeploymentSerializer, KubernetesHorizontalAutoscalerSerializer

load_dotenv()
configuration = configuration.Configuration()
configuration.host = environ['KUBERNETES_HOST']
configuration.api_key["authorization"] = environ['KUBERNETES_KEY']
api_client = ApiClient(configuration=configuration)
v1 = client.CoreV1Api(api_client=api_client)
appApi = client.AppsV1Api(api_client=api_client)
autoScalev1 = client.AutoscalingV1Api(api_client=api_client)


def getAllPods():
    response = v1.list_pod_for_all_namespaces(watch=False)
    output = []
    for i in response.items:
        object = KubernetesPod(podip=i.status.pod_ip, namespace=i.metadata.namespace, podname=i.metadata.name,
                               status=i.status.phase, node=i.spec.node_name)
        output.append(object)
    podSerializers = KubernetesPodSerializer(output, many=True)
    return podSerializers


def getAllPodsFromNameSpace(namespace):
    response = v1.list_namespaced_pod(namespace=namespace)
    output = []
    for i in response.items:
        object = KubernetesPod(podip=i.status.pod_ip, namespace=i.metadata.namespace, podname=i.metadata.name,
                               status=i.status.phase, node=i.spec.node_name)
        output.append(object)
    podSerializers = KubernetesPodSerializer(output, many=True)
    return podSerializers


def getAllServices():
    response = v1.list_service_for_all_namespaces(watch=False)
    output = []
    for i in response.items:
        if i.spec.external_i_ps is None:
            dataExternalip = "None"
        else:
            dataExternalip = i.spec.external_i_ps[0]
        object = KubernetesService(
            namespace=i.metadata.namespace,
            servicename=i.metadata.name,
            port=i.spec.ports[0].port,
            protocol=i.spec.ports[0].protocol,
            clusterip=i.spec.cluster_ip,
            externalip=dataExternalip,
            type=i.spec.type
        )
        output.append(object)
    serviceSerializers = KubernetesServiceSerializer(output, many=True)
    return serviceSerializers


def getAllServicesFromNameSpace(namespace):
    response = v1.list_namespaced_service(namespace=namespace, watch=False)
    output = []
    for i in response.items:
        if i.spec.external_i_ps is None:
            dataExternalip = "None"
        else:
            dataExternalip = i.spec.external_i_ps[0]
        object = KubernetesService(
            namespace=i.metadata.namespace,
            servicename=i.metadata.name,
            port=i.spec.ports[0].port,
            protocol=i.spec.ports[0].protocol,
            clusterip=i.spec.cluster_ip,
            externalip=dataExternalip,
            type=i.spec.type
        )
        output.append(object)
    serviceSerializers = KubernetesServiceSerializer(output, many=True)
    return serviceSerializers


def getAllNode():
    response = v1.list_node(watch=False)
    output = []
    for i in response.items:
        allkeys = list(i.metadata.labels.keys())
        matching = [s for s in allkeys if "node-role.kubernetes.io/" in s]
        roles = []
        for r in matching:
            r = r.replace("node-role.kubernetes.io/", "")
            roles.append(r)
        role = ', '.join(roles)
        object = KubernetesNode(ip=i.status.addresses[0].address, name=i.metadata.name, role=role,
                                cpu_capacity=i.status.capacity["cpu"], memory_capacity=i.status.capacity["memory"])
        output.append(object)
    nodeSerializers = KubernetesNodeSerializer(output, many=True)
    return nodeSerializers


def getAllDeployment():
    response = appApi.list_deployment_for_all_namespaces()
    output = []
    for i in response.items:
        object = KubernetesDeployment(
            name=i.metadata.name,
            namespace=i.metadata.namespace,
            image=i.spec.template.spec.containers[0].image,
            readyReplicas=i.status.ready_replicas,
            availableReplicas=i.status.available_replicas,
            uptodateReplicas=i.status.updated_replicas
        )
        output.append(object)
    deploymentSerializer = KubernetesDeploymentSerializer(output, many=True)
    return deploymentSerializer


def getAllDeploymentFromNameSpace(namespace):
    response = appApi.list_namespaced_deployment(
        namespace=namespace
    )
    output = []
    for i in response.items:
        object = KubernetesDeployment(
            name=i.metadata.name,
            namespace=i.metadata.namespace,
            image=i.spec.template.spec.containers[0].image,
            readyReplicas=i.status.ready_replicas,
            availableReplicas=i.status.available_replicas,
            uptodateReplicas=i.status.updated_replicas
        )
        output.append(object)
    deploymentSerializer = KubernetesDeploymentSerializer(output, many=True)
    return deploymentSerializer


def getAllHorizontalAutoScalerPodAll():
    response = autoScalev1.list_horizontal_pod_autoscaler_for_all_namespaces()
    output = []
    for i in response.items:
        object = KubernetesHorizontal(
            name=i.metadata.name,
            namespace=i.metadata.namespace,
            deploymentTarget=i.spec.scale_target_ref.name,
            targetcpu=i.spec.target_cpu_utilization_percentage,
            currentcpu=i.status.current_cpu_utilization_percentage,
            minpod=i.spec.min_replicas,
            maxpod=i.spec.max_replicas,
            currentpod=i.status.current_replicas
        )
        output.append(object)
    horizontalSerializer = KubernetesHorizontalAutoscalerSerializer(output, many=True)
    return horizontalSerializer


def getAllHorizontalAutoScalerPodAllFromNamespace(namespace):
    response = autoScalev1.list_namespaced_horizontal_pod_autoscaler(
        namespace=namespace
    )
    output = []
    for i in response.items:
        object = KubernetesHorizontal(
            name=i.metadata.name,
            namespace=i.metadata.namespace,
            deploymentTarget=i.spec.scale_target_ref.name,
            targetcpu=i.spec.target_cpu_utilization_percentage,
            currentcpu=i.status.current_cpu_utilization_percentage,
            minpod=i.spec.min_replicas,
            maxpod=i.spec.max_replicas,
            currentpod=i.status.current_replicas
        )
        output.append(object)
    horizontalSerializer = KubernetesHorizontalAutoscalerSerializer(output, many=True)
    return horizontalSerializer


def getAllSecret():
    response = v1.list_secret_for_all_namespaces()
    output = []
    for i in response.items:
        data = {
            "name": i.metadata.name,
            "namespace": i.metadata.namespace
        }
        output.append(data)
    return output


def getAllSecretFromNameSpace(namespace):
    response = v1.list_namespaced_secret(namespace=namespace)
    output = []
    for i in response.items:
        data = {
            "name": i.metadata.name,
            "namespace": i.metadata.namespace
        }
        output.append(data)
    return output
