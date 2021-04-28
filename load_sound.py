import essentia.standard as E
import numpy as np
import json
import matplotlib.pyplot as plt


def extract_features(audio):
    # Get audio features of sound for inference
    w = E.Windowing(type='hann', size=1024)
    spectrum = E.Spectrum()
    mfcc=E.MFCC()
    frame_cnt = 0
    mfcc_total = np.array([[]])
    hop_size = 512

    # # Computes effective duration of clip and time index for max amplitude
    # effective_duration = E.EffectiveDuration(sampleRate=44100, thresholdRatio=0.4)
    # dur = effective_duration(audio)
    # dur_samples = int(44100*dur)

    # try:
    #     max_i = audio.tolist().index(np.max(np.abs(audio)))
    # except Exception:
    #     max_i = audio.tolist().index(-np.max(np.abs(audio)))

    # Computes MFCC for samples around max amplitude time
    for frame in E.FrameGenerator(audio, frameSize=1024, hopSize=512, startFromZero=True):
        spec = spectrum(w(frame))
        mfcc_bands, mfcc_coeffs = mfcc(spec)
        mfcc_total = np.append(mfcc_total, mfcc_coeffs)
        frame_cnt += 1

    mfcc_total = np.reshape(mfcc_total, newshape=(frame_cnt, len(mfcc_coeffs)))
    # mfcc_total = np.mean(mfcc_total, axis=0)

    return mfcc_total

def normalize_features(ftrs):
    # Get normalization variables
    norm_path = "/Users/marcoferreira/Now/Programming/Sound Classifier/FSD50K/Data/norm_var.json"
    with open(norm_path, "r") as json_file:
        norm_var = json.load(json_file)

    # Normalize input data
    ftrs_mean = np.array(norm_var["mean"])
    ftrs_variance = np.array(norm_var["variance"])
    mfcc_norm = (ftrs - ftrs_mean) / ftrs_variance

    return mfcc_norm 

def main():
    # Load sound
    # audio_path = "/Users/marcoferreira/Now/Programming/Sound Classifier/FSD50K/FSD50K.eval_audio/424616.wav"
    audio_path = "/Users/marcoferreira/Now/Programming/Sound Classifier/FSD50K/new_sound.wav"
    loader = E.essentia.standard.MonoLoader(filename=audio_path, sampleRate = 44100)
    audio = loader()

    ftrs = extract_features(audio = audio)
    ftrs_norm = normalize_features(ftrs = ftrs)

    # Dump sound features in json file
    sound_path = "/Users/marcoferreira/Now/Programming/Sound Classifier/FSD50K/new_sound.json"
    json.dump(ftrs_norm.tolist(), open(sound_path, "w"), indent=4)



if __name__ == "__main__":
    main()