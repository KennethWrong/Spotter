import pandas as pd
import numpy as np
import torch

import matplotlib.pyplot as plt
import neattext.functions as nfx
import torch.nn as nn

class EmotionModel(nn.Module):
    def __init__(self, vocab_size, output_size, embedding_matrix, hidden_dim, n_layers, drop_prob=0.5):
        super(EmotionModel, self).__init__()
        self.output_size = output_size
        self.n_layers = n_layers
        self.hidden_dim = hidden_dim
        
        embedding_dim = embedding_matrix.size(1)
        self.embedding = nn.Embedding(vocab_size, embedding_dim, _weight=embedding_matrix)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, n_layers, dropout=drop_prob, batch_first=True)
        self.dropout = nn.Dropout(drop_prob)
        self.fc = nn.Linear(hidden_dim, output_size)
        self.sigmoid = nn.Sigmoid()
        self.Softmax = nn.Softmax(dim=1)
        
    def forward(self, x, hidden):
        batch_size = x.size(0)
        embeds = self.embedding(x) # [1, 79, 200]
        lstm_out, hidden = self.lstm(embeds, hidden) # [1, 79, 128]

        lstm_out = lstm_out.contiguous().view(-1, self.hidden_dim)  #[79, 128]
    
        
        out = self.dropout(lstm_out) # [79, 128]
        out = self.fc(out) # [79, 8]
        out = self.sigmoid(out)
        
        out = out.view(batch_size, -1, self.output_size)
        out = out[:, -1]  
        out = self.Softmax(out)
        
        return out, hidden
    
    def init_hidden(self, batch_size, device):
        weight = next(self.parameters()).data
        hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(torch.float32).to(device),
                      weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(torch.float32).to(device))
        return hidden