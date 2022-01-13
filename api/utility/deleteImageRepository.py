from os import environ

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()
imageRegistry = environ['IMAGE_REGISTRY']
imageRegistry = imageRegistry.replace("/library", "")
imageRegistryUser = environ['IMAGE_REGISTRY_USER']
imageRegistryPassword = environ['IMAGE_REGISTRY_PASSWORD']


def deleteImageRepository(repository):
    response = requests.delete(
        'https://' + imageRegistry + '/api/v2.0/projects/library/repositories/' + repository,
        auth=HTTPBasicAuth(imageRegistryUser, imageRegistryPassword))
    return response
