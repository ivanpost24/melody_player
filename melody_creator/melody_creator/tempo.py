from fractions import Fraction
from numbers import Rational

from melody_creator.note import Note, MachineNote


class Tempo:
    """Stores information about a musical tempo. Tempo instances are immutable."""

    def __init__(self, subdivision: Rational, beats_per_minute: int):
        """
        Initializes a new Tempo.
        :param subdivision: The subdivision to which the rate of the tempo is relative.
        :param beats_per_minute: The rate of the tempo relative to the given in beats per minute.
        """
        self.__subdivision = Fraction(subdivision)
        self.__beats_per_minute = int(beats_per_minute)

    # The following definition defines both a property called "subdivision" and a getter for that property. Because
    # no setter is defined, it's impossible to modify the subdivision on this tempo.
    @property
    def subdivision(self) -> Fraction:
        """The subdivision to which the rate of the tempo is relative."""
        return self.__subdivision

    @property
    def beats_per_minute(self) -> int:
        """The rate of the tempo in beats per minute."""
        return self.__beats_per_minute

    @classmethod
    def quarter_equals(cls, beats_per_minute: int):
        """
        Initializes a new Tempo relative to the quarter note at the given rate.
        :param beats_per_minute: The number of quarter notes that occur in a single minute.
        """
        return Tempo(Fraction(1, 4), beats_per_minute)

    def convert_to_subdivision(self, subdivision: Fraction) -> 'Tempo':
        """
        Converts the tempo into a new Tempo in the given subdivision. If necessary, the number of beats per minute
        will be rounded to the nearest integer.
        :param subdivision: The new subdivision.
        :return: A Tempo roughly equivalent to this Tempo with the given subdivision.
        """
        return Tempo(subdivision, round(self.beats_per_minute * subdivision / self.subdivision))

    def note_to_machine_note(self, note: Note) -> MachineNote:
        """Converts the given note in this tempo to a machine note."""
        actual_duration_wholes = note.articulation * note.duration
        return MachineNote(round(note.pitch.freq440),
                           self.__wholes_to_milliseconds(note.offset),
                           (100 + self.__wholes_to_milliseconds(actual_duration_wholes) - round(note.articulation * 100)))

    def __wholes_to_milliseconds(self, duration: Fraction) -> int:
        """
        Converts the given number of whole-lengths in this tempo to milliseconds. This rounds to the
        nearest millisecond.
        :param duration: The number of whole-lengths to convert.
        """
        return round(duration / (self.beats_per_minute * self.subdivision) * 60_000)

    # This just allows us to convert the tempo to a nice human-readable string
    def __str__(self) -> str:
        return f'<{type(self).__qualname__} {self.subdivision} note = {self.beats_per_minute} bpm>'
