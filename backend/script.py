from transformers import pipeline
import json

def generate_structured_json(ocr_text, structure_prompt):
    """
    Generate a structured JSON string from OCR text using a Hugging Face model.

    Parameters:
        ocr_text (str): The raw OCR text.
        structure_prompt (str): A description or example structure to instruct the model.

    Returns:
        str: The generated structured JSON as a string.
    """
    # Load a pre-trained model from Hugging Face that can handle text generation
    model_name = "facebook/bart-large"  # You can use other models like 't5-base'
    generator = pipeline("text2text-generation", model=model_name)

    # Combine the structure prompt with the OCR text
    prompt = f"{structure_prompt}\n\nOCR Text:\n{ocr_text}"

    # Generate structured output
    result = generator(prompt, max_length=512, num_return_sequences=1)[0]['generated_text']

    try:
        # Attempt to parse the result as JSON to ensure it's valid
        json_result = json.loads(result)
        return json.dumps(json_result, indent=4)
    except json.JSONDecodeError:
        return "Error: The model output could not be parsed as JSON.\nOutput:\n" + result

# Example usage
if __name__ == "__main__":
    ocr_text = "Ingredients: Water, Sugar, Lemon Juice, Natural Flavors."
    structure_prompt = "Convert the following OCR text into a structured JSON with fields 'ingredients', each ingredient listed as an item in an array."

    structured_json = generate_structured_json(ocr_text, structure_prompt)
    print("Generated JSON:\n", structured_json)
