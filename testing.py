import google.generativeai as genai



# Ensure the API key is set in the environment
genai.configure(api_key='AIzaSyCbA1elHwgftmfJS3GckbM82Tlxwy8O3Y4')

# Initialize the model
model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")

# Generate content
response = model.generate_content("Explain the theory of relativity in simple terms.")
print(response.text)
