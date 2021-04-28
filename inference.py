from tensorflow import keras
import numpy as np
import json

model = keras.models.load_model('Model')

# Script to use while essentia and tensorflow are incompatible

# Load Features of sound to classify
with open("new_sound.json", "r") as json_file:
    new_sound = np.array(json.load(json_file))
# new_sound = np.reshape(new_sound, (1, len(new_sound)))

# Load Data
with open("Data/data.json", "r") as fp:
    data = json.load(fp)

data_mapping = data["mapping"]
data_labels = data["labels"]

# Model prediction
prediction_list = model.predict_classes(new_sound)
prediction = np.bincount(prediction_list).argmax()
print(f"This sound fits in the {data_mapping[data_labels.index(prediction)]} category")


