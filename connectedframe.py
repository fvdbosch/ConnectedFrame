#!/usr/bin/env python

from Tkinter import *
from os import putenv, system
from PIL import Image, ImageTk 
from glob import glob

putenv("DISPLAY",":0.0")

dropbox_link = "https://www.dropbox.com/sh/vhy51qtdt18nr0a/AACmd_XT8PITPrFDi0UvaEFla?dl=1"
base_path = "/usr/src/app/images/"
carrousel_status = True

image_index = 0
image_list = []

def download_images(url):
	archive = base_path + "temp.zip"

	remove = "sudo rm -rf " + base_path + "*"
	download = "wget -q  "+ url + " -O " + archive
	extract = "unzip -o " + archive + " -d " + base_path

	system(remove)
	system(download)
	system(extract)

def resize_images():
	images = list_images()

	for file in images:
		img = Image.open(file)
		img = img.resize((640, 480), Image.ANTIALIAS)
		img.save(file, "JPEG")

def list_images():
	images = []

	dir = base_path + "*.jpg"

	images = glob(dir)

	return images

def previous_image():
	global image_index
	image_index = image_index - 1

	if image_index < 0:
		image_index = len(image_list) - 1

	image_path = image_list[image_index]

	update_image(image_path)
	
def next_image():
	global image_index
	image_index = image_index + 1

	if image_index > len(image_list) - 1:
		image_index = 0

	image_path = image_list[image_index]

	update_image(image_path)

def play_pause():
	global carrousel_status

	carrousel_status = not carrousel_status

	if(carrousel_status):
		img = ImageTk.PhotoImage(Image.open("/usr/src/app/icons/pause.png"))
	else:
		img = ImageTk.PhotoImage(Image.open("/usr/src/app/icons/play.png"))
	
	play_button.configure(image=img)
	play_button.image = img

def carrousel():
	if(carrousel_status):
		next_image()

	root.after(5000, carrousel)


def update_image(image_path):
	img = ImageTk.PhotoImage(Image.open(image_path))
	center_label.configure(image=img)
	center_label.image = img

def initialize():
	global image_list

	download_images(dropbox_link)
	resize_images()
	image_list = list_images()


initialize()

root = Tk()
root.title('Connected Frame')
root.geometry('{}x{}'.format(800, 480))
root.attributes("-fullscreen", True)
root.config(cursor='none')

left_column = Frame(root, bg='black', width=80, height=480)
center_column = Frame(root, bg='black', width=640, height=480)
right_column = Frame(root, bg='black', width=80, height=480)

left_column.pack_propagate(0)
center_column.pack_propagate(0)
right_column.pack_propagate(0)

left_column.grid(row=0, column=0, sticky="nsew")
center_column.grid(row=0, column=1, sticky="nsew")
right_column.grid(row=0, column=2, sticky="nsew")

next_icon = ImageTk.PhotoImage(Image.open("/usr/src/app/icons/next.png"))
previous_icon = ImageTk.PhotoImage(Image.open("/usr/src/app/icons/previous.png"))
play_icon = ImageTk.PhotoImage(Image.open("/usr/src/app/icons/pause.png"))
like_icon = ImageTk.PhotoImage(Image.open("/usr/src/app/icons/like.png"))

previous_button = Button(left_column, image=previous_icon, borderwidth=0, background="black", foreground="white", activebackground="black", activeforeground="white", highlightthickness=0, command=previous_image)
next_button = Button(left_column, image=next_icon, borderwidth=0, background="black", foreground="white", activebackground="black", activeforeground="white", highlightthickness=0, command=next_image)
play_button = Button(right_column, image=play_icon, borderwidth=0, background="black", foreground="white", activebackground="black", activeforeground="white", highlightthickness=0, command=play_pause)
like_button = Button(right_column, image=like_icon, borderwidth=0, background="black", foreground="white", activebackground="black", activeforeground="white", highlightthickness=0)

center_image = Image.open(image_list[0])
center_photo = ImageTk.PhotoImage(center_image)
center_label = Label(center_column, image=center_photo)

previous_button.pack(fill=BOTH, expand=1)
next_button.pack(fill=BOTH, expand=1)
center_label.pack(side="bottom", fill=BOTH, expand=1)
play_button.pack(fill=BOTH, expand=1)
like_button.pack(fill=BOTH, expand=1)

carrousel()

root.mainloop()
