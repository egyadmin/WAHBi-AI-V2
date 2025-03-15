import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging():
    """
    إعداد نظام التسجيل للتطبيق
    """
    # إنشاء مجلد السجلات إذا لم يكن موجوداً
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "app.log"
    
    # إعداد التسجيل الرئيسي
    logger = logging.getLogger("TenderAnalysisSystem")
    logger.setLevel(logging.INFO)
    
    # تنسيق السجلات
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # إضافة معالج للملف مع تدوير السجلات
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 ميجابايت
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # إضافة معالج للإخراج القياسي
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # إضافة المعالجات إلى المسجل
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def ensure_directories():
    """
    إنشاء المجلدات الضرورية للتطبيق إذا لم تكن موجودة
    """
    directories = [
        "data",
        "data/uploads",
        "data/processed",
        "reports",
        "models",
        "models/cache",
        "models/embeddings",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def save_uploaded_file(uploaded_file, directory="data/uploads"):
    """
    حفظ الملف المرفوع في المجلد المحدد
    
    المعلمات:
        uploaded_file: الملف المرفوع من Streamlit
        directory: المجلد الذي سيتم حفظ الملف فيه
    
    الإرجاع:
        مسار الملف المحفوظ
    """
    # التأكد من وجود المجلد
    os.makedirs(directory, exist_ok=True)
    
    # إنشاء مسار الملف
    file_path = os.path.join(directory, uploaded_file.name)
    
    # حفظ الملف
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def get_file_extension(file_name):
    """
    الحصول على امتداد الملف
    
    المعلمات:
        file_name: اسم الملف
    
    الإرجاع:
        امتداد الملف
    """
    return os.path.splitext(file_name)[1].lower()