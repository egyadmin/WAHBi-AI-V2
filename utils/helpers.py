import os
import re
import json
import pandas as pd
from typing import Dict, List, Any, Union, Tuple, Optional
from datetime import datetime

def format_currency(amount: float, currency: str = "ريال") -> str:
    """
    تنسيق المبالغ المالية
    
    المعاملات:
    ----------
    amount : float
        المبلغ
    currency : str, optional
        العملة (افتراضي: "ريال")
        
    المخرجات:
    --------
    str
        المبلغ بالتنسيق المناسب
    """
    if not amount and amount != 0:
        return "غير محدد"
    
    # تنسيق الأرقام بالفواصل الآلاف
    formatted = f"{amount:,.2f}".replace(".00", "")
    
    # ترتيب العملة حسب اللغة العربية (يمين)
    return f"{formatted} {currency}"

def format_percentage(value: float) -> str:
    """
    تنسيق النسب المئوية
    
    المعاملات:
    ----------
    value : float
        القيمة
        
    المخرجات:
    --------
    str
        النسبة بالتنسيق المناسب
    """
    if not value and value != 0:
        return "غير محدد"
    
    return f"{value:.2f}%".replace(".00", "")

def format_date(date_obj: Any) -> str:
    """
    تنسيق التواريخ
    
    المعاملات:
    ----------
    date_obj : Any
        كائن التاريخ
        
    المخرجات:
    --------
    str
        التاريخ بالتنسيق المناسب
    """
    if not date_obj:
        return "غير محدد"
    
    # إذا كان التاريخ سلسلة نصية
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, "%Y-%m-%d")
        except ValueError:
            try:
                date_obj = datetime.strptime(date_obj, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return date_obj
    
    # تنسيق التاريخ بالطريقة العربية
    month_names = [
        "يناير", "فبراير", "مارس", "إبريل", "مايو", "يونيو", 
        "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
    ]
    
    return f"{date_obj.day} {month_names[date_obj.month - 1]} {date_obj.year}"

def extract_keywords(text: str, keywords: List[str], context_size: int = 50) -> List[Dict[str, str]]:
    """
    استخراج الكلمات المفتاحية من النص مع سياقها
    
    المعاملات:
    ----------
    text : str
        النص المراد البحث فيه
    keywords : List[str]
        قائمة الكلمات المفتاحية
    context_size : int, optional
        حجم السياق بالأحرف قبل وبعد الكلمة (افتراضي: 50)
        
    المخرجات:
    --------
    List[Dict[str, str]]
        قائمة بالكلمات المفتاحية وسياقها
    """
    results = []
    
    for keyword in keywords:
        # البحث عن الكلمة المفتاحية في النص
        pattern = re.compile(r'\\b' + re.escape(keyword) + r'\\b', re.IGNORECASE | re.MULTILINE)
        matches = pattern.finditer(text)
        
        for match in matches:
            start_idx = max(0, match.start() - context_size)
            end_idx = min(len(text), match.end() + context_size)
            
            # استخراج السياق
            context = text[start_idx:end_idx]
            
            # إضافة النتيجة
            results.append({
                "keyword": keyword,
                "context": context,
                "position": match.start()
            })
    
    # ترتيب النتائج حسب الموقع في النص
    results = sorted(results, key=lambda x: x["position"])
    
    return results

def calculate_progress(current: float, total: float) -> Dict[str, Any]:
    """
    حساب نسبة الإنجاز
    
    المعاملات:
    ----------
    current : float
        القيمة الحالية
    total : float
        القيمة الإجمالية
        
    المخرجات:
    --------
    Dict[str, Any]
        معلومات التقدم
    """
    if total == 0:
        return {
            "percentage": 0,
            "status": "لم يبدأ",
            "color": "gray"
        }
    
    percentage = min(100, (current / total) * 100)
    
    if percentage == 0:
        status = "لم يبدأ"
        color = "gray"
    elif percentage < 25:
        status = "بداية"
        color = "red"
    elif percentage < 50:
        status = "قيد التنفيذ"
        color = "orange"
    elif percentage < 75:
        status = "متقدم"
        color = "blue"
    elif percentage < 100:
        status = "شبه مكتمل"
        color = "teal"
    else:
        status = "مكتمل"
        color = "green"
    
    return {
        "percentage": round(percentage, 1),
        "status": status,
        "color": color
    }

def create_directory_structure(base_dir: str, structure: Dict[str, Any]) -> None:
    """
    إنشاء هيكل المجلدات
    
    المعاملات:
    ----------
    base_dir : str
        المجلد الأساسي
    structure : Dict[str, Any]
        هيكل المجلدات
    """
    os.makedirs(base_dir, exist_ok=True)
    
    for key, value in structure.items():
        path = os.path.join(base_dir, key)
        
        if isinstance(value, dict):
            # إذا كانت القيمة قاموساً، استمر في إنشاء الهيكل الفرعي
            create_directory_structure(path, value)
        else:
            # إنشاء المجلد
            os.makedirs(path, exist_ok=True)
            
            # إذا كانت القيمة قائمة، إنشاء ملفات فارغة
            if isinstance(value, list):
                for file_name in value:
                    file_path = os.path.join(path, file_name)
                    if not os.path.exists(file_path):
                        with open(file_path, 'w', encoding='utf-8') as f:
                            # يمكن كتابة محتوى افتراضي هنا
                            pass

def export_to_excel(data: List[Dict[str, Any]], file_path: str, sheet_name: str = "Sheet1") -> bool:
    """
    تصدير البيانات إلى ملف Excel
    
    المعاملات:
    ----------
    data : List[Dict[str, Any]]
        البيانات المراد تصديرها
    file_path : str
        مسار الملف
    sheet_name : str, optional
        اسم ورقة العمل (افتراضي: "Sheet1")
        
    المخرجات:
    --------
    bool
        نجاح أو فشل العملية
    """
    try:
        # تحويل البيانات إلى DataFrame
        df = pd.DataFrame(data)
        
        # تصدير إلى Excel
        df.to_excel(file_path, sheet_name=sheet_name, index=False)
        
        return True
    except Exception as e:
        print(f"Error exporting to Excel: {str(e)}")
        return False

def export_to_json(data: Any, file_path: str) -> bool:
    """
    تصدير البيانات إلى ملف JSON
    
    المعاملات:
    ----------
    data : Any
        البيانات المراد تصديرها
    file_path : str
        مسار الملف
        
    المخرجات:
    --------
    bool
        نجاح أو فشل العملية
    """
    try:
        # إنشاء المجلد إذا لم يكن موجوداً
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # تصدير إلى JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        return True
    except Exception as e:
        print(f"Error exporting to JSON: {str(e)}")
        return False

def validate_input(input_data: Dict[str, Any], validation_rules: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    التحقق من صحة البيانات المدخلة
    
    المعاملات:
    ----------
    input_data : Dict[str, Any]
        البيانات المدخلة
    validation_rules : Dict[str, Dict[str, Any]]
        قواعد التحقق
        
    المخرجات:
    --------
    Dict[str, List[str]]
        قائمة بالأخطاء لكل حقل
    """
    errors = {}
    
    for field, rules in validation_rules.items():
        field_errors = []
        value = input_data.get(field)
        
        # التحقق من الحقول المطلوبة
        if rules.get("required", False) and (value is None or (isinstance(value, str) and value.strip() == "")):
            field_errors.append("هذا الحقل مطلوب")
        
        # التحقق من النوع
        if value is not None and "type" in rules:
            expected_type = rules["type"]
            if expected_type == "number" and not (isinstance(value, (int, float)) or (isinstance(value, str) and value.strip().replace(".", "", 1).isdigit())):
                field_errors.append("يجب أن يكون هذا الحقل رقماً")
            elif expected_type == "email" and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', str(value)):
                field_errors.append("يرجى إدخال بريد إلكتروني صحيح")
            elif expected_type == "date" and not re.match(r'^\d{4}-\d{2}-\d{2}$', str(value)):
                field_errors.append("يرجى إدخال تاريخ صحيح (YYYY-MM-DD)")
        
        # التحقق من الحد الأدنى والأقصى
        if value is not None and isinstance(value, (int, float)):
            if "min" in rules and value < rules["min"]:
                field_errors.append(f"يجب أن يكون هذا الحقل أكبر من أو يساوي {rules['min']}")
            if "max" in rules and value > rules["max"]:
                field_errors.append(f"يجب أن يكون هذا الحقل أصغر من أو يساوي {rules['max']}")
        
        # التحقق من طول النص
        if value is not None and isinstance(value, str):
            if "min_length" in rules and len(value) < rules["min_length"]:
                field_errors.append(f"يجب أن يحتوي هذا الحقل على {rules['min_length']} أحرف على الأقل")
            if "max_length" in rules and len(value) > rules["max_length"]:
                field_errors.append(f"يجب أن يحتوي هذا الحقل على {rules['max_length']} أحرف كحد أقصى")
        
        # إضافة الأخطاء إذا وجدت
        if field_errors:
            errors[field] = field_errors
    
    return errors