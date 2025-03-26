from tkinter import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from functions import *

# Create main window
root = Tk()
root.title("Analiza i przetwarzanie dźwięku - Projekt 1 - cechy sygnału audio w dziedzinie czasu")
root.geometry('1200x700')

sample_rate = None
audio_data = None
func_nr = -1
scroll_pos = 0

# Create a menu bar
menu = Menu(root)
root.config(menu=menu)

# Submenus
upload_menu = Menu(menu, tearoff=0)
upload_menu.add_command(label='Załaduj plik',
                        command=lambda: menu_function(fig1, canvas1, sl, 1, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2))
upload_menu.add_command(label='Odtwórz nagranie',
                        command=lambda: menu_function(fig1, canvas1, sl, 10, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2))
menu.add_cascade(label='Plik', menu=upload_menu)

# Submenus
params_menu = Menu(menu, tearoff=0)
params_menu.add_command(label='Głośność',
                        command=lambda: menu_function(fig2, canvas2, sl, 2, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2))
params_menu.add_command(label='Short Time Energy (STE)',
                        command=lambda: menu_function(fig2, canvas2, sl, 3, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2))
params_menu.add_command(label='Zero Crossing Rate (ZCR)',
                        command=lambda: menu_function(fig2, canvas2, sl, 4, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2))
params_menu.add_command(label='Silent Ratio (SR)',
                        command=lambda: menu_function(fig2, canvas2, sl, 5, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2))

params_menu.add_command(label='Częstotliwość tonu podstawowego F0 - z autokorelacji',
                        command=lambda: menu_function(fig2, canvas2, sl, 6, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2))

params_menu.add_command(label='Częstotliwość tonu podstawowego F0 - z AMDF',
                        command=lambda: menu_function(fig2, canvas2, sl, 7, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2))

menu.add_cascade(label='Parametry na poziomie klipu', menu=params_menu)

clip_params_menu = Menu(menu, tearoff=0)

clip_params_menu.add_command(label='Bazujące na głośności: VSTD, VDR, VU',
                             command=lambda: menu_function(fig2, canvas2, sl, 8, scrollbar, scrollbar2, slider2,
                                                           slider3, labelVSTD, canvas_widget2))

clip_params_menu.add_command(label='Bazujące na energii: LSTER, Energy Entropy',
                             command=lambda: menu_function(fig2, canvas2, sl, 9, scrollbar, scrollbar2, slider2,
                                                           slider3, labelVSTD, canvas_widget2))

menu.add_cascade(label='Parametry na poziomie ramki', menu=clip_params_menu)

# Tworzenie figury matplotlib
fig1 = Figure(figsize=(11, 3), dpi=100)

canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas_widget1 = canvas1.get_tk_widget()
canvas_widget1.grid(column=0, row=2, columnspan=11, rowspan=2, padx=10, pady=10)

# Tworzenie figury matplotlib
fig2 = Figure(figsize=(11, 3), dpi=100)
canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas_widget2 = canvas2.get_tk_widget()
canvas_widget2.grid(column=0, row=6, columnspan=11, rowspan=2, padx=10, pady=10)

slider2 = Scale(root, from_=0, to=10000, orient=VERTICAL, label="RMS level", length=300,
                command=lambda value: slider_function(sl, fig2, canvas2, slider2, slider3, labelVSTD))
slider2.set(0)
slider2.grid(column=12, row=2, rowspan=2, padx=10, pady=10)
slider2.grid_remove()

slider3 = Scale(root, from_=0, to=100, orient=VERTICAL, label="ZCR level", length=300,
                command=lambda value: slider_function(sl, fig2, canvas2, slider2, slider3, labelVSTD))
slider3.set(10)
slider3.grid(column=13, row=2, rowspan=2, padx=10, pady=10)
slider3.grid_remove()

sl = Scale(root, from_=1, to=600, orient=VERTICAL, label="Wielkość ramki", length=300,
           command=lambda value: slider_function(sl, fig2, canvas2, slider2, slider3, labelVSTD))
sl.set(220)
sl.grid(column=12, row=6, rowspan=2, padx=10, pady=10)
sl.grid_remove()

scrollbar = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=1100,
                  command=lambda value: scroll_function1(fig1, canvas1, int(value), sl, scrollbar, scrollbar2))
scrollbar.grid(column=0, row=5, columnspan=12, padx=10, pady=10)
scrollbar.grid_remove()

scrollbar2 = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=1100,
                   command=lambda value: scroll_function(fig2, canvas2, int(value), sl, slider2, slider3, scrollbar,
                                                         scrollbar2))
scrollbar2.grid(column=0, row=8, columnspan=12, padx=10, pady=10)
scrollbar2.grid_remove()

labelVSTD = Label(root, text="", font=("Arial", 12), wraplength=1000, )  # Początkowo pusta
labelVSTD.grid(column=0, row=6, padx=10, pady=10)
labelVSTD.grid_remove()

play_button = Button(root, text="Odtwórz audio", command=lambda: play_audio())
play_button.grid(column=10, row=9, columnspan=1, padx=10, pady=10)

root.mainloop()
