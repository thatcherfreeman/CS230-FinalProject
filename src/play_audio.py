import argparse

import torch

from args import *
import models
from StftData import *
import model_utils
from AudioDataUtils import *


def main():
    parser = argparse.ArgumentParser()
    add_test_args(parser)
    add_common_args(parser)
    args = parser.parse_args()

    x_train, y_train_biden, y_train_trump, mask_train, x_dev, y_dev_biden, y_dev_trump, mask_dev, container = model_utils.load_data(args.dataset_dir, dev_frac=args.dev_frac, max_entries=args.dataset_cap)

    model = model_utils.load_model(models.get_model(args.model)(), args.load_path)
    model.eval()

    # Change this line to hear other kinds of samples.
    dataset = x_train

    for i in range(dataset.shape[0]):
        print(f"Playing Combined {i}...")
        container.data = dataset[i, 0].numpy()
        play(container.invert())

        y_b, y_t = model(dataset[i:i+1].abs())
        container.data = (torch.clamp(y_b / dataset[i:i+1].abs(), 0, 1) * dataset[i:i+1]).detach().numpy()[0,0]
        print(f"Playing model output {i}...")
        play(container.invert())


if __name__ == "__main__":
    main()