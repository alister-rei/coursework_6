# Generated by Django 4.2.7 on 2023-11-25 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Тема письма')),
                ('text', models.TextField(verbose_name='Письмо')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщения',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='MailingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Дата начала рассылки')),
                ('end_time', models.DateTimeField(verbose_name='Дата окончания рассылки')),
                ('next_send', models.DateTimeField(blank=True, null=True, verbose_name='Дата следующей рассылки')),
                ('periodicity', models.CharField(choices=[('Раз в день', 'Раз в день'), ('Раз в неделю', 'Раз в неделю'), ('Раз в месяц', 'Раз в месяц')], max_length=50, verbose_name='Периодичность')),
                ('status', models.CharField(choices=[('Завершена', 'Завершена'), ('Создана', 'Создана'), ('Запущена', 'Запущена')], default='Создана', max_length=50, verbose_name='Статус рассылки')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_active', models.BooleanField(choices=[(True, 'Активна'), (False, 'На модерации')], default=True, verbose_name='Активна')),
                ('clients', models.ManyToManyField(to='clients.client', verbose_name='Клиенты рассылки')),
                ('message', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='distribution.message', verbose_name='Сообщение')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'настройки рассылки',
                'verbose_name_plural': 'настройки рассылки',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='MailingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания лога')),
                ('status', models.BooleanField(verbose_name='Статус попытки')),
                ('server_response', models.CharField(blank=True, null=True, verbose_name='Ответ почтового сервера')),
                ('client', models.ManyToManyField(to='clients.client', verbose_name='Клиент рассылки')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribution.mailingsettings', verbose_name='Рассылка')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'лог',
                'verbose_name_plural': 'логи',
                'ordering': ('time',),
            },
        ),
    ]
