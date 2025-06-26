from transformers import pipeline

# Use instruction-following model
tutor = pipeline("text2text-generation", model="google/flan-t5-small", device=-1)

questions = [
    "What is a variable in Python?",
    "Explain what a function is in programming.",
    "What is the use of a for loop?",
    "Define a class in Python."
]

for question in questions:
    prompt = f"Explain to a 13-year-old student: {question}"
    response = tutor(prompt, max_new_tokens=100)[0]['generated_text']
    print(f"\nStudent Question: {question}")
    print(f"Tutor's Answer: {response}")
