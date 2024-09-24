// This file contains implementations for things we forward-declared in our corresponding header file. By convention,
// the files have the same name. It's also expected that we have the file extension .h, .hpp, or .h++.

// In order to link the implmentations to their definitions, we must #include their declarations here.
#include "melody.hpp"

// Because we're no longer inside the Melody struct, we need to enter its namespace by typing out the name of the struct,
// resolving its template arguments, and then using :: to find the thing we want.
template <size_t N>
void Melody<N>::setup() {
  // After getting all the notes in the melody, they need to be sorted by offset to ensure everything is played in the
  // correct order.
  sortInPlace(m_notes);
}

template <size_t N>
const Note& Melody<N>::operator[](const size_t& index) const {
  return m_notes[index]; 
}

template <size_t N>
Note& Melody<N>::operator[](const size_t& index) {
    return m_notes[index];
}

template <size_t N>
const Note* Melody<N>::cbegin() const {
  // The & is an operator that creates a reference to the r-value to its right (m_notes[0]). The reference is
  // implicitly const due to the marked return type of this member function.
  return &m_notes[0];
}

template <size_t N>
Note* Melody<N>::begin() {
  return &m_notes[0];
}

template <size_t N>
const Note* Melody<N>::cend() const {
  return &m_notes[N];
}

template <size_t N>
Note* Melody<N>::end() {
  return &m_notes[N];
  }

template <size_t length>
void playMelody(uint8_t buzzerPin, const Melody<length>& melody) {
  // The -> is a combination of a dereference (getting the actual value the reference points to) and a member accessor.
  // Another more verbose way to write the line below would be: delay((*melody.cbegin()).offset());
  delay(melody.cbegin()->offset());
  // This is called the iterator pattern for "for" loops, and it's much safer than using raw indices. We end one index
  // early because special behavior is required for the final note.
  for (const Note* note = melody.cbegin(); note < melody.cend() - 1; note++) {
    // This line actually plays the note at the given frequency and for the given duration.
    tone(buzzerPin, note->frequency(), note->duration());
    // delay() suspends execution for the given number of milliseconds. In this case, we're calculating the differences
    // in offsets to determine the space between adjacent notes.
    delay((note + 1)->offset() - note->offset());
  }
  tone(buzzerPin, (melody.cend() - 1)->frequency(), (melody.cend() - 1)->duration());
  delay((melody.cend() - 1)->duration());
  noTone(buzzerPin);
}

// This implementation of the template specialization simply does nothing, because melodies of zero length don't really
// need to be played. This prevents us from having to do some annoying bounds checks in the standard implementation.
template <>
void playMelody<0>(uint8_t, const Melody<0>&) {}

// This particular algorithm sorts notes by offset using insertion sort. This algorithm was chosen because its memory
// use grows at O(1) in the worst case (i.e., it doesn't grow) and the target machine (an Arduino) has very little
// memory capacity.
/// Sorts the given Note array in place.
template <size_t N>
void sortInPlace(Note (&notes)[N]) {
  for (size_t i = 1; i < N; i++) {
    for (int j = i; j >= 0; j--) {
      if (notes[j - 1] > notes[j]) {
        swap(notes[j - 1], notes[j]);
      }
    }
  }
}

/// Swaps the contents of the variables passed in.
template <typename T>
void swap(T& a, T& b) {
  T tmp = a;
  a = b;
  b = tmp;
}