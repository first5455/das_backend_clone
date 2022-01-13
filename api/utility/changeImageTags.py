from os import environ

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()
imageRegistry = environ['IMAGE_REGISTRY']
imageRegistry = imageRegistry.replace("/library", "")
imageRegistryUser = environ['IMAGE_REGISTRY_USER']
imageRegistryPassword = environ['IMAGE_REGISTRY_PASSWORD']

def changeTags(appName, namespace):
    oldTags = requests.get(
        'https://' + imageRegistry + '/api/v2.0/projects/library/repositories/' + namespace + "-" + appName + '/artifacts',
        params={"q": "tags=old"})
    latestTags = requests.get(
        'https://' + imageRegistry + '/api/v2.0/projects/library/repositories/' + namespace + "-" + appName + '/artifacts',
        params={"q": "tags=latest"})
    if not oldTags.json() and not latestTags.json():
        return "No Version found"
    if not oldTags.json():
        latestDigest = latestTags.json()[0].get("digest")
        requests.post(
            'https://' + imageRegistry + '/api/v2.0/projects/library/repositories/' + namespace + "-" + appName + '/artifacts/' + latestDigest + '/tags',
            auth=HTTPBasicAuth(imageRegistryUser, imageRegistryPassword), json={"name": "old"})
        return "No Old Version found"
    oldDigest = oldTags.json()[0].get("digest")
    latestDigest = latestTags.json()[0].get("digest")
    if oldDigest == latestDigest:
        return "Only 1 version"
    requests.delete(
        'https://' + imageRegistry + '/api/v2.0/projects/library/repositories/' + namespace + "-" + appName + '/artifacts/' + oldDigest,
        auth=HTTPBasicAuth(imageRegistryUser, imageRegistryPassword))
    requests.post(
        'https://' + imageRegistry + '/api/v2.0/projects/library/repositories/' + namespace + "-" + appName + '/artifacts/' + latestDigest + '/tags',
        auth=HTTPBasicAuth(imageRegistryUser, imageRegistryPassword), json={"name": "old"})
    return "Change Complete"
