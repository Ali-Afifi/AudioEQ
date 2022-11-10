import os
import base64

import numpy as np
import pandas as pd
import panel as pn

from scipy.io import wavfile

from panel.interact import interact

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Slider, Button, Select, CustomJS, Div
from bokeh.layouts import column, row, Spacer


file_input = pn.widgets.FileInput(accept=".txt,.csv,.wav", width=200, margin=(70,0,10,10))
modes = pn.widgets.Select(name='modes', options=[
                          'default', 'music', 'vocals'], width=400)


info_msg = Div(text="""<h1 style="font-size: 50px; color: #242020;">Upload a file and start mixing <br> <span style="font-size: 30px; color: grey;">&lpar;only *.csv and *.wav files&rpar;</span></h1>""",
               width=1200, height=400)


input_source = ColumnDataSource(pd.DataFrame())

input_graph = figure(height=400, width=1200,
                     tools="crosshair,pan,reset,save,wheel_zoom", title="Input Graph")

input_graph.line(x="time", y="amp", source=input_source,
                 line_width=3, line_alpha=0.6)

input_graph.visible = False

input_audio = pn.pane.Audio(name='Input Audio', margin=(15,0,15,130))
input_audio.visible = False


def file_input_callback(*events):

    for event in events:
        file_name_array = event.new.split(".")
        type = file_name_array[len(file_name_array) - 1]

    file_handler(type)
    plot_input(type)


def file_handler(type):

    if type == "wav":
        file_input.save("temp.wav")
    elif type == "csv":
        if os.path.exists("temp.csv"):
            os.remove("temp.csv")

        csv_file = open("temp.csv", "w")
        csv_file.write(file_input.value.decode("utf-8"))
        csv_file.close()

    else:
        print("file type is not compatible")


def plot_input(type):
    if type == "wav":
        fs, data = wavfile.read("temp.wav")
        n_samples = len(data)
        time = np.linspace(0, n_samples/fs, num=n_samples)
        df = pd.DataFrame(data={
            "time": time,
            "amp": data
        })

        input_source.data = df

        info_msg.visible = False
        input_graph.visible = True
        input_audio.visible = True

    elif type == "csv":
        csv_df = pd.read_csv("temp.csv", index_col=False, header=0)
        csv_df.columns = ["time", "amp"]
        input_source.data = csv_df

        info_msg.visible = False
        input_graph.visible = True
        input_audio.visible = True
        
    else:
        info_msg.visible = True
        input_graph.visible = False
        input_audio.visible = False
        return


file_input.param.watch(file_input_callback, "filename")

# graphs = pn.Column("#A")
# inputs = pn.Column(file_input)

# app = pn.Row(graphs, inputs)

in_graph = pn.pane.Bokeh(row(Spacer(width=130), column(info_msg, input_graph), Spacer(width=50)))

visual_sec = pn.Column(in_graph, input_audio)

app = pn.Row(visual_sec, pn.Column(file_input,modes))


app.servable()
