from tensorflow import keras
import essentia.standard as E
import numpy as np
import json


def extract_features(audio):
    # Get audio features of sound for inference
    w = E.Windowing(type='hann', size=1024)
    spectrum = E.Spectrum()
    mfcc=E.MFCC()
    frame_cnt = 0
    mfcc_total = np.array([[]])
    hop = 250

    # Computes sound energy and threshold
    array_energy = np.square(np.abs(audio))
    mean_energy = np.mean(array_energy)
    threshold = 0.2 * mean_energy

    for frame in E.FrameGenerator(audio, frameSize=1024, hopSize=hop, startFromZero=True):
        frame_energy = np.square(np.abs(frame))
        frame_mean_energy = np.mean(frame_energy)
        if frame_mean_energy >= threshold:
            spec = spectrum(w(frame))
            mfcc_bands, mfcc_coeffs = mfcc(spec)
            mfcc_total = np.append(mfcc_total, mfcc_coeffs)
            frame_cnt += 1
    mfcc_total = np.reshape(mfcc_total, newshape=(frame_cnt, len(mfcc_coeffs)))
    mfcc_total = np.mean(mfcc_total, axis=0)
    mfcc_total = np.reshape(mfcc_total, newshape=(1, 13))
    return mfcc_total

def normalize_features(ftrs):
    # Get normalization variables
    norm_path = "Data/norm_var.json"
    with open(norm_path, "r") as json_file:
        norm_var = json.load(json_file)

    # Normalize input data
    ftrs_mean = np.array(norm_var["mean"])
    ftrs_variance = np.array(norm_var["variance"])
    mfcc_norm = (ftrs - ftrs_mean) / ftrs_variance

    return mfcc_norm 

def main():
    # Load sound
    audio_path = "../FSD50K_Data/FSD50K.eval_audio/65880.wav"
    loader = E.MonoLoader(filename=audio_path, sampleRate = 44100)
    audio = loader()

    ftrs = extract_features(audio = audio)
    ftrs_norm = normalize_features(ftrs = ftrs)

    # Load Data
    with open("Data/data.json", "r") as fp:
        data = json.load(fp)

    data_mapping = data["mapping"]
    data_labels = data["labels"]

    # Load Model
    model = keras.models.load_model('Model')

    # Model prediction
    prediction = model.predict_classes(ftrs_norm)
    print(f"This sound fits in the {data_mapping[data_labels.index(prediction)]} category")


if __name__=="__main__":
    main()