import dijkprofile_annotator.preprocessing as preprocessing
import dijkprofile_annotator.utils as utils
import numpy as np
import torch
import torch.nn as nn
from dijkprofile_annotator.models import Dijknet
from PIL import Image
from torch.utils.data import DataLoader
from tqdm import tqdm


def get_loss_train(model, data_train, criterion):
    """generate loss over train set.

    Args:
        model (): model to use for prediction
        data_train (torch.utils.data.DataLoader)): Dataloader containing the profiles
        and labels
        criterion (pytorch loss function, probably nn.CrossEntropyLoss): loss function to be used.

    Returns:
        float: total accuracy
        float: total loss
    """
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.eval()
    total_acc = 0
    total_loss = 0
    for batch, (profile, masks) in enumerate(data_train):
        with torch.no_grad():
            profile = torch.Tensor(profile).to(device)
            masks = torch.Tensor(masks).to(device)
            outputs = model(profile)
            loss = criterion(outputs, masks)
            preds = torch.argmax(outputs, dim=1).float()
            acc = accuracy_check_for_batch(masks.cpu(), preds.cpu(), profile.size()[0])
            total_acc = total_acc + acc
            total_loss = total_loss + loss.cpu().item()
    return total_acc/(batch+1), total_loss/(batch + 1)


def accuracy_check(mask, prediction):
    """check accuracy of prediciton.

    Args:
        mask (torch.Tensor, PIL Image or str): labels
        prediction (torch.Tensor, PIL Image or str): predictions

    Returns:
        float: accuracy of prediction given mask.
    """
    ims = [mask, prediction]
    np_ims = []
    for item in ims:
        if 'str' in str(type(item)):
            item = np.array(Image.open(item))
        elif 'PIL' in str(type(item)):
            item = np.array(item)
        elif 'torch' in str(type(item)):
            item = item.numpy()
        np_ims.append(item)

    compare = np.equal(np_ims[0], np_ims[1])
    accuracy = np.sum(compare)

    return accuracy/len(np_ims[0].flatten())


def accuracy_check_for_batch(masks, predictions, batch_size):
    """check accuracy of prediciton given mask.

    Args:
        masks (torch.Tensor): labels
        predictions (torch.Tensor): predictions
        batch_size (int): batch size of prediciton/mask.

    Returns:
        float: accuracy of prediction given mask.
    """
    total_acc = 0
    for index in range(batch_size):
        total_acc += accuracy_check(masks[index], predictions[index])
    return total_acc/batch_size


def train(annotation_tuples,
          epochs=100,
          batch_size_train=32,
          batch_size_val=512,
          num_workers=6,
          custom_scaler_path=None,
          class_list='simple',
          test_size=0.2,
          max_profile_size=512,
          shuffle=True):
    """[summary]

    Args:
        annotation_tuples ([type]): [description]
        epochs (int, optional): [description]. Defaults to 100.
        batch_size_train (int, optional): [description]. Defaults to 32.
        batch_size_val (int, optional): [description]. Defaults to 512.
        num_workers (int, optional): [description]. Defaults to 6.
        custom_scaler_path ([type], optional): [description]. Defaults to None.
        class_list (str, optional): [description]. Defaults to 'simple'.
        test_size (float, optional): [description]. Defaults to 0.2.
        max_profile_size (int, optional): [description]. Defaults to 512.
        shuffle (bool, optional): [description]. Defaults to True.

    Raises:
        NotImplementedError: when given class_list is not implemented

    Returns:
        [type]: trained Dijknet model.
    """
    print(f"loading datasets")
    train_dataset, test_dataset = preprocessing.load_datasets(annotation_tuples,
                                                              custom_scaler_path=custom_scaler_path,
                                                              test_size=test_size,
                                                              max_profile_size=max_profile_size)
    print(f"loaded datasets:")
    print(f"    train: {len(train_dataset)} samples")
    print(f"    test:  {len(test_dataset)} samples")

    class_dict, _, class_weights = utils.get_class_dict(class_list)

    print(f"constructing model with {len(class_dict)} output classes")
    model = Dijknet(1, len(class_dict))

    # parameters
    train_params = {'batch_size': batch_size_train,
                    'shuffle': shuffle,
                    'num_workers': num_workers}

    params_val = {'batch_size': batch_size_val,
                  'shuffle': False,
                  'num_workers': num_workers}

    training_generator = DataLoader(train_dataset, **train_params)
    validation_generator = DataLoader(test_dataset, **params_val)

    # CUDA for PyTorch
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # loss
    criterion = nn.CrossEntropyLoss(weight=torch.FloatTensor(class_weights).to(device))

    # Optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    print("starting training.")
    # Loop over epochs
    for epoch in range(epochs):
        print("epoch: {}".format(epoch))
        # Training
        loss_list = []
        model.train()
        for local_batch, local_labels in tqdm(training_generator):
            # bug with dataloader, it doesn't return the right size batch when it runs out of samples
            if not local_labels.shape[0] == train_params['batch_size']:
                continue

            # Transfer to GPU
            local_batch, local_labels = local_batch.to(device), local_labels.to(device).long()

            # Model computations
            outputs = model(local_batch)
            local_labels = local_labels.reshape(train_params['batch_size'], -1)

            loss = criterion(outputs, local_labels)
            optimizer.zero_grad()
            loss.backward()

            # Update weights
            optimizer.step()
            loss_list.append(loss.detach().cpu().numpy())

        # report average loss over epoch
        print("training loss: ", np.mean(loss_list))

        # Validation
        model.eval()
        batch_accuracies = []
        batch_accuracies_iso = []
        batch_loss_val = []
        for local_batch, local_labels in validation_generator:
            # get new batches
            local_batch, local_labels = local_batch.to(device), local_labels.to(device).long()

            # Model computations
            outputs = model(local_batch)

            # calc loss
            loss = criterion(outputs, local_labels.reshape(local_labels.shape[0], -1))
            batch_loss_val.append(loss.detach().cpu().numpy())

            outputs_iso = utils.force_sequential_predictions(outputs, method='isotonic')
            outputs_first = utils.force_sequential_predictions(outputs, method='first')

            # compute accuracy for whole validation set
            flat_output = torch.argmax(outputs, dim=1).cpu().reshape(local_batch.shape[0], 1, -1)
            compare = flat_output == local_labels.cpu()
            acc = np.sum(compare.numpy(), axis=2) / \
                int(local_batch.shape[-1])  # * params_val['batch_size']
            batch_accuracies.append(np.mean(acc, axis=0)[0])

            flat_output = torch.argmax(outputs_iso, dim=1).cpu().reshape(local_batch.shape[0], 1, -1)
            compare = flat_output == local_labels.cpu()
            acc = np.sum(compare.numpy(), axis=2) / \
                int(local_batch.shape[-1])  # * params_val['batch_size']
            batch_accuracies_iso.append(np.mean(acc, axis=0)[0])

        print("validation accuracy: {}".format(np.mean(batch_accuracies)))
        print("validation accuracy isotonic regression: {}".format(np.mean(batch_accuracies_iso)))
        print("validation loss: {}".format(np.mean(batch_loss_val)))
        print("="*50)

    return model
