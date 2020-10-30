import argparse
import os

import bsseval
import numpy as np
import torch
from torch import nn
from torch import optim
from torch.utils import data
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm # type: ignore

from args import add_test_args
import models
import model_utils
from StftData import StftData
from AudioDataUtils import AudioData, play


def test_model(
    dev_dl: data.DataLoader,
    model: nn.Module,
    args: argparse.Namespace,
    stft_container: StftData,
) -> nn.Module:

    device = model_utils.get_device()
    loss_fn = model_utils.l1_norm_loss

    print('Running test metrics...')

    # Validation portion


    ground_truths = []
    model_outputs = []

    # Forward inference on model
    predicted_masks = []
    print('\n  Running forward inference...')
    with tqdm(total=args.batch_size * len(dev_dl)) as progress_bar:
        for i, (x_batch, y_batch, ground_truth) in enumerate(dev_dl):
            x_batch = x_batch.abs().to(device)
            y_batch = y_batch.abs().to(device)

            # Forward pass on model
            # y_pred = model(torch.clamp_min(torch.log(x_batch), 0))

            y_pred = model(x_batch)
            y_pred_mask = torch.ones_like(y_pred) * (y_pred > args.alpha)
            predicted_masks.append(y_pred_mask.cpu())

            progress_bar.update(len(x_batch))

            del x_batch
            del y_batch
            del y_pred


    print('\n  Processing results...')
    SDR, ISR, SIR, SAR = [], [], [], []
    with tqdm(total=args.batch_size * len(dev_dl)) as progress_bar:
        for i, ((x_batch, _, ground_truth), y_pred_mask) in enumerate(zip(dev_dl, predicted_masks)):
            stft_audio = y_pred_mask * x_batch

            # Calculate other stats
            model_stft = stft_audio.cpu().numpy()
            stft_container.data = stft_audio.numpy()
            model_audio = model_utils.invert_batch_like(model_stft, stft_container)
            ground_truths.append(ground_truth.numpy())
            model_outputs.append(model_audio)

            batch_sdr, batch_isr, batch_sir, batch_sar = bsseval.evaluate(
                ground_truth,
                model_audio,
                win=stft_container.fs,
                hop=stft_container.fs,
            )

            SDR = np.concatenate([SDR, np.mean(batch_sdr, axis=1)], axis=0)
            ISR = np.concatenate([ISR, np.mean(batch_isr, axis=1)], axis=0)
            SIR = np.concatenate([SIR, np.mean(batch_sir, axis=1)], axis=0)
            SAR = np.concatenate([SAR, np.mean(batch_sar, axis=1)], axis=0)

            progress_bar.update(len(x_batch))

    print(f'\n  Calculating overall metrics...')
    # model_outputs = np.concatenate(model_outputs, axis=0)
    # ground_truths = np.concatenate(ground_truths, axis=0)

    print()
    print('*' * 30)
    print(f'SDR: {np.mean(SDR)}')
    print(f'ISR: {np.mean(ISR)}')
    print(f'SIR: {np.mean(SIR)}')
    print(f'SAR: {np.mean(SAR)}')
    print('*' * 30)

    # for i in range(ground_truths.shape[0]):
    #     audio = AudioData(manual_init=[stft_container.fs, ground_truths[i, :, 0]])
    #     audio2 = AudioData(manual_init=[stft_container.fs, model_outputs[i, :, 0]])
    #     play(audio)
    #     play(audio2)

    return model


def main():
    parser = argparse.ArgumentParser()
    add_test_args(parser)
    args = parser.parse_args()

    device = model_utils.get_device()

    # Load dataset from disk
    x_dev, y_dev, ground_truths, container = model_utils.load_test_data(args.dataset_dir, dev_frac=0.1)
    dev_dl = data.DataLoader(
        data.TensorDataset(x_dev, y_dev, ground_truths),
        batch_size=args.batch_size,
        shuffle=False,
    )

    # Initialize a model
    model = models.get_model(args.model)()

    # load from checkpoint if path specified
    assert args.load_path is not None
    model = model_utils.load_model(model, args.load_path)
    model.eval()

    # Move model to GPU if necessary
    model.to(device)

    # test!
    test_model(
        dev_dl,
        model,
        args,
        container,
    )


if __name__ == '__main__':
    model_utils.verify_versions()
    main()


