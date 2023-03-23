




def clear_widget(widget):
	# Очистка переданного окна 
	for chil_widget in widget.winfo_children():
		chil_widget.destroy()