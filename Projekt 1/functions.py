import math

from scipy.io import wavfile
import numpy as np
from tkinter import filedialog
import matplotlib.pyplot as plt


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
    elif function_nr >1 and function_nr <= 7:
        slider.configure(to=500, from_=1)
        slider.grid()
        scrollbar2.grid()
        if len(audio_data) > 10000:
            max_scroll = (len(audio_data)-10000) // slider.get()  # Zakres przewijania w krokach
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
            slider2.grid()
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
        if function_nr ==8:
            calculate_VSTD(slider.get(), label)
        elif function_nr ==9:
            slider2.grid()
            slider2.configure(to=slider.get()//2, from_=1)
            calculate_LSTER(slider.get(), label, slider2.get())

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
    ax.set_ylim(min(audio_data)*0.9, max(audio_data)*1.1)
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
    ax.set_ylim(0, max(max(rms)*1.05, 300000))
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
    ax.set_ylim(0, max(max(zcr)*1.1,0.8))
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
    print(min(f0)*0.9)
    ax.set_ylim(min(min(f0)*0.9, 0), max(max(f0)*1.1,23000 ))
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
    ax.set_ylim(min(min(f0)*0.95,40), max(max(f0)*1.05,105))

    ax.legend()
    fig.tight_layout()
    canvas.draw()

def calculate_VSTD(frame_size, label):
    global func_nr
    func_nr = 8
    max_val = max(abs(x) for x in audio_data)
    audio_data_sk = [x / max_val for x in audio_data]
    # max_val = max(audio_data)  # Maksymalna wartość w oryginalnych danych
    # min_val = min(audio_data)  # Minimalna wartość w oryginalnych danych
    #
    # # Normalizacja danych: (x - min) / (max - min)
    # audio_data_sk = [(x - min_val) / (max_val - min_val) for x in audio_data]
    print(audio_data_sk)
    num_frames = len(audio_data_sk) // frame_size
    vol = []
    sum_vol = 0
    for i in range(num_frames):
        frame_start = i * frame_size
        frame_end = min(frame_start + frame_size, len(audio_data_sk))
        frame = audio_data_sk[frame_start:frame_end]
        frame = [float(x) for x in frame]
        vol_value = (sum(((x ** 2) / len(frame)) for x in frame)) ** 0.5
        sum_vol += vol_value
        vol.append(vol_value)
    max_vol = max(vol)
    min_vol = min(vol)
    mean_vol = sum_vol / num_frames
    std_vol = math.sqrt(sum((vol_value - mean_vol)**2 for vol_value in vol) / len(vol))
    vstd = std_vol / max_vol if max_vol > 0 else 0
    vdr = (max_vol - min_vol) / max_vol

    frames_per_window = sample_rate // frame_size

    peaks_all = []
    valleys_all = []

    # Analiza w oknach 1-sekundowych
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
        print("peaks: ", peaks)
        print("valleys: ", valleys)
        peaks_all.append(peaks)
        valleys_all.append(valleys)



    # peaks = []
    # valleys = []
    # for j in range(1, len(vol) - 1):
    #     if vol[j] > vol[j - 1] and vol[j] > vol[j + 1]:
    #         peaks.append(vol[j])
    #     elif vol[j] < vol[j - 1] and vol[j] < vol[j + 1]:
    #         valleys.append(vol[j])

    # Oblicz różnice między sąsiednimi pikami i dolinami
    vu_all = []
    for i in range(0, len(peaks_all)):
        vu=0

        for p, v in zip(peaks_all[i], valleys_all[i]):
            vu += abs(p - v)
        vu_all.append(vu)
    # vu = 0
    #
    # for p, v in zip(peaks, valleys):
    #     vu += abs(p - v)
    # print("vol: ", vol)
    # print("peaks: ",peaks)
    # print("valleys: ", valleys)

    label.config(text="VSTD = " + str(vstd) + "   std = " + str(std_vol) + "   mean = " + str(mean_vol) +
                      "   max = " + str(max_vol) + "\nmin_vol = " + str(min_vol) + "   VDR = " + str(vdr) +
                      "\nVU = " + str(vu_all))
    label.grid()


def calculate_LSTER(frame_size, label, segment_size):
    global func_nr
    func_nr = 9

    # Wyznaczanie zakresu widocznych danych (start_idx do end_idx)
    time = [i / sample_rate for i in range(0,len(audio_data))]


    max_val = max(abs(x) for x in audio_data)
    audio_data_sk = [x / max_val for x in audio_data]


    # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
    num_frames = len(audio_data) // frame_size
    ste = []
    frames_per_window = sample_rate // frame_size

    entropy = []
    entropy_val = 0
    for i in range(num_frames):
        frame_start = i * frame_size
        frame_end = min(frame_start + frame_size, len(audio_data))
        frame = audio_data_sk[frame_start:frame_end]
        entropy_val += calculate_EE(frame, segment_size, audio_data_sk)
        print(entropy_val)
        print("par: ", frames_per_window)
        print("i: ", i)
        if i % frames_per_window == frames_per_window - 1:
            entropy.append(entropy_val)
            entropy_val = 0
        # Oblicz RMS dla każdej ramki
        # rms_value = (sum(x ** 2 for x in frame) / len(frame)) ** 0.5
        ste_value = (sum(((x ** 2) / len(frame)) for x in frame))
        ste.append(ste_value)
    if entropy_val != 0:
        entropy.append(entropy_val)

    # lster_count = 0
    lster_per_window = []

    # Analiza w oknach 1-sekundowych
    for start in range(0, len(ste), frames_per_window):
        window_ste = ste[start:start + frames_per_window]
        if len(window_ste) == 0:
            continue

        # Oblicz średnią STE w oknie
        av_ste = sum(window_ste) / len(window_ste)

        # Licz ramki z niską energią (STE < 50% średniej)
        low_energy_frames = sum(1 for ste in window_ste if ste < 0.5 * av_ste)
        lster = low_energy_frames / len(window_ste)
        lster_per_window.append(lster)
        # Dodaj wynik do całkowitej liczby ramek o niskiej energii
    #     lster_count += low_energy_frames
    #
    # # Oblicz odsetek ramek z niską energią
    # lster = lster_count / num_frames if num_frames > 0 else 0



    label.config(text="LSTER = " + str(lster_per_window) + "\nEnergy Entropy = " + str(entropy))
    label.grid()

def calculate_EE(frame, segment_size, audio_data_sk):

    # Obliczenie RMS na poziomie ramek widocznych w zakresie (start_idx -> end_idx)
    num_segments = len(frame) // segment_size
    ste = []
    ste_time = []

    for i in range(num_segments):
        segment_start = i * segment_size
        segment_end = min(segment_start + segment_size, len(audio_data))
        segment = audio_data_sk[segment_start:segment_end]

        # Oblicz RMS dla każdej ramki
        # rms_value = (sum(x ** 2 for x in frame) / len(frame)) ** 0.5
        ste_value = (sum(((x ** 2) / len(segment)) for x in segment))
        ste.append(ste_value)
    if len(frame) % segment_size != 0:
        segment = frame[num_segments * segment_size:]
        ste.append(sum(x ** 2 for x in segment))
    total_energy = sum(ste)
    print("total_energy: ", total_energy)
    print("ste: ", ste)
    # for i in range(len(ste)):
    #     ste[i] = ste[i]/total_energy
    ste = [e / total_energy for e in ste]
    print("ste: ", ste)
    print(math.log(ste[0], 2))
    entropy = -sum(e * math.log(e, 2) for e in ste if e > 0)
    print("entropy: ", entropy)
    return entropy


def slider_function(slider, canvas, fig, slider2, slider3, label):
    # global func_nr
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
    elif func_nr ==9:
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
            max_scroll = (len(audio_data)-10000) // slider.get()  # Zakres przewijania w krokach
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
