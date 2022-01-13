from os import environ
from time import sleep

from dotenv import load_dotenv
from kubernetes import client
from kubernetes.client import AppsV1Api, configuration, ApiClient, CoreV1Api, AutoscalingV1Api
from kubernetes.client.exceptions import ApiException

from ..kubernetes.start import startDeployment
from ..kubernetes.stop import stopDeployment
from ..kubernetes.update import updateReplicaSet
from ..models.Kubernetes import KubernetesDeployment, KubernetesService
from ..serializers.KubernetesSerializer import KubernetesDeploymentSerializer, KubernetesServiceSerializer

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


def createDeploymentObject(name, namespace, port, envData):
    envlist = []
    for i in envData:
        envObject = client.V1EnvVar(
            name=i.get("key"),
            value=i.get("value")
        )
        envlist.append(envObject)

    containerPort = client.V1ContainerPort(
        container_port=port
    )

    resource = client.V1ResourceRequirements(
        requests={
            "cpu": "100m"
        },
        limits={
            "cpu": "250m"
        }
    )

    container = client.V1Container(
        name=name,
        image=imageRegistry + "/" + namespace + "-" + name,
        ports=[containerPort],
        env=envlist,
        resources=resource,
        image_pull_policy="Always"
    )

    imagePullSecret = client.V1LocalObjectReference(
        name=namespace + "secret"
    )

    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(
            labels={"app": name}
        ),
        spec=client.V1PodSpec(
            containers=[container],
            image_pull_secrets=[imagePullSecret]),
    )

    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={
            "matchLabels": {"app": name}
        }
    )

    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(
            name=name + "-deployment",
            labels={"app": name}
        ),
        spec=spec
    )

    return deployment


def createServiceObject(name, appPort, containerPort):
    port = client.V1ServicePort(
        protocol="TCP",
        name=name + "-port",
        port=appPort,
        target_port=containerPort,
        node_port=appPort
    )

    spec = client.V1ServiceSpec(
        type="NodePort",
        selector={"app": name},
        ports=[port],
        external_i_ps=[kubernetesIp],
    )

    service = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name=name + "-service",
        ),
        spec=spec,
    )

    return service


def createDeployment(deployment, namespace):
    try:
        response = appV1Api.create_namespaced_deployment(
            body=deployment, namespace=namespace
        )
    except ApiException as err:
        if err.status == 409:
            deploymentData = appV1Api.read_namespaced_deployment_scale(name=deployment.metadata.name,
                                                                       namespace=namespace)
            saveReplicas = deploymentData.spec.replicas
            response = appV1Api.patch_namespaced_deployment(
                name=deployment.metadata.name, body=deployment, namespace=namespace
            )
            stopDeployment(name=deployment.metadata.name, namespace=namespace)
            sleep(10.0)
            startDeployment(name=deployment.metadata.name, namespace=namespace)
            updateReplicaSet(name=deployment.metadata.name, namespace=namespace, replicas=saveReplicas)
        else:
            raise err
    output = KubernetesDeployment(
        name=response.metadata.name,
        namespace=response.metadata.namespace,
        image=response.spec.template.spec.containers[0].image
    )
    deploymentSerializer = KubernetesDeploymentSerializer(output)
    return deploymentSerializer


def createService(service, namespace):
    try:
        response = v1Api.create_namespaced_service(
            body=service, namespace=namespace
        )
    except ApiException as err:
        if err.status == 422:
            v1Api.delete_namespaced_service(name=service.metadata.name, namespace=namespace)
            response = v1Api.create_namespaced_service(
                body=service, namespace=namespace
            )
        else:
            raise err
    output = KubernetesService(
        servicename=response.metadata.name,
        namespace=response.metadata.namespace,
        port=response.spec.ports[0].port
    )
    serviceSerializer = KubernetesServiceSerializer(output)
    return serviceSerializer


def createNamespace(namespace):
    metadata = client.V1ObjectMeta(
        name=namespace
    )

    namespaceObj = client.V1Namespace(
        metadata=metadata,
        api_version="v1",
        kind="Namespace"
    )
    try:
        v1Api.create_namespace(namespaceObj)
    except ApiException as err:
        if err.status == 409:
            v1Api.patch_namespace(
                name=namespace,
                body=namespaceObj
            )
        else:
            raise err


def createSecret(namespace):
    metadata = client.V1ObjectMeta(
        name=namespace + "secret",
        namespace=namespace
    )

    secret = client.V1Secret(
        api_version="v1",
        data={
            '.dockerconfigjson': dockerConfigJson},
        kind="Secret",
        metadata=metadata,
        type="kubernetes.io/dockerconfigjson"
    )
    try:
        v1Api.create_namespaced_secret(
            body=secret, namespace=namespace
        )
    except ApiException as err:
        if err.status == 409:
            v1Api.patch_namespaced_secret(
                name=namespace + "secret",
                body=secret,
                namespace=namespace
            )
        else:
            raise err


def createHorizontalPodAutoScaleObj(name, namespace):
    scaleTargetRef = client.V1CrossVersionObjectReference(
        api_version="apps/v1",
        kind="Deployment",
        name=name + "-deployment"
    )

    spec = client.V1HorizontalPodAutoscalerSpec(
        max_replicas=5,
        min_replicas=1,
        scale_target_ref=scaleTargetRef,
        target_cpu_utilization_percentage=80
    )

    metadata = client.V1ObjectMeta(
        name=name + "-podautoscaler",
        namespace=namespace
    )

    horizontalPod = client.V1HorizontalPodAutoscaler(
        api_version="autoscaling/v1",
        kind="HorizontalPodAutoscaler",
        metadata=metadata,
        spec=spec
    )
    return horizontalPod


def createHorizontalPodAutoScale(name, namespace, horizonPod):
    try:
        autoscaleV1.create_namespaced_horizontal_pod_autoscaler(
            namespace=namespace,
            body=horizonPod
        )
    except ApiException as err:
        if err.status == 409:
            autoscaleV1.patch_namespaced_horizontal_pod_autoscaler(
                name=name + "-podautoscaler",
                namespace=namespace,
                body=horizonPod
            )
        else:
            raise err
