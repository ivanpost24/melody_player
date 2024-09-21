/// Defines a collection of sequential notes, or a melody.

// See note.hpp for an explanation of header guards.
#ifndef MELODY_HPP
#define MELODY_HPP

// We need stuff from note.hpp, so we include it here
#include "note.hpp"

// Thanks to this for guiding me in creating what is basically a custom std::array for Notes: 
// https://arduino.stackexchange.com/a/69178
// This is what is known as a template declaration. Templates are probably one of the most complicated parts of C++,
// so I will keep my explanation brief. Basically, a template declaration indicates to the compiler that the following
// struct/class/variable/whatever declaration is a template for actual structures that will be compiled, subject to
// the given parameters. This particular one takes a single parameter called N of type size_t which indicates the
// length of the melody. When you declare a variable of type Melody<6> in a different file, that will tell the compiler
// to compile a version of this code where 6 is substituted for N in all the instances below.
// If you'd like to learn more, start with the Wikipedia page: https://en.wikipedia.org/wiki/Template_metaprogramming
template <size_t N>
struct Melody {

  // Unfortunately, using C arrays is weird. Thanks to this SO answer for resolving an issue I had:
  // https://stackoverflow.com/a/68745603
  /// Constructs a new Melody object with the given notes. The notes are automatically sorted after being passed in.
  Melody(const Note (&notes)[N]) : m_notes(notes) {
    setup();
  }

  /// Returns the length of the melody.
  static size_t length() { return N; }

  // This member function header is a forward declaration. A forward declaration indicates to the compiler that the
  // thing in question exists, but it doesn't provide a definition. To make the program compile, we need to provide an
  // definition (i.e., declaration) somewhere, which is the "melody.ino" file in this case. During compilation, the
  // linker will connect this forward declaration with its definition.
  // The reason why we separate declaration from definition is because it speeds up compilation if files using this
  // header are not modified or the just the file implementing the header is modified, it's easier for someone using
  // this header file to read what's going on, and it allows us to hide implementation details from the client.
  // This overloads the indexing operator. It takes a single argument of size_t (the type used for indexes and lengths
  // of arrays) which indicates (starting from 0) which note in the array to get.
  const Note& operator[](const size_t& index) const;
  // The & indicates that we are returning a reference to the Note. If the client assigns the result of the subscript
  // operator to a variable and modifies it, it will also modify the note in the melody.
  // The const in the previous one prevents that, but it still saves memory by not copying the original Note.
  Note& operator[](const size_t& index);

  // The following member functions implement the C++ iterator pattern. An iterator must have two functions called
  // begin() and end() which return pointers to the first item and the memory immediately past the last item,
  // respectively. I've also defined constant iterator pointers that prevent the returned pointer or its underlying
  const Note* cbegin() const;
  Note* begin();
  // The const at the beginning indicates the result cannot be modified. The const at the end promises to the compiler
  // that the Melody itself won't be modified when calling this member function.
  const Note* cend() const;
  Note* end();

private:

  // Setup is called by the constructor to run a few things after initializing all internal values.
  void setup();

  // This is an array of size N (the length of the melody) storing notes.
  Note m_notes[N];

};

// There are multiple things going on in this forward declaration.
// First is the template, which is explained above.
// Second is the presence of arguments to this function. Argument declarations consist of a type followed by a name
// that allows code inside the function to access whatever value was passed in. The type of the first argument is
// "uint8_t", a positive-only small integer type, and the type of the second argument is "const Melody<length>&",
// a constant reference to a Melody of the given length.
// Third is the return type, which is "void". This simply means the function doesn't return anything.
// Finally is the fact that this is a forward declaration. A forward declaration indicates to the compiler that the
// thing in question (in this case a function) exists, but we haven't defined it yet. In this case, it's defined in
// the "melody.ino" file, and something called the linker will connect this declaration with its implementation when
// the code is compiled.
/// Plays the given melody by repeated tone() calls to the given pin.
template <size_t length>
void playMelody(uint8_t buzzerPin, const Melody<length>& melody);

// This is called a template specialization because we're indicating that something different should be done for a
// specific set of arguments. This one is really simple: a specialization when there are no notes in the melody.
// Because they don't matter here, names of arguments were omitted.
template <>
void playMelody<0>(uint8_t, const Melody<0>&);

#endif /* MELODY_HPP */