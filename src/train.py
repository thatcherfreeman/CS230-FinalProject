import argparse
import os

import torch
from torch import nn
from torch import optim
from torch.utils import data
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm # type: ignore

from args import add_train_args, add_experiment
import models
import model_utils


def train_model(
    train_dl: data.DataLoader,
    dev_dl: data.DataLoader,
    model: nn.Module,
    optimizer: optim.Optimizer,
    args: argparse.Namespace,
) -> nn.Module:

    device = model_utils.get_device()
    loss_fn = nn.functional.binary_cross_entropy
    best_val_loss = torch.tensor(float('inf'))
    saved_checkpoints = []
    writer = SummaryWriter(log_dir=f'{args.log_dir}/{args.experiment}')

    for e in range(1, args.train_epochs + 1):
        print(f'Training epoch {e}...')

        # Training portion
        with tqdm(total=args.train_batch_size * len(train_dl)) as progress_bar:
            model.train()
            for i, (x_batch, y_batch) in enumerate(train_dl):
                # Forward pass on model
                optimizer.zero_grad()
                y_pred = model(x_batch)
                loss = loss_fn(y_pred, y_batch)

                # Backward pass and optimization
                loss.backward()
                optimizer.step()

                progress_bar.update(len(x_batch))
                progress_bar.set_postfix(loss=loss.item())
                writer.add_scalar("Loss/train", loss, e * len(train_dl) + i)

        # Validation portion
        with tqdm(total=args.val_batch_size * len(dev_dl)) as progress_bar:
            model.eval()
            val_loss = torch.tensor(0.0).to(device)
            num_batches_processed = 0
            for i, (x_batch, y_batch) in enumerate(dev_dl):
                # Forward pass on model
                y_pred = model(x_batch)
                loss = loss_fn(y_pred, y_batch)

                val_loss += loss
                num_batches_processed += 1

                progress_bar.update(len(x_batch))
                progress_bar.set_postfix(val_loss=val_loss.item() / num_batches_processed)
                writer.add_scalar("Loss/val", loss, e * len(train_dl) + i)

            # Save model if it's the best one yet.
            if val_loss / num_batches_processed < best_val_loss:
                best_val_loss = val_loss / num_batches_processed
                filename = f'{args.save_path}/{args.experiment}/{model.__class__.__name__}_best_val.checkpoint'
                model_utils.save_model(model, filename)
                print(f'Model saved!')
                print(f'Best validation loss yet: {best_val_loss}')
            # Save model on checkpoints.
            if e % args.checkpoint_freq == 0:
                filename = f'{args.save_path}/{args.experiment}/{model.__class__.__name__}_epoch_{e}.checkpoint'
                model_utils.save_model(model, filename)
                print(f'Model checkpoint reached!')
                saved_checkpoints.append(filename)
                # Delete checkpoints if there are too many
                while len(saved_checkpoints) > args.num_checkpoints:
                    os.remove(saved_checkpoints.pop(0))

    return model


def main():
    parser = argparse.ArgumentParser()
    add_train_args(parser)
    args = parser.parse_args()
    add_experiment(args)
    device = model_utils.get_device()
    os.makedirs(f'{args.save_path}/{args.experiment}')

    # Load datasets somehow, replace this with real data, put train/val data on `device` for all of training.
    train_n = 10
    x_train = torch.rand((train_n, 100, 20)).to(device)
    y_train = torch.rand((train_n, 100, 20)).to(device)
    val_n = 2
    x_dev = torch.rand((val_n, 100, 20)).to(device)
    y_dev = torch.rand((val_n, 100, 20)).to(device)
    train_dl = data.DataLoader(data.TensorDataset(x_train, y_train), batch_size=args.train_batch_size, shuffle=True)
    dev_dl = data.DataLoader(data.TensorDataset(x_dev, y_dev), batch_size=args.val_batch_size, shuffle=False)

    # Initialize a model
    model = models.get_model(args.model)(num_features=2000)

    # load from checkpoint if path specified
    if args.load_path is not None:
        model = model_utils.load_model(model, args.load_path)

    # Move model to GPU if necessary
    model.to(device)

    # Initialize optimizer
    optimizer = optim.Adam(
        model.parameters(),
        lr=args.learning_rate,
        weight_decay=args.weight_decay,
    )

    # Train!
    trained_model = train_model(
        train_dl,
        dev_dl,
        model,
        optimizer,
        args,
    )

    # Save trained model
    filename = f'{args.save_path}/{args.experiment}/{model.__class__.__name__}_trained.checkpoint'
    model_utils.save_model(trained_model, filename)


if __name__ == '__main__':
    model_utils.verify_versions()
    main()
