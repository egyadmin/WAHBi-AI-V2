import os
from typing import Dict, Any
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# إعدادات عامة
APP_NAME = "نظام تحليل المناقصات"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# مسارات الملفات
DATA_DIR = os.getenv("DATA_DIR", "data")
TEMPLATES_DIR = os.path.join(DATA_DIR, "templates")
VECTOR_DB_DIR = os.path.join(DATA_DIR, "vector_db")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
LOGS_DIR = os.getenv("LOGS_DIR", "logs")

# التأكد من وجود المجلدات
for directory in [DATA_DIR, TEMPLATES_DIR, VECTOR_DB_DIR, OUTPUT_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

# إعدادات API
API_KEYS = {
    "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
    "MUNAFASAT_API_KEY": os.getenv("MUNAFASAT_API_KEY"),
    "ETIMAD_API_KEY": os.getenv("ETIMAD_API_KEY"),
    "BALADY_API_KEY": os.getenv("BALADY_API_KEY")
}

# إعدادات نماذج الذكاء الاصطناعي
AI_MODELS = {
    "default_llm": os.getenv("DEFAULT_LLM", "claude-3-haiku-20240307"),
    "use_rag": os.getenv("USE_RAG", "True").lower() in ("true", "1", "t"),
    "embedding_model": os.getenv("EMBEDDING_MODEL", "huggingface/arabic-embedding-base")
}

# إعدادات المحتوى المحلي
LOCAL_CONTENT = {
    "min_percentage": {
        "الإنشاءات": 30,
        "تقنية المعلومات": 25,
        "عام": 20
    },
    "target_percentage": {
        "الإنشاءات": 60,
        "تقنية المعلومات": 50,
        "عام": 40
    }
}

# إعدادات واجهة المستخدم
UI_SETTINGS = {
    "theme": os.getenv("UI_THEME", "light"),
    "language": os.getenv("UI_LANGUAGE", "ar"),
    "page_size": int(os.getenv("UI_PAGE_SIZE", "10")),
    "charts_theme": os.getenv("UI_CHARTS_THEME", "blue")
}

# إعدادات قاعدة البيانات
DB_SETTINGS = {
    "vector_db": {
        "path": VECTOR_DB_DIR,
        "dimension": 384,
        "similarity_threshold": 0.75
    }
}

# وظيفة للحصول على إعدادات محددة
def get_config(section: str = None) -> Dict[str, Any]:
    """
    الحصول على إعدادات محددة أو جميع الإعدادات
    
    المعاملات:
    ----------
    section : str, optional
        اسم قسم الإعدادات المطلوب (افتراضي: None = جميع الإعدادات)
        
    المخرجات:
    --------
    Dict[str, Any]
        الإعدادات المطلوبة
    """
    config = {
        "app": {
            "name": APP_NAME,
            "version": APP_VERSION,
            "debug": DEBUG
        },
        "paths": {
            "data_dir": DATA_DIR,
            "templates_dir": TEMPLATES_DIR,
            "vector_db_dir": VECTOR_DB_DIR,
            "output_dir": OUTPUT_DIR,
            "logs_dir": LOGS_DIR
        },
        "api_keys": API_KEYS,
        "ai_models": AI_MODELS,
        "local_content": LOCAL_CONTENT,
        "ui": UI_SETTINGS,
        "db": DB_SETTINGS
    }
    
    if section:
        return config.get(section, {})
    
    return config