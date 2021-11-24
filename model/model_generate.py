import time

import textwrap
import torch
from transformers import GPT2Tokenizer


try:
    model = torch.load('model/model.pt', map_location=torch.device('cpu'))
    tokenizer = GPT2Tokenizer.from_pretrained('sberbank-ai/rugpt3small_based_on_gpt2')
except Exception as e:
    print(f'Loading model error: {e.args}')


def generate(prompt, len_gen=100, temperature=.8):
    if torch.cuda.is_available():    
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    try:
        generated = tokenizer.encode(prompt)
        context = torch.tensor([generated]).to(device)
        past = None

        for i in range(len_gen):
            print(f'Iter-{i} in {time.strftime("%M:%S", time.localtime())}: Get values for out and past')
            output, past = model(context, past_key_values=past).values()
            output = output / temperature
            print(f'Iter-{i} in {time.strftime("%M:%S", time.localtime())}: Token distributions')
            token = torch.distributions.Categorical(logits=output[..., -1, :]).sample()
            print(f'Iter-{i} in {time.strftime("%M:%S", time.localtime())}: Token to list')
            generated += token.tolist()
            print(f'Iter-{i} in {time.strftime("%M:%S", time.localtime())}: Token unsqueeze')
            context = token.unsqueeze(0)
        print(f'Iter-{len_gen} in {time.asctime()}: Decode tokenizer')
        sequence = tokenizer.decode(generated)
    except Exception as e:
        print(f"Error: {e.args}")
    return textwrap.fill(sequence, 120)
