from transformers import LlamaForCausalLM, LlamaTokenizer

def loading_llama_model(model, tokenn, checkpoint_dir):
    tokenizer = LlamaTokenizer.from_pretrained(model, token=tokenn)
    model = LlamaForCausalLM.from_pretrained(checkpoint_dir, low_cpu_mem_usage=True)
    #model.to('cuda')

    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        model.resize_token_embeddings(len(tokenizer))

    return model, tokenizer

