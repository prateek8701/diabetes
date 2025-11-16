def get_health_advice(question):
    question_lower = question.lower()
    
    # Diet-related questions
    if 'diet' in question_lower or 'eat' in question_lower or 'food' in question_lower:
        if 'diabetes' in question_lower or 'sugar' in question_lower:
            return {
                'answer': "For diabetes management, focus on low glycemic index foods like whole grains, lean proteins, non-starchy vegetables, and healthy fats. Avoid refined sugars, white bread, and sugary drinks.",
                'tips': [
                    "Choose whole grains over refined grains",
                    "Include plenty of vegetables in every meal",
                    "Opt for lean proteins like chicken, fish, and legumes",
                    "Limit processed and packaged foods",
                    "Monitor portion sizes"
                ]
            }
        return {
            'answer': "A balanced diet should include plenty of fruits, vegetables, whole grains, lean proteins, and healthy fats. Aim for variety and moderation.",
            'tips': [
                "Eat a rainbow of colorful fruits and vegetables",
                "Stay hydrated with water",
                "Limit processed foods and added sugars",
                "Include fiber-rich foods",
                "Practice mindful eating"
            ]
        }
    
    # Exercise-related questions
    elif 'exercise' in question_lower or 'workout' in question_lower or 'physical' in question_lower:
        return {
            'answer': "Regular physical activity is crucial for managing blood sugar levels and overall health. Aim for at least 150 minutes of moderate aerobic activity per week.",
            'tips': [
                "Start with 30 minutes of walking daily",
                "Include strength training twice a week",
                "Try activities you enjoy like dancing, swimming, or cycling",
                "Check blood sugar before and after exercise",
                "Stay consistent with your routine"
            ]
        }
    
    # Blood sugar monitoring
    elif 'blood sugar' in question_lower or 'glucose' in question_lower or 'monitor' in question_lower:
        return {
            'answer': "Regular blood sugar monitoring helps you understand how food, activity, and stress affect your levels. Keep a log and look for patterns.",
            'tips': [
                "Monitor at consistent times daily",
                "Track your readings in a journal",
                "Note what you ate before each reading",
                "Check before and 2 hours after meals",
                "Share your log with your healthcare provider"
            ]
        }
    
    # Stress management
    elif 'stress' in question_lower or 'anxiety' in question_lower or 'mental' in question_lower:
        return {
            'answer': "Stress can significantly impact blood sugar levels. Managing stress through relaxation techniques and mindfulness is important for diabetes management.",
            'tips': [
                "Practice deep breathing exercises daily",
                "Try meditation or yoga",
                "Ensure 7-8 hours of quality sleep",
                "Connect with friends and family",
                "Consider professional counseling if needed"
            ]
        }
    
    # Sleep-related questions
    elif 'sleep' in question_lower or 'rest' in question_lower:
        return {
            'answer': "Quality sleep is essential for blood sugar regulation and overall health. Poor sleep can increase insulin resistance.",
            'tips': [
                "Maintain a consistent sleep schedule",
                "Create a relaxing bedtime routine",
                "Keep your bedroom cool and dark",
                "Avoid screens 1 hour before bed",
                "Limit caffeine in the afternoon"
            ]
        }
    
    # Medication-related questions
    elif 'medication' in question_lower or 'medicine' in question_lower or 'insulin' in question_lower:
        return {
            'answer': "Always take medications as prescribed by your healthcare provider. Never adjust doses without consulting them first.",
            'tips': [
                "Take medications at the same time daily",
                "Set reminders on your phone",
                "Keep a medication log",
                "Report any side effects to your doctor",
                "Never skip doses"
            ]
        }
    
    # Default response
    else:
        return {
            'answer': "I can help with questions about diet, exercise, blood sugar monitoring, stress management, sleep, and general diabetes care. What would you like to know?",
            'tips': [
                "Ask about healthy eating habits",
                "Learn about exercise recommendations",
                "Get tips on blood sugar monitoring",
                "Understand stress management",
                "Discover sleep improvement strategies"
            ]
        }
