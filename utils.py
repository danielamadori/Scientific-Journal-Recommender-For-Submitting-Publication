from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

'''
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping

def crete_model(num_words, embedding_dim, sequence_length, lstm_units, num_classes):
    model = Sequential()

    model.add(Embedding(input_dim=num_words, output_dim=embedding_dim, input_length=sequence_length))
    model.add(LSTM(units=lstm_units, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(units=num_classes, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=[f1_score])
    return model

embedding_dim = 200
lstm_units = 200

model = crete_model(num_words, embedding_dim, sequence_length, lstm_units, num_classes)
model.summary()

'''



# Count frequency of each unique word in the dataset
def word_frequency_analysis(df, feature, max_frequency):
    print(f"Word frequency analysis for feature: {feature}\n")

    counter = Counter()
    for row in df[feature]:
        counter.update(row.split())

    frequency_data = [len(counter)]

    print("Number of unique words: ", frequency_data[0])
    for frequency in range(2, max_frequency):
        number = sum(count >= frequency for count in counter.values())
        print(f"Number of words with frequency >= {frequency}: {number}")
        frequency_data.append(number)

    plt.figure(figsize=(10, 5))
    plt.stem(range(1, max_frequency), frequency_data)
    plt.xlabel("Frequency")
    plt.xticks(range(1, max_frequency))
    plt.ylabel("Number of words")
    plt.grid(True)
    plt.show()

    return frequency_data

# Feature text analysis
def sentences_length_analysis(df, feature_name, length_range):
    lengths = [len(row.split()) for row in df[feature_name]]
    lengths_counts = Counter(lengths)

    for i in range(0, max(lengths)):
        if i not in lengths_counts:
            lengths_counts[i] = 0

    lengths = sorted(lengths_counts.items())

    # Filtering lengths
    lengths = [length for length in lengths if length_range[0] <= length[0] <= length_range[1]]

    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # First subplot - stem plot for number of sequences with this length
    axs[0].stem([length for length, count in lengths], [count for length, count in lengths])
    axs[0].set_title(feature_name + ": Number of sequence with this Length")
    axs[0].set_xlabel("Length")
    axs[0].set_ylabel("Number of sequence")
    axs[0].grid(True)

    # Second subplot - stem plot for inverse cumulative number of sequences with this length
    inverse_cumulative = []
    inverse_cumulative_sum = sum(count for length, count in lengths)
    for length, count in lengths:
        inverse_cumulative.append(inverse_cumulative_sum)
        inverse_cumulative_sum -= count

    axs[1].stem([length for length, count in lengths], [count / inverse_cumulative[0] * 100 for count in inverse_cumulative])
    axs[1].set_title(feature_name + ": Inverse Cumulative Number of sequence with this Length")
    axs[1].set_xlabel("Length")
    axs[1].set_ylabel("Cumulative Number of sequence %")
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()


def plot_class_distribution(y, labels):
    plt.figure(figsize=(10, 5))
    plt.hist(y)
    plt.title("Number of instances per class")
    plt.xlabel("Class")
    plt.ylabel("Number of instances")
    plt.xticks(list(range(len(labels))), labels)
    plt.xticks(rotation=30)
    plt.grid(True)
    plt.show()

def evaluation_report(y_test, y_pred, labels):
    report = classification_report(y_test, y_pred, target_names=labels)  # Assuming class_names is defined
    print(report)

    cm = confusion_matrix(y_test, y_pred)
    cm = cm.astype('float')/cm.sum(axis=1)[:,np.newaxis]

    sns.heatmap(cm, annot=True, fmt='.5%', cmap='Blues', yticklabels=labels, xticklabels=labels, cbar=False)
    plt.show()

    return report