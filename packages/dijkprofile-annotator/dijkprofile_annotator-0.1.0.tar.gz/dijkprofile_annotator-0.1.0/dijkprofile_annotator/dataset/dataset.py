import numpy as np
import torch.utils.data as data


class DijkprofileDataset(data.Dataset):
    """Pytorch custom dataset class to use with the pytorch dataloader."""
    
    def __init__(self, profile_dict, partition, custom_scaler_path=None):
        """Dijkprofile Dataset, provides profiles and labels to pytorch model.

        Args:
            profile_dict (dict): dict containing the profiles and labels
            partition (list): list used to split the dataset into train and test
            sets. list contains ids to use for this dataset, format is
            as returned by sklearn.model_selection.train_test_split
        """
        self.data_dict = profile_dict
        self.list_IDs = partition

        print("scaler in dataset class is depracated and moved to preprocessing")
        # load scaler
        # if custom_scaler_path:
        #     self.scaler = joblib.load(custom_scaler_path)
        # else:
        #     self.scaler = joblib.load(os.path.join(dir, config.SCALER_PATH))
        # # rescale all profiles profiles
        # for key in profile_dict.keys():
            # profile_dict[key]['profile'] = self.scaler.transform(
            #     profile_dict[key]['profile'].reshape(-1, 1)).reshape(-1)
            # profile_dict[key]['profile'] = profile_dict[key]['profile'] / 10
    
    def __len__(self):
        return len(self.list_IDs)
    
    def __getitem__(self, index):
        id = self.list_IDs[index]
        X = self.data_dict[id]['profile'].reshape(1,-1).astype(np.float32)
        y = self.data_dict[id]['label'].reshape(1,-1)
        return X, y
    
    def __str__(self):
        return "<Dijkprofile dataset: datapoints={}>".format(len(self.list_IDs))
