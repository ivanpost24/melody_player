/// Defines a structure for representing individual notes in a melody.

// This is what is known as a header file. Header files are #included at the top of other files to use the interfaces
// located there.

// The following two lines (and the #endif at the end of the file) comprise a header guard. This resolves the problem
// illustrated in the following example:
// Say a.hpp #includes b.hpp and main.ino #includes both a.hpp AND b.hpp. Because #include basically just inserts the
// code from a header file into the location of the #include, this will cause b.hpp to be included twice! If we allow
// this to happen, the compiler will get very mad at us because we're duplicating definitions. Therefore, we add a
// header guard to the top to prevent this issue.
// The #ifndef directive indicates that the following code, up until the #endif, should be removed from compilation if
// the following precompiler variable is defined.
// If the #ifndef detects the following variable is not defined, the #define later defines that variable. If another
// file #includes this header, then #ifndef will detect the defined variable and prevent duplicate compilation.
#ifndef NOTE_HPP
#define NOTE_HPP

// A "struct" defines a blueprint for objects, encapsulate data. In this case, the blueprint's name is Note, and it
// has all objects created from the blueprint contain information about individual notes that will be played.
struct Note {

  // uint16_t indicates that the type is an unsigned (>= 0) 16-bit integer. We use this instead of things like short
  // or int because it guarantees that the 16-bit integer will be chosen.
  // This is an
  Note(const uint16_t& frequency, const unsigned long offset, const unsigned long duration): m_frequency(frequency), m_offset(offset), m_duration(duration) {
    if (frequency < 31) {
      // Under normal circumstances you would want to throw this string, but unfortunately that is not possible in
      // the Arduino subset of C++.
      Serial.println("ERROR: Frequency less than 31 Hz provided");
    }
  }
  
  // The three declarations below are known as member functions, since they will be members of each object created from
  // this struct and they are callable functions. These particular member functions are known as getters because they
  // get the data stored by each of the members listed in the private section, but in a way such that they cannot be 
  // modified.
  // The & indicates that the return type (the kind of data returned) is a reference, which means this struct's data
  // won't be copied upon return. The first "const" is there to make sure that client code can't modify the original
  // integer stored in the Note. In plain English, the type would be read as "a reference to a constant unsigned
  // 16-bit integer."" The second "const" indicates that this member function doesn't modify the Note, which
  // means a const Note object will have this member function.
  /// Returns the pitch of the note as a frequency in Hertz.
  const uint16_t& frequency() const { return m_frequency; }

  // "unsigned long" is a large integer type that stores only positive integers.
  /// Returns the offset of the note (position from the start) in milliseconds.
  const unsigned long& offset() const { return m_offset; }
  
  // "unsigned int" is slightly smaller than 
  /// Returns the duration of the note in milliseconds.
  const unsigned int& duration() const { return m_duration; }

  // This function is special in two ways: it overloads an operator and it is a friend. Operator overloading implements
  // the behavior of the given operator (in this case, the > operator) for the given signature (comparing two Notes).
  // This allows us to do something like note1 > note2 and get a sensible result.
  // friend indicates that this actually isn't a member function, but that wherever else it's defined it can access
  // private members of the instance.
  friend bool operator>(const Note& lhs, const Note& rhs);

// By default, struct members are public, which means that any client code that can access Note is able to access the
// member. However, to prevent the client from modifying the internal data of objects created from Note, we indicate
// them as private. The client can still view, but not modify the data using the getters above.
private:

  // Prefixing with "m_" is convention to ensure there are no name conflicts with the member functions above. The "m"
  // stands for member. This form of disambiguation is almost always unnecessary in other programming languages (or
  // a different convention is used).
  uint16_t m_frequency;
  unsigned long m_offset;
  unsigned int m_duration;

};

// This is our actual implementation of >. It's declared inline to encourage the compiler to basically substitute the
// comparison in for efficiency.
// The reference (&) means we won't copy notes when trying to compare them, saving memory; and const ensures the
// implementation cannot modify the passed in Note.
// "bool" is a true/false data type (it stores Boolean data).
inline bool operator>(const Note& lhs, const Note& rhs) { return lhs.m_offset > rhs.m_offset; }

// The NOTE_HPP down here is optional (it's in a comment).
#endif /* NOTE_HPP */