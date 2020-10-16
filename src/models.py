import torch
from torch import nn
from typing import Tuple, Optional

class FCModel(nn.Module):
    '''
    Copy of the model from `Deep Karaoke: Extracting Vocals from Musical
    Mixtures Using a Convolutional Deep Neural Network`,
    https://arxiv.org/ftp/arxiv/papers/1504/1504.04658.pdf

    Intended for use on 44.1khz audio samples with window size of 2048 and
    20-sample windows. 20500 comes from 20 * (2048 / 2)
    '''
    def __init__(self, num_features=512*128):
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
        assert len(x.shape) == 4
        assert x.shape[2] * x.shape[3] == self.num_features

        x_flat = torch.reshape(x, (x.shape[0], self.num_features))
        y_flat = self.model(x_flat)
        assert y_flat.shape == x_flat.shape
        y_pred = torch.reshape(y_flat, x.shape)
        return y_pred


class Encoder(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        ksize: int = 5,
        kstride: int = 2,
    ):
        super(Encoder, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels

        self.conv1 = nn.Conv2d(
            in_channels,
            out_channels,
            kernel_size=ksize,
            stride=kstride,
            padding=(ksize-1)//2,
            padding_mode='replicate',
        )
        self.relu1 = nn.LeakyReLU(0.2)
        # self.pool = nn.MaxPool2d(2)

    def forward(self, x: torch.Tensor) -> torch.Tensor: #-> Tuple[torch.Tensor, torch.Tensor]:
        n, c, h, w = x.shape
        assert c == self.in_channels
        out = self.conv1(x)
        out = self.relu1(out)
        return out
        # out_small = self.pool(out)
        # return out_small, out


class Decoder(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        dropout_p: float,
        up_ksize: int = 5,
        up_kstride: int = 2,
        ksize: int = 3,
        kstride: int = 1,
    ):
        super(Decoder, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels

        self.upres = nn.ConvTranspose2d(
            in_channels,
            out_channels,
            kernel_size=up_ksize,
            stride=up_kstride,
            padding=(up_ksize-1)//2,
            output_padding=1,
            )
        self.conv1 = nn.Conv2d(
            out_channels * 2,
            out_channels,
            kernel_size=ksize,
            stride=kstride,
            padding=(ksize-1)//2,
            padding_mode='replicate'
        )
        self.relu1 = nn.ReLU()
        self.dropout = nn.Dropout(dropout_p)

    def forward(self, x_small: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
        n_small, c_small, h_small, w_small = x_small.shape
        assert c_small == self.in_channels
        x_big = self.upres(x_small)
        assert x_big.shape == x.shape
        x_cat = torch.cat([x_big, x], dim=1)
        out = self.conv1(x_cat)
        out = self.relu1(out)
        out = self.dropout(out)
        return out


class ResidualDecoder(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        dropout_p: float,
        up_ksize: int = 5,
        up_kstride: int = 2,
        ksize: int = 3,
        kstride: int = 1,
    ):
        super(ResidualDecoder, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels

        self.upres = nn.ConvTranspose2d(
            in_channels,
            out_channels,
            kernel_size=up_ksize,
            stride=up_kstride,
            padding=(up_ksize-1)//2,
            output_padding=1,
        )
        self.conv1 = nn.Conv2d(
            out_channels,
            out_channels,
            kernel_size=ksize,
            stride=kstride,
            padding=(ksize-1)//2,
            padding_mode='replicate'
        )
        self.relu1 = nn.ReLU()
        self.dropout = nn.Dropout(dropout_p)

    def forward(self, x_small: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
        n_small, c_small, h_small, w_small = x_small.shape
        assert c_small == self.in_channels
        x_big = self.upres(x_small)
        assert x_big.shape == x.shape
        out = self.conv1(x_big)
        out = out + x # Residual connection
        out = self.relu1(out)
        out = self.dropout(out)
        return out


class UNet(nn.Module):
    def __init__(self, num_features: Optional[int] = None, drop_p: float = 0.5):
        super(UNet, self).__init__()
        layer_channels = [1, 16, 32, 64, 128, 256 , 512]

        self.encoder1 = Encoder(1, 16)
        self.encoder2 = Encoder(16, 32)
        self.encoder3 = Encoder(32, 64)
        self.encoder4 = Encoder(64, 128)
        self.encoder5 = Encoder(128, 256)
        self.encoder6 = Encoder(256, 512)

        self.decoder6 = Decoder(512, 256, drop_p)
        self.decoder5 = Decoder(256, 128, drop_p)
        self.decoder4 = Decoder(128, 64, drop_p)
        self.decoder3 = Decoder(64, 32, 0)
        self.decoder2 = Decoder(32, 16, 0)
        self.decoder1 = Decoder(16, 1, 0) # A little questionable, maybe should be conv layer

        self.sigmoid = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        assert len(x.shape) == 4
        e_out1 = self.encoder1(x)
        e_out2 = self.encoder2(e_out1)
        e_out3 = self.encoder3(e_out2)
        e_out4 = self.encoder4(e_out3)
        e_out5 = self.encoder5(e_out4)
        e_out6 = self.encoder6(e_out5)

        d_out5 = self.decoder6(e_out6, e_out5)
        d_out4 = self.decoder5(d_out5, e_out4)
        d_out3 = self.decoder4(d_out4, e_out3)
        d_out2 = self.decoder3(d_out3, e_out2)
        d_out1 = self.decoder2(d_out2, e_out1)
        out    = self.decoder1(d_out1, x) # Not sure on this part lol

        out = self.sigmoid(out)
        return out

class ResidualUNet(nn.Module):
    def __init__(self, num_features: Optional[int] = None, drop_p: float = 0.5):
        super(ResidualUNet, self).__init__()
        layer_channels = [1, 16, 32, 64, 128, 256 , 512]

        self.encoder1 = Encoder(1, 16)
        self.encoder2 = Encoder(16, 32)
        self.encoder3 = Encoder(32, 64)
        self.encoder4 = Encoder(64, 128)
        self.encoder5 = Encoder(128, 256)
        self.encoder6 = Encoder(256, 512)

        self.decoder6 = ResidualDecoder(512, 256, drop_p)
        self.decoder5 = ResidualDecoder(256, 128, drop_p)
        self.decoder4 = ResidualDecoder(128, 64, drop_p)
        self.decoder3 = ResidualDecoder(64, 32, 0)
        self.decoder2 = ResidualDecoder(32, 16, 0)
        self.decoder1 = ResidualDecoder(16, 1, 0) # A little questionable, maybe should be conv layer

        self.sigmoid = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        assert len(x.shape) == 4
        e_out1 = self.encoder1(x)
        e_out2 = self.encoder2(e_out1)
        e_out3 = self.encoder3(e_out2)
        e_out4 = self.encoder4(e_out3)
        e_out5 = self.encoder5(e_out4)
        e_out6 = self.encoder6(e_out5)

        d_out5 = self.decoder6(e_out6, e_out5)
        d_out4 = self.decoder5(d_out5, e_out4)
        d_out3 = self.decoder4(d_out4, e_out3)
        d_out2 = self.decoder3(d_out3, e_out2)
        d_out1 = self.decoder2(d_out2, e_out1)
        out    = self.decoder1(d_out1, x) # Not sure on this part lol

        out = self.sigmoid(out)
        return out


def get_model(model_name: str) -> type:
    models = [FCModel, UNet, ResidualUNet]
    for m in models:
        if m.__name__ == model_name:
            return m
    assert False, f'Could not find model {model_name}!'
