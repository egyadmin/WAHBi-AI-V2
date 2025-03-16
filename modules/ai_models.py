import os
import json
import re
import requests
import numpy as np
from typing import Dict, List, Any, Union, Tuple, Optional
from datetime import datetime
from dotenv import load_dotenv
import os

# تحميل المتغيرات البيئية
load_dotenv()

# استخدام المتغيرات البيئية
api_key = os.getenv("ANTHROPIC_API_KEY")

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
        
        الرجاء تقديم التحليل التالي:
        1. ملخص عام للمتطلبات
        2. تقييم جودة المتطلبات (الوضوح، الاكتمال، القابلية للقياس)
        3. تحديد أي فجوات أو تناقضات في المتطلبات
        4. توصيات لتحسين المتطلبات
        5. المخاطر المحتملة المرتبطة بهذه المتطلبات
        
        يرجى تقديم إجابتك في تنسيق JSON مع المفاتيح التالية: summary, quality_assessment, gaps, recommendations, risks
        """
        
        # إضافة معلومات السياق
        if context:
            prompt += "\n\nمعلومات إضافية للسياق:\n"
            for key, value in context.items():
                prompt += f"{key}: {value}\n"
        
        # إضافة محتوى RAG إذا كان مفعلاً
        if self.use_rag:
            relevant_content = self.vector_db.retrieve_similar_content(
                " ".join([req.get("title", "") + " " + req.get("description", "") for req in requirements])
            )
            
            if relevant_content:
                prompt += "\n\nمعلومات ذات صلة من مناقصات سابقة:\n"
                for i, content in enumerate(relevant_content):
                    prompt += f"{i+1}. {content}\n"
        
        return prompt
    
    def _prepare_local_content_prompt(self, local_content_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        إعداد استعلام لتحليل المحتوى المحلي
        """
        prompt = """
        أنت خبير في تحليل المحتوى المحلي في المناقصات. يرجى تحليل بيانات المحتوى المحلي التالية وتقديم نظرة ثاقبة حول الامتثال لمتطلبات المحتوى المحلي وفرص التحسين.
        
        بيانات المحتوى المحلي:
        """
        
        # إضافة بيانات المحتوى المحلي
        prompt += f"\nالنسبة الإجمالية للمحتوى المحلي: {local_content_data.get('overall_percentage', 'غير محدد')}%"
        
        if "breakdown" in local_content_data:
            prompt += "\n\nتفاصيل المحتوى المحلي:"
            for category, percentage in local_content_data["breakdown"].items():
                prompt += f"\n- {category}: {percentage}%"
        
        if "requirements" in local_content_data:
            prompt += "\n\nمتطلبات المحتوى المحلي:"
            for i, req in enumerate(local_content_data["requirements"]):
                prompt += f"\n{i+1}. {req.get('title', '')}: {req.get('description', '')}"
        
        prompt += """
        
        الرجاء تقديم التحليل التالي:
        1. تقييم الامتثال لمتطلبات المحتوى المحلي
        2. فرص تحسين نسبة المحتوى المحلي
        3. استراتيجيات لزيادة المحتوى المحلي
        4. المخاطر المرتبطة بالمحتوى المحلي
        5. أفضل الممارسات من مشاريع مماثلة
        
        يرجى تقديم إجابتك في تنسيق JSON مع المفاتيح التالية: compliance_assessment, improvement_opportunities, strategies, risks, best_practices
        """
        
        # إضافة معلومات السياق
        if context:
            prompt += "\n\nمعلومات إضافية للسياق:\n"
            for key, value in context.items():
                prompt += f"{key}: {value}\n"
        
        # إضافة محتوى RAG إذا كان مفعلاً
        if self.use_rag:
            relevant_content = self.vector_db.retrieve_similar_content("المحتوى المحلي نطاقات توطين")
            
            if relevant_content:
                prompt += "\n\nمعلومات ذات صلة من مناقصات سابقة:\n"
                for i, content in enumerate(relevant_content):
                    prompt += f"{i+1}. {content}\n"
        
        return prompt
    
    def _prepare_supply_chain_prompt(self, supply_chain_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        إعداد استعلام لتحليل سلسلة الإمداد
        """
        prompt = """
        أنت خبير في تحليل سلسلة الإمداد في المناقصات. يرجى تحليل بيانات سلسلة الإمداد التالية وتقديم نظرة ثاقبة حول المخاطر وفرص التحسين.
        
        بيانات سلسلة الإمداد:
        """
        
        # إضافة بيانات سلسلة الإمداد
        if "potential_suppliers" in supply_chain_data:
            prompt += "\n\nالموردين المحتملين:"
            for i, supplier in enumerate(supply_chain_data["potential_suppliers"][:5]):  # أخذ أول 5 موردين
                prompt += f"\n{i+1}. {supplier.get('name', '')}, التقييم: {supplier.get('rating', '')}, نسبة المحتوى المحلي: {supplier.get('local_content_percentage', '')}%"
        
        if "needed_materials" in supply_chain_data:
            prompt += "\n\nالمواد المطلوبة:"
            for i, material in enumerate(supply_chain_data["needed_materials"]):
                prompt += f"\n{i+1}. {material.get('name', '')}, التوفر المحلي: {material.get('local_availability', '')}"
        
        if "risks" in supply_chain_data:
            prompt += "\n\nالمخاطر:"
            for i, risk in enumerate(supply_chain_data["risks"]):
                prompt += f"\n{i+1}. {risk.get('title', '')}: {risk.get('description', '')}"
        
        prompt += """
        
        الرجاء تقديم التحليل التالي:
        1. تقييم عام لسلسلة الإمداد
        2. نقاط القوة والضعف في سلسلة الإمداد
        3. استراتيجيات لتحسين سلسلة الإمداد
        4. فرص لزيادة المحتوى المحلي في سلسلة الإمداد
        5. خطة للتخفيف من مخاطر سلسلة الإمداد
        
        يرجى تقديم إجابتك في تنسيق JSON مع المفاتيح التالية: overall_assessment, strengths_weaknesses, improvement_strategies, local_content_opportunities, risk_mitigation_plan
        """
        
        # إضافة معلومات السياق
        if context:
            prompt += "\n\nمعلومات إضافية للسياق:\n"
            for key, value in context.items():
                prompt += f"{key}: {value}\n"
        
        # إضافة محتوى RAG إذا كان مفعلاً
        if self.use_rag:
            relevant_content = self.vector_db.retrieve_similar_content("سلسلة الإمداد موردين مواد مخاطر")
            
            if relevant_content:
                prompt += "\n\nمعلومات ذات صلة من مناقصات سابقة:\n"
                for i, content in enumerate(relevant_content):
                    prompt += f"{i+1}. {content}\n"
        
        return prompt
    
    def _prepare_summary_prompt(self, extracted_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> str:
        """
        إعداد استعلام لإعداد ملخص شامل
        """
        prompt = """
        أنت خبير في تحليل المناقصات والعقود. يرجى إعداد ملخص تنفيذي شامل للمناقصة وتقديم توصيات استراتيجية بناءً على البيانات ونتائج التحليل المقدمة.
        
        معلومات المناقصة:
        """
        
        # إضافة معلومات أساسية عن المناقصة
        if "project_title" in extracted_data:
            prompt += f"\nعنوان المشروع: {extracted_data.get('project_title', '')}"
        
        if "project_type" in extracted_data:
            prompt += f"\nنوع المشروع: {extracted_data.get('project_type', '')}"
        
        if "financial_data" in extracted_data and "total_cost" in extracted_data["financial_data"]:
            total_cost = extracted_data["financial_data"]["total_cost"]
            prompt += f"\nالقيمة الإجمالية: {total_cost.get('value', '')} {total_cost.get('currency', 'ريال')}"
        
        # إضافة ملخص نتائج التحليل
        prompt += "\n\nملخص نتائج التحليل:"
        
        if "requirements" in analysis_results:
            req_count = len(analysis_results["requirements"].get("requirements", []))
            prompt += f"\n- تم تحليل {req_count} متطلبات"
            
            if "compliance" in analysis_results["requirements"]:
                compliance_rate = analysis_results["requirements"]["compliance"].get("compliance_rate", 0)
                prompt += f", نسبة الامتثال: {compliance_rate}%"
        
        if "local_content" in analysis_results:
            local_content = analysis_results["local_content"]
            prompt += f"\n- المحتوى المحلي: {local_content.get('overall_percentage', 0)}%"
        
        if "supply_chain" in analysis_results:
            supply_chain = analysis_results["supply_chain"]
            suppliers_count = len(supply_chain.get("potential_suppliers", []))
            risks_count = len(supply_chain.get("risks", []))
            prompt += f"\n- سلسلة الإمداد: {suppliers_count} موردين محتملين, {risks_count} مخاطر محددة"
        
        if "cost_analysis" in analysis_results:
            cost_analysis = analysis_results["cost_analysis"]
            if "contingency_reserve" in cost_analysis:
                prompt += f"\n- احتياطي الطوارئ المقترح: {cost_analysis.get('contingency_reserve', 0)} ريال"
        
        prompt += """
        
        الرجاء إعداد:
        1. ملخص تنفيذي (500-700 كلمة) يشمل:
           - نظرة عامة على المناقصة
           - النقاط الرئيسية من التحليل
           - الفرص والتحديات الرئيسية
           - توصيات استراتيجية
        
        2. قائمة بأهم 5-7 توصيات مرتبة حسب الأولوية، مع شرح موجز لكل توصية
        
        يرجى تقديم إجابتك في تنسيق JSON مع المفاتيح التالية: executive_summary, key_recommendations
        """
        
        # إضافة محتوى RAG إذا كان مفعلاً
        if self.use_rag:
            query = f"{extracted_data.get('project_title', '')} {extracted_data.get('project_type', '')}"
            relevant_content = self.vector_db.retrieve_similar_content(query)
            
            if relevant_content:
                prompt += "\n\nمعلومات ذات صلة من مناقصات سابقة:\n"
                for i, content in enumerate(relevant_content):
                    prompt += f"{i+1}. {content}\n"
        
        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        """
        استدعاء نموذج اللغة الكبيرة
        """
        try:
            # استدعاء واجهة برمجة التطبيقات Anthropic
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": self.model_name,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000,
                "temperature": 0.2
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["content"][0]["text"]
            else:
                print(f"Error calling LLM API: {response.status_code}, {response.text}")
                return f"Error: {response.status_code}, {response.text}"
        
        except Exception as e:
            print(f"Exception calling LLM API: {str(e)}")
            return f"Error: {str(e)}"
    
    def _parse_requirements_response(self, response: str) -> Dict[str, Any]:
        """
        معالجة استجابة تحليل المتطلبات
        """
        try:
            # محاولة استخراج JSON من الاستجابة
            json_pattern = r'```json(.*?)```'
            json_match = re.search(json_pattern, response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)
            
            # محاولة تحميل الاستجابة الكاملة كـ JSON
            return json.loads(response)
        
        except Exception as e:
            print(f"Error parsing requirements response: {str(e)}")
            
            # إذا فشل تحليل JSON، إرجاع النص كملخص
            return {
                "summary": response,
                "error": str(e)
            }
    
    def _parse_local_content_response(self, response: str) -> Dict[str, Any]:
        """
        معالجة استجابة تحليل المحتوى المحلي
        """
        try:
            # محاولة استخراج JSON من الاستجابة
            json_pattern = r'```json(.*?)```'
            json_match = re.search(json_pattern, response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)
            
            # محاولة تحميل الاستجابة الكاملة كـ JSON
            return json.loads(response)
        
        except Exception as e:
            print(f"Error parsing local content response: {str(e)}")
            
            # إذا فشل تحليل JSON، إرجاع النص كتقييم
            return {
                "compliance_assessment": response,
                "error": str(e)
            }
    
    def _parse_supply_chain_response(self, response: str) -> Dict[str, Any]:
        """
        معالجة استجابة تحليل سلسلة الإمداد
        """
        try:
            # محاولة استخراج JSON من الاستجابة
            json_pattern = r'```json(.*?)```'
            json_match = re.search(json_pattern, response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)
            
            # محاولة تحميل الاستجابة الكاملة كـ JSON
            return json.loads(response)
        
        except Exception as e:
            print(f"Error parsing supply chain response: {str(e)}")
            
            # إذا فشل تحليل JSON، إرجاع النص كتقييم
            return {
                "overall_assessment": response,
                "error": str(e)
            }
    
    def _parse_summary_response(self, response: str) -> Dict[str, Any]:
        """
        معالجة استجابة الملخص
        """
        try:
            # محاولة استخراج JSON من الاستجابة
            json_pattern = r'```json(.*?)```'
            json_match = re.search(json_pattern, response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)
            
            # محاولة تحميل الاستجابة الكاملة كـ JSON
            return json.loads(response)
        
        except Exception as e:
            print(f"Error parsing summary response: {str(e)}")
            
            # إذا فشل تحليل JSON، إرجاع النص كملخص
            return {
                "executive_summary": response,
                "error": str(e)
            }


class ArabicBERTModel:
    """
    فئة للتعامل مع نموذج BERT العربي المخصص لتحليل المناقصات
    """
    
    def __init__(self, model_path: str = "arabic-bert-base"):
        """
        تهيئة نموذج BERT العربي
        
        المعاملات:
        ----------
        model_path : str, optional
            مسار نموذج BERT العربي (افتراضي: "arabic-bert-base")
        """
        self.model_path = model_path
        
        # تحميل النموذج
        # في التطبيق الفعلي، يتم تحميل النموذج باستخدام مكتبة transformers
        # self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        # self.model = AutoModel.from_pretrained(model_path)
        
        # تمثيل مؤقت للنموذج
        self.model_loaded = False
    
    def extract_entities(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        استخراج الكيانات من النص
        
        المعاملات:
        ----------
        text : str
            النص المراد استخراج الكيانات منه
            
        المخرجات:
        --------
        Dict[str, List[Dict[str, Any]]]
            الكيانات المستخرجة مصنفة حسب النوع
        """
        # في التطبيق الفعلي، يتم استخدام النموذج لاستخراج الكيانات
        # هذا تمثيل مؤقت للوظيفة
        
        entities = {
            "organizations": [],
            "persons": [],
            "locations": [],
            "dates": [],
            "money": []
        }
        
        # استخراج المنظمات (مثال)
        org_pattern = r'(شركة|مؤسسة|هيئة|وزارة)\s+([^\n.,]{3,50})'
        org_matches = re.finditer(org_pattern, text)
        
        for match in org_matches:
            entity_text = match.group(0)
            entities["organizations"].append({
                "text": entity_text,
                "start": match.start(),
                "end": match.end(),
                "confidence": 0.85
            })
        
        # استخراج الأشخاص (مثال)
        person_pattern = r'(المهندس|الدكتور|السيد)\s+([^\n.,]{3,50})'
        person_matches = re.finditer(person_pattern, text)
        
        for match in person_matches:
            entity_text = match.group(0)
            entities["persons"].append({
                "text": entity_text,
                "start": match.start(),
                "end": match.end(),
                "confidence": 0.8
            })
        
        return entities
    
    def classify_text(self, text: str, categories: List[str]) -> Dict[str, float]:
        """
        تصنيف النص إلى فئات محددة
        
        المعاملات:
        ----------
        text : str
            النص المراد تصنيفه
        categories : List[str]
            قائمة الفئات المحتملة
            
        المخرجات:
        --------
        Dict[str, float]
            درجات الثقة لكل فئة
        """
        # في التطبيق الفعلي، يتم استخدام النموذج لتصنيف النص
        # هذا تمثيل مؤقت للوظيفة
        
        # توليد درجات ثقة عشوائية للفئات
        import random
        
        scores = {}
        total_score = 0
        
        for category in categories:
            score = random.random()
            scores[category] = score
            total_score += score
        
        # تطبيع درجات الثقة
        for category in scores:
            scores[category] = round(scores[category] / total_score, 2)
        
        return scores
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        استخراج الكلمات المفتاحية من النص
        
        المعاملات:
        ----------
        text : str
            النص المراد استخراج الكلمات المفتاحية منه
        top_n : int, optional
            عدد الكلمات المفتاحية المراد استخراجها (افتراضي: 10)
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            الكلمات المفتاحية مع درجات الأهمية
        """
        # في التطبيق الفعلي، يتم استخدام النموذج لاستخراج الكلمات المفتاحية
        # هذا تمثيل مؤقت للوظيفة
        
        # قائمة بالكلمات المفتاحية المحتملة في مجال المناقصات
        potential_keywords = [
            "مناقصة", "عقد", "توريد", "تنفيذ", "مشروع", "ميزانية", "مدة", "غرامة",
            "جودة", "مواصفات", "شروط", "تسليم", "ضمان", "كفالة", "دفعات", "مستحقات",
            "محتوى محلي", "توطين", "متطلبات", "مخاطر", "تكاليف", "سعر", "عمالة"
        ]
        
        # اختيار كلمات مفتاحية عشوائية من النص
        words = text.split()
        selected_keywords = []
        
        for keyword in potential_keywords:
            if keyword in words and len(selected_keywords) < top_n:
                count = words.count(keyword)
                selected_keywords.append({
                    "keyword": keyword,
                    "count": count,
                    "importance": round(count / len(words) * 10, 2)
                })
        
        # ترتيب الكلمات المفتاحية حسب الأهمية
        selected_keywords = sorted(selected_keywords, key=lambda x: x["importance"], reverse=True)
        
        return selected_keywords


class VectorDB:
    """
    فئة للتعامل مع قاعدة بيانات المتجهات لدعم عمليات RAG
    """
    
    def __init__(self, db_path: str = "vector_db"):
        """
        تهيئة قاعدة بيانات المتجهات
        
        المعاملات:
        ----------
        db_path : str, optional
            مسار قاعدة بيانات المتجهات (افتراضي: "vector_db")
        """
        self.db_path = db_path
        
        # في التطبيق الفعلي، يتم تحميل أو إنشاء قاعدة بيانات المتجهات
        # هذا تمثيل مؤقت للوظيفة
        
        # قاعدة بيانات مؤقتة للأغراض التوضيحية
        self.sample_db = [
            {
                "text": "تعتبر نسبة المحتوى المحلي من أهم العوامل في تقييم المناقصات، حيث يجب أن تكون 40% على الأقل للمشاريع الإنشائية و30% للمشاريع التقنية وفقاً لمتطلبات هيئة المحتوى المحلي والمشتريات الحكومية.",
                "vector": np.random.rand(384)  # تمثيل عشوائي للمتجه
            },
            {
                "text": "يعد تحليل المخاطر في سلسلة الإمداد جزءاً أساسياً من تقييم المناقصات، خاصةً في ظل تقلبات الأسعار العالمية وتأثيرها على توفر المواد.",
                "vector": np.random.rand(384)
            },
            {
                "text": "من أفضل الممارسات في إدارة المناقصات تقسيم المتطلبات إلى فئات واضحة (فنية، إدارية، مالية) مع تحديد الأولويات والمعايير القابلة للقياس.",
                "vector": np.random.rand(384)
            },
            {
                "text": "وفقاً لنظام المنافسات والمشتريات الحكومية، يجب تضمين بند التوطين ونسبة المحتوى المحلي في جميع المناقصات الحكومية، مع منح أفضلية للعروض ذات النسب الأعلى.",
                "vector": np.random.rand(384)
            },
            {
                "text": "من التحديات الشائعة في تنفيذ المشاريع الإنشائية: تأخر توريد المواد، ونقص العمالة الماهرة، وتغيير نطاق العمل، والتأخير في اعتماد المخططات.",
                "vector": np.random.rand(384)
            }
        ]
    
    def retrieve_similar_content(self, query: str, top_k: int = 3) -> List[str]:
        """
        استرجاع المحتوى المشابه للاستعلام من قاعدة البيانات
        
        المعاملات:
        ----------
        query : str
            الاستعلام المراد البحث عن محتوى مشابه له
        top_k : int, optional
            عدد النتائج المراد استرجاعها (افتراضي: 3)
            
        المخرجات:
        --------
        List[str]
            قائمة بالمحتوى المشابه للاستعلام
        """
        # في التطبيق الفعلي، يتم تحويل الاستعلام إلى متجه والبحث في قاعدة البيانات
        # هذا تمثيل مؤقت للوظيفة
        
        # اختيار محتوى عشوائي من قاعدة البيانات
        import random
        
        # تحقق بسيط من وجود كلمات مشتركة بين الاستعلام والمحتوى
        query_words = set(query.lower().split())
        matching_content = []
        
        for item in self.sample_db:
            content_words = set(item["text"].lower().split())
            common_words = query_words.intersection(content_words)
            
            if common_words:
                matching_content.append(item["text"])
        
        # إذا لم يتم العثور على تطابق، إرجاع عناصر عشوائية
        if not matching_content and self.sample_db:
            return random.sample([item["text"] for item in self.sample_db], min(top_k, len(self.sample_db)))
        
        # إرجاع أفضل النتائج (أو كل النتائج إذا كان عددها أقل من top_k)
        return matching_content[:top_k]