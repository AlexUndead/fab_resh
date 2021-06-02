from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response


class AuthView(APIView):
    '''аутентификация пользователя'''
    permission_classes = [permissions.IsAuthenticated]


class CreateBaseView(APIView):
    '''базоый класс для создание'''
    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeBaseView(APIView):
    '''базоый класс для изменения'''
    def patch(self, request, id):
        try:
            object = self.object.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response(
                self.DOES_NOT_EXIST_MESSAGE,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteBaseView(APIView):
    '''удаление вопроса'''
    def delete(self, request, id):
        try:
            self.object.objects.get(id=id).delete()
        except ObjectDoesNotExist:
            return Response(
                self.DOES_NOT_EXIST_MESSAGE,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)
