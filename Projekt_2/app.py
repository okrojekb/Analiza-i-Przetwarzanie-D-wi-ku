from tkinter import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from functions import *

root = Tk()
root.title("Analiza i przetwarzanie dźwięku - Projekt 1 - cechy sygnału audio w dziedzinie czasu")
root.geometry('1200x700')

sample_rate = None
audio_data = None
func_nr = -1
scroll_pos = 0

menu = Menu(root)
root.config(menu=menu)

upload_menu = Menu(menu, tearoff=0)
upload_menu.add_command(label='Załaduj plik',
                        command=lambda: menu_function(fig1, canvas1, sl, 1, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5,v.get()))
upload_menu.add_command(label='Odtwórz nagranie',
                        command=lambda: menu_function(fig1, canvas1, sl, 11, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5,v.get()))
menu.add_cascade(label='Plik', menu=upload_menu)

params_menu = Menu(menu, tearoff=0)
params_menu.add_command(label='Głośność',
                        command=lambda: menu_function(fig2, canvas2, sl, 2, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5,v.get()))
params_menu.add_command(label='Short Time Energy (STE)',
                        command=lambda: menu_function(fig2, canvas2, sl, 3, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5,v.get()))
params_menu.add_command(label='Zero Crossing Rate (ZCR)',
                        command=lambda: menu_function(fig2, canvas2, sl, 4, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5,v.get()))
params_menu.add_command(label='Silent Ratio (SR)',
                        command=lambda: menu_function(fig2, canvas2, sl, 5, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5,v.get()))

params_menu.add_command(label='Częstotliwość tonu podstawowego F0 - z autokorelacji',
                        command=lambda: menu_function(fig2, canvas2, sl, 6, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5,v.get()))

params_menu.add_command(label='Częstotliwość tonu podstawowego F0 - z AMDF',
                        command=lambda: menu_function(fig2, canvas2, sl, 7, scrollbar, scrollbar2, slider2, slider3,
                                                      labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5,v.get()))

menu.add_cascade(label='Parametry na poziomie ramki', menu=params_menu)

clip_params_menu = Menu(menu, tearoff=0)

clip_params_menu.add_command(label='Bazujące na głośności: VSTD, VDR, VU',
                             command=lambda: menu_function(fig2, canvas2, sl, 8, scrollbar, scrollbar2, slider2,
                                                           slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3,
                                                           rbtn4, rbtn5,v.get()))

clip_params_menu.add_command(label='Bazujące na energii: LSTER, Energy Entropy',
                             command=lambda: menu_function(fig2, canvas2, sl, 9, scrollbar, scrollbar2, slider2,
                                                           slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3,
                                                           rbtn4, rbtn5,v.get()))

clip_params_menu.add_command(label='Bazujące na ZCR: ZSTD, HZCRR',
                             command=lambda: menu_function(fig2, canvas2, sl, 10, scrollbar, scrollbar2, slider2,
                                                           slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3,
                                                           rbtn4, rbtn5,v.get()))

menu.add_cascade(label='Parametry na poziomie klipu', menu=clip_params_menu)

analiza_menu = Menu(menu, tearoff=0)

analiza_menu.add_command(label='Detekcja ciszy',
                         command=lambda: menu_function(fig2, canvas2, sl, 12, scrollbar, scrollbar2, slider2,
                                                       slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4,
                                                       rbtn5,v.get()))

analiza_menu.add_command(label='Określenie fragmentów dźwięcznych / bezdźwięcznych',
                         command=lambda: menu_function(fig2, canvas2, sl, 13, scrollbar, scrollbar2, slider2,
                                                       slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4,
                                                       rbtn5,v.get()))

analiza_menu.add_command(label='Określenie fragmentów muzyka / mowa',
                         command=lambda: menu_function(fig2, canvas2, sl, 14, scrollbar, scrollbar2, slider2,
                                                       slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4,
                                                       rbtn5,v.get()))

menu.add_cascade(label='Analiza sygnału', menu=analiza_menu)

domain_trans_menu = Menu(menu, tearoff=0)

# domain_trans_menu.add_command(label='Wykres widma częstotliwościowego całego sygnału',
#                              command=lambda: menu_function(fig2, canvas2, sl, 19, scrollbar, scrollbar2, slider2,
#                                                            slider3, labelVSTD, canvas_widget2))

domain_trans_menu.add_command(label='Wykres widma częstotliwościowego',
                              command=lambda: menu_function(fig2, canvas2, sl, 20, scrollbar, scrollbar2, slider2,
                                                            slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3,
                                                            rbtn4, rbtn5,v.get()))

# domain_trans_menu.add_command(label='Wykres sygnału w dziedzinie czasu i częstotliwości po funkcji okna',
#                              command=lambda: menu_function(fig2, canvas2, sl, 18, scrollbar, scrollbar2, slider2,
#                                                            slider3, labelVSTD, canvas_widget2))

# 19
domain_trans_menu.add_command(label='Wykres sygnału w dziedzinie czasu i częstotliwości po funkcji okna',
                              command=lambda: plot_window_effect(fig1, canvas1, fig2, canvas2, sl.get(), scrollbar,
                                                                 scrollbar2, slider2, canvas_widget2, rbtn1, rbtn2,
                                                                 rbtn3, rbtn4, rbtn5,v.get()))

menu.add_cascade(label='Transformacja na dziedzinę częstotliwości', menu=domain_trans_menu)

param_freq_menu = Menu(menu, tearoff=0)

param_freq_menu.add_command(label='Głośność (Volume)',
                            command=lambda: menu_function(fig2, canvas2, sl, 21, scrollbar, scrollbar2, slider2,
                                                          slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3,
                                                          rbtn4, rbtn5,v.get()))

param_freq_menu.add_command(label='Frequency Centroid (FC)',
                            command=lambda: menu_function(fig2, canvas2, sl, 22, scrollbar, scrollbar2, slider2,
                                                          slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3,
                                                          rbtn4, rbtn5,v.get()))

param_freq_menu.add_command(label='Effective Bandwidth (BW)',
                            command=lambda: menu_function(fig2, canvas2, sl, 23, scrollbar, scrollbar2, slider2,
                                                          slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3,
                                                          rbtn4, rbtn5,v.get()))

param_freq_menu.add_command(label='Band Energy (BE)',
                            command=lambda: menu_function(fig2, canvas2, sl, 24, scrollbar, scrollbar2, slider2,
                                                          slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3,
                                                          rbtn4, rbtn5,v.get()))

param_freq_menu.add_command(label='Band Energy Ratio (BER or ERSB)',
                            command=lambda: menu_function(fig2, canvas2, sl, 25, scrollbar, scrollbar2, slider2,
                                                          slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3,
                                                          rbtn4, rbtn5,v.get()))

param_freq_menu.add_command(label='Spectral Flatness Measure (SFM)',
                            command=lambda: menu_function(fig2, canvas2, sl, 26, scrollbar, scrollbar2, slider2,
                                                          slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3,
                                                          rbtn4, rbtn5,v.get()))

param_freq_menu.add_command(label='Spectral Crest Factor (SCF)',
                            command=lambda: menu_function(fig2, canvas2, sl, 27, scrollbar, scrollbar2, slider2,
                                                          slider3, labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3,
                                                          rbtn4, rbtn5,v.get()))

menu.add_cascade(label='Parametry z dziedziny częstotliwości', menu=param_freq_menu)

fig1 = Figure(figsize=(11, 3), dpi=100)

canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas_widget1 = canvas1.get_tk_widget()
canvas_widget1.grid(column=0, row=2, columnspan=11, rowspan=3, padx=10, pady=10)

fig2 = Figure(figsize=(11, 3), dpi=100)
canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas_widget2 = canvas2.get_tk_widget()
canvas_widget2.grid(column=0, row=7, columnspan=11, rowspan=3, padx=10, pady=10)

slider2 = Scale(root, from_=0, to=10000, orient=VERTICAL, label="RMS level", length=300,
                command=lambda value: slider_function(sl, fig2, canvas2, slider2, slider3, labelVSTD, scrollbar2,
                                                      scrollbar, fig1, canvas1, canvas_widget2, rbtn1, rbtn2, rbtn3,
                                                      rbtn4, rbtn5, v.get()))
slider2.set(5)
slider2.grid(column=12, row=2, rowspan=3, padx=10, pady=10)
slider2.grid_remove()

slider3 = Scale(root, from_=0, to=100, orient=VERTICAL, label="ZCR level", length=300,
                command=lambda value: slider_function(sl, fig2, canvas2, slider2, slider3, labelVSTD, scrollbar2,
                                                      scrollbar, fig1, canvas1, canvas_widget2, rbtn1, rbtn2, rbtn3,
                                                      rbtn4, rbtn5, v.get()))
slider3.set(10)
slider3.grid(column=13, row=2, rowspan=3, padx=10, pady=10)
slider3.grid_remove()

sl = Scale(root, from_=1, to=600, orient=VERTICAL, label="Wielkość ramki", length=300,
           command=lambda value: slider_function(sl, fig2, canvas2, slider2, slider3, labelVSTD, scrollbar2, scrollbar,
                                                 fig1, canvas1, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5, v.get()))
sl.set(220)
sl.grid(column=12, row=6, rowspan=3, padx=10, pady=10)
sl.grid_remove()

scrollbar = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=1100,
                  command=lambda value: scroll_function1(fig1, canvas1, int(value), sl, scrollbar, scrollbar2))
scrollbar.grid(column=0, row=6, columnspan=12, padx=10, pady=10)
scrollbar.grid_remove()

scrollbar2 = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=1100,
                   command=lambda value: scroll_function(fig2, canvas2, int(value), sl, slider2, slider3, scrollbar,
                                                         scrollbar2, fig1, canvas1, fig2, canvas2, canvas_widget2,
                                                         rbtn1, rbtn2, rbtn3, rbtn4, rbtn5, v.get()))
scrollbar2.grid(column=0, row=10, columnspan=12, padx=10, pady=10)
scrollbar2.grid_remove()

labelVSTD = Label(root, text="", font=("Arial", 12), wraplength=1000, )  # Początkowo pusta
labelVSTD.grid(column=0, row=6, padx=10, pady=10)
labelVSTD.grid_remove()

play_button = Button(root, text="Odtwórz audio", command=lambda: play_audio())
play_button.grid(column=10, row=11, columnspan=1, padx=10, pady=10)

v = IntVar()
v.set(1)
rbtn1 = Radiobutton(root, text='okno prostokątne', variable=v, value=1,
                    command=lambda: button_function(fig2, canvas2, sl, scrollbar, scrollbar2, slider2, slider3,
                                                    labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5, v.get(),
                                                    fig1, canvas1, canvas_widget2))
rbtn2 = Radiobutton(root, text='okno trójkatne', variable=v, value=2,
                    command=lambda: button_function(fig2, canvas2, sl, scrollbar, scrollbar2, slider2, slider3,
                                                    labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5, v.get(),
                                                    fig1, canvas1, canvas_widget2))
rbtn3 = Radiobutton(root, text='okno Hamminga', variable=v, value=3,
                    command=lambda: button_function(fig2, canvas2, sl, scrollbar, scrollbar2, slider2, slider3,
                                                    labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5, v.get(),
                                                    fig1, canvas1, canvas_widget2))
rbtn4 = Radiobutton(root, text='okno van Hanna', variable=v, value=4,
                    command=lambda: button_function(fig2, canvas2, sl, scrollbar, scrollbar2, slider2, slider3,
                                                    labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5, v.get(),
                                                    fig1, canvas1, canvas_widget2))
rbtn5 = Radiobutton(root, text='okno Blackmana', variable=v, value=5,
                    command=lambda: button_function(fig2, canvas2, sl, scrollbar, scrollbar2, slider2, slider3,
                                                    labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5, v.get(),
                                                    fig1, canvas1, canvas_widget2))

rbtn1.grid(row=6, column=13, padx=5, pady=5, sticky=W)
rbtn2.grid(row=7, column=13, padx=5, pady=5, sticky=W)
rbtn3.grid(row=8, column=13, padx=5, pady=5, sticky=W)
rbtn4.grid(row=9, column=13, padx=5, pady=5, sticky=W)
rbtn5.grid(row=10, column=13, padx=5, pady=5, sticky=W)
rbtn1.grid_remove()
rbtn2.grid_remove()
rbtn3.grid_remove()
rbtn4.grid_remove()
rbtn5.grid_remove()

root.mainloop()
