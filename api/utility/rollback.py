import re
from os import environ
from time import sleep

import requests
from dotenv import load_dotenv
from kubernetes.client import AppsV1Api, configuration, ApiClient, ApiException, CoreV1Api
from requests.auth import HTTPBasicAuth
from rest_framework.exceptions import NotFound

from ..kubernetes.get import getDeployment
from ..kubernetes.start import startDeployment
from ..kubernetes.stop import stopDeployment

load_dotenv()
imageRegistry = environ['IMAGE_REGISTRY']
imageRegistry = imageRegistry.replace("/library", "")
imageRegistryUser = environ['IMAGE_REGISTRY_USER']
imageRegistryPassword = environ['IMAGE_REGISTRY_PASSWORD']
configuration = configuration.Configuration()
configuration.host = environ['KUBERNETES_HOST']
configuration.api_key["authorization"] = environ['KUBERNETES_KEY']
api_client = ApiClient(configuration=configuration)
appV1Api = AppsV1Api(api_client=api_client)
v1Api = CoreV1Api(api_client=api_client)


def rollbackImage(appName, namespace):
    oldTags = requests.get(
        'https://' + imageRegistry + '/api/v2.0/projects/library/repositories/' + namespace + "-" + appName + '/artifacts',
        params={"q": "tags=old"})
    latestTags = requests.get(
        'https://' + imageRegistry + '/api/v2.0/projects/library/repositories/' + namespace + "-" + appName + '/artifacts',
        params={"q": "tags=latest"})
    if not oldTags.json() and not latestTags.json():
        return "No Version found"
    if not oldTags.json():
        return "No Old Version found"
    oldDigest = oldTags.json()[0].get("digest")
    latestDigest = latestTags.json()[0].get("digest")
    if oldDigest == latestDigest:
        return "Only 1 version"
    requests.delete(
        'https://' + imageRegistry + '/api/v2.0/projects/library/repositories/' + namespace + "-" + appName + '/artifacts/' + latestDigest,
        auth=HTTPBasicAuth(imageRegistryUser, imageRegistryPassword))
    requests.post(
        'https://' + imageRegistry + '/api/v2.0/projects/library/repositories/' + namespace + "-" + appName + '/artifacts/' + oldDigest + '/tags',
        auth=HTTPBasicAuth(imageRegistryUser, imageRegistryPassword), json={"name": "latest"})
    historyData = requests.get(
        'https://' + imageRegistry + '/api/v2.0/projects/library/repositories/' + namespace + "-" + appName + '/artifacts/' + oldDigest + '/additions/build_history')
    deploymentData = getDeployment(name=appName + "-deployment", namespace=namespace)
    serviceBody = v1Api.read_namespaced_service(
        name=appName + "-service",
        namespace=namespace
    )
    for i in historyData.json()[::-1]:
        data = i.get("created_by")
        if "EXPOSE" in data:
            port = re.sub("[^0-9]*", "", data)
            deploymentData.spec.template.spec.containers[0].ports[0].container_port = int(port)
            serviceBody.spec.ports[0].target_port = int(port)
            break
    try:
        appV1Api.patch_namespaced_deployment(
            name=appName + "-deployment",
            namespace=namespace,
            body=deploymentData
        )
        v1Api.patch_namespaced_service(name=appName + "-service", namespace=namespace, body=serviceBody)
    except ApiException as err:
        if err.status == 404:
            raise NotFound("No Deployment Found")
        else:
            raise err
    stopDeployment(name=appName + "-deployment", namespace=namespace)
    sleep(10.0)
    startDeployment(name=appName + "-deployment", namespace=namespace)
    return "Rollback Complete"


def rollbackList(appName, namespace):
    oldTags = requests.get(
        'https://' + imageRegistry + '/api/v2.0/projects/library/repositories/' + namespace + "-" + appName + '/artifacts',
        params={"q": "tags=old"})
    latestTags = requests.get(
        'https://' + imageRegistry + '/api/v2.0/projects/library/repositories/' + namespace + "-" + appName + '/artifacts',
        params={"q": "tags=latest"})
    if not oldTags.json() and not latestTags.json():
        return {"message": "No Version Found"}
    if not oldTags.json():
        return {
            "latest": latestTags.json()[0]['extra_attrs']['created']
        }
    oldDigest = oldTags.json()[0].get("digest")
    latestDigest = latestTags.json()[0].get("digest")
    if oldDigest == latestDigest:
        return {
            "latest": latestTags.json()[0]['extra_attrs']['created']
        }
    return {
        "old": oldTags.json()[0]['extra_attrs']['created'],
        "latest": latestTags.json()[0]['extra_attrs']['created']
    }
