import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

class TextModels:
    @staticmethod
    def generate_response(prompt):
        try:
            inputs = tokenizer(prompt, return_tensors="pt", padding=True, return_attention_mask=True).to(device)
            
            ids = model.generate(
                inputs.input_ids, 
                attention_mask=inputs.attention_mask, 
                max_length=700,
                pad_token_id=tokenizer.pad_token_id,
                num_return_sequences=1,
                do_sample=True,
                temperature=1.2,
                top_k=50,
                top_p=0.9
            )

            decoded = tokenizer.batch_decode(ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)

            return decoded[0]
        except Exception as ex:
            print(f"Exception thrown: {ex}")