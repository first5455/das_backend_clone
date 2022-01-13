from os import environ

from django.core.files.storage import FileSystemStorage
from dotenv import load_dotenv
from paramiko import SSHClient, AutoAddPolicy
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from ..utility.authenticated import checkToken
from ..utility.changeImageTags import changeTags

load_dotenv()
serverIp = environ['UPLOAD_SERVER_IP']
serverPort = environ['UPLOAD_SERVER_PORT']
serverUsername = environ['UPLOAD_SERVER_USERNAME']
serverPassword = environ['UPLOAD_SERVER_PASSWORD']


class UploadSerializer(serializers.Serializer):
    def validate_file_extension(value):
        import os
        from django.core.exceptions import ValidationError
        ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
        valid_extensions = ['.zip']
        if not ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')

    file = serializers.FileField(validators=[validate_file_extension])


class FileUploadView(GenericAPIView):
    parser_classes = (MultiPartParser,)
    serializer_class = UploadSerializer

    def post(self, request, appname, namespace):
        checkToken(request)
        fileSerializer = UploadSerializer(data=request.data)
        if not fileSerializer.is_valid():
            return Response(
                data=fileSerializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        changeTags(appName=appname, namespace=namespace)
        file = request.data['file']
        fs = FileSystemStorage()
        fileName = namespace + "-" + appname + ".zip"
        fs.save(fileName, file)
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(serverIp, serverPort, serverUsername, serverPassword)
        sftp = client.open_sftp()
        sftp.put('./UploadFile/' + fileName, "/home/" + serverUsername + "/Upload/" + fileName)
        sftp.close()
        stdin, stdout, stderr = client.exec_command('~/scriptExtract.sh ' + fileName)
        error1 = stderr.read().decode("utf8")
        if error1 != "":
            fs.delete(fileName)
            return Response({
                "detail": error1
            }, status=400)
        stdin2, stdout2, stderr2 = client.exec_command('~/scriptDocker.sh ' + fileName)
        error2 = stderr2.read().decode("utf8")
        if error2 != "":
            fs.delete(fileName)
            return Response({
                "detail": error2
            }, status=400)
        commandOutput = stdout2.read().decode("utf8").replace("\n", "")
        client.close()
        fs.delete(fileName)
        return Response({
            "message": "file received",
            "portFound": commandOutput
        })
