from django.db import models


class KubernetesPod(models.Model):
    podip = models.CharField(max_length=500)
    podname = models.CharField(max_length=500)
    namespace = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    node = models.CharField(max_length=254, default="")


class KubernetesService(models.Model):
    servicename = models.CharField(max_length=500)
    namespace = models.CharField(max_length=500)
    port = models.CharField(max_length=500, default="")
    protocol = models.CharField(max_length=500, default="")
    clusterip = models.CharField(max_length=500, default="")
    externalip = models.CharField(max_length=500, default="")
    type = models.CharField(max_length=500, default="")


class KubernetesNode(models.Model):
    ip = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    role = models.CharField(max_length=500)
    cpu_capacity = models.CharField(max_length=500, default="")
    memory_capacity = models.CharField(max_length=500, default="")

class KubernetesDeployment(models.Model):
    name = models.CharField(max_length=500)
    namespace = models.CharField(max_length=500)
    image = models.CharField(max_length=500)
    readyReplicas = models.CharField(max_length=500)
    availableReplicas = models.CharField(max_length=500)
    uptodateReplicas = models.CharField(max_length=500)


class KubernetesCreateOutput(models.Model):
    deploymentName = models.CharField(max_length=500)
    serviceName = models.CharField(max_length=500)
    nameSpace = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    port = models.CharField(max_length=500)


class KubernetesHorizontal(models.Model):
    name = models.CharField(max_length=500)
    namespace = models.CharField(max_length=500)
    deploymentTarget = models.CharField(max_length=500)
    targetcpu = models.CharField(max_length=500)
    currentcpu = models.CharField(max_length=500)
    minpod = models.CharField(max_length=500)
    maxpod = models.CharField(max_length=500)
    currentpod = models.CharField(max_length=500)
