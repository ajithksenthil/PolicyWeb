from django.urls import path
from . import views


urlpatterns = [
    path("all-transcripts/<int:user_id>/", views.AllTranscripts.as_view(), name="all-transcripts"),
    path("create-messages/<transcript_id>/", views.CreateMessages.as_view(), name="create-messages"),
    path("transcription/", views.Transcription.as_view(), name="transcription"),
]
