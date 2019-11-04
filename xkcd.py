#!/usr/bin/env python
# See http://cactusprojects.com/xkcd-widget-for-rpi/ for set-up
import requests
import urllib
from bs4 import BeautifulSoup, Comment
import io
import Tkinter as tk
import PIL
from PIL import Image
from PIL import ImageTk

def on_vertical(event):
    canvas.yview_scroll(-1 * event.delta, 'units')

def on_horizontal(event):
    canvas.xview_scroll(-1 * event.delta, 'units')

def close_window(): 
    root.destroy()

def pressed2():
    root.destroy()

def pressed():
	global theImage
	res = requests.get(url)
	html_page = res.content
	soup = BeautifulSoup(html_page, 'html.parser')
	images = soup.findAll('img')
	images = images[2]
	images = images['src']
	images = "http:" + images
        print images
	img_data = requests.get(images).content
	with open('xkcd.png', 'wb') as handler:
		handler.write(img_data)
	pil_image = Image.open("xkcd.png")
	theImage = ImageTk.PhotoImage(pil_image)
	canvas.itemconfigure(display, image=theImage)

root = tk.Tk()
root.title("There's an XKCD for Everything")
root.geometry('800x480')
h = tk.Scrollbar(root, orient="horizontal")
v = tk.Scrollbar(root, orient="vertical")
canvas = tk.Canvas(root, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v.set, xscrollcommand=h.set)
h['command'] = canvas.xview
v['command'] = canvas.yview


url = 'https://c.xkcd.com/random/comic/'
res = requests.get(url)
html_page = res.content
soup = BeautifulSoup(html_page, 'html.parser')
images = soup.findAll('img')
images = images[2]
images = images['src']
images = "http:" + images
img_data = requests.get(images).content
with open('xkcd.png', 'wb') as handler:
    handler.write(img_data)
pil_image = Image.open("xkcd.png")
theImage = ImageTk.PhotoImage(pil_image)
display = canvas.create_image(0,0,image=theImage, anchor='nw')
canvas.grid(column=0, row=0, sticky=("N","W","E","S"))

canvas.bind_all('<MouseWheel>', on_vertical)
canvas.bind_all('<Shift-MouseWheel>', on_horizontal)

h.grid(column=0, row=1, sticky=("W","E"))
v.grid(column=1, row=0, sticky=("N","S"))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

frame3 = tk.Frame(root, borderwidth=0, relief='ridge')
frame3.grid(column=0, row=2, columnspan=2)

button = tk.Button(frame3,text="Random",command=pressed)
button.grid(row=2,column=0)

close = tk.Button(frame3, text = "Exit", command = close_window)
close.grid(row=2,column=1)

root.mainloop()
