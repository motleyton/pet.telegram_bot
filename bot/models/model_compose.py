from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained('/home/anton/Desktop/pythonProject/bot/models/downloaded models/tokenizer_compose')
model = AutoModelForCausalLM.from_pretrained("/home/anton/Desktop/pythonProject/bot/models/downloaded models/model_compose")
