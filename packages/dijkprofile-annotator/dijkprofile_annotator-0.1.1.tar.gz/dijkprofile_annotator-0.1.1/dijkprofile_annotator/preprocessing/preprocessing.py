import csv
import os
from operator import itemgetter

import numpy as np
from dijkprofile_annotator.config import (CLASS_DICT_FULL, CLASS_DICT_REGIONAL,
                                          CLASS_DICT_SIMPLE,
                                          CLASS_DICT_SIMPLE_BERM,
                                          CLASS_DICT_SIMPLE_SLOOT)
from dijkprofile_annotator.dataset import DijkprofileDataset
from sklearn.model_selection import train_test_split


def read_surfaceline_file(surfaceline_fp):
    """Read surfaceline file and convert to dict.

    Args:
        surfaceline_fp (string): path to the surfacelines file.

    Returns:
        dict: dict containing list of points per location.
    """
    # read the coordinates and collect to surfaceline_dict
    surfacelines = {}
    with open(surfaceline_fp) as csvfile:
        surfacereader = csv.reader(csvfile, delimiter=';', quotechar='|')
        next(surfacereader)  # skip header
        # print("header: {}".format(header)) # not very useful
        stop_exec = False
        for row in surfacereader:
            if stop_exec:
                break
            location = row[0]
            surfacelines[location] = []
            for i in range(1, len(row)-2, 3):
                # some files have empty points
                if row[i] == '' or row[i+1] == '' or row[i+2] == '':
                    continue
                try:

                    x = _parse_coordinate(row[i].replace('"', ''))
                    y = _parse_coordinate(row[i+1].replace('"', ''))
                    z = _parse_coordinate(row[i+2].replace('"', ''))
                    surfacelines[location].append((x, y, z))
                except ValueError as e:
                    print(f"error reading point from surfaceline at location: {location} (index: {i}), error: {e}")
                    stop_exec = True
                    break
    return surfacelines


def read_charpoints_file(charlines_fp):
    """Read characteristicpoints file and convert to dict.

    Args:
        charlines_fp (string): path to characteristicpoints file.

    Returns:
        dict: dict containing list of points per location.
    """
    charpoints = {}
    with open(charlines_fp) as csvfile:
        cpointsreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        header = next(cpointsreader)
        stop_exec = False
        for idx, row in enumerate(cpointsreader):
            if stop_exec:
                break
            try:
                location = row[0]
            except IndexError as e:
                print(f"couldn't read location in row: {row} at {idx}, file: {charlines_fp}")
            point_dict = {}
            for i in range(1, len(row)-2, 3):
                if row[i] == '' or row[i+1] == '' or row[i+2] == '':
                    continue
                try:
                    x = _parse_coordinate(row[i].replace('"', ''))
                    y = _parse_coordinate(row[i+1].replace('"', ''))
                    z = _parse_coordinate(row[i+2].replace('"', ''))

                    point_dict[header[i][2:]] = (x, y, z)
                except ValueError as e:
                    print(
                        f"error reading point from characteristicpoints at location: {location} (index: {i}), error: {e}")
                    stop_exec = True

            charpoints[location] = point_dict
    return charpoints


def _parse_coordinate(coord):
    """Convert string point coordinate to float, remove double dots if needed.
       Some of the coordinates contain multiple dots, probably because someone
       opened the file in excel and it formatted it weird. In all examples I've
       seen the first point is only to indicate 1000's and can savely be removed

    Args:
        point (str): string representation of the number to parse

    Returns:
        float: float representation of the coordinate
    """
    try:
        return float(coord)
    except:
        parts = coord.split(".")
        return float("".join(parts[:-1]) + "." + parts[-1])


def make_height_profiles(surfaceline_dict, max_profile_size):
    """Make height arrays from surfacelines dict.

    Args:
        surfaceline_dict (dict): dict of surfacelines by location.
        max_profile_size (int): fixed max size for the height profile.

    Returns:
        dict: dict containing height profiles by location.
    """
    profile_dict = {}
    for location in surfaceline_dict.keys():
        heights = np.array(surfaceline_dict[location])[:, 2].astype(np.float32)

        # we'll fit whole profile in a fixed length so that multiple profiles can be used as samples
        z_tmp = np.zeros(max_profile_size)
        profile_length = heights.shape[0]
        if profile_length < max_profile_size:
            z_tmp[:profile_length] = np.array(heights, dtype=np.float32)[:profile_length]
            z_tmp[profile_length:] = heights[profile_length-1]
            heights = z_tmp
        else:
            heights = heights[:max_profile_size]
        profile_dict[location] = {"profile": heights}
    return profile_dict


def make_labeled_height_profiles(surfaceline_dict, cpoints_dict, max_profile_size, class_list='simple', require_all_points=True):
    """Make height profile and labels from surfacelines and cpoints.

    Args:
        surfaceline_dict (dict): dict of surfacelines by location.
        cpoints_dict (dict): dict of characteristic points by location.
        max_profile_size (int): fixed max size for the height profile.
        class_list (bool): selection of classes to use, see config.
        require_all_points: filter profiles that do not contain all the points in the class_list.

    Returns:
        dict: dict containing height profiles and their labels by location.
    """
    profile_label_dict = {}

    class_list = class_list.lower()
    class_dict = {}
    if class_list == 'regional':
        class_dict = CLASS_DICT_REGIONAL
    elif class_list == 'simple':
        class_dict = CLASS_DICT_SIMPLE
    elif class_list == 'berm':
        class_dict = CLASS_DICT_SIMPLE_BERM
    elif class_list == 'sloot':
        class_dict = CLASS_DICT_SIMPLE_SLOOT
    elif class_list == 'full':
        class_dict = CLASS_DICT_FULL
    else:
        raise NotImplementedError(f"No class list available of type: {class_list}")
    
    required_point_types = list(class_dict.keys())
    required_point_types.remove('leeg')  # we don't want to require check for the empty class
        
    for location in surfaceline_dict.keys():
        heights = np.array(surfaceline_dict[location])[:, 2].astype(np.float32)
        labels = np.zeros(len(heights))

        # if no labels were given for this location, skip it
        if not location in cpoints_dict.keys():
            # print(f"location not in cpoints dict, {location}")
            continue
        
        # skip the location if the required points are not all present
        if require_all_points:
            labeled_point_types = [key for key, value in cpoints_dict[location].items() if value != (-1.0, -1.0, -1.0)]
            if not all([point_type in labeled_point_types for point_type in required_point_types]):
                # print(f"not all point types present, missing {set(required_point_types) - set(labeled_point_types)}")
                continue

        for i, (key, point) in enumerate(cpoints_dict[location].items()):
            # if the point is not empty, find the nearest point in the surface file,
            # problems with rounding errors require matching by distance per point
            if point == (-1.0, -1.0, -1.0):
                continue

            distances = []
            for idx, surfacepoint in enumerate(surfaceline_dict[location]):
                dist = np.linalg.norm(np.array(surfacepoint)-np.array(point))
                distances.append((idx, dist))
            (idx, dist) = sorted(distances, key=itemgetter(1))[0]
            if key in class_dict:
                labels[idx] = class_dict[key]

        # forward fill the labels
        for i in range(1, len(labels)):
            if labels[i] == 0.0:
                labels[i] = labels[i-1]

        # we'll fit whole profile in a fixed length so that multiple profiles can be used as samples
        z_tmp = np.zeros(max_profile_size)
        labels_tmp = np.zeros(max_profile_size)
        profile_length = labels.shape[0]
        if profile_length < max_profile_size:
            z_tmp[:profile_length] = np.array(heights, dtype=np.float32)[:profile_length]
            labels_tmp[:profile_length] = np.array(labels)[:profile_length]
            z_tmp[profile_length:] = heights[profile_length-1]
            labels_tmp[profile_length:] = labels[profile_length-1]
            heights = z_tmp
            labels = labels_tmp
        else:
            heights = heights[:max_profile_size]
            labels = labels[:max_profile_size]

        # rescale every profile to between -1 and 1
        # scaler = MinMaxScaler(feature_range=(-1, 1))
        # heights = scaler.fit_transform(heights.reshape(-1, 1))

        profile_label_dict[location] = {}
        profile_label_dict[location]['profile'] = heights.astype(np.float32)
        profile_label_dict[location]['label'] = labels.astype(np.int32)
    return profile_label_dict


def filepath_pair_to_labeled_sample(source_surfacelines, source_characteristicpoints, max_profile_size=352, class_list='simple', require_all_points=True):
    """Convert pair of surfacelines and characteristicpoints filepaths to format suited for machine learning.

    Args:
        source_surfacelines (string): path to the surfacelines file.
        source_characteristicpoints (string): path to the characteristicpoints file.
        max_profile_size (int, optional): max size for the profile. Defaults to 352.
        regional (bool): use regional point labelset, see config. Defaults to False.

    Returns:
        dict: dict containing height profile and labels by location.
    """
    surfaceline_dict = read_surfaceline_file(source_surfacelines)
    cpoints_dict = read_charpoints_file(source_characteristicpoints)

    profile_label_dict = make_labeled_height_profiles(
                            surfaceline_dict, 
                            cpoints_dict, 
                            max_profile_size, 
                            class_list=class_list, 
                            require_all_points=require_all_points)
    return profile_label_dict


def file_pairs_to_tensor_profiles(filepair_list, max_profile_size=352, class_list='simple', require_all_points=True):
    """Convert list of pairs of surfacelines and characteristicpoints to format suited for machine learning.

    Args:
        filepair_list (list): list of tuples containing the paths to the surfacelines and characteristicpoints files.
        max_profile_size (int, optional): max size for the profile. Defaults to 352.
        regional (bool): use regional point labelset, see config. Defaults to False.

    Returns:
        dict: Dict containing all the height profiles and labels by location.
    """
    all_profiles = {}
    for source_surfacelines, source_characteristicpoints in filepair_list:
        profile_label_dict = filepath_pair_to_labeled_sample(
            source_surfacelines,
            source_characteristicpoints,
            max_profile_size,
            class_list,
            require_all_points=require_all_points)
        for key, value in profile_label_dict.items():
            all_profiles[key] = value
    return all_profiles


def get_file_pairs_from_dir(path, krp_format=False):
    """Recursively get all pairs of lines and points files in a directory.

    Args:
        path (str): path to the root directory containing the lines and points csv files,
                    directory is searched recursively for pairs.
        krp (bool): Indicates that the folder contains csv files in the naming convention used by 
                    waterschap Vallei en Veluwe.

    Returns:
        list: list of tuples where the first item is the path to the surfacelines.csv and the second
              the path to the characteristicpoints.csv
    """
    if krp_format:
        return _get_file_pairs_from_dir_krp(path)
    list_of_files = []
    for (dirpath, _, filenames) in os.walk(path):
        for filename in filenames:
            if filename.endswith('lines.csv'):
                if os.path.exists(os.sep.join([dirpath, filename])) and \
                   os.path.exists(os.sep.join([dirpath, 'characteristicpoints.csv'])):

                    list_of_files.append((
                        os.sep.join([dirpath, filename]),
                        os.sep.join([dirpath, 'characteristicpoints.csv'])))
    return list_of_files


def _get_file_pairs_from_dir_krp(path):
    """Recursively get all pairs of lines and points files in a directory but in the format used
    by Waterschap Vallei en Veluwe, same functionality as get_file_pairs_from_dir.

    Args:
        path (str): path to the root directory containing the lines and points csv files,
                    directory is searched recursively for pairs 

    Returns:
        list: list of tuples where the first item is the path to the surfacelines.csv and the second
              the path to the characteristicpoints.csv
    """
    list_of_files = []
    for (dirpath, _, filenames) in os.walk(path):
        for filename in filenames:
            if filename.endswith('.krp.csv'):
                if os.path.exists(os.sep.join([dirpath, filename])) and \
                   os.path.exists(os.sep.join([dirpath, filename.split(".krp")[0] + ".csv"])):

                    list_of_files.append((
                        os.sep.join([dirpath, filename.split(".krp")[0] + ".csv"]),
                        os.sep.join([dirpath, filename])))
    return list_of_files


def load_datasets(annotation_tuples, custom_scaler_path=None, test_size=0.2, max_profile_size=512, class_list='simple', require_all_points=True):
    """Load datasets given list of annotation tuples.

    Args:
        annotation_tuples ([(str,str)]): list of tuples of filepaths to the lines and points files.
        custom_scaler_path (str, optional): path to a custom scaler to rescale the data. Defaults to None.
        test_size (float, optional): Test size for the training. Defaults to 0.2.
        max_profile_size (int, optional): max profile size. Defaults to 512.
        class_list (str, optional): class_mapping/class_list to use. Defaults to 'simple'.
        require_all_points (bool, optional): wether to drop profiles that don't contain all points in the mapping. Defaults to True.

    Returns:
        DijkprofileDataset, DijkprofileDataset: train and test dataset classes
    """
    profile_dict = file_pairs_to_tensor_profiles(annotation_tuples, max_profile_size=max_profile_size, class_list=class_list, require_all_points=require_all_points)

    # construct dataloaders
    id_list = list(profile_dict.keys())
    [train, test] = train_test_split(id_list, shuffle=True, test_size=test_size)

    dataset_train = DijkprofileDataset(profile_dict, train, custom_scaler_path=custom_scaler_path)
    dataset_validation = DijkprofileDataset(profile_dict, test, custom_scaler_path=custom_scaler_path)

    return dataset_train, dataset_validation
