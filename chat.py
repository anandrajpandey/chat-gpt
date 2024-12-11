from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the GPT model and tokenizer
print("Loading GPT-2 model...")
try:
    model_name = "gpt2"  # Replace with a different model if needed
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # Set padding token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("Model and tokenizer loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def generate_response(prompt):
    try:
        if not model:
            raise Exception("Model is not loaded.")

        # Tokenize input with padding and attention mask
        inputs = tokenizer(
            prompt, 
            return_tensors="pt", 
            padding=True,  # Ensures inputs are padded
            truncation=True  # Prevents inputs from being too long
        )

        # Generate response using attention_mask
        outputs = model.generate(
            input_ids=inputs["input_ids"], 
            attention_mask=inputs["attention_mask"], 
            max_length=100, 
            num_return_sequences=1, 
            do_sample=True
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I had trouble processing your request."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    prompt = f"User: {user_message}\nAssistant:"
    response = generate_response(prompt)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
