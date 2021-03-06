import argparse
import os
import json


def add_experiment(args: argparse.Namespace) -> None:
    if args.save_path not in os.listdir('.'):
        os.makedirs(args.save_path)
    num_folders = len(os.listdir(args.save_path))
    args.experiment = f'{args.model}_exp{num_folders}'
    if args.name is not None:
        args.experiment += f'_{args.name}'


def save_arguments(args: argparse.Namespace, filename: str) -> None:
    with open(filename, 'w') as f:
        json.dump(args.__dict__, f)


def add_train_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '--learning_rate',
        type=float,
        default=1e-4,
        help='Learning rate for the optimizer',
    )
    parser.add_argument(
        '--train_batch_size',
        type=int,
        default=5,
        help='training mini-batch size',
    )
    parser.add_argument(
        '--val_batch_size',
        type=int,
        default=100,
        help='validation mini-batch size',
    )
    parser.add_argument(
        '--train_epochs',
        type=int,
        default=30,
        help='Number of epochs to train for',
    )
    parser.add_argument(
        '--checkpoint_freq',
        type=int,
        default=5,
        help='Number of epochs between each checkpoint',
    )
    parser.add_argument(
        '--num_checkpoints',
        type=int,
        default=6,
        help='Number of checkpoints to keep'
    )
    parser.add_argument(
        '--weight_decay',
        type=float,
        default=0.0,
        help='regularization strength',
    )
    parser.add_argument(
        '--save_path',
        type=str,
        default='checkpoints',
        help='specify path to save the trained model'
    )
    parser.add_argument(
        '--log_dir',
        type=str,
        default='logs',
        help='Directory to store tensorboard logs',
    )
    parser.add_argument(
        '--use_scheduler',
        action='store_true',
        help='Use this flag to avoid learning rate scheduling.',
    )
    parser.add_argument(
        '--train_trump',
        action='store_true',
        help='Use this flag to train the model to remove biden from audio clips.',
    )


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '--alpha',
        type=float,
        default = 0.85,
        help='Mask threshold (between 0 and 1)',
    )
    parser.add_argument(
        '--model',
        type=str,
        default='UNet',
        help='choose the model to train',
    )
    parser.add_argument(
        '--dataset_dir',
        type=str,
        default='/home/ubuntu/cs230/audio/combined',
        help='path to directory containing .pkl files',
    )
    parser.add_argument(
        '--load_path',
        type=str,
        default=None,
        help='specify path to load the model at the given path before training.'
    )
    parser.add_argument(
        '--name',
        type=str,
        default=None,
        help='Give the model a name that will be a part of the experiment path.',
    )
    parser.add_argument(
        '--dev_frac',
        type=float,
        default=0.1,
        help='Indicates fraction of data to be partitioned into dev set.'
    )
    parser.add_argument(
        '--dataset_cap',
        type=int,
        default=15000,
        help='specifies a limit for the number of samples to have in the dataset.',
    )

def add_wav_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '--input_file',
        type=str,
        default=None,
        help='input wav file to process',
    )
    parser.add_argument(
        '--output_file',
        type=str,
        default='out.wav',
        help='Location to write output processed wav file.'
    )

def add_test_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '--batch_size',
        type=int,
        default=1,
        help='mini-batch size',
    )
    parser.add_argument(
        '--biden_only_sdr',
        action='store_true',
        help='Calculate SDR using only the biden track.',
    )
    parser.add_argument(
        '--nonboolean_mask',
        action='store_true',
        help='Just use mask directly out of model instead of casting to 0 or 1',
    )
