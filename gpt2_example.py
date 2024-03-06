from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch


def generate_and_save_function(prompt_text, model_name="gpt2", filename="sum_function.py"):
    # Ensure PyTorch is imported
    import torch

    # Load pre-trained model tokenizer (vocabulary)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)

    # Load pre-trained model (weights)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Encode context the generation is conditioned on
    input_ids = tokenizer.encode(prompt_text, return_tensors="pt")

    # Convert attention_mask to a PyTorch tensor
    attention_mask = torch.tensor([1] * len(input_ids[0]), dtype=torch.long).unsqueeze(0)

    # Generate text with adjusted parameters for sample-based generation
    output = model.generate(
        input_ids,
        max_length=150,  # Adjust based on expected length of output
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        do_sample=True,  # Enable sampling to use temperature and top_p effectively
        temperature=0.5,  # Adjust to control randomness
        top_k=50,
        top_p=0.95,
        attention_mask=attention_mask,  # Using the tensor attention_mask
    )

    # Decode the generated text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Assuming the function starts at the beginning of the generated text and ends before an additional double newline
    function_code = generated_text.split("\n\n")[0].strip()

    # Write the extracted function to a file
    with open(filename, "w") as file:
        file.write(function_code)
        print(f"Function written to {filename}")


if __name__ == "__main__":
    prompt = """
    # Python task: Write a simple function named 'f' that takes two integers and returns their sum.
    # The function should look like this:
    """
    generate_and_save_function(prompt)
