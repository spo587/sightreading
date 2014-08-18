import basic_functions_sightreading as s
import random
import subprocess
import time

class Piano_score(object):
    '''formats the inputs to make a lilypond string'''
    ## dictionary to convert scale degrees to notes of c major or c minor scale
    C_major_dictionary = {1: 'c', 1.3: 'cis', 1.6:'des', 2:'d', 2.3:'dis', 2.6:'ees', 3:'e', 3.3:'eis', 3.6:'fes', 4:'f', 4.3:'fis', 4.6:'ges', 5:'g', 6:'a', 7:'b', '':'r'}
    c_minor_dictionary = {1:'c', 2:'d', 3:'ees', 4:'f', 5:'g', 6:'aes', 7:'bes', '':'r'}
    ## dict to convert number of beats to lilypond note names (quarter notes: 1 beat, written as a 4 in lilypond)
    rhythm_converter = {1:'4', 2:'2', 4:'1', 3:'2.'}
    def __init__(self, rh_voice, lh_voice, beatsPer, key, quality):
        '''rh_voice and lh_voice are each instances of voice class.
        beatsPer is beats per measure. right now only supporting quarter note beats
        key is name of the key (e, f, c, etc), while quality is 'major' or 'minor' '''
        self.rh_voice = rh_voice
        self.lh_voice = lh_voice
        self.beatsPer = str(beatsPer)
        self.key = key
        self.quality = quality
        self.string = self.getLilyString() 
    def getLilyString(self):
        '''this part's kinda ugly, but whatre ya gonna do
        have to build a big ol string for the lilypond output. this makes it somewhat
        pretty/viewable. the transpose line is important. everything is written in c
        and then transposed to a different key later'''
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
    '''a single line of music in the rh or lh. the toString() method gives us a string
    we can then insert into the lilystring from the piano_score class
    level: 1 or 2, for sightreading purposes'''
    def __init__(self, numMeasures, beatsPer, bass_or_treble, rests_or_notes, quality, level):
        self.note_list = [] ## the notelist will have the notes and rests
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
            ## add rests to the note_list
            rest_beat = ' r' + Piano_score.rhythm_converter[self.beatsPer] + ' '
            for i in range(self.numMeasures):
                self.addNote(rest_beat)
        else:
            for i in range(len(self.rhythms)):
                if self.bass_or_treble == 'bass':
                    ## notes down by c the octave below middle c (comma in lilypond)
                    self.addNote(self.transposition_dict[self.stepNums[i]] + ',' + Piano_score.rhythm_converter[self.rhythms[i]] + ' ')
                else:
                    self.addNote(self.transposition_dict[self.stepNums[i]] + Piano_score.rhythm_converter[self.rhythms[i]] + ' ')

    def addFingering(self):
        ## add fingering to the first note of the phrase
        if self.rests_or_notes != 'rests':
            lowestNote = min(self.stepNums) ## find the lowest scale degree
            fingering = str(self.stepNums[0] - lowestNote + 1) ## assign the fingering string
            if self.bass_or_treble == 'bass': ## switch fingering for LH
                reverse =  {'5':'1', '4':'2', '3':'3', '2':'4', '1':'5'}
                fingering = reverse[fingering]
            ## modify the first note to put the fingering in
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



def make_sightreading(numMeasures_per_hand, beatsPer, key, quality, level):
    '''first the LH notes while RH rests, then reverse'''
    rh_voice = Voice(numMeasures_per_hand, beatsPer, 'treble', 'rests', quality, level)
    rh_notes = Voice(numMeasures_per_hand, beatsPer, 'treble', 'notes', quality, level)
    rh_voice.combine(rh_notes)
    lh_voice = Voice(numMeasures_per_hand, beatsPer, 'bass', 'notes', quality, level)
    lh_rests = Voice(numMeasures_per_hand, beatsPer, 'bass', 'rests', quality, level)
    lh_voice.combine(lh_rests)
    score = Piano_score(rh_voice, lh_voice, beatsPer, key, quality)
    return score.getLilyString()


def random_sightreading(level, numMeasures_per_hand=4):
    beatsPer = 4 if random.random() < 0.7 else 3
    ## five finger positions with no sharps/flats
    if level == 1:
        key_quality = random.choice(['c major','d minor','a minor', 'g major'])
    elif level == 2:
        key_quality = random.choice(['c major','d minor','a minor', 'g major', 'a major', 'd major', 'g minor', 'e minor', 'f major'])
    key = key_quality[0]
    quality = key_quality[2:]
    return make_sightreading(numMeasures_per_hand, beatsPer, key, quality, level)

def make_sightreadings(level, numExamples):
    s = ''
    for i in range(numExamples):
        s += random_sightreading(level)
    return s



if __name__ == '__main__':
    ## make 10 examples of level 1 sightreading and save output to a pdf
    level = 2
    string = make_sightreadings(level,10)
    date_addendum = time.asctime()
    title = 'level_1_august_16_2.ly'
    subprocess.call(['touch',title])
    f = open(title,'w')
    subprocess.call(['echo',string],stdout=f)
    subprocess.call(['lilypond',title])
    # title = 'sightreading '+ 'level ' + str(level) + ' ' + date_addendum + '.ly'
    # subprocess.call(['touch',title])
    # f = open(title,'w')
    # subprocess.call(['echo',string], stdout=f)
    # subprocess.call(['lilypond',title])
    
