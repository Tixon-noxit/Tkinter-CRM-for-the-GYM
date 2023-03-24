from tkinter import * 
from tkinter import Menu, ttk, messagebox 
import tkinter as tk
from tkinter.ttk import Combobox
from tkcalendar import Calendar, DateEntry 
import sqlite3
from peewee import *
from ttkwidgets.autocomplete import AutocompleteCombobox
from views import clear_widget, new_contact, close_window, new_deal, new_trener, new_staff, new_warehouse, new_services, new_new_applications, clock # search_for_table


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
""" Унифицировать функцию поиска по таблицам """

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

width = window.winfo_screenwidth()  # Ширина окна
height = window.winfo_screenheight()  # Высота окна

###-------------------------------------------------------------------------------------------------------------------------------------------------####

# Блок поиска по таблице (В reset_search необходимо менять вызываемую функцию)

def search_for_table(parent, var, treeview, db_name, table_name, search_value, column_name, column_var,  function): 

	# Поиск по указанной таблице
	def search(treeview, desired, db_name, table_name, column_var):
		treeview.selection()
		fetchdata = treeview.get_children()
		for f in fetchdata:
			treeview.delete(f)
			conn = None
		try:
			conn = sqlite3.connect(db_name)
			core = conn.cursor()
			if var==2:
				db = f"select * from {table_name} where {search_value} = '%s' and {column_name} = '{column_var}' "
			else:
				db = f"select * from {table_name} where '{desired}' = '%s'"
			name = desired.get()
			if (len(name) < 2) or (not name.isalpha()):
				messagebox.showerror("Ошибка!", "Имя указано не верно!")
				function()
			else:
				core.execute(db %(name))
				data = core.fetchall()
				for d in data:
					treeview.insert("", END, values=d)

		except Exception as e:
			messagebox.showerror("issue", e)

		finally:
			if conn is not None:
				conn.close()

	entry_search = Entry(parent, width=50)
	entry_search.pack(side=tk.LEFT, pady=6, padx=6)
	Button_clients2 = tk.Button(master=parent, text='Найти', command=lambda: search(treeview, entry_search, db_name, table_name, column_var))
	Button_clients2.pack(side=tk.LEFT)

	def reset_search():
		entry_search.delete("0", END)
		function()
	Button_clients2 = tk.Button(master=parent, text='Очистить', command=reset_search)
	Button_clients2.pack(side=tk.LEFT)		

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

	tree2= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column6"), show='headings')
	tree2.heading("#1", text="id")
	tree2.column("#1", minwidth=40, width=40)
	tree2.heading("#2", text="Фамилия")
	tree2.heading("#3", text="Имя")
	tree2.heading("#4", text="Телефон")
	tree2.column("#4", minwidth=80, width=100)
	tree2.heading("#5", text="Тип")
	tree2.column("#5", minwidth=50, width=120)
	tree2.heading("#6", text="Источник")
	tree2.column("#6", minwidth=120, width=150)
	tree2.heading("#7", text="Дата создания")
	tree2.pack(expand=1, anchor=NW, fill="both")

	data = Contact.select().order_by(Contact.create_date)

	for row in data:
		tree2.insert("", tk.END, values=[row.id, row.First_Name, row.Last_Name, row.Phone_number, row.Type, row.Source, row.create_date])
	


def provider(): # Окно поставщиков
	clear_widget(work_frame)
	frame_provider = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_provider.pack(side=tk.TOP, fill='both')	
	Button_clients = tk.Button(master=frame_provider, text='Добавить', command=create_contact)
	Button_clients.pack(side=tk.LEFT)
	Button_clients2 = tk.Button(master=frame_provider, text='Назад', command=clients)
	Button_clients2.pack(side=tk.LEFT)

	tree2= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column6"), show='headings')
	tree2.heading("#1", text="id")
	tree2.column("#1", minwidth=40, width=40)
	tree2.heading("#2", text="Фамилия")
	tree2.heading("#3", text="Имя")
	tree2.heading("#4", text="Телефон")
	tree2.column("#4", minwidth=80, width=100)
	tree2.heading("#5", text="Тип")
	tree2.column("#5", minwidth=50, width=120)
	tree2.heading("#6", text="Источник")
	tree2.column("#6", minwidth=120, width=150)
	tree2.heading("#7", text="Дата создания")
	tree2.pack(expand=1, anchor=NW, fill="both")

	data = Contact.select().where(Contact.Type == 'Поставщик')

	for row in data:
		tree2.insert("", tk.END, values=[row.id, row.First_Name, row.Last_Name, row.Phone_number, row.Type, row.Source, row.create_date])	


def clients():
	clear_widget(work_frame)
	frame_clients = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_clients.pack(side=tk.TOP, fill='both')	
	Button_clients = tk.Button(master=frame_clients, text='Контакты', command=contacts)
	Button_clients.pack(side=tk.LEFT)
	Button_clients2 = tk.Button(master=frame_clients, text='Поставщики', command=provider)
	Button_clients2.pack(side=tk.LEFT)
	
	tree2= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4"), show='headings')
	tree2.heading("#1", text="id")
	tree2.column("#1", minwidth=20, width=30)
	tree2.heading("#2", text="Фамилия")
	tree2.heading("#3", text="Имя")
	tree2.heading("#4", text="Телефон")
	tree2.column("#4", minwidth=50, width=120)
	tree2.pack(expand=1, anchor=NW, fill="both")

	data = Contact.select().where(Contact.Type=='Клиент').order_by(Contact.create_date.desc())

	for row in data:
		tree2.insert("", tk.END, values=[row.id, row.First_Name, row.Last_Name, row.Phone_number, row.Type, row.Source, row.create_date])
	search_for_table(frame_clients, 2, tree2, 'organization.db', 'Contact', 'First_Name', 'Type', 'Клиент',  clients)

###-------------------------------------------------------------------------------------------------------------------------------------------------####

def contact_selection():
	clear_widget(work_frame)
	a = tk.Toplevel()
	a.geometry("750x700+400+50")
	a.resizable(0, 0)
	# a['bg'] = 'grey'
	a.overrideredirect(True)
	
	def show():
		ws_ent.delete(0, END)
		ws_ent.focus()
		treeview.selection()
		
		conn = sqlite3.connect("organization.db")
		cur = conn.cursor()
		cur.execute("SELECT * FROM contact ORDER BY First_Name DESC")
		rows = cur.fetchall()
		fetchdata = treeview.get_children()
		for elements in fetchdata:
			treeview.delete(elements)
	
		data = cur.fetchall()
		for d in data:
			treeview.insert("", END, values=d.First_Name)


	def search():
		treeview.selection()
		fetchdata = treeview.get_children()
		for f in fetchdata:
			treeview.delete(f)
		
		db = Client.select().where(First_Name == '%s')
		name = ws_ent.get()
		if (len(name) < 2) or (not name.isalpha()):
			showerror("fail", "invalid name")
		else:
			core.execute(db %(name))
			data = core.fetchall()
			for d in data:
				treeview.insert("", END, values=d)
	
	def reset():
		show()
	
	scrollbarx = Scrollbar(a, orient=HORIZONTAL)  
	scrollbary = Scrollbar(a, orient=VERTICAL)    
	treeview = ttk.Treeview(a, columns=("rollno", "name"), show='headings', height=22)  
	treeview.pack()
	treeview.heading('rollno', text="Roll No", anchor=CENTER)
	treeview.column("rollno", stretch=NO, width = 100) 
	treeview.heading('name', text="Name", anchor=CENTER)
	treeview.column("name", stretch=NO)
	scrollbary.config(command=treeview.yview)
	scrollbary.place(x = 526, y = 7)
	scrollbarx.config(command=treeview.xview)
	scrollbarx.place(x = 220, y = 460)
	style = ttk.Style()
	style.theme_use("default")
	style.map("Treeview")
	
	
	ws_lbl = Label(a, text = "Name", font=('calibri', 12, 'normal'))
	ws_lbl.place(x = 290, y = 518)
	ws_ent = Entry(a,  width = 20, font=('Arial', 15, 'bold'))
	ws_ent.place(x = 220, y = 540)
	ws_btn1 = Button(a, text = 'Search',  width = 8, font=('calibri', 12, 'normal'), command = search)
	ws_btn1.place(x = 480, y = 540)
	ws_btn2 = Button(a, text = 'Reset',  width = 8, font=('calibri', 12, 'normal'), command = reset)
	ws_btn2.place(x = 600, y = 540)


	show()


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

	# countries = [
	# 	'Antigua and Barbuda', 'Bahamas','Barbados','Belize', 'Canada',
	# 	'Costa Rica ', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador ',
	# 	'Grenada', 'Guatemala ', 'Haiti', 'Honduras ', 'Jamaica', 'Mexico',
	# 	'Nicaragua', 'Saint Kitts and Nevis', 'Panama ', 'Saint Lucia',
	# 	'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States of America'
	# 	]

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

	# Поиск по указанной таблице
	def search_deal():
		tree.selection()
		fetchdata = tree.get_children()
		for f in fetchdata:
			tree.delete(f)
			conn = None
		try:
			conn = sqlite3.connect('organization.db')
			core = conn.cursor()
			
			db = f"select * from Deal where client_first_name = '%s' "
			
			name = entry_search.get()
			if (len(name) < 2) or (not name.isalpha()):
				messagebox.showerror("Ошибка!", "Имя указано не верно!")
				deal()
			else:
				core.execute(db %(name))
				data = core.fetchall()
				for d in data:
					tree.insert("", END, values=d)

		except Exception as e:
			messagebox.showerror("issue", e)

		finally:
			if conn is not None:
				conn.close()

	entry_search = Entry(frame_history_deal, width=50)
	entry_search.pack(side=tk.LEFT, pady=6, padx=6)
	Button_clients2 = tk.Button(master=frame_history_deal, text='Найти', command=lambda: search_deal())
	Button_clients2.pack(side=tk.LEFT)
	def reset_search():
		entry_search.delete("0", END)
		deal_now()
	Button_clients2 = tk.Button(master=frame_history_deal, text='Очистить', command=reset_search)
	Button_clients2.pack(side=tk.LEFT)

	# Взаимодействие с таблицей
	def item_selected(event): # Выделение фрагмента таблицы
		def createNewWindow(arg):
			newWindow = tk.Toplevel(frame_history_deal)
			labelExample = tk.Label(newWindow, text = arg[4])
			buttonExample = tk.Button(newWindow, text = "New Window button")

			labelExample.pack()
			buttonExample.pack()					
		selected_people = ""																	
		for selected_item in tree.selection():									
			item = tree.item(selected_item)									
			selected_people = item["values"]
		createNewWindow(selected_people)	
	tree.bind("<ButtonPress-3>", item_selected)


def deal_now():
	clear_widget(work_frame)
	
	frame_deal = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_deal.pack(side=tk.TOP, fill='both')
	Button_deal = tk.Button(master=frame_deal, text='Создать сделку', command=create_deal)
	Button_deal.pack(side=tk.LEFT)
	Button_deal2 = tk.Button(master=frame_deal, text='История продаж', command=history_deal)
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
	now = datetime.now().strftime("%d.%m.%Y")
	table_deal = Deal.select().where(Deal.create_date == now)
	for t in table_deal:
		tree.insert("", tk.END, values=(t.id, t.summ, t.stady, t.create_date, 
										t.client_first_name, t.client_last_name, 
										t.tip, t.source, t.date_the_start, 
										t.responsible, t.comment))




	# Поиск по указанной таблице
	def search_deal():
		tree.selection()
		fetchdata = tree.get_children()
		for f in fetchdata:
			tree.delete(f)
			conn = None
		try:
			conn = sqlite3.connect('organization.db')
			core = conn.cursor()
			
			db = f"select * from Deal where client_first_name = '%s' "
			
			name = entry_search.get()
			if (len(name) < 2) or (not name.isalpha()):
				messagebox.showerror("Ошибка!", "Имя указано не верно!")
				deal()
			else:
				core.execute(db %(name))
				data = core.fetchall()
				for d in data:
					tree.insert("", END, values=d)

		except Exception as e:
			messagebox.showerror("issue", e)

		finally:
			if conn is not None:
				conn.close()

	entry_search = Entry(frame_deal, width=50)
	entry_search.pack(side=tk.LEFT, pady=6, padx=6)
	Button_clients2 = tk.Button(master=frame_deal, text='Найти', command=lambda: search_deal())
	Button_clients2.pack(side=tk.LEFT)
	def reset_search():
		entry_search.delete("0", END)
		deal_now()
	Button_clients2 = tk.Button(master=frame_deal, text='Очистить', command=reset_search)
	Button_clients2.pack(side=tk.LEFT)


	# Взаимодействие с таблицей
	def item_selected(event): # Выделение фрагмента таблицы
		def createNewWindow(arg):
			# Файл лого для окон
			# logo = 'Images/boxing.ico'
			newWindow = Toplevel(frame_deal)
			# labelExample = tk.Label(newWindow, text = arg[4])
			newWindow.geometry('500x360+380+200')
			# newWindow.iconbitmap(logo)
			newWindow.title('Информация о сделке')
			newWindow.resizable(False, False)
			newWindow.focus_force()
			newWindow.grab_set()


			deal_var = Deal.get(Deal.id == arg[0])
			
			label_name = Label(newWindow, text = "id")
			label_name.place(x=100, y=37, anchor="e", height=20, width=95, bordermode=OUTSIDE)
			label_name = Label(newWindow, text = deal_var.id)
			label_name.place(x=150, y=37, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
			labeljob = Label(newWindow, text = "Сумма:")
			labeljob.place(x=100, y=67, anchor="e", height=20, width=95, bordermode=OUTSIDE)
			labeljob = Label(newWindow, text = deal_var.summ)
			labeljob.place(x=150, y=67, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
			labelnum = Label(newWindow, text = "Стадия:")
			labelnum.place(x=100, y=97, anchor="e", height=20, width=95, bordermode=OUTSIDE)
			labelnum = Label(newWindow, text = deal_var.stady)
			labelnum.place(x=150, y=97, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
			labelnum1 = Label(newWindow, text = "Создана:")
			labelnum1.place(x=100, y=127, anchor="e", height=20, width=95, bordermode=OUTSIDE)
			labelnum1 = Label(newWindow, text = deal_var.create_date)
			labelnum1.place(x=150, y=127, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
			labelnum2 = Label(newWindow, text = "Клиент:")
			labelnum2.place(x=100, y=157, anchor="e", height=20, width=95, bordermode=OUTSIDE)
			labelnum2t = Label(newWindow, text = f'{deal_var.client_first_name} {deal_var.client_last_name}')
			labelnum2t.place(x=150, y=157, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
			labelnum3 = Label(newWindow, text = "Тип:")
			labelnum3.place(x=100, y=187, anchor="e", height=20, width=95, bordermode=OUTSIDE)
			labelnum3 = Label(newWindow, text = deal_var.tip)
			labelnum3.place(x=150, y=187, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
			labelnum4 = Label(newWindow, text = "Источник:")
			labelnum4.place(x=100, y=217, anchor="e", height=20, width=95, bordermode=OUTSIDE)
			labelnum4 = Label(newWindow, text = deal_var.source)
			labelnum4.place(x=150, y=217, anchor="w", height=20, width=200, bordermode=OUTSIDE)

			labelnum5 = Label(newWindow, text = "Дата начала:")
			labelnum5.place(x=100, y=247, anchor="e", height=20, width=95, bordermode=OUTSIDE)
			labelnum5 = Label(newWindow, text = deal_var.date_the_start)
			labelnum5.place(x=150, y=247, anchor="w", height=20, width=200, bordermode=OUTSIDE)

			labelnum6 = Label(newWindow, text = "Ответственный:")
			labelnum6.place(x=100, y=277, anchor="e", height=20, width=95, bordermode=OUTSIDE)
			labelnum6 = Label(newWindow, text = deal_var.responsible)
			labelnum6.place(x=150, y=277, anchor="w", height=20, width=200, bordermode=OUTSIDE)

			labelnum7 = Label(newWindow, text = "Комментарий:")
			labelnum7.place(x=100, y=307, anchor="e", height=20, width=95, bordermode=OUTSIDE)
			labelnum7 = Label(newWindow, text = deal_var.comment)
			labelnum7.place(x=150, y=307, anchor="w", height=20, width=200, bordermode=OUTSIDE)

			# Кнопки окна истории шкафчика
			btn_history = Button(newWindow, text="Клиент", 
					        	width=10, height=1, anchor="n")  # , command = lambda: history(arg,arg2)
			btn_history.place(relx=0.60, y=337, anchor="e")
		
			btn_change = Button(newWindow, text="Изменить", 
					        	width=10, height=1, anchor="n")  # , command = lambda: change(arg,arg2)
			btn_change.place(relx=0.78, y=337, anchor="e")
		
			btn_change = Button(newWindow, text="Удалить", 
					        	width=10, height=1, anchor="n")  # , command = delete_locker
			btn_change.place(relx=0.96, y=337, anchor="e")

		# Получение значений выбранной строки таблицы					
		selected_people = ""																	
		for selected_item in tree.selection():									
			item = tree.item(selected_item)									
			selected_people = item["values"]
		createNewWindow(selected_people)

	tree.bind("<ButtonPress-3>", item_selected)
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
	
	tree2= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"), show='headings')
	tree2.heading("#1", text="id")
	tree2.column("#1", minwidth=40, width=50)
	tree2.heading("#2", text="Фамилия")
	tree2.heading("#3", text="Имя")
	tree2.heading("#4", text="Телефон")
	tree2.column("#4", minwidth=80, width=110)
	tree2.heading("#5", text="Дисциплина")
	tree2.heading("#6", text="Тип")
	tree2.heading("#7", text="Дата внесения")
	tree2.pack(expand=1, anchor=NW, fill="both")
	data = Trener.select()
	for row in data:
		tree2.insert("", tk.END, values=[row.id, row.First_Name, row.Last_Name, row.Phone_number, row.Type, row.Source, row.create_date])
	

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

	tree2= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"), show='headings')
	tree2.heading("#1", text="id")
	tree2.column("#1", minwidth=40, width=50)
	tree2.heading("#2", text="Фамилия")
	tree2.heading("#3", text="Имя")
	tree2.heading("#4", text="Телефон")
	tree2.column("#4", minwidth=80, width=110)
	tree2.heading("#5", text="Тип")
	tree2.heading("#6", text="Внес")
	tree2.heading("#7", text="Дата внесения")
	tree2.pack(expand=1, anchor=NW, fill="both")
	data = Staff.select()
	for row in data:
		tree2.insert("", tk.END, values=[row.id, row.First_Name, row.Last_Name, row.Phone_number, row.Type, row.Source, row.create_date])

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

def warehouse():
	clear_widget(work_frame)
	frame_deal = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_deal.pack(side=tk.TOP, fill='both')
	Button_deal = tk.Button(master=frame_deal, text='Добавить товар', command=create_warehous)
	Button_deal.pack(side=tk.LEFT)

	tree2= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5"), show='headings')
	tree2.heading("#1", text="id")
	tree2.column("#1", minwidth=30, width=40)
	tree2.heading("#2", text="Наименование")
	tree2.column("#2", minwidth=250, width=550)
	tree2.heading("#3", text="Розничнвя цена")
	tree2.column("#3", minwidth=100, width=100)
	tree2.heading("#4", text="Количество")
	tree2.column("#4", minwidth=100, width=100)
	tree2.heading("#5", text="Зарезервировано")
	tree2.column("#5", minwidth=120, width=120)
	tree2.pack(expand=1, anchor=NW, fill="both")
	data = Warehouse.select(Warehouse.id, Warehouse.name, Warehouse.retail_price, Warehouse.quantity,Warehouse.reserved)
	for row in data:
		tree2.insert("", tk.END, values=[row.id, row.name, row.retail_price, row.quantity,row.reserved ])

###-------------------------------------------------------------------------------------------------------------------------------------------------####

def inventory_control(): # Окно Складского учета
	clear_widget(work_frame)
	frame_deal = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_deal.pack(side=tk.TOP, fill='both')
	Button_deal = tk.Button(master=frame_deal, text='Создать оприходование')
	Button_deal['state']='disabled'
	Button_deal.pack(side=tk.LEFT)
	Button_deal2 = tk.Button(master=frame_deal, text='Журнал')
	Button_deal2['state']='disabled'
	Button_deal2.pack(side=tk.LEFT)

	tree2= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4",
										"column5", "column6", "column7", "column8"), show='headings')
	tree2.heading("#1", text="Название")
	tree2.heading("#2", text="Номер документа основания")
	tree2.heading("#3", text="Тип")
	tree2.heading("#4", text="Статус")
	tree2.heading("#5", text="Дата изменения")
	tree2.heading("#6", text="Ответственный")
	tree2.heading("#7", text="Поставщик")
	tree2.heading("#8", text="Сумма")
	tree2.pack(expand=1, anchor=NW, fill="both")
	# for row in rows:
	# 	print(row) # it print all records in the database
	# 	tree2.insert("", tk.END, values=row)
	# conn.close()

###-------------------------------------------------------------------------------------------------------------------------------------------------####

def create_services():
	clear_widget(work_frame)
	frame_services = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_services.pack(side=tk.TOP, fill='both')

	labelframe = LabelFrame(frame_services, text="Новая услуга")
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
																			entry_quantity.get(),frame_services, services))
	Button_deal.pack(side=tk.LEFT)
	Button_deal2 = tk.Button(master=frame, text='Отмена', command=lambda: close_window(frame_services, services))
	Button_deal2.pack(side=tk.RIGHT)



def services():
	clear_widget(work_frame)
	frame_deal = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	frame_deal.pack(side=tk.TOP, fill='both')
	Button_deal = tk.Button(master=frame_deal, text='Добавить Услугу', command=create_services)
	Button_deal.pack(side=tk.LEFT)

	tree2= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4"), show='headings')
	tree2.heading("#1", text="id")
	tree2.column("#1", minwidth=30, width=40)
	tree2.heading("#2", text="Наименование")
	tree2.column("#2", minwidth=250, width=550)
	tree2.heading("#3", text="Розничнвя цена")
	tree2.column("#3", minwidth=100, width=100)
	tree2.heading("#4", text="Количество")
	tree2.column("#4", minwidth=100, width=100)
	tree2.pack(expand=1, anchor=E, fill="both")
	data = Service.select(Service.id, Service.name, Service.retail_price, Service.quantity)
	for row in data:
		tree2.insert("", tk.END, values=[row.id, row.name, row.retail_price, row.quantity])

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
	new_applications = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
	new_applications.pack(side=tk.TOP, fill='both')
	Button_deal = tk.Button(master=new_applications, text='Добавить заявку', command=create_new_applications)
	Button_deal.pack(side=tk.LEFT)

	tree2= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"), show='headings')
	tree2.heading("#1", text="id")
	tree2.column("#1", minwidth=30, width=40)
	tree2.heading("#2", text="Имя")
	tree2.column("#2", minwidth=100, width=150)
	tree2.heading("#3", text="Телефон")
	tree2.column("#3", minwidth=100, width=100)
	tree2.heading("#4", text="Создан")
	tree2.column("#4", minwidth=100, width=150)
	tree2.heading("#5", text="Источник")
	tree2.column("#5", minwidth=100, width=130)
	tree2.heading("#6", text="Ответственный")
	tree2.column("#6", minwidth=100, width=100)
	tree2.heading("#7", text="Комментарии")
	tree2.column("#7", minwidth=100, width=100)
	tree2.pack(expand=1, anchor=E, fill="both")
	data = Lid.select(Lid.id, Lid.name, Lid.telephone_number, Lid.create_date, Lid.Source, Lid.responsible, Lid.comment)
	for row in data:
		tree2.insert("", tk.END, values=[row.id, row.name, row.telephone_number, row.create_date, row.Source, row.responsible, row.comment])

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
		new_applications = tk.Frame(master=work_frame, width=200, height=100, bg=color_frame_menu)
		new_applications.pack(side=tk.TOP, fill='both')
		Button_deal = tk.Button(master=new_applications, text='Добавить заявку', command=create_new_applications)
		Button_deal.pack(side=tk.LEFT)

		tree2= ttk.Treeview(work_frame, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8"), show='headings')
		tree2.heading("#1", text="id")
		tree2.column("#1", minwidth=30, width=40)
		tree2.heading("#2", text="Имя")
		tree2.column("#2", minwidth=100, width=150)
		tree2.heading("#3", text="Телефон")
		tree2.column("#3", minwidth=100, width=100)
		tree2.heading("#4", text="Создан")
		tree2.column("#4", minwidth=100, width=150)
		tree2.heading("#5", text="Источник")
		tree2.column("#5", minwidth=100, width=130)
		tree2.heading("#6", text="Ответственный")
		tree2.column("#6", minwidth=100, width=100)
		tree2.heading("#7", text="Комментарии")
		tree2.column("#7", minwidth=100, width=100)
		tree2.heading("#8", text="Статус")
		tree2.column("#8", minwidth=100, width=100)
		tree2.pack(expand=1, anchor=E, fill="both")
		data = Lid.select()
		for row in data:
			tree2.insert("", tk.END, values=[row.id, row.name,
				row.telephone_number, row.create_date, row.Source, row.responsible, row.comment, row.status])

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