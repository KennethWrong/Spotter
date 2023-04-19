import pandas as pd
import numpy as np
import torch

import matplotlib.pyplot as plt
import neattext.functions as nfx
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class EmotionModel:
    def __init__(self) -> None:
        
        self.tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")

        self.model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-emotion")

    def get_emotion(self, text):
        input_ids = self.tokenizer.encode(text + '</s>', return_tensors='pt')

        output = self.model.generate(input_ids=input_ids,
                    max_length=2)
        
        dec = [self.tokenizer.decode(ids) for ids in output]
        label = dec[0].split(" ")
        return label[-1]


if __name__ == "__main__":
    model = EmotionModel()
    print(model.get_emotion("I just scored a goal!"))
    