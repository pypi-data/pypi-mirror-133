import os
import math
import gradio as gr
import dijkprofile_annotator
from zipfile import ZipFile

def annotate_file(file_objects, model_type):
    # TODO: actually use different model types based on selected model, only a well trained dijk model is available now.
    generated_charfiles = []
    str1 = "Starting processing of files." 
    pad1 = math.floor((os.get_terminal_size().columns - len(str1)) / 2) * "="
    print(pad1 + "Starting processing of files." + pad1)
    for i, file_obj in enumerate(file_objects):
        target_filepath = f"/tmp/characteristicpoints_{i}.csv"
        print(f"    Processing file '{file_obj.name}', model '{model_type}', saving to '{target_filepath}'")
        dijkprofile_annotator.annotate(file_obj.name, target_filepath, device='cpu')
        generated_charfiles.append(target_filepath)
        print(f"    finished processing: {file_obj.name}! saved to : {target_filepath}")
        print("    ", "-" * (os.get_terminal_size().columns - 5))

    print("finished with all processing!")
    # return the csv file if only 1 file was given, return a zip otherwise.
    if len(generated_charfiles) == 1:
        print(f"returning file: {generated_charfiles[0]}")
        return generated_charfiles[0]
    else:
        return_zipfile = "/tmp/characterist_points.zip"
        with ZipFile(return_zipfile, 'w') as zipObj:
            for filepath in generated_charfiles:
                zipObj.write(filepath)
        print(f"returning file: {return_zipfile}")
        return return_zipfile

description = "Upload een surfacelines.csv bestand in QDAMEdit format en krijg een annotatie file in characteristicpoints format terug. \n" +\
              "Een neural netwerk gebaseerd op image segmentation heeft geleerd op basis van ~6000 geannoteerde profielen om zo goed mogelijk automatisch de punten te plaatsen op de profielen.\n" +\
              "Er zijn meerdere modellen beschikbaar om de annotatie te genereren, het 'dijk' model probeert alleen de dijk te vinden, het 'dijk+sloot' model zoekt ook naar een sloot en het 'volledig' model " +\
              "probeert zo veel mogelijk van de punten beschikbaar in het QDAMEdit format te vinden. Probeer eerst het 'dijk' model aangezien hier de consistentste resultaten uit komen."

def run():
    iface = gr.Interface(
    fn=annotate_file,
    title="Dijkprofiel Annotator",
    description=description,
    inputs=[gr.inputs.File(file_count="multiple", type="file", label="te annoteren surfacelines files", optional=False), gr.inputs.Dropdown(['dijk', 'dijk+sloot', "volledig"], type="value", default=None, label='Model type')],
    outputs=gr.outputs.File(label="gegenereerde file"))
    iface.launch()