from midiutil.MidiFile import MIDIFile
from mido import MidiFile
import numpy as np
from note_dict import note2num, num2note, hex2num

# legend: 0,1,2,3,4,5,6,7,8,9,a,b = mod12 notes in hex format
#         c                       = add a pause of 1 beat

#takes list of (one or more) melody strings and concatonates it into a single MIDI file
def midi_gen(mel_list,name):
    mf = MIDIFile(1)     # one tracks
    track = 0           # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, name)
    mf.addTempo(track, time, 120)

    volume = 100

    # iterative beat value
    b = 0
    increment = 1 # amount to increment by

    for j in range(len(mel_list)):
        for i in mel_list[j]:

            #allows break in tune
            if hex2num[i] == 12:
                b += 1
            
            else:
                pitch = hex2num[i] + 60     # note converted from our format to MIDI format (+ 60)
                time = b                    # start on beat b
                duration = 1                # 1 beat long
                mf.addNote(track, j, pitch, time, duration, volume)

                b += increment # update beat by a given increment
        
        b = 0 # reset beat

    # write it to disk
    with open("{0}.mid".format(name), 'wb') as outf:
        mf.writeFile(outf)




# read a MIDI file and return a numpy array containing the melody
def midi_read(filename):

    #read MIDI file
    mf = MidiFile(filename)

    # melody string
    mldy_arry = []

    for msg in mf:
        if msg.type == "note_on":
            mldy_arry.append(msg.note)
    
    return mldy_arry



# takes a melody array from midi_read and writes to a file
def midi_write(mldy_arry,output):
    
    mf = MIDIFile(1)     # one tracks
    track = 0           # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, output)
    mf.addTempo(track, time, 120)

    volume = 100

    # iterative beat value
    b = 0
    increment = 1 # amount to increment by

    for j in range(len(mldy_arry)):
        for i in mldy_arry[j]:
            pitch = i    # note converted from our format to MIDI format (+ 60)
            time = b                    # start on beat b
            duration = 1                # 1 beat long
            mf.addNote(track, j, pitch, time, duration, volume)

            b += increment # update beat by a given increment

        b = 0 # reset beat counter

    # write it to disk
    with open("{0}.mid".format(output), 'wb') as outfile:
        mf.writeFile(outfile)
