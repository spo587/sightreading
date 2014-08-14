import sightreading as s
import random

class Piano_score(object):
    ## dictionary to convert scale degrees to notes of c major or c minor scale
    C_major_dictionary = {1: 'c', 1.3: 'cis', 1.6:'des', 2:'d', 2.3:'dis', 2.6:'ees', 3:'e', 3.3:'eis', 3.6:'fes', 4:'f', 4.3:'fis', 4.6:'ges', 5:'g', 6:'a', 7:'b', '':'r'}
    c_minor_dictionary = {1:'c', 2:'d', 3:'ees', 4:'f', 5:'g', 6:'aes', 7:'bes', '':'r'}
    ## to convert number of beats to lilypond note names (quarter notes: 1 beat encoded as 4)
    rhythm_converter = {1:'4', 2:'2', 4:'1', 3:'2.'}
    def __init__(self, rh_voice, lh_voice, beatsPer, key, quality):
        self.rh_voice = rh_voice
        self.lh_voice = lh_voice
        self.beatsPer = str(beatsPer)
        self.key = key
        self.quality = quality
        self.string = self.getLilyString() 
    def getLilyString(self):
        lilyString = '' 
        lilyString += '\\score {\n'
        lilyString += ' \\new PianoStaff << \n'
        lilyString += '     \\time '+ self.beatsPer +'/' + '4' + '\n'
        lilyString += '     \\new Staff {\n'
        lilyString += '         \\transpose c ' + self.key + '\' {\n'
        lilyString += '         \\clef "treble"\n'
        lilyString += '         \\key c \\'+ self.quality +'\n' 
        lilyString += '             ' + self.rh_voice.toString() + '\n'
        lilyString += '             }\n'
        lilyString += '         }\n'
        lilyString += '     \\new Staff {\n'
        lilyString += '         \\transpose c ' + self.key + '\' {\n'  
        lilyString += '         \\clef "bass"\n'
        lilyString += '         \\key c \\'+ self.quality +'\n'
        lilyString += '             ' + self.lh_voice.toString() + '\\bar "|."\n'
        lilyString += '             }\n'
        lilyString += '         }\n'
        lilyString += '     >>\n'
        lilyString += '}'
        return lilyString

class Voice(object):
    '''a single line of music in the rh or lh'''
    def __init__(self, numMeasures, beatsPer, bass_or_treble, rests_or_notes, quality, level):
        self.note_list = []
        self.rests_or_notes = rests_or_notes
        self.numMeasures = numMeasures
        self.beatsPer = beatsPer
        self.bass_or_treble = bass_or_treble
        self.quality = quality
        self.level = level
        self.rhythms = s.makeRhythms_unnested(self.numMeasures, self.beatsPer)
        self.stepNums = s.stepNoteNumsFiveFinger(self.rhythms, self.level)
        self.transposition_dict = Piano_score.c_minor_dictionary if self.quality == 'minor' else Piano_score.C_major_dictionary
        self.buildNotes()
        self.addFingering()
    def buildNotes(self):
        if self.rests_or_notes == 'rests':
            rest_beat = ' r' + Piano_score.rhythm_converter[self.beatsPer] + ' '
            for i in range(self.numMeasures):
                self.addNote(rest_beat)
        else:
            for i in range(len(self.rhythms)):
                if self.bass_or_treble == 'bass':
                    self.addNote(self.transposition_dict[self.stepNums[i]] + ',' + Piano_score.rhythm_converter[self.rhythms[i]] + ' ')
                else:
                    self.addNote(self.transposition_dict[self.stepNums[i]] + Piano_score.rhythm_converter[self.rhythms[i]] + ' ')

    def addFingering(self):
        if self.rests_or_notes != 'rests':
            lowestNote = min(self.stepNums) ## find the lowest scale degree
            fingering = str(self.stepNums[0] - lowestNote + 1) ## assign the fingering string
            if self.bass_or_treble == 'bass': ## 
                reverse =  {'5':'1', '4':'2', '3':'3', '2':'4', '1':'5'}
                fingering = reverse[fingering]
            self.note_list[0] = self.note_list[0] + '-' + fingering
    def toString(self):
        '''to be read by lilypond'''
        string = ''
        for i in range(len(self.note_list)):
            string += self.note_list[i]
        return string
    def addNote(self, note):
        self.note_list.append(note)
    def combine(self, other):
        '''for combining sequentially two voices in the same hand'''
        for i in range(len(other.note_list)):
            self.numMeasures = self.numMeasures + other.numMeasures
            self.note_list.append(other.note_list[i])

# def make_voice(numMeasures, beatsPer, bass_or_treble):
#     rhythms = s.makeRhythms_unnested(numMeasures, beatsPer)
#     stepNums = s.stepNoteNumsFiveFinger(rhythms)
#     assert len(rhythms) == len(stepNums)
#     voice = Voice([])
#     for i in range(len(rhythms)):
#         if bass_or_treble == 'bass':
#             voice.addNote(Piano_score.C_major_dictionary[stepNums[i]] + ',' + Piano_score.rhythm_converter[rhythms[i]] + ' ')
#         else:
#             voice.addNote(Piano_score.C_major_dictionary[stepNums[i]] + Piano_score.rhythm_converter[rhythms[i]] + ' ')
#     ## add fingering to first note
#     voice.note_list[0] = voice.note_list[0] + '-' + str(Piano_score.C_major_dictionary_reverse[voice.note_list[0][0]])
#     return voice


def make_sightreading(numMeasures_per_hand, beatsPer, key, quality, level):
    rh_voice = Voice(numMeasures_per_hand, beatsPer, 'treble', 'rests', quality, level)
    rh_notes = Voice(numMeasures_per_hand, beatsPer, 'treble', 'notes', quality, level)
    rh_voice.combine(rh_notes)
    lh_voice = Voice(numMeasures_per_hand, beatsPer, 'bass', 'notes', quality, level)
    lh_rests = Voice(numMeasures_per_hand, beatsPer, 'bass', 'rests', quality, level)
    lh_voice.combine(lh_rests)
    score = Piano_score(rh_voice, lh_voice, beatsPer, key, quality)
    return score.getLilyString()
    # rest_beat = ' r' + Piano_score.rhythm_converter[beatsPer] + ' '
    # rh_voice = Voice([])
    # for i in range(numMeasures_per_hand):
    #     rh_voice.addNote(rest_beat)
    # rh_notes = make_voice(numMeasures_per_hand, beatsPer, 'treble')
    # rh_voice.combine(rh_notes)
    # lh_voice = make_voice(numMeasures_per_hand, beatsPer, 'bass')
    # lh_rests = Voice([])
    # for i in range(numMeasures_per_hand):
    #     lh_rests.addNote(rest_beat)
    # lh_voice.combine(lh_rests)
    # score = Piano_score(rh_voice, lh_voice, beatsPer, key, quality)
    # return score.getLilyString()


def random_sightreading(level, numMeasures_per_hand=4):
    beatsPer = random.choice([3,4])
    ## five finger positions with no sharps/flats
    key_quality = random.choice(['c major','d minor','a minor', 'g major'])
    key = key_quality[0]
    quality = key_quality[2:]
    return make_sightreading(numMeasures_per_hand, beatsPer, key, quality, level)

def make_sightreadings(level, numExamples):
    s = ''
    for i in range(numExamples):
        s += random_sightreading(level)
    return s








if __name__ == '__main__':
    print make_sightreadings(2,4)
