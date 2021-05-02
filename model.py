import os
import datetime
import json
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow import keras
import matplotlib.pyplot as plt

def train_model(data, epochs):

    #load data
    inputs = np.array(data["features"])
    targets = np.array(data["labels"])

    #split the data into train and test sets
    inputs_train, inputs_test, targets_train, targets_test = train_test_split(inputs, targets, test_size=0.3)
    
    #build the network architecture
    model = keras.Sequential([
        #input layer
        # keras.layers.InputLayer(input_shape=inputs.shape[1]),

        #1 hidden layer with regularization
        keras.layers.Dense(512, activation="relu", kernel_regularizer=keras.regularizers.l2(0), input_shape=(inputs.shape[1],)),
        
        #dropout for overfitting prevention
        keras.layers.Dropout(0.3),
    
        #2 hidden layer
        keras.layers.Dense(256, activation="relu", kernel_regularizer = keras.regularizers.l2(0)),
        keras.layers.Dropout(0.3),

        # #3 hidden layer
        # keras.layers.Dense(256, activation="relu", kernel_regularizer = keras.regularizers.l2(0)),
        # # keras.layers.Dropout(0.3),

        #4 hidden layer
        keras.layers.Dense(64, activation="relu", kernel_regularizer = keras.regularizers.l2(0)),
        keras.layers.Dropout(0.3),

        #output layer
        keras.layers.Dense(np.max(targets) + 1, activation="softmax")

    ])

    #compile network
    optimizer = keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.summary()

    #train network
    history = model.fit(inputs_train, targets_train,
            validation_data=(inputs_test, targets_test),
            epochs=epochs,
            batch_size=32)


    model_path = "Model"
    model.save(model_path)

    history_path = model_path + "/history.json"
    history_data = history.history
    history_data["epochs"] = epochs
    json.dump(history_data, open(history_path + f"_{datetime.datetime.now().day}{datetime.datetime.now().month}_{datetime.datetime.now().hour}{datetime.datetime.now().minute}", "w"), indent=4)

    return history

def plot_history(history):
    fig, axs = plt.subplots(2)

    #create the accuracy subplot
    axs[0].plot(history.history["accuracy"], label="train accuracy")
    axs[0].plot(history.history["val_accuracy"], label = "test accuracy")
    axs[0].set_ylabel("Accuracy")
    axs[0].legend(loc = "lower right")
    axs[0].set_title("Accuracy eval")

    #create the error subplot
    axs[1].plot(history.history["loss"], label="train error")
    axs[1].plot(history.history["val_loss"], label = "test error")
    axs[1].set_ylabel("Error")
    axs[1].set_xlabel("Epoch")
    axs[1].legend(loc = "upper right")
    axs[1].set_title("Error eval")

    plt.show()


def main():
    # Load Data
    with open("Data/data_norm.json", "r") as json_file:
        data_norm = json.load(json_file)

    #initialize and train the model
    history = train_model(data=data_norm, epochs = 50)

    #plot accuracy and error over epochs
    plot_history(history)


if __name__ == "__main__":
    main()