from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the small GPT model and tokenizer
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set to eval mode and use CPU
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def ask_tutor(lesson_title, lesson_content, student_question):
    prompt = f"""
You are a friendly coding tutor helping a student understand lessons.

Lesson Title: {lesson_title}
Lesson Content: {lesson_content[:500]}  # Truncate for short models
Student Question: {student_question}
Tutor's Answer:"""

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_length=inputs['input_ids'].shape[1] + 100,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    response = answer[len(prompt):].strip()
    return response
