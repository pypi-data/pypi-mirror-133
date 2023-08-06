import csv
import os

import numpy as np
import torch

import dijkprofile_annotator.config as config
import dijkprofile_annotator.utils as utils
import dijkprofile_annotator.preprocessing as preprocessing
from dijkprofile_annotator.models import Dijknet


def annotate(surfacelines_filepath, outputfile, class_list='simple', max_profile_length=512, custom_model_path=None, custom_scaler_path=None, device=None):
    surfacelines_dict = preprocessing.read_surfaceline_file(surfacelines_filepath)
    profile_dict = preprocessing.make_height_profiles(surfacelines_dict, max_profile_length)

    dir = os.path.dirname(__file__)

    if device:
        device = device
    else:
        # setup model
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    class_dict, _, _ = utils.get_class_dict(class_list)
    model = Dijknet(1, len(class_dict))

    if custom_model_path:
        model.load_state_dict(torch.load(custom_model_path, map_location=device))
    else:
        model.load_state_dict(torch.load(os.path.join(dir, config.MODEL_PATH), map_location=device))
    model.eval()

    # copy network to device
    model = model.to(device)

    predictions = make_predictions(model, profile_dict, max_profile_length, device)

    write_predictions(predictions, profile_dict, surfacelines_dict, outputfile, class_list)


def make_predictions(model, profile_dict, max_profile_length, device):
    accumulator = np.zeros((len(profile_dict), max_profile_length))
    for i, key in enumerate(profile_dict.keys()):
        accumulator[i] = profile_dict[key]['profile'][:max_profile_length]

    accumulator = accumulator.reshape(accumulator.shape[0], 1, max_profile_length)

    outputs = model(torch.tensor(accumulator).to(device).float())
    flat_output = torch.argmax(outputs, dim=1).cpu()
    predictions = flat_output.numpy()
    return predictions


def write_predictions(predictions, profile_dict, surfacelines_dict, output_filepath, class_list):
    class_dict, inverse_class_dict, class_weights = utils.get_class_dict(class_list)

    with open(output_filepath, 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(config.HEADER)
        for i, key in enumerate(profile_dict.keys()):
            # get predictions
            profile_pred = predictions[i]

            # construct dict with key for each row
            row_dict = {key:-1 for key in config.HEADER}
            row_dict["LOCATIONID"] = key

            # loop through predictions and for the entries
            used_classes = []
            prev_class_n = 999 # key thats not in the inverse_class_dict
            for index, class_n in enumerate(profile_pred):
                if class_n == 0 or class_n in used_classes:
                    continue
                if class_n != prev_class_n:
                    # get class name
                    class_name = inverse_class_dict[class_n]

                    # if this index is different from the last, this is the characteristicpoint
                    used_classes.append(prev_class_n)

                    # set prev_class to the new class
                    prev_class_n = class_n

                    # construct the csv row with the new class
                    if index >= len(surfacelines_dict[key]):
                        continue

                    (x,y,z) = surfacelines_dict[key][index]
                    row_dict["X_" + class_name] = round(x, 3)
                    row_dict["Y_" + class_name] = round(y, 3)
                    row_dict["Z_" + class_name] = round(z, 3)

            # write the row to the csv file
            row = []
            for columnname in config.HEADER:
                row.append(row_dict[columnname])
            writer.writerow(row)
