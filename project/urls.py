from django.urls import path
from . import visitor_views, user_views

urlpatterns = [
    path('getdata', visitor_views.analyse),
    path('getlabels', visitor_views.labels),
    path('getlegends', visitor_views.labels_legends),
    path('test', visitor_views.convertEPS),
    path('editable', visitor_views.edit_value),

    # Registered Users Routes
    path('getData', user_views.analyse),
    path('getLabels', user_views.labels),
    path('getLegends', user_views.labels_legends),
    path('usereditable', user_views.edit_value),
    path('saveGraph', user_views.saveGraph ),
    path('newGraph', user_views.newGraph ),
    path('getGraph', user_views.getGraph),
    path('deleteGraph', user_views.deleteGraph),
    path('projectCreate', user_views.createProject),
    path('projectsCount', user_views.projectCount),
    path('projectsList', user_views.projectList),
    path('yourProjects', user_views.yourProjects),
    path('projectDelete', user_views.projectDelete),
    
    path('archiveProject', user_views.archiveProject),
    path('unArchive', user_views.unArchive),
    path('archivedProjects', user_views.archivedProjects),
    path('fileDelete', user_views.fileDelete),
    path('fileRename', user_views.fileRename),
    path('fileDownload', user_views.fileDownload),
    path('projectGraphCount', user_views.projectGraphCount),
    path('fileDownload', user_views.download_project_file),
    path('saveFile', user_views.newFile), #change the name on frontend
    path('openProject', user_views.projectOpen),
    path('trashedProjectsList', user_views.trashedProject),
    path('projectRestore', user_views.projectRestore),
    path('projectDeletePermenantly', user_views.projectDeletePermanently),

    path('sendNotification', user_views.sendNotification),
    path('sharedProjects', user_views.sharedProjects),
    path('getSharedList', user_views.getSharedList), 
    path('deleteAccess', user_views.deleteAccess), 
    path('getNotifications/', user_views.getNotifications),
    path('readNotification', user_views.openNotification),
    path('testNotification/<id>/', user_views.testNotification, name='testNotification'),
    path('markAsRead', user_views.markAsRead),
    path('markAllAsRead', user_views.markAllAsRead),
    path('acceptProject', user_views.shareAccept),
    path('declineProject', user_views.shareDecline),
    path('deleteNotification', user_views.deleteNotification),
    path('getLogs', user_views.projectHistory),
    path('getLogsGraph', user_views.getLogsGraph),

    path('sendMail/', user_views.sendMail),
]