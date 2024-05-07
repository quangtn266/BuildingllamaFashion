from transformers import LlamaForCausalLM, LlamaTokenizer

MODEL = 'TinyPixel/small-llama2'

tokenizer = LlamaTokenizer.from_pretrained(MODEL, token=" ") # Huggingface access token
model = LlamaForCausalLM.from_pretrained("results", low_cpu_mem_usage = True)
model.to('cuda')

if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    model.resize_token_embeddings(len(tokenizer))

batch = tokenizer("Routine", return_tensors = "pt")
print(tokenizer.decode(model.generate(batch["input_ids"].cuda(), max_length=100)[0]))
