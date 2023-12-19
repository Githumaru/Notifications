from .services import send_message_to_api
from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Mailing, Client, Message
from .serializers import MailingSerializer, ClientSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.decorators import action
from django.utils import timezone
import re



class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    # Метод для создания новой рассылки
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        processor = MailingProcessor()
        processor.process_active_mailings()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
    def message_statistics(self, request, pk=None):
        mailing = self.get_object()
        messages = Message.objects.filter(mailing=mailing)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def update_mailing_attributes(self, request, pk=None):
        try:
            mailing = self.get_object()
            serializer = self.get_serializer(mailing, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def delete_mailing(self, request, pk=None):
        try:
            mailing = self.get_object()
            mailing.delete()
            return Response({"message": "Mailing deleted successfully"})
        except Mailing.DoesNotExist:
            return Response({"error": "Mailing does not exist"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def validate_phone_number(self, phone_number):
        return bool(re.match(r'^7\d{10}$', phone_number))

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', '')
        if not self.validate_phone_number(phone_number):
            return Response({"message": "Неверный формат номера телефона"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', '')
        if not self.validate_phone_number(phone_number):
            return Response({"message": "Неверный формат номера телефона"}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Client.DoesNotExist:
            return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Client deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




class MailingStatisticsAPIView(APIView):
    def get(self, request, format=None):
        # Получение общей статистики по созданным рассылкам
        mailings_count = Mailing.objects.count()

        # Получение количества отправленных сообщений по статусам
        messages_statistics = Message.objects.values('status').annotate(total=Count('status'))

        return Response({
            'total_mailings': mailings_count,
            'messages_statistics': messages_statistics
        })


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MailingProcessor:
    @staticmethod
    def process_active_mailings():
        active_mailings = Mailing.objects.filter(start_datetime__lte=timezone.now(), end_datetime__gte=timezone.now())
        for mailing in active_mailings:
            clients = Client.objects.filter(mobile_operator_code=mailing.mobile_operator_code, tag=mailing.tag)
            for client in clients:
                send_message_to_api(client.id, mailing.message_text)
                pass
