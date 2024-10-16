from models_DB import *  # Data Base
import tkinter as tk
from tkinter import BOTH, END, LEFT, messagebox 

import threading  # Импортируем модель для дополнительных процессов
import tkinter as tk
from time import sleep
from datetime import timedelta, datetime

def clear_widget(widget):
	# Очистка переданного окна 
	for chil_widget in widget.winfo_children():
		chil_widget.destroy()

def new_contact(arg, arg2, arg3, arg4, arg5, parent, open_window):  # Создать новый контакт в базе данных
	Contact.create(First_Name=arg, Last_Name=arg2, Phone_number=arg3 , Type=arg4 ,  Source=arg5)
	parent.destroy()
	open_window()

def new_deal(arg, arg2, arg3, arg4, arg5, arg6,	arg7, arg8, arg9, parent, open_window):  # Создать новую сделку в базе данных
	name = arg4.split()
	first_name = name[0]
	last_name = name[1]
	Deal.create(summ=arg, stady=arg2, create_date=arg3, client_first_name=first_name, client_last_name=last_name,
				tip=arg5, source=arg6, date_the_start=arg7, responsible=arg8,
				comment=arg9)
	close_window(parent, open_window)


def new_trener(arg,arg2,arg3,arg4,arg5, parent, open_window):
	Trener.create(First_Name=arg, Last_Name=arg2, Phone_number=arg3 , Type=arg4 ,  Source=arg5)   
	close_window(parent, open_window)	


def new_staff(arg,arg2,arg3,arg4,arg5, parent, open_window):
	Staff.create(First_Name=arg, Last_Name=arg2, Phone_number=arg3 , Type=arg4 ,  Source=arg5)	
	close_window(parent, open_window)

def new_warehouse(arg,arg2,arg3,arg4,arg5,arg6,arg7, parent, open_window):
	Warehouse.create(name=arg, description=arg2, unit=arg3 , purchase_price=arg4 ,  retail_price=arg5, quantity=arg6, reserved=arg7)	
	close_window(parent, open_window)

def new_services(arg,arg2,arg3,arg4, parent, open_window):
	Service.create(name=arg, description=arg2, retail_price=arg3, quantity=arg4)	
	close_window(parent, open_window)

def new_new_applications(arg,arg2,arg3,arg4,arg5,arg6,parent,open_window):
	Lid.create(name=arg, telephone_number=arg2, Source=arg3, comment=arg4, responsible=arg5, status=arg6)	
	close_window(parent, open_window)	

def close_window(parent, open_window):  # Закрыть окно
	parent.destroy()
	open_window()


class TableSearch():
	""" Поиск по таблице """
	def __init__(self, parent, treeview, DB, search_field, function):
		super(TableSearch, self).__init__()
		self.parent = parent
		self.treeview = treeview
		self.function = function
		self.search_field = search_field
		self.DB = DB
		self.entry()
		self.clear()


	def search(self):

		self.desired = self.Entry_search.get()

		if (len(self.desired) < 2) or (not self.desired.isalpha()):
				messagebox.showerror("Ошибка!", "Имя указано не верно!")
				self.function()
		else:
			self.treeview.selection()
			fetchdata = self.treeview.get_children()

			for f in fetchdata:
				self.treeview.delete(f)
		
		try:

			if self.DB == Deal and self.search_field == 'Новые':
				now = datetime.now().strftime("%d.%m.%Y")
				db = self.DB.select().where(self.DB.client_first_name.contains(self.desired), self.DB.date_the_start == now)
				for d in db:
					self.treeview.insert("", END, values=[d.id, d.summ, d.stady, 
								d.create_date, d.client_first_name, d.client_last_name, d.tip, d.source, 
								d.date_the_start, d.responsible, d.comment])

			elif self.DB == Deal and self.search_field == 'Старые':
				db = self.DB.select().where(self.DB.client_first_name.contains(self.desired))
				for d in db:
					self.treeview.insert("", END, values=[d.id, d.summ, d.stady, 
								d.create_date, d.client_first_name, d.client_last_name, d.tip, d.source, 
								d.date_the_start, d.responsible, d.comment])		


			elif self.DB == Trener:	
				db = self.DB.select().where(self.DB.First_Name.contains(self.desired))
				for d in db:
					self.treeview.insert("", END, values=[d.id, d.First_Name, d.Last_Name, d.Phone_number, d.Type, d.Source, d.create_date])

			elif self.DB == Warehouse:
				db = self.DB.select().where(self.DB.name.contains(self.desired))
				for d in db:
					self.treeview.insert("", END, values=[d.id, d.name, d.purchase_price, d.quantity, d.reserved])

			elif self.DB == Service:
				db = self.DB.select().where(self.DB.name.contains(self.desired))
				for d in db:
					self.treeview.insert("", END, values=[d.id, d.name, d.retail_price, d.quantity])

			elif self.DB == Contact and self.search_field == 'Поставщик':
				db = self.DB.select().where(self.DB.First_Name.contains(self.desired), self.DB.Type == 'Поставщик')	
				for d in db:
					self.treeview.insert("", END, values=[d.id, d.First_Name, d.Last_Name, d.Phone_number])


			elif self.DB == Contact and self.search_field == 'Клиент':
				db = self.DB.select().where(self.DB.First_Name.contains(self.desired), self.DB.Type == 'Клиент')	
				for d in db:
					self.treeview.insert("", END, values=[d.id, d.First_Name, d.Last_Name, d.Phone_number])		

			elif self.DB == Contact and self.search_field == 'Контакт':
				db = self.DB.select().where(self.DB.First_Name.contains(self.desired))	
				for d in db:
					self.treeview.insert("", END, values=[d.id, d.First_Name, d.Last_Name, d.Phone_number])

			elif self.DB == Staff:
				db = self.DB.select().where(self.DB.First_Name.contains(self.desired))	
				for d in db:
					self.treeview.insert("", END, values=[d.id, d.First_Name, d.Last_Name, d.Phone_number])										

		except Exception as e:
			messagebox.showerror("issue", e)	
	
	def entry(self):
		self.Entry_search = tk.Entry(self.parent, width=50)
		self.Entry_search.pack(side=tk.LEFT, pady=6, padx=6)
		Button_search = tk.Button(master=self.parent, text='Найти', command=self.search)
		Button_search.pack(side=tk.LEFT)

	def reset_search(self):
		self.Entry_search.delete("0", END)
		self.function()

	def clear(self):	
		Button_clear = tk.Button(master=self.parent, text='Очистить', command=self.reset_search)
		Button_clear.pack(side=tk.LEFT)		
		




class TableInteraction(object):
	""" Взаимодействие с таблицей """
	def __init__(self, parent, treeview):
		super(TableInteraction, self).__init__()
		self.parent= parent
		self.treeview = treeview

		self.innteraction()
			
	def innteraction(self):
		def createNewWindow(arg):
			newWindow = tk.Toplevel(self.parent)
			try:
				if arg[0]:
					labelExample0 = tk.Label(newWindow, text = arg[0])
					labelExample0.pack()
			except:
				pass

			try:	
				if arg[1]:	
					labelExample1 = tk.Label(newWindow, text = arg[1])
					labelExample1.pack()
			except:
				pass
						
			try:
				if arg[2]:	
					labelExample2 = tk.Label(newWindow, text = arg[2])
					labelExample2.pack()
			except:
				pass
						
			try:
				if arg[3]:	
					labelExample3 = tk.Label(newWindow, text = arg[3])
					labelExample3.pack()
			except:
				pass		

			try:	
				if arg[4]:	
					labelExample4 = tk.Label(newWindow, text = arg[4])
					labelExample4.pack()
			except:
				pass
						
			try:	
				if arg[5]:	
					labelExample5 = tk.Label(newWindow, text = arg[5])
					labelExample5.pack()
			except:
				pass

			try:				
				if arg[6]:
					labelExample6 = tk.Label(newWindow, text = arg[6])
					labelExample6.pack()
			except:
				pass
						
			try:
				if arg[7]:	
					labelExample7 = tk.Label(newWindow, text = arg[7])
					labelExample7.pack()
			except:
				pass
						
			try:		
				if arg[8]:	
					labelExample8 = tk.Label(newWindow, text = arg[8])
					labelExample8.pack()
			except:
				pass
						
			try:
				if arg[9]:	
					labelExample9 = tk.Label(newWindow, text = arg[9])
					labelExample9.pack()
			except:
				pass
						
			try:
				if arg[10]:	
					labelExample10 = tk.Label(newWindow, text = arg[10])
					labelExample10.pack()
			except:
				pass
						
			try:
				if arg[11]:	
					labelExample11 = tk.Label(newWindow, text = arg[11])
					labelExample11.pack()
			except:
				pass							
				
		selected_people = ""																	
		for selected_item in self.treeview.selection():									
			item = self.treeview.item(selected_item)									
			selected_people = item["values"]
		createNewWindow(selected_people)



def clock(parent, color_frame_menu):
	frame1_5 = tk.Frame(master=parent, width=200, height=50, bg=color_frame_menu)
	frame1_5.pack(fill=tk.Y, side=tk.LEFT)
	
	time = (datetime.utcnow() + timedelta(hours = 3)).strftime('%H:%M:%S')
	lbl_time = tk.Label(frame1_5 ,text = time, font="Arial 10")  # заранее создаем надпись
	lbl_time.pack(padx=10, pady=5)  # размещаем ее
	# process.switch_backend('agg')  

	def clock_update():  # создаем функцию
		while True:
			# Постоянно меняем значение у наших часов
			try:
				lbl_time['text'] = (datetime.utcnow() + timedelta(hours = 3)).strftime('%H:%M:%S')
				sleep(0.5)  # засыпаем на половину секунды, чтобы не перегружать процесс постоянными обновлениями
			except:
				break				
	process = threading.Thread(target=clock_update)  # Создаем процесс, в котором будем обновлять наши часы
	process.start()  # Запускаем процесс
