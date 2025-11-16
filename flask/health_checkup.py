"""
Health Checkup Recommendation Tool
Generates personalized health checkup recommendations based on patient data
"""

def get_blood_test_recommendations(age, bmi, glucose, blood_pressure_systolic, blood_pressure_diastolic, has_diabetes, family_history):
    """
    Generate recommended blood tests based on patient profile
    
    Args:
        age: Patient age
        bmi: Body Mass Index
        glucose: Glucose level
        blood_pressure_systolic: Systolic blood pressure (top number)
        blood_pressure_diastolic: Diastolic blood pressure (bottom number)
        has_diabetes: Whether patient has diabetes
        family_history: Whether patient has family history of diabetes
    
    Returns:
        dict: Recommended tests with priorities
    """
    tests = {
        "essential": [],
        "recommended": [],
        "optional": []
    }
    
    # Essential tests for everyone
    tests["essential"].append({
        "name": "Fasting Blood Glucose (FBG)",
        "reason": "Monitor blood sugar levels",
        "frequency": "Every 6 months" if (has_diabetes or glucose > 100) else "Annually"
    })
    
    tests["essential"].append({
        "name": "HbA1c (Glycated Hemoglobin)",
        "reason": "3-month average blood sugar indicator",
        "frequency": "Every 3 months" if has_diabetes else "Every 6 months" if glucose > 100 else "Annually"
    })
    
    tests["essential"].append({
        "name": "Lipid Panel (Cholesterol)",
        "reason": "Check heart health and cholesterol levels",
        "frequency": "Every 6 months" if (age > 45 or bmi > 30) else "Annually"
    })
    
    # Blood pressure related tests
    if blood_pressure_systolic >= 140 or blood_pressure_diastolic >= 90:
        tests["essential"].append({
            "name": "Blood Pressure Monitoring",
            "reason": "Your BP is elevated - monitor regularly",
            "frequency": "Weekly at home, monthly with doctor"
        })
        
        tests["recommended"].append({
            "name": "Kidney Function Tests (Creatinine, BUN)",
            "reason": "High BP can affect kidney function",
            "frequency": "Every 6 months"
        })
    
    # Diabetes-specific tests
    if has_diabetes or glucose > 125:
        tests["essential"].append({
            "name": "Urine Microalbumin",
            "reason": "Screen for kidney damage from diabetes",
            "frequency": "Annually"
        })
        
        tests["recommended"].append({
            "name": "Comprehensive Metabolic Panel",
            "reason": "Monitor kidney and liver function",
            "frequency": "Every 6 months"
        })
        
        tests["recommended"].append({
            "name": "Eye Examination (Dilated)",
            "reason": "Screen for diabetic retinopathy",
            "frequency": "Annually"
        })
        
        tests["recommended"].append({
            "name": "Foot Examination",
            "reason": "Check for diabetic neuropathy",
            "frequency": "Every 6 months"
        })
    
    # Age-based recommendations
    if age > 40:
        tests["recommended"].append({
            "name": "Thyroid Function Tests (TSH)",
            "reason": "Screen for thyroid disorders (common after 40)",
            "frequency": "Every 2-3 years"
        })
    
    if age > 50:
        tests["recommended"].append({
            "name": "Vitamin D Levels",
            "reason": "Important for bone health",
            "frequency": "Annually"
        })
        
        tests["optional"].append({
            "name": "Bone Density Scan",
            "reason": "Screen for osteoporosis risk",
            "frequency": "Every 2 years"
        })
    
    # BMI-based recommendations
    if bmi > 30:
        tests["recommended"].append({
            "name": "Liver Function Tests",
            "reason": "Higher BMI can affect liver health",
            "frequency": "Annually"
        })
    
    # Family history considerations
    if family_history:
        tests["recommended"].append({
            "name": "Insulin Levels (Fasting)",
            "reason": "Family history increases diabetes risk",
            "frequency": "Annually"
        })
        
        tests["recommended"].append({
            "name": "C-Peptide Test",
            "reason": "Assess insulin production",
            "frequency": "Every 2 years"
        })
    
    # General health tests
    tests["optional"].append({
        "name": "Complete Blood Count (CBC)",
        "reason": "General health screening",
        "frequency": "Annually"
    })
    
    tests["optional"].append({
        "name": "Vitamin B12",
        "reason": "Important for nerve function (especially for diabetics)",
        "frequency": "Annually" if has_diabetes else "Every 2 years"
    })
    
    return tests


def get_checkup_frequency(age, has_diabetes, glucose, blood_pressure_systolic, blood_pressure_diastolic):
    """Determine overall checkup frequency"""
    # Check for hypertension (either systolic ≥140 OR diastolic ≥90)
    has_hypertension = blood_pressure_systolic >= 140 or blood_pressure_diastolic >= 90
    has_elevated_bp = blood_pressure_systolic >= 130 or blood_pressure_diastolic >= 80
    
    if has_diabetes:
        return {
            "doctor_visits": "Every 3 months",
            "reason": "Active diabetes management requires frequent monitoring"
        }
    elif has_hypertension:
        return {
            "doctor_visits": "Every 3-4 months",
            "reason": "Hypertension requires close monitoring and management"
        }
    elif glucose > 125 or has_elevated_bp:
        return {
            "doctor_visits": "Every 4-6 months",
            "reason": "Pre-diabetic or elevated BP requires regular monitoring"
        }
    elif age > 60:
        return {
            "doctor_visits": "Every 6 months",
            "reason": "Regular checkups important for seniors"
        }
    else:
        return {
            "doctor_visits": "Annually",
            "reason": "Maintain regular health screening"
        }


def get_lifestyle_recommendations(age, bmi, glucose, blood_pressure_systolic, has_diabetes):
    """Generate personalized lifestyle tips"""
    tips = []
    
    # Sleep recommendations
    if age < 65:
        tips.append({
            "category": "Sleep",
            "icon": "🛌",
            "recommendation": "Aim for 7-9 hours of quality sleep each night",
            "details": "Good sleep helps regulate blood sugar and blood pressure"
        })
    else:
        tips.append({
            "category": "Sleep",
            "icon": "🛌",
            "recommendation": "Aim for 7-8 hours of sleep each night",
            "details": "Quality sleep is crucial for metabolic health"
        })
    
    # Exercise recommendations
    if bmi > 30:
        tips.append({
            "category": "Exercise",
            "icon": "🏃",
            "recommendation": "Start with 20-30 minutes of walking daily",
            "details": "Gradually increase to 150 minutes of moderate activity per week"
        })
    elif has_diabetes:
        tips.append({
            "category": "Exercise",
            "icon": "🏃",
            "recommendation": "Exercise 30-45 minutes daily, 5 days a week",
            "details": "Mix cardio and strength training to improve insulin sensitivity"
        })
    else:
        tips.append({
            "category": "Exercise",
            "icon": "🏃",
            "recommendation": "Exercise 30 minutes daily, at least 5 days a week",
            "details": "Regular physical activity prevents chronic diseases"
        })
    
    # Hydration
    tips.append({
        "category": "Hydration",
        "icon": "💧",
        "recommendation": "Drink 8-10 glasses of water daily",
        "details": "Proper hydration helps kidney function and blood sugar regulation"
    })
    
    # Stress management
    if blood_pressure_systolic >= 140:
        tips.append({
            "category": "Stress Management",
            "icon": "🧘",
            "recommendation": "Practice stress reduction techniques daily",
            "details": "Try meditation, deep breathing, or yoga to lower blood pressure"
        })
    else:
        tips.append({
            "category": "Stress Management",
            "icon": "🧘",
            "recommendation": "Manage stress through relaxation techniques",
            "details": "Chronic stress can raise blood sugar and blood pressure"
        })
    
    # Blood sugar monitoring
    if has_diabetes or glucose > 125:
        tips.append({
            "category": "Monitoring",
            "icon": "📊",
            "recommendation": "Monitor blood sugar regularly",
            "details": "Check fasting glucose and track patterns with your doctor"
        })
    
    # Weight management
    if bmi > 25:
        tips.append({
            "category": "Weight Management",
            "icon": "⚖️",
            "recommendation": "Work towards a healthy weight gradually",
            "details": "Even 5-10% weight loss can significantly improve health markers"
        })
    
    # Alcohol and smoking
    tips.append({
        "category": "Avoid Harmful Habits",
        "icon": "🚭",
        "recommendation": "Avoid smoking and limit alcohol consumption",
        "details": "Both can worsen diabetes and cardiovascular health"
    })
    
    return tips


def generate_health_checkup_plan(age, bmi, glucose, blood_pressure_systolic, blood_pressure_diastolic, has_diabetes, family_history):
    """
    Generate complete health checkup recommendation plan
    
    Args:
        age: Patient age
        bmi: Body Mass Index
        glucose: Glucose level
        blood_pressure_systolic: Systolic BP
        blood_pressure_diastolic: Diastolic BP
        has_diabetes: Whether patient has diabetes
        family_history: Whether patient has family history of diabetes
    
    Returns:
        dict: Complete health checkup plan
    """
    
    blood_tests = get_blood_test_recommendations(
        age, bmi, glucose, blood_pressure_systolic, 
        blood_pressure_diastolic, has_diabetes, family_history
    )
    
    checkup_frequency = get_checkup_frequency(age, has_diabetes, glucose, blood_pressure_systolic, blood_pressure_diastolic)
    
    lifestyle_tips = get_lifestyle_recommendations(age, bmi, glucose, blood_pressure_systolic, has_diabetes)
    
    # Determine BP category
    if blood_pressure_systolic >= 140 or blood_pressure_diastolic >= 90:
        bp_category = "High (Hypertension)"
        bp_status = "concerning"
    elif blood_pressure_systolic >= 130 or blood_pressure_diastolic >= 80:
        bp_category = "Elevated"
        bp_status = "attention"
    else:
        bp_category = "Normal"
        bp_status = "good"
    
    checkup_plan = {
        "blood_pressure_info": {
            "reading": f"{blood_pressure_systolic}/{blood_pressure_diastolic} mmHg",
            "category": bp_category,
            "status": bp_status
        },
        "blood_tests": blood_tests,
        "checkup_frequency": checkup_frequency,
        "lifestyle_tips": lifestyle_tips,
        "family_history": family_history,
        "next_steps": [
            "Schedule an appointment with your primary care physician",
            "Discuss these test recommendations with your doctor",
            "Get baseline tests done if you haven't had them recently",
            "Create a health tracking log for blood sugar and blood pressure",
            "Follow up on any abnormal results promptly"
        ]
    }
    
    return checkup_plan
