import json

with open('settings/settings.json', 'r', encoding='utf-8') as file: # settings/
  data = json.load(file)

LABLE = data['lable']
color_button_menu = data['color_button_menu']
color_frame_menu = data['color_frame_menu']
color_label_menu = data['color_label_menu']
button_width = data['button_width']
font_lable_menu = (data['font_lable_menu'][0], data['font_lable_menu'][1])
font_button_menu = (data['font_button_menu'][0], data['font_button_menu'][1])
