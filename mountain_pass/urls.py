from django.urls import path
from .views import SubmitDataView, UpdatePassStatusView, MountainPassDetail, MountainPassUpdate, UserMountainPassList

urlpatterns = [
    path('submitData/', SubmitDataView.as_view(), name='submit-data'),
    path('updateStatus/<int:pass_id>/', UpdatePassStatusView.as_view()),

    path('submitData/get/<int:pk>/', MountainPassDetail.as_view()),
    path('submitData/update/<int:pk>/', MountainPassUpdate.as_view()),
    path('submitData/list/', UserMountainPassList.as_view()),
]
