import math
from tkinter import filedialog

import numpy as np
import sounddevice as sd
from scipy.io import wavfile


def menu_function(fig, canvas, slider, function_nr, scrollbar, scrollbar2, slider2, slider3, label, canvas_widget,
                  rbtn1, rbtn2, rbtn3, rbtn4, rbtn5, v):
    slider2.grid_remove()
    slider3.grid_remove()
    slider.grid_remove()
    label.grid_remove()
    canvas_widget.grid()
    rbtn1.grid_remove()
    rbtn2.grid_remove()
    rbtn3.grid_remove()
    rbtn5.grid_remove()
    rbtn4.grid_remove()
    if function_nr == 1:
        slider.grid_remove()
        scrollbar.set(0)
        scrollbar.grid()
        scrollbar2.grid_remove()
        load_audio(fig, canvas, scrollbar, scrollbar2)
    if func_nr == 19:
        slider.grid_remove()
        scrollbar.set(0)
        scrollbar.grid()
        scrollbar2.grid_remove()
        plot_audio_waveform(sample_rate, audio_data, fig, canvas)
    if function_nr > 1 and function_nr <= 7:
        slider.configure(to=min(0.25 * sample_rate, 2000), from_=1)
        slider.set(0.02 * sample_rate)
        slider.grid()
        scrollbar2.grid()
        if len(audio_data) > 20000:
            max_scroll = (len(audio_data) - 20000) // slider.get()
        else:
            scrollbar.grid_remove()
            scrollbar2.grid_remove()
        if function_nr == 2:
            print("menu vol", type(fig))
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
    ## projekt 2
    elif function_nr == 20:
        rbtn1.grid()
        rbtn2.grid()
        rbtn3.grid()
        rbtn5.grid()
        rbtn4.grid()

        max_scroll = (len(audio_data) - slider2.get()) // slider.get()
        scrollbar2.configure(to=max_scroll)
        print("menu max: ", max_scroll)
        scrollbar2.set(0)
        # scrollbar2.config(from_=0, to = max(audio_data))
        scrollbar2.grid()
        slider2.config(from_=1, to=len(audio_data), label="wielkość próbki do fft")
        slider2.set(20000)
        print("zakres, pop  ", len(audio_data))
        print("wartość slider   ", slider2.get())
        slider2.grid()
        print("menu", type(fig))
        calc_show_freq(fig, canvas, v, 0, slider2.get())
    # elif function_nr == 19:
    #     calc_show_freq(fig, canvas, 0, len(audio_data))

    elif function_nr > 20:
        rbtn1.grid()
        rbtn2.grid()
        rbtn3.grid()
        rbtn5.grid()
        rbtn4.grid()
        slider.configure(to=min(0.25 * sample_rate, 2000), from_=1)
        slider.set(0.02 * sample_rate)
        slider.grid()
        scrollbar2.grid()
        if len(audio_data) > 20000:
            max_scroll = (len(audio_data) - 20000) // slider.get()
        else:
            scrollbar.grid_remove()
            scrollbar2.grid_remove()
        if function_nr == 21:
            calculate_volume_freq_and_plot(slider.get(), fig, canvas, v)
        elif function_nr == 22:
            calculate_frequency_centroid_and_plot(slider.get(), fig, canvas, v)
        elif function_nr == 23:
            calculate_effective_bandwidth_and_plot(slider.get(), fig, canvas, v)
        elif function_nr == 24:
            slider2.config(label="Lower Bound f0", from_=0, to=22050)
            slider2.set(630)
            slider2.grid()
            slider3.config(label="Higher Bound f1", from_=0, to=22050)
            slider3.set(1720)
            slider3.grid()
            calculate_band_energy_and_plot(slider.get(), fig, canvas, slider2.get(), slider3.get(), v)
        elif function_nr == 25:
            calculate_ersb_and_plot(slider.get(), fig, canvas, v)
        elif function_nr == 26:
            calculate_spectral_flatness_and_plot(slider.get(), fig, canvas, v)
        elif function_nr == 27:
            calculate_spectral_crest_factor_and_plot(slider.get(), fig, canvas, v)
    #
    # #
    else:
        if len(audio_data) > 80000:
            max_scroll = (len(audio_data) - 80000) // slider.get()
            scrollbar2.grid()
            scrollbar2.config(to=max_scroll)
        else:
            scrollbar2.grid_remove()
        if function_nr == 12:
            slider.grid()
            slider2.set(5)
            scrollbar2.grid()
            slider2.config(to=100, label="volume level")
            slider2.grid()
            slider3.set(3)
            slider3.config(label="ZCR level")
            slider3.grid()
            silence_detection(slider.get(), fig, canvas, slider2.get(), slider3.get())
        elif function_nr == 13:
            slider.grid()
            slider2.set(5)
            slider2.config(to=100, label="volume level")
            slider2.grid()
            sound_detection(slider.get(), fig, canvas, slider2)
        elif function_nr == 14:
            scrollbar2.grid()
            if len(audio_data) > 176400:
                max_scroll = 10 * (len(audio_data) - 176400) // slider.get()
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
                max_scroll = (len(audio_data) - 20000) // 200
                scrollbar.configure(to=max_scroll)
                scrollbar2.configure(to=max_scroll)
            else:
                scrollbar.grid_remove()
                scrollbar2.grid_remove()

            plot_audio_waveform(sample_rate, audio_data, fig, canvas)

        except Exception as e:
            print(f"Wystąpił błąd: {e}")
            return None, None


def play_audio():
    global sample_rate, audio_data

    if audio_data is None or sample_rate is None:
        print("Brak danych audio do odtworzenia.")
        return
    try:
        sd.play(audio_data, samplerate=sample_rate)
        sd.wait()
    except Exception as e:
        print(f"Wystąpił błąd podczas odtwarzania dźwięku: {e}")


def calculate_volume_and_plot(frame_size, fig, canvas, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 2

    print("vol", type(fig))
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]
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
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(time, visible_audio, label='Przebieg czasowy (audio)', color='blue', alpha=0.6, linewidth=0.5)
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

    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
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
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
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
    max_val = max(abs(x) for x in audio_data)
    audio_data_sk = [x / max_val for x in audio_data]
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data_sk[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]
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
    fig.clear()
    ax = fig.add_subplot(111)
    ax.fill_between(silent_time, silent, color='grey', alpha=0.2)
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
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
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


def min_max_scaling(data, new_min=0, new_max=1):
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
    cut_off = slider2.get()
    max_val = max(abs(x) for x in audio_data)
    audio_data_sk = [x / max_val for x in audio_data]
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data_sk[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]
    visible_num_frames = len(visible_audio) // frame_size
    f0 = []
    f0_time = []
    silent = []
    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = audio_data[frame_start:frame_end]
        frame = [float(x) for x in frame]
        autocorr = [sum(frame[i] * frame[i + lag] for i in range(len(frame) - lag)) for lag in range(len(frame))]
        if len(autocorr) <= 1:
            break
        lag = autocorr.index(max(autocorr[1:]))
        f0_val = sample_rate / lag if lag != 0 else 0
        f0.append(f0_val)
        f0_time.append(frame_start / sample_rate)
        if f0_val < cut_off:
            silent.append(1)
        else:
            silent.append(0)
    scaled_audio = min_max_scaling(np.array(visible_audio), 0, 1)
    scaled_f0 = min_max_scaling(np.array(f0), 0, 1)
    if max(f0) - min(f0) != 0:
        scaled_cut_off = max(0, (cut_off - min(f0)) / (max(f0) - min(f0)))
    else:
        scaled_cut_off = max(0, cut_off)
    slider2.config(to=max(f0), label="Poziom bezdźwięczności")
    slider2.grid()
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(time, scaled_audio, label='Przeskalowane nagranie audio', color='blue', alpha=0.4, linewidth=0.5)
    ax.plot(f0_time, scaled_f0, label='Przeskalowane F0', color='red', linewidth=2)
    ax.axhline(y=scaled_cut_off, color='blue', linestyle='--', label=f'Cut Off ({cut_off} Hz)')
    ax.set_title("Częstotliwość tonu podstawowego F0 - Autokorelacja")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Wartości skalowane")
    ax.grid(True)
    ax.set_ylim(0, 1.1)
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def calculate_f0_autocorrelation(frame_size, fig, canvas, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 6
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
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
        f0_val = sample_rate / lag if lag != 0 else 0
        f0.append(f0_val)
        f0_time.append(frame_start / sample_rate)
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(f0_time, f0, label='(Fundamental Frequency', color='red', linewidth=2)
    ax.set_title("Częstotliwość tonu podstawowego F0 - autokorelacja")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("F0")
    ax.grid(True)
    ax.set_ylim(min(min(f0) * 0.9, 0), max(max(f0) * 1.1, 23000))
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def calculate_f0_AMDF(frame_size, fig, canvas, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 7

    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
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
            if amdf[lag - 1] < amdf[lag] and amdf[lag + 1] < amdf[lag]:
                max_lag = lag
                break
        max_lag = min(frame_size // 2, len(frame) // 2, max_lag)
        search_range = range(max_lag, len(amdf))
        min_lag = min(search_range, key=lambda lag: amdf[lag])
        f0_val = sample_rate / min_lag if min_lag != 0 else 0
        f0.append(f0_val)
        f0_time.append(frame_start / sample_rate)
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(f0_time, f0, label='(Fundamental Frequency', color='red', linewidth=2)
    ax.set_title("Częstotliwość tonu podstawowego F0 - AMDF")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("F0")
    ax.grid(True)
    ax.set_ylim(min(min(f0) * 0.95, 40), max(max(f0) * 1.05, 105))
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def format_value(value):
    return "{:.2f}".format(value)


def calculate_VSTD(frame_size, label):
    global func_nr
    func_nr = 8
    max_val = max(abs(x) for x in audio_data)
    audio_data_sk = [x / max_val for x in audio_data]
    num_frames = len(audio_data_sk) // frame_size
    vol = []
    sum_vol = 0
    peaks_all = []
    valleys_all = []
    vstd = []
    vdr = []
    vu_all = []

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
    std_vol = math.sqrt(sum((vol_value - mean_vol) ** 2 for vol_value in vol) / len(vol))
    VSTD_full = std_vol / max_vol if max_vol > 0 else 0
    VDR_full = (max_vol - min_vol) / max_vol if max_vol > 0 else 0

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

        window_mean_vol = sum(window_vol) / len(window_vol)
        window_std_vol = math.sqrt(sum((x - window_mean_vol) ** 2 for x in window_vol) / len(window_vol))
        VSTD_window = window_std_vol / max(window_vol) if max(window_vol) > 0 else 0
        vstd.append(VSTD_window)

        window_max_vol = max(window_vol)
        window_min_vol = min(window_vol)
        VDR_window = (window_max_vol - window_min_vol) / window_max_vol if window_max_vol > 0 else 0
        vdr.append(VDR_window)
        vu = 0
        for p, v in zip(peaks, valleys):
            vu += abs(p - v)
        vu_all.append(vu)

    vu_total = 0
    for peaks, valleys in zip(peaks_all, valleys_all):
        for p, v in zip(peaks, valleys):
            vu_total += abs(p - v)
    VU_full = vu_total

    VSTD_full_str = format_value(VSTD_full)
    VDR_full_str = format_value(VDR_full)
    vstd_str = [format_value(val) for val in vstd]
    vdr_str = [format_value(val) for val in vdr]
    VU_full_str = format_value(VU_full)
    vu_str = [format_value(val) for val in vu_all]
    label.config(text="VSTD_full = " + VSTD_full_str +
                      "\nVDR_full = " + VDR_full_str +
                      "\nvstd (dla każdego okna 1s) = " + ", ".join(vstd_str) +
                      "\nvdr (dla każdego okna 1s) = " + ", ".join(vdr_str) +
                      "\nVU_full = " + VU_full_str +
                      "\nvu (dla każdego okna 1s) = " + ", ".join(vu_str))

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
        low_energy_frames = (sum(signum(0.5 * av_ste - window_ste[x]) + 1 for x in range(len(window_ste)))) / (
                2 * len(window_ste))

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


def mean(values):
    return sum(values) / len(values) if values else 0


def std(values, avg):
    return (sum((x - avg) ** 2 for x in values) / len(values)) ** 0.5 if values else 0


def calculate_klip_ZCR(frame_size, label):
    global func_nr
    func_nr = 10

    # Obliczenie liczby ramek w oknie 1s
    frames_per_window = sample_rate // frame_size
    num_frames = len(audio_data) // frame_size
    zcr_values = []
    for i in range(num_frames):
        frame_start = i * frame_size
        frame_end = min(frame_start + frame_size, len(audio_data))
        frame = audio_data[frame_start:frame_end]
        zcr_val = (sum(abs(signum(frame[x]) - signum(frame[x + 1])) for x in range(len(frame) - 1))) / (2 * len(frame))
        zcr_values.append(zcr_val)

    zcr_std_per_window = []
    hzcrr_per_window = []

    for start in range(0, len(zcr_values), frames_per_window):
        window_zcr_values = zcr_values[start:start + frames_per_window]
        if len(window_zcr_values) > 0:
            avg_zcr = mean(window_zcr_values)
            zcr_std = std(window_zcr_values, avg_zcr)
            zcr_std_per_window.append(zcr_std)

            hzcrr = 0
            for zcr in window_zcr_values:
                hzcrr += (signum(zcr - 1.5 * avg_zcr) + 1) / 2
            hzcrr_per_window.append(hzcrr / len(window_zcr_values))

    zcr_std_full = mean(zcr_std_per_window) if zcr_std_per_window else 0
    hzcrr_full = mean(hzcrr_per_window) if hzcrr_per_window else 0

    zcr_std_full_str = format_value(zcr_std_full)
    hzcrr_full_str = format_value(hzcrr_full)

    zcr_std_per_window_str = [format_value(val) for val in zcr_std_per_window]
    hzcrr_per_window_str = [format_value(val) for val in hzcrr_per_window]

    label.config(text="ZSTD = " + zcr_std_full_str +
                      "\nZSTD (dla każdego okna 1s) = " + ", ".join(zcr_std_per_window_str) +
                      "\nHZCRR = " + hzcrr_full_str +
                      "\nHZCRR (dla każdego okna 1s) = " + ", ".join(hzcrr_per_window_str))

    label.grid()


def calculate_lster(window, frame_size):
    num_frames = len(window) // frame_size
    ste = []
    for i in range(num_frames):
        frame_start = i * frame_size
        frame_end = min(frame_start + frame_size, len(window))
        frame = window[frame_start:frame_end]
        spectrum = [abs(x) ** 2 for x in frame]
        ste.extend(spectrum)
    if len(ste) == 0:
        return 0
    elif len(ste) == 1:
        av_ste = ste[0]
    else:
        av_ste = sum(ste) / len(ste)
    LSTER = (sum(signum(0.5 * av_ste - ste[x]) + 1 for x in range(len(ste)))) / (
            2 * len(ste))

    return LSTER


def calculate_zstd(window, frame_size):
    num_frames = len(window) // frame_size
    zcr = []

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
    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data_sk[start_idx:end_idx]
    time = [i / sample_rate for i in range(start_idx, end_idx)]
    visible_num_windows = len(visible_audio) // window_size

    lster_values = []
    zstd_values = []

    for i in range(visible_num_windows):
        window_start = start_idx + i * window_size
        window_end = min(window_start + window_size, end_idx)
        lster_time.append(window_start / sample_rate)

        window = audio_data[window_start:window_end]
        window = [float(x) for x in window]

        lster_val = calculate_lster(window, frame_size)
        lster_values.append(lster_val)

        zstd_val = calculate_zstd(window, frame_size)
        zstd_values.append(zstd_val)

    if len(visible_audio) % window_size != 0:
        window_start = start_idx + visible_num_windows * window_size
        window_end = min(window_start + window_size, end_idx)
        lster_time.append(window_start / sample_rate)

        window = audio_data[window_start:window_end]
        window = [float(x) for x in window]

        lster_val = calculate_lster(window, frame_size)
        lster_values.append(lster_val)

        zstd_val = calculate_zstd(window, frame_size)
        zstd_values.append(zstd_val)

    scaled_audio = min_max_scaling(visible_audio, 0, 1)
    fig.clear()
    ax = fig.add_subplot(111)

    ax.plot(time, scaled_audio, label='Przeskalowane nagranie audio', color='blue', alpha=0.4, linewidth=0.5)

    ax.plot(lster_time, lster_values, label='Przeskalowane LSTER', color='green', linewidth=2)

    ax.plot(lster_time, zstd_values, label='Przeskalowane ZSTD', color='red', linewidth=2)

    ax.set_title("LSTER i ZSTD dla każdego okna")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Wartości skalowane")
    ax.grid(True)
    ax.set_ylim(0, 1.1)
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def button_function(fig, canvas, slider, scroll, scroll2, slider2, slider3,
                    labelVSTD, canvas_widget2, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5, v, fig1, canvas1, canvas_widget):
    if func_nr == 20:
        print("slid, slid val:  ", slider2.get())
        print("slid freq", type(fig))
        max_scroll = (len(audio_data) - slider2.get()) // slider.get()
        print("max_scroll   ,    slider2:   ", max_scroll, slider2.get())
        scroll2.configure(to=max_scroll)
        calc_show_freq(fig, canvas, v, 0, slider2.get())
    elif func_nr == 21:
        calculate_volume_freq_and_plot(slider.get(), fig, canvas, v)
    elif func_nr == 22:
        calculate_frequency_centroid_and_plot(slider.get(), fig, canvas, v)
    elif func_nr == 23:
        calculate_effective_bandwidth_and_plot(slider.get(), fig, canvas, v)
    elif func_nr == 24:
        calculate_band_energy_and_plot(slider.get(), fig, canvas, slider2.get(), slider3.get(), v)
    elif func_nr == 25:
        calculate_ersb_and_plot(slider.get(), fig, canvas, v)
    elif func_nr == 26:
        calculate_spectral_flatness_and_plot(slider.get(), fig, canvas, v)
    elif func_nr == 27:
        calculate_spectral_crest_factor_and_plot(slider.get(), fig, canvas, v)
    elif func_nr == 19:
        plot_window_effect(fig1, canvas1, fig, canvas, slider.get(), scroll, scroll2, slider2, canvas_widget, rbtn1,
                           rbtn2, rbtn3, rbtn4, rbtn5, v)


def slider_function(slider, fig, canvas, slider2, slider3, label, scroll2, scroll, fig1, canvas1, canvas_widget, rbtn1,
                    rbtn2, rbtn3, rbtn4, rbtn5, v=1):
    if func_nr == 2:
        calculate_volume_and_plot(slider.get(), fig, canvas)
    elif func_nr == 3:
        calculate_STE_and_plot(slider.get(), fig, canvas)
    elif func_nr == 4:
        calculate_ZCR_and_plot(slider.get(), fig, canvas)
    elif func_nr == 5:
        SilentRatio(slider.get(), fig, canvas, slider2.get(), slider3.get())
    elif func_nr == 6:
        calculate_f0_autocorrelation(slider.get(), fig, canvas)
    elif func_nr == 7:
        calculate_f0_AMDF(slider.get(), fig, canvas)
    elif func_nr == 8:
        calculate_VSTD(slider.get(), label)
    elif func_nr == 9:
        slider2.configure(to=slider.get() // 2, from_=1, label="segment size")
        calculate_LSTER(slider.get(), label, slider2.get())
    elif func_nr == 10:
        calculate_klip_ZCR(slider.get(), label)
    elif func_nr == 12:
        silence_detection(slider.get(), fig, canvas, slider2.get(), slider3.get())
    elif func_nr == 13:
        sound_detection(slider.get(), fig, canvas, slider2)
    elif func_nr == 14:
        differentiate(slider.get(), fig, canvas)
    elif func_nr == 20:
        print("slid, slid val:  ", slider2.get())
        print("slid freq", type(fig))
        max_scroll = (len(audio_data) - slider2.get()) // slider.get()
        print("max_scroll   ,    slider2:   ", max_scroll, slider2.get())
        scroll2.configure(to=max_scroll)
        calc_show_freq(fig, canvas, v, 0, slider2.get())
    elif func_nr == 21:
        calculate_volume_freq_and_plot(slider.get(), fig, canvas, v)
    elif func_nr == 22:
        calculate_frequency_centroid_and_plot(slider.get(), fig, canvas, v)
    elif func_nr == 23:
        calculate_effective_bandwidth_and_plot(slider.get(), fig, canvas, v)
    elif func_nr == 24:
        print("slid   f0", slider2.get(), "f1", slider3.get())
        calculate_band_energy_and_plot(frame_size=slider.get(),fig= fig, canvas=canvas, f_low=slider2.get(), f_high=slider3.get(), v=v)
    elif func_nr == 25:
        calculate_ersb_and_plot(slider.get(), fig, canvas, v)
    elif func_nr == 26:
        calculate_spectral_flatness_and_plot(slider.get(), fig, canvas, v)
    elif func_nr == 27:
        calculate_spectral_crest_factor_and_plot(slider.get(), fig, canvas, v)
    elif func_nr == 19:
        plot_window_effect(fig1, canvas1, fig, canvas, slider.get(), scroll, scroll2, slider2, canvas_widget, rbtn1,
                           rbtn2, rbtn3, rbtn4, rbtn5, v)


def scroll_function1(fig, canvas, position, slider, scrollbar, scrollbar2):
    if audio_data is not None:
        max_points = 20000
        if len(audio_data) <= max_points:
            start_idx = 0
        else:
            start_idx = position * slider.get()
            max_scroll = (len(audio_data) - 20000) // slider.get()
            scrollbar.configure(to=max_scroll)
            scrollbar2.configure(to=max_scroll)
        plot_audio_waveform(sample_rate, audio_data, fig, canvas, start_idx=start_idx)


def scroll_function(fig, canvas, position, slider, slider2, slider3, scrollbar, scrollbar2, fig1, canvas1, fig2,
                    canvas2, canvas_widget, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5, v):
    if audio_data is not None:
        max_points = 20000
        if len(audio_data) <= max_points:
            start_idx = 0
        else:
            if func_nr != 20 and func_nr != 19:
                start_idx = position * slider.get()
                max_scroll = (len(audio_data) - 20000) // slider.get()
                scrollbar.configure(to=max_scroll)
                scrollbar2.configure(to=max_scroll)
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
            elif func_nr > 11 and func_nr < 19:
                max_scroll = (len(audio_data) - 80000) // slider.get()
                scrollbar2.configure(to=max_scroll)
                if func_nr == 12:
                    silence_detection(slider.get(), fig, canvas, slider2.get(), slider3.get(), start_idx=start_idx)
                elif func_nr == 13:
                    sound_detection(slider.get(), fig, canvas, slider2, start_idx=start_idx)
                elif func_nr == 14:
                    max_scroll = 10 * (len(audio_data) - 176400) // slider.get()
                    scrollbar2.configure(to=max_scroll)
                    differentiate(slider.get(), fig, canvas, start_idx=start_idx)

            elif func_nr == 20:

                calc_show_freq(fig, canvas, start_idx, slider2.get(), v)

            elif func_nr == 19:
                print("scroll: ", scrollbar2.get())
                plot_window_effect(fig1, canvas1, fig2, canvas2, slider.get(), scrollbar, scrollbar2, slider2,
                                   canvas_widget, rbtn1, rbtn2, rbtn3, rbtn4, rbtn5, v)
            elif func_nr == 21:
                calculate_volume_freq_and_plot(slider.get(), fig, canvas, v, start_idx)
            elif func_nr == 22:
                calculate_frequency_centroid_and_plot(slider.get(), fig, canvas, v, start_idx)
            elif func_nr == 23:
                calculate_effective_bandwidth_and_plot(slider.get(), fig, canvas, v, start_idx)
            elif func_nr == 24:
                calculate_band_energy_and_plot(slider.get(), fig, canvas, slider2.get(), slider3.get(), v, start_idx)
            elif func_nr == 25:
                calculate_ersb_and_plot(slider.get(), fig, canvas, v, start_idx)
            elif func_nr == 26:
                calculate_spectral_flatness_and_plot(slider.get(), fig, canvas, v, start_idx)
            elif func_nr == 27:
                calculate_spectral_crest_factor_and_plot(slider.get(), fig, canvas, v, start_idx)


def calc_show_freq(fig, canvas, v, start_idx=0, max_points=20000):
    global func_nr
    print("freq", type(fig))
    func_nr = 20
    print("freq, długoź audio  ", len(audio_data))
    end_idx = min(start_idx + max_points, len(audio_data))
    print("starr", start_idx, "end ", end_idx, "diff: ", end_idx - start_idx)
    visible_audio = np.array(audio_data[start_idx:end_idx])

    if len(visible_audio) == 0:
        print("0")
        return
    # FFT i częstotliwości
    windowed_audio = apply_window(size=len(visible_audio), window_type=v, signal=visible_audio)

    freq_domain = np.fft.fft(visible_audio)
    freq = np.fft.fftfreq(len(visible_audio), 1 / sample_rate)
    magnitude = np.abs(freq_domain)

    # Wykres FFT
    fig.clear()
    ax = fig.add_subplot(111)
    half = len(freq) // 2
    ax.plot(freq[:half], magnitude[:half], color='green')
    ax.set_title("Widmo częstotliwości (FFT)")
    ax.set_xlabel("Częstotliwość [Hz]")
    ax.set_ylabel("Amplituda")
    ax.grid(True)

    num_peaks = 5
    peak_indices = np.argsort(magnitude[:half])[-num_peaks:]  # tylko pierwsza połowa FFT

    for idx in peak_indices:
        f = freq[idx]
        m = magnitude[idx]
        ax.text(f, m, f"{f:.0f} Hz", fontsize=8, color='black', ha='center', va='bottom')
    fig.tight_layout()
    canvas.draw()


def calculate_volume_freq_and_plot(frame_size, fig, canvas, v, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 21  # albo inny numer, który przypiszesz tej funkcji w swoim systemie

    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    visible_num_frames = len(visible_audio) // frame_size

    volume = []
    volume_time = []

    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = np.array(audio_data[frame_start:frame_end])

        if len(frame) < frame_size:
            continue  # pomiń niepełne ramki

        # okno Hanninga
        windowed = apply_window(size=len(frame), window_type=v, signal=frame)

        # windowed = frame * np.hanning(len(frame))

        # FFT i moc widma
        spectrum = np.fft.fft(windowed)
        magnitude_squared = np.abs(spectrum) ** 2
        avg_energy = np.sum(magnitude_squared) / frame_size

        volume.append(avg_energy)
        volume_time.append(frame_start / sample_rate)
    # Rysowanie
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(volume_time, volume, label='Głośność (FFT)', color='orange', linewidth=2)
    ax.set_title("głośność (FFT) dla dziedziny częstotliwości")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Głośność")
    ax.grid(True)
    ax.set_ylim(min(volume) * 0.9, max(volume) * 1.1)
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def calculate_frequency_centroid_and_plot(frame_size, fig, canvas, v, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 22  # dowolny numer funkcji w twoim systemie

    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    visible_num_frames = len(visible_audio) // frame_size

    fc = []
    fc_time = []

    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = np.array(audio_data[frame_start:frame_end])

        if len(frame) < frame_size:
            continue

        windowed = apply_window(len(frame), v, frame)

        # windowed = frame * np.hanning(len(frame))
        spectrum = np.fft.fft(windowed)
        magnitude = np.abs(spectrum[:len(spectrum) // 2])
        freqs = np.fft.fftfreq(len(spectrum), d=1 / sample_rate)[:len(spectrum) // 2]

        if np.sum(magnitude) == 0:
            centroid = 0
        else:
            centroid = np.sum(freqs * magnitude) / np.sum(magnitude)

        fc.append(centroid)
        fc_time.append(frame_start / sample_rate)
    # Rysowanie
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(fc_time, fc, label='Frequency Centroid (FC)', color='purple', linewidth=2)
    ax.set_title("Frequency Centroid (jasność widma)")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("FC [Hz]")
    ax.grid(True)
    ax.set_ylim(min(fc) * 0.9, max(fc) * 1.1)
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def calculate_effective_bandwidth_and_plot(frame_size, fig, canvas, v, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 23  # lub inny numer przypisany tej funkcji

    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    visible_num_frames = len(visible_audio) // frame_size

    bw = []
    bw_time = []

    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = np.array(audio_data[frame_start:frame_end])

        if len(frame) < frame_size:
            continue

        # Okno Hanninga
        # windowed = frame * np.hanning(len(frame))
        windowed = apply_window(len(frame), v, frame)

        spectrum = np.fft.fft(windowed)
        magnitude = np.abs(spectrum[:len(spectrum) // 2])
        freqs = np.fft.fftfreq(len(spectrum), d=1 / sample_rate)[:len(spectrum) // 2]

        if np.sum(magnitude) == 0:
            centroid = 0
            bandwidth = 0
        else:
            # Centroid
            centroid = np.sum(freqs * magnitude) / np.sum(magnitude)

            # Effective Bandwidth
            variance = np.sum(((freqs - centroid) ** 2) * magnitude) / np.sum(magnitude)
            bandwidth = np.sqrt(variance)

        bw.append(bandwidth)
        bw_time.append(frame_start / sample_rate)

    # Rysowanie
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(bw_time, bw, label='Effective Bandwidth (BW)', color='darkorange', linewidth=2)
    ax.set_title("Effective Bandwidth (szerokość pasma)")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("BW [Hz]")
    ax.grid(True)
    ax.set_ylim(min(bw) * 0.9, max(bw) * 1.1)
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def calculate_band_energy_and_plot(frame_size, fig, canvas, f_low, f_high, v, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 24  # Dowolny unikalny numer

    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    visible_num_frames = len(visible_audio) // frame_size

    be = []
    be_time = []

    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = np.array(audio_data[frame_start:frame_end])

        if len(frame) < frame_size:
            continue

        # Okno Hanninga (rekomendowane)
        windowed = apply_window(len(frame), v, frame)

        # windowed = frame * np.hanning(len(frame))
        spectrum = np.fft.fft(windowed)
        magnitude = np.abs(spectrum[:len(spectrum) // 2])  # tylko dodatnie cz. FFT
        power_spectrum = magnitude ** 2

        freqs = np.fft.fftfreq(len(spectrum), d=1 / sample_rate)[:len(spectrum) // 2]
        print("plot   f0", f_low, "f1", f_high)
        # Indeksy pasma [f_low, f_high]
        band_mask = (freqs >= f_low) & (freqs <= f_high)

        band_energy = np.sum(power_spectrum[band_mask]) / frame_size
        be.append(band_energy)
        be_time.append(frame_start / sample_rate)

    # Rysowanie
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(be_time, be, label=f'Band Energy {f_low}-{f_high} Hz', color='darkgreen', linewidth=2)
    ax.set_title(f"Przebieg czasowy i Band Energy [{f_low}-{f_high} Hz]")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Amplituda / Energia")
    ax.grid(True)
    ax.set_ylim(min(be) * 0.9, max(be) * 1.1)
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def calculate_ersb_and_plot(frame_size, fig, canvas, v, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 25  # dowolny, unikalny numer funkcji

    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    visible_num_frames = len(visible_audio) // frame_size

    ersb1_list, ersb2_list, ersb3_list, time_list = [], [], [], []
    if sample_rate > 2 * 4400:
        ersb4_list = []
    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = np.array(audio_data[frame_start:frame_end])

        if len(frame) < frame_size:
            continue

        # Okno Hanninga dla lepszego FFT
        windowed = apply_window(len(frame), v, frame)

        # windowed = frame * np.hanning(len(frame))
        spectrum = np.fft.fft(windowed)
        magnitude = np.abs(spectrum[:len(spectrum) // 2])
        power_spectrum = magnitude ** 2
        freqs = np.fft.fftfreq(len(spectrum), d=1 / sample_rate)[:len(spectrum) // 2]

        total_energy = np.sum(power_spectrum)
        if total_energy == 0:
            ersb1, ersb2, ersb3 = 0, 0, 0
            if sample_rate > 2 * 4400:
                ersb4 = 0
        else:
            # Maska subbandów
            mask1 = (freqs >= 0) & (freqs < 630)
            mask2 = (freqs >= 630) & (freqs < 1720)
            mask3 = (freqs >= 1720) & (freqs < 4400)

            ersb1 = np.sum(power_spectrum[mask1]) / total_energy
            ersb2 = np.sum(power_spectrum[mask2]) / total_energy
            ersb3 = np.sum(power_spectrum[mask3]) / total_energy

            if sample_rate > 2 * 4400:
                mask4 = (freqs >= 4400) & (freqs <= 0.5 * sample_rate)  # nieużywane
                ersb4 = np.sum(power_spectrum[mask4]) / total_energy

        ersb1_list.append(ersb1)
        ersb2_list.append(ersb2)
        ersb3_list.append(ersb3)
        if sample_rate > 2 * 4400:
            ersb4_list.append(ersb4)
        time_list.append(frame_start / sample_rate)

    # Rysowanie
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(time_list, ersb1_list, label="ERSB1 (0–630 Hz)", color='blue')
    ax.plot(time_list, ersb2_list, label="ERSB2 (630–1720 Hz)", color='orange')
    ax.plot(time_list, ersb3_list, label="ERSB3 (1720–4400 Hz)", color='green')
    if sample_rate > 2 * 4400:
        ax.plot(time_list, ersb4_list, label=f"ERSB4 (4400–{0.5 * sample_rate} Hz)", color='pink')
    ax.set_title("Energy Ratio Subbands (ERSB)")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Stosunek energii")
    ax.set_ylim(0, 1)
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def calculate_spectral_flatness_and_plot(frame_size, fig, canvas, v, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 26  # dowolny numer do identyfikacji

    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    visible_num_frames = len(visible_audio) // frame_size
    sfm_list = []
    time_list = []

    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = audio_data[frame_start:frame_end]

        if len(frame) == 0:
            continue

        # Okno Hanninga
        windowed = apply_window(len(frame), v, frame)

        # windowed = frame * np.hanning(len(frame))

        # FFT i widmo mocy
        spectrum = np.abs(np.fft.fft(windowed))[:len(frame) // 2]
        power_spectrum = spectrum ** 2 + 1e-6  # zabezpieczenie przed zerem

        # Obliczenia SFM
        geo_mean = np.exp(np.mean(np.log(power_spectrum)))
        arith_mean = np.mean(power_spectrum)

        sfm = geo_mean / arith_mean if arith_mean > 0 else 1.0
        sfm_list.append(sfm)
        time_list.append(frame_start / sample_rate)

    # Rysowanie wykresu
    # print(sfm_list)
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(time_list, sfm_list, label="Spectral Flatness (SFM)", color="purple")
    ax.set_title("Miara płaskości widma (Spectral Flatness)")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("SFM (0 = tonalne, 1 = szumowe)")
    ax.set_ylim(0, 1.05)
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def calculate_spectral_crest_factor_and_plot(frame_size, fig, canvas, v, start_idx=0, max_points=20000):
    global func_nr
    func_nr = 27  # dowolny unikalny numer funkcji

    end_idx = min(start_idx + max_points, len(audio_data))
    visible_audio = audio_data[start_idx:end_idx]
    visible_num_frames = len(visible_audio) // frame_size
    scf_list = []
    scf_time = []

    for i in range(visible_num_frames):
        frame_start = start_idx + i * frame_size
        frame_end = min(frame_start + frame_size, end_idx)
        frame = np.array(audio_data[frame_start:frame_end])

        if len(frame) < frame_size:
            continue

        # Okno Hann'a dla lepszego widma
        # window = np.hanning(len(frame))
        # frame = frame * window
        frame = apply_window(len(frame), v, frame)

        # FFT i moc widma
        spectrum = np.fft.fft(frame)[:len(frame) // 2]
        power_spectrum = np.abs(spectrum) ** 2 + 1e-10

        # Spectral Crest Factor: max(PSD) / mean(PSD)
        crest = np.max(power_spectrum) / np.mean(power_spectrum)
        scf_list.append(crest)
        scf_time.append(frame_start / sample_rate)

    # Wykres
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(scf_time, scf_list, label='Spectral Crest Factor (SCF)', color='orange', linewidth=2)
    ax.set_title("Spectral Crest Factor (SCF) w czasie")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("SCF")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    canvas.draw()


def plot_window_effect(fig1, canvas1, fig2, canvas2, frame_size, scrollbar, scrollbar2, slider2, canvas_widget, rbtn1,
                       rbtn2, rbtn3, rbtn4, rbtn5, v):
    global func_nr

    rbtn1.grid()
    rbtn2.grid()
    rbtn3.grid()
    rbtn5.grid()
    rbtn4.grid()
    func_nr = 19  # dowolny unikalny numer funkcji
    canvas_widget.grid()
    max_scroll = (len(audio_data) - slider2.get()) // frame_size
    scrollbar2.configure(to=max_scroll)
    # scrollbar2.config(from_=0, to = max(audio_data))
    scrollbar2.grid()
    slider2.config(from_=1, to=len(audio_data), label="wielkość próbki do fft")

    slider2.grid()
    size = slider2.get()

    scrollbar.grid_remove()
    # scrollbar2.grid_remove()

    start_idx = scrollbar2.get() * frame_size
    end_idx = min(start_idx + size, len(audio_data))
    signal_segment = np.array(audio_data[start_idx:end_idx])

    # Wyrównanie długości do 'size' (na końcu sygnału)
    if len(signal_segment) < size:
        signal_segment = np.pad(signal_segment, (0, size - len(signal_segment)), mode='constant')

    # Zastosowanie okna Hanninga na całym fragmencie
    windowed_signal = apply_window(size, v, signal_segment)

    # window = np.hanning(size)
    # windowed_signal = signal_segment * window

    # Oś czasu
    time_axis = np.arange(size) / sample_rate

    # FFT po okienkowaniu
    fft_result = np.fft.fft(windowed_signal)
    freq_axis = np.fft.fftfreq(size, d=1 / sample_rate)
    half_len = size // 2
    magnitude = np.abs(fft_result[:half_len])
    freq_axis = freq_axis[:half_len]

    # === WYKRES CZASOWY (fig1, canvas1) ===
    fig1.clear()
    ax1 = fig1.add_subplot(111)
    ax1.plot(time_axis, signal_segment, label="Oryginalny sygnał", alpha=0.5)
    ax1.plot(time_axis, windowed_signal, label="Po zastosowaniu okna", color='red')
    ax1.set_title("Czas: przed i po zastosowaniu okna")
    ax1.set_xlabel("Czas [s]")
    ax1.set_ylabel("Amplituda")
    ax1.grid(True)
    ax1.legend()
    fig1.tight_layout()
    canvas1.draw()

    # === WYKRES CZĘSTOTLIWOŚCIOWY (fig2, canvas2) ===
    fig2.clear()
    ax2 = fig2.add_subplot(111)
    ax2.plot(freq_axis, magnitude, color='green')
    ax2.set_title("Widmo częstotliwości po zastosowaniu okna (FFT)")
    ax2.set_xlabel("Częstotliwość [Hz]")
    ax2.set_ylabel("Amplituda")
    ax2.grid(True)
    num_peaks = 5
    half = len(magnitude) // 2
    peak_indices = np.argsort(magnitude[:half])[-num_peaks:]
    peak_indices = sorted(peak_indices)  # sortujemy po częstotliwości

    for idx in peak_indices:
        f = freq_axis[idx]
        m = magnitude[idx]
        ax2.text(f, m, f"{f:.0f} Hz", fontsize=8, color='black', ha='center', va='bottom')
    fig2.tight_layout()
    canvas2.draw()


def apply_window(size, window_type, signal):
    print(window_type)
    """
    Zastosuj wybrane okno do sygnału.

    Parameters:
        size (int): długość okna
        window_type (int): numer typu okna (1–5)
        signal (np.ndarray): sygnał wejściowy

    Returns:
        windowed_signal (np.ndarray): sygnał po przemnożeniu przez okno
    """

    if len(signal) < size:
        # Uzupełniamy zerami jeśli sygnał krótszy niż okno
        signal = np.pad(signal, (0, size - len(signal)), mode='constant')
    else:
        signal = signal[:size]  # Przycinamy jeśli sygnał dłuższy

    # Wybór odpowiedniego okna
    if window_type == 1:
        window = np.ones(size)  # okno prostokątne
    elif window_type == 2:
        window = 1 - np.abs((np.arange(size) - (size - 1) / 2) / ((size + 1) / 2))  # trójkątne
    elif window_type == 3:
        window = np.hamming(size)
    elif window_type == 4:
        window = np.hanning(size)  # van Hann (czyli Hanning)
    elif window_type == 5:
        window = np.blackman(size)
    else:
        raise ValueError("Niepoprawny typ okna. Wybierz liczbę od 1 do 5.")

    windowed_signal = signal * window
    return windowed_signal
