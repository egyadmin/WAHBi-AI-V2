import os
import json
import re
import requests
import numpy as np
from typing import Dict, List, Any, Union, Tuple, Optional
from datetime import datetime

class LLMProcessor:
    """
    فئة للتعامل مع نماذج اللغة الكبيرة (LLM) لتحليل المناقصات
    """
    
    def __init__(self, model_name: str = "claude-3-haiku-20240307", use_rag: bool = True):
        """
        تهيئة معالج نماذج اللغة الكبيرة
        
        المعاملات:
        ----------
        model_name : str, optional
            اسم النموذج المستخدم (افتراضي: "claude-3-haiku-20240307")
        use_rag : bool, optional
            استخدام تقنية RAG (Retrieval-Augmented Generation) (افتراضي: True)
        """
        self.model_name = model_name
        self.use_rag = use_rag
        
        # الحصول على مفتاح واجهة برمجة التطبيقات من متغيرات البيئة
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # تهيئة قاعدة بيانات المتجهات إذا كان استخدام RAG مفعلاً
        if self.use_rag:
            self.vector_db = VectorDB()
    
    def analyze_requirements(self, requirements: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل المتطلبات باستخدام نموذج اللغة الكبيرة
        
        المعاملات:
        ----------
        requirements : List[Dict[str, Any]]
            قائمة المتطلبات المستخرجة من المستندات
        context : Dict[str, Any]
            معلومات السياق الإضافية
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المتطلبات
        """
        # إعداد الاستعلام بناءً على المتطلبات والسياق
        prompt = self._prepare_requirements_prompt(requirements, context)
        
        # استدعاء النموذج
        response = self._call_llm(prompt)
        
        # معالجة الاستجابة
        analysis = self._parse_requirements_response(response)
        
        return analysis
    
    def analyze_local_content(self, local_content_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل بيانات المحتوى المحلي باستخدام نموذج اللغة الكبيرة
        
        المعاملات:
        ----------
        local_content_data : Dict[str, Any]
            بيانات المحتوى المحلي المستخرجة
        context : Dict[str, Any]
            معلومات السياق الإضافية
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المحتوى المحلي
        """
        # إعداد الاستعلام بناءً على بيانات المحتوى المحلي والسياق
        prompt = self._prepare_local_content_prompt(local_content_data, context)
        
        # استدعاء النموذج
        response = self._call_llm(prompt)
        
        # معالجة الاستجابة
        analysis = self._parse_local_content_response(response)
        
        return analysis
    
    def analyze_supply_chain(self, supply_chain_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل بيانات سلسلة الإمداد باستخدام نموذج اللغة الكبيرة
        
        المعاملات:
        ----------
        supply_chain_data : Dict[str, Any]
            بيانات سلسلة الإمداد المستخرجة
        context : Dict[str, Any]
            معلومات السياق الإضافية
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل سلسلة الإمداد
        """
        # إعداد الاستعلام بناءً على بيانات سلسلة الإمداد والسياق
        prompt = self._prepare_supply_chain_prompt(supply_chain_data, context)
        
        # استدعاء النموذج
        response = self._call_llm(prompt)
        
        # معالجة الاستجابة
        analysis = self._parse_supply_chain_response(response)
        
        return analysis
    
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
        # إعداد الاستعلام بناءً على البيانات المستخرجة ونتائج التحليل
        prompt = self._prepare_summary_prompt(extracted_data, analysis_results)
        
        # استدعاء النموذج
        response = self._call_llm(prompt)
        
        # معالجة الاستجابة
        summary = self._parse_summary_response(response)
        
        return summary
    
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
        
        الرجاء ت