from django.urls import path
from .views import SubmitDataView,  UserMountainPassList, MountainPassDetailUpdate

urlpatterns = [

    path('submitData/', SubmitDataView.as_view(), name='submit-data'),

    path('submitData/<int:pk>/', MountainPassDetailUpdate.as_view(), name='mountainpass-detail-update'),


    path('submitData/', UserMountainPassList.as_view(), name='mountainpass-user-list'),
]
