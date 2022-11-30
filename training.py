# for training 
import numpy as np
import json
import pickle
import random

import nltk
from nltk import tokenize
from nltk.stem import WordNetLemmatizer
from sklearn import metrics

from tensorflow import keras
from tensorflow.keras.optimizers import SGD

lm = WordNetLemmatizer()

# loading the json file 
with open('intents.json','r') as f:
    intents = json.load(f)

words = []
classes = []
documents = []
ignore_words = ['?','!','.',',']
all_patterns = []

for intent in intents['intents']:
    # print("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    # print(f'current intent is  : {intent}')
    for pattern in intent['patterns']:
        # print(f"patterns are : {pattern}")
        word_list = tokenize.word_tokenize(pattern)
        # print(f"tokenized words : {word_list}")
        words.append(word_list)
        # print(f"appended words are : {words}")

        documents.append(((word_list),intent['tag']))
        # print(f"appended ducuments are : {documents}")

        if intent['tag'] not in classes:
            classes.append(intent['tag'])
        # print(f"appended classes are : {classes}")
        
        # print('---------------------------------')

# lemmetize the words 

current_word = []

for word in words:
    # lemmitized_words = lm.lemmatize(words) 
    for word1 in word:
        current_word.append(word1)
# print(f"current words :{current_word}")

words = current_word
words = [lm.lemmatize(word) for word in words if word not in ignore_words]

# create the unique items 
words = sorted(set(words))
# print(words)
print(f"len of words : {len(words)}")

classes = sorted(set(classes))
# print(classes)

# save the words, classes in pickle 
pickle.dump(words, open('words.pkl','wb'))
pickle.dump(classes, open('classes.pkl','wb'))




training = []
# output_empty = np.zeros(len(classes),dtype=np.int32)
output_empty = [0] * len(classes)

# output_row = list(output_empty) 
# print(f"this is output row : {output_row}")
# print(f"this is the lenght of classes : {len(classes)}")
# print(f"this is my output_empty {output_empty}")

# print(f"this is our classes : {classes}")
for document in documents:
    # print(f"this is in document 0 {document[0]}, and this is in document 1 {document[1]}")
    bag = []
    word_pattern = document[0] # word_patterns = ['see', 'you', 'later']
    # print(f"this is before word pattern : {word_pattern}")
    word_pattern = [lm.lemmatize(word.lower()) for word in word_pattern] # word_pattern = lemetize(word = 'see';  'you'; 'later';)
    # print(f"this is lemetized word pattern : {word_pattern}")
    for word in words: # word = 'hello'
        # print(f"this is word: {word} , and this is word pattern : {word_pattern} ")
        bag.append(1) if word in word_pattern else bag.append(0)

    # print(f'this bag contains : {bag}') # this is word: you , and this is word pattern : ['see', 'you', 'later'] ; bag = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    output_row = list(output_empty)             
    output_row[classes.index(document[1])] = 1 # setting the value of output row  ; classes.index('bye')
    # print(f"this is our output row : {output_row}")
    training.append([bag,output_row])
    # print(f"this is in appended training : {training}")

    # print(document[0])
    # print("--------------------------")


# print(f'this is len of output empty :{len(output_empty)}')
# print(f"this is our classes index of 'general question' : {classes.index('general question')}")

# training the data 
random.shuffle(training)
training = np.array(training)

x_train = list(training[:,0])
y_train = list(training[:,1])
# print(f"len of x train : {len(x_train[0])}")
# import pandas as pd 

# dfx = pd.DataFrame(x_train)
# print(len(dfx.columns))
# print(len(x_train[0]))
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(len(x_train[0]),)),
    keras.layers.Dense(128 ,activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(64,activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(len(y_train[0]),activation='softmax')
])

sgd = SGD(learning_rate=0.01,decay=1e-6,momentum=0.9,nesterov=True)

model.compile(loss='categorical_crossentropy',optimizer=sgd, metrics=['accuracy'])



hist = model.fit(np.array(x_train),np.array(y_train),epochs=200,batch_size=5,verbose=1)
model.save('va_model.h5',hist)
print('model saved done')













# this is lemetizer example 
# from nltk.stem import WordNetLemmatizer
 
# lemmatizer = WordNetLemmatizer()
 
# print("rocks :", lemmatizer.lemmatize("rocks"))
# print("corpora :", lemmatizer.lemmatize("corpora"))
 
# # a denotes adjective in "pos"
# print("tolds :", lemmatizer.lemmatize("told", pos ="a"))