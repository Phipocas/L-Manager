import os 
import essentia.standard as E
import numpy as np

# print(os.listdir("/Users/marcoferreira/Now/Programming/Sound Classifier/FSD50K/FSD50K_Data/FSD50K.dev_audio")[0])

# audio_path = "389.wav"
# loader = E.essentia.standard.MonoLoader(filename=audio_path)
# audio = loader()
# audio_filt = audio.copy()

# # Computes sound energy and threshold
# array_energy = np.square(np.abs(audio))
# max_energy = np.mean(array_energy)
# threshold = 0.3 * max_energy

# hop = 250
# w_size = 1024

# # Removes low energy samples
# for i, frame in enumerate(E.FrameGenerator(audio, frameSize=w_size, hopSize=hop, startFromZero=True, lastFrameToEndOfFile=False)):
# 	frame_energy = np.square(np.abs(frame))
# 	frame_mean_energy = np.mean(frame_energy)
# 	if frame_mean_energy < threshold:
# 		try:
# 			audio_filt[i*hop:i*hop+len(frame)] = np.zeros(shape=(len(frame),))
# 		except:
# 			remaining_samples = (i*hop+w_size)-len(audio_filt)
# 			audio_filt[i*hop:i*hop+remaining_samples] = np.zeros(remaining_samples)

# writer = E.MonoWriter(filename = "389_filt.wav")
# writer(audio_filt)



