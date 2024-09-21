from dataclasses import dataclass
from fractions import Fraction
from numbers import Rational

import music21 as m21

from melody_creator import articulations


class Note:
    """A Note stores a pitch, its offset from the starting point in the relevant music, and its duration."""

    def __init__(self, pitch: m21.pitch.Pitch, offset: Rational, duration: Rational,
                 articulation: Rational = articulations.NON_LEGATO):
        """
        Initializes a new Note.
        :param pitch: The pitch of the note, in Hertz.
        :param offset: The offset of the note (position from the start), in whole-lengths.
        :param duration: The duration of the note, in whole-lengths.
        :param articulation: The articulation of the note, as a proportion of the note's written duration.
        """
        self.__pitch = pitch
        self.__offset = Fraction(offset)
        self.__duration = Fraction(duration)
        self.__articulation = Fraction(articulation)

    @property
    def pitch(self) -> m21.pitch.Pitch:
        """The pitch of the note, in Hertz."""
        return self.__pitch

    @property
    def offset(self) -> Fraction:
        """The offset of the note (position from the start), in whole-lengths."""
        return self.__offset

    @property
    def duration(self) -> Fraction:
        """The duration of the note, in whole-lengths."""
        return self.__duration

    @property
    def end_offset(self) -> Fraction:
        """The offset of the end of the note (position from the start), in whole-lengths."""
        return self.__offset + self.__duration

    @property
    def articulation(self) -> Fraction:
        """The articulation of the note, as a proportion of the note's written duration."""
        return self.__articulation

    @articulation.setter
    def articulation(self, articulation: Rational) -> None:
        """
        Sets the articulation of the note, as a proportion of the note's written duration.
        :param articulation: The articulation of the note, as a proportion of the note's written duration.
        """
        self.__articulation = Fraction(articulation)

    def tie_with(self, other: 'Note') -> 'Note':
        """Returns a new note that is this note tied with the provided note. Both notes must have the same pitch."""
        if self.__pitch != other.pitch:
            raise ValueError('Tied notes must have the same pitch')
        offset = min(self.__offset, other.__offset)
        duration = max(self.end_offset - offset, other.end_offset - offset)
        return Note(self.__pitch, offset, duration, other.__articulation)

    # Gets a human-readable representation of the note
    def __str__(self):
        return (f'Note(pitch={self.pitch}, offset={self.offset}, duration={self.duration}, '
                f'articulation={self.articulation})')

    # Gets a representation of the note that could be evaluated in Python to produce the instance exactly
    def __repr__(self):
        return (f'Note(pitch={self.pitch!r}, offset={self.offset!r}, duration={self.duration!r}, '
                f'articulation={self.articulation!r})')


# A dataclass is a very simple class that stores the listed information in the given data type. The initializer
# (__init__), __str__, __repr__, and many other things are generated for us.
# The frozen keyword indicates that instances of MachineNote will be immutable.
@dataclass(frozen=True)
class MachineNote:
    """A MachineNote stores information that the Arduino will use to play a note."""

    frequency: int
    """The pitch of the note, in Hertz."""
    offset_millis: int
    """The offset of the note (position from the start), in milliseconds."""
    duration_millis: int
    """The duration of the note, in milliseconds."""
