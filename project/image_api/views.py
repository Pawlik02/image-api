from rest_framework import generics
from image_api.models import Image
from image_api.serializers import ImageSerializer, ImageSerializerCreateUpdate, ImageSerializerCreateUpdateTime, ImageSerializerExpiring
from image_api.permissions import IsOwner, HasOriginalImage, HasPlan
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
import datetime


class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated, HasPlan]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ImageSerializer
        if self.request.method == 'POST':
            if self.request.user.plan.expiring_link:
                return ImageSerializerCreateUpdateTime
            else:
                return ImageSerializerCreateUpdate

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ImageSerializer
        if self.request.method == 'PUT':
            if self.request.user.plan.expiring_link:
                return ImageSerializerCreateUpdateTime
            else:
                return ImageSerializerCreateUpdate
        if self.request.method == 'PATCH':
            if self.request.user.plan.expiring_link:
                return ImageSerializerCreateUpdateTime
            else:
                return ImageSerializerCreateUpdate


class ImageOriginal(generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsOwner, HasOriginalImage]

    def get(self, request, *args, **kwargs):
        image = self.get_object()
        return HttpResponse(f'<img src={image.image.url}>')


@api_view(['GET'])
def image_detail_expiring(request, pk, expiring_link):
    try:
        image = Image.objects.get(pk=pk)
        if image.expiring_link != expiring_link:
            return Response(status=status.HTTP_404_NOT_FOUND)
        link_time = image.time
        expired_time = int(datetime.datetime.now(datetime.timezone.utc).strftime('%s')) - int(image.created_on.strftime('%s'))
        if expired_time > link_time:
            return Response(status=status.HTTP_410_GONE)
    except Image.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer_context = {
            'request': request,
        }
        serializer = ImageSerializerExpiring(image, context=serializer_context)
        return Response(serializer.data)
    else:
        return status.HTTP_405_METHOD_NOT_ALLOWED


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def image_thumbnail(request, pk, height):
    try:
        image = Image.objects.get(pk=pk)
        if request.user != image.owner:
            return Response(status=status.HTTP_403_FORBIDDEN)
    except Image.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.user.plan.height.values_list()
    heights = []
    for item in data:
        heights.append(item[1])

    if height not in heights:
        return Response(status=status.HTTP_403_FORBIDDEN)

    # image = PIL.Image.open(image.image.path)
    # ratio = height / image.size[1]
    # size = (int(image.size[0] * ratio), height)
    # image = image.resize(size)
    return HttpResponse(f'<img src={image.image.url} height="{height}px">')
