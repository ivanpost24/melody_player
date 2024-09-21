import re
from collections.abc import Sequence
from fractions import Fraction
from typing import Self

import music21 as m21
from pydub import AudioSegment
from pydub.generators import Square
from pydub.utils import ratio_to_db

from melody_creator import articulations
from melody_creator.note import Note, MachineNote
from melody_creator.tempo import Tempo

MUSIC21_ARTICULATION_MAPPING = {
    m21.articulations.Staccatissimo: articulations.STACCATISSIMO,
    m21.articulations.Staccato: articulations.STACCATO,
    m21.articulations.Spiccato: articulations.STACCATISSIMO,
    m21.articulations.DetachedLegato: articulations.NON_LEGATO,
    m21.articulations.Tenuto: articulations.TENUTO
}
"""A map from music21 articulation types to articulations defined by Melody Creator."""


class Melody:
    """A Melody stores a sequential collection of Notes and a Tempo indicating the speed to play the melody."""

    def __init__(self, notes: Sequence[Note], tempo: Tempo = Tempo.quarter_equals(120)) -> None:
        """
        Initializes a new Melody.
        :param notes: The sequence of notes in this melody. Notes will be automatically sorted by offset (required).
        :param tempo: The tempo of the melody (optional, defaults to quarter = 120 bpm).
        """
        self.__notes = sorted(notes, key=lambda n: n.offset)
        self.tempo = tempo

    @property
    def number_of_notes(self) -> int:
        """The number of notes in this melody."""
        return len(self.__notes)

    @property
    def duration(self) -> Fraction:
        """The duration of this melody in the number of whole notes."""
        return self.__notes[-1].offset + self.__notes[-1].duration

    def get_actual_duration(self) -> int:
        """The actual duration of this melody when played by an Arduino in milliseconds."""
        mnotes = self.get_machine_notes()
        return mnotes[-1].offset_millis + mnotes[-1].duration_millis

    @classmethod
    def from_stream(cls, stream: m21.stream.Stream) -> Self:
        """
        Creates a new melody from a music21 stream. The converter will consider all notes in the stream, even if
        they're in different parts/chords, and add them to the melody. Marked articulations will also be considered.
        """
        # Because music21 streams are highly nested, we must flatten them with stream.flatten() and simplify tied notes.
        # Then, we get only the elements of class "m21.note.Note", music21's class for representing notes (distinct from
        # the class defined in this project, disambiguated by the m21.note). We then convert them into the Note type
        # from this project and store them in a dictionary. Dictionaries map keys to values, and in this case the keys
        # are notes in the music21 format and the values are the notes in this project's format.
        # Because durations in music21 are indicated in quarter-lengths, we first convert to an exact format (Fraction,
        # as opposed to the approximate float) and divide by four to convert to whole-lengths.
        flattened_stream = stream.flatten().stripTies()
        notes: dict[m21.note.Note, Note] = {note: Note(pitch=note.pitch,
                                                       offset=Fraction(note.offset) / 4,
                                                       duration=Fraction(note.quarterLength) / 4)
                                            for note in flattened_stream.getElementsByClass(m21.note.Note)}

        # In the following section, we use slurs to infer legato articulations on specific notes. Every note in the
        # slur except for the last one (the [:-1] cuts off before the last note) will be marked as legato.
        # This is known as a type annotation. Although not strictly required, it's useful for telling your IDE what type
        # a variable is (since variables in Python can change types at any time). This particular one is one a different
        # line than the actual assignment to the variable in the following line. The above definition of notes provides
        # an example of combining these into one line.
        slur: m21.spanner.Slur
        for slur in flattened_stream.getElementsByClass(m21.spanner.Slur):
            legato_notes: list[Note]
            for legato_note in slur.getSpannedElementsByClass(m21.note.Note)[:-1]:
                notes[legato_note].articulation = articulations.LEGATO

        # Finally, we check other articulations. Combined staccato and tenuto is marked as mezzo-staccato because
        # music21 cannot represent mezzo-staccato as a single articulation. If you don't know what I'm talking about,
        # see this image: https://press.rebus.community/app/uploads/sites/81/2017/09/Mezzo-Staccato-II_0001.png
        for original_note, note in notes.items():
            if original_note.articulations:
                # Because the dictionary keys are types (not instances), we must first figure out the type of each
                # marked articulation, resulting in this longer syntax.
                if (any(a for a in original_note.articulations if type(a) is m21.articulations.Staccato)
                        and any(a for a in original_note.articulations if type(a) is m21.articulations.Tenuto)):
                    notes[original_note].articulation = articulations.MEZZO_STACCATO
                else:
                    articulation = next((a for a in original_note.articulations
                                         if type(a) in MUSIC21_ARTICULATION_MAPPING), None)
                    if articulation is not None:
                        notes[original_note].articulation = MUSIC21_ARTICULATION_MAPPING[type(articulation)]

        tempo = _get_tempo_from_stream(stream)
        if tempo is None:
            tempo = Tempo.quarter_equals(120)

        return cls(list(notes.values()), tempo)

    def get_machine_notes(self) -> list[MachineNote]:
        """Returns the machine notes for this melody."""
        return [self.tempo.note_to_machine_note(note) for note in self.__notes]

    def get_cpp_string(self, variable_name: str = 'MY_MELODY') -> str:
        """Returns the source code of the C++ definition required to define this melody."""
        if re.fullmatch(r'[A-Za-z_]+', variable_name) is None:
            raise ValueError('variable_name must be a valid C++ variable name')
        machine_note_strings = [f'  {{{mnote.frequency}, {mnote.offset_millis}, {mnote.duration_millis}}}'
                                for mnote in self.get_machine_notes()]

        return f'const Melody<{self.number_of_notes}> {variable_name} = {{{{\n{',\n'.join(machine_note_strings)}\n}}}};'

    def get_audio_segment(self) -> AudioSegment:
        """Returns a PyDub AudioSegment that plays this melody."""
        # First get silence that is the complete length of the resulting audio segment
        result = AudioSegment.silent(duration=self.get_actual_duration())
        for mnote in self.get_machine_notes():
            # Overlay notes one by one at the correct offset and with the correct duration
            result = result.overlay(
                AudioSegment.silent(duration=mnote.offset_millis, frame_rate=result.frame_rate)
                + Square(mnote.frequency).to_audio_segment(duration=mnote.duration_millis)
            )
        # Tip from https://github.com/jiaaro/pydub/issues/496
        return result.apply_gain(ratio_to_db(0.02))


def _get_tempo_from_stream(stream: m21.stream.Stream) -> Tempo | None:
    """Gets the first tempo indication in the stream, if there is one."""
    tempo_indication: m21.tempo.TempoIndication
    tempo_indication = next(stream.flatten().getElementsByClass(m21.tempo.TempoIndication), None)
    if tempo_indication is not None:
        metronome_mark = tempo_indication.getSoundingMetronomeMark()
        return Tempo(Fraction(metronome_mark.referent.quarterLength) / 4, metronome_mark.numberSounding)
    return
