import numpy as np
import json 
import time

# Get features
data_path = "/Users/marcoferreira/Now/Programming/Sound Classifier/FSD50K/Data/data.json"
with open (data_path, "r") as json_file:
    data = json.load(json_file)

ftrs = np.array(data["features"])

# Apply Normalization
norm_var = {}
ftrs_mean = np.mean(ftrs, axis = 0)
ftrs_variance = np.sum(((ftrs - ftrs_mean) ** 2), axis = 0)/ ftrs.shape[0]
norm_var["mean"] = ftrs_mean.tolist()
norm_var["variance"] = ftrs_variance.tolist()

ftrs_norm = (ftrs - ftrs_mean) / ftrs_variance
data["features"] = ftrs_norm.tolist()

# Dump normalized data and normalization variables into json file
out_dir = "/Users/marcoferreira/Now/Programming/Sound Classifier/FSD50K/Data"
json.dump(data, open(out_dir + "/data_norm.json", "w"), indent=4)
json.dump(norm_var, open(out_dir + "/norm_var.json", "w"), indent=4)

