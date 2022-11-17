import os
import base64

import librosa
import numpy as np
import pandas as pd
import panel as pn
import soundfile as sf

from scipy.io import wavfile
from scipy.fft import rfftfreq, rfft, irfft


from panel.interact import interact

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Slider, Button, Select, CustomJS, Div
from bokeh.models.formatters import PrintfTickFormatter
from bokeh.layouts import column, row, Spacer


file_input = pn.widgets.FileInput(
    accept=".txt,.csv,.wav", width=200, margin=(70, 0, 10, 10))


modes = pn.widgets.Select(name='modes', options=[
                          'default', 'music', 'vocals'], width=400)


info_msg = pn.pane.Alert("""<h1 style="font-size: 50px; color: #242020;">Upload a file and start mixing <br> <span style="font-size: 30px; color: grey;">&lpar;only *.csv and *.wav files&rpar;</span></h1>""",
                         alert_type="dark", width=800, height=400, margin=(0, 50, 0, 130))


input_source = ColumnDataSource(pd.DataFrame())
output_source = ColumnDataSource(pd.DataFrame())

hover_tools = [
    ("(time,amp)", "($x, $y)")
]

input_graph = figure(height=280, width=800,
                     tools="crosshair,pan,reset,save,wheel_zoom", title="Input Graph", tooltips=hover_tools)

input_graph.line(x="time", y="amp", source=input_source,
                 line_width=3, line_alpha=0.6)

input_graph.visible = False


output_graph = figure(height=280, width=800,
                      tools="crosshair,pan,reset,save,wheel_zoom", title="Output Graph", tooltips=hover_tools, x_range=input_graph.x_range, y_range=input_graph.y_range)

output_graph.line(x="time", y="amp", source=output_source,
                  line_width=3, line_alpha=0.6, color="firebrick")

output_graph.visible = False

default_sliders_values = [0] * 10
music_sliders_values = [0] * 10
vocals_sliders_values = [0] * 10

# slider1 = Slider(title="20Hz - 40Hz", value=0.0,
#                  start=-20.0, end=20.0, step=0.1, format="@[.] {dB}")


slider1 = pn.widgets.FloatSlider(name="20Hz - 40Hz", value=0.0,
                                 start=-20.0, end=20.0, step=0.1, format=PrintfTickFormatter(format='%.2f dB'))
slider2 = pn.widgets.FloatSlider(name="40Hz - 80Hz", value=0.0,
                                 start=-20.0, end=20.0, step=0.1, format=PrintfTickFormatter(format='%.2f dB'))
slider3 = pn.widgets.FloatSlider(name="80Hz - 160Hz", value=0.0,
                                 start=-20.0, end=20.0, step=0.1, format=PrintfTickFormatter(format='%.2f dB'))
slider4 = pn.widgets.FloatSlider(name="160Hz - 320Hz", value=0.0,
                                 start=-20.0, end=20.0, step=0.1, format=PrintfTickFormatter(format='%.2f dB'))
slider5 = pn.widgets.FloatSlider(name="320Hz - 640Hz", value=0.0,
                                 start=-20.0, end=20.0, step=0.1, format=PrintfTickFormatter(format='%.2f dB'))
slider6 = pn.widgets.FloatSlider(name="640Hz - 1280Hz", value=0.0,
                                 start=-20.0, end=20.0, step=0.1, format=PrintfTickFormatter(format='%.2f dB'))
slider7 = pn.widgets.FloatSlider(name="1280Hz - 2560Hz", value=0.0,
                                 start=-20.0, end=20.0, step=0.1, format=PrintfTickFormatter(format='%.2f dB'))
slider8 = pn.widgets.FloatSlider(name="2560Hz - 5120Hz", value=0.0,
                                 start=-20.0, end=20.0, step=0.1, format=PrintfTickFormatter(format='%.2f dB'))
slider9 = pn.widgets.FloatSlider(name="5120Hz - 10024Hz", value=0.0,
                                 start=-20.0, end=20.0, step=0.1, format=PrintfTickFormatter(format='%.2f dB'))
slider10 = pn.widgets.FloatSlider(name="10024Hz - 20000Hz", value=0.0,
                                  start=-20.0, end=20.0, step=0.1, format=PrintfTickFormatter(format='%.2f dB'))


input_audio = pn.pane.Audio(name='Input Audio')
input_audio.visible = False

input_audio_label = pn.Row("####Input Audio", margin=(12, 0, 0, 0))
input_audio_label.visible = False


output_audio = pn.pane.Audio(name='Output Audio')
output_audio.visible = False

output_audio_label = pn.Row("####Output Audio", margin=(12, 0, 0, 0))
output_audio_label.visible = False


def activate_sliders(flag):
    if flag == True:
        slider1.disabled = False
        slider2.disabled = False
        slider3.disabled = False
        slider4.disabled = False
        slider5.disabled = False
        slider6.disabled = False
        slider7.disabled = False
        slider8.disabled = False
        slider9.disabled = False
        slider10.disabled = False
    else:
        slider1.disabled = True
        slider2.disabled = True
        slider3.disabled = True
        slider4.disabled = True
        slider5.disabled = True
        slider6.disabled = True
        slider7.disabled = True
        slider8.disabled = True
        slider9.disabled = True
        slider10.disabled = True


activate_sliders(False)


def file_input_callback(*events):

    for event in events:
        file_name_array = event.new.split(".")
        type = file_name_array[len(file_name_array) - 1]

    file_handler(type)
    plot_input(type)


def file_handler(type):

    if type == "wav":
        file_input.save("input.wav")
        file_input.save("output.wav")
    elif type == "csv":
        if os.path.exists("input.csv"):
            os.remove("input.csv")

        if os.path.exists("output.csv"):
            os.remove("output.csv")

        csv_file = open("input.csv", "w")
        csv_file.write(file_input.value.decode("utf-8"))
        csv_file.close()

        csv_file = open("output.csv", "w")
        csv_file.write(file_input.value.decode("utf-8"))
        csv_file.close()

    else:
        print("file type is not compatible")


def graph_visibility(flag):
    if flag == True:
        info_msg.visible = False
        input_graph.visible = True
        input_audio.visible = True
        input_audio_label.visible = True
        output_graph.visible = True
        output_audio.visible = True
        output_audio_label.visible = True

    else:
        info_msg.visible = True
        input_graph.visible = False
        input_audio.visible = False
        input_audio_label.visible = False
        output_graph.visible = False
        output_audio.visible = False
        output_audio_label.visible = False


def plot_input(type):
    if type == "wav":

        fs, data = wavfile.read("input.wav")

        n_samples = len(data)
        time = np.linspace(0, n_samples/fs, num=n_samples)

        # data, fs =  librosa.load("input.wav")

        # MAX = data.max()

        # data = data + MAX

        # data = data - MAX

        # data_fft = fft.rfft(data)

        # data = np.divide(np.abs(data_fft), data.size)

        # data = np.abs(data_fft)

        # time = fft.rfftfreq(n=n_samples, d=1.0/fs)

        # data = fft.irfft(data_fft)

        # time = data_time

        # data = librosa.amplitude_to_db(S=data)
        # data = librosa.db_to_amplitude(S_db=data)

        df = pd.DataFrame(data={
            "time": time,
            "amp": data
        })

        df.astype(float)

        # df.to_csv("dow.csv", index=False)

        # print(df["amp"].max())

        # df["amp"] = df["amp"].add(df["amp"].max())

        input_source.data = df
        output_source.data = df

        input_audio.object = "input.wav"
        output_audio.object = "output.wav"

        activate_sliders(True)
        graph_visibility(True)

    elif type == "csv":
        csv_df = pd.read_csv("input.csv", index_col=False, header=0)
        csv_df.columns = ["time", "amp"]

        csv_df = csv_df.astype(float)

        # csv_df["amp"] = librosa.amplitude_to_db(S=csv_df["amp"].to_numpy(), ref=1)
        # csv_df["amp"] = librosa.db_to_amplitude(S_db=csv_df["amp"].to_numpy(), ref=1)

        # data = csv_df["amp"].values

        # times = csv_df["time"].values
        # n_measurements = len(times)
        # timespan_seconds = times[-1] - times[0]
        # sample_rate_hz = int(n_measurements / timespan_seconds)

        # n_samples = len(data)

        # data_time = np.linspace(0, n_samples/sample_rate_hz, num=n_samples)

        # data_fft = fft.rfft(data)

        # data = np.abs(data_fft)*2 / n_samples

        # time = fft.rfftfreq(n=n_samples, d=1.0/sample_rate_hz)

        # csv_df = pd.DataFrame(data={
        #     "time": time,
        #     "amp": data
        # })

        input_source.data = csv_df
        output_source.data = csv_df

        times = csv_df["time"].values
        n_measurements = len(times)
        timespan_seconds = times[-1] - times[0]
        sample_rate_hz = int(n_measurements / timespan_seconds)

        data = csv_df["amp"].divide(32767).values

        if os.path.exists("input.wav"):
            os.remove("input.wav")

        if os.path.exists("output.wav"):
            os.remove("output.wav")

        sf.write("input.wav", data, sample_rate_hz)
        sf.write("output.wav", data, sample_rate_hz)

        input_audio.object = "input.wav"
        output_audio.object = "output.wav"

        graph_visibility(True)
        activate_sliders(True)

    else:
        graph_visibility(False)
        activate_sliders(False)


def update_output_audio(*events):
    amp = output_source.data["amp"]
    time = output_source.data["time"]

    n_measurements = len(amp)
    timespan_seconds = time[-1] - time[0]
    fs = int(n_measurements / timespan_seconds)

    data = amp/(32767)

    if os.path.exists("output.wav"):
        os.remove("output.wav")

    sf.write("output.wav", data, fs)

    output_audio.object = "output.wav"


def adding_gain(begin, finish, coef):
    amp = output_source.data["amp"].tolist()
    time = output_source.data["time"]

    n_samples = len(amp)
    timespan_seconds = time[-1] - time[0]

    fs = int(n_samples / timespan_seconds)

    data_fft = rfft(amp).tolist()

    # abs_data_fft = np.abs(data_fft)
    freq = rfftfreq(n=n_samples, d=1.0/fs).tolist()

    start = freq.index(begin)
    end = freq.index(finish)

    # print(start, end)

    print(max(freq))

    band = data_fft[start:end + 1]

    updated_band = [coef * i for i in band]

    data_fft = data_fft[:start] + updated_band + data_fft[end + 1:]
    
    data = irfft(data_fft)

    output_source.data = pd.DataFrame(data={
        "time": time,
        "amp": data
    })

    # update_output_audio()
    

    n_measurements = len(data)
    timespan_seconds = time[-1] - time[0]
    fs = int(n_measurements / timespan_seconds)

    data = data/(32767)

    if os.path.exists("output.wav"):
        os.remove("output.wav")

    sf.write("output.wav", data, fs)

    output_audio.object = "output.wav"



def update_data_source():

    for i, value in enumerate(default_sliders_values):

        coef = 10**(value/20)

        if i == 0:
            # adding_gain(19.970472013548132, 40.76164835642017, coef)
            adding_gain(20, 40, coef)
        elif i == 1:
            adding_gain(41, 80, coef)
        elif i == 2:
            adding_gain(81, 160, coef)
        elif i == 3:
        # if i == 3:
            adding_gain(161, 320, coef)
        elif i == 4:
            adding_gain(321, 640, coef)
        elif i == 5:
            adding_gain(641, 1280, coef)
        elif i == 6:
            adding_gain(1281, 2560, coef)
        elif i == 7:
            adding_gain(2561, 5120, coef)
        elif i == 8:
            adding_gain(5121, 10240, coef)
        # elif i == 9:
        #     adding_gain(10241, 20000, coef)


def update_sliders_value(*events):
    for i, s in enumerate([slider1, slider2, slider3, slider4, slider5, slider6, slider7, slider8, slider9, slider10]):
        default_sliders_values[i] = np.round(s.value, 3)
        # s.js_link(output_audio, value="object")
    update_data_source()


for s in [slider1, slider2, slider3, slider4, slider5, slider6, slider7, slider8, slider9, slider10]:
    # s.on_change("value", update_sliders_value)
    s.param.watch(update_sliders_value, "value")
    s.jslink(output_graph, value="source")
    # s.jslink(output_audio)



# output_audio.jscallback(args={
#     "source": output_audio.object
# })



file_input.param.watch(file_input_callback, "filename")


file_input.jslink(input_audio, value="object")
file_input.jslink(output_audio, value="object")

in_graph_layout = pn.pane.Bokeh(row(Spacer(width=130), column(
    input_graph), Spacer(width=50)))

out_graph_layout = pn.pane.Bokeh(row(Spacer(width=130), column(
    output_graph), Spacer(width=50)))

in_audio_layout = pn.Row(
    input_audio_label, input_audio, margin=(15, 0, 15, 150))

out_audio_layout = pn.Row(
    output_audio_label, output_audio, margin=(15, 0, 15, 150))


visual_sec = pn.Column(info_msg, in_graph_layout,
                       in_audio_layout, out_graph_layout, out_audio_layout)

# visual_sec.visible = False

# sliders = pn.pane.Bokeh(column(slider1, slider2, slider3, slider4, slider5,
#                                slider6, slider7, slider8, slider9, slider10), width=400, margin=(0, 0, 0, 5))


sliders = pn.Column(slider1, slider2, slider3, slider4, slider5,
                    slider6, slider7, slider8, slider9, slider10, width=400, margin=(0, 0, 0, 5))

app = pn.Row(visual_sec, pn.Column(file_input, modes, sliders))

app.servable()
