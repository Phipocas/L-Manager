import os 
import essentia.standard as E
import numpy as np

# print(os.listdir("/Users/marcoferreira/Now/Programming/Sound Classifier/FSD50K/FSD50K.dev_audio")[0])

audio_path = "/Users/marcoferreira/Now/Programming/Sound Classifier/FSD50K/new_sound.wav"
loader = E.essentia.standard.MonoLoader(filename=audio_path)
audio = loader()

effective_duration = E.EffectiveDuration(sampleRate=44100, thresholdRatio=0.4)
dur = effective_duration(audio)
dur_samples = int(44100*dur)

filt = E.MedianFilter(kernelSize = dur_samples)
audio_filtered = filt(audio)

writer = E.MonoWriter(filename = "new_sound_filt.wav")
writer(audio_filtered)



