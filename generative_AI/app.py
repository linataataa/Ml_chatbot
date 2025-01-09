from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

# Set the device to CPU
device = torch.device("cpu")
print(f"Using device: {device}")

# Load the model and tokenizer
MODEL_NAME = "Mohammedbendahrass/threat-detection-gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
model.to(device)  # Move the model to CPU

# Test the model with a sample prompt
test_prompt = "THREAT_NAME: Phishing attack\nTHREAT_DESCRIPTION:"
inputs = tokenizer(test_prompt, return_tensors="pt").to(device)

# Generate text
max_length = len(inputs.input_ids[0]) + 512 
outputs = model.generate(
    inputs.input_ids,
    max_length=max_length,
    num_beams=5,
    temperature=0.6,
    no_repeat_ngram_size=2,
    early_stopping=True
)

# Decode and print the output
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Generated Text:")
print(generated_text)