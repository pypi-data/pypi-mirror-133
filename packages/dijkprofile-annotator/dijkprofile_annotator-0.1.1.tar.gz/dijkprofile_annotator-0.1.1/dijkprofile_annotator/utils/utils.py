import os
import random
from collections import defaultdict

import dijkprofile_annotator.preprocessing as preprocessing
import dijkprofile_annotator.config as config
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch
import torch.nn.functional as F
from sklearn.isotonic import IsotonicRegression
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def extract_img(size, in_tensor):
    """
    Args:
        size(int) : size of cut
        in_tensor(tensor) : tensor to be cut
    """
    dim1 = in_tensor.size()[2]
    in_tensor = in_tensor[:, :, int((dim1-size)/2):int((size + (dim1-size)/2))]
    return in_tensor


def ffill(arr):
    """Forward fill utility function.

    Args:
        arr (np.array): numpy array to fill

    Returns:
        np.array: filled array.
    """
    mask = np.isnan(arr)
    idx = np.where(~mask, np.arange(mask.shape[1]), 0)
    np.maximum.accumulate(idx, axis=1, out=idx)
    out = arr[np.arange(idx.shape[0])[:,None], idx]
    return out

def train_scaler(profile_dict, scaler_type='minmax'):
    """Train a scaler given a profile dict

    Args:
        profile_dict (dict): dict containing the profile heights and labels

    Returns:
        sklearn MinMaxScaler or StandardScaler: fitted scaler in sklearn format
    """
    if scaler_type == 'minmax':
        scaler = MinMaxScaler(feature_range=(-1, 1))  # for neural networks -1,1 is better than 0,1
    elif scaler_type == 'standard':
        scaler = StandardScaler()
    else:
        raise NotImplementedError(f"no scaler: {scaler}")
    randkey = random.choice(list(profile_dict.keys()))
    accumulator = np.zeros((len(profile_dict), profile_dict[randkey]['profile'].shape[0]))

    for i, key in enumerate(profile_dict.keys()):
        accumulator[i, :] = profile_dict[key]['profile']

    scaler.fit(accumulator.reshape(-1, 1))
    return scaler


def get_class_dict(class_list):
    """Get correct class dicts and weights from config.

    Args:
        class_list (string): string representing the class mappings to use

    Raises:
        NotImplementedError: raise if an not implemented class mapping is passed

    Returns:
        (dict,dict,list): dict with class mappings, inverse of that dict, weights for each class.
    """
    class_list = class_list.lower()
    if class_list == 'regional':
        class_dict = config.CLASS_DICT_REGIONAL
        inverse_class_dict = config.INVERSE_CLASS_DICT_REGIONAL
        class_weights = config.WEIGHT_DICT_REGIONAL
    elif class_list == 'simple':
        class_dict = config.CLASS_DICT_SIMPLE
        class_weights = config.WEIGHT_DICT_SIMPLE
        inverse_class_dict = config.INVERSE_CLASS_DICT_SIMPLE
    elif class_list == 'berm':
        class_dict = config.CLASS_DICT_SIMPLE_BERM
        class_weights = config.WEIGHT_DICT_SIMPLE_BERM
        inverse_class_dict = config.INVERSE_CLASS_DICT_SIMPLE_BERM
    elif class_list == 'sloot':
        class_dict = config.CLASS_DICT_SIMPLE_SLOOT
        class_weights = config.WEIGHT_DICT_SIMPLE_SLOOT
        inverse_class_dict = config.INVERSE_CLASS_DICT_SIMPLE_SLOOT
    elif class_list == 'full':
        class_dict = config.CLASS_DICT_FULL
        class_weights = config.WEIGHT_DICT_FULL
        inverse_class_dict = config.INVERSE_CLASS_DICT_FULL
    else:
        raise NotImplementedError(f"No configs found for class list of type: {class_list}")
    return class_dict, inverse_class_dict, class_weights


def force_sequential_predictions(predictions, method='isotonic'):
    """Force the classes in the sample to always go up from left to right. This is
    makes sense because a higher class could never be left of a lower class in the 
    representation chosen here. Two methods are available, Isotonic Regression and
    a group first method. I would use the Isotonic regression.

    Args:
        predictions (torch.Tensor): Tensor output of the model in shape (batch_size, channel_size, sample_size)
        method (str, optional): method to use for enforcing the sequentiality. Defaults to 'isotonic'.

    Raises:
        NotImplementedError: if the given method is not implemented

    Returns:
        torch.Tensor: Tensor in the same shape as the input but then with only increasing classes from left to right.
    """
    predictions = predictions.detach().cpu()
    n_classes = predictions.shape[1]  # 1 is the channel dimension
    if method == 'first':
        # loop over batch
        for j in range(predictions.shape[0]):
            pred = torch.argmax(predictions[j], dim=0)

            # construct dict of groups of start-end indices for class
            groups = defaultdict(list)
            current_class = pred[0]
            group_start_idx = 0
            for i in range(1, len(pred)):
                if pred[i] != current_class:
                    groups[current_class.item()].append((group_start_idx, i))
                    group_start_idx = i
                    current_class = pred[i]

            # if the class occurs again later in the profile
            # discard this occurance of it
            new_pred = torch.zeros(len(pred))
            last_index = 0
            for class_n, group_tuples in sorted(groups.items()):
                for group_tuple in group_tuples:
                    if group_tuple[0] >= last_index:
                        new_pred[group_tuple[0]:group_tuple[1]] = class_n
                        last_index = group_tuple[1]
                        break
            
            # simple forward fill
            for i in range(1, len(new_pred)):
                if new_pred[i] == 0:
                    new_pred[i] = new_pred[i-1]
            
            # encode back to one-hot tensor
            predictions[j] = F.one_hot(new_pred.to(torch.int64), num_classes=n_classes).permute(1,0)
    elif method == 'isotonic':
        for i in range(predictions.shape[0]):
            pred = torch.argmax(predictions[i], dim=0)

            x = np.arange(0,len(pred))
            iso_reg = IsotonicRegression().fit(x, pred)
            new_pred = iso_reg.predict(x)
            new_pred = np.round(new_pred)

            # encode back to one-hot tensor
            new_pred = F.one_hot(torch.Tensor(new_pred).to(torch.int64), num_classes=n_classes).permute(1,0)
            predictions[i] = new_pred
    else:
        raise NotImplementedError(f"Unknown method: {method}")
    
    return predictions



def visualize_prediction(heights, prediction, labels, location_name, class_list):
    """visualize a profile plus labels and prediction

    Args:
        heights (tensor): tensor containing the heights data of the profile
        prediction (tensor): tensor containing the predicted data of the profile
        labels (tensor): tensor containing the labels for each height point in heights
        location_name (str): name of the profile, just for visualization
        class_list (str): class mapping to use, determines which labels are visualized
    """
    class_dict, inverse_class_dict, _ = get_class_dict(class_list)
    fig, ax = plt.subplots(figsize=(20,11))
    plt.title(location_name)
    plt.plot(heights, label='profile')

    # change one-hot batched format to list of classes
    if prediction.dim() == 3:
        prediction = torch.argmax(torch.squeeze(prediction, dim=0), dim=0)
    if prediction.dim() == 2:
        # assuming channel first representation
        prediction = torch.argmax(prediction, dim=0)
    prediction = prediction.detach().cpu().numpy()
    
    # ax.set_ylim(top=np.max(heights), bottom=np.min(heights))
    label_height = np.min(heights)
    n_labels = len(np.unique(labels))
    label_height_distance = (np.max(heights) - np.min(heights))/(n_labels*2)

    cmap = sns.color_palette("Set2", len(set(class_dict.values())))

    # plot actual labels
    prev_class_n = 999
    for index, class_n in enumerate(labels):
        if class_n == 0:
            continue
        if class_n != prev_class_n:
            plt.axvline(index, 0,5, color=cmap[class_n], linestyle=(0,(5,10))) # loose dashes
            plt.text(index, label_height, inverse_class_dict[class_n], rotation=0)
            label_height += label_height_distance
            prev_class_n = class_n
        
    # plot predicted points
    used_classes = []
    prev_class_n = 999
    for index, class_n in enumerate(prediction):
        if class_n == 0 or class_n in used_classes:
            continue
        if class_n != prev_class_n:
            plt.axvline(index, 0,5, color=cmap[class_n], linestyle=(0,(1,1))) # small dots
            plt.text(index, label_height, "predicted " + inverse_class_dict[class_n], rotation=0)
            label_height += label_height_distance
            used_classes.append(prev_class_n)
            prev_class_n = class_n
    
    plt.show()


def visualize_sample(heights, labels, location_name, class_list):
    """visualize a profile and labels.

    Args:
        heights (tensor): tensor containing the heights data of the profile
        labels (tensor): tensor containing the labels for each height point in heights
        location_name (str): name of the profile, just for visualization
        class_list (str): class mapping to use, determines which labels are visualized
    """
    class_dict, inverse_class_dict, _ = get_class_dict(class_list)
    fig, ax = plt.subplots(figsize=(20,11))
    plt.title(location_name)
    plt.plot(heights, label='profile')
    
    # ax.set_ylim(top=np.max(heights), bottom=np.min(heights))
    label_height = np.min(heights)
    n_labels = len(np.unique(labels))
    label_height_distance = (np.max(heights) - np.min(heights))/(n_labels*2)

    cmap = sns.color_palette("Set2", len(set(class_dict.values())))

    # plot actual labels
    prev_class_n = 999
    for index, class_n in enumerate(labels):
        if class_n == 0:
            continue
        if class_n != prev_class_n:
            plt.axvline(index, 0,5, color=cmap[class_n], linestyle=(0,(5,10))) # loose dashes
            plt.text(index, label_height, inverse_class_dict[class_n], rotation=0)
            label_height += label_height_distance
            prev_class_n = class_n
    
    plt.show()
    
def visualize_files(linesfp, pointsfp, max_profile_size=512, class_list='simple', location_index=0, return_dict=False):
    """visualize profile lines and points filepaths.

    Args:
        linesfp (str): path to surfacelines file.
        pointsfp (str): path to points file.
        max_profile_size (int, optional): cutoff size of the profile, can leave on default here. Defaults to 512.
        class_list (str, optional): class mapping to use. Defaults to 'simple'.
        location_index (int, optional): index of profile to visualize.. Defaults to 0.
        return_dict (bool, optional): return the profile dict for faster visualization. Defaults to False.

    Returns:
        [dict, optional]: profile dict containing the profiles of the given files
    """
    profile_label_dict = preprocessing.filepath_pair_to_labeled_sample(linesfp, 
                                                               pointsfp, 
                                                               max_profile_size=max_profile_size, 
                                                               class_list=class_list)

    location_name = list(profile_label_dict.keys())[location_index]
    heights = profile_label_dict[location_name]['profile']
    labels = profile_label_dict[location_name]['label']
    
    class_dict, inverse_class_dict, _ = get_class_dict(class_list)
    fig, ax = plt.subplots(figsize=(20,11))
    plt.title(location_name)
    plt.plot(heights, label='profile')
    
    label_height = np.min(heights)
    n_labels = len(np.unique(labels))
    label_height_distance = (np.max(heights) - np.min(heights))/(n_labels)

    cmap = sns.color_palette("Set2", len(set(class_dict.values())))

    # plot actual labels
    prev_class_n = 999
    for index, class_n in enumerate(labels):
        if class_n == 0:
            continue
        if class_n != prev_class_n:
            plt.axvline(index, 0,5, color=cmap[class_n], linestyle=(0,(5,10))) # loose dashes
            plt.text(index, label_height, inverse_class_dict[class_n], rotation=0)
            label_height += label_height_distance
            prev_class_n = class_n
    
    plt.show()

    if return_dict:
        return profile_label_dict

def visualize_dict(profile_label_dict, class_list='simple', location_index=0):
    """visualise profile with labels from profile_dict, profile specified by index.

    Args:
        profile_label_dict (dict): dict containing profiles and labels
        class_list (str, optional): class_mapping to use for visualization. Defaults to 'simple'.
        location_index (int, optional): specifies the index of the profile to visualize. Defaults to 0.
    """
    location_name = list(profile_label_dict.keys())[location_index]
    heights = profile_label_dict[location_name]['profile']
    labels = profile_label_dict[location_name]['label']
    
    class_dict, inverse_class_dict, _ = get_class_dict(class_list)
    fig, ax = plt.subplots(figsize=(20,11))
    plt.title(location_name)
    plt.plot(heights, label='profile')
    
    label_height = np.min(heights)
    n_labels = len(np.unique(labels))
    label_height_distance = (np.max(heights) - np.min(heights))/(n_labels)

    cmap = sns.color_palette("Set2", len(set(class_dict.values())))

    # plot actual labels
    prev_class_n = 999
    for index, class_n in enumerate(labels):
        if class_n == 0:
            continue
        if class_n != prev_class_n:
            plt.axvline(index, 0,5, color=cmap[class_n], linestyle=(0,(5,10))) # loose dashes
            plt.text(index, label_height, inverse_class_dict[class_n], rotation=0)
            label_height += label_height_distance
            prev_class_n = class_n
    
    plt.show()