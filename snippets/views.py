from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics, permissions, mixins
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer


# Create your views here.

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        context = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(context, **kwargs)


@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        # return JSONResponse(serializer.data)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    if request.method == 'GET':
        try:
            snippet = Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)
        # return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        #
        # data = JSONParser().parse(request)
        # serializer = SnippetSerializer(snippet, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        # JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            snippet = Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        snippet.delete()
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


'''--------------------USE API-------------------------------------'''

#
# class SnippetList(APIView):
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
#
#
# class SnippetDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         return Response(SnippetSerializer(self.get_object(pk)))
#
#     def put(self, request, pk, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#
#     def delete(self, request, pk, format=None):
#         self.get_object(pk).delete()
#         return Response('delete success', status=status.HTTP_204_NO_CONTENT)


'''--------------------USE Mixin-----------------------------------'''
#
# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


'''--------------------USE generics APIView-----------------------------------'''


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # serializer.save()


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView, ):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
