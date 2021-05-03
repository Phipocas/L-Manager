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
    
    mfcc_total = np.array([[]])
    snd_cnt = 0
    test_list = list(clip_dict.keys())

    for filename in os.listdir(path)[:num_files]:
        filename = filename.split(".")[0]
        if filename in clip_dict.keys():
            print(f"Processing sound number {snd_cnt}, with id {filename}")
            
            # Loads Audio
            loader = E.essentia.standard.MonoLoader(filename=os.path.join(path, filename + ".wav"), sampleRate=44100)
            audio = loader()

            # Computes sound energy and threshold
            array_energy = np.square(np.abs(audio))
            mean_energy = np.mean(array_energy)
            threshold = 0.2 * mean_energy

            for frame in E.FrameGenerator(audio, frameSize=1024, hopSize=250, startFromZero=True):
                
                frame_energy = np.square(np.abs(frame))
                frame_mean_energy = np.mean(frame_energy)
                if frame_mean_energy >= threshold:
                    spec = spectrum(w(frame))
                    mfcc_bands, mfcc_coeffs = mfcc(spec)

                    data["mapping"].append(clip_dict[filename])
                    data["features"].append(mfcc_coeffs.tolist())
                    data["labels"].append(float(label_dict[clip_dict[filename]]))

            snd_cnt += 1

    return data

def main():
    # Get clip mapping -> clip_id:label
    csv_path = "../FSD50K_Data/FSD50K.ground_truth/dev.csv"
    clip_map =  get_labels(path=csv_path)

    # Get label mapping -> label_name:label_index
    label_map={}
    csv_path = "../FSD50K_Data/FSD50K.ground_truth/vocabulary.csv"
    with open(csv_path, "r") as csv_file:
        csv_data = csv.reader(csv_file, delimiter = ",")
        for row in csv_data:
            label_map[row[1]] = row[0]
    
    # Extract features
    audio_path = "../FSD50K_Data/FSD50K.dev_audio"
    data = extract_features(clip_dict = clip_map, label_dict = label_map, path = audio_path, num_files = 10)
    
    # Create json file with input data
    out_dir = "Data"
    json.dump(data, open(out_dir + "/data.json", 'w'), indent=4)

if __name__ == "__main__":
    main()