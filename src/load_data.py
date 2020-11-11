import os
from AudioDataUtils import AudioData, downsample, cut_into_snippets
from DataPrep import create_data_for_model

NEW_TRUMP_DIR = "./tmp/trump"
NEW_BIDEN_DIR = "./tmp/biden"
OLD_TRUMP_DIR = "./tmp/pre_milestone/trump"
OLD_BIDEN_DIR = "./tmp/pre_milestone/biden"

def snippet_generator(wav: str, dir: str):
    ad = AudioData(os.path.join(dir, "full", wav))
    downsampled = downsample(ad, 3)
    cut_into_snippets(downsampled, os.path.join(dir, "snippet"), 4500, 0.7)


for wav in os.listdir(os.path.join(NEW_TRUMP_DIR, "full")):
    snippet_generator(wav, NEW_TRUMP_DIR)

for wav in os.listdir(os.path.join(NEW_BIDEN_DIR, "full")):
    snippet_generator(wav, NEW_BIDEN_DIR)

for wav in os.listdir(os.path.join(OLD_TRUMP_DIR, "full")):
    snippet_generator(wav, OLD_TRUMP_DIR)

for wav in os.listdir(os.path.join(OLD_BIDEN_DIR, "full")):
    snippet_generator(wav, OLD_BIDEN_DIR)


# new biden x new trump
create_data_for_model(
    "./audio/new_biden_x_new_trump",
    "./tmp/trump/snippet",
    "./tmp/biden/snippet",
    source1_name="trump",
    source2_name="biden"
)

# new biden x old trump
create_data_for_model(
    "./audio/new_biden_x_old_trump",
    "./tmp/trump/snippet",
    "./tmp/pre_milestone/biden/snippet",
    source1_name="trump",
    source2_name="biden"
)

# old biden x old trump
create_data_for_model(
    "./audio/old_biden_x_old_trump",
    "./tmp/pre_milestone/trump/snippet",
    "./tmp/pre_milestone/biden/snippet",
    source1_name="trump",
    source2_name="biden"
)

# old biden x new trump
create_data_for_model(
    "./audio/old_biden_x_new_trump",
    "./tmp/trump/snippet",
    "./tmp/pre_milestone/biden/snippet",
    source1_name="trump",
    source2_name="biden"
)

