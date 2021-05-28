from fastai.text import *
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
#data_path = Path('./resources')

#data = pd.read_json(data_path/'Sarcasm_Headlines_Dataset_v2.json', lines=True)

import fastai
from fastai.text.all import * 

dls_lm = TextDataLoaders.from_df(
    data, 
    path=data_path,
    #text_col='headline',
    valid_pct=0,
    is_lm=True
)

learn = language_model_learner(
    dls_lm, 
    arch=AWD_LSTM, 
    drop_mult=0.5,
    path=data_path,
).to_fp16()

learn.fine_tune(4, base_lr=1e-2)

learn.predict('', n_words=5, no_unk=True)