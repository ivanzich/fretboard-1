import numpy as np

NTONES = 12
MAJOR = [2, 2, 1, 2, 2, 2, 1]

whole_notes = [n for n in 'CDEFGAB']
sharps = [n + '#' for n in whole_notes]
flats = [n + 'b' for n in whole_notes]

# Names of all notes using sharp notation
notess = list(reduce(lambda a, b: a + b, zip(whole_notes, sharps)))
notess.remove('E#')
notess.remove('B#')

# Names of all notes using float notation
notesb = list(reduce(lambda a, b: a + b, zip(flats, whole_notes)))
notesb.remove('Fb')
notesb.remove('Cb')

def i2ns(i):
    '''Returns name of note (using sharp), given number of semitones above C.'''
    return notess[i % NTONES]

def i2nb(i):
    '''Returns name of note (using flat), given number of semitones above C.'''
    return notesb[i % NTONES]

def n2i(note_name):
    '''Return numeric index of note, given note string.'''
    if 'b' in note_name:
        return notesb.index(note_name)
    else:
        return notess.index(note_name)
    
class Scale(object):
    def __init__(self, key):
        self.key = key
        self.create_notes()

    def level(self, i):
        return self.notes[level - 1]

    def get_scale_degree(self, note):
        if note not in self.notes:
            raise ValueError('Note is not in scale')
        return str(self.notes.index(note) + 1)

    def __iter__(self):
        for t in self.notes:
            yield t

    def __getitem__(self, i):
        if i < 1 or i > len(self.notes):
            raise ValueError(str(i))
        return self.notes[i - 1]

    def __str__(self):
        return '[{}]'.format(', '.join([str(n) for n in self.notes]))

class Major(Scale):
    def __init__(self, key, mode=0):
        self.mode = mode
        super(Major, self).__init__(key)
    def create_notes(self):
        intervals = np.roll(MAJOR, -self.mode)[:-1]
        self.notes = [Note(self.key)]    
        for i in intervals:
            self.notes.append(self.notes[-1] + i)

class Minor(Major):
    def __init__(self, key):
        super(Minor, self).__init__(key, 5)

class HarmonicMinor(Minor):
    def create_notes(self):
        super(HarmonicMinor, self).create_notes()
        self.notes[-1] = self.notes[-1] + 1

class Pentatonic(Scale):
    def __init__(self, scale, levels=None):
        if levels is not None:
            if len(levels) != 5:
                raise ValueError('Pentatonic scale requires exactly 5 levels')
        elif isinstance(scale, Minor):
            self.levels = [1, 3, 4, 5, 7]
            
        elif isinstance(scale, Major):
            self.levels = [1, 2, 3, 5, 6]
        else:
            raise TypeError('Invalid base type for pentatonic scale')
        self.base_scale = scale
        super(Pentatonic, self).__init__(scale.key)

    def create_notes(self):
        self.notes = [self.base_scale[i] for i in self.levels]

    def get_scale_degree(self, note):
        if note not in self.notes:
            raise ValueError('Note is not in scale')
        return str(self.levels[self.notes.index(note)])

class Blues(Scale):
    def __init__(self, key):
        super(Blues, self).__init__(key)

    def create_notes(self):
        pm = Pentatonic(Minor(self.key))
        self.notes = [note for note in pm]
        flat5 = self.notes[3] - 1
        flat5.display_sharp = False
        self.notes.insert(3, flat5)
        self.degrees = ['1', '3', '4', '5b', '5', '7']

    def get_scale_degree(self, note):
        if note not in self.notes:
            raise ValueError('Note is not in scale')
        return self.degrees[self.notes.index(note)]

class Note:
    display_sharp = True
    def __init__(self, tone):
        if type(tone) == str:
            tone = n2i(tone)
        while tone < 0:
            tone += NTONES
        self.tone = tone
        self.value = tone % NTONES
    def __str__(self):
        if self.display_sharp:
            return i2ns(self.value % NTONES)
        else:
            return i2nb(self.value % NTONES)
    def __eq__(self, note):
        if type(note) in (int, str):
            note = Note(note)
        return self.value == note.value
    def __repr__(self):
        return str(self)
    def __add__(self, semitones):
        return Note(self.tone + semitones)
    def __sub__(self, lower):
        if isinstance(lower, int):
            return Note(self.tone - lower)
        else:
            return self.tone - lower.tone

# Functions for display in spreadsheet

def note_name(note, scale):
    return Note(note) if note in scale else None

def names(notes, sharps=True):
    if sharps:
        f = i2ns
    else:
        f = i2nb
    return [f(n) for n in notes]

def show_X(n, scale):
    n = n % NTONES
    if n == scale[0]:
        return 'XX'
    elif n in scale:
        return 'X'
    else:
        return None

def show_scale_degree(note, scale):
    if note in scale:
        return scale.get_scale_degree(note)
    else:
        return None

def display_note(i, scale, sharps=True):
    if sharps:
        return i2ns(i)
    else:
        return i2nb(i)
