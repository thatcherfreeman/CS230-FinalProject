import argparse
import os

def add_experiment(args: argparse.Namespace) -> None:
    if args.save_path not in os.listdir('.'):
        os.makedirs(args.save_path)
    num_folders = len(os.listdir(args.save_path))
    args.experiment = f'{args.model}_exp{num_folders}'

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
        default=1,
        help='training mini-batch size',
    )
    parser.add_argument(
        '--val_batch_size',
        type=int,
        default=1,
        help='validation mini-batch size',
    )
    parser.add_argument(
        '--train_epochs',
        type=int,
        default=100,
        help='Number of epochs to train for',
    )
    parser.add_argument(
        '--checkpoint_freq',
        type=int,
        default=10,
        help='Number of epochs between each checkpoint',
    )
    parser.add_argument(
        '--num_checkpoints',
        type=int,
        default=5,
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
        '--load_path',
        type=str,
        default=None,
        help='specify path to load the model at the given path before training.'
    )
    parser.add_argument(
        '--log_dir',
        type=str,
        default='logs',
        help='Directory to store tensorboard logs'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='UNet'
    )
