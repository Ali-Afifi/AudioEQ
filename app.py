import os
import base64

import numpy as np
import pandas as pd
import panel as pn
import soundfile as sf

from scipy.io import wavfile


from panel.interact import interact

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Slider, Button, Select, CustomJS, Div
from bokeh.layouts import column, row, Spacer


file_input = pn.widgets.FileInput(
    accept=".txt,.csv,.wav", width=200, margin=(70, 0, 10, 10))
modes = pn.widgets.Select(name='modes', options=[
                          'default', 'music', 'vocals'], width=400)


info_msg = pn.pane.Alert("""<h1 style="font-size: 50px; color: #242020;">Upload a file and start mixing <br> <span style="font-size: 30px; color: grey;">&lpar;only *.csv and *.wav files&rpar;</span></h1>""",
                         alert_type="dark", width=1200, height=400, margin=(0, 50, 0, 130))


input_source = ColumnDataSource(pd.DataFrame())

input_graph = figure(height=400, width=1200,
                     tools="crosshair,pan,reset,save,wheel_zoom", title="Input Graph")

input_graph.line(x="time", y="amp", source=input_source,
                 line_width=3, line_alpha=0.6)

input_graph.visible = False

input_audio = pn.pane.Audio(name='Input Audio')
input_audio.visible = False

input_audio_label = pn.Row("####Input Audio", margin=(12, 0, 0, 0))
input_audio_label.visible = False


def file_input_callback(*events):

    for event in events:
        file_name_array = event.new.split(".")
        type = file_name_array[len(file_name_array) - 1]

    file_handler(type)
    plot_input(type)


def file_handler(type):

    if type == "wav":
        file_input.save("input.wav")
    elif type == "csv":
        if os.path.exists("input.csv"):
            os.remove("input.csv")

        csv_file = open("input.csv", "w")
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

    else:
        info_msg.visible = True
        input_graph.visible = False
        input_audio.visible = False
        input_audio_label.visible = False


def plot_input(type):
    if type == "wav":
        fs, data = wavfile.read("input.wav")
        n_samples = len(data)
        time = np.linspace(0, n_samples/fs, num=n_samples)
        df = pd.DataFrame(data={
            "time": time,
            "amp": data
        })

        input_source.data = df


        if os.path.exists("dow.csv"):
            os.remove("dow.csv")
            
        df.to_csv("dow.csv", encoding='utf-8', index=False)

        input_audio.object = "input.wav"

        graph_visibility(True)

    elif type == "csv":
        csv_df = pd.read_csv("input.csv", index_col=False, header=0)
        csv_df.columns = ["time", "amp"]

        csv_df = csv_df.astype(float)
        
        input_source.data = csv_df

        times = csv_df["time"].values
        n_measurements = len(times)
        timespan_seconds = times[-1] - times[0]
        sample_rate_hz = int(n_measurements / timespan_seconds)

        # print("fs:", sample_rate_hz)
        data = csv_df["amp"].values

        # csv_df.info()
        
        if os.path.exists("input.wav"):
            os.remove("input.wav")

        sf.write("input.wav", data, sample_rate_hz)

        input_audio.object = "input.wav"

        graph_visibility(True)

    else:
        graph_visibility(False)
        return


file_input.param.watch(file_input_callback, "filename")

file_input.jslink(input_audio, value="object")


in_graph_layout = pn.pane.Bokeh(row(Spacer(width=130), column(
    input_graph), Spacer(width=50)))

in_audio_layout = pn.Row(
    input_audio_label, input_audio, margin=(15, 0, 15, 150))

visual_sec = pn.Column(info_msg, in_graph_layout, in_audio_layout)

# visual_sec.visible = False

app = pn.Row(visual_sec, pn.Column(file_input, modes))


app.servable()
