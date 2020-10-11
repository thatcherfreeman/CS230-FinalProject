# Project Discussion Notes

## Key parts

1. Data collection (download Trump and other folks audio clips as .wav or .mp3)

    - Provided as standard, readable format, ideally something smaller though.
    - Probably only need like a few hours of data

2. Preprocess this data, create synthetic data/audio files, divided into short segments, save as some zipped array

    - Save it as a tensor or numpy pickled thing
    - Need exposed parameters for the following things:
        - STFT window size and overlap
        - Sampling rate (can downsample from 44.1 khz for processing performance)
    - Convert to mono, normalize peaks
        - Technically speaking, in the news they probably normalize to like -23 LUFs when blending rather than normalizing according to peak volume
    - Create blended audio clips (linear sum of peak normalized audio)

3. Create/choose a model architecture
    - Probably use U-Net architecture like others have
4. Train the model on our data, iterate

    - Convert FFTs to audio files

5. Create some "cleaned up" audio clip of the debate that sound believable.
6. Measure Audio Quality of separation on validation set
    - Use something like Mus Eval library [GitHub](https://github.com/sigsep/sigsep-mus-eval)


## Relevant Papers

[Singing Voice Separation with Deep U-Net Convolutional Networks](https://openaccess.city.ac.uk/id/eprint/19289/1/)
- Discusses the use of U-Net networks on voice separation. This might be the most promising architecture in the literature.

[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/pdf/1505.04597.pdf)
- Discusses U-Net architecture in detail

[Singing Voice Separation: A Study on Training Data](https://arxiv.org/pdf/1906.02618.pdf)
- Discusses effect of training data augmentation on the performance of the above U-Net network architecture.

[Audio AI: isolating vocals from stereo music using Convolutional Neural Networks \| by Ale Koretzky | Towards Data Science](https://towardsdatascience.com/audio-ai-isolating-vocals-from-stereo-music-using-convolutional-neural-networks-210532383785)
[Probabilistic Binary-Mask Cocktail-Party Source Separation in a Convolutional Deep Neural Network](https://arxiv.org/ftp/arxiv/papers/1503/1503.06962.pdf) (doesn't really use CONV layers lol)
[Deep Karaoke: Extracting Vocals from Musical Mixtures Using a Convolutional Deep Neural Network](https://arxiv.org/ftp/arxiv/papers/1504/1504.04658.pdf) (parts look low key plaigerised from the previous paper lol)
- Discusses network that essentially tries to mask out vocal portions of the spectrograph.
- Second technique apparently had decent results even with minimal training audio for each voice (two minutes each!), though in ideal circumstances.

[How To Build a Deep Audio De-Noiser Using TensorFlow 2.0 \| by Daitan | Better Programming | Medium](https://medium.com/better-programming/how-to-build-a-deep-audio-de-noiser-using-tensorflow-2-0-79c1c1aea299)
- Discusses Denoising application of neural networks.

[A Fully Convolutional Neural Network for Speech Enhancement](https://arxiv.org/pdf/1609.07132.pdf)
- Discusses some CNN architectures that were useful in denoising audio (noise in the form of chatter)

[Performance measurement in blind audio source separation](https://hal.inria.fr/inria-00544230/document)
- Discusses quality metrics useful in source separation tasks
- Python implementation of MUS-EVAL is here: [GitHub](https://github.com/sigsep/sigsep-mus-eval)


**Reading on STFT:**
[scipy.signal.stft — SciPy v1.5.2 Reference Guide](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.stft.html)
[Short-time Fourier transform - Wikipedia](https://en.wikipedia.org/wiki/Short-time_Fourier_transform)
[Practical Cython— Music Retrieval: Short Time Fourier Transform \| by Stefano Bosisio | Aug, 2020 | Towards Data Science](https://towardsdatascience.com/practical-cython-music-retrieval-short-time-fourier-transform-f89a0e65754d)

**Non-Negative Matrix Factorization** - Generally considered to be a low quality approach, but probably worth mentioning in the "Related Works" section.
[Supervised non-negative matrix factorization for audio source separation](https://vista.cs.technion.ac.il/wp-content/uploads/2018/09/SprBroSapEHA15.pdf)


## Discussion Topics:
- Should we consider limiting the scope of the project to just separation of Biden and Trump? (two known speakers, instead of Trump vs Anyone Else?)
- In the above case, we can use multi-task learning to probably improve performance (remove Biden from Trump, remove Trump from Biden)


**Possible Types of Training Data**:
- Trump + biden clips -> trump audio, biden audio
- Trump + noise -> noise
- biden + noise -> noise

- Make sure to peak normalize audio levels before blending together in linear mode
- Probably convert all audio to mono for simplicity
