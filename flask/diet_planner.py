"""
Diet Plan Generator for Diabetes Predictor
Generates personalized diet plans based on user data and prediction results
"""

def calculate_daily_calories(age, bmi, glucose, has_diabetes):
    """Calculate personalized daily calorie target"""
    # Base calorie calculation
    if bmi < 18.5:
        base_calories = 2200
    elif bmi < 25:
        base_calories = 2000
    elif bmi < 30:
        base_calories = 1800
    else:
        base_calories = 1600
    
    # Adjust for age
    if age > 60:
        base_calories -= 200
    elif age < 30:
        base_calories += 100
    
    # Adjust for diabetes or high glucose
    if has_diabetes or glucose > 140:
        base_calories = min(base_calories, 1800)
    
    # Further reduce if glucose is very high
    if glucose > 180:
        base_calories = min(base_calories, 1600)
    
    return base_calories


def get_macronutrient_breakdown(glucose, insulin, has_diabetes):
    """Get recommended macronutrient breakdown"""
    # Determine if patient has high glucose or insulin resistance
    high_glucose = glucose > 140
    high_insulin = insulin > 150
    
    if has_diabetes or high_glucose:
        carb_range = "35-40%" if glucose > 180 else "40-45%"
        details = "Focus on complex carbs with low glycemic index"
        if high_insulin:
            details += ". Limit simple sugars to manage insulin resistance"
        
        return {
            "carbohydrates": carb_range,
            "protein": "25-30%",
            "healthy_fats": "30-35%",
            "fiber": "30-35g daily",
            "details": details
        }
    else:
        return {
            "carbohydrates": "45-50%",
            "protein": "20-25%",
            "healthy_fats": "25-30%",
            "fiber": "25-30g daily",
            "details": "Balanced diet to maintain healthy blood sugar levels"
        }


def get_diabetic_friendly_foods():
    """Get list of diabetic-friendly foods"""
    return {
        "vegetables": [
            "Leafy greens (spinach, kale, lettuce)",
            "Broccoli and cauliflower",
            "Tomatoes and bell peppers",
            "Cucumber and zucchini",
            "Green beans and asparagus"
        ],
        "proteins": [
            "Skinless chicken and turkey",
            "Fish (salmon, tuna, sardines)",
            "Eggs",
            "Legumes (lentils, chickpeas, beans)",
            "Tofu and tempeh"
        ],
        "grains": [
            "Whole wheat bread",
            "Brown rice and quinoa",
            "Oatmeal",
            "Whole grain pasta",
            "Barley"
        ],
        "fruits": [
            "Berries (strawberries, blueberries)",
            "Apples and pears",
            "Oranges and grapefruits",
            "Peaches",
            "Cherries (in moderation)"
        ],
        "dairy": [
            "Low-fat Greek yogurt",
            "Skim or low-fat milk",
            "Low-fat cottage cheese",
            "Sugar-free yogurt"
        ],
        "healthy_fats": [
            "Avocado",
            "Nuts (almonds, walnuts)",
            "Olive oil",
            "Chia seeds and flax seeds"
        ]
    }


def get_foods_to_avoid():
    """Get list of foods to avoid"""
    return {
        "high_sugar": [
            "Sugary drinks (soda, energy drinks)",
            "Candy and sweets",
            "Pastries and cakes",
            "Ice cream",
            "Sweetened breakfast cereals"
        ],
        "refined_carbs": [
            "White bread and white rice",
            "Regular pasta",
            "Processed snacks",
            "French fries and chips"
        ],
        "unhealthy_fats": [
            "Fried foods",
            "Fatty cuts of meat",
            "Full-fat dairy products",
            "Butter and margarine (in excess)",
            "Processed meats (sausages, bacon)"
        ],
        "high_sodium": [
            "Canned soups",
            "Processed foods",
            "Pickles and olives (in excess)",
            "Salty snacks"
        ]
    }


def generate_meal_suggestions(calories, has_diabetes):
    """Generate meal suggestions for different times of day"""
    breakfast_cals = int(calories * 0.25)
    lunch_cals = int(calories * 0.35)
    dinner_cals = int(calories * 0.30)
    snack_cals = int(calories * 0.10)
    
    return {
        "breakfast": {
            "calories": breakfast_cals,
            "options": [
                "Oatmeal with berries and almonds + boiled eggs",
                "Whole wheat toast with avocado and poached eggs",
                "Greek yogurt with nuts and chia seeds",
                "Vegetable omelet with whole grain toast"
            ]
        },
        "lunch": {
            "calories": lunch_cals,
            "options": [
                "Grilled chicken salad with olive oil dressing",
                "Lentil soup with whole wheat bread and side salad",
                "Brown rice with grilled fish and steamed vegetables",
                "Quinoa bowl with chickpeas and mixed vegetables"
            ]
        },
        "dinner": {
            "calories": dinner_cals,
            "options": [
                "Baked salmon with roasted vegetables and quinoa",
                "Grilled turkey with sweet potato and green beans",
                "Stir-fried tofu with broccoli and brown rice",
                "Chicken breast with cauliflower rice and salad"
            ]
        },
        "snacks": {
            "calories": snack_cals,
            "options": [
                "A handful of almonds or walnuts",
                "Carrot and cucumber sticks with hummus",
                "Apple slices with peanut butter",
                "Low-fat Greek yogurt"
            ]
        }
    }


def generate_weekly_schedule(calories, has_diabetes):
    """Generate a 7-day diet schedule"""
    meals = generate_meal_suggestions(calories, has_diabetes)
    
    schedule = {
        "Monday": {
            "breakfast": meals["breakfast"]["options"][0],
            "lunch": meals["lunch"]["options"][0],
            "dinner": meals["dinner"]["options"][0],
            "snack": meals["snacks"]["options"][0]
        },
        "Tuesday": {
            "breakfast": meals["breakfast"]["options"][1],
            "lunch": meals["lunch"]["options"][1],
            "dinner": meals["dinner"]["options"][1],
            "snack": meals["snacks"]["options"][1]
        },
        "Wednesday": {
            "breakfast": meals["breakfast"]["options"][2],
            "lunch": meals["lunch"]["options"][2],
            "dinner": meals["dinner"]["options"][2],
            "snack": meals["snacks"]["options"][2]
        },
        "Thursday": {
            "breakfast": meals["breakfast"]["options"][3],
            "lunch": meals["lunch"]["options"][3],
            "dinner": meals["dinner"]["options"][3],
            "snack": meals["snacks"]["options"][3]
        },
        "Friday": {
            "breakfast": meals["breakfast"]["options"][0],
            "lunch": meals["lunch"]["options"][2],
            "dinner": meals["dinner"]["options"][1],
            "snack": meals["snacks"]["options"][0]
        },
        "Saturday": {
            "breakfast": meals["breakfast"]["options"][1],
            "lunch": meals["lunch"]["options"][3],
            "dinner": meals["dinner"]["options"][2],
            "snack": meals["snacks"]["options"][1]
        },
        "Sunday": {
            "breakfast": meals["breakfast"]["options"][2],
            "lunch": meals["lunch"]["options"][0],
            "dinner": meals["dinner"]["options"][3],
            "snack": meals["snacks"]["options"][2]
        }
    }
    
    return schedule


def generate_diet_plan(glucose, insulin, bmi, age, has_diabetes):
    """
    Generate complete diet plan based on user data and prediction
    
    Args:
        glucose: Glucose level (mg/dL)
        insulin: Insulin level (μU/mL)
        bmi: Body Mass Index
        age: Patient age
        has_diabetes: Whether patient has diabetes (1) or not (0)
    
    Returns:
        dict: Complete diet plan with all components
    """
    has_diabetes_bool = bool(has_diabetes)
    
    calories = calculate_daily_calories(age, bmi, glucose, has_diabetes_bool)
    macros = get_macronutrient_breakdown(glucose, insulin, has_diabetes_bool)
    friendly_foods = get_diabetic_friendly_foods()
    foods_avoid = get_foods_to_avoid()
    meal_suggestions = generate_meal_suggestions(calories, has_diabetes_bool)
    weekly_schedule = generate_weekly_schedule(calories, has_diabetes_bool)
    
    # Generate personalized tips based on glucose and insulin levels
    tips = [
        "Eat at regular intervals to maintain stable blood sugar",
        "Stay hydrated - drink 8-10 glasses of water daily",
        "Monitor portion sizes carefully",
        "Choose whole grains over refined carbohydrates",
        "Include fiber-rich foods in every meal",
        "Limit saturated fats and avoid trans fats",
        "Exercise regularly for at least 30 minutes daily"
    ]
    
    # Add personalized tips based on glucose levels
    if glucose > 140:
        tips.insert(0, f"Your glucose level ({glucose:.0f} mg/dL) is elevated. Focus on low glycemic index foods")
    
    if glucose > 180:
        tips.insert(1, "Avoid sugary drinks and desserts completely until glucose levels stabilize")
    
    # Add personalized tips based on insulin levels
    if insulin > 150:
        tips.insert(0, f"Your insulin level ({insulin:.0f} μU/mL) suggests possible insulin resistance. Reduce simple carbs")
    
    if bmi > 30:
        tips.append("Weight management is crucial - combine diet with regular physical activity")
    
    diet_plan = {
        "daily_calories": calories,
        "macronutrients": macros,
        "diabetic_friendly_foods": friendly_foods,
        "foods_to_avoid": foods_avoid,
        "meal_suggestions": meal_suggestions,
        "weekly_schedule": weekly_schedule,
        "tips": tips,
        "health_metrics": {
            "glucose": f"{glucose:.0f} mg/dL",
            "insulin": f"{insulin:.0f} μU/mL",
            "bmi": f"{bmi:.1f}",
            "age": int(age)
        }
    }
    
    return diet_plan
