from smtplib import SMTPException

from django.core.mail import send_mail
import calendar
from datetime import datetime, timedelta

from django.db.models import QuerySet

from config import settings
from distribution.models import MailingSettings, MailingLog
from django.utils import timezone


def sort_mailing():
    # Получаем все активные настройки рассылки
    active_mailings: QuerySet = MailingSettings.objects.filter(is_active=True)
    mailing_to_send = []
    now: str = datetime.now().strftime('%Y-%m-%d %H:%M')
    current_time = timezone.localtime(timezone.now())
    for mailing in active_mailings:
        # Проверяем, находится ли время рассылки в заданном интервале
        if mailing.start_time.strftime('%Y-%m-%d %H:%M') <= now <= mailing.end_time.strftime('%Y-%m-%d %H:%M'):
            mailing.status = "Запущена"
            mailing.save()
            mailing_to_send.append(mailing)
        if mailing.end_time <= current_time:
            mailing.status = "Завершена"
            mailing.save()
    # Определяем периодичность рассылки
    for mailing in mailing_to_send:
        next_send_str: str = mailing.next_send.strftime('%Y-%m-%d %H:%M')
        if next_send_str == now:
            send_mailing(mailing)
            if mailing.periodicity == "Раз в день":
                mailing.next_send = current_time + timedelta(days=1)
            if mailing.periodicity == "Раз в неделю":
                mailing.next_send = current_time + timedelta(days=7)
            if mailing.periodicity == "Раз в месяц":
                today = datetime.today()
                days = calendar.monthrange(today.year, today.month)[1]
                mailing.next_send = current_time + timedelta(days=days)
            mailing.save()
        if mailing.next_send > mailing.end_time:
            mailing.status = "Завершена"
            mailing.save()


# def send_mailing(mailing):
#     current_time = timezone.localtime(timezone.now())
#     status = ''
#     server_response = ''
#     try:
#         send_mail(
#             subject=mailing.message.title,
#             message=mailing.message.text,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[client.email for client in mailing.clients.all()],
#             fail_silently=False
#         )
#         status = 'Удачно'
#         server_response = 'OK'
#
#     except SMTPException as error:
#         status = 'Ошибка'
#         if 'authentication failed' in str(error):
#             server_response = 'Ошибка аутентификации в почтовом сервисе'
#         elif 'suspicion of SPAM' in str(error):
#             server_response = 'Слишком много рассылок, сервис отклонил письмо'
#         else:
#             server_response = error
#
#     finally:
#         MailingLog.objects.create(
#             time=current_time,
#             status=status,
#             server_response=server_response,
#             mailing=mailing,
#             client=mailing.clients,
#             owner=mailing.owner
#         )


def send_mailing(mailing):
    current_time = timezone.localtime(timezone.now())
    for client in mailing.client.all():
        try:
            send_mail(
                subject=mailing.message.title,
                message=mailing.message.text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.clients.all()],
                fail_silently=False
            )
            log = MailingLog.objects.create(
                time=current_time,
                status='Успешно',
                server_response='',
                mailing=mailing,
                client=client.email,
                owner=mailing.owner
            )
            log.save()
            return log

        except SMTPException as error:
            log = MailingLog.objects.create(
                time=current_time,
                status='Успешно',
                server_response=error,
                mailing=mailing,
                client=client.email,
                owner=mailing.owner
            )
            log.save()
            return log
