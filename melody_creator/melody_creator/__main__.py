# The __main__ file is executed when executing the entire module.
import argparse
import sys
from pathlib import Path

import music21 as m21

from melody_creator.melody import Melody


def run(music_path: Path, var_name: str, sample_audio_path: Path | None = None) -> None:
    """Runs the main bulk of the program."""
    # First parse the MusicXML file.
    stream = m21.converter.parseFile(music_path)
    # Then convert to a Melody.
    melody = Melody.from_stream(stream)
    # Then print the C++ definition required to define the melody.
    print(melody.get_cpp_string(var_name))
    # If the user enabled saving a sample to a file, then do that.
    if sample_audio_path is not None:
        melody.get_audio_segment().export(sample_audio_path)


def main() -> None:
    """Runs Melody Creator."""

    # This part allows us to set up arguments to the executable.
    parser = argparse.ArgumentParser()
    parser.add_argument('music_path', type=Path,
                        help='Path to a MusicXML (or compressed MusicXML) file from which the melody will be read. '
                             'It\'s expected for the file only to have a single part and no chords.')
    parser.add_argument('-n', '--name', dest='var_name', type=str, default='MY_MELODY',
                        help='The name of the printed variable. Must be a valid C++ variable name.')
    parser.add_argument('-s', '--export-sample-audio', dest='sample_audio_path', type=Path,
                        metavar='OUTPUT_FILE',
                        help='Export a sample of what the melody will sound like when played on an Arduino to a file. '
                             'Most common audio file formats are supported.')
    parser.add_argument('-t', '--print-traceback', dest='print_traceback', action='store_true', default=False,
                        help='Print full tracebacks of errors raised during the program\'s execution.')

    namespace = parser.parse_args()
    if namespace.print_traceback:
        run(namespace.music_path, namespace.var_name, namespace.sample_audio_path)
    else:
        # Instead of printing out the entire traceback, we just print the messages of errors that occur. The user can
        # enable typical behavior by setting the --print-traceback flag.
        try:
            run(namespace.music_path, namespace.var_name, namespace.sample_audio_path)
        except Exception as e:
            print(f'ERROR ({type(e).__name__}): {e}\n', file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
