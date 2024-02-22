import os
from json import load

from django.core.management import BaseCommand

from catalog.models import Category, Product

DATAFILE_FOR_BD = 'data.json'


def read_json():  # читает JSON
    with open(DATAFILE_FOR_BD) as file:
        return load(file)


class Command(BaseCommand):

    def handle(self, *args, **options):

        bd_fill_data = read_json()  # чтение JSON с данными

        Product.objects.all().delete()  # очистка таблицы
        Category.objects.all().delete()  # очистка таблицы

        category_to_create = []  # список для хранения объектов category
        category_pk_to_name_map = []  # список для хранения пар pk-name

        for item in bd_fill_data:
            if 'category' in item['model']:  # выборка данных для category
                category_to_create.append(Category(**item['fields']))  # добавление к списку
                category_pk_to_name_map.append({item['pk']: item['fields']['name']})  # добавление пар pk-name
        Category.objects.bulk_create(category_to_create)  # наполнение таблицы БД

        product_to_create = []  # список для хранения объектов product

        for item in bd_fill_data:
            if 'product' in item['model']:  # выборка данных для product
                category_pk = item['fields']['category']  # чтение pk
                for unit in category_pk_to_name_map:  # поиск name для pk
                    if unit.get(category_pk): break
                # добавление экземпляра category вместо pk в данные для создания экземпляра product
                item['fields']['category'] = Category.objects.get(name=unit[category_pk])
                product_to_create.append(Product(**item['fields']))  # добавление к списку
        Product.objects.bulk_create(product_to_create)  # наполнение таблицы БД

        # os.system('manage.py loaddata data.json') - другой вариант наполнения БД
