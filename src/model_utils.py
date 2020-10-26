import os
from typing import Tuple, List
import random

import pickle
import numpy as np # type: ignore
import torch
from torch import nn

from StftData import StftData


def save_model(model: nn.Module, path: str) -> nn.Module:
    model.cpu()
    torch.save(model.state_dict(), path)
    model.to(get_device())
    return model


def load_model(model: nn.Module, path: str) -> nn.Module:
    model.cpu()
    model.load_state_dict(torch.load(path))
    model.to(get_device())
    return model


def get_device() -> torch.device:
    '''
    Guesses the best device for the current machine.
    '''
    return torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


def load_data(
    directory_path: str,
    pickle_filename: str = 'datset.pkl',
    dev_frac: float = 0.1,
    reload: bool = False,
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
    # if reload:
    print("Reading datasets...")
    pickled_filenames = os.listdir(directory_path)
    combined_filenames = sorted([fn for fn in pickled_filenames if fn.startswith('combined_')])
    biden_filenames = sorted([fn for fn in pickled_filenames if fn.startswith('biden_')])
    trump_filenames = sorted([fn for fn in pickled_filenames if fn.startswith('trump_')])
    zipped_filenames = list(zip(combined_filenames, biden_filenames, trump_filenames))
    random.Random(230).shuffle(zipped_filenames)

    # Read files as stft data
    num_examples = len(zipped_filenames)
    combined_ls, biden_ls = [], []
    masks_ls = []
    for i, (cd, bd, td) in enumerate(zipped_filenames):
        if i % 2000 == 0:
            print(f"  Reading example {i} / {num_examples}...")
        combined_data = StftData(pickle_file=f'{directory_path}/{cd}')
        biden_data = StftData(pickle_file=f'{directory_path}/{bd}')
        trump_data = StftData(pickle_file=f'{directory_path}/{td}')
        combined_ls.append(combined_data.data)
        biden_ls.append(biden_data.data)
        biden_mag = np.abs(biden_data.data)
        trump_mag = np.abs(trump_data.data)
        masks_ls.append(np.ones_like(biden_mag, dtype=np.float32) * (biden_mag > trump_mag))

    #     with open(f'{directory_path}/{pickle_filename}', 'wb') as file:
    #         pickle.dump((combined_ls, biden_ls, masks_ls, num_examples), file, -1)

    # else:
    #     # not reload
    #     print("Loading pre-baked dataset...")
    #     with open(f'{directory_path}/{pickle_filename}', 'rb') as file:
    #         combined_ls, biden_ls, masks_ls, num_examples = pickle.load(file)


    # Reformat arrays
    combined = _convert_to_tensor(combined_ls, torch.complex64)
    biden = _convert_to_tensor(biden_ls, torch.complex64)
    masks = _convert_to_tensor(masks_ls, torch.float32)

    # Partition into train and dev
    print("  Done!")
    dev_idx = num_examples - int(num_examples * dev_frac + 1)
    return (
        combined[:dev_idx],
        biden[:dev_idx],
        masks[:dev_idx],
        combined[dev_idx:],
        biden[dev_idx:],
        masks[dev_idx:],
    )


def _convert_to_tensor(x: List[np.ndarray], dtype: torch.dtype) -> torch.Tensor:
    '''
    x is a list of ndarrays of shape H, W, output torch tensor of dimension m, 1, H, W
    of type dtype
    '''
    out = np.stack(x, axis=0)
    out = np.expand_dims(out, axis=1)
    return torch.tensor(out, dtype=dtype)

def l1_norm_loss(input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    return torch.mean(torch.abs(input - target))

def verify_versions() -> None:
    # Version 1.5.0 has a bug where certain type annotations don't pass typecheck
    assert torch.__version__ == '1.6.0', 'Incorrect torch version installed!'
