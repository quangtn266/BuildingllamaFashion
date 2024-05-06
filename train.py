import llama
import torch
import pandas as pd
from torch.utils.data import Dataset, random_split
from transformers import TrainingArguments, Trainer
from transformers import LlamaForCausalLM, LlamaTokenizer

MODEL = 'TinyPixel/small-llama2'
DATA_FILE_PATH = '/content/drive/MyDrive/BuildingLLMFashion/data/page_number.csv'

texts = pd.read_csv(DATA_FILE_PATH)['Description']

tokenizer = LlamaTokenizer.from_pretrained(MODEL, token=" ") # Huggingface access token
model = LlamaForCausalLM.from_pretrained(MODEL).cuda()

class TextDataset(Dataset):
    def __init__(self, txt_list, tokenizer, max_length):
        self.labels = []
        self.input_ids = []
        self.attn_masks = []
        for txt in txt_list:
            encodings_dict = tokenizer(txt, truncation = True, max_length = max_length, padding = "max_length")
            self.input_ids.append(torch.tensor(encodings_dict['input_ids']))
            self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']))
    def __len__(self): return len(self.input_ids)
    def __getitem__(self, idx): return self.input_ids[idx], self.attn_masks[idx]

if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    model.resize_token_embeddings(len(tokenizer))

dataset = TextDataset(texts, tokenizer, max_length = max([len(tokenizer.encode(text)) for text in texts]))
train_dataset, val_dataset = random_split(dataset, [int(0.9 * len(dataset)), len(dataset) - int(0.9 * len(dataset))])

training_args = TrainingArguments(
                                  save_steps = 5000,
                                  warmup_steps = 10,
                                  logging_steps = 100,
                                  weight_decay = 0.05,
                                  num_train_epochs = 100,
                                  logging_dir = './logs',
                                  output_dir = './results',
                                  per_device_eval_batch_size = 1,
                                  per_device_train_batch_size = 1)

torch.cuda.empty_cache()


Trainer(model = model,
        args = training_args,
        eval_dataset = val_dataset,
        train_dataset = train_dataset,
        data_collator = lambda data: {'input_ids': torch.stack([f[0] for f in data]), 'attention_mask': torch.stack([f[1] for f in data]), 'labels': torch.stack([f[0] for f in data])}).train()

sample_outputs = model.generate(tokenizer('', return_tensors="pt").input_ids.cuda(),
                                do_sample = True,
                                top_k = 50, pad_token_id=tokenizer.eos_token_id,
                                max_length = 100,
                                top_p = 0.95,
                                temperature = 1.0)