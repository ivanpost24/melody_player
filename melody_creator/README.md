# Melody Creator

Melody Creator is a program for generating C++ definitions for melodies written in music notation software to use on
an Arduino.

## How to run this software

First, make sure you have Python 3 installed (this has only been tested on Python 3.12).

Open a terminal window and navigate to the directory containing this file. Then create and activate a new virtual
environment by running

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Install required packages by running

```shell
pip install -r requirements.txt
```

Finally, run the `melody_creator` module with `python3 -m melody_creator`. The arguments for this are as follows:

```
python3 -m melody_creator [-h] [-n VAR_NAME] [-s OUTPUT_FILE] [-t] music_path
```

This can be run anywhere as long as the virtual environment is active.

For more information, run

```shell
python3 -m melody_creator -h
```

## Example use

Assume that `The_Good_Old_Song.mxl` is a compressed MusicXML file located in the current directory. Then run

```shell
python3 -m melody_creator The_Good_Old_Song.mxl -n "THE_GOOD_OLD_SONG" -s sample_audio.wav
```

This prints a C++ definition for playing the melody stored in `The_Good_Old_Song.mxl`. The variable to which the melody
is assigned is called `THE_GOOD_OLD_SONG`, and a sample of what the result will sound like is saved to
`sample_audio.wav`.