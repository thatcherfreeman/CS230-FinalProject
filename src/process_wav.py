import argparse

import torch

from args import add_test_args, add_common_args, add_wav_args
from AudioDataUtils import play
import model_utils
import models
import TrumpRemover


def main():
    parser = argparse.ArgumentParser()
    add_test_args(parser)
    add_common_args(parser)
    add_wav_args(parser)
    args = parser.parse_args()

    model = models.get_model(args.model)()
    assert args.load_path is not None, "Did not specify model load path"
    model = model_utils.load_model(model, args.load_path)
    model.eval()

    assert args.input_file is not None, "Did not specify input file!"

    print("Processing file...")
    audio_data = TrumpRemover.process_through_model(args.input_file, args.output_file, model, args)
    play(audio_data)
    print("Done!")

if __name__ == '__main__':
    main()