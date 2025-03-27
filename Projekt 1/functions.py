from tkinter import filedialog

import sounddevice as sd
from scipy.io import wavfile
import math
import numpy as np



def menu_function(fig, canvas, slider, function_nr, scrollbar, scrollbar2, slider2, slider3, label, canvas_widget):
    slider2.grid_remove()
    slider3.grid_remove()
    label.grid_remove()
    canvas_widget.grid()
    if function_nr == 1:
        slider.grid_remove()
        scrollbar.set(0)
        scrollbar.grid()
        scrollbar2.grid_remove()
        load_audio(fig, canvas, scrollbar, scrollbar2)
    elif function_nr > 1 and function_nr <= 7:
        slider.configure(to=0.25*sample_rate, from_=1)
        slider.set(0.02*sample_rate)
        slider.grid()
        scrollbar2.grid()
        if len(audio_data) > 20000:
            max_scroll = (len(audio_data) - 20000) // slider.get()  # Zakres przewijania w krokach

        else:
            scrollbar.grid_remove()
            scrollbar2.grid_remove()
        if function_nr == 2:
            calculate_volume_and_plot(slider.get(), fig, canvas)
        elif function_nr == 3:
            calculate_STE_and_plot(slider.get(), fig, canvas)
        elif function_nr == 4:
            calculate_ZCR_and_plot(slider.get(), fig, canvas)
        elif function_nr == 5:
            slider2.set(0.05 * max(audio_data))
            slider2.config(to=max(audio_data), label="volume level")

            slider2.grid()
            slider3.set(3)
            slider3.config(label="ZCR level")

            slider3.grid()
            SilentRatio(slider.get(), fig, canvas, slider2.get(), slider3.get())
        elif function_nr == 6:
            # slider2.grid()
            calculate_f0_autocorrelation(slider.get(), fig, canvas)
        elif function_nr == 7:
            calculate_f0_AMDF(slider.get(), fig, canvas)
    elif function_nr >= 8 and function_nr < 11:
        slider2.grid_remove()
        slider3.grid_remove()
        scrollbar2.grid_remove()
        canvas_widget.grid_remove()
        slider.grid()
        if function_nr == 8:
            calculate_VSTD(slider.get(), label)
        elif function_nr == 9:
            slider2.grid()
            slider2.set(50)
            slider2.configure(to=slider.get() // 2, from_=1, label="segment size")
            calculate_LSTER(slider.get(), label, slider2.get())
        elif function_nr == 10:
            calculate_klip_ZCR(slider.get(), label)
    elif function_nr == 11:
        play_audio()
    else:
        if len(audio_data) > 80000:
            max_scroll = (len(audio_data) - 80000) // slider.get()  # Zakres przewijania w krokach
            scrollbar2.grid()
            scrollbar2.config(to=max_scroll)
        else:
            scrollbar2.grid_remove()
        if function_nr == 12:
            slider.grid()
            # slider.
            slider2.set(5)
            scrollbar2.grid()
            # slider2.config(to=max(audio_data), label="volume level")
            slider2.config(to=100, label="volume level")

            slider2.grid()
            slider3.set(3)
            slider3.config(label="ZCR level")

            slider3.grid()
            silence_detection(slider.get(), fig, canvas, slider2.get(), slider3.get())

        elif function_nr == 13:
            slider.grid()
            # slider.
            slider2.set(5)
            # scrollbar2.grid()
            # slider2.config(to=max(audio_data), label="volume level")
            slider2.config(to=100, label="volume level")

            slider2.grid()

            sound_detection(slider.get(), fig, canvas, slider2)
        elif function_nr == 14:
            # slider2.set(sample_rate)
            scrollbar2.grid()
            # slider2.config(to=max(audio_data), label="volume level")
            # slider2.config(to=100, label="volume level")
            #
            # slider2.grid()
            if len(audio_data) > 176400:
                max_scroll = 10*(len(audio_data) - 176400) // slider.get()  # Zakres przewijania w krokach
                scrollbar2.grid()
                scrollbar2.config(to=max_scroll)
            else:
                scrollbar2.grid_remove()
            differentiate(slider.get(), fig, canvas)


def plot_audio_waveform(sample_rate, audio_data, fig, canvas, start_idx=0, max_points=20000):
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]

    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(time, visible_audio, color='blue')
    ax.set_title("Przebieg czasowy pliku audio")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Amplituda")
    ax.set_ylim(min(audio_data), max(audio_data))
    ax.grid(True)
    fig.tight_layout()
    canvas.draw()


def load_audio(fig, canvas, scrollbar, scrollbar2):
    print("new")
    global func_nr
    func_nr = 1
    filepath = filedialog.askopenfilename(
        filetypes=[("WAV Files", "*.wav")]
    )
    if filepath:
        try:
            global sample_rate
            global audio_data
            sample_rate, audio_data = wavfile.read(filepath)
            if len(audio_data.shape) == 2:
                audio_data = np.mean(audio_data, axis=1).astype(np.int16)
            print(f"Częstotliwość próbkowania: {sample_rate} Hz")
            print(f"Długość danych audio: {len(audio_data)} próbek")
            if len(audio_data) > 20000:
                max_scroll = (len(audio_data) - 20000) // 200  # Zakres przewijania w krokach
                scrollbar.configure(to=max_scroll)
                scrollbar2.configure(to=max_scroll)
            else:
                scrollbar.grid_remove()
                scrollbar2.grid_remove()

            plot_audio_waveform(sample_rate, audio_data, fig, canvas)
            print("fin show")

        except Exception as e:
            print(f"Wystąpił błąd: {e}")
            return None, None


def play_audio():
    """
    Funkcja odtwarzająca nagranie audio.
    """
    # global func_nr
    # func_nr = 11
    global sample_rate, audio_data

    # Sprawdzamy, czy dane audio zostały wczytane
    if audio_data is None or sample_rate is None:
        print("Brak danych audio do odtworzenia.")
        return

    try:
        # Odtwarzanie audio za pomocą sounddevice
        sd.play(audio_data, samplerate=sample_rate)

        # Czekamy, aż odtwarzanie się zakończy
        sd.wait()

    except Exception as e:
        print(f"Wystąpił błąd podczas odtwarzania dźwięku: {e}")


def calculate_volume_and_plot(frame_size, fig, canvas, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 2

    # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]

    # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
    visible_num_frames = len(visible_audio) // frame_size
    rms = []
    rms_time = []

    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = audio_data[frame_start:frame_end]

        rms_value = (sum(((x ** 2) / len(frame)) for x in frame)) ** 0.5
        rms.append(rms_value)
        rms_time.append(frame_start / sample_rate)

    # Rysowanie wykresu
    fig.clear()
    ax = fig.add_subplot(111)

    # Tworzenie wykresu audio
    ax.plot(time, visible_audio, label='Przebieg czasowy (audio)', color='blue', alpha=0.6, linewidth=0.5)

    # Tworzenie wykresu RMS
    ax.plot(rms_time, rms, label='Głośność (RMS)', color='red', linewidth=2)

    ax.set_title("Przebieg czasowy pliku audio i głośność (RMS)")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Amplituda / Głośność")
    ax.grid(True)
    ax.set_ylim(min(audio_data) * 0.9, max(audio_data) * 1.1)
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def calculate_STE_and_plot(frame_size, fig, canvas, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 3

    # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]

    # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
    visible_num_frames = len(visible_audio) // frame_size
    rms = []
    rms_time = []

    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = audio_data[frame_start:frame_end]

        rms_value = (sum(((x ** 2) / len(frame)) for x in frame))
        rms.append(rms_value)
        rms_time.append(frame_start / sample_rate)

    # Rysowanie wykresu
    fig.clear()
    ax = fig.add_subplot(111)

    ax.plot(rms_time, rms, label='Short Time Energy (STE)', color='red', linewidth=2)

    ax.set_title("Short Time Energy (STE)")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("STE")
    ax.grid(True)
    ax.set_ylim(0, max(max(rms) * 1.05, 300000))
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def signum(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1


def calculate_ZCR_and_plot(frame_size, fig, canvas, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 4

    # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]

    # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
    visible_num_frames = len(visible_audio) // frame_size
    zcr = []
    zcr_time = []

    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = audio_data[frame_start:frame_end]

        zcr_val = (sum(abs(signum(frame[x]) - signum(frame[x + 1])) for x in range(len(frame) - 1))) / (2 * len(frame))
        zcr.append(zcr_val)
        zcr_time.append(frame_start / sample_rate)

    # Rysowanie wykresu
    fig.clear()
    ax = fig.add_subplot(111)

    ax.plot(zcr_time, zcr, label='Zero Crossing Rate (ZCR)', color='red', linewidth=2)

    ax.set_title("Zero Crossing Rate (ZCR)")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("ZCR")
    ax.set_ylim(0, max(max(zcr) * 1.1, 0.8))
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    canvas.draw()

def silence_detection(frame_size, fig, canvas, vol_level, zcr_level, start_idx=0, max_points=80000):
    global func_nr
    func_nr = 12
    # max_points = len(audio_data)
    max_val = max(abs(x) for x in audio_data)
    audio_data_sk = [x / max_val for x in audio_data]
    # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data_sk[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]

    # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
    visible_num_frames = len(audio_data_sk) // frame_size
    silent = []
    silent_time = []
    zcr = []
    vol = []

    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = audio_data_sk[frame_start:frame_end]
        if len(frame) == 0:
            break
        zcr_val = (sum(abs(signum(frame[x]) - signum(frame[x + 1])) for x in range(len(frame) - 1))) / (2 * len(frame))
        vol_value = (sum(((x ** 2) / len(frame)) for x in frame)) ** 0.5
        zcr.append(zcr_val)
        vol.append(vol_value)
        if (zcr_val < zcr_level / 100 and vol_value < vol_level / 100):
            silent.append(1)
        else:
            silent.append(0)
        silent_time.append(frame_start / sample_rate)
    # Rysowanie wykresu
    fig.clear()
    ax = fig.add_subplot(111)
    # ax.fill_betweenx(silent, 0, silent_time, color='grey', alpha = 0.2)  # Poprawne kolorowanie obszaru pod wykresem
    ax.fill_between(silent_time, silent, color='grey', alpha = 0.2)  # Poprawne kolorowanie obszaru pod wykresem

    ax.plot(silent_time, silent, label='Silent Ratio (SR)', color='red', linewidth=2)

    ax.plot(silent_time, zcr, label='ZCR', color='green', linewidth=1)
    ax.plot(silent_time, vol, label='VOL', color='yellow', linewidth=1)

    ax.plot(time, visible_audio, label='Przebieg czasowy (audio)', color='blue', alpha=0.4, linewidth=0.5)

    ax.set_title("Silent Ratio (SR)")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("SR")
    ax.grid(True)
    ax.set_ylim(0, 0.5)

    ax.legend()
    fig.tight_layout()
    canvas.draw()


def SilentRatio(frame_size, fig, canvas, vol_level, zcr_level, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 5
    # max_points = len(audio_data)
    # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]

    # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
    visible_num_frames = len(visible_audio) // frame_size
    silent = []
    silent_time = []

    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = audio_data[frame_start:frame_end]

        zcr_val = (sum(abs(signum(frame[x]) - signum(frame[x + 1])) for x in range(len(frame) - 1))) / (2 * len(frame))
        vol_value = (sum(((x ** 2) / len(frame)) for x in frame)) ** 0.5
        if (zcr_val < zcr_level / 100 and vol_value < vol_level):
            silent.append(1)
        else:
            silent.append(0)
        silent_time.append(frame_start / sample_rate)
    # Rysowanie wykresu
    fig.clear()
    ax = fig.add_subplot(111)

    ax.plot(silent_time, silent, label='Silent Ratio (SR)', color='red', linewidth=2)

    ax.set_title("Silent Ratio (SR)")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("SR")
    ax.grid(True)
    ax.set_ylim(0, 1.1)

    ax.legend()
    fig.tight_layout()
    canvas.draw()


# Funkcja min-max scaling
def min_max_scaling(data, new_min=0, new_max=1):
    """Funkcja do skalowania danych na zakres [new_min, new_max] przy użyciu metody min-max."""
    if len(data) == 0:
        return data
    data_min = np.min(data)
    data_max = np.max(data)
    if (data_max - data_min) != 0:

        return new_min + (data - data_min) * (new_max - new_min) / (data_max - data_min)
    else:
        if data_max == 0:
            return np.ones(len(data)) * new_min
        else:
            return np.ones(len(data)) * new_max

def sound_detection(frame_size, fig, canvas, slider2, start_idx=0, max_points=80000):
    global func_nr
    func_nr = 13
    cut_off = slider2.get()  # Próg ciszy ustawiony za pomocą suwaka
    # # max_points = len(audio_data)
    # start_idx = 0
    # time = [i / sample_rate for i in range(start_idx, end_idx)]
    #
    # # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
    # end_idx = min(start_idx + max_points, len(audio_data))
    # visible_audio = audio_data[start_idx:end_idx]
    # time = [i / sample_rate for i in range(start_idx, end_idx)]

    max_val = max(abs(x) for x in audio_data)
    audio_data_sk = [x / max_val for x in audio_data]
    # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data_sk[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]

    # max_val = max(abs(x) for x in audio_data)
    # audio_data_sk = [x / max_val for x in audio_data]
    # # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
    # end_idx = min(start_idx + max_points, len(audio_data))
    # visible_audio = audio_data[start_idx:end_idx]
    # time = [i / sample_rate for i in range(start_idx, end_idx)]


    visible_num_frames = len(visible_audio) // frame_size
    f0 = []
    f0_time = []
    silent = []

    # Obliczanie wartości F0 i sprawdzanie ciszy
    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = audio_data[frame_start:frame_end]
        frame = [float(x) for x in frame]

        # Obliczanie autokorelacji
        autocorr = [sum(frame[i] * frame[i + lag] for i in range(len(frame) - lag)) for lag in range(len(frame))]
        if len(autocorr) <= 1:
            break
        lag = autocorr.index(max(autocorr[1:]))  # Ignorujemy zerowy lag
        f0_val = sample_rate / lag if lag != 0 else 0
        f0.append(f0_val)
        f0_time.append(frame_start / sample_rate)

        # Sprawdzamy, czy F0 jest mniejsze niż cut_off (cisza)
        if f0_val < cut_off:
            silent.append(1)
        else:
            silent.append(0)

    # Przeskalowanie danych audio do zakresu [0, 1]
    scaled_audio = min_max_scaling(np.array(visible_audio), 0, 1)
    print(f0)
    # Przeskalowanie wartości F0 do zakresu [0, 1]
    scaled_f0 = min_max_scaling(np.array(f0), 0, 1)
    print(scaled_f0)
    print("min, max",max(f0) - min(f0))
    if max(f0) - min(f0) != 0:
        scaled_cut_off = max(0,(cut_off - min(f0)) / (max(f0) - min(f0))) # Używamy [cut_off] jako tablicy
    else:
        scaled_cut_off = max(0,cut_off)
    print("cut", cut_off)
    print("scaled: ", scaled_cut_off)

    # ax.fill_between(silent_time, silent, color='grey', alpha = 0.2)  # Poprawne kolorowanie obszaru pod wykresem

    # ax.plot(silent_time, silent, label='Silent Ratio (SR)', color='red', linewidth=2)

    # ax.plot(silent_time, zcr, label='ZCR', color='green', linewidth=1)
    # ax.plot(silent_time, vol, label='VOL', color='yellow', linewidth=1)

    # ax.plot(time, visible_audio, label='Przebieg czasowy (audio)', color='blue', alpha=0.4, linewidth=0.5)



    # Ustawienie wartości suwaka dla poziomu ciszy
    slider2.config(to=max(f0), label="Poziom bezdźwięczności")
    slider2.grid()

    # Rysowanie wykresu
    fig.clear()
    ax = fig.add_subplot(111)

    # Narysowanie przeskalowanego audio
    ax.plot(time, scaled_audio, label='Przeskalowane nagranie audio', color='blue', alpha=0.4, linewidth=0.5)

    # Narysowanie przeskalowanego F0
    ax.plot(f0_time, scaled_f0, label='Przeskalowane F0', color='red', linewidth=2)

    # Zaznaczenie fragmentów ciszy (gdzie F0 < cut_off)
    # for i in range(len(silent)):
    #     if silent[i] == 1:  # Jeżeli F0 < cut_off, to zaznaczamy ciszę
    #         ax.fill_between(f0_time[i:i+2], 0, scaled_f0[i:i+2], color='green', alpha=0.3, label='Cisza')

    # Dodanie linii na poziomie cut_off
    ax.axhline(y=scaled_cut_off, color='blue', linestyle='--', label=f'Cut Off ({cut_off} Hz)')

    # Ustawienia wykresu
    ax.set_title("Częstotliwość tonu podstawowego F0 - Autokorelacja")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Wartości skalowane")
    ax.grid(True)
    ax.set_ylim(0, 1.1)  # Zakres dla wartości skalowanych
    ax.legend()
    fig.tight_layout()
    canvas.draw()


# def sound_detection(frame_size, fig, canvas, slider2, start_idx=0, max_points=10000):
#     global func_nr
#     func_nr = 6
#     cut_off = slider2.get()
#     max_points = len(audio_data)
#     start_idx = 0
#     # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
#     end_idx = min(start_idx + max_points, len(audio_data))
#     visible_audio = audio_data[start_idx:end_idx]
#     time = [i / sample_rate for i in range(start_idx, end_idx)]
#
#     visible_num_frames = len(visible_audio) // frame_size
#     f0 = []
#     f0_time = []
#     silent = []
#
#     for i in range(visible_num_frames):
#         frame_start = start_idx + i * frame_size
#         frame_end = min(frame_start + frame_size, end_idx)
#         frame = audio_data[frame_start:frame_end]
#         frame = [float(x) for x in frame]
#
#         # Obliczanie autokorelacji
#         autocorr = [sum(frame[i] * frame[i + lag] for i in range(len(frame) - lag)) for lag in range(len(frame))]
#         lag = autocorr.index(max(autocorr[1:]))  # Ignorujemy zerowy lag
#         f0_val = sample_rate / lag if lag != 0 else 0
#         f0.append(f0_val)
#         f0_time.append(frame_start / sample_rate)
#
#         # Sprawdzamy, czy F0 jest mniejsze niż cut_off
#         if f0_val < cut_off:
#             silent.append(1)
#         else:
#             silent.append(0)
#     # slider2.set(0.1*max(f0))
#     # slider2.config(to=max(audio_data), label="volume level")
#     slider2.config(to=max(f0), label="poziom bezdźwięczności")
#
#     slider2.grid()
#     # Rysowanie wykresu
#     fig.clear()
#     ax = fig.add_subplot(111)
#
#     ax.plot(f0_time, f0, label='Fundamental Frequency (F0)', color='red', linewidth=2)
#     ax.axhline(y=cut_off, color='blue', linestyle='--', label=f'Cut Off ({cut_off} Hz)')
#
#     # # Zaznaczenie fragmentów ciszy (gdzie F0 < cut_off)
#     # for i in range(len(silent)):
#     #     if silent[i] == 1:  # Jeżeli F0 < cut_off, to zaznaczamy ciszę
#     #         ax.fill_between(f0_time[i:i+2], 0, f0[i:i+2], color='red', alpha=0.2)
#
#     ax.set_title("Częstotliwość tonu podstawowego F0 - Autokorelacja")
#     ax.set_xlabel("Czas [s]")
#     ax.set_ylabel("F0 (Hz)")
#     ax.grid(True)
#     ax.set_ylim(min(min(f0) * 0.9, 0), max(max(f0) * 1.1, 23000))
#     ax.legend()
#     fig.tight_layout()
#     canvas.draw()


def calculate_f0_autocorrelation(frame_size, fig, canvas, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 6

    # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]

    visible_num_frames = len(visible_audio) // frame_size
    f0 = []
    f0_time = []

    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = audio_data[frame_start:frame_end]
        frame = [float(x) for x in frame]

        autocorr = [sum(frame[i] * frame[i + lag] for i in range(len(frame) - lag)) for lag in range(len(frame))]
        lag = autocorr.index(max(autocorr[1:]))
        print(lag)
        f0_val = sample_rate / lag if lag != 0 else 0
        # f0_val = 1 / (lag) if lag != 0 else 0
        f0.append(f0_val)
        f0_time.append(frame_start / sample_rate)
    # Rysowanie wykresu
    fig.clear()
    ax = fig.add_subplot(111)

    ax.plot(f0_time, f0, label='(Fundamental Frequency', color='red', linewidth=2)

    ax.set_title("Częstotliwość tonu podstawowego F0 - autokorelacja")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("F0")
    ax.grid(True)
    print(min(f0) * 0.9)
    ax.set_ylim(min(min(f0) * 0.9, 0), max(max(f0) * 1.1, 23000))
    # ax.set_ylim(min(min(f0)*0.9, 0), max(f0)*1.1)
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def calculate_f0_AMDF(frame_size, fig, canvas, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 7

    # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]

    visible_num_frames = len(visible_audio) // frame_size
    f0 = []
    f0_time = []

    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = audio_data[frame_start:frame_end]
        frame = [float(x) for x in frame]

        amdf = [sum(abs(frame[i] - frame[i + lag]) for i in range(len(frame) - lag)) for lag in range(1, len(frame))]

        max_lag = 0
        for lag in range(1, len(amdf) - 1):
            if amdf[lag - 1] < amdf[lag] and amdf[lag + 1] < amdf[lag]:  # Maksimum
                max_lag = lag
                break
        max_lag = min(frame_size // 2, len(frame) // 2, max_lag)
        # Ograniczenie zakresu szukania minimum po pierwszym maksimum
        search_range = range(max_lag, len(amdf))  # Poszukiwanie minimum po pierwszym maksimum
        min_lag = min(search_range, key=lambda lag: amdf[lag])  # Znalezienie minimum w wybranym zakresie

        f0_val = sample_rate / min_lag if min_lag != 0 else 0

        f0.append(f0_val)
        f0_time.append(frame_start / sample_rate)
    # Rysowanie wykresu
    fig.clear()
    ax = fig.add_subplot(111)

    # Tworzenie wykresu audio
    # ax.plot(time, visible_audio, label='Przebieg czasowy (audio)', color='blue', alpha=0.6, linewidth=0.5)

    # Tworzenie wykresu RMS
    ax.plot(f0_time, f0, label='(Fundamental Frequency', color='red', linewidth=2)

    ax.set_title("Częstotliwość tonu podstawowego F0 - AMDF")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("F0")
    ax.grid(True)
    # ax.set_ylim(min(min(f0)*0.9, 50), max(max(f0)*1.1,120 ))
    # ax.set_ylim(min(f0)*0.9, max(f0)*1.1)
    ax.set_ylim(min(min(f0) * 0.95, 40), max(max(f0) * 1.05, 105))

    ax.legend()
    fig.tight_layout()
    canvas.draw()


def format_value(value):
    return "{:.2f}".format(value)  # Formatuj wartość z 2 miejscami po przecinku


def calculate_VSTD(frame_size, label):
    global func_nr
    func_nr = 8
    max_val = max(abs(x) for x in audio_data)
    audio_data_sk = [x / max_val for x in audio_data]

    # Obliczanie liczby ramek w nagraniu
    num_frames = len(audio_data_sk) // frame_size
    vol = []
    sum_vol = 0
    peaks_all = []
    valleys_all = []
    vstd = []  # Lista do przechowywania VSTD dla każdego okna 1-sekundowego
    vdr = []  # Lista do przechowywania VDR dla każdego okna 1-sekundowego
    vu_all = []  # Lista do przechowywania VU dla każdego okna 1-sekundowego

    # Obliczanie głośności (vol) dla całego nagrania
    for i in range(num_frames):
        frame_start = i * frame_size
        frame_end = min(frame_start + frame_size, len(audio_data_sk))
        frame = audio_data_sk[frame_start:frame_end]
        frame = [float(x) for x in frame]
        vol_value = (sum(((x ** 2) / len(frame)) for x in frame)) ** 0.5
        sum_vol += vol_value
        vol.append(vol_value)

    # Obliczanie VSTD_full i VDR_full dla całego nagrania
    max_vol = max(vol)
    min_vol = min(vol)
    mean_vol = sum_vol / num_frames
    std_vol = math.sqrt(sum((vol_value - mean_vol) ** 2 for vol_value in vol) / len(vol))
    VSTD_full = std_vol / max_vol if max_vol > 0 else 0
    VDR_full = (max_vol - min_vol) / max_vol if max_vol > 0 else 0

    # Analiza w oknach 1-sekundowych
    frames_per_window = sample_rate // frame_size

    for start in range(0, len(vol), frames_per_window):
        window_vol = vol[start:start + frames_per_window]
        peaks = []
        valleys = []
        if len(window_vol) == 0:
            continue
        for j in range(1, len(window_vol) - 1):
            if window_vol[j] > window_vol[j - 1] and window_vol[j] > window_vol[j + 1]:
                peaks.append(window_vol[j])
            elif window_vol[j] < window_vol[j - 1] and window_vol[j] < window_vol[j + 1]:
                valleys.append(window_vol[j])
        peaks_all.append(peaks)
        valleys_all.append(valleys)

        # Obliczanie VSTD dla każdego okna 1-sekundowego
        window_mean_vol = sum(window_vol) / len(window_vol)
        window_std_vol = math.sqrt(sum((x - window_mean_vol) ** 2 for x in window_vol) / len(window_vol))
        VSTD_window = window_std_vol / max(window_vol) if max(window_vol) > 0 else 0
        vstd.append(VSTD_window)

        # Obliczanie VDR dla każdego okna 1-sekundowego
        window_max_vol = max(window_vol)
        window_min_vol = min(window_vol)
        VDR_window = (window_max_vol - window_min_vol) / window_max_vol if window_max_vol > 0 else 0
        vdr.append(VDR_window)

        # Obliczanie VU dla każdego okna 1-sekundowego
        vu = 0
        for p, v in zip(peaks, valleys):
            vu += abs(p - v)
        vu_all.append(vu)

    # Obliczanie VU dla całego nagrania
    vu_total = 0
    for peaks, valleys in zip(peaks_all, valleys_all):
        for p, v in zip(peaks, valleys):
            vu_total += abs(p - v)
    VU_full = vu_total

    VSTD_full_str = format_value(VSTD_full)
    VDR_full_str = format_value(VDR_full)
    vstd_str = [format_value(val) for val in vstd]  # Sformatuj każdą wartość w liście vstd
    vdr_str = [format_value(val) for val in vdr]  # Sformatuj każdą wartość w liście vdr
    VU_full_str = format_value(VU_full)
    vu_str = [format_value(val) for val in vu_all]  # Sformatuj każdą wartość w liście vu_all

    # Wyświetlenie wyników w label
    label.config(text="VSTD_full = " + VSTD_full_str +
                      "\nVDR_full = " + VDR_full_str +
                      "\nvstd (dla każdego okna 1s) = " + ", ".join(vstd_str) +  # Wyświetlanie listy vstd
                      "\nvdr (dla każdego okna 1s) = " + ", ".join(vdr_str) +  # Wyświetlanie listy vdr
                      "\nVU_full = " + VU_full_str +
                      "\nvu (dla każdego okna 1s) = " + ", ".join(vu_str))  # Wyświetlanie listy vu_all

    label.grid()


def compute_entropy(frame_size, segment_size, audio_data):
    num_frames = len(audio_data) // frame_size
    entropies = []

    for frame_idx in range(num_frames):
        frame = audio_data[frame_idx * frame_size:(frame_idx + 1) * frame_size]
        num_segments = len(frame) // segment_size
        segment_energies = []

        for seg_idx in range(num_segments):
            segment = frame[seg_idx * segment_size:(seg_idx + 1) * segment_size]
            energy = sum(x ** 2 for x in segment)
            segment_energies.append(energy)

        total_energy = sum(segment_energies)
        normalized_energies = [energy / total_energy for energy in segment_energies] if total_energy != 0 else [
                                                                                                                   0] * len(
            segment_energies)

        entropy = -sum(e * math.log2(e) for e in normalized_energies if e > 0)
        entropies.append(entropy)

    return sum(entropies) / len(entropies) if entropies else 0


def calculate_LSTER(frame_size, label, segment_size):
    global func_nr
    func_nr = 9
    max_val = max(abs(x) for x in audio_data)
    audio_data_sk = [x / max_val for x in audio_data]
    num_frames = len(audio_data) // frame_size
    frames_per_window = sample_rate // frame_size

    entropy = []
    ste = []
    lster_per_window = []
    energy_entropy_per_window = []

    for i in range(num_frames):
        frame_start = i * frame_size
        frame_end = min(frame_start + frame_size, len(audio_data))
        frame = audio_data_sk[frame_start:frame_end]
        entropy_val = calculate_EE(frame, segment_size, audio_data_sk)
        entropy.append(entropy_val)

        ste_value = sum((x ** 2) / len(frame) for x in frame)
        ste.append(ste_value)

    energy_entropy_full = compute_entropy(frame_size, segment_size, audio_data_sk)

    for start in range(0, len(ste), frames_per_window):
        window_ste = ste[start:start + frames_per_window]
        if len(window_ste) == 0:
            continue

        av_ste = sum(window_ste) / len(window_ste)
        # low_energy_frames = sum(1 for ste_val in window_ste if ste_val < 0.5 * av_ste)
        print("ste count: ", len(window_ste))
        print("frames/window: ", frames_per_window)
        low_energy_frames = (sum(signum(0.5*av_ste - window_ste[x]) + 1 for x in range(len(window_ste)))) / (2 * len(window_ste))

        # lster = low_energy_frames / len(window_ste)
        # lster_per_window.append(lster)
        lster_per_window.append(low_energy_frames)

        energy_entropy = calculate_energy_entropy(window_ste)
        energy_entropy_per_window.append(energy_entropy)

    LSTER_full = sum(lster_per_window) / len(lster_per_window) if lster_per_window else 0

    LSTER_full_str = format_value(LSTER_full)
    energy_entropy_full_str = format_value(energy_entropy_full)
    lster_per_window_str = [format_value(val) for val in lster_per_window]
    energy_entropy_per_window_str = [format_value(val) for val in energy_entropy_per_window]

    label.config(text="LSTER = " + LSTER_full_str +
                      "\nEnergy Entropy full = " + energy_entropy_full_str +
                      "\nLSTER (dla każdego okna 1s) = " + ", ".join(lster_per_window_str) +
                      "\nEnergy Entropy (dla każdego okna 1s) = " + ", ".join(energy_entropy_per_window_str))

    label.grid()


def calculate_EE(frame, segment_size, audio_data_sk):
    num_segments = len(frame) // segment_size
    ste = []

    for i in range(num_segments):
        segment_start = i * segment_size
        segment_end = min(segment_start + segment_size, len(audio_data_sk))
        segment = audio_data_sk[segment_start:segment_end]
        ste_value = sum((x ** 2) / len(segment) for x in segment)
        ste.append(ste_value)

    if len(frame) % segment_size != 0:
        segment = frame[num_segments * segment_size:]
        ste.append(sum(x ** 2 for x in segment))

    total_energy = sum(ste)
    ste = [e / total_energy for e in ste] if total_energy > 0 else [0] * len(ste)

    entropy = -sum(e * math.log2(e) for e in ste if e > 0)
    return entropy


def calculate_energy_entropy(ste_values):
    total_energy = sum(ste_values)
    if total_energy > 0:
        normalized_ste = [e / total_energy for e in ste_values]
        energy_entropy = -sum(e * math.log2(e) for e in normalized_ste if e > 0)
        return energy_entropy
    return 0


# def calculate_klip_ZCR(frame_size, label):
#     global func_nr
#     func_nr = 10
#
#
#     # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
#     num_frames = len(audio_data) // frame_size
#     zcr = []
#     zcr_time = []
#
#     for i in range(num_frames):
#         frame_start = i * frame_size
#         frame_end = min(frame_start + frame_size, len(audio_data))
#         frame = audio_data[frame_start:frame_end]
#
#         zcr_val = (sum(abs(signum(frame[x]) - signum(frame[x + 1])) for x in range(len(frame) - 1))) / (2 * len(frame))
#         zcr.append(zcr_val)
#     zcr_std = np.std(zcr)
#
#     zcr_std_full_str = format_value(zcr_std)
#     # lster_per_window_str = [format_value(val) for val in lster_per_window]
#
#     label.config(text="ZSTD = " + zcr_std_full_str)
#                       # "\nEnergy Entropy full = " + energy_entropy_full_str +
#                       # "\nLSTER (dla każdego okna 1s) = " + ", ".join(lster_per_window_str) +
#                       # "\nEnergy Entropy (dla każdego okna 1s) = " + ", ".join(energy_entropy_per_window_str))
#
#     label.grid()

# def calculate_klip_ZCR(frame_size, label):
#     global func_nr
#     func_nr = 10
#
#     # Obliczenie liczby ramek w oknie 1s
#     frames_per_window = sample_rate // frame_size
#
#     num_frames = len(audio_data) // frame_size
#     zcr_values = []
#
#     # Obliczanie ZCR dla każdej ramki
#     for i in range(num_frames):
#         frame_start = i * frame_size
#         frame_end = min(frame_start + frame_size, len(audio_data))
#         frame = audio_data[frame_start:frame_end]
#
#         zcr_val = (sum(abs(signum(frame[x]) - signum(frame[x + 1])) for x in range(len(frame) - 1))) / (2 * len(frame))
#         zcr_values.append(zcr_val)
#
#     # Obliczamy ZSTD dla każdego okna 1s
#     zcr_std_per_window = []
#
#     for start in range(0, len(zcr_values), frames_per_window):
#         window_zcr_values = zcr_values[start:start + frames_per_window]
#         if len(window_zcr_values) > 0:
#             zcr_std = np.std(window_zcr_values)
#             zcr_std_per_window.append(zcr_std)
#
#     # Obliczenie średniego ZSTD dla wszystkich okien
#     zcr_std_full = np.mean(zcr_std_per_window) if zcr_std_per_window else 0
#
#     zcr_std_full_str = format_value(zcr_std_full)
#     zcr_std_per_window_str = [format_value(val) for val in zcr_std_per_window]
#
#     label.config(text="ZSTD = " + zcr_std_full_str +
#                       "\nZSTD (dla każdego okna 1s) = " + ", ".join(zcr_std_per_window_str))
#
#     label.grid()


def mean(values):
    # Obliczanie średniej
    return sum(values) / len(values) if values else 0


def std(values, avg):
    # Obliczanie odchylenia standardowego
    return (sum((x - avg) ** 2 for x in values) / len(values)) ** 0.5 if values else 0


def calculate_klip_ZCR(frame_size, label):
    global func_nr
    func_nr = 10

    # Obliczenie liczby ramek w oknie 1s
    frames_per_window = sample_rate // frame_size

    num_frames = len(audio_data) // frame_size
    zcr_values = []

    # Obliczanie ZCR dla każdej ramki
    for i in range(num_frames):
        frame_start = i * frame_size
        frame_end = min(frame_start + frame_size, len(audio_data))
        frame = audio_data[frame_start:frame_end]

        zcr_val = (sum(abs(signum(frame[x]) - signum(frame[x + 1])) for x in range(len(frame) - 1))) / (2 * len(frame))
        zcr_values.append(zcr_val)

    # Obliczamy ZSTD dla każdego okna 1s
    zcr_std_per_window = []
    hzcrr_per_window = []

    for start in range(0, len(zcr_values), frames_per_window):
        window_zcr_values = zcr_values[start:start + frames_per_window]
        if len(window_zcr_values) > 0:
            # Obliczenie ZSTD dla okna
            avg_zcr = mean(window_zcr_values)
            zcr_std = std(window_zcr_values, avg_zcr)
            zcr_std_per_window.append(zcr_std)

            # Obliczanie HZCRR dla okna
            hzcrr = 0
            for zcr in window_zcr_values:
                hzcrr += (signum(zcr - 1.5 * avg_zcr) + 1) / 2
            hzcrr_per_window.append(hzcrr / len(window_zcr_values))

    # Obliczenie średniego ZSTD i HZCRR dla całego nagrania
    zcr_std_full = mean(zcr_std_per_window) if zcr_std_per_window else 0
    hzcrr_full = mean(hzcrr_per_window) if hzcrr_per_window else 0

    # Formatujemy wyniki
    zcr_std_full_str = format_value(zcr_std_full)
    hzcrr_full_str = format_value(hzcrr_full)

    # Formatujemy wyniki dla każdego okna
    zcr_std_per_window_str = [format_value(val) for val in zcr_std_per_window]
    hzcrr_per_window_str = [format_value(val) for val in hzcrr_per_window]

    # Wyświetlanie wyników
    label.config(text="ZSTD = " + zcr_std_full_str +
                      "\nZSTD (dla każdego okna 1s) = " + ", ".join(zcr_std_per_window_str) +
                      "\nHZCRR = " + hzcrr_full_str +
                      "\nHZCRR (dla każdego okna 1s) = " + ", ".join(hzcrr_per_window_str))

    label.grid()


import math
import matplotlib.pyplot as plt


# Funkcja do obliczania wartości LSTER dla okna (bez użycia numpy)
def calculate_lster(window, frame_size):
    """
    Oblicza wartość Loudness Spectral Temporal Energy Ratio (LSTER) dla okna, które składa się z ramek.
    """

    num_frames = len(window) // frame_size
    ste = []
    # Obliczanie ZCR dla każdej ramki
    for i in range(num_frames):
        frame_start = i * frame_size
        frame_end = min(frame_start + frame_size, len(window))
        frame = window[frame_start:frame_end]
        spectrum = [abs(x) ** 2 for x in frame]
        ste.extend(spectrum)
    # Obliczamy widmo (kwadrat amplitudy) dla okna
    if len(ste) == 0:
        return 0
    elif len(ste) == 1:
        av_ste = ste[0]
    else:
        av_ste = sum(ste) / len(ste)
    # low_energy_frames = sum(1 for ste_val in window_ste if ste_val < 0.5 * av_ste)
    # print("ste count: ", len(window_ste))
    # print("frames/window: ", frames_per_window)
    LSTER = (sum(signum(0.5 * av_ste - ste[x]) + 1 for x in range(len(ste)))) / (
                2 * len(ste))

    return LSTER


# Funkcja do obliczania wartości ZSTD (Zero Crossing Rate) dla okna (bez użycia numpy)
def calculate_zstd(window, frame_size):
    """
    Oblicza wartość Zero Crossing Rate (ZSTD) dla okna, które składa się z ramek.
    """
    num_frames = len(window) // frame_size
    zcr = []

    # Obliczanie ZCR dla każdej ramki
    for i in range(num_frames):
        frame_start = i * frame_size
        frame_end = min(frame_start + frame_size, len(window))
        frame = window[frame_start:frame_end]

        zcr_val = (sum(abs(signum(frame[x]) - signum(frame[x + 1])) for x in range(len(frame) - 1))) / (2 * len(frame))
        zcr.append(zcr_val)
    if len(zcr) == 0:
        return 0
    av_zcr = sum(zcr) / len(zcr)

    zcr_std = std(zcr, av_zcr)
    return zcr_std



def differentiate(frame_size, fig, canvas, start_idx=0, max_points=176400):
    global func_nr
    func_nr = 14
    lster_time = []
    max_val = max(abs(x) for x in audio_data)
    audio_data_sk = [x / max_val for x in audio_data]
    window_size = sample_rate
    # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data_sk[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]

    # Okno składające się z kilku ramek
    num_frames_in_window = window_size // frame_size  # Liczba ramek w jednym oknie
    visible_num_windows = len(visible_audio) // window_size  # Liczba okien w widocznej części sygnału

    lster_values = []
    zstd_values = []

    # Obliczanie wartości LSTER i ZSTD dla każdego okna
    for i in range(visible_num_windows):
        window_start = start_idx + i * window_size
        window_end = min(window_start + window_size, end_idx)
        lster_time.append(window_start / sample_rate)

        # Przekształcenie okna do jednego dużego wektora składającego się z ramek
        window = audio_data[window_start:window_end]
        window = [float(x) for x in window]

        # Obliczanie LSTER dla okna
        lster_val = calculate_lster(window, frame_size)
        print("lster_val: ", lster_val)
        lster_values.append(lster_val)
        # lster_time.extend(lster_time_win)

        # Obliczanie ZSTD dla okna
        zstd_val = calculate_zstd(window, frame_size)
        zstd_values.append(zstd_val)
        print("zstd_val: ", zstd_val)

    if len(visible_audio) % window_size != 0:

        window_start = start_idx + visible_num_windows * window_size
        window_end = min(window_start + window_size, end_idx)
        lster_time.append(window_start / sample_rate)

        # Przekształcenie okna do jednego dużego wektora składającego się z ramek
        window = audio_data[window_start:window_end]
        window = [float(x) for x in window]

        # Obliczanie LSTER dla okna
        lster_val = calculate_lster(window, frame_size)
        print("lster_val: ", lster_val)
        lster_values.append(lster_val)
        # lster_time.extend(lster_time_win)

        # Obliczanie ZSTD dla okna
        zstd_val = calculate_zstd(window, frame_size)
        zstd_values.append(zstd_val)
        print("zstd_val: ", zstd_val)

    # Przeskalowanie danych audio do zakresu [0, 1]
    scaled_audio = min_max_scaling(visible_audio, 0, 1)
    print(lster_values)
    # # Przeskalowanie wartości LSTER i ZSTD do zakresu [0, 1]
    # scaled_lster = min_max_scaling(lster_values, 0, 1)
    # scaled_zstd = min_max_scaling(zstd_values, 0, 1)
    #
    # # Ustawienie wartości suwaka dla poziomu ciszy
    # slider2.config(to=max(lster_values), label="Poziom LSTER/ZSTD")
    # slider2.grid()

    # Rysowanie wykresu
    fig.clear()
    ax = fig.add_subplot(111)
    print(f"Rozmiar lster_time: {len(lster_time)}, Rozmiar scaled_lster: {len(lster_values)}, Rozmiar lster: {len(lster_values)}")

    # Narysowanie przeskalowanego audio
    ax.plot(time, scaled_audio, label='Przeskalowane nagranie audio', color='blue', alpha=0.4, linewidth=0.5)

    # Narysowanie przeskalowanego LSTER
    ax.plot(lster_time, lster_values, label='Przeskalowane LSTER', color='green', linewidth=2)

    # Narysowanie przeskalowanego ZSTD
    ax.plot(lster_time, zstd_values, label='Przeskalowane ZSTD', color='red', linewidth=2)

    # Dodanie linii na poziomie cut_off (jeśli dotyczy)
    # ax.axhline(y=cut_off, color='blue', linestyle='--', label=f'Cut Off ({cut_off} Hz)')

    # Ustawienia wykresu
    ax.set_title("LSTER i ZSTD dla każdego okna")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Wartości skalowane")
    ax.grid(True)
    ax.set_ylim(0, 1.1)  # Zakres dla wartości skalowanych
    ax.legend()
    fig.tight_layout()
    canvas.draw()


#
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# # Funkcja do obliczania wartości LSTER
# def calculate_lster(frame):
#     """
#     Oblicza wartość Loudness Spectral Temporal Energy Ratio (LSTER) dla pojedynczego okna.
#     """
#     # Przykład prostej metody obliczania LSTER:
#     # Możesz dostosować to do swojego przypadku w zależności od definicji LSTER w literaturze.
#     # W tym przypadku wykorzystamy energię w widmie jako przybliżenie.
#
#     # Obliczenie widma (moc w każdym paśmie częstotliwości)
#     spectrum = np.abs(np.fft.fft(frame)) ** 2
#     energy = np.sum(spectrum)  # Całkowita energia w widmie
#     return energy
#
#
# # Funkcja do obliczania wartości ZSTD (Zero Crossing Rate)
# def calculate_zstd(frame):
#     """
#     Oblicza wartość Zero Crossing Rate (ZSTD) dla pojedynczego okna.
#     """
#     zero_crossings = np.count_nonzero(np.diff(np.sign(frame)))
#     return zero_crossings
#
#
#
# def differentiate(frame_size, fig, canvas, window_size, start_idx=0, max_points=100000):
#     global func_nr
#     func_nr = 14
#
#     max_val = max(abs(x) for x in audio_data)
#     audio_data_sk = [x / max_val for x in audio_data]
#
#     # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
#     end_idx = min(start_idx + max_points, len(audio_data))
#     visible_audio = audio_data_sk[start_idx:end_idx]
#     time = [i / sample_rate for i in range(start_idx, end_idx)]
#
#     visible_num_frames = len(visible_audio) // frame_size
#     lster_values = []
#     zstd_values = []
#
#     # Obliczanie wartości LSTER i ZSTD dla każdego okna
#     for i in range(visible_num_frames):
#         frame_start = start_idx + i * frame_size
#         frame_end = min(frame_start + frame_size, end_idx)
#         frame = audio_data[frame_start:frame_end]
#         frame = [float(x) for x in frame]
#
#         # Obliczanie LSTER
#         lster_val = calculate_lster(frame)
#         lster_values.append(lster_val)
#
#         # Obliczanie ZSTD
#         zstd_val = calculate_zstd(frame)
#         zstd_values.append(zstd_val)
#
#     # Przeskalowanie danych audio do zakresu [0, 1]
#     scaled_audio = min_max_scaling(np.array(visible_audio), 0, 1)
#
#     # Przeskalowanie wartości LSTER i ZSTD do zakresu [0, 1]
#     scaled_lster = min_max_scaling(np.array(lster_values), 0, 1)
#     scaled_zstd = min_max_scaling(np.array(zstd_values), 0, 1)
#
#     # Ustawienie wartości suwaka dla poziomu ciszy
#     slider2.config(to=max(lster_values), label="Poziom LSTER/ZSTD")
#     slider2.grid()
#
#     # Rysowanie wykresu
#     fig.clear()
#     ax = fig.add_subplot(111)
#
#     # Narysowanie przeskalowanego audio
#     ax.plot(time, scaled_audio, label='Przeskalowane nagranie audio', color='blue', alpha=0.4, linewidth=0.5)
#
#     # Narysowanie przeskalowanego LSTER
#     ax.plot(time[:len(scaled_lster)], scaled_lster, label='Przeskalowane LSTER', color='green', linewidth=2)
#
#     # Narysowanie przeskalowanego ZSTD
#     ax.plot(time[:len(scaled_zstd)], scaled_zstd, label='Przeskalowane ZSTD', color='red', linewidth=2)
#
#     # Dodanie linii na poziomie cut_off (jeśli dotyczy)
#     ax.axhline(y=cut_off, color='blue', linestyle='--', label=f'Cut Off ({cut_off} Hz)')
#
#     # Ustawienia wykresu
#     ax.set_title("LSTER i ZSTD dla każdego okna")
#     ax.set_xlabel("Czas [s]")
#     ax.set_ylabel("Wartości skalowane")
#     ax.grid(True)
#     ax.set_ylim(0, 1.1)  # Zakres dla wartości skalowanych
#     ax.legend()
#     fig.tight_layout()
#     canvas.draw()


# # Funkcja do obliczania wartości LSTER
# def calculate_lster(frame):
#     """
#     Oblicza wartość Loudness Spectral Temporal Energy Ratio (LSTER) dla pojedynczego okna.
#     """
#     # Przykład prostej metody obliczania LSTER:
#     # Możesz dostosować to do swojego przypadku w zależności od definicji LSTER w literaturze.
#     # W tym przypadku wykorzystamy energię w widmie jako przybliżenie.
#
#     # Obliczenie widma (moc w każdym paśmie częstotliwości)
#     spectrum = np.abs(np.fft.fft(frame)) ** 2
#     energy = np.sum(spectrum)  # Całkowita energia w widmie
#     return energy
#
# # Funkcja do obliczania wartości ZSTD (Zero Crossing Rate)
# def calculate_zstd(frame):
#     """
#     Oblicza wartość Zero Crossing Rate (ZSTD) dla pojedynczego okna.
#     """
#     zero_crossings = np.count_nonzero(np.diff(np.sign(frame)))
#     return zero_crossings
#
# # Funkcja rysująca wykres z wartościami LSTER i ZSTD
# def differentiate(frame_size, window_size, start_idx = 0, max_points = 80000):
#     global func_nr
#     func_nr = 14
#
#     max_val = max(abs(x) for x in audio_data)
#     audio_data_sk = [x / max_val for x in audio_data]
#     # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
#     end_idx = min(start_idx + max_points, len(audio_data))
#     visible_audio = audio_data_sk[start_idx:end_idx]
#     time = [i / sample_rate for i in range(start_idx, end_idx)]
#
#     visible_num_frames = len(visible_audio) // frame_size
#
#     # Obliczanie wartości F0 i sprawdzanie ciszy
#     for i in range(visible_num_frames):
#         frame_start = start_idx + i * frame_size
#         frame_end = min(frame_start + frame_size, end_idx)
#         frame = audio_data[frame_start:frame_end]
#         frame = [float(x) for x in frame]
#
#     num_frames = window_size // frame_size  # Liczba ramek (okien)
#
#     lster_values = []
#     zstd_values = []
#     time = []  # Oś czasu
#
#     for i in range(num_frames):
#         frame_start = i * window_size
#         frame_end = min((i + 1) * window_size, len(audio_data))
#
#         frame = audio_data[frame_start:frame_end]
#
#         # Oblicz LSTER i ZSTD dla danego okna
#         lster_values.append(calculate_lster(frame))
#         zstd_values.append(calculate_zstd(frame))
#
#         # Czas dla danego okna (połowa okna, aby wskazać czas reprezentujący to okno)
#         time.append((frame_start + frame_end) / (2 * sample_rate))
#
#     # Rysowanie wykresu
#     plt.figure(figsize=(10, 6))
#
#     # Wykres LSTER
#     plt.plot(time, lster_values, label='LSTER', color='blue', linewidth=2)
#
#     # Wykres ZSTD
#     plt.plot(time, zstd_values, label='ZSTD', color='red', linewidth=2)
#
#     plt.title("LSTER i ZSTD dla każdego okna audio")
#     plt.xlabel("Czas [s]")
#     plt.ylabel("Wartości")
#     plt.legend(loc='upper right')
#     plt.grid(True)
#
#     # Wyświetlanie wykresu
#     plt.tight_layout()
#     plt.show()


def slider_function(slider, canvas, fig, slider2, slider3, label):
    # global func_nr
    print(slider2.get())
    if func_nr == 2:
        calculate_volume_and_plot(slider.get(), canvas, fig)
    elif func_nr == 3:
        calculate_STE_and_plot(slider.get(), canvas, fig)
    elif func_nr == 4:
        calculate_ZCR_and_plot(slider.get(), canvas, fig)
    elif func_nr == 5:
        SilentRatio(slider.get(), canvas, fig, slider2.get(), slider3.get())
    elif func_nr == 6:
        calculate_f0_autocorrelation(slider.get(), canvas, fig)
    elif func_nr == 7:
        calculate_f0_AMDF(slider.get(), canvas, fig)
    elif func_nr == 8:
        calculate_VSTD(slider.get(), label)
    elif func_nr == 9:
        slider2.configure(to=slider.get() // 2, from_=1, label="segment size")
        calculate_LSTER(slider.get(), label, slider2.get())
    elif func_nr == 10:
        calculate_klip_ZCR(slider.get(), label)
    elif func_nr == 12:
        silence_detection(slider.get(), canvas, fig, slider2.get(), slider3.get())
    elif func_nr == 13:
        sound_detection(slider.get(), canvas, fig, slider2)
    elif func_nr == 14:
        differentiate(slider.get(), canvas, fig)


def scroll_function1(fig, canvas, position, slider, scrollbar, scrollbar2):
    """
    Obsługuje przesunięcie widocznego fragmentu danych na wykresie.
    """
    if audio_data is not None:
        max_points = 20000  # Maksymalna liczba punktów widocznych na raz
        if len(audio_data) <= max_points:
            # Gdy długość audio jest mniejsza niż max_points, start_idx zawsze wynosi 0
            start_idx = 0
        else:
            # Oblicz przesunięcie dla większych danych
            # start_idx = position * 200
            start_idx = position * slider.get()
            max_scroll = (len(audio_data) -20000) // slider.get()  # Zakres przewijania w krokach
            scrollbar.configure(to=max_scroll)
            scrollbar2.configure(to=max_scroll)

        # start_idx = position * 200  # Przesunięcie na podstawie pozycji suwaka
        plot_audio_waveform(sample_rate, audio_data, fig, canvas, start_idx=start_idx)


def scroll_function(fig, canvas, position, slider, slider2, slider3, scrollbar, scrollbar2):
    """
    Obsługuje przesunięcie widocznego fragmentu danych na wykresie.
    """
    if audio_data is not None:
        max_points = 20000  # Maksymalna liczba punktów widocznych na raz
        if len(audio_data) <= max_points:
            # Gdy długość audio jest mniejsza niż max_points, start_idx zawsze wynosi 0
            start_idx = 0
        else:
            # Oblicz przesunięcie dla większych danych
            # start_idx = position * 200
            start_idx = position * slider.get()
            max_scroll = (len(audio_data) - 20000) // slider.get()  # Zakres przewijania w krokach
            scrollbar.configure(to=max_scroll)
            scrollbar2.configure(to=max_scroll)
        # start_idx = position * 200  # Przesunięcie na podstawie pozycji suwaka
        if func_nr == 1:
            plot_audio_waveform(sample_rate, audio_data, fig, canvas, start_idx=start_idx)
        else:
            start_idx = position * slider.get()
            if func_nr == 2:
                calculate_volume_and_plot(slider.get(), fig, canvas, start_idx=start_idx)
            elif func_nr == 3:
                calculate_STE_and_plot(slider.get(), fig, canvas, start_idx=start_idx)
            elif func_nr == 4:
                calculate_ZCR_and_plot(slider.get(), fig, canvas, start_idx=start_idx)
            elif func_nr == 5:
                SilentRatio(slider.get(), fig, canvas, slider2.get(), slider3.get(), start_idx=start_idx)
            elif func_nr == 6:
                calculate_f0_autocorrelation(slider.get(), fig, canvas, start_idx=start_idx)
            elif func_nr == 7:
                calculate_f0_AMDF(slider.get(), fig, canvas, start_idx=start_idx)
            elif func_nr > 11:
                max_scroll = (len(audio_data) - 80000) // slider.get()  # Zakres przewijania w krokach
                scrollbar2.configure(to=max_scroll)
                if func_nr == 12:
                    silence_detection(slider.get(), fig, canvas, slider2.get(), slider3.get(), start_idx=start_idx)
                elif func_nr == 13:
                    sound_detection(slider.get(), fig, canvas, slider2, start_idx=start_idx)
                elif func_nr == 14:
                    max_scroll = 10*(len(audio_data) - 176400) // slider.get()  # Zakres przewijania w krokach
                    print(max_scroll)
                    scrollbar2.configure(to=max_scroll)
                    differentiate(slider.get(), fig, canvas, start_idx=start_idx)
