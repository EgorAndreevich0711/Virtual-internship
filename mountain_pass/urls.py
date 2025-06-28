from django.urls import path
from .views import SubmitDataView, UpdatePassStatusView, MountainPassDetail, MountainPassUpdate, UserMountainPassList

urlpatterns = [
    path('submitData/', SubmitDataView.as_view(), name='submit-data'),
    path('updateStatus/<int:pass_id>/', UpdatePassStatusView.as_view(), name='update-status'),

    path('submitData/get/<int:pk>/', MountainPassDetail.as_view(), name='mountain_pass-detail'),
    path('submitData/update/<int:pk>/', MountainPassUpdate.as_view(), name='mountain_pass-update'),
    path('submitData/list/', UserMountainPassList.as_view(), name='mountain_pass-user-list'),
]
