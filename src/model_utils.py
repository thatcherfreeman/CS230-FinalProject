import torch
from torch import nn


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


def verify_versions() -> None:
    # Version 1.5.0 has a bug where certain type annotations don't pass typecheck
    assert torch.__version__ == '1.6.0', 'Incorrect torch version installed!'
