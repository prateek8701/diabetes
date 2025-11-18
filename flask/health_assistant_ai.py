import os
from health_assistant import get_health_advice as get_rule_based_advice

def get_health_advice_ai(question):
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    if not openai_api_key:
        return get_rule_based_advice(question)
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_api_key)
        
        system_prompt = """You are a knowledgeable and empathetic health assistant specializing in diabetes management and general wellness. 
        Provide helpful, evidence-based advice about diet, exercise, blood sugar monitoring, stress management, and lifestyle choices.
        Always remind users to consult healthcare professionals for medical decisions.
        Keep responses concise (2-3 paragraphs) and include 3-5 actionable tips."""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        ai_answer = response.choices[0].message.content
        
        lines = ai_answer.split('\n')
        answer_text = []
        tips_list = []
        
        in_tips = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.lower().startswith('tips:') or '1.' in line or '2.' in line:
                in_tips = True
            
            if in_tips and (line.startswith('-') or line.startswith('•') or any(line.startswith(f'{i}.') for i in range(1,10))):
                tip = line.lstrip('-•0123456789. ')
                if tip:
                    tips_list.append(tip)
            elif not in_tips:
                answer_text.append(line)
        
        if not tips_list:
            sentences = ' '.join(answer_text).split('. ')
            if len(sentences) > 3:
                tips_list = sentences[-3:]
                answer_text = sentences[:-3]
        
        return {
            'answer': ' '.join(answer_text) if answer_text else ai_answer,
            'tips': tips_list if tips_list else []
        }
        
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return get_rule_based_advice(question)
