from health_assistant import get_health_advice as get_rule_based_advice

LOCAL_MODEL = None
LOCAL_TOKENIZER = None

def initialize_local_model():
    global LOCAL_MODEL, LOCAL_TOKENIZER
    
    if LOCAL_MODEL is not None:
        return True
    
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
        import torch
        
        print("Loading local AI model (TinyLlama)...")
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        
        LOCAL_TOKENIZER = AutoTokenizer.from_pretrained(model_name)
        LOCAL_MODEL = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            low_cpu_mem_usage=True
        )
        
        print("Local AI model loaded successfully!")
        return True
        
    except Exception as e:
        print(f"Failed to load local AI model: {e}")
        return False

def get_health_advice_local_ai(question):
    if not initialize_local_model():
        return get_rule_based_advice(question)
    
    try:
        from transformers import pipeline
        
        system_prompt = """You are a helpful health assistant specializing in diabetes management. 
Provide concise, practical advice about diet, exercise, blood sugar monitoring, and wellness. 
Keep your response under 100 words and include 2-3 actionable tips."""

        chat = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        
        prompt = LOCAL_TOKENIZER.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
        
        inputs = LOCAL_TOKENIZER(prompt, return_tensors="pt", truncation=True, max_length=512)
        
        if LOCAL_MODEL.device.type == "cuda":
            inputs = {k: v.to("cuda") for k, v in inputs.items()}
        
        outputs = LOCAL_MODEL.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        response = LOCAL_TOKENIZER.decode(outputs[0], skip_special_tokens=True)
        
        if "<|assistant|>" in response:
            response = response.split("<|assistant|>")[-1].strip()
        elif "Assistant:" in response:
            response = response.split("Assistant:")[-1].strip()
        
        lines = response.split('\n')
        answer_text = []
        tips_list = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('-') or line.startswith('•') or any(line.startswith(f'{i}.') for i in range(1, 10)):
                tip = line.lstrip('-•0123456789. ')
                if tip and len(tip) > 5:
                    tips_list.append(tip)
            else:
                answer_text.append(line)
        
        if not tips_list and len(answer_text) > 2:
            sentences = ' '.join(answer_text).split('. ')
            if len(sentences) >= 3:
                tips_list = sentences[-2:]
                answer_text = sentences[:-2]
        
        return {
            'answer': ' '.join(answer_text) if answer_text else response,
            'tips': tips_list[:5] if tips_list else []
        }
        
    except Exception as e:
        print(f"Local AI Error: {e}")
        return get_rule_based_advice(question)
