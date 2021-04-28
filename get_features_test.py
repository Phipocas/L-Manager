import os
import time
import csv
import json
import numpy as np
import matplotlib.pyplot as plt
import essentia.standard as E


def get_labels(path):
    clip_map = {}
    with open(path, "r") as csv_file:
        csv_data = csv.reader(csv_file, delimiter = ",")
        line_cnt = 0
        for row in csv_data:
            if line_cnt == 0:
                line_cnt+=1
                continue
            else:
                clip_map[row[0]]=row[1].split(",")[0]
            line_cnt+=1
    return clip_map

            
def extract_features(clip_dict, label_dict, path, num_files):
# Extract features from audio clips
    data = {
            "mapping":[],
            "features":[],
            "labels":[]
        }

    w = E.Windowing(type='hann', size=1024)
    spectrum = E.Spectrum()
    mfcc=E.MFCC()
    # pool=E.essentia.Pool()

    # Computes effective duration of clip and time index for max amplitude
    # effective_duration = E.EffectiveDuration(sampleRate=44100, thresholdRatio=0.4)
    
    mfcc_total = np.array([[]])
    frame_cnt = 0
    test_list = list(clip_dict.keys())

    for filename in os.listdir(path)[:num_files]:
        filename = filename.split(".")[0]
        if filename in clip_dict.keys():
            print(f"Processing sound number {frame_cnt}, with id {filename}")
            
            # Extract MFCCs
            loader = E.essentia.standard.MonoLoader(filename=os.path.join(path, filename + ".wav"), sampleRate=44100)
            audio = loader()
            # dur = effective_duration(audio)
            # dur_samples = int(44100*dur)
            # try:
            #     max_i = audio.tolist().index(np.max(np.abs(audio)))
            # except Exception:
            #     max_i = audio.tolist().index(-np.max(np.abs(audio)))

            for frame in E.FrameGenerator(audio, frameSize=1024, hopSize=512, startFromZero=True):
                spec = spectrum(w(frame))
                mfcc_bands, mfcc_coeffs = mfcc(spec)

                data["mapping"].append(clip_dict[filename])
                data["features"].append(mfcc_coeffs.tolist())
                data["labels"].append(float(label_dict[clip_dict[filename]]))

                frame_cnt += 1

    return data

def main():
    # Get clip mapping -> clip_id:label
    csv_path = "/Users/marcoferreira/Now/Programming/Sound Classifier/FSD50K/FSD50K.ground_truth/dev.csv"
    clip_map =  get_labels(path=csv_path)

    # Get label mapping -> label_name:label_index
    label_map={}
    csv_path = "/Users/marcoferreira/Now/Programming/Sound Classifier/FSD50K/FSD50K.ground_truth/vocabulary.csv"
    with open(csv_path, "r") as csv_file:
        csv_data = csv.reader(csv_file, delimiter = ",")
        for row in csv_data:
            label_map[row[1]] = row[0]
    
    # Extract features
    audio_path = "/Users/marcoferreira/Now/Programming/Sound Classifier/FSD50K/FSD50K.dev_audio"
    data = extract_features(clip_dict = clip_map, label_dict = label_map, path = audio_path, num_files = 10)
    
    # Create json file with input data
    out_dir = "/Users/marcoferreira/Now/Programming/Sound Classifier/FSD50K/Data"
    json.dump(data, open(out_dir + "/data.json", 'w'), indent=4)

if __name__ == "__main__":
        
    main()