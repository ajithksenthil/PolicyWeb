from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .serializers import *


class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.all().order_by('-date_created')
        serializer = PostSerializer(posts, many=True)  # Use your serializer to serialize the data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialized_post = PostSerializer(data=request.data)
        if serialized_post.is_valid():
            serialized_post.save()
            return Response(serialized_post.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_post.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PostView(APIView):
    def get(self, request, eid):  # Change 'post_id' to 'eid'
        post = get_object_or_404(Post, eid=eid)  # Change 'post_id' to 'eid'
        serializer = PostSerializer(post)  # Use your serializer to serialize the data
        return Response(serializer.data, status=status.HTTP_200_OK)


   
class PostCommentsView(APIView):
    def get(self, request, eid):  # Change 'post_id' to 'eid'
        post = get_object_or_404(Post, eid=eid)  # Change 'post_id' to 'eid'
        comments = Comment.objects.filter(post=post).order_by('-date_created')  # Use 'post' instead of 'post_id'
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, eid):
        serialized_comment = CommentSerializer(data=request.data)
        if serialized_comment.is_valid():
            serialized_comment.save()
            return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_comment.errors, status=status.HTTP_400_BAD_REQUEST)




        