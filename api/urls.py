from django.urls import path

from .views.KubernetesAllDeploymentView import *
from .views.KubernetesAllHorizontalView import *
from .views.KubernetesAllNodeView import *
from .views.KubernetesAllPodView import *
from .views.KubernetesAllSecretView import *
from .views.KubernetesAllServiceView import *
from .views.KubernetesCreateDeploymentView import kubernetesCreateDeployment
from .views.KubernetesDeleteDeployment import kubernetesDeleteDeployment
from .views.KubernetesDeleteHorizontalAutoScaler import kubernetesDeleteHorizontalAutoScaler
from .views.KubernetesDeleteNamespace import kubernetesDeleteNamespace
from .views.KubernetesDeleteServiceView import kubernetesDeleteService
from .views.KubernetesGetApp import kubernetesGetApp
from .views.KubernetesGetNodeUsage import kubernetesGetNodeUsage
from .views.KubernetesGetPodLog import kubernetesGetPogLog
from .views.KubernetesGetPodUsage import kubernetesGetPodUsage, kubernetesGetPodUsageFromNamespace, \
    kubernetesGetPodUsageFromAppName
from .views.KubernetesRollback import kubernetesRollback
from .views.KubernetesRollbackListView import kubernetesRollbackList
from .views.KubernetesStartDeployment import kubernetesStartDeployment
from .views.KubernetesStopDeployment import kubernetesStopDeployment
from .views.KubernetesUpdateLimitAutoScaleView import kubernetesUpdateLimitAutoScaler
from .views.KubernetesUpdateReplicasetView import kubernetesUpdateReplicaSet
from .views.UploadView import FileUploadView
from .views.UserView import *
from .views.UserRoleView import UserRoleView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/<int:id>', UserView.as_view()),
    path('user/', UserAllView.as_view()),
    path('user/editrole/<int:id>', UserRoleView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('kubernetes/allpods/', kubernetesAllPodView.as_view()),
    path('kubernetes/allpods/<namespace>', kubernetesAllPodViewFromNamespace.as_view()),
    path('kubernetes/allservices/', kubernetesAllServiceView.as_view()),
    path('kubernetes/allservices/<namespace>', kubernetesAllServiceViewFromNamespace.as_view()),
    path('kubernetes/alldeployments/', kubernetesAllDeployment.as_view()),
    path('kubernetes/alldeployments/<namespace>', kubernetesAllDeploymentFromNameSpace.as_view()),
    path('kubernetes/allnodes/', kubernetesAllNodesView.as_view()),
    path('kubernetes/allhorizontalpods/', kubernetesAllHorizontal.as_view()),
    path('kubernetes/allhorizontalpods/<namespace>', kubernetesAllHorizontalFromNamespace.as_view()),
    path('kubernetes/allsecrets/', kubernetesAllSecretView.as_view()),
    path('kubernetes/allsecrets/<namespace>', kubernetesAllSecretViewFromNamespace.as_view()),
    path('kubernetes/getpodlog/<namespace>/<name>', kubernetesGetPogLog.as_view()),
    path('kubernetes/getapp/<namespace>/<name>', kubernetesGetApp.as_view()),
    path('kubernetes/getrollback/<namespace>/<name>', kubernetesRollbackList.as_view()),
    path('kubernetes/createdeployment/<namespace>/<name>/<portdocker>', kubernetesCreateDeployment.as_view()),
    path('kubernetes/deletedeployment/<namespace>/<name>', kubernetesDeleteDeployment.as_view()),
    path('kubernetes/deleteservice/<namespace>/<name>', kubernetesDeleteService.as_view()),
    path('kubernetes/deletehorizontalpod/<namespace>/<name>', kubernetesDeleteHorizontalAutoScaler.as_view()),
    path('kubernetes/deletenamespace/<namespace>', kubernetesDeleteNamespace.as_view()),
    path('kubernetes/stopdeployment/<namespace>/<name>', kubernetesStopDeployment.as_view()),
    path('kubernetes/startdeployment/<namespace>/<name>', kubernetesStartDeployment.as_view()),
    path('kubernetes/rollback/<namespace>/<name>', kubernetesRollback.as_view()),
    path('kubernetes/getpodlog/<namespace>/<name>', kubernetesGetPogLog.as_view()),
    path('kubernetes/getpodusage/', kubernetesGetPodUsage.as_view()),
    path('kubernetes/getpodusage/<namespace>', kubernetesGetPodUsageFromNamespace.as_view()),
    path('kubernetes/getpodusage/<namespace>/<name>', kubernetesGetPodUsageFromAppName.as_view()),
    path('kubernetes/getnodeusage/', kubernetesGetNodeUsage.as_view()),
    path('kubernetes/updatereplicas/<namespace>/<name>', kubernetesUpdateReplicaSet.as_view()),
    path('kubernetes/updatelimitautoscaler/<namespace>/<name>', kubernetesUpdateLimitAutoScaler.as_view()),
    path('upload/<namespace>/<appname>', FileUploadView.as_view()),
]
