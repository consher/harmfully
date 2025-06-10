from midiutil.MidiFile import MIDIFile
from mido import MidiFile
import numpy as np
from note_dict import note2num, num2note, hex2num



# read a MIDI file and return a numpy array containing the melody
def midi_read(filename):

    #read MIDI file
    mf = MidiFile(filename)

    # melody arrays
    mldy_n = []     #notes
    mldy_t = []     #times

    for msg in mf:
        if msg.type == "note_on":
            mldy_n.append(msg.note)
            mldy_t.append(msg.time)
        if msg.type == "set_tempo":
            tempo = msg.tempo
    
    return mldy_n, mldy_t, tempo



# takes a melody array from midi_read and writes to a file
def midi_write(mldy_n_ar,mldy_d_ar,output,tempo=120,vol=True):
    
    mf = MIDIFile(1)     # one tracks
    track = 0           # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, output)
    mf.addTempo(track, time, tempo)

    channels = len(mldy_n_ar) #no. of channels


    # default is all channels have volume 100
    if vol == True:
        vol = np.zeros(channels)
        vol += 100

    T = len(mldy_d_ar)
    timestmps = np.zeros(T)
    
    # generate note timestamps from durations
    for d in range(T):
        if d < T-1:
            timestmps[d+1] = timestmps[d] + mldy_d_ar[d]
        else:
            pass

    # add notes per each channel
    for c in range(channels):
        for i in range(len(mldy_n_ar[c])):
            pitch = mldy_n_ar[c][i]       # pitch from melody list
            
            mf.addNote(track, c, pitch, timestmps[i], mldy_d_ar[i], vol[c])

    # write it to disk
    with open("{0}.mid".format(output), 'wb') as outfile:
        mf.writeFile(outfile)
