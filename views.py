




def clear_widget(widget):
	# Очистка переданного окна 
	for chil_widget in widget.winfo_children():
		chil_widget.destroy()


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
