# Brain-kinematics-decoder
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/RyotaroNumata/Brain-kinematics-decoder/blob/master/LICENSE) <br>
A simple brain decoder for kinematic infomation decoding analysis.

## Demo
Decoding finger flextion movement from ECoG signals.<br>
The BCI competion Ⅳ dataset is used for this Demo. 

![Brain-kinematics-decoder](https://user-images.githubusercontent.com/60598478/74128402-70010180-4c20-11ea-825c-846e36d016f9.gif)

## Major features
- GUI support<br>
Brain-kinematics-decoder has simple GUI for analysis.<br>
So, you can easy to start Decoding analysis.

## Installation
### Requirements
- Linux and Windows (MacOS X is not officially supported)
- Python 3.7

## Getting Start
a. Create a conda virtual environment and activate it.

```shell
conda create -n BrainDecoder python=3.7 anaconda
conda activate BrainDecoder
```

b. Install MNE-Python following the [official instructions](https://anaconda.org/conda-forge/mne), e.g.,

```shell
conda install -c conda-forge mne
```

c. Clone the Brain-kinematics-decoder repository.

```shell
git clone https://github.com/RyotaroNumata/Brain-kinematics-decoder.git
cd Brain-kinematics-decoder
```

## Licence

[MIT](https://github.com/RyotaroNumata/Brain-kinematics-decoder/blob/master/LICENSE)

## Author

[RyotaroNumata](https://github.com/RyotaroNumata)