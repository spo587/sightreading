import random

def makeRhythms_unnested(numMeasures, beatsPer):
    '''outputs a list of beats in 4/4 or 3/4 with quarter notes, half notes and some 
    dotted halfs on the first beats, except final note of phrase, which takes up the whole
    measure. no syncopations in 4/4, some 1 2 groups in 3/4. fix?'''
    rhythms = []
    beat = 0 ## indexed to 0
    measures = 0 # samesies
    while (measures < numMeasures-1): ##not in the final measure
        if beat > beatsPer - 1: ## new measure
            beat = beat % beatsPer ## heh? why not just 0, check this later
            measures += 1
        if beat == 0:
            randNum = random.random()
            if randNum < 0.1:
                rhythms.append(3)
                beat += 3
            elif 0.1 < randNum < 0.5:
                rhythms.append(2)
                beat += 2
            else:
                rhythms.append(1)
                beat += 1
        elif beat == beatsPer/2: ## beat 3 of 4/4
            randNum = random.random()
            if randNum < 0.5:
                rhythms.append(1)
                beat += 1
            else:
                rhythms.append(2)
                beat += 2
        else:
            rhythms.append(1)
            beat += 1
    rhythms[-1] = beatsPer
    return rhythms

def nextNoteStep(currentScaleDegree, level, pinkyDegree=4):
    '''for 5 finger position, not necessarily on tonic though. thumb steps go negative if pinky below 5th degree
    the tonic is 0 in this implementation'''
    randNum = random.random()
    randnum2 = random.random()
    thumbDegree = pinkyDegree - 4
    if level == 1:
        increment = 1
    elif level == 2:
        increment = 2 if randnum2 < 0.3 else 1
    if currentScaleDegree == thumbDegree:
        nextDegree = currentScaleDegree + increment if randNum < 0.8 else currentScaleDegree
    elif currentScaleDegree == pinkyDegree:
        nextDegree = currentScaleDegree - increment if randNum < 0.8 else currentScaleDegree
    else:
        if randNum < 0.4:
            nextDegree = currentScaleDegree - increment
        if 0.4<= randNum < 0.6:
            nextDegree = currentScaleDegree
        else:
            nextDegree = currentScaleDegree + increment
    if thumbDegree <= nextDegree and nextDegree <= pinkyDegree:
        return nextDegree
    else:
        return nextNoteStep(currentScaleDegree, level, pinkyDegree)



def stepNoteNumsFiveFinger(rhythms, level, pinkyDegree=4):
    '''takes the rhythms and the level and creates a list of scale degrees, ending
    on the tonic'''
    notes = [0] ## always end on tonic
    for i in range(1,len(rhythms)):
        notes.append(nextNoteStep(notes[i-1], level))
    notes.reverse()
    notes = [notes[i] + 1 for i in range(len(notes))] ## other module has tonic = 1, not 0. fix this!!
    return notes




# class Tone(object):
#     note_dict = {'a':0,'b':2,'c':3,'d':5,'e':7,'f':8,'g':10,'rest':0}
#     for note in note_dict.keys():
#         note_dict[note + '#'] = note_dict[note] + 1
#         note_dict[note + 'b'] = note_dict[note] - 1
#     def __init__(self, step, alter, octave, rhythmValue): ##, metricBeat):
#         self.step = step
#         self.alter = alter
#         self.halfSteps = Tone.note_dict[step] + self.alter
#         self.octave = octave
#         self.rhythmValue = rhythmValue
#         ##self.metricBeat = metricBeat




# class MajorScale(object):
#     note_dict = {'a':0,'b':2,'c':3,'d':5,'e':7,'f':8,'g':10,'rest':0}
#     reverse_dict = {0:'a',2:'b',3:'c',5:'d',7:'e',8:'f',10:'g'}
#     notesList = ['a','b','c','d','e','f','g']
#     majorScaleDict = {1:0, 2:2, 3:4, 4:6, 5:7, 6:9, 7:11}
#     majorScaleList = [0,2,4,5,7,9,11]
#     def __init__(self, tonic, step, fifthsCircle):
#         self.step = step
#         self.tonic = tonic
#         self.fifthsCircle = fifthsCircle
#         ind = MajorScale.notesList.index(step)
#         for i in range(ind):
#             MajorScale.notesList.append(MajorScale.notesList.pop(0))
#         print MajorScale.notesList
#         self.scaleDegreesNums = [(tonic + MajorScale.majorScaleList[i])%12 for i in range(7)]
#         self.scaleDegrees = {}
#         if fifthsCircle <= 6:
#             for i in range(7):
#                 try:
#                     self.scaleDegrees[i+1] = MajorScale.reverse_dict[self.scaleDegreesNums[i]]
#                 except KeyError:
#                     self.scaleDegrees[i+1] = MajorScale.notesList[i] + '#'



# def fiveFingerStepNotes(tonic,step,fifthsCirle,rhythms):
#     scale = MajorScale(tonic,step,fifthsCirle)
#     print scale
#     notes = stepNoteNumsFiveFinger(rhythms)
#     print notes
#     readnotes = []
#     for i in range(len(notes)):
#         readnotes.append(scale.scaleDegrees[notes[i]])
#     return readnotes


# def makeRhythms(numMeasures, beatsPer):
#     rhythms = []
#     for i in range(numMeasures):
#         rhythms.append([])
#     beat = 0
#     measures = 0
#     while (measures < numMeasures-1): ##not in the final measure
#         if beat > beatsPer - 1: ## not on final beat
#             beat = beat % beatsPer
#             measures += 1
#         if beat == 0 or beat == beatsPer/2:
#             randNum = random.random()
#             if randNum < 0.5:
#                 rhythms[measures].append(1)
#                 beat += 1
#             else:
#                 rhythms[measures].append(2)
#                 beat += 2
#         else:
#             rhythms[measures].append(1)
#             beat += 1
#     rhythms[-1] = [beatsPer]
#     return rhythms


# def makeRhythms_(numMeasures):
#     '''for 4/4 time only, no syncopations'''
#     rhythms = []
#     beat = 1
#     measures = 0
#     while measures < numMeasures:
#         if beat > 4:
#             beat = beat % 4
#             measures += 1
#         if beat == 1 or beat == 3:
#             randNum = random.random()
#             if randNum < 0.5:
#                 rhythms.append(1)
#                 beat += 1
#             else:
#                 rhythms.append(2)
#                 beat += 2
#         elif beat == 2:
#             rhythms.append(1)
#             beat += 1
#         elif beat == 4:
#             rhythms.append(1)
#             beat += 1
#         if sum(rhythms) == numMeasures*4:
#             break
            
#     print rhythms
#     return rhythms

# def combineNotesRhythms(tonic, step, fifthsCirle, numMeasures):
#     rhythms = makeRhythms(numMeasures)
#     notes = fiveFingerStepNotes(tonic, step, fifthsCirle, rhythms)
#     combined = []
#     for i in range(len(notes)):
#         combined.append((notes[i],rhythms[i]))

#     return combined








