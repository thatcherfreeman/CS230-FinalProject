import torch
from torch import nn

class FCModel(nn.Module):
    '''
    Copy of the model from `Deep Karaoke: Extracting Vocals from Musical
    Mixtures Using a Convolutional Deep Neural Network`,
    https://arxiv.org/ftp/arxiv/papers/1504/1504.04658.pdf

    Intended for use on 44.1khz audio samples with window size of 2048 and
    20-sample windows. 20500 comes from 20 * (2048 / 2)
    '''
    def __init__(self, num_features=20500):
        super(FCModel, self).__init__()
        self.num_features = num_features
        self.model = nn.Sequential(
            nn.Linear(num_features, num_features),
            nn.Sigmoid(),
            nn.Linear(num_features, num_features),
            nn.Sigmoid(),
            nn.Linear(num_features, num_features),
            nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        assert len(x.shape) == 3
        assert x.shape[1] * x.shape[2] == self.num_features

        x_flat = torch.reshape(x, (x.shape[0], self.num_features))
        y_flat = self.model(x_flat)
        assert y_flat.shape == x_flat.shape
        y_pred = torch.reshape(y_flat, x.shape)
        return y_pred

