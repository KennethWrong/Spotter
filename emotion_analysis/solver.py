import pandas as pd
import torch
from torchtext.data import get_tokenizer
from collections import Counter
from keras_preprocessing.sequence import pad_sequences
import numpy as np
from sklearn.model_selection import train_test_split
from model import EmotionModel
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import tqdm

def to_categorical(y, num_classes=None, dtype="float32"):
    y = np.array(y, dtype="int")
    input_shape = y.shape

    # Shrink the last dimension if the shape is (..., 1).
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])

    y = y.reshape(-1)
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes), dtype=dtype)
    categorical[np.arange(n), y] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape)
    return categorical

class Solver():
    def __init__(self, device):
        self.device = device
        text_data = pd.read_csv("../data/data.csv")
        text_labels = pd.read_csv("../data/labels.csv")
        
        label_emotion = text_labels['Emotion'].tolist()
        label_encoded = text_labels['emotion_encoded'].tolist()

        label_mapping = {idx: emotion for idx,emotion in zip(label_encoded, label_emotion)}
        vectorized_labels = to_categorical(label_encoded)
        
        sentences = text_data['Clean_Text'].tolist()
        full_doc = " ".join([str(s) for s in sentences])
        tokenizer = get_tokenizer("basic_english")

        tokenized_doc = tokenizer(full_doc)
        
        vocab = list(set(tokenized_doc))

        tokens_map_wn = {token:idx+1 for idx,token in enumerate(vocab)}
        tokens_map_nw = {idx+1:token for idx,token in enumerate(vocab)}
        tokens_map_nw[0] = ""
        tokens_map_wn[""] = 0

        

        sentence_tokenized = [tokenizer(str(s)) for s in sentences]
        sentence_tokenized = [[tokens_map_wn[w] for w in s] for s in sentence_tokenized]
        
        max_sequence_length = max([len(s) for s in sentence_tokenized])
        vocab_size = len(vocab) + 1

        sentence_tokenized_p = pad_sequences(sentence_tokenized, maxlen=max_sequence_length)
        
        
        sentence_tokenized_p = np.array(sentence_tokenized_p)

        glove_file = "glove.6B.200d.txt"
        glove_path = "../data/glove/" + glove_file
        
        glove = {}

        with open(glove_path, "r", encoding="utf-8") as f:
            for line in f:
                values = line.split()
                word = values[0]
                coefs = np.asarray(values[1:], dtype='float32')
                glove[word] = coefs
        
        embedding_matrix = np.zeros((vocab_size, 200), dtype="float32")


        for token in tokenized_doc:
            embedding_vector = glove.get(token, None)

            if embedding_vector is not None:
                embedding_matrix[tokens_map_wn[token]] = embedding_vector

        
        sentence_embedded_p = np.array([[embedding_matrix[t,:] for t in q] for q in sentence_tokenized_p.tolist()])
        
        self.label_mapping = label_mapping
        self.labels = label_emotion
        self.vectorized_labels = torch.Tensor(vectorized_labels, device=self.device)
        self.tokens_map_wn = tokens_map_wn
        self.tokens_map_nw = tokens_map_nw
        self.embedding_matrix = torch.Tensor(embedding_matrix, device=self.device).to(torch.float32)


        self.training_data = torch.Tensor(sentence_tokenized_p, device=self.device).to(torch.long)

        # Fields for the model
        self.model = EmotionModel(
            vocab_size= self.embedding_matrix.shape[0],
            output_size= vectorized_labels.shape[1],
            embedding_matrix= self.embedding_matrix,
            hidden_dim= 128,
            n_layers= 2,
            drop_prob=0.2
            ).to(device=self.device)
        self.loss_fn = nn.BCELoss().to(self.device)
        self.optim = torch.optim.Adam(self.model.parameters(), lr=0.005)
    
    def get_train_test_split(self):
        return train_test_split(self.training_data, self.vectorized_labels, test_size=0.3)
    
    def train_step(self, epochs, dataloader, batch_size):
        self.model.train()
        h = self.model.init_hidden(batch_size=batch_size, device=self.device)
        
        for i, (x, y) in enumerate(dataloader):
            h = tuple([e.data for e in h])
            x, y = x.to(self.device), y.to(self.device)
            

            self.optim.zero_grad()

            output, h = self.model(x, h)

            loss = self.loss_fn(output, y.float())

            if i % 200 == 0:
                print(output, y)
                print(i, loss)

            loss.backward()
            self.optim.step()
            # break

    
    def train(self, epochs, batch_size):
        train_X, test_X, train_y, test_y = self.get_train_test_split()
        train_data = TensorDataset(train_X, train_y)
        train_loader = DataLoader(train_data, shuffle=True, batch_size=batch_size)
        for e in range(epochs):
            self.train_step(e+1, train_loader, batch_size)
            



if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    solver = Solver(device=device)
    
    solver.train(epochs=1, batch_size=2)
        
        
    
    