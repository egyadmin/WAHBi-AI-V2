"""
محمّل النماذج
يقوم بتحميل وإدارة نماذج الذكاء الاصطناعي المستخدمة في النظام
"""

import os
import logging
import torch
import gc
from typing import Dict, Any, Optional, Union, List
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelLoader:
    """
    محمّل النماذج
    """
    
    def __init__(self, config=None, use_gpu=True):
        """
        تهيئة محمّل النماذج
        
        المعاملات:
        ----------
        config : Dict, optional
            إعدادات محمّل النماذج
        use_gpu : bool, optional
            استخدام GPU إذا كان متاحًا
        """
        self.config = config or {}
        self.use_gpu = use_gpu and torch.cuda.is_available()
        
        # التحقق من توفر GPU
        if self.use_gpu:
            self.device = torch.device("cuda")
            logger.info(f"تم اكتشاف GPU: {torch.cuda.get_device_name(0)}")
            logger.info(f"ذاكرة GPU المتاحة: {self._get_available_gpu_memory()} ميجابايت")
        else:
            self.device = torch.device("cpu")
            logger.info("استخدام المعالج المركزي CPU")
        
        # تهيئة قواميس لتخزين النماذج المحملة
        self.models = {}
        self.tokenizers = {}
        
        # تحميل النماذج المطلوبة بشكل افتراضي
        self._load_default_models()
        
        logger.info("تم تهيئة محمّل النماذج")
    
    def get_ner_model(self):
        """
        الحصول على نموذج التعرف على الكيانات المسماة
        
        المخرجات:
        --------
        أي
            نموذج التعرف على الكيانات المسماة
        """
        if "ner" in self.models:
            return self.models["ner"]
        
        # تحميل النموذج إذا لم يكن محملاً
        ner_model = self._load_ner_model()
        
        return ner_model
    
    def get_similarity_model(self):
        """
        الحصول على نموذج التشابه النصي
        
        المخرجات:
        --------
        أي
            نموذج التشابه النصي
        """
        if "similarity" in self.models:
            return self.models["similarity"]
        
        # تحميل النموذج إذا لم يكن محملاً
        similarity_model = self._load_similarity_model()
        
        return similarity_model
    
    def get_classification_model(self):
        """
        الحصول على نموذج التصنيف
        
        المخرجات:
        --------
        أي
            نموذج التصنيف
        """
        if "classification" in self.models:
            return self.models["classification"]
        
        # تحميل النموذج إذا لم يكن محملاً
        classification_model = self._load_classification_model()
        
        return classification_model
    
    def get_tokenizer(self, model_name):
        """
        الحصول على محلل الترميز للنموذج
        
        المعاملات:
        ----------
        model_name : str
            اسم النموذج
            
        المخرجات:
        --------
        أي
            محلل الترميز
        """
        if model_name in self.tokenizers:
            return self.tokenizers[model_name]
        
        # تحميل محلل الترميز إذا لم يكن محملاً
        if model_name == "ner":
            tokenizer = self._load_tokenizer("aubmindlab/bert-base-arabertv02-ner")
        elif model_name == "similarity":
            tokenizer = self._load_tokenizer("UBC-NLP/ARBERT")
        elif model_name == "classification":
            tokenizer = self._load_tokenizer("CAMeL-Lab/bert-base-arabic-camelbert-mix")
        else:
            raise ValueError(f"محلل الترميز غير معروف: {model_name}")
        
        self.tokenizers[model_name] = tokenizer
        return tokenizer
    
    def release_model(self, model_name):
        """
        تحرير النموذج من الذاكرة
        
        المعاملات:
        ----------
        model_name : str
            اسم النموذج
        """
        if model_name in self.models:
            del self.models[model_name]
            
            if self.use_gpu:
                torch.cuda.empty_cache()
                gc.collect()
            
            logger.info(f"تم تحرير النموذج: {model_name}")
    
    def release_all_models(self):
        """
        تحرير جميع النماذج من الذاكرة
        """
        self.models = {}
        self.tokenizers = {}
        
        if self.use_gpu:
            torch.cuda.empty_cache()
            gc.collect()
        
        logger.info("تم تحرير جميع النماذج")
    
    def get_available_memory(self):
        """
        الحصول على كمية الذاكرة المتاحة
        
        المخرجات:
        --------
        int
            كمية الذاكرة المتاحة بالميجابايت
        """
        if self.use_gpu:
            return self._get_available_gpu_memory()
        else:
            # ليس هناك طريقة موحدة للحصول على ذاكرة CPU
            return 0
    
    def _load_default_models(self):
        """
        تحميل النماذج الافتراضية
        """
        default_models = self.config.get("default_models", [])
        
        for model_name in default_models:
            try:
                if model_name == "ner":
                    self._load_ner_model()
                elif model_name == "similarity":
                    self._load_similarity_model()
                elif model_name == "classification":
                    self._load_classification_model()
                else:
                    logger.warning(f"نموذج غير معروف: {model_name}")
            except Exception as e:
                logger.error(f"فشل في تحميل النموذج {model_name}: {str(e)}")
    
    def _load_ner_model(self):
        """
        تحميل نموذج التعرف على الكيانات المسماة
        
        المخرجات:
        --------
        أي
            نموذج التعرف على الكيانات المسماة
        """
        try:
            from transformers import pipeline
            
            logger.info("جاري تحميل نموذج التعرف على الكيانات المسماة...")
            
            model_name = self.config.get("ner_model", "aubmindlab/bert-base-arabertv02-ner")
            
            # تحميل النموذج
            ner_model = pipeline(
                "token-classification", 
                model=model_name,
                aggregation_strategy="simple",
                device=0 if self.use_gpu else -1
            )
            
            self.models["ner"] = ner_model
            logger.info(f"تم تحميل نموذج التعرف على الكيانات المسماة: {model_name}")
            
            return ner_model
            
        except Exception as e:
            logger.error(f"فشل في تحميل نموذج التعرف على الكيانات المسماة: {str(e)}")
            raise
    
    def _load_similarity_model(self):
        """
        تحميل نموذج التشابه النصي
        
        المخرجات:
        --------
        أي
            نموذج التشابه النصي
        """
        try:
            from transformers import AutoModel
            
            logger.info("جاري تحميل نموذج التشابه النصي...")
            
            model_name = self.config.get("similarity_model", "UBC-NLP/ARBERT")
            
            # تحميل النموذج
            similarity_model = AutoModel.from_pretrained(model_name)
            
            if self.use_gpu:
                similarity_model = similarity_model.to(self.device)
            
            self.models["similarity"] = similarity_model
            logger.info(f"تم تحميل نموذج التشابه النصي: {model_name}")
            
            return similarity_model
            
        except Exception as e:
            logger.error(f"فشل في تحميل نموذج التشابه النصي: {str(e)}")
            raise
    
    def _load_classification_model(self):
        """
        تحميل نموذج التصنيف
        
        المخرجات:
        --------
        أي
            نموذج التصنيف
        """
        try:
            from transformers import pipeline
            
            logger.info("جاري تحميل نموذج التصنيف...")
            
            model_name = self.config.get("classification_model", "CAMeL-Lab/bert-base-arabic-camelbert-mix")
            
            # تحميل النموذج
            classification_model = pipeline(
                "text-classification",
                model=model_name,
                device=0 if self.use_gpu else -1
            )
            
            self.models["classification"] = classification_model
            logger.info(f"تم تحميل نموذج التصنيف: {model_name}")
            
            return classification_model
            
        except Exception as e:
            logger.error(f"فشل في تحميل نموذج التصنيف: {str(e)}")
            raise
    
    def _load_tokenizer(self, model_name):
        """
        تحميل محلل الترميز
        
        المعاملات:
        ----------
        model_name : str
            اسم النموذج
            
        المخرجات:
        --------
        أي
            محلل الترميز
        """
        try:
            from transformers import AutoTokenizer
            
            logger.info(f"جاري تحميل محلل الترميز: {model_name}...")
            
            # تحميل محلل الترميز
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            logger.info(f"تم تحميل محلل الترميز: {model_name}")
            
            return tokenizer
            
        except Exception as e:
            logger.error(f"فشل في تحميل محلل الترميز {model_name}: {str(e)}")
            raise
    
    def _get_available_gpu_memory(self):
        """
        الحصول على كمية ذاكرة GPU المتاحة
        
        المخرجات:
        --------
        int
            كمية ذاكرة GPU المتاحة بالميجابايت
        """
        if not self.use_gpu:
            return 0
        
        try:
            torch.cuda.empty_cache()
            # الحصول على إجمالي ذاكرة GPU
            total_memory = torch.cuda.get_device_properties(0).total_memory
            # الحصول على ذاكرة GPU المستخدمة
            allocated_memory = torch.cuda.memory_allocated(0)
            # الحصول على ذاكرة GPU المحجوزة
            reserved_memory = torch.cuda.memory_reserved(0)
            
            # حساب الذاكرة المتاحة
            available_memory = total_memory - allocated_memory - reserved_memory
            
            # تحويل إلى ميجابايت
            return available_memory / (1024 * 1024)
            
        except Exception as e:
            logger.error(f"فشل في الحصول على ذاكرة GPU المتاحة: {str(e)}")
            return 0