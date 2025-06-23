from django.urls import path
from .views import SubmitDataView, UpdatePassStatusView

urlpatterns = [
    path('submitData/', SubmitDataView.as_view(), name='submit-data'),
    path('updateStatus/<int:pass_id>/', UpdatePassStatusView.as_view()),
]