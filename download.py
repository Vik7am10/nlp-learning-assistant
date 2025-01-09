from transformers import T5Tokenizer, T5ForConditionalGeneration

model_name = "t5-small"  # Alternative model

tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

print("Alternative model and tokenizer loaded successfully!")
