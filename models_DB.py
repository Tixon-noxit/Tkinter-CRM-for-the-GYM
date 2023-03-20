import datetime
from peewee import *

database = SqliteDatabase('organization.db')

class BaseModel(Model):
    class Meta:
        database = database


class Client(BaseModel): # Клиент
    id = PrimaryKeyField(null=False)
    First_Name = CharField(max_length=100)
    Last_Name = CharField(max_length=100)
    Phone_number = CharField(max_length=12)
    create_date = DateTimeField(default=datetime.datetime.now)       

class Contact(BaseModel): # Контакты
    id = PrimaryKeyField(null=False)
    First_Name = CharField(max_length=100)
    Last_Name = CharField(max_length=100)
    Phone_number = CharField(max_length=12)
    Type = CharField()
    Source = CharField() # Источник
    create_date = DateTimeField(default=datetime.datetime.now)

class Trener(BaseModel): # Тренеры
    id = PrimaryKeyField(null=False)
    First_Name = CharField(max_length=100) # Фамилия
    Last_Name = CharField(max_length=100) # Имя
    Phone_number = CharField(max_length=12) # Номер телефона
    Type = CharField() # Тип
    Source = CharField() # Источник
    create_date = DateTimeField(default=datetime.datetime.now)

class Staff(BaseModel): # Административный персонал
    id = PrimaryKeyField(null=False)
    First_Name = CharField(max_length=100) # Фамилия
    Last_Name = CharField(max_length=100) # Имя
    Phone_number = CharField(max_length=12) # Номер телефона
    Type = CharField() # Тип
    Source = CharField() # Источник
    create_date = DateTimeField(default=datetime.datetime.now) # Дата создания      

class Warehouse(BaseModel): # Товары на складе
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=255) # Название позиции
    description = TextField() # Описание позиции
    unit = CharField() # Единица измерения
    purchase_price = CharField(max_length=6) # Цена в закупке
    retail_price = CharField(max_length=6) # Розничная цена
    quantity = CharField(max_length=6) # Кол-во штук
    reserved = CharField(max_length=6) # Зарезервировано
    create_date = DateTimeField(default=datetime.datetime.now) 

class Service(BaseModel): # Услуги
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=255) # Наименование
    description = TextField() # Описание услуги
    retail_price = CharField(max_length=6) # Розничная цена
    quantity = CharField(max_length=6) # Кол-во штук
    create_date = DateTimeField(default=datetime.datetime.now) 

class Lid(BaseModel): # Лид
    id = PrimaryKeyField(null=False)
    name = CharField() # Имя
    telephone_number = CharField(max_length=12) # Номер телефона
    create_date = DateTimeField(default=datetime.datetime.now) # Дата создания
    Source = CharField() # Источник
    responsible = CharField() # Ответственный - Изменить на зависимость от Сотрудников
    comment = TextField() # Коментарии
    status = CharField() # Статус

class Deal(BaseModel): # Сделки
    id = PrimaryKeyField(null=False)
    summ = CharField(max_length=7)
    stady = CharField(max_length=255)
    create_date = DateTimeField(default=datetime.datetime.now)    
    # client = CharField() # Изменить на зависимость от Contact
    client_first_name = CharField() # Фамилия
    client_last_name = CharField() # Имя
    tip = CharField() # Тип
    source = CharField() # Источник
    date_the_start = DateTimeField(default=datetime.datetime.now)
    responsible = CharField() # Изменить на зависимость от Сотрудников
    comment = TextField()
    # ТОВАРЫ - надо как-то прилепить
    
    # class Lockers(BaseModel): # Шкафчики
#     id = PrimaryKeyField(null=False)
#     Name = CharField(max_length=7)
#     sum_lockers INTEGER = CharField(max_length=7)
#     paid_before DATE = CharField(max_length=7)
#     telephone_number = CharField(max_length=7)
#     comments = CharField(max_length=7)
#     status = CharField(max_length=7) 
