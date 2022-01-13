from rest_framework import serializers

from ..models.Kubernetes import KubernetesPod, KubernetesService, KubernetesNode, KubernetesDeployment, \
    KubernetesCreateOutput, KubernetesHorizontal


class KubernetesPodSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesPod
        fields = ['podip', 'podname', 'namespace', 'status', 'node']


class KubernetesServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesService
        fields = ['servicename', 'namespace', 'port', 'clusterip', 'externalip', 'type', 'protocol']


class KubernetesNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesNode
        fields = ['ip', 'name', 'role', 'cpu_capacity', 'memory_capacity']


class KubernetesDeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesDeployment
        fields = ['name', 'namespace', 'readyReplicas', 'availableReplicas', 'uptodateReplicas']


class KubernetesCreateOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesCreateOutput
        fields = ['deploymentName', 'serviceName', 'nameSpace', 'name', 'port']


class KubernetesHorizontalAutoscalerSerializer(serializers.ModelSerializer):
    class Meta:
        model = KubernetesHorizontal
        fields = ["name", "namespace", "deploymentTarget", "targetcpu", "currentcpu", "minpod", "maxpod", "currentpod"]
