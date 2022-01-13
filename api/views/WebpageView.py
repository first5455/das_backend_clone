from django.template.response import TemplateResponse
from os import environ
from dotenv import load_dotenv

load_dotenv()
def home(request, template_name="home.html"):
    args = {}
    backend = environ['BACKEND_WEBSITE']
    frontend = environ['FRONTEND_WEBSITE']
    args['frontendweb'] = frontend
    args['backendweb'] = backend
    return TemplateResponse(request, template_name, args)
