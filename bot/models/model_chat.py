from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained('/home/anton/Desktop/pythonProject/bot/models/downloaded models/tokenizer_chat')
model = AutoModelForCausalLM.from_pretrained("/home/anton/Desktop/pythonProject/bot/models/downloaded models/model_chat")

def respond_to_dialog(texts):
        prefix = '\nx:'
        for i, t in enumerate(texts):
            prefix += t
            prefix += '\nx:' if i % 2 == 1 else '\ny:'
        tokens = tokenizer(prefix, return_tensors='pt')
        tokens = {k: v.to(model.device) for k, v in tokens.items()}
        end_token_id = tokenizer.encode('\n')[0]
        size = tokens['input_ids'].shape[1]
        output = model.generate(
            **tokens,
            eos_token_id=end_token_id,
            do_sample=True,
            max_length=size+128,
            repetition_penalty=3.2,
            temperature=1,
            num_beams=3,
            length_penalty=0.01,
            pad_token_id=tokenizer.eos_token_id
        )
        decoded = tokenizer.decode(output[0])
        result = decoded[len(prefix):]
        return result.strip()


