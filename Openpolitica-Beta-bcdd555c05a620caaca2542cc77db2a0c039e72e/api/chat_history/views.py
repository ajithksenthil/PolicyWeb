from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Transcript, ChatMessage
from .serializers import TranscriptSerializer, ChatMessagesSerializer

def llm_response(user_response: str) -> str:
    # Replace this with your actual AI response generation logic
    # For now, it echoes the user's input
    ai_response = f"Hello, you said: {user_response}"
    return ai_response


class Transcription(APIView):
    def post(self, request):
        serialized_transcript = TranscriptSerializer(data=request.data)
        if serialized_transcript.is_valid():
            serialized_transcript.save()
            return Response(serialized_transcript.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_transcript.errors, status=status.HTTP_400_BAD_REQUEST)

class AllTranscripts(APIView):
    def get(self, request, user_id):
        # Retrieve all transcripts for the given user
        user_transcripts = Transcript.objects.filter(user_id=user_id)
        
        # Serialize and return the transcripts
        serializer = TranscriptSerializer(user_transcripts, many=True)
        return Response(serializer.data)

class CreateMessages(APIView):
    def get(self, request, transcript_id):
        # Get the transcript object or return a 404 if not found
        transcript = get_object_or_404(Transcript, pk=transcript_id)
        
        # Retrieve all messages of a particular transcript
        user_messages = ChatMessage.objects.filter(transcript=transcript_id)
        # Serialize and return the messages
        serializer = ChatMessagesSerializer(user_messages, many=True)
        return Response(serializer.data)

    def post(self, request, transcript_id):
        # Get the transcript object or return a 404 if not found
        transcript = get_object_or_404(Transcript, pk=transcript_id)
        
        # Extract user_response from the request data (adjust based on your request structure)
        user_response = request.data.get('user_response')

        # Generate AI response based on user input
        ai_response = llm_response(user_response)

        # Create a new ChatMessage using the transcript object
        chat_message = ChatMessage.objects.create(
            transcript=transcript,
            user_response=user_response,
            ai_response=ai_response
        )
        chat_message.save()
        # Serialize and return the created chat message with a 201 status code
        serializer = ChatMessagesSerializer(chat_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, transcript_id):
        transcript = get_object_or_404(Transcript, pk=transcript_id)
        transcript.delete()
        return Response({"message": "Transcript deleted successfully"}, status=status.HTTP_204_NO_CONTENT)