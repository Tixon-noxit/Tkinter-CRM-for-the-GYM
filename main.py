from tkinter import * 
from tkinter import Menu, ttk, messagebox 
import tkinter as tk
from tkinter.ttk import Combobox
from tkcalendar import Calendar, DateEntry 
import sqlite3
from peewee import *
from ttkwidgets.autocomplete import AutocompleteCombobox
from views import clear_widget, new_contact, close_window, new_deal, new_trener, new_staff, new_warehouse, new_services, new_new_applications, clock # search_for_table
from views import TableSearch, TableInteraction

# Data Base
from models_DB import *

Contact.create_table()
Deal.create_table()
Trener.create_table()
Staff.create_table()
Warehouse.create_table()
Service.create_table()
Client.create_table()
Lid.create_table()

from datetime import timedelta, datetime

# Парсер заявок
from mail.postal_data import MAIL, PASSWORD, PASSWORD_MAIL_APP  # Отредактировать данные в файле
import getpass
import imaplib
from html.parser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc
import email


""" Битрикс24 => Клиенты """
""" При нажатии на Enter активировать сохранение формы """

ADMIN = 'Тихон'

# Стилистические переменные
from settings.settings import *

color_label_menu = color_frame_menu

###-------------------------------------------------------------------------------------------------------------------------------------------------####

# Основное окно

window = Tk()
window.title(LABLE)
window.resizable(False, False)
style = ttk.Style(window)
style.configure("vista")
window.state('zoomed')  
menu = Menu(window)
window.config(menu=menu)

###-------------------------------------------------------------------------------------------------------------------------------------------------####
# Адаптивность - Данный модуль под вопросом
width = window.winfo_screenwidth()  # Ширина окна
height = window.winfo_screenheight()  # Высота окна

###-------------------------------------------------------------------------------------------------------------------------------------------------####
# Если фокус на окне то обновлять окно каждые 2 секунды

def passage_control():
	clear_widget(work_frame)
	frame_passage_control = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_passage_control.pack(side=tk.TOP, fill='both')	
	Button_clients = tk.Button(master=frame_passage_control, text='Добавить')
	Button_clients.pack(side=tk.LEFT)
	# Button_clients2 = tk.Button(master=frame_passage_control, text='Назад', command=clients)
	# Button_clients2.pack(side=tk.LEFT)
	
	check_list = []
	def check_passage():
		TABLE_NAME = 'FB_EVN'
		SELECT = """SELECT FB_EVN.EKEY, FB_KEY_H.USR_FN, FB_EVN.DT from %s 
				    INNER JOIN FB_KEY_H ON FB_KEY_H.ID = FB_EVN.EKEY

				    -- INNER JOIN FB_KEY ON FB_KEY.ID = FB_ENV.EKEY

				    where EXTRACT(YEAR FROM FB_EVN.DT) = EXTRACT(YEAR FROM current_date) 
				    and EXTRACT(MONTH FROM FB_EVN.DT) = EXTRACT(MONTH FROM current_date)
				    and EXTRACT(DAY FROM FB_EVN.DT) = EXTRACT(DAY FROM current_date)
				    order by FB_EVN.DT desc""" % TABLE_NAME

		con = fdb.connect(dsn='C:/Program Files/ENT/Server/DB/CBASE.FDB', user='sysdba', password='masterkey')
		cur_user = con.cursor()

		# try:
			# print('Соединение с БД CBASE.FBD установлено')
		# except:
			# print('Ошибка соединения!')

		cur_user.execute(SELECT)


		# try:
			# print('Успешный вывод данных из FB_USR')
		# except:
			# print('Ошибка вывода данных из FB_USR')


			
		user = cur_user.fetchall()
		data = (row for row in user)
		monitor = fdb.monitor.Monitor()
		monitor.bind(con)
		monitor.db.name
		for row in data:
			check_list.append(row)

	if check_list == []:
		check_passage()
		# print('Список проходов пуст!')
	else:
		pass
		print(check_list)
			


	headings = (
		'Карта',
		'ФИО',
		'Дата посещения',
		'Активен до:',)

	table = ttk.Treeview(work_frame, show="headings", selectmode="browse", height=100)
	table["columns"] = headings
	table["displaycolumns"] = headings

	for head in headings:
		table.heading(head, text=head, anchor=tk.CENTER)
		table.column(head, anchor=tk.CENTER)

	rows = data
	
	for row in check_list:
		table.insert('', tk.END, values=tuple(row))

	scrolltable = tk.Scrollbar(work_frame, command=table.yview)
	table.configure(yscrollcommand=scrolltable.set)
	scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
	# table.pack(fill=tk.BOTH)
	table.pack(side=TOP)

	left = Label(frame_passage_control, text=f'Клиентов сегодня: {len(set(check_list))}')
	left.pack(side=tk.LEFT)
	
	# TableSearch(frame_passage_control, tree_passage_control, Contact, 'Контакт', passage_control)

	# # Взаимодействие с таблицей
	# def item_selected(event):
	# 	TableInteraction(frame_passage_control, passage_control)

	# tree_passage_control.bind("<ButtonPress-3>", item_selected)
	# tree_passage_control.bind("<Return>", item_selected)
	


###-------------------------------------------------------------------------------------------------------------------------------------------------####

def create_contact():
	clear_widget(work_frame)
	frame_contact = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_contact.pack(side=tk.TOP, fill='both')

	labelframe = LabelFrame(frame_contact, text="Новый контакт")
	labelframe.pack(fill="both", expand="yes")
 
	labelwork_frame = LabelFrame(labelframe, text="О контакте")
	labelwork_frame.pack(fill="both", expand="yes") 

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Фамилия")
	left.pack(side='left')
	entry_1 = Entry(frame, width=50)
	entry_1.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Имя")
	left.pack(side='left')
	entry_2 = Entry(frame, width=50)
	entry_2.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Телефон")
	left.pack(side='left')
	entry_3 = Entry(frame, width=50)
	entry_3.pack(side='right', pady=6, padx=6)

	labelwork_frame = LabelFrame(labelframe, text="Дополнительно")
	labelwork_frame.pack(fill="both", expand="yes") 

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Тип")
	left.pack(side='left')
	languages = ["Клиент", "Поставщик", "Партнер", "Сотрудник"]
	combobox_1 = ttk.Combobox(frame, values=languages, width=48)
	combobox_1.current(0)
	combobox_1.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Источник")
	left.pack(side='left')
	lst = ["Звонок", "Электронная почта", "Веб-сайт", "Реклама", "Существующий клиент", "По рекомендации", "Другое"]
	combobox_2 = ttk.Combobox(frame, values=lst, width=48)
	combobox_2.current(2)
	combobox_2.pack(side='right', pady=6, padx=6)

	labelframe5 = LabelFrame(labelframe, text="Опции")
	labelframe5.pack(fill="both", expand="yes")
	frame = tk.Frame(labelframe5)
	frame.pack(side='top')

	Button_deal = tk.Button(master=frame, text='Сохранить', command=lambda: new_contact(entry_1.get(),entry_2.get(),entry_3.get(),combobox_1.get(),combobox_2.get(),frame_contact, contacts))
	Button_deal.pack(side=tk.LEFT)
	Button_deal2 = tk.Button(master=frame, text='Отмена', command=lambda: close_window(frame_contact, contacts))
	Button_deal2.pack(side=tk.RIGHT)


def contacts():
	clear_widget(work_frame)
	frame_contacts = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_contacts.pack(side=tk.TOP, fill='both')	
	Button_clients = tk.Button(master=frame_contacts, text='Добавить', command=create_contact)
	Button_clients.pack(side=tk.LEFT)
	Button_clients2 = tk.Button(master=frame_contacts, text='Назад', command=clients)
	Button_clients2.pack(side=tk.LEFT)

	tree_contacts= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column6"), show='headings')
	tree_contacts.heading("#1", text="id")
	tree_contacts.column("#1", minwidth=40, width=40)
	tree_contacts.heading("#2", text="Фамилия")
	tree_contacts.heading("#3", text="Имя")
	tree_contacts.heading("#4", text="Телефон")
	tree_contacts.column("#4", minwidth=80, width=100)
	tree_contacts.heading("#5", text="Тип")
	tree_contacts.column("#5", minwidth=50, width=120)
	tree_contacts.heading("#6", text="Источник")
	tree_contacts.column("#6", minwidth=120, width=150)
	tree_contacts.heading("#7", text="Дата создания")
	tree_contacts.pack(expand=1, anchor=NW, fill="both")

	data = Contact.select().order_by(Contact.create_date)

	for row in data:
		tree_contacts.insert("", tk.END, values=[row.id, row.First_Name, row.Last_Name, row.Phone_number, row.Type, row.Source, row.create_date])
	
	TableSearch(frame_contacts, tree_contacts, Contact, 'Контакт', contacts)

	# Взаимодействие с таблицей
	def item_selected(event):
		TableInteraction(frame_contacts, tree_contacts)

	tree_contacts.bind("<ButtonPress-3>", item_selected)
	tree_contacts.bind("<Return>", item_selected)	


def provider(): # Окно поставщиков
	clear_widget(work_frame)
	frame_provider = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_provider.pack(side=tk.TOP, fill='both')	
	Button_clients = tk.Button(master=frame_provider, text='Добавить', command=create_contact)
	Button_clients.pack(side=tk.LEFT)
	Button_clients2 = tk.Button(master=frame_provider, text='Назад', command=clients)
	Button_clients2.pack(side=tk.LEFT)

	tree_provider= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column6"), show='headings')
	tree_provider.heading("#1", text="id")
	tree_provider.column("#1", minwidth=40, width=40)
	tree_provider.heading("#2", text="Фамилия")
	tree_provider.heading("#3", text="Имя")
	tree_provider.heading("#4", text="Телефон")
	tree_provider.column("#4", minwidth=80, width=100)
	tree_provider.heading("#5", text="Тип")
	tree_provider.column("#5", minwidth=50, width=120)
	tree_provider.heading("#6", text="Источник")
	tree_provider.column("#6", minwidth=120, width=150)
	tree_provider.heading("#7", text="Дата создания")
	tree_provider.pack(expand=1, anchor=NW, fill="both")

	data = Contact.select().where(Contact.Type == 'Поставщик')

	for row in data:
		tree_provider.insert("", tk.END, values=[row.id, row.First_Name, row.Last_Name, row.Phone_number, row.Type, row.Source, row.create_date])	
	TableSearch(frame_provider, tree_provider, Contact, 'Поставщик', provider)

	# Взаимодействие с таблицей
	def item_selected(event):
		TableInteraction(frame_provider, tree_provider)

	tree_provider.bind("<ButtonPress-3>", item_selected)
	tree_provider.bind("<Return>", item_selected)

def clients():
	clear_widget(work_frame)
	frame_clients = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_clients.pack(side=tk.TOP, fill='both')	
	Button_clients = tk.Button(master=frame_clients, text='Контакты', command=contacts)
	Button_clients.pack(side=tk.LEFT)
	Button_clients2 = tk.Button(master=frame_clients, text='Поставщики', command=provider)
	Button_clients2.pack(side=tk.LEFT)
	
	tree_clients= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4"), show='headings')
	tree_clients.heading("#1", text="id")
	tree_clients.column("#1", minwidth=20, width=30)
	tree_clients.heading("#2", text="Фамилия")
	tree_clients.heading("#3", text="Имя")
	tree_clients.heading("#4", text="Телефон")
	tree_clients.column("#4", minwidth=50, width=120)
	tree_clients.pack(expand=1, anchor=NW, fill="both")

	data = Contact.select().where(Contact.Type=='Клиент').order_by(Contact.create_date.desc())

	for row in data:
		tree_clients.insert("", tk.END, values=[row.id, row.First_Name, row.Last_Name, row.Phone_number, row.Type, row.Source, row.create_date])
	TableSearch(frame_clients, tree_clients, Contact, 'Клиент', clients)	

	# Взаимодействие с таблицей
	def item_selected(event):
		TableInteraction(frame_clients, tree_clients)

	tree_clients.bind("<ButtonPress-3>", item_selected)
	tree_clients.bind("<Return>", item_selected)

###-------------------------------------------------------------------------------------------------------------------------------------------------####

def create_deal():
	clear_widget(work_frame)
	frame_create_deal = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_create_deal.pack(side=tk.TOP, fill='both')

	labelframe = LabelFrame(frame_create_deal, text="Новая Сделка")
	labelframe.pack(fill="both", expand="yes")
 
	labelwork_frame = LabelFrame(labelframe, text="О сделке")
	labelwork_frame.pack(fill="both", expand="yes") 

	frame = tk.Frame(labelwork_frame)
	frame.pack()
	left = Label(frame, text="Сумма")
	left.pack(side='left')
	summ_entr = ttk.Entry(frame, width=50)
	summ_entr.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack()
	left = Label(frame, text="Стадия ")
	left.pack(side='left')
	languages = ["Новая", "Подготовка Документов", "Счёт на предоплату", "В работе", "Финальный счет", 
				"Сделка успешна", "Сделка провалена", "Анализ причины провала"]
	combobox_st = ttk.Combobox(frame, values=languages, width=48)
	combobox_st.current(0)
	combobox_st.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(side='left', padx=15)
	left = Label(frame, text="Дата    ")
	left.pack(side='left')
	cal_date = DateEntry(frame, width=12, background='darkblue', locale='ru_RU',
					foreground='white', borderwidth=2, year=2023)
	cal_date.pack(padx=10, pady=10)

	countries =	[]

	for cl in Contact.select():
		countries.append(f'{cl.First_Name} {cl.Last_Name}')

	def check_input(event):
		value = event.widget.get()
		data = []

		if len(event.keysym) == 1:
			event.widget.autocomplete()

		if value == '':
			combobox_cont['values'] = countries
		else:
			data = []
		for item in countries:
			if value.lower() in item[0:len(value)].lower():
				data.append(item)
		combobox_cont['values'] = data	

	labelwork_frame = LabelFrame(labelframe, text="Клиент")
	labelwork_frame.pack(fill="both", expand="yes")

	left = Label(labelwork_frame, text="Контакт")
	left.pack()
	combobox_cont = AutocompleteCombobox(labelwork_frame, width=30, completevalues=countries)
	combobox_cont.bind('<KeyRelease>', check_input)
	combobox_cont.pack(side=tk.RIGHT)


	Button_deal = tk.Button(master=labelwork_frame, text='Создать Контакт', command=create_contact)
	Button_deal.pack(side=tk.LEFT)

	labelframe3 = LabelFrame(labelframe, text="Дополнительно")
	labelframe3.pack(fill="both", expand="yes")

	frame = tk.Frame(labelframe3)
	frame.pack(side='top', padx=15)
	left = Label(frame, text="Тип сделки")
	left.pack(side='left')
	languages = ["Продажа", "Не выбран", "Комплексная продажа", "Продажа товара", "Продажа услуги"]
	combobox_tip = ttk.Combobox(frame, values=languages, width=48)
	combobox_tip.current(4)
	combobox_tip.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelframe3)
	frame.pack(side='top')
	left = Label(frame, text="Источник")
	left.pack(side='left')
	languages = ["Звонок", "Электронная почта", "Веб-сайт", "Реклама", "Существующий клиент", "По рекомендации", "Другое"]
	combobox_source = ttk.Combobox(frame, values=languages, width=48)
	combobox_source.current(2)
	combobox_source.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelframe3)
	frame.pack(side='top')
	left = Label(frame, text="Дата начала")
	left.pack(side='left')
	cal_start = DateEntry(frame, width=12, background='darkblue', locale='ru_RU',
					foreground='white', borderwidth=2, year=2023)
	cal_start.pack(padx=10, pady=10)

	frame = tk.Frame(labelframe3)
	frame.pack(side='top')
	left = Label(frame, text="Комментарии")
	left.pack(side='left')
	comment_entry = tk.Entry(frame, width=60)
	comment_entry.pack(padx=8, pady= 8)

	labelframe4 = LabelFrame(labelframe, text="Товары")
	labelframe4.pack(fill="both", expand="yes")
	Button_deal = tk.Button(master=labelframe4, text='Добавить +')
	Button_deal.pack(side=tk.LEFT)

	labelframe4 = LabelFrame(labelframe, text="Услуги")
	labelframe4.pack(fill="both", expand="yes") 
	Button_deal = tk.Button(master=labelframe4, text='Добавить +')
	Button_deal.pack(side=tk.LEFT)

	labelframe5 = LabelFrame(labelframe, text="Опции")
	labelframe5.pack(fill="both", expand="yes")
	frame = tk.Frame(labelframe5)
	frame.pack(side='top')
	
	frame.bind('<Return>', Button_deal)	
	Button_deal = tk.Button(master=frame, text='Сохранить', command=lambda: new_deal(summ_entr.get(), combobox_st.get(), cal_date.get(), 
															combobox_cont.get(), combobox_tip.get(), combobox_source.get(), cal_start.get(), 
															ADMIN, comment_entry.get(), frame_create_deal, history_deal))
	Button_deal.pack(side=tk.LEFT)
	Button_deal2 = tk.Button(master=frame, text='Отмена', command=lambda: close_window(frame_create_deal, history_deal))
	Button_deal2.pack(side=tk.RIGHT)

	# При нажатии на Enter Сохранять сделку

def history_deal():
	clear_widget(work_frame)
	
	frame_history_deal = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_history_deal.pack(side=tk.TOP, fill='both')
	Button_deal = tk.Button(master=frame_history_deal, text='Создать сделку', command=create_deal)
	Button_deal.pack(side=tk.LEFT)
	Button_deal2 = tk.Button(master=frame_history_deal, text='Назад', command=deal_now)
	Button_deal2.pack(side=tk.LEFT)
	
	tree = ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8", "column9", "column10", "column11"), show ='headings')
	tree.heading("#1", text="id")
	tree.column("#1", minwidth=0, width=20)
	tree.heading("#2", text="Сумма")
	tree.column("#2", minwidth=0, width=50)
	tree.heading("#3", text="Стадия")
	tree.column("#3", minwidth=0, width=120)
	tree.heading("#4", text="Дата")
	tree.column("#4", minwidth=0, width=65)
	tree.heading("#5", text="Фамилия")
	tree.column("#5", minwidth=0, width=120)
	tree.heading("#6", text="Имя")
	tree.column("#6", minwidth=0, width=120)
	tree.heading("#7", text="Тип")
	tree.column("#7", minwidth=0, width=120)
	tree.heading("#8", text="Источник")
	tree.column("#8", minwidth=0, width=150)
	tree.heading("#9", text="Дата начала")
	tree.column("#9", minwidth=0, width=80)
	tree.heading("#10", text="Ответственный")
	tree.column("#10", minwidth=0, width=120)
	tree.heading("#11", text="Комментарии")
	tree.column("#11", minwidth=0, width=170)
	tree.pack(expand=1, anchor=N, fill="both")
	table_deal = Deal.select().order_by(Deal.create_date)
	for t in table_deal:
		tree.insert("", tk.END, values=(t.id, t.summ, t.stady, t.create_date, 
										t.client_first_name, t.client_last_name, 
										t.tip, t.source, t.date_the_start, 
										t.responsible, t.comment))
	# Поиск по таблице
	TableSearch(frame_history_deal, tree, Deal, 'Старые', history_deal)

	def item_selected(event):
		TableInteraction(frame_history_deal, tree)

	tree.bind("<ButtonPress-3>", item_selected)
	tree.bind("<Return>", item_selected)


def deal_now():
	clear_widget(work_frame)
	
	frame_deal_now = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_deal_now.pack(side=tk.TOP, fill='both')
	Button_deal = tk.Button(master=frame_deal_now, text='Создать сделку', command=create_deal)
	Button_deal.pack(side=tk.LEFT)
	Button_deal2 = tk.Button(master=frame_deal_now, text='История продаж', command=history_deal)
	Button_deal2.pack(side=tk.LEFT)

	tree_deal_now = ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8", "column9", "column10", "column11"), show ='headings')
	tree_deal_now.heading("#1", text="id")
	tree_deal_now.column("#1", minwidth=0, width=20)
	tree_deal_now.heading("#2", text="Сумма")
	tree_deal_now.column("#2", minwidth=0, width=50)
	tree_deal_now.heading("#3", text="Стадия")
	tree_deal_now.column("#3", minwidth=0, width=120)
	tree_deal_now.heading("#4", text="Дата")
	tree_deal_now.column("#4", minwidth=0, width=65)
	tree_deal_now.heading("#5", text="Фамилия")
	tree_deal_now.column("#5", minwidth=0, width=120)
	tree_deal_now.heading("#6", text="Имя")
	tree_deal_now.column("#6", minwidth=0, width=120)
	tree_deal_now.heading("#7", text="Тип")
	tree_deal_now.column("#7", minwidth=0, width=120)
	tree_deal_now.heading("#8", text="Источник")
	tree_deal_now.column("#8", minwidth=0, width=150)
	tree_deal_now.heading("#9", text="Дата начала")
	tree_deal_now.column("#9", minwidth=0, width=80)
	tree_deal_now.heading("#10", text="Ответственный")
	tree_deal_now.column("#10", minwidth=0, width=120)
	tree_deal_now.heading("#11", text="Комментарии")
	tree_deal_now.column("#11", minwidth=0, width=170)
	tree_deal_now.pack(expand=1, anchor=N, fill="both")
	now = datetime.now().strftime("%d.%m.%Y")
	table_deal = Deal.select().where(Deal.create_date == now)
	for t in table_deal:
		tree_deal_now.insert("", tk.END, values=(t.id, t.summ, t.stady, t.create_date, 
										t.client_first_name, t.client_last_name, 
										t.tip, t.source, t.date_the_start, 
										t.responsible, t.comment))

	# Поиск по таблице
	TableSearch(frame_deal_now, tree_deal_now, Deal, 'Новые', deal_now)

	# Взаимодействие с таблицей
	def item_selected(event):
		TableInteraction(frame_deal_now, tree_deal_now)

	tree_deal_now.bind("<ButtonPress-3>", item_selected)
	tree_deal_now.bind("<Return>", item_selected)

"""---------------------МОЖНО ЛИ С ЭТИМ ЧТО-ТО СДЕЛАТЬ?------------------------------------------------------------------------------------------------------ """
	# Взаимодействие с таблицей
	# def item_selected(event): # Выделение фрагмента таблицы
	# 	def createNewWindow(arg):
	# 		# Файл лого для окон
	# 		# logo = 'Images/boxing.ico'
	# 		newWindow = Toplevel(frame_deal)
	# 		# labelExample = tk.Label(newWindow, text = arg[4])
	# 		newWindow.geometry('500x360+380+200')
	# 		# newWindow.iconbitmap(logo)
	# 		newWindow.title('Информация о сделке')
	# 		newWindow.resizable(False, False)
	# 		newWindow.focus_force()
	# 		newWindow.grab_set()


	# 		deal_var = Deal.get(Deal.id == arg[0])
			
	# 		label_name = Label(newWindow, text = "id")
	# 		label_name.place(x=100, y=37, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	# 		label_name = Label(newWindow, text = deal_var.id)
	# 		label_name.place(x=150, y=37, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
	# 		labeljob = Label(newWindow, text = "Сумма:")
	# 		labeljob.place(x=100, y=67, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	# 		labeljob = Label(newWindow, text = deal_var.summ)
	# 		labeljob.place(x=150, y=67, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
	# 		labelnum = Label(newWindow, text = "Стадия:")
	# 		labelnum.place(x=100, y=97, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	# 		labelnum = Label(newWindow, text = deal_var.stady)
	# 		labelnum.place(x=150, y=97, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
	# 		labelnum1 = Label(newWindow, text = "Создана:")
	# 		labelnum1.place(x=100, y=127, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	# 		labelnum1 = Label(newWindow, text = deal_var.create_date)
	# 		labelnum1.place(x=150, y=127, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
	# 		labelnum2 = Label(newWindow, text = "Клиент:")
	# 		labelnum2.place(x=100, y=157, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	# 		labelnum2t = Label(newWindow, text = f'{deal_var.client_first_name} {deal_var.client_last_name}')
	# 		labelnum2t.place(x=150, y=157, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
	# 		labelnum3 = Label(newWindow, text = "Тип:")
	# 		labelnum3.place(x=100, y=187, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	# 		labelnum3 = Label(newWindow, text = deal_var.tip)
	# 		labelnum3.place(x=150, y=187, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
	# 		labelnum4 = Label(newWindow, text = "Источник:")
	# 		labelnum4.place(x=100, y=217, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	# 		labelnum4 = Label(newWindow, text = deal_var.source)
	# 		labelnum4.place(x=150, y=217, anchor="w", height=20, width=200, bordermode=OUTSIDE)

	# 		labelnum5 = Label(newWindow, text = "Дата начала:")
	# 		labelnum5.place(x=100, y=247, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	# 		labelnum5 = Label(newWindow, text = deal_var.date_the_start)
	# 		labelnum5.place(x=150, y=247, anchor="w", height=20, width=200, bordermode=OUTSIDE)

	# 		labelnum6 = Label(newWindow, text = "Ответственный:")
	# 		labelnum6.place(x=100, y=277, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	# 		labelnum6 = Label(newWindow, text = deal_var.responsible)
	# 		labelnum6.place(x=150, y=277, anchor="w", height=20, width=200, bordermode=OUTSIDE)

	# 		labelnum7 = Label(newWindow, text = "Комментарий:")
	# 		labelnum7.place(x=100, y=307, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	# 		labelnum7 = Label(newWindow, text = deal_var.comment)
	# 		labelnum7.place(x=150, y=307, anchor="w", height=20, width=200, bordermode=OUTSIDE)

	# 		# Кнопки окна истории шкафчика
	# 		btn_history = Button(newWindow, text="Клиент", 
	# 				        	width=10, height=1, anchor="n")  # , command = lambda: history(arg,arg2)
	# 		btn_history.place(relx=0.60, y=337, anchor="e")
		
	# 		btn_change = Button(newWindow, text="Изменить", 
	# 				        	width=10, height=1, anchor="n")  # , command = lambda: change(arg,arg2)
	# 		btn_change.place(relx=0.78, y=337, anchor="e")
		
	# 		btn_change = Button(newWindow, text="Удалить", 
	# 				        	width=10, height=1, anchor="n")  # , command = delete_locker
	# 		btn_change.place(relx=0.96, y=337, anchor="e")

	# 	# Получение значений выбранной строки таблицы					
	# 	selected_people = ""																	
	# 	for selected_item in tree_deal_now.selection():									
	# 		item = tree_deal_now.item(selected_item)									
	# 		selected_people = item["values"]
	# 	createNewWindow(selected_people)

	# tree_deal_now.bind("<ButtonPress-3>", item_selected)
###-------------------------------------------------------------------------------------------------------------------------------------------------####
 
def create_trener():
	clear_widget(work_frame)
	frame_treners = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_treners.pack(side=tk.TOP, fill='both')

	labelframe = LabelFrame(frame_treners, text="Новый Тренер")
	labelframe.pack(fill="both", expand="yes")
 
	labelwork_frame = LabelFrame(labelframe, text="О Тренере")
	labelwork_frame.pack(fill="both", expand="yes") 

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Фамилия")
	left.pack(side='left')
	entry_1 = Entry(frame, width=50)
	entry_1.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Имя")
	left.pack(side='left')
	entry_2 = Entry(frame, width=50)
	entry_2.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Телефон")
	left.pack(side='left')
	entry_3 = Entry(frame, width=50)
	entry_3.pack(side='right', pady=6, padx=6)

	labelwork_frame = LabelFrame(labelframe, text="Дополнительно")
	labelwork_frame.pack(fill="both", expand="yes") 

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Тип")
	left.pack(side='left')
	tip_trn = ["Бокс", "Тайский бокс", "ММА", "Фитбокс"]
	combobox_trn = ttk.Combobox(frame, values=tip_trn, width=48)
	combobox_trn.current(0)
	combobox_trn.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Источник")
	left.pack(side='left')
	lst = ["Звонок", "Электронная почта", "Веб-сайт", "Реклама", "Существующий тренер", "По рекомендации", "Другое"]
	combobox_2 = ttk.Combobox(frame, values=lst, width=48)
	combobox_2.current(2)
	combobox_2.pack(side='right', pady=6, padx=6)

	labelframe5 = LabelFrame(labelframe, text="Опции")
	labelframe5.pack(fill="both", expand="yes")
	frame = tk.Frame(labelframe5)
	frame.pack(side='top')

	Button_deal = tk.Button(master=frame, text='Сохранить', command=lambda: new_trener(entry_1.get(), entry_2.get(), 
																		entry_3.get(), combobox_trn.get(), combobox_2.get(), frame_treners, treners))
	Button_deal.pack(side=tk.LEFT)
	Button_deal2 = tk.Button(master=frame, text='Отмена', command=lambda: clear_widget(work_frame))
	Button_deal2.pack(side=tk.RIGHT)


def treners():
	clear_widget(work_frame)
	frame_treners = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_treners.pack(side=tk.TOP, fill='both')	
	Button_clients = tk.Button(master=frame_treners, text='Добавить', command=create_trener)
	Button_clients.pack(side=tk.LEFT)
	
	tree_treners= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"), show='headings')
	tree_treners.heading("#1", text="id")
	tree_treners.column("#1", minwidth=40, width=50)
	tree_treners.heading("#2", text="Фамилия")
	tree_treners.heading("#3", text="Имя")
	tree_treners.heading("#4", text="Телефон")
	tree_treners.column("#4", minwidth=80, width=110)
	tree_treners.heading("#5", text="Дисциплина")
	tree_treners.heading("#6", text="Тип")
	tree_treners.heading("#7", text="Дата внесения")
	tree_treners.pack(expand=1, anchor=NW, fill="both")
	data = Trener.select()
	for row in data:
		tree_treners.insert("", tk.END, values=[row.id, row.First_Name, row.Last_Name, row.Phone_number, row.Type, row.Source, row.create_date])
	
	# Поиск по таблице
	TableSearch(frame_treners, tree_treners, Trener, 'First_Name', treners)

	# Взаимодействие с таблицей
	def item_selected(event):
		TableInteraction(frame_treners, tree_treners)

	tree_treners.bind("<ButtonPress-3>", item_selected)
	tree_treners.bind("<Return>", item_selected)

###-------------------------------------------------------------------------------------------------------------------------------------------------####

def create_staff():
	clear_widget(work_frame)
	frame_create_staff = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_create_staff.pack(side=tk.TOP, fill='both')

	labelframe = LabelFrame(frame_create_staff, text="Новый Тренер")
	labelframe.pack(fill="both", expand="yes")
 
	labelwork_frame = LabelFrame(labelframe, text="О Тренере")
	labelwork_frame.pack(fill="both", expand="yes") 

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Фамилия")
	left.pack(side='left')
	entry_1 = Entry(frame, width=50)
	entry_1.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Имя")
	left.pack(side='left')
	entry_2 = Entry(frame, width=50)
	entry_2.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Телефон")
	left.pack(side='left')
	entry_3 = Entry(frame, width=50)
	entry_3.pack(side='right', pady=6, padx=6)

	labelwork_frame = LabelFrame(labelframe, text="Дополнительно")
	labelwork_frame.pack(fill="both", expand="yes") 

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Тип")
	left.pack(side='left')
	tip_trn = ["Администратор", "Старший администратор", "Технический администратор"]
	combobox_adm = ttk.Combobox(frame, values=tip_trn, width=48)
	combobox_adm.current(0)
	combobox_adm.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Источник")
	left.pack(side='left')
	lst = ["Звонок", "Электронная почта", "Веб-сайт", "Реклама", "Существующий сотрудник", "По рекомендации", "Другое"]
	combobox_2 = ttk.Combobox(frame, values=lst, width=48)
	combobox_2.current(2)
	combobox_2.pack(side='right', pady=6, padx=6)

	labelframe5 = LabelFrame(labelframe, text="Опции")
	labelframe5.pack(fill="both", expand="yes")
	frame = tk.Frame(labelframe5)
	frame.pack(side='top')

	Button_save = tk.Button(master=frame, text='Сохранить', command=lambda: new_staff(entry_1.get(),entry_2.get(),
															entry_3.get(),combobox_adm.get(),combobox_2.get(), frame_create_staff, staff))
	Button_save.pack(side=tk.LEFT)
	Button_cansel = tk.Button(master=frame, text='Отмена', command=lambda: clear_widget(work_frame))
	Button_cansel.pack(side=tk.RIGHT)



def staff():
	clear_widget(work_frame)
	frame_staff = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_staff.pack(side=tk.TOP, fill='both')	
	Button_staff = tk.Button(master=frame_staff, text='Добавить', command=create_staff)
	Button_staff.pack(side=tk.LEFT)

	tree_staff = ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"), show='headings')
	tree_staff.heading("#1", text="id")
	tree_staff.column("#1", minwidth=40, width=50)
	tree_staff.heading("#2", text="Фамилия")
	tree_staff.heading("#3", text="Имя")
	tree_staff.heading("#4", text="Телефон")
	tree_staff.column("#4", minwidth=80, width=110)
	tree_staff.heading("#5", text="Тип")
	tree_staff.heading("#6", text="Внес")
	tree_staff.heading("#7", text="Дата внесения")
	tree_staff.pack(expand=1, anchor=NW, fill="both")
	data = Staff.select()
	for row in data:
		tree_staff.insert("", tk.END, values=[row.id, row.First_Name, row.Last_Name, row.Phone_number, row.Type, row.Source, row.create_date])

	# Поиск по таблице	
	TableSearch(frame_staff, tree_staff, Staff, 'First_Name', staff)

	# Взаимодействие с таблицей
	def item_selected(event):
		TableInteraction(frame_staff, tree_staff)

	tree_staff.bind("<ButtonPress-3>", item_selected)
	tree_staff.bind("<Return>", item_selected)
###-------------------------------------------------------------------------------------------------------------------------------------------------####

def create_warehous():
	clear_widget(work_frame)
	frame_warehous = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_warehous.pack(side=tk.TOP, fill='both')

	labelframe = LabelFrame(frame_warehous, text="Новый товар")
	labelframe.pack(fill="both", expand="yes")
 
	labelwork_frame = LabelFrame(labelframe, text="О товаре")
	labelwork_frame.pack(fill="both", expand="yes") 

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Наименование")
	left.pack(side='left')
	entry_name = Entry(frame, width=50)
	entry_name.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Описание")
	left.pack(side='left')
	entry_description = Entry(frame, width=50)
	entry_description.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Ед.измерения")
	left.pack(side='left')
	lst = ["Штука", "Килограмм", "Грамм", "Литр", "Метр"]
	combobox_unit = ttk.Combobox(frame, values=lst, width=48)
	combobox_unit.current(0)
	combobox_unit.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Цена в закупке")
	left.pack(side='left')
	entry_purchase_price = Entry(frame, width=50)
	entry_purchase_price.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Розничная цена")
	left.pack(side='left')
	entry_retail_price = Entry(frame, width=50)
	entry_retail_price.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Количество")
	left.pack(side='left')
	entry_quantity = Entry(frame, width=50)
	entry_quantity.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Зарезервировано")
	left.pack(side='left')
	entry_reserved = Entry(frame, width=50)
	entry_reserved.pack(side='right', pady=6, padx=6)


	labelframe5 = LabelFrame(labelframe, text="Опции")
	labelframe5.pack(fill="both", expand="yes")
	frame = tk.Frame(labelframe5)
	frame.pack(side='top')
	
	Button_deal = tk.Button(master=frame, text='Сохранить', command=lambda: new_warehouse(entry_name.get(),entry_description.get(),combobox_unit.get(),entry_purchase_price.get(),
																							entry_retail_price.get(), entry_quantity.get(), entry_reserved.get(), frame_warehous, warehouse))
	Button_deal.pack(side=tk.LEFT)
	Button_deal2 = tk.Button(master=frame, text='Отмена', command=lambda: close_window(frame_warehous,warehouse))
	Button_deal2.pack(side=tk.RIGHT)	

def warehouse():  # Товар
	clear_widget(work_frame)
	frame_warehouse = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_warehouse.pack(side=tk.TOP, fill='both')
	Button_deal = tk.Button(master=frame_warehouse, text='Добавить товар', command=create_warehous)
	Button_deal.pack(side=tk.LEFT)

	tree_warehouse= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5"), show='headings')
	tree_warehouse.heading("#1", text="id")
	tree_warehouse.column("#1", minwidth=30, width=40)
	tree_warehouse.heading("#2", text="Наименование")
	tree_warehouse.column("#2", minwidth=250, width=550)
	tree_warehouse.heading("#3", text="Розничнвя цена")
	tree_warehouse.column("#3", minwidth=100, width=100)
	tree_warehouse.heading("#4", text="Количество")
	tree_warehouse.column("#4", minwidth=100, width=100)
	tree_warehouse.heading("#5", text="Зарезервировано")
	tree_warehouse.column("#5", minwidth=120, width=120)
	tree_warehouse.pack(expand=1, anchor=NW, fill="both")
	data = Warehouse.select(Warehouse.id, Warehouse.name, Warehouse.retail_price, Warehouse.quantity,Warehouse.reserved)
	for row in data:
		tree_warehouse.insert("", tk.END, values=[row.id, row.name, row.retail_price, row.quantity,row.reserved ])

	# Поиск по таблице	
	TableSearch(frame_warehouse, tree_warehouse, Warehouse, 'name', warehouse)

	# Взаимодействие с таблицей
	def item_selected(event):
		TableInteraction(frame_warehouse, tree_warehouse)

	tree_warehouse.bind("<ButtonPress-3>", item_selected)
	tree_warehouse.bind("<Return>", item_selected)
###-------------------------------------------------------------------------------------------------------------------------------------------------####

def inventory_control(): # Окно Складского учета
	clear_widget(work_frame)
	frame_inventory_control = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_inventory_control.pack(side=tk.TOP, fill='both')
	Button_deal = tk.Button(master=frame_inventory_control, text='Создать оприходование')
	Button_deal['state']='disabled'
	Button_deal.pack(side=tk.LEFT)
	Button_deal2 = tk.Button(master=frame_inventory_control, text='Журнал')
	Button_deal2['state']='disabled'
	Button_deal2.pack(side=tk.LEFT)

	tree_inventory_control= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4",
										"column5", "column6", "column7", "column8"), show='headings')
	tree_inventory_control.heading("#1", text="Название")
	tree_inventory_control.heading("#2", text="Номер документа основания")
	tree_inventory_control.heading("#3", text="Тип")
	tree_inventory_control.heading("#4", text="Статус")
	tree_inventory_control.heading("#5", text="Дата изменения")
	tree_inventory_control.heading("#6", text="Ответственный")
	tree_inventory_control.heading("#7", text="Поставщик")
	tree_inventory_control.heading("#8", text="Сумма")
	tree_inventory_control.pack(expand=1, anchor=NW, fill="both")
	# for row in rows:
	# 	print(row) # it print all records in the database
	# 	tree_inventory_control.insert("", tk.END, values=row)
	# conn.close()

###-------------------------------------------------------------------------------------------------------------------------------------------------####

def create_services():
	clear_widget(work_frame)
	frame_create_services = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_create_services.pack(side=tk.TOP, fill='both')

	labelframe = LabelFrame(frame_create_services, text="Новая услуга")
	labelframe.pack(fill="both", expand="yes")
 
	labelwork_frame = LabelFrame(labelframe, text="Об услуге")
	labelwork_frame.pack(fill="both", expand="yes") 

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Наименование")
	left.pack(side='left')
	entry_name = Entry(frame, width=50)
	entry_name.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Описание")
	left.pack(side='left')
	entry_description = Entry(frame, width=50)
	entry_description.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Розничная цена")
	left.pack(side='left')
	entry_retail_price = Entry(frame, width=50)
	entry_retail_price.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Количество")
	left.pack(side='left')
	entry_quantity = Entry(frame, width=50)
	entry_quantity.pack(side='right', pady=6, padx=6)

	labelframe5 = LabelFrame(labelframe, text="Опции")
	labelframe5.pack(fill="both", expand="yes")
	frame = tk.Frame(labelframe5)
	frame.pack(side='top')
	
	Button_deal = tk.Button(master=frame, text='Сохранить', command=lambda: new_services(entry_name.get(), entry_description.get(),entry_retail_price.get(),
																			entry_quantity.get(),frame_create_services, services))
	Button_deal.pack(side=tk.LEFT)
	Button_deal2 = tk.Button(master=frame, text='Отмена', command=lambda: close_window(frame_create_services, services))
	Button_deal2.pack(side=tk.RIGHT)



def services():
	clear_widget(work_frame)
	frame_services = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_services.pack(side=tk.TOP, fill='both')
	Button_deal = tk.Button(master=frame_services, text='Добавить Услугу', command=create_services)
	Button_deal.pack(side=tk.LEFT)

	tree_services = ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4"), show='headings')
	tree_services.heading("#1", text="id")
	tree_services.column("#1", minwidth=30, width=40)
	tree_services.heading("#2", text="Наименование")
	tree_services.column("#2", minwidth=250, width=550)
	tree_services.heading("#3", text="Розничнвя цена")
	tree_services.column("#3", minwidth=100, width=100)
	tree_services.heading("#4", text="Количество")
	tree_services.column("#4", minwidth=100, width=100)
	tree_services.pack(expand=1, anchor=E, fill="both")
	data = Service.select(Service.id, Service.name, Service.retail_price, Service.quantity)
	for row in data:
		tree_services.insert("", tk.END, values=[row.id, row.name, row.retail_price, row.quantity])

	# Поиск по таблице
	TableSearch(frame_services, tree_services, Service, 'name', services)

	# Взаимодействие с таблицей
	def item_selected(event):
		TableInteraction(frame_services, tree_services)

	tree_services.bind("<ButtonPress-3>", item_selected)
	tree_services.bind("<Return>", item_selected)
###-------------------------------------------------------------------------------------------------------------------------------------------------####

def create_new_applications(): # Создать новую заявку
	clear_widget(work_frame)
	frame_new_applications = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_new_applications.pack(side=tk.TOP, fill='both')

	labelframe = LabelFrame(frame_new_applications, text="Новая заявка")
	labelframe.pack(fill="both", expand="yes")
 
	labelwork_frame = LabelFrame(labelframe, text="О заявке")
	labelwork_frame.pack(fill="both", expand="yes") 

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Имя")
	left.pack(side='left')
	entry_name = Entry(frame, width=50)
	entry_name.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Телефон")
	left.pack(side='left')
	entry_telphone = Entry(frame, width=50)
	entry_telphone.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Источник")
	left.pack(side='left')
	lst = ["Звонок", "Электронная почта", "Веб-сайт", "Реклама", "Существующий клиент", "По рекомендации", "Другое"]
	combobox_2 = ttk.Combobox(frame, values=lst, width=48)
	combobox_2.current(0)
	combobox_2.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Комментарии")
	left.pack(side='left')
	entry_comment = Entry(frame, width=50)
	entry_comment.pack(side='right', pady=6, padx=6)

	labelframe5 = LabelFrame(labelframe, text="Опции")
	labelframe5.pack(fill="both", expand="yes")
	frame = tk.Frame(labelframe5)
	frame.pack(side='top')
		
	Button_deal = tk.Button(master=frame, text='Сохранить', command=lambda: new_new_applications(entry_name.get(),entry_telphone.get(),
																			combobox_2.get(),entry_comment.get(),ADMIN,'Новая', 
																				frame_new_applications, new_applications))
	Button_deal.pack(side=tk.LEFT)
	Button_deal2 = tk.Button(master=frame, text='Отмена', command=lambda: close_window(frame_new_applications, new_applications))
	Button_deal2.pack(side=tk.RIGHT)

	

def new_applications():  # Новые заявки
	clear_widget(work_frame)
	frame_new_applications = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_new_applications.pack(side=tk.TOP, fill='both')
	Button_deal = tk.Button(master=frame_new_applications, text='Добавить заявку', command=create_new_applications)
	Button_deal.pack(side=tk.LEFT)

	tree_new_applications= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"), show='headings')
	tree_new_applications.heading("#1", text="id")
	tree_new_applications.column("#1", minwidth=30, width=40)
	tree_new_applications.heading("#2", text="Имя")
	tree_new_applications.column("#2", minwidth=100, width=150)
	tree_new_applications.heading("#3", text="Телефон")
	tree_new_applications.column("#3", minwidth=100, width=100)
	tree_new_applications.heading("#4", text="Создан")
	tree_new_applications.column("#4", minwidth=100, width=150)
	tree_new_applications.heading("#5", text="Источник")
	tree_new_applications.column("#5", minwidth=100, width=130)
	tree_new_applications.heading("#6", text="Ответственный")
	tree_new_applications.column("#6", minwidth=100, width=100)
	tree_new_applications.heading("#7", text="Комментарии")
	tree_new_applications.column("#7", minwidth=100, width=100)
	tree_new_applications.pack(expand=1, anchor=E, fill="both")
	data = Lid.select(Lid.id, Lid.name, Lid.telephone_number, Lid.create_date, Lid.Source, Lid.responsible, Lid.comment)
	for row in data:
		tree_new_applications.insert("", tk.END, values=[row.id, row.name, row.telephone_number, row.create_date, row.Source, row.responsible, row.comment])
	# TableSearch(frame_new_applications, tree_new_applications, Lid, 'name', new_applications)
###-------------------------------------------------------------------------------------------------------------------------------------------------####

def create_all_applications():
	clear_widget(work_frame)
	frame_create_all_applications = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_create_all_applications.pack(side=tk.TOP, fill='both')

	labelframe = LabelFrame(frame_create_all_applications, text="Новая заявка")
	labelframe.pack(fill="both", expand="yes")
 
	labelwork_frame = LabelFrame(labelframe, text="О заявке")
	labelwork_frame.pack(fill="both", expand="yes") 

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Имя")
	left.pack(side='left')
	entry_name = Entry(frame, width=50)
	entry_name.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Телефон")
	left.pack(side='left')
	entry_telphone = Entry(frame, width=50)
	entry_telphone.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Источник")
	left.pack(side='left')
	lst = ["Звонок", "Электронная почта", "Веб-сайт", "Реклама", "Существующий клиент", "По рекомендации", "Другое"]
	combobox_2 = ttk.Combobox(frame, values=lst, width=48)
	combobox_2.current(0)
	combobox_2.pack(side='right', pady=6, padx=6)

	frame = tk.Frame(labelwork_frame)
	frame.pack(anchor='w')
	left = Label(frame, text="Комментарии")
	left.pack(side='left')
	entry_comment = Entry(frame, width=50)
	entry_comment.pack(side='right', pady=6, padx=6)

	labelframe5 = LabelFrame(labelframe, text="Опции")
	labelframe5.pack(fill="both", expand="yes")
	frame = tk.Frame(labelframe5)
	frame.pack(side='top')
	
	Button_deal = tk.Button(master=frame, text='Сохранить', command=lambda: new_new_applications(entry_name.get(),entry_telphone.get(),
																			combobox_2.get(),entry_comment.get(),ADMIN,'Новая', 
																				frame_create_all_applications, new_applications))
	Button_deal.pack(side=tk.LEFT)
	Button_deal2 = tk.Button(master=frame, text='Отмена', command=close_window(frame_create_all_applications, all_applications))
	Button_deal2.pack(side=tk.RIGHT)

def all_applications():
	clear_widget(work_frame)
	frame_all_applications = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_all_applications.pack(side=tk.TOP, fill='both')
	Button_deal = tk.Button(master=frame_all_applications, text='Добавить заявку', command=create_new_applications)
	Button_deal.pack(side=tk.LEFT)

	tree_all_applications= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8"), show='headings')
	tree_all_applications.heading("#1", text="id")
	tree_all_applications.column("#1", minwidth=30, width=40)
	tree_all_applications.heading("#2", text="Имя")
	tree_all_applications.column("#2", minwidth=100, width=150)
	tree_all_applications.heading("#3", text="Телефон")
	tree_all_applications.column("#3", minwidth=100, width=100)
	tree_all_applications.heading("#4", text="Создан")
	tree_all_applications.column("#4", minwidth=100, width=150)
	tree_all_applications.heading("#5", text="Источник")
	tree_all_applications.column("#5", minwidth=100, width=130)
	tree_all_applications.heading("#6", text="Ответственный")
	tree_all_applications.column("#6", minwidth=100, width=100)
	tree_all_applications.heading("#7", text="Комментарии")
	tree_all_applications.column("#7", minwidth=100, width=100)
	tree_all_applications.heading("#8", text="Статус")
	tree_all_applications.column("#8", minwidth=100, width=100)
	tree_all_applications.pack(expand=1, anchor=E, fill="both")
	data = Lid.select()
	for row in data:
		tree_all_applications.insert("", tk.END, values=[row.id, row.name,
			row.telephone_number, row.create_date, row.Source, row.responsible, row.comment, row.status])

	# TableSearch(frame_all_applications, tree_all_applications, Lid, 'name', all_applications)

	# Взаимодействие с таблицей
	def item_selected(event):
		TableInteraction(frame_all_applications, tree_all_applications)

	tree_all_applications.bind("<ButtonPress-3>", item_selected)
	tree_all_applications.bind("<Return>", item_selected)	
###-------------------------------------------------------------------------------------------------------------------------------------------------####

def info():  
    messagebox.showinfo('О программе', 'Прототип замены EXEL')

def onExit():
	if messagebox.askokcancel("Выход", "Вы уверены что хотите выйти?"):
		window.destroy()

###-------------------------------------------------------------------------------------------------------------------------------------------------####    
# Блок верхнего меню
filemenu = Menu(menu, tearoff=0)

filemenu2 = Menu(filemenu, tearoff=0)
filemenu2.add_command(label="Клиенты")
filemenu2.add_command(label="Сотрудники")
filemenu2.add_command(label="Посещаемость")
filemenu2.add_command(label="Оплаты")

filemenu.add_cascade(label='Экспорт', menu=filemenu2)
filemenu.add_separator() 

filemenu3 = Menu(filemenu, tearoff=0)
filemenu3.add_command(label="Клиент")
filemenu3.add_command(label="Сотрудник") 
filemenu.add_cascade(label='Добавить', menu=filemenu3)  

menu.add_cascade(label='Файл', menu=filemenu)
menu.add_cascade(label='Информация о программе', command = info) 
menu.add_cascade(label='Выход', command = onExit) 

###-------------------------------------------------------------------------------------------------------------------------------------------------####

# Левый меню-бар

frame1 = tk.Frame(master=window, width=200, height=100, bg=color_frame_menu)
frame1.pack(side=tk.LEFT, fill='both')

frame1_1 = tk.Frame(master=frame1, width=200, height=50, bg=color_frame_menu)
frame1_1.pack(fill=tk.X)
lbl = Label(frame1_1, text="    CRM    ", font=font_lable_menu, bg=color_label_menu)  
lbl.pack()
button_1_1 = tk.Button(frame1_1, text="Сделки", font=font_button_menu, bg=color_button_menu, width=button_width, command=deal_now)
button_1_1.pack()
button_1_4 = tk.Button(frame1_1, text="Клиенты", font=font_button_menu, bg=color_button_menu, width=button_width, command=clients)
button_1_4.pack()
button_1_5 = tk.Button(frame1_1, text="Продажи", font=font_button_menu, bg=color_button_menu, width=button_width)
button_1_5['state'] = 'disabled'  # button['state'] = 'normal'
button_1_5.pack()
button_1_6 = tk.Button(frame1_1, text="Лиды", font=font_button_menu, bg=color_button_menu, width=button_width)
button_1_6['state'] = 'disabled'
button_1_6.pack()
button_1_7 = tk.Button(frame1_1, text="Контроль", font=font_button_menu, bg=color_button_menu, width=button_width, command=passage_control)
# button_1_7['state'] = 'disabled'
button_1_7.pack()

lbl = Label(frame1_1, text="    Товары / Склад    ", font=font_lable_menu, bg=color_label_menu)  
lbl.pack()
button_1_1 = tk.Button(frame1_1, text="Каталог товаров", font=font_button_menu, bg=color_button_menu, width=button_width, command=warehouse)
button_1_1.pack()
button_1_2 = tk.Button(frame1_1, text="Услуги", font=font_button_menu, bg=color_button_menu, width=button_width, command=services) # , command=inventory_control
button_1_2.pack()
button_1_3 = tk.Button(frame1_1, text="Складской учет", font=font_button_menu, bg=color_button_menu, width=button_width, command=inventory_control)
button_1_3.pack()
 
frame1_2 = tk.Frame(master=frame1, width=200, height=50, bg=color_frame_menu)
frame1_2.pack(fill=tk.X)
lbl = Label(frame1_2, text="Сотрудники", font=font_lable_menu, bg=color_label_menu)  
lbl.pack()
button_2_1 = tk.Button(frame1_2, text="Тренеры", font=font_button_menu, bg=color_button_menu, width=button_width, command = treners)
button_2_1.pack()
button_2_2 = tk.Button(frame1_2, text="Администраторы", font=font_button_menu, bg=color_button_menu, width=button_width, command = staff)
button_2_2.pack()

frame1_3 = tk.Frame(master=frame1, width=200, height=50, bg=color_frame_menu)
frame1_3.pack(fill=tk.X)
lbl = Label(frame1_3, text="Заявки", font=font_lable_menu, bg=color_label_menu)  
lbl.pack()

button_3_1 = tk.Button(frame1_3, text="Все", font=font_button_menu,bg=color_button_menu, width=button_width, command=all_applications)
# button_3_1['state'] = 'disabled'
button_3_2 = tk.Button(frame1_3, text="Новые", font=font_button_menu,bg=color_button_menu, width=button_width, command = new_applications)
# button_3_2['state'] = 'disabled'
button_3_3 = tk.Button(frame1_3, text="Архив", font=font_button_menu,bg=color_button_menu, width=button_width)
button_3_3['state'] = 'disabled'
button_3_1.pack()
button_3_2.pack()
button_3_3.pack()

frame1_4 = tk.Frame(master=frame1, width=200, height=50, bg=color_frame_menu)
frame1_4.pack(fill=tk.X)
lbl = Label(frame1_4, text="Звонки", font=font_lable_menu, bg=color_label_menu)  
lbl.pack()

button_3_1 = tk.Button(frame1_4, text="Все", font=font_button_menu,bg=color_button_menu, width=button_width)
button_3_1['state'] = 'disabled'
button_3_2 = tk.Button(frame1_4, text="Новые", font=font_button_menu,bg=color_button_menu, width=button_width)
button_3_2['state'] = 'disabled'
button_3_3 = tk.Button(frame1_4, text="Архив", font=font_button_menu,bg=color_button_menu, width=button_width)
button_3_3['state'] = 'disabled'
button_3_1.pack()
button_3_2.pack()
button_3_3.pack()

###-------------------------------------------------------------------------------------------------------------------------------------------------#### 

# Наполнение страницы

work_frame = tk.Frame(master=window, width=1180, height=50)
work_frame.pack(side=tk.LEFT, fill='both')

###-------------------------------------------------------------------------------------------------------------------------------------------------#### 

# Часы и Имя пользователя

frame_bottom = tk.Frame(master=frame1, width=1180, height=10, bg=color_frame_menu)
frame_bottom.pack(side=tk.BOTTOM, fill='both')

clock(frame_bottom, color_frame_menu)  # Часы

def user():
	frame1_6 = tk.Frame(master=frame_bottom, width=200, height=50, bg=color_frame_menu)
	frame1_6.pack(fill=tk.Y, side=tk.LEFT)

	lbl = Label(frame1_6, text=ADMIN, font=10, bg=color_label_menu)  
	lbl.pack(padx=5, pady=5)

user()

###-------------------------------------------------------------------------------------------------------------------------------------------------#### 


window.mainloop()

# Нужно доработать БД для возможности фильтрации данных
# Приделать и доделать БД для хранения и обработки заявок
# Сделать прикрепление к тренеру
# Сделать экспорт/импорт exel для возможности сбора отчетов

# class ProgrammWindow(object):
# 	"""docstring for ProgrammWindow"""
# 	def __init__(self, arg):
# 		super(ProgrammWindow, self).__init__()
# 		self.arg = arg


# if __name__== '__main__':
# 	main_window = Tk()
# 	run = ProgrammWindow(main_window)
# 	main_window.mainloop()
