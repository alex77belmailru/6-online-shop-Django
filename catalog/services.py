from django.core.cache import cache
from django.core.mail import send_mail

from catalog.models import Category
from config import settings


def get_category_cached(product_pk):  # получает категорию товара
    if settings.CACHE_ENABLED:  # если кэш включен
        key = f'category_list'
        category_list = cache.get(key)  # ищем нужный ключ
        if category_list is None:  # если не нашли
            category_list = Category.objects.all()  # берем из бд
            cache.set(key, category_list)  # и кэшируем
    else:
        category_list = Category.objects.all()  # если кэш отключен, берем из бд

    return category_list.get(product=product_pk)


def sendmail(message, recipient, subject='Рассылка Django'):  # отправка письма
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient)
