import os
from typing import Tuple, List
import random

import pickle
import numpy as np # type: ignore
import torch
from torch import nn
from tqdm import tqdm # type: ignore

from StftData import StftData
import models


def save_model(model: nn.Module, path: str) -> nn.Module:
    model = model.cpu()
    torch.save(model.state_dict(), path)
    model = model.to(get_device())
    return model


def load_model(model: nn.Module, path: str) -> nn.Module:
    model = model.cpu()
    model.load_state_dict(torch.load(path))
    model = model.to(get_device())
    return model


def get_device() -> torch.device:
    '''
    Guesses the best device for the current machine.
    '''
    return torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


def load_data(
    directory_path: str,
    dev_frac: float = 0.1,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    '''
    Returns data in order of combined_train, biden_train, mask_train, combined_dev, biden_dev, mask_dev
    combined and biden are complex64, but mask_train is float32.
    Note: Train model on x_train.abs() and y_train.abs(), but in practice you need to input
    x_train.abs() and multiply the output by x_train (complex) to get the real prediction.
    Perhaps threshold the output to create a more binary mask.
    '''
    # Open given directory, expecting files with the names
    # biden_%d.pkl, combined_%d.pkl, and trump_%d.pkl

    # Choose file names and deterministically shuffle
    print('Reading datasets...')
    pickled_filenames = os.listdir(directory_path)
    combined_filenames = sorted([fn for fn in pickled_filenames if fn.startswith('combined_')])
    biden_filenames = sorted([fn for fn in pickled_filenames if fn.startswith('biden_')])
    trump_filenames = sorted([fn for fn in pickled_filenames if fn.startswith('trump_')])
    zipped_filenames = list(zip(combined_filenames, biden_filenames, trump_filenames))
    random.Random(230).shuffle(zipped_filenames)

    # Read files as stft data
    num_examples = len(zipped_filenames)
    combined_ls, biden_ls, trump_ls = [], [], []
    masks_ls = []
    with tqdm(total=len(zipped_filenames)) as progress_bar:
        for i, (cd, bd, td) in enumerate(zipped_filenames):
            combined_data = StftData(pickle_file=f'{directory_path}/{cd}')
            biden_data = StftData(pickle_file=f'{directory_path}/{bd}')
            trump_data = StftData(pickle_file=f'{directory_path}/{td}')
            combined_ls.append(combined_data.data)
            # combined_ls.append(trump_data.data)
            # combined_ls.append(biden_data.data)
            biden_ls.append(biden_data.data)
            # biden_ls.append(np.zeros_like(biden_data.data))
            # biden_ls.append(biden_data.data)
            trump_ls.append(trump_data.data)
            # trump_ls.append(trump_data.data)
            # trump_ls.append(np.zeros_like(trump_data.data))
            biden_mag = np.abs(biden_data.data)
            trump_mag = np.abs(trump_data.data)
            masks_ls.append(np.ones_like(biden_mag, dtype=np.float32) * (biden_mag > trump_mag))
            # masks_ls.append(np.zeros_like(trump_mag, dtype=np.float32))
            # masks_ls.append(np.ones_like(biden_mag, dtype=np.float32))
            progress_bar.update()

    # Reformat arrays
    combined = _convert_to_tensor(combined_ls, torch.complex64)
    biden = _convert_to_tensor(biden_ls, torch.complex64)
    trump = _convert_to_tensor(trump_ls, torch.complex64)
    masks = _convert_to_tensor(masks_ls, torch.float32)

    # Partition into train and dev
    print('  Done!')
    num_examples = len(combined)
    dev_idx = num_examples - int(num_examples * dev_frac)
    return (
        combined[:dev_idx],
        biden[:dev_idx],
        trump[:dev_idx],
        masks[:dev_idx],
        combined[dev_idx:],
        biden[dev_idx:],
        trump[dev_idx:],
        masks[dev_idx:],
    )


def load_test_data(
    directory_path: str,
    dev_frac: float = 0.1,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, StftData]:
    '''
    Returns data in order of combined_train, biden_train, mask_train, combined_dev, biden_dev, mask_dev
    combined and biden are complex64, but mask_train is float32.
    Note: Train model on x_train.abs() and y_train.abs(), but in practice you need to input
    x_train.abs() and multiply the output by x_train (complex) to get the real prediction.
    Perhaps threshold the output to create a more binary mask.
    '''
    # Open given directory, expecting files with the names
    # biden_%d.pkl, combined_%d.pkl, and trump_%d.pkl

    # Choose file names and deterministically shuffle
    print('Reading datasets...')
    pickled_filenames = os.listdir(directory_path)
    combined_filenames = sorted([fn for fn in pickled_filenames if fn.startswith('combined_')])
    biden_filenames = sorted([fn for fn in pickled_filenames if fn.startswith('biden_')])
    trump_filenames = sorted([fn for fn in pickled_filenames if fn.startswith('trump_')])
    zipped_filenames = list(zip(combined_filenames, biden_filenames, trump_filenames))
    random.Random(230).shuffle(zipped_filenames)

    # Only load dev examples
    num_examples = len(zipped_filenames)
    dev_idx = num_examples - int(num_examples * dev_frac)
    zipped_filenames = zipped_filenames[dev_idx:]

    # Need combined as STFT data (for network input) and inverted biden
    combined_ls, biden_samples_ls, trump_samples_ls, biden_ls = [], [], [], []
    with tqdm(total=len(zipped_filenames)) as progress_bar:
        for i, (cd, bd, td) in enumerate(zipped_filenames):
            combined_data = StftData(pickle_file=f'{directory_path}/{cd}')
            biden_data = StftData(pickle_file=f'{directory_path}/{bd}')
            trump_data = StftData(pickle_file=f'{directory_path}/{td}')
            combined_ls.append(combined_data.data)
            biden_ls.append(biden_data.data)
            biden_time_amplitude = biden_data.invert().time_amplitudes
            trump_time_amplitude = trump_data.invert().time_amplitudes
            biden_samples_ls.append(biden_time_amplitude)
            trump_samples_ls.append(trump_time_amplitude)
            progress_bar.update()

    # Reformat arrays
    combined = _convert_to_tensor(combined_ls, torch.complex64)
    biden = _convert_to_tensor(biden_ls, torch.complex64)
    biden_samples = np.expand_dims(np.asarray(biden_samples_ls), axis=2)
    trump_samples = np.expand_dims(np.asarray(trump_samples_ls), axis=2)
    gt_samples = torch.tensor(np.stack([biden_samples, trump_samples], axis=1)) # Shape 2, time_samples, 1

    print('  Done!')

    return (
        combined,
        biden,
        gt_samples,
        biden_data,
    )

def invert_batch_like(batch: np.ndarray, container: StftData) -> np.ndarray:
    '''
    Takes in batch of shape (m, nsrc, 1, H, W), returns ndarray of shape (m * nsrc, time_samples, 1),
    containing the inverse STFT of the H,W images in batch.
    '''
    # Assume batch is shape (m, nsrc, 1, H, W)
    m, nsrc, _, _, _= batch.shape
    batch_small = np.squeeze(batch, axis=2)
    output = []
    for i in range(m):
        for j in range(nsrc):
            container.data = batch[i, j, :, :]
            audio = container.invert()
            output.append(audio.time_amplitudes)
    output = np.array(output)
    time_samples = output.shape[2]
    output = np.reshape(output, (m * nsrc, time_samples, 1))
    # output = np.expand_dims(np.concatenate(output, axis=0),3) # (m, nsrc, time_samples, 1)
    return output


def _convert_to_tensor(x: List[np.ndarray], dtype: torch.dtype) -> torch.Tensor:
    '''
    x is a list of ndarrays of shape H, W, output torch tensor of dimension m, 1, H, W
    of type dtype
    '''
    out = np.stack(x, axis=0)
    out = np.expand_dims(out, axis=1)
    return torch.tensor(out, dtype=dtype)

def l1_norm_loss(input: torch.Tensor, pos_target: torch.Tensor) -> torch.Tensor:
    return torch.mean(torch.abs(input - pos_target))

def l2_norm_loss(input: torch.Tensor, pos_target: torch.Tensor) -> torch.Tensor:
    return torch.mean(torch.pow(input - pos_target, 2))

def danny_loss(input: torch.Tensor, pos_target: torch.Tensor) -> torch.Tensor:
    return -2 * torch.mean(input * pos_target) + torch.mean(input * input)

def l1_norm_triplet_loss(input: torch.Tensor, pos_target: torch.Tensor, neg_target: torch.Tensor) -> torch.Tensor:
    return torch.mean(torch.abs(input - pos_target) - torch.abs(input - neg_target)) + 1

def verify_versions() -> None:
    # Version 1.5.0 has a bug where certain type annotations don't pass typecheck
    assert torch.__version__ == '1.6.0', 'Incorrect torch version installed!'

def combine_unets(f1: str, f2: str, fout: str) -> models.DoubleUNet:
    net1 = models.UNet()
    net2 = models.UNet()
    net1 = load_model(net1, f1)
    net2 = load_model(net2, f2)
    dnet = models.DoubleUNet()
    dnet.net_b = net1
    dnet.net_t = net2
    save_model(dnet, fout)
