from tkinter import filedialog

import numpy as np
import sounddevice as sd
from scipy.io import wavfile


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
        slider.configure(to=500, from_=1)
        slider.grid()
        scrollbar2.grid()
        if len(audio_data) > 10000:
            max_scroll = (len(audio_data) - 10000) // slider.get()  # Zakres przewijania w krokach
            # scrollbar.configure(to=max_scroll)
            # scrollbar2.configure(to=max_scroll)
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
            slider2.config(to=max(audio_data), label= "volume level")
            slider2.grid()
            slider3.config(ext="ZCR level")

            slider3.grid()
            SilentRatio(slider.get(), fig, canvas, slider2.get(), slider3.get())
        elif function_nr == 6:
            calculate_f0_autocorrelation(slider.get(), fig, canvas)
        elif function_nr == 7:
            calculate_f0_AMDF(slider.get(), fig, canvas)
    elif function_nr >= 8:
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
            slider2.configure(to=slider.get() // 2, from_=1, label= "segment size")
            calculate_LSTER(slider.get(), label, slider2.get())
    elif function_nr == 10:
        play_audio()


def plot_audio_waveform(sample_rate, audio_data, fig, canvas, start_idx=0, max_points=10000):
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
            if len(audio_data) > 10000:
                max_scroll = (len(audio_data) - 10000) // 200  # Zakres przewijania w krokach
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
        print("Odtwarzanie zakończone.")

    except Exception as e:
        print(f"Wystąpił błąd podczas odtwarzania dźwięku: {e}")


def calculate_volume_and_plot(frame_size, fig, canvas, start_idx=0, max_points=10000):
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

        # Oblicz RMS dla każdej ramki
        # rms_value = (sum(x ** 2 for x in frame) / len(frame)) ** 0.5
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


def calculate_STE_and_plot(frame_size, fig, canvas, start_idx=0, max_points=10000):
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

        # Oblicz RMS dla każdej ramki
        # rms_value = (sum(x ** 2 for x in frame) / len(frame)) ** 0.5
        rms_value = (sum(((x ** 2) / len(frame)) for x in frame))
        rms.append(rms_value)
        rms_time.append(frame_start / sample_rate)

    # Rysowanie wykresu
    fig.clear()
    ax = fig.add_subplot(111)

    # Tworzenie wykresu audio
    # ax.plot(time, visible_audio, label='Przebieg czasowy (audio)', color='blue', alpha=0.6, linewidth=0.5)

    # Tworzenie wykresu RMS
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


def calculate_ZCR_and_plot(frame_size, fig, canvas, start_idx=0, max_points=10000):
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

        # Oblicz RMS dla każdej ramki
        # rms_value = (sum(x ** 2 for x in frame) / len(frame)) ** 0.5
        # zcr = (sum(abs(signum(frame[x]) - signum(frame[x+1])) for x in range(len(frame)-1) ) )/ (2*len(frame)
        zcr_val = (sum(abs(signum(frame[x]) - signum(frame[x + 1])) for x in range(len(frame) - 1))) / (2 * len(frame))
        zcr.append(zcr_val)
        zcr_time.append(frame_start / sample_rate)

    # Rysowanie wykresu
    fig.clear()
    ax = fig.add_subplot(111)

    # Tworzenie wykresu audio
    # ax.plot(time, visible_audio, label='Przebieg czasowy (audio)', color='blue', alpha=0.6, linewidth=0.5)

    # Tworzenie wykresu RMS
    ax.plot(zcr_time, zcr, label='Zero Crossing Rate (ZCR)', color='red', linewidth=2)

    ax.set_title("Zero Crossing Rate (ZCR)")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("ZCR")
    ax.set_ylim(0, max(max(zcr) * 1.1, 0.8))
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def SilentRatio(frame_size, fig, canvas, vol_level, zcr_level, start_idx=0, max_points=10000):
    global func_nr
    func_nr = 5

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

        # Oblicz RMS dla każdej ramki
        # rms_value = (sum(x ** 2 for x in frame) / len(frame)) ** 0.5
        # zcr = (sum(abs(signum(frame[x]) - signum(frame[x+1])) for x in range(len(frame)-1) ) )/ (2*len(frame)
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

    # Tworzenie wykresu audio
    # ax.plot(time, visible_audio, label='Przebieg czasowy (audio)', color='blue', alpha=0.6, linewidth=0.5)

    # Tworzenie wykresu RMS
    ax.plot(silent_time, silent, label='Silent Ratio (SR)', color='red', linewidth=2)

    ax.set_title("Silent Ratio (SR)")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("SR")
    ax.grid(True)
    ax.set_ylim(0, 1.1)

    ax.legend()
    fig.tight_layout()
    canvas.draw()


def calculate_f0_autocorrelation(frame_size, fig, canvas, start_idx=0, max_points=10000):
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

    # Tworzenie wykresu audio
    # ax.plot(time, visible_audio, label='Przebieg czasowy (audio)', color='blue', alpha=0.6, linewidth=0.5)

    # Tworzenie wykresu RMS
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


def calculate_f0_AMDF(frame_size, fig, canvas, start_idx=0, max_points=10000):
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


# def calculate_VSTD(frame_size, label):
#     global func_nr
#     func_nr = 8
#     max_val = max(abs(x) for x in audio_data)
#     audio_data_sk = [x / max_val for x in audio_data]
#     # max_val = max(audio_data)  # Maksymalna wartość w oryginalnych danych
#     # min_val = min(audio_data)  # Minimalna wartość w oryginalnych danych
#     #
#     # # Normalizacja danych: (x - min) / (max - min)
#     # audio_data_sk = [(x - min_val) / (max_val - min_val) for x in audio_data]
#     print(audio_data_sk)
#     num_frames = len(audio_data_sk) // frame_size
#     vol = []
#     sum_vol = 0
#     for i in range(num_frames):
#         frame_start = i * frame_size
#         frame_end = min(frame_start + frame_size, len(audio_data_sk))
#         frame = audio_data_sk[frame_start:frame_end]
#         frame = [float(x) for x in frame]
#         vol_value = (sum(((x ** 2) / len(frame)) for x in frame)) ** 0.5
#         sum_vol += vol_value
#         vol.append(vol_value)
#     max_vol = max(vol)
#     min_vol = min(vol)
#     mean_vol = sum_vol / num_frames
#     std_vol = math.sqrt(sum((vol_value - mean_vol) ** 2 for vol_value in vol) / len(vol))
#     vstd = std_vol / max_vol if max_vol > 0 else 0
#     vdr = (max_vol - min_vol) / max_vol
#
#     frames_per_window = sample_rate // frame_size
#
#     peaks_all = []
#     valleys_all = []
#
#     # Analiza w oknach 1-sekundowych
#     for start in range(0, len(vol), frames_per_window):
#         window_vol = vol[start:start + frames_per_window]
#         peaks = []
#         valleys = []
#         if len(window_vol) == 0:
#             continue
#         for j in range(1, len(window_vol) - 1):
#             if window_vol[j] > window_vol[j - 1] and window_vol[j] > window_vol[j + 1]:
#                 peaks.append(window_vol[j])
#             elif window_vol[j] < window_vol[j - 1] and window_vol[j] < window_vol[j + 1]:
#                 valleys.append(window_vol[j])
#         print("peaks: ", peaks)
#         print("valleys: ", valleys)
#         peaks_all.append(peaks)
#         valleys_all.append(valleys)
#
#     # peaks = []
#     # valleys = []
#     # for j in range(1, len(vol) - 1):
#     #     if vol[j] > vol[j - 1] and vol[j] > vol[j + 1]:
#     #         peaks.append(vol[j])
#     #     elif vol[j] < vol[j - 1] and vol[j] < vol[j + 1]:
#     #         valleys.append(vol[j])
#
#     # Oblicz różnice między sąsiednimi pikami i dolinami
#     vu_all = []
#     for i in range(0, len(peaks_all)):
#         vu = 0
#
#         for p, v in zip(peaks_all[i], valleys_all[i]):
#             vu += abs(p - v)
#         vu_all.append(vu)
#     # vu = 0
#     #
#     # for p, v in zip(peaks, valleys):
#     #     vu += abs(p - v)
#     # print("vol: ", vol)
#     # print("peaks: ",peaks)
#     # print("valleys: ", valleys)
#
#     label.config(text="VSTD = " + str(vstd)  +
#                       "\nVDR = " + str(vdr) +
#                       "\nVU = " + str(vu_all))
#     label.grid()


# import math
#
#
# def calculate_VSTD(frame_size, label):
#     global func_nr
#     func_nr = 8
#     max_val = max(abs(x) for x in audio_data)
#     audio_data_sk = [x / max_val for x in audio_data]
#
#     # Obliczanie liczby ramek w nagraniu
#     num_frames = len(audio_data_sk) // frame_size
#     vol = []
#     sum_vol = 0
#
#     # Obliczanie głośności (vol) dla całego nagrania
#     for i in range(num_frames):
#         frame_start = i * frame_size
#         frame_end = min(frame_start + frame_size, len(audio_data_sk))
#         frame = audio_data_sk[frame_start:frame_end]
#         frame = [float(x) for x in frame]
#         vol_value = (sum(((x ** 2) / len(frame)) for x in frame)) ** 0.5
#         sum_vol += vol_value
#         vol.append(vol_value)
#
#     # Obliczanie VSTD_full dla całego nagrania
#     max_vol = max(vol)
#     min_vol = min(vol)
#     mean_vol = sum_vol / num_frames
#     std_vol = math.sqrt(sum((vol_value - mean_vol) ** 2 for vol_value in vol) / len(vol))
#     VSTD_full = std_vol / max_vol if max_vol > 0 else 0
#
#     # Analiza w oknach 1-sekundowych
#     frames_per_window = sample_rate // frame_size
#     peaks_all = []
#     valleys_all = []
#     vstd = []  # Lista do przechowywania VSTD dla każdego okna 1-sekundowego
#
#     for start in range(0, len(vol), frames_per_window):
#         window_vol = vol[start:start + frames_per_window]
#         peaks = []
#         valleys = []
#         if len(window_vol) == 0:
#             continue
#         for j in range(1, len(window_vol) - 1):
#             if window_vol[j] > window_vol[j - 1] and window_vol[j] > window_vol[j + 1]:
#                 peaks.append(window_vol[j])
#             elif window_vol[j] < window_vol[j - 1] and window_vol[j] < window_vol[j + 1]:
#                 valleys.append(window_vol[j])
#         peaks_all.append(peaks)
#         valleys_all.append(valleys)
#
#         # Obliczanie VSTD dla każdego okna 1-sekundowego
#         window_mean_vol = sum(window_vol) / len(window_vol)
#         window_std_vol = math.sqrt(sum((x - window_mean_vol) ** 2 for x in window_vol) / len(window_vol))
#         VSTD_window = window_std_vol / max(window_vol) if max(window_vol) > 0 else 0
#         vstd.append(VSTD_window)
#
#     # Wyświetlanie wyników
#     label.config(text="VSTD_full = " + str(VSTD_full) +
#                       "\nvstd (dla każdego okna 1s) = " + str(vstd))
#     label.grid()

# import math
#
#
# def calculate_VSTD(frame_size, label):
#     global func_nr
#     func_nr = 8
#     max_val = max(abs(x) for x in audio_data)
#     audio_data_sk = [x / max_val for x in audio_data]
#
#     # Obliczanie liczby ramek w nagraniu
#     num_frames = len(audio_data_sk) // frame_size
#     vol = []
#     sum_vol = 0
#
#     # Obliczanie głośności (vol) dla całego nagrania
#     for i in range(num_frames):
#         frame_start = i * frame_size
#         frame_end = min(frame_start + frame_size, len(audio_data_sk))
#         frame = audio_data_sk[frame_start:frame_end]
#         frame = [float(x) for x in frame]
#         vol_value = (sum(((x ** 2) / len(frame)) for x in frame)) ** 0.5
#         sum_vol += vol_value
#         vol.append(vol_value)
#
#     # Obliczanie VSTD_full i VDR_full dla całego nagrania
#     max_vol = max(vol)
#     min_vol = min(vol)
#     mean_vol = sum_vol / num_frames
#     std_vol = math.sqrt(sum((vol_value - mean_vol) ** 2 for vol_value in vol) / len(vol))
#     VSTD_full = std_vol / max_vol if max_vol > 0 else 0
#     VDR_full = (max_vol - min_vol) / max_vol if max_vol > 0 else 0
#
#     # Analiza w oknach 1-sekundowych
#     frames_per_window = sample_rate // frame_size
#     peaks_all = []
#     valleys_all = []
#     vstd = []  # Lista do przechowywania VSTD dla każdego okna 1-sekundowego
#     vdr = []  # Lista do przechowywania VDR dla każdego okna 1-sekundowego
#
#     for start in range(0, len(vol), frames_per_window):
#         window_vol = vol[start:start + frames_per_window]
#         peaks = []
#         valleys = []
#         if len(window_vol) == 0:
#             continue
#         for j in range(1, len(window_vol) - 1):
#             if window_vol[j] > window_vol[j - 1] and window_vol[j] > window_vol[j + 1]:
#                 peaks.append(window_vol[j])
#             elif window_vol[j] < window_vol[j - 1] and window_vol[j] < window_vol[j + 1]:
#                 valleys.append(window_vol[j])
#         peaks_all.append(peaks)
#         valleys_all.append(valleys)
#
#         # Obliczanie VSTD dla każdego okna 1-sekundowego
#         window_mean_vol = sum(window_vol) / len(window_vol)
#         window_std_vol = math.sqrt(sum((x - window_mean_vol) ** 2 for x in window_vol) / len(window_vol))
#         VSTD_window = window_std_vol / max(window_vol) if max(window_vol) > 0 else 0
#         vstd.append(VSTD_window)
#
#         # Obliczanie VDR dla każdego okna 1-sekundowego
#         window_max_vol = max(window_vol)
#         window_min_vol = min(window_vol)
#         VDR_window = (window_max_vol - window_min_vol) / window_max_vol if window_max_vol > 0 else 0
#         vdr.append(VDR_window)
#
#     # Wyświetlanie wyników
#     label.config(text="VSTD_full = " + str(VSTD_full) +
#                       "\nVDR_full = " + str(VDR_full) +
#                       "\nvstd (dla każdego okna 1s) = " + str(vstd) +
#                       "\nvdr (dla każdego okna 1s) = " + str(vdr))
#     label.grid()


import math

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

    # # Wyświetlanie wyników
    # label.config(text="VSTD_full = " + str(VSTD_full) +
    #                   "\nVDR_full = " + str(VDR_full) +
    #                   "\nvstd (dla każdego okna 1s) = " + str(vstd) +
    #                   "\nvdr (dla każdego okna 1s) = " + str(vdr) +
    #                   "\nVU_full = " + str(VU_full) +
    #                   "\nvu (dla każdego okna 1s) = " + str(vu_all))

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


# def calculate_LSTER(frame_size, label, segment_size):
#     global func_nr
#     func_nr = 9
#
#     # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
#     time = [i / sample_rate for i in range(0, len(audio_data))]
#
#     max_val = max(abs(x) for x in audio_data)
#     audio_data_sk = [x / max_val for x in audio_data]
#
#     # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
#     num_frames = len(audio_data) // frame_size
#     ste = []
#     frames_per_window = sample_rate // frame_size
#
#     entropy = []
#     entropy_val = 0
#     for i in range(num_frames):
#         frame_start = i * frame_size
#         frame_end = min(frame_start + frame_size, len(audio_data))
#         frame = audio_data_sk[frame_start:frame_end]
#         entropy_val += calculate_EE(frame, segment_size, audio_data_sk)
#         print(entropy_val)
#         print("par: ", frames_per_window)
#         print("i: ", i)
#         if i % frames_per_window == frames_per_window - 1:
#             entropy.append(entropy_val)
#             entropy_val = 0
#         # Oblicz RMS dla każdej ramki
#         # rms_value = (sum(x ** 2 for x in frame) / len(frame)) ** 0.5
#         ste_value = (sum(((x ** 2) / len(frame)) for x in frame))
#         ste.append(ste_value)
#     if entropy_val != 0:
#         entropy.append(entropy_val)
#
#     # lster_count = 0
#     lster_per_window = []
#
#     # Analiza w oknach 1-sekundowych
#     for start in range(0, len(ste), frames_per_window):
#         window_ste = ste[start:start + frames_per_window]
#         if len(window_ste) == 0:
#             continue
#
#         # Oblicz średnią STE w oknie
#         av_ste = sum(window_ste) / len(window_ste)
#
#         # Licz ramki z niską energią (STE < 50% średniej)
#         low_energy_frames = sum(1 for ste in window_ste if ste < 0.5 * av_ste)
#         lster = low_energy_frames / len(window_ste)
#         lster_per_window.append(lster)
#         # Dodaj wynik do całkowitej liczby ramek o niskiej energii
#     #     lster_count += low_energy_frames
#     #
#     # # Oblicz odsetek ramek z niską energią
#     # lster = lster_count / num_frames if num_frames > 0 else 0
#
#     label.config(text="LSTER = " + str(lster_per_window) + "\nEnergy Entropy = " + str(entropy))
#     label.grid()
#
#
# def calculate_EE(frame, segment_size, audio_data_sk):
#     # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
#     num_segments = len(frame) // segment_size
#     ste = []
#     ste_time = []
#
#     for i in range(num_segments):
#         segment_start = i * segment_size
#         segment_end = min(segment_start + segment_size, len(audio_data))
#         segment = audio_data_sk[segment_start:segment_end]
#
#         # Oblicz RMS dla każdej ramki
#         # rms_value = (sum(x ** 2 for x in frame) / len(frame)) ** 0.5
#         ste_value = (sum(((x ** 2) / len(segment)) for x in segment))
#         ste.append(ste_value)
#     if len(frame) % segment_size != 0:
#         segment = frame[num_segments * segment_size:]
#         ste.append(sum(x ** 2 for x in segment))
#     total_energy = sum(ste)
#     print("total_energy: ", total_energy)
#     print("ste: ", ste)
#     # for i in range(len(ste)):
#     #     ste[i] = ste[i]/total_energy
#     ste = [e / total_energy for e in ste]
#     print("ste: ", ste)
#     print(math.log(ste[0], 2))
#     entropy = -sum(e * math.log(e, 2) for e in ste if e > 0)
#     print("entropy: ", entropy)
#     return entropy

# def calculate_LSTER(frame_size, label, segment_size):
#     global func_nr
#     func_nr = 9
#
#     # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
#     time = [i / sample_rate for i in range(0, len(audio_data))]
#
#     max_val = max(abs(x) for x in audio_data)
#     audio_data_sk = [x / max_val for x in audio_data]
#
#     # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
#     num_frames = len(audio_data) // frame_size
#     ste = []
#     frames_per_window = sample_rate // frame_size
#
#     entropy = []
#     entropy_val = 0
#     for i in range(num_frames):
#         frame_start = i * frame_size
#         frame_end = min(frame_start + frame_size, len(audio_data))
#         frame = audio_data_sk[frame_start:frame_end]
#         entropy_val += calculate_EE(frame, segment_size, audio_data_sk)
#         print(entropy_val)
#         print("par: ", frames_per_window)
#         print("i: ", i)
#         if i % frames_per_window == frames_per_window - 1:
#             entropy.append(entropy_val)
#             entropy_val = 0
#         # Oblicz RMS dla każdej ramki
#         # rms_value = (sum(x ** 2 for x in frame) / len(frame)) ** 0.5
#         ste_value = (sum(((x ** 2) / len(frame)) for x in frame))
#         ste.append(ste_value)
#
#     if entropy_val != 0:
#         entropy.append(entropy_val)
#
#     # lster_per_window to lista odsetków ramek z niską energią w każdej sekundy
#     lster_per_window = []
#
#     # Analiza w oknach 1-sekundowych
#     for start in range(0, len(ste), frames_per_window):
#         window_ste = ste[start:start + frames_per_window]
#         if len(window_ste) == 0:
#             continue
#
#         # Oblicz średnią STE w oknie
#         av_ste = sum(window_ste) / len(window_ste)
#
#         # Licz ramki z niską energią (STE < 50% średniej)
#         low_energy_frames = sum(1 for ste in window_ste if ste < 0.5 * av_ste)
#         lster = low_energy_frames / len(window_ste)
#         lster_per_window.append(lster)
#
#     # Obliczenie średniego LSTER (LSTER_full)
#     if len(lster_per_window) > 0:
#         LSTER_full = sum(lster_per_window) / len(lster_per_window)
#     else:
#         LSTER_full = 0
#
#     label.config(text="LSTER per window = " + str(lster_per_window) +
#                       "\nLSTER full = " + str(LSTER_full) +
#                       "\nEnergy Entropy = " + str(entropy))
#     label.grid()
#
#
# def calculate_EE(frame, segment_size, audio_data_sk):
#     # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
#     num_segments = len(frame) // segment_size
#     ste = []
#     ste_time = []
#
#     for i in range(num_segments):
#         segment_start = i * segment_size
#         segment_end = min(segment_start + segment_size, len(audio_data))
#         segment = audio_data_sk[segment_start:segment_end]
#
#         # Oblicz RMS dla każdej ramki
#         # rms_value = (sum(x ** 2 for x in frame) / len(frame)) ** 0.5
#         ste_value = (sum(((x ** 2) / len(segment)) for x in segment))
#         ste.append(ste_value)
#     if len(frame) % segment_size != 0:
#         segment = frame[num_segments * segment_size:]
#         ste.append(sum(x ** 2 for x in segment))
#     total_energy = sum(ste)
#     print("total_energy: ", total_energy)
#     print("ste: ", ste)
#     # for i in range(len(ste)):
#     #     ste[i] = ste[i]/total_energy
#     ste = [e / total_energy for e in ste]
#     print("ste: ", ste)
#     print(math.log(ste[0], 2))
#     entropy = -sum(e * math.log(e, 2) for e in ste if e > 0)
#     print("entropy: ", entropy)
#     return entropy

# def calculate_LSTER(frame_size, label, segment_size):
#     global func_nr
#     func_nr = 9
#
#     # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
#     time = [i / sample_rate for i in range(0, len(audio_data))]
#
#     max_val = max(abs(x) for x in audio_data)
#     audio_data_sk = [x / max_val for x in audio_data]
#
#     # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
#     num_frames = len(audio_data) // frame_size
#     ste = []
#     frames_per_window = sample_rate // frame_size
#
#     entropy = []
#     entropy_val = 0
#     all_entropy_values = []  # Zbiera wszystkie entropie z ramek
#
#     for i in range(num_frames):
#         frame_start = i * frame_size
#         frame_end = min(frame_start + frame_size, len(audio_data))
#         frame = audio_data_sk[frame_start:frame_end]
#         entropy_val += calculate_EE(frame, segment_size, audio_data_sk)
#         all_entropy_values.append(entropy_val)  # Dodajemy wartość entropii każdej ramki
#         print(entropy_val)
#         print("par: ", frames_per_window)
#         print("i: ", i)
#         if i % frames_per_window == frames_per_window - 1:
#             entropy.append(entropy_val)
#             entropy_val = 0
#         # Oblicz RMS dla każdej ramki
#         # rms_value = (sum(x ** 2 for x in frame) / len(frame)) ** 0.5
#         ste_value = (sum(((x ** 2) / len(frame)) for x in frame))
#         ste.append(ste_value)
#
#     if entropy_val != 0:
#         entropy.append(entropy_val)
#
#     # lster_per_window to lista odsetków ramek z niską energią w każdej sekundy
#     lster_per_window = []
#
#     # Analiza w oknach 1-sekundowych
#     for start in range(0, len(ste), frames_per_window):
#         window_ste = ste[start:start + frames_per_window]
#         if len(window_ste) == 0:
#             continue
#
#         # Oblicz średnią STE w oknie
#         av_ste = sum(window_ste) / len(window_ste)
#
#         # Licz ramki z niską energią (STE < 50% średniej)
#         low_energy_frames = sum(1 for ste in window_ste if ste < 0.5 * av_ste)
#         lster = low_energy_frames / len(window_ste)
#         lster_per_window.append(lster)
#
#     # Obliczenie średniego LSTER (LSTER_full)
#     if len(lster_per_window) > 0:
#         LSTER_full = sum(lster_per_window) / len(lster_per_window)
#     else:
#         LSTER_full = 0
#
#     # Obliczenie entropii energetycznej dla całego nagrania
#     print("all_entropy_values  ", all_entropy_values)
#     total_entropy = sum(all_entropy_values)  # Suma wszystkich entropii
#     print("total_entrupy", total_entropy)
#
#     if len(all_entropy_values) > 0:
#         energy_entropy_full = total_entropy / len(all_entropy_values)  # Średnia entropii
#     else:
#         energy_entropy_full = 0
#
#     label.config(text="LSTER per window = " + str(lster_per_window) +
#                       "\nLSTER full = " + str(LSTER_full) +
#                       "\nEnergy Entropy per window = " + str(entropy) +
#                       "\nEnergy Entropy full = " + str(energy_entropy_full))
#     label.grid()
#
#
# def calculate_EE(frame, segment_size, audio_data_sk):
#     # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
#     num_segments = len(frame) // segment_size
#     ste = []
#     ste_time = []
#
#     for i in range(num_segments):
#         segment_start = i * segment_size
#         segment_end = min(segment_start + segment_size, len(audio_data))
#         segment = audio_data_sk[segment_start:segment_end]
#
#         # Oblicz RMS dla każdej ramki
#         # rms_value = (sum(x ** 2 for x in frame) / len(frame)) ** 0.5
#         ste_value = (sum(((x ** 2) / len(segment)) for x in segment))
#         ste.append(ste_value)
#     if len(frame) % segment_size != 0:
#         segment = frame[num_segments * segment_size:]
#         ste.append(sum(x ** 2 for x in segment))
#     total_energy = sum(ste)
#     print("total_energy: ", total_energy)
#     print("ste: ", ste)
#     # for i in range(len(ste)):
#     #     ste[i] = ste[i]/total_energy
#     ste = [e / total_energy for e in ste]
#     print("ste: ", ste)
#     print(math.log(ste[0], 2))
#     entropy = -sum(e * math.log(e, 2) for e in ste if e > 0)
#     print("entropy: ", entropy)
#     return entropy

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
        normalized_energies = [energy / total_energy for energy in segment_energies] if total_energy != 0 else [0] * len(segment_energies)

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
        low_energy_frames = sum(1 for ste_val in window_ste if ste_val < 0.5 * av_ste)
        lster = low_energy_frames / len(window_ste)
        lster_per_window.append(lster)

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


# def compute_entropy(frame_size, segment_size):
#     # Krok 1: Podziel sygnał na ramki o rozmiarze frame_size
#     num_frames = len(audio_data) // frame_size
#     entropies = []
#
#     for frame_idx in range(num_frames):
#         # Wybieramy próbki dla bieżącej ramki
#         frame = audio_data[frame_idx * frame_size:(frame_idx + 1) * frame_size]
#
#         # Krok 2: Dziel ramkę na segmenty o rozmiarze segment_size
#         num_segments = len(frame) // segment_size
#         segment_energies = []
#
#         for seg_idx in range(num_segments):
#             # Pobieramy próbki dla bieżącego segmentu
#             segment = frame[seg_idx * segment_size:(seg_idx + 1) * segment_size]
#
#             # Obliczamy energię segmentu (suma kwadratów próbek)
#             energy = sum(x ** 2 for x in segment)
#             segment_energies.append(energy)
#
#         # Krok 3: Normalizacja energii segmentów
#         total_energy = sum(segment_energies)
#         if total_energy == 0:
#             normalized_energies = [0] * len(segment_energies)  # Jeśli energia całkowita wynosi 0
#         else:
#             normalized_energies = [energy / total_energy for energy in segment_energies]
#
#         # Krok 4: Obliczanie entropii na podstawie znormalizowanych energii
#         entropy = 0
#         for energy in normalized_energies:
#             if energy > 0:  # Aby uniknąć log(0)
#                 entropy -= energy * math.log2(energy)
#
#         entropies.append(entropy)
#
#     # Zwracamy średnią entropię dla wszystkich ramek
#     return sum(entropies) / len(entropies) if entropies else 0
#
#
#
# def calculate_LSTER(frame_size, label, segment_size):
#     global func_nr
#     func_nr = 9
#     max_val = max(abs(x) for x in audio_data)
#     audio_data_sk = [x / max_val for x in audio_data]
#
#     # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
#     num_frames = len(audio_data) // frame_size
#     ste = []
#     frames_per_window = sample_rate // frame_size
#
#     entropy = []
#     all_entropy_values = []  # Zbiera wszystkie entropie z ramek
#     energy_entropy_per_window = []  # Zbiera entropie energetyczne dla każdego okna
#
#     total_energy = 0  # Zmienna na całkowitą energię nagrania
#
#     for i in range(num_frames):
#         frame_start = i * frame_size
#         frame_end = min(frame_start + frame_size, len(audio_data))
#         frame = audio_data_sk[frame_start:frame_end]
#         entropy_val = calculate_EE(frame, segment_size, audio_data_sk)
#         all_entropy_values.append(entropy_val)  # Dodajemy wartość entropii każdej ramki
#         total_energy += sum(x ** 2 for x in frame)  # Sumujemy energię z całego nagrania
#
#
#         if i % frames_per_window == frames_per_window - 1:
#             entropy.append(entropy_val)
#
#         # Oblicz RMS dla każdej ramki
#         ste_value = (sum(((x ** 2) / len(frame)) for x in frame))
#         ste.append(ste_value)
#     energy_entropy_full = compute_entropy(frame_size, segment_size)
#     # Oblicz średnią entropię energetyczną dla całego nagrania
#     # if total_energy > 0:
#     #     energy_entropy_full = sum(all_entropy_values) / total_energy  # Normalizowanie przez całkowitą energię
#     # else:
#     #     energy_entropy_full = 0
#
#     # lster_per_window to lista odsetków ramek z niską energią w każdej sekundy
#     lster_per_window = []
#
#     # Analiza w oknach 1-sekundowych
#     for start in range(0, len(ste), frames_per_window):
#         window_ste = ste[start:start + frames_per_window]
#         if len(window_ste) == 0:
#             continue
#
#         # Oblicz średnią STE w oknie
#         av_ste = sum(window_ste) / len(window_ste)
#
#         # Licz ramki z niską energią (STE < 50% średniej)
#         low_energy_frames = sum(1 for ste in window_ste if ste < 0.5 * av_ste)
#         lster = low_energy_frames / len(window_ste)
#         lster_per_window.append(lster)
#
#         # Obliczanie energy entropy dla okna
#         energy_entropy = calculate_energy_entropy(window_ste)
#         energy_entropy_per_window.append(energy_entropy)
#
#     # Obliczenie średniego LSTER (LSTER_full)
#     if len(lster_per_window) > 0:
#         LSTER_full = sum(lster_per_window) / len(lster_per_window)
#     else:
#         LSTER_full = 0
#
#     # # Wyświetlanie wyników
#     # label.config(text="LSTER per window = " + str(lster_per_window) +
#     #                   "\nLSTER full = " + str(LSTER_full) +
#     #                   "\nEnergy Entropy per window = " + str(energy_entropy_per_window) +
#     #                   "\nEnergy Entropy full = " + str(energy_entropy_full))
#
#     LSTER_full_str = format_value(LSTER_full)
#     energy_entropy_full_str = format_value(energy_entropy_full)
#     lster_per_window_str = [format_value(val) for val in lster_per_window]  # Sformatuj każdą wartość w liście vstd
#     energy_entropy_per_window_str = [format_value(val) for val in energy_entropy_per_window]  # Sformatuj każdą wartość w liście vdr
# # Sformatuj każdą wartość w liście vu_all
#
#     # Wyświetlenie wyników w label
#     label.config(text="LSTER = " + LSTER_full_str +
#                       "\nEnergy Entropy full = " + energy_entropy_full_str +
#                       "\nLSTER (dla każdego okna 1s) = " + ", ".join(lster_per_window_str) +  # Wyświetlanie listy vstd
#                       "\nEnergy Entropy (dla każdego okna 1s) = " + ", ".join(energy_entropy_per_window_str))  # Wyświetlanie listy vu_all
#
#     label.grid()
#
#
# def calculate_EE(frame, segment_size, audio_data_sk):
#     # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
#     num_segments = len(frame) // segment_size
#     ste = []
#     ste_time = []
#
#     for i in range(num_segments):
#         segment_start = i * segment_size
#         segment_end = min(segment_start + segment_size, len(audio_data))
#         segment = audio_data_sk[segment_start:segment_end]
#
#         ste_value = (sum(((x ** 2) / len(segment)) for x in segment))
#         ste.append(ste_value)
#
#     if len(frame) % segment_size != 0:
#         segment = frame[num_segments * segment_size:]
#         ste.append(sum(x ** 2 for x in segment))
#
#     total_energy = sum(ste)
#     ste = [e / total_energy for e in ste]
#
#     entropy = -sum(e * math.log(e, 2) for e in ste if e > 0)
#     return entropy
#
#
# ##################### do poprawy EE
#
# def calculate_energy_entropy(ste_values):
#     # Normalizacja energii w oknie
#     total_energy = sum(ste_values)
#     if total_energy > 0:
#         normalized_ste = [e / total_energy for e in ste_values]
#
#         # Obliczanie entropii energetycznej dla okna
#         energy_entropy = -sum(e * math.log(e, 2) for e in normalized_ste if e > 0)
#         return energy_entropy
#     else:
#         return 0


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


def scroll_function1(fig, canvas, position, slider, scrollbar, scrollbar2):
    """
    Obsługuje przesunięcie widocznego fragmentu danych na wykresie.
    """
    if audio_data is not None:
        max_points = 10000  # Maksymalna liczba punktów widocznych na raz
        if len(audio_data) <= max_points:
            # Gdy długość audio jest mniejsza niż max_points, start_idx zawsze wynosi 0
            start_idx = 0
        else:
            # Oblicz przesunięcie dla większych danych
            # start_idx = position * 200
            start_idx = position * slider.get()
            max_scroll = (len(audio_data) - 10000) // slider.get()  # Zakres przewijania w krokach
            scrollbar.configure(to=max_scroll)
            scrollbar2.configure(to=max_scroll)

        # start_idx = position * 200  # Przesunięcie na podstawie pozycji suwaka
        plot_audio_waveform(sample_rate, audio_data, fig, canvas, start_idx=start_idx)


def scroll_function(fig, canvas, position, slider, slider2, slider3, scrollbar, scrollbar2):
    """
    Obsługuje przesunięcie widocznego fragmentu danych na wykresie.
    """
    if audio_data is not None:
        max_points = 10000  # Maksymalna liczba punktów widocznych na raz
        if len(audio_data) <= max_points:
            # Gdy długość audio jest mniejsza niż max_points, start_idx zawsze wynosi 0
            start_idx = 0
        else:
            # Oblicz przesunięcie dla większych danych
            # start_idx = position * 200
            start_idx = position * slider.get()
            max_scroll = (len(audio_data) - 10000) // slider.get()  # Zakres przewijania w krokach
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
