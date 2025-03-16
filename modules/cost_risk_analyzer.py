"""
فئة للتعامل مع نماذج اللغة الكبيرة (LLM) لتحليل المناقصات
"""

import os
import json
import re
import requests
import numpy as np
import logging
from typing import Dict, List, Any, Union, Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class LLMProcessor:
    """
    فئة للتعامل مع نماذج اللغة الكبيرة (LLM) لتحليل المناقصات
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        تهيئة معالج نماذج اللغة الكبيرة
        
        المعاملات:
        ----------
        config : Dict[str, Any], optional
            إعدادات معالج نماذج اللغة الكبيرة
        """
        self.config = config or {}
        self.model_name = self.config.get('model_name', "claude-3-haiku-20240307")
        self.use_rag = self.config.get('use_rag', True)
        self.temperature = self.config.get('temperature', 0.7)
        self.max_tokens = self.config.get('max_tokens', 4096)
        
        # الحصول على مفتاح واجهة برمجة التطبيقات من متغيرات البيئة أو الإعدادات
        self.api_key = self.config.get('api_key') or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            logger.warning("لم يتم تحديد مفتاح واجهة برمجة التطبيقات لـ Anthropic. لن تعمل وظائف LLM.")
        
        # تهيئة قاعدة بيانات المتجهات إذا كان استخدام RAG مفعلاً
        if self.use_rag:
            try:
                from utils.vector_db import VectorDB
                self.vector_db = VectorDB(self.config.get('vector_db_config', {}))
                logger.info("تم تهيئة قاعدة بيانات المتجهات بنجاح.")
            except ImportError as e:
                logger.error(f"فشل في تهيئة قاعدة بيانات المتجهات: {str(e)}")
                self.use_rag = False
        
        logger.info(f"تم تهيئة معالج نماذج اللغة الكبيرة: {self.model_name}, RAG: {self.use_rag}")
    
    def analyze_requirements(self, requirements: List[Dict[str, Any]], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        تحليل المتطلبات باستخدام نموذج اللغة الكبيرة
        
        المعاملات:
        ----------
        requirements : List[Dict[str, Any]]
            قائمة المتطلبات المستخرجة من المستندات
        context : Dict[str, Any], optional
            معلومات السياق الإضافية
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المتطلبات
        """
        context = context or {}
        
        try:
            # إعداد الاستعلام بناءً على المتطلبات والسياق
            prompt = self._prepare_requirements_prompt(requirements, context)
            
            # استرجاع معلومات إضافية من قاعدة البيانات إذا كان استخدام RAG مفعلاً
            if self.use_rag:
                retrieval_results = self.vector_db.search(
                    query=self._create_search_query(requirements),
                    collection="requirements",
                    limit=5
                )
                prompt += "\n\nمعلومات إضافية مسترجعة:\n" + self._format_retrieval_results(retrieval_results)
            
            # استدعاء النموذج
            response = self._call_llm(prompt)
            
            # معالجة الاستجابة
            analysis = self._parse_requirements_response(response)
            
            logger.info("تم تحليل المتطلبات بنجاح.")
            return analysis
            
        except Exception as e:
            logger.error(f"فشل في تحليل المتطلبات: {str(e)}")
            return {
                "summary": "حدث خطأ أثناء تحليل المتطلبات",
                "error": str(e),
                "technical": [],
                "financial": [],
                "legal": [],
                "local_content": [],
                "total_count": len(requirements),
                "mandatory_count": 0,
                "avg_difficulty": 0,
                "local_content_percentage": 0
            }
    
    def analyze_local_content(self, local_content_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        تحليل بيانات المحتوى المحلي باستخدام نموذج اللغة الكبيرة
        
        المعاملات:
        ----------
        local_content_data : Dict[str, Any]
            بيانات المحتوى المحلي المستخرجة
        context : Dict[str, Any], optional
            معلومات السياق الإضافية
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المحتوى المحلي
        """
        context = context or {}
        
        try:
            # إعداد الاستعلام بناءً على بيانات المحتوى المحلي والسياق
            prompt = self._prepare_local_content_prompt(local_content_data, context)
            
            # استرجاع معلومات إضافية من قاعدة البيانات إذا كان استخدام RAG مفعلاً
            if self.use_rag:
                retrieval_results = self.vector_db.search(
                    query=self._create_search_query(local_content_data),
                    collection="local_content",
                    limit=5
                )
                prompt += "\n\nمعلومات إضافية مسترجعة:\n" + self._format_retrieval_results(retrieval_results)
            
            # استدعاء النموذج
            response = self._call_llm(prompt)
            
            # معالجة الاستجابة
            analysis = self._parse_local_content_response(response)
            
            logger.info("تم تحليل بيانات المحتوى المحلي بنجاح.")
            return analysis
            
        except Exception as e:
            logger.error(f"فشل في تحليل بيانات المحتوى المحلي: {str(e)}")
            return {
                "estimated_local_content": 0,
                "required_local_content": 0,
                "required_materials": [],
                "improvement_strategies": []
            }
    
    def analyze_supply_chain(self, supply_chain_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        تحليل بيانات سلسلة الإمداد باستخدام نموذج اللغة الكبيرة
        
        المعاملات:
        ----------
        supply_chain_data : Dict[str, Any]
            بيانات سلسلة الإمداد المستخرجة
        context : Dict[str, Any], optional
            معلومات السياق الإضافية
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل سلسلة الإمداد
        """
        context = context or {}
        
        try:
            # إعداد الاستعلام بناءً على بيانات سلسلة الإمداد والسياق
            prompt = self._prepare_supply_chain_prompt(supply_chain_data, context)
            
            # استرجاع معلومات إضافية من قاعدة البيانات إذا كان استخدام RAG مفعلاً
            if self.use_rag:
                retrieval_results = self.vector_db.search(
                    query=self._create_search_query(supply_chain_data),
                    collection="supply_chain",
                    limit=5
                )
                prompt += "\n\nمعلومات إضافية مسترجعة:\n" + self._format_retrieval_results(retrieval_results)
            
            # استدعاء النموذج
            response = self._call_llm(prompt)
            
            # معالجة الاستجابة
            analysis = self._parse_supply_chain_response(response)
            
            logger.info("تم تحليل بيانات سلسلة الإمداد بنجاح.")
            return analysis
            
        except Exception as e:
            logger.error(f"فشل في تحليل بيانات سلسلة الإمداد: {str(e)}")
            return {
                "supply_chain_risks": [],
                "optimizations": [],
                "local_suppliers_availability": 0
            }
    
    def analyze_risks(self, extracted_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        تحليل المخاطر من نص المناقصة
        
        المعاملات:
        ----------
        extracted_text : str
            النص المستخرج من المناقصة
        context : Dict[str, Any], optional
            معلومات السياق الإضافية
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المخاطر
        """
        context = context or {}
        
        try:
            # إعداد الاستعلام
            prompt = self._prepare_risk_analysis_prompt(extracted_text, context)
            
            # استرجاع معلومات إضافية من قاعدة البيانات إذا كان استخدام RAG مفعلاً
            if self.use_rag:
                # استخراج كلمات مفتاحية من النص
                keywords = self._extract_keywords(extracted_text)
                query = " ".join(keywords[:10])  # استخدام أهم 10 كلمات مفتاحية
                
                retrieval_results = self.vector_db.search(
                    query=query,
                    collection="risks",
                    limit=5
                )
                prompt += "\n\nمعلومات إضافية مسترجعة:\n" + self._format_retrieval_results(retrieval_results)
            
            # استدعاء النموذج
            response = self._call_llm(prompt)
            
            # معالجة الاستجابة
            analysis = self._parse_risk_response(response)
            
            logger.info("تم تحليل المخاطر بنجاح.")
            return analysis
            
        except Exception as e:
            logger.error(f"فشل في تحليل المخاطر: {str(e)}")
            return {
                "all_risks": [],
                "technical_risks": [],
                "financial_risks": [],
                "supply_chain_risks": [],
                "legal_risks": [],
                "mitigation_plan": [],
                "avg_severity": 0
            }
    
    def generate_summary(self, extracted_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        إعداد ملخص شامل للمناقصة ونتائج التحليل
        
        المعاملات:
        ----------
        extracted_data : Dict[str, Any]
            البيانات المستخرجة من المستندات
        analysis_results : Dict[str, Any]
            نتائج التحليلات المختلفة
            
        المخرجات:
        --------
        Dict[str, Any]
            الملخص والتوصيات
        """
        try:
            # إعداد الاستعلام بناءً على البيانات المستخرجة ونتائج التحليل
            prompt = self._prepare_summary_prompt(extracted_data, analysis_results)
            
            # استرجاع معلومات إضافية من قاعدة البيانات إذا كان استخدام RAG مفعلاً
            if self.use_rag:
                # إنشاء استعلام متجه من البيانات المستخرجة
                query = self._create_search_query(extracted_data)
                
                retrieval_results = self.vector_db.search(
                    query=query,
                    collection="summaries",
                    limit=3
                )
                prompt += "\n\nأمثلة مشابهة من المناقصات السابقة:\n" + self._format_retrieval_results(retrieval_results)
            
            # استدعاء النموذج
            response = self._call_llm(prompt)
            
            # معالجة الاستجابة
            summary = self._parse_summary_response(response)
            
            logger.info("تم إعداد الملخص بنجاح.")
            return summary
            
        except Exception as e:
            logger.error(f"فشل في إعداد الملخص: {str(e)}")
            return {
                "executive_summary": "حدث خطأ أثناء إعداد الملخص",
                "recommendations": [],
                "bid_strategy": {},
                "error": str(e)
            }
    
    def _call_llm(self, prompt: str) -> str:
        """
        استدعاء نموذج اللغة الكبيرة
        
        المعاملات:
        ----------
        prompt : str
            الاستعلام المُرسل للنموذج
            
        المخرجات:
        --------
        str
            استجابة النموذج
        """
        if not self.api_key:
            logger.warning("لم يتم تحديد مفتاح واجهة برمجة التطبيقات.")
            return "لم يتم تحديد مفتاح واجهة برمجة التطبيقات. يرجى تكوين مفتاح API في الإعدادات."
        
        try:
            headers = {
                "x-api-key": self.api_key,
                "content-type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return response.json()["content"][0]["text"]
            else:
                logger.error(f"فشل في استدعاء النموذج: {response.status_code} - {response.text}")
                return f"فشل في استدعاء النموذج: {response.status_code}"
                
        except Exception as e:
            logger.error(f"خطأ في استدعاء النموذج: {str(e)}")
            return f"خطأ في استدعاء النموذج: {str(e)}"
    
    def _prepare_requirements_prompt(self, requirements: List[Dict[str, Any]], context: Dict[str, Any]) -> str:
        """
        إعداد استعلام لتحليل المتطلبات
        """
        prompt = """
        أنت خبير في تحليل المناقصات والعقود. يرجى تحليل المتطلبات التالية وتقديم نظرة ثاقبة حول جودتها واكتمالها ووضوحها وأي فجوات أو مخاطر محتملة.
        
        المتطلبات:
        """
        
        for i, req in enumerate(requirements):
            prompt += f"\n{i+1}. {req.get('title', 'متطلب')}: {req.get('description', '')}"
            prompt += f"\n   الفئة: {req.get('category', 'عامة')}, الأهمية: {req.get('importance', 'عادية')}"
        
        prompt += """
        
        يرجى تقديم التحليل التالي:
        1. ملخص شامل للمتطلبات وجودتها العامة
        2. تصنيف المتطلبات إلى الفئات التالية:
           - متطلبات فنية
           - متطلبات مالية
           - متطلبات قانونية
           - متطلبات المحتوى المحلي
        3. تحديد عدد المتطلبات الإلزامية
        4. تقييم متوسط صعوبة التنفيذ (على مقياس من 1 إلى 5)
        5. تقدير نسبة متطلبات المحتوى المحلي من إجمالي المتطلبات
        6. تحديد أي فجوات أو تناقضات في المتطلبات
        7. اقتراح تحسينات للمتطلبات غير الواضحة
        
        قدم الإجابة بتنسيق JSON التالي:
        {
            "summary": "ملخص شامل للمتطلبات",
            "technical": [{"title": "عنوان المتطلب", "description": "وصف المتطلب", "analysis": "تحليل المتطلب", "importance": "الأهمية", "difficulty": 3, "gaps": "الفجوات", "improvements": "التحسينات المقترحة"}],
            "financial": [...],
            "legal": [...],
            "local_content": [...],
            "total_count": 10,
            "mandatory_count": 5,
            "avg_difficulty": 3.5,
            "local_content_percentage": 25
        }
        """
        
        if context:
            prompt += "\n\nمعلومات سياقية إضافية:\n"
            for key, value in context.items():
                prompt += f"{key}: {value}\n"
        
        return prompt
    
    def _prepare_local_content_prompt(self, local_content_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        إعداد استعلام لتحليل المحتوى المحلي
        """
        prompt = """
        أنت خبير في تحليل المحتوى المحلي وسلاسل الإمداد في المملكة العربية السعودية. يرجى تحليل البيانات التالية وتقديم توصيات لتحسين نسبة المحتوى المحلي.
        
        بيانات المحتوى المحلي:
        """
        
        prompt += f"\nنسبة المحتوى المحلي المطلوبة: {local_content_data.get('required_percentage', 'غير محدد')}"
        prompt += f"\nالفئة: {local_content_data.get('category', 'غير محدد')}"
        
        if 'materials' in local_content_data:
            prompt += "\n\nالمواد والمنتجات المطلوبة:"
            for material in local_content_data['materials']:
                prompt += f"\n- {material.get('name', '')} - الكمية: {material.get('quantity', '')}, وحدة القياس: {material.get('unit', '')}"
        
        if 'services' in local_content_data:
            prompt += "\n\nالخدمات المطلوبة:"
            for service in local_content_data['services']:
                prompt += f"\n- {service.get('name', '')} - {service.get('description', '')}"
        
        prompt += """
        
        يرجى تقديم التحليل التالي:
        1. تقدير نسبة المحتوى المحلي المتوقعة بناءً على البيانات المقدمة
        2. تحليل مدى توافق النسبة المتوقعة مع النسبة المطلوبة
        3. تحديد المواد والمنتجات التي يمكن توريدها محلياً
        4. اقتراح استراتيجيات لزيادة نسبة المحتوى المحلي
        5. تحديد الموردين المحليين المحتملين (إن وجدت معلومات)
        
        قدم الإجابة بتنسيق JSON التالي:
        {
            "estimated_local_content": 35.5,
            "required_local_content": 40,
            "required_materials": [
                {"name": "اسم المادة", "quantity": "الكمية", "unit": "وحدة القياس", "local_availability": "متوفر محلياً؟", "potential_suppliers": ["مورد 1", "مورد 2"]}
            ],
            "improvement_strategies": ["استراتيجية 1", "استراتيجية 2"]
        }
        """
        
        if context:
            prompt += "\n\nمعلومات سياقية إضافية:\n"
            for key, value in context.items():
                prompt += f"{key}: {value}\n"
        
        return prompt
    
    def _prepare_supply_chain_prompt(self, supply_chain_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        إعداد استعلام لتحليل سلسلة الإمداد
        """
        prompt = """
        أنت خبير في سلاسل الإمداد والمشتريات. يرجى تحليل بيانات سلسلة الإمداد التالية وتقديم توصيات لتحسين الكفاءة وتقليل المخاطر.
        
        بيانات سلسلة الإمداد:
        """
        
        if 'materials' in supply_chain_data:
            prompt += "\n\nالمواد والمنتجات:"
            for material in supply_chain_data['materials']:
                prompt += f"\n- {material.get('name', '')} - المصدر: {material.get('source', '')}, وقت التوريد: {material.get('lead_time', '')}"
        
        if 'suppliers' in supply_chain_data:
            prompt += "\n\nالموردين:"
            for supplier in supply_chain_data['suppliers']:
                prompt += f"\n- {supplier.get('name', '')} - الموقع: {supplier.get('location', '')}, التصنيف: {supplier.get('rating', '')}"
        
        if 'logistics' in supply_chain_data:
            prompt += "\n\nالخدمات اللوجستية:"
            for logistic in supply_chain_data['logistics']:
                prompt += f"\n- {logistic.get('type', '')} - المدة: {logistic.get('duration', '')}, التكلفة: {logistic.get('cost', '')}"
        
        prompt += """
        
        يرجى تقديم التحليل التالي:
        1. تحليل المخاطر المحتملة في سلسلة الإمداد
        2. اقتراح تحسينات لتقليل المخاطر وزيادة الكفاءة
        3. تقييم مدى توفر الموردين المحليين للمواد المطلوبة
        4. اقتراح استراتيجية مشتريات فعالة
        
        قدم الإجابة بتنسيق JSON التالي:
        {
            "supply_chain_risks": [
                {"risk": "وصف المخاطرة", "severity": 4, "probability": 3, "impact": "تأثير المخاطرة", "mitigation": "إجراءات التخفيف"}
            ],
            "optimizations": ["تحسين 1", "تحسين 2"],
            "local_suppliers_availability": 65.5,
            "procurement_strategy": {
                "approach": "نهج المشتريات",
                "timeline": "الجدول الزمني",
                "key_considerations": ["اعتبار 1", "اعتبار 2"]
            }
        }
        """
        
        if context:
            prompt += "\n\nمعلومات سياقية إضافية:\n"
            for key, value in context.items():
                prompt += f"{key}: {value}\n"
        
        return prompt
    
    def _prepare_risk_analysis_prompt(self, extracted_text: str, context: Dict[str, Any]) -> str:
        """
        إعداد استعلام لتحليل المخاطر
        """
        # اختصار النص المستخرج إذا كان طويلاً جدًا
        max_chars = 15000  # الحد الأقصى لطول النص
        if len(extracted_text) > max_chars:
            extracted_text = extracted_text[:max_chars] + "... (تم اختصار النص)"
        
        prompt = """
        أنت خبير في تحليل المخاطر في المناقصات والمشاريع. يرجى تحليل النص التالي من وثيقة المناقصة وتحديد المخاطر المحتملة.
        
        نص المناقصة:
        """
        
        prompt += f"\n{extracted_text}"
        
        prompt += """
        
        يرجى تحديد وتحليل المخاطر التالية:
        1. المخاطر التقنية
        2. المخاطر المالية
        3. مخاطر سلسلة الإمداد
        4. المخاطر القانونية
        
        لكل مخاطرة، يرجى تقديم:
        - وصف المخاطرة
        - درجة الخطورة (على مقياس من 1 إلى 5)
        - احتمالية الحدوث (على مقياس من 1 إلى 5)
        - التأثير المحتمل
        - إجراءات مقترحة للتخفيف
        
        يرجى أيضًا تقديم خطة شاملة للتخفيف من المخاطر العالية.
        
        قدم الإجابة بتنسيق JSON التالي:
        {
            "all_risks": [
                {"risk": "وصف المخاطرة", "type": "نوع المخاطرة", "severity": 4, "probability": 3, "impact": "تأثير المخاطرة", "mitigation": "إجراءات التخفيف"}
            ],
            "technical_risks": [...],
            "financial_risks": [...],
            "supply_chain_risks": [...],
            "legal_risks": [...],
            "mitigation_plan": ["خطوة 1", "خطوة 2"],
            "avg_severity": 3.5
        }
        """
        
        if context:
            prompt += "\n\nمعلومات سياقية إضافية:\n"
            for key, value in context.items():
                prompt += f"{key}: {value}\n"
        
        return prompt
    
    def _prepare_summary_prompt(self, extracted_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> str:
        """
        إعداد استعلام لإعداد ملخص شامل
        """
        prompt = """
        أنت مستشار استراتيجي في مجال المناقصات والمشاريع. يرجى إعداد ملخص تنفيذي شامل وتوصيات استراتيجية بناءً على البيانات والتحليلات التالية.
        
        البيانات المستخرجة:
        """
        
        # إضافة البيانات المستخرجة
        for key, value in extracted_data.items():
            if isinstance(value, dict) or isinstance(value, list):
                prompt += f"\n{key}: {json.dumps(value, ensure_ascii=False)[:500]}..."
            else:
                prompt += f"\n{key}: {str(value)[:500]}..."
        
        prompt += "\n\nنتائج التحليلات:"
        
        # إضافة نتائج التحليلات
        for key, value in analysis_results.items():
            if isinstance(value, dict) or isinstance(value, list):
                prompt += f"\n{key}: {json.dumps(value, ensure_ascii=False)[:500]}..."
            else:
                prompt += f"\n{key}: {str(value)[:500]}..."
        
        prompt += """
        
        يرجى إعداد:
        1. ملخص تنفيذي شامل للمناقصة
        2. توصيات استراتيجية للتقدم للمناقصة
        3. استراتيجية تقديم العطاء، بما في ذلك النقاط التنافسية والأسعار المقترحة
        4. خطة عمل لتحسين فرص الفوز بالمناقصة
        
        قدم الإجابة بتنسيق JSON التالي:
        {
            "executive_summary": "ملخص تنفيذي شامل للمناقصة",
            "recommendations": ["توصية 1", "توصية 2", "توصية 3"],
            "bid_strategy": {
                "competitive_points": ["نقطة 1", "نقطة 2"],
                "proposed_price": "السعر المقترح",
                "profit_margin": "هامش الربح المقترح"
            },
            "action_plan": ["خطوة 1", "خطوة 2", "خطوة 3"]
        }
        """
        
        return prompt
    
    def _parse_requirements_response(self, response: str) -> Dict[str, Any]:
        """
        تحليل استجابة المتطلبات من النموذج
        """
        try:
            # البحث عن كتلة JSON في الاستجابة
            json_match = re.search(r'```json\s*(.*?)```', response, re.DOTALL)
            if not json_match:
                json_match = re.search(r'{.*}', response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1) if json_match.groups() else json_match.group(0)
                return json.loads(json_str)
            else:
                logger.warning("لم يتم العثور على JSON في استجابة تحليل المتطلبات. استخدام قيم افتراضية.")
                return {
                    "summary": "لم يتم تحليل المتطلبات بشكل صحيح",
                    "technical": [],
                    "financial": [],
                    "legal": [],
                    "local_content": [],
                    "total_count": 0,
                    "mandatory_count": 0,
                    "avg_difficulty": 0,
                    "local_content_percentage": 0
                }
        except json.JSONDecodeError as e:
            logger.error(f"خطأ في تحليل استجابة JSON للمتطلبات: {str(e)}")
            return {
                "summary": "حدث خطأ في تحليل استجابة JSON",
                "error": str(e),
                "raw_response": response[:1000] + "..." if len(response) > 1000 else response,
                "technical": [],
                "financial": [],
                "legal": [],
                "local_content": [],
                "total_count": 0,
                "mandatory_count": 0,
                "avg_difficulty": 0,
                "local_content_percentage": 0
            }
    
    def _parse_local_content_response(self, response: str) -> Dict[str, Any]:
        """
        تحليل استجابة المحتوى المحلي من النموذج
        """
        try:
            # البحث عن كتلة JSON في الاستجابة
            json_match = re.search(r'```json\s*(.*?)```', response, re.DOTALL)
            if not json_match:
                json_match = re.search(r'{.*}', response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1) if json_match.groups() else json_match.group(0)
                return json.loads(json_str)
            else:
                logger.warning("لم يتم العثور على JSON في استجابة تحليل المحتوى المحلي. استخدام قيم افتراضية.")
                return {
                    "estimated_local_content": 0,
                    "required_local_content": 0,
                    "required_materials": [],
                    "improvement_strategies": []
                }
        except json.JSONDecodeError as e:
            logger.error(f"خطأ في تحليل استجابة JSON للمحتوى المحلي: {str(e)}")
            return {
                "estimated_local_content": 0,
                "required_local_content": 0,
                "required_materials": [],
                "improvement_strategies": [],
                "error": str(e),
                "raw_response": response[:1000] + "..." if len(response) > 1000 else response
            }
    
    def _parse_supply_chain_response(self, response: str) -> Dict[str, Any]:
        """
        تحليل استجابة سلسلة الإمداد من النموذج
        """
        try:
            # البحث عن كتلة JSON في الاستجابة
            json_match = re.search(r'```json\s*(.*?)```', response, re.DOTALL)
            if not json_match:
                json_match = re.search(r'{.*}', response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1) if json_match.groups() else json_match.group(0)
                return json.loads(json_str)
            else:
                logger.warning("لم يتم العثور على JSON في استجابة تحليل سلسلة الإمداد. استخدام قيم افتراضية.")
                return {
                    "supply_chain_risks": [],
                    "optimizations": [],
                    "local_suppliers_availability": 0,
                    "procurement_strategy": {}
                }
        except json.JSONDecodeError as e:
            logger.error(f"خطأ في تحليل استجابة JSON لسلسلة الإمداد: {str(e)}")
            return {
                "supply_chain_risks": [],
                "optimizations": [],
                "local_suppliers_availability": 0,
                "procurement_strategy": {},
                "error": str(e),
                "raw_response": response[:1000] + "..." if len(response) > 1000 else response
            }
    
    def _parse_risk_response(self, response: str) -> Dict[str, Any]:
        """
        تحليل استجابة تحليل المخاطر من النموذج
        """
        try:
            # البحث عن كتلة JSON في الاستجابة
            json_match = re.search(r'```json\s*(.*?)```', response, re.DOTALL)
            if not json_match:
                json_match = re.search(r'{.*}', response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1) if json_match.groups() else json_match.group(0)
                return json.loads(json_str)
            else:
                logger.warning("لم يتم العثور على JSON في استجابة تحليل المخاطر. استخدام قيم افتراضية.")
                return {
                    "all_risks": [],
                    "technical_risks": [],
                    "financial_risks": [],
                    "supply_chain_risks": [],
                    "legal_risks": [],
                    "mitigation_plan": [],
                    "avg_severity": 0
                }
        except json.JSONDecodeError as e:
            logger.error(f"خطأ في تحليل استجابة JSON للمخاطر: {str(e)}")
            return {
                "all_risks": [],
                "technical_risks": [],
                "financial_risks": [],
                "supply_chain_risks": [],
                "legal_risks": [],
                "mitigation_plan": [],
                "avg_severity": 0,
                "error": str(e),
                "raw_response": response[:1000] + "..." if len(response) > 1000 else response
            }
    
    def _parse_summary_response(self, response: str) -> Dict[str, Any]:
        """
        تحليل استجابة الملخص من النموذج
        """
        try:
            # البحث عن كتلة JSON في الاستجابة
            json_match = re.search(r'```json\s*(.*?)```', response, re.DOTALL)
            if not json_match:
                json_match = re.search(r'{.*}', response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1) if json_match.groups() else json_match.group(0)
                return json.loads(json_str)
            else:
                logger.warning("لم يتم العثور على JSON في استجابة الملخص. استخدام قيم افتراضية.")
                return {
                    "executive_summary": "لم يتم إعداد الملخص بشكل صحيح",
                    "recommendations": [],
                    "bid_strategy": {},
                    "action_plan": []
                }
        except json.JSONDecodeError as e:
            logger.error(f"خطأ في تحليل استجابة JSON للملخص: {str(e)}")
            return {
                "executive_summary": "حدث خطأ في تحليل استجابة JSON",
                "recommendations": [],
                "bid_strategy": {},
                "action_plan": [],
                "error": str(e),
                "raw_response": response[:1000] + "..." if len(response) > 1000 else response
            }
    
    def _create_search_query(self, data) -> str:
        """
        إنشاء استعلام بحث من البيانات
        """
        if isinstance(data, list):
            # إذا كانت البيانات قائمة، جمع النصوص من العناصر
            texts = []
            for item in data:
                if isinstance(item, dict):
                    texts.extend([str(v) for k, v in item.items() if isinstance(v, (str, int, float))])
                else:
                    texts.append(str(item))
            return " ".join(texts[:20])  # استخدام أول 20 عنصر فقط
        
        elif isinstance(data, dict):
            # إذا كانت البيانات قاموس، جمع القيم النصية
            texts = [str(v) for k, v in data.items() if isinstance(v, (str, int, float))]
            return " ".join(texts[:20])  # استخدام أول 20 عنصر فقط
        
        else:
            # إذا كانت البيانات نص أو قيمة أخرى
            return str(data)
    
    def _format_retrieval_results(self, results: List[Dict[str, Any]]) -> str:
        """
        تنسيق نتائج الاسترجاع من قاعدة البيانات
        """
        if not results:
            return "لا توجد نتائج مسترجعة."
        
        formatted = ""
        for i, result in enumerate(results):
            formatted += f"\n{i+1}. "
            if 'title' in result:
                formatted += f"{result['title']}: "
            if 'content' in result:
                content = result['content']
                # اقتصار المحتوى إذا كان طويلاً
                if len(content) > 300:
                    content = content[:300] + "..."
                formatted += content
            if 'metadata' in result and isinstance(result['metadata'], dict):
                formatted += f"\n   معلومات إضافية: {', '.join([f'{k}: {v}' for k, v in result['metadata'].items() if k != 'text'])}"
            formatted += "\n"
        
        return formatted
    
    def _extract_keywords(self, text: str, top_n: int = 20) -> List[str]:
        """
        استخراج الكلمات المفتاحية من النص
        
        المعاملات:
        ----------
        text : str
            النص المراد استخراج الكلمات المفتاحية منه
        top_n : int, optional
            عدد الكلمات المفتاحية المراد استخراجها
            
        المخرجات:
        --------
        List[str]
            قائمة بالكلمات المفتاحية
        """
        # قائمة الكلمات الغير مهمة (stop words) باللغة العربية
        arabic_stop_words = ['من', 'الى', 'إلى', 'عن', 'على', 'في', 'و', 'ا', 'ان', 'أن', 'لا', 'ما', 'هذا', 'هذه', 'ذلك', 'تلك', 'هناك', 'هنالك', 'هو', 'هي', 'هم']
        
        # تنظيف النص وتقسيمه إلى كلمات
        words = re.findall(r'[\u0600-\u06FF]+|[a-zA-Z]+', text)
        
        # تحويل الكلمات إلى أحرف صغيرة وإزالة الكلمات الغير مهمة
        filtered_words = [word.lower() for word in words if word.lower() not in arabic_stop_words and len(word) > 2]
        
        # حساب تكرار الكلمات
        word_counts = {}
        for word in filtered_words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # ترتيب الكلمات حسب التكرار والحصول على أهم الكلمات
        sorted_words = [word for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True)]
        
        return sorted_words[:top_n]
    
    def _split_text_into_chunks(self, text: str, max_length: int = 4000) -> List[str]:
        """
        تقسيم النص إلى أجزاء أصغر لمعالجتها بشكل منفصل
        
        المعاملات:
        ----------
        text : str
            النص المراد تقسيمه
        max_length : int, optional
            الحد الأقصى لطول كل جزء
            
        المخرجات:
        --------
        List[str]
            قائمة بأجزاء النص
        """
        # إذا كان النص قصيراً، إرجاعه كما هو
        if len(text) <= max_length:
            return [text]
        
        # تقسيم النص إلى فقرات
        paragraphs = text.split('\n')
        
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # إذا كانت إضافة الفقرة ستجعل الجزء الحالي أطول من الحد الأقصى
            if len(current_chunk) + len(paragraph) > max_length:
                # إذا كان الجزء الحالي غير فارغ، إضافته إلى القائمة
                if current_chunk:
                    chunks.append(current_chunk)
                
                # إذا كانت الفقرة نفسها أطول من الحد الأقصى، تقسيمها
                if len(paragraph) > max_length:
                    # تقسيم الفقرة إلى جمل
                    sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                    
                    current_chunk = ""
                    for sentence in sentences:
                        if len(current_chunk) + len(sentence) > max_length:
                            if current_chunk:
                                chunks.append(current_chunk)
                            
                            # إذا كانت الجملة نفسها أطول من الحد الأقصى، تقسيمها
                            if len(sentence) > max_length:
                                # تقسيم الجملة إلى أجزاء بطول الحد الأقصى
                                for i in range(0, len(sentence), max_length):
                                    chunks.append(sentence[i:i+max_length])
                            else:
                                current_chunk = sentence
                        else:
                            current_chunk += " " + sentence if current_chunk else sentence
                else:
                    current_chunk = paragraph
            else:
                current_chunk += "\n" + paragraph if current_chunk else paragraph
        
        # إضافة الجزء الأخير إذا لم يكن فارغاً
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks