import os
from typing import List, Set, Tuple, Any, Optional
import random

import AudioDataUtils
from AudioDataUtils import AudioData
from StftData import StftArgs, StftData

MAX_COLLISIONS_BEFORE_FAILURE = 10
DESIRED_NUM_STFT_WINDOWS = 128


"""Returns unique pairs of elements from 2 lists. The number of pairs you want is assumed to be significantly less than the total number possible."""
class PairGenerator:
    list1: List[Any]
    list2: List[Any]

    # Use this data structure to track pairs of audio we've already seen, we don't want duplicate examples
    seen_pairs: Set[Tuple[int, int]]
    step_size: int
    prev_pair: Optional[Tuple[int, int]]

    def __init__(self, list1: List[Any], list2: List[Any]):
        self.list1 = list1
        self.list2 = list2
        self.seen_pairs = set()
        self.step_size = 1
        self.prev_pair = None

    def get_pair(self) -> Tuple[Any, Any]:
        if self.prev_pair is None:
            self.prev_pair = (0,0)
            return self._fetch_elements(self.prev_pair)

        found_new_pair = False
        next_idx1, next_idx2 = self.prev_pair
        num_collisions = 0
        while not found_new_pair:
            idx1, idx2 = next_idx1, next_idx2
            next_idx1 = (idx1 + 1)%len(self.list1)
            if next_idx1 == self.step_size:
                self.step_size += 1
                next_idx1 += self.step_size
            next_idx2 = (idx2 + 1)%len(self.list2)
            if (next_idx1, next_idx2) not in self.seen_pairs:
                found_new_pair = True
                self.seen_pairs.add((next_idx1, next_idx2))
            else:
                num_collisions += 1
                if num_collisions >= MAX_COLLISIONS_BEFORE_FAILURE:
                    raise ValueError("stopping pair generation, too many collisions")
        self.prev_pair = (next_idx1, next_idx2)
        return self._fetch_elements((next_idx1, next_idx2))

    def _fetch_elements(self, indices: Tuple[int, int]) -> Tuple[Any, Any]:
        return self.list1[indices[0]], self.list2[indices[1]]

# Creates many pkl files in a specified directory. Files come in pairs of 3, the pickled stft data of the first source,
# the pickled stft data of the second source, and the pickled stft data of their superposition. Triplets will all have the
# same number in their name. For example, "source1_0.pkl", "source2_0.pkl", "combined_0.pkl" are from the same triplet.
# Once unpickled, appropriate-dimensional data (e.g., 512x128) can be found in the 'data' field of the StftData object.
# input pkl files are read from the specified directories, source1_dir and source2_dir. Each directory is expected to contain
# only pkl files corresponding to its category. Use "AudioDataUtils.cut_into_snippets()" to populate such directories.
# WARNING: reads all audio data into RAM at the same time
def create_data_for_model(target_dir: str, source1_dir: str, source2_dir: str,
                          source1_name: str = "source1", source2_name: str = "source2",
                          num_examples_to_create: int = 15000):
    if num_examples_to_create > 50000:
        raise ValueError("Let's not brick the VM. If you really want to create this many examples, edit the code to allow it.")

    # desired frequency outputs are 512x128.
    args: StftArgs = StftArgs(nperseg=1022, noverlap=511)
    source1_snippets = load_snippets(source1_dir)
    source2_snippets = load_snippets(source2_dir)

    if num_examples_to_create > len(source1_snippets) * len(source2_snippets):
        print("There aren't enough unique combinations to create {} unique examples! Falling back to only creating {} examples instead."
              .format(num_examples_to_create, len(source1_snippets) * len(source2_snippets)))
        num_examples_to_create = len(source1_snippets) * len(source2_snippets)

    random.shuffle(source1_snippets)
    random.shuffle(source2_snippets)

    pairgen: PairGenerator = PairGenerator(source1_snippets, source2_snippets)
    example_num = 0
    while example_num < num_examples_to_create:
        if example_num%100 == 0:
            print("Processing example #{}".format(example_num))
        audio1, audio2 = pairgen.get_pair()
        superimposed, audio1, audio2 = AudioDataUtils.superimpose(audio1, audio2)

        freqdata1 = trim_stft_data(StftData(args=args, audiodata=audio1))
        freqdata2 = trim_stft_data(StftData(args=args, audiodata=audio2))
        freqdata_super = trim_stft_data(StftData(args=args, audiodata=superimposed))

        file_prefix = target_dir + "/"
        freqdata1.save(file_prefix + source1_name + "_{}.pkl".format(example_num))
        freqdata2.save(file_prefix + source2_name + "_{}.pkl".format(example_num))
        freqdata_super.save(file_prefix + "combined_{}.pkl".format(example_num))
        example_num += 1


def load_snippets(source_dir: str) -> List[AudioData]:
    data_list = list()
    for filename in os.listdir(source_dir):
        if filename[-4:] == ".pkl":
            data_list.append(AudioData(pickled_filepath=source_dir + "/" + filename))
    return data_list


# modifies the param StftData object
def trim_stft_data(freq_data: StftData) -> StftData:
    freq_data.segment_times = freq_data.segment_times[0:DESIRED_NUM_STFT_WINDOWS]
    freq_data.data = freq_data.data[:, 0:DESIRED_NUM_STFT_WINDOWS]
    return freq_data
