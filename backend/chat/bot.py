import numpy as np
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.neighbors import KDTree
import os

# Установка переменной окружения TOKENIZERS_PARALLELISM в значение "false"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

m = 'cointegrated/rubert-tiny'

tokenizer = AutoTokenizer.from_pretrained(m)
model = AutoModel.from_pretrained(m)


def normalize(v):
    return v / sum(v**2)**0.5


def embed_rubert(text, mean=False):
    encoded_input = tokenizer(text, padding=True, truncation=True, max_length=128, return_tensors='pt')
    # В режиме экспдуатации сети подаем эмбеддинги на вход модели
    with torch.no_grad():
        model_output = model(**encoded_input)
    sentence_embeddings = model_output[0][:, 0]
    sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings)
    return sentence_embeddings[0].numpy()


current_directory = os.getcwd()
file_name = 'ds.xlsx'
file_path = os.path.join(current_directory, 'chat', file_name)
data = pd.read_excel(file_path)

questions = data.iloc[:, 0].tolist()
answers = data.iloc[:, 1].tolist()
images = data.iloc[:, 2].tolist()

data = pd.DataFrame({'q': questions, 'a': answers, 'i': images})

vectors = np.stack([embed_rubert(t) for t in data.q])
index = KDTree(vectors)


def respond(text):
    distances, indices = index.query(embed_rubert([text])[np.newaxis, :], k=3)
    if distances[0][0] > 0.77:
        np.random.seed()
        return f'Кажется, у меня нет ответа на ваш вопрос. Может быть, вы хотите знать, ' \
               f'{data.q[np.random.choice(len(data.q))]}', 'None'
    else:
        i = 'None' if len(str(data.i[indices[0][0]])) < 5 else data.i[indices[0][0]]
        return data.a[indices[0][0]], i