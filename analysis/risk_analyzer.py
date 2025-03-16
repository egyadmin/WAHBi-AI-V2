"""
محلل المخاطر في المناقصات
يقوم بتحليل وتحديد المخاطر المحتملة في المناقصات وتقديم خطط للتخفيف منها
"""

import re
import json
import logging
import os
from typing import Dict, List, Any, Tuple, Optional, Union
import numpy as np
from collections import defaultdict

logger = logging.getLogger(__name__)

class RiskAnalyzer:
    """
    محلل المخاطر في المناقصات
    """
    
    def __init__(self, llm_processor, config=None):
        """
        تهيئة محلل المخاطر
        
        المعاملات:
        ----------
        llm_processor : LLMProcessor
            معالج نماذج اللغة الكبيرة
        config : Dict, optional
            إعدادات المحلل
        """
        self.config = config or {}
        self.llm_processor = llm_processor
        
        # تحميل قوالب المخاطر
        self.risk_templates = self._load_risk_templates()
        
        logger.info("تم تهيئة محلل المخاطر")
    
    def analyze(self, extracted_text: str) -> Dict[str, Any]:
        """
        تحليل المخاطر من نص المناقصة
        
        المعاملات:
        ----------
        extracted_text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المخاطر
        """
        try:
            logger.info("بدء تحليل المخاطر")
            
            # إذا كان معالج LLM متوفرًا، استخدمه لتحليل المخاطر
            if self.llm_processor:
                # تحليل المخاطر باستخدام نموذج اللغة الكبيرة
                llm_risks = self.llm_processor.analyze_risks(extracted_text)
                
                # استخدام المعلومات من تحليل LLM والمراجعة
                risk_analysis = self._review_and_enhance_risks(llm_risks, extracted_text)
                
                logger.info(f"اكتمل تحليل المخاطر باستخدام LLM: {len(risk_analysis['all_risks'])} مخاطر محددة")
                return risk_analysis
            else:
                # تحليل المخاطر باستخدام النهج التقليدي
                return self._traditional_risk_analysis(extracted_text)
            
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
    
    def _traditional_risk_analysis(self, text: str) -> Dict[str, Any]:
        """
        تحليل المخاطر باستخدام النهج التقليدي
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المخاطر
        """
        # استخراج المخاطر من قوالب المخاطر
        all_risks = []
        
        # تحديد نوع المشروع
        project_type = self._determine_project_type(text)
        
        # استخراج المخاطر المشتركة
        common_risks = self.risk_templates.get("common_risks", [])
        all_risks.extend(common_risks)
        
        # استخراج المخاطر الخاصة بنوع المشروع
        project_specific_risks = self.risk_templates.get("project_types", {}).get(project_type, [])
        all_risks.extend(project_specific_risks)
        
        # البحث عن المخاطر المذكورة صراحة في النص
        explicit_risks = self._extract_explicit_risks(text)
        all_risks.extend(explicit_risks)
        
        # تصنيف المخاطر
        technical_risks = [risk for risk in all_risks if risk.get("type") == "technical"]
        financial_risks = [risk for risk in all_risks if risk.get("type") == "financial"]
        supply_chain_risks = [risk for risk in all_risks if risk.get("type") == "supply_chain"]
        legal_risks = [risk for risk in all_risks if risk.get("type") == "legal"]
        
        # حساب متوسط الخطورة
        if all_risks:
            avg_severity = sum(risk.get("severity", 0) for risk in all_risks) / len(all_risks)
        else:
            avg_severity = 0
        
        # إعداد خطة تخفيف المخاطر
        mitigation_plan = self._generate_mitigation_plan(all_risks)
        
        return {
            "all_risks": all_risks,
            "technical_risks": technical_risks,
            "financial_risks": financial_risks,
            "supply_chain_risks": supply_chain_risks,
            "legal_risks": legal_risks,
            "mitigation_plan": mitigation_plan,
            "avg_severity": avg_severity
        }
    
    def _determine_project_type(self, text: str) -> str:
        """
        تحديد نوع المشروع من النص
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        str
            نوع المشروع
        """
        # البحث عن الكلمات المفتاحية
        keywords = {
            "construction": ["إنشاء", "بناء", "تشييد", "مبنى", "عمارة", "هيكل", "مركز"],
            "infrastructure": ["طريق", "جسر", "نفق", "سد", "شبكة", "بنية تحتية"],
            "technology": ["تقنية", "برمجة", "نظام", "برنامج", "تطبيق", "حاسب", "رقمية"],
            "maintenance": ["صيانة", "تأهيل", "إصلاح", "ترميم", "تحديث", "تجديد"],
            "consulting": ["استشارة", "دراسة", "تصميم", "تخطيط", "استراتيجية"],
            "services": ["خدمة", "تشغيل", "إدارة", "تقديم"]
        }
        
        # حساب عدد مرات ظهور كل كلمة مفتاحية
        scores = defaultdict(int)
        
        for project_type, words in keywords.items():
            for word in words:
                count = len(re.findall(r'\b' + re.escape(word) + r'\w*', text, re.IGNORECASE))
                scores[project_type] += count
        
        # تحديد نوع المشروع بناءً على أعلى نتيجة
        if not scores:
            return "general"
        
        return max(scores, key=scores.get)
    
    def _extract_explicit_risks(self, text: str) -> List[Dict[str, Any]]:
        """
        استخراج المخاطر المذكورة صراحة في النص
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة بالمخاطر المستخرجة
        """
        explicit_risks = []
        
        # البحث عن كلمات المخاطر
        risk_keywords = [
            "مخاطر", "مخاطرة", "خطر", "تحدي", "صعوبة", "مشكلة", "عائق",
            "تأخير", "تأخر", "عدم الالتزام", "خرق", "غرامة", "عقوبة"
        ]
        
        # البحث عن الفقرات التي تحتوي على كلمات المخاطر
        for keyword in risk_keywords:
            # البحث عن الفقرات التي تحتوي على الكلمة المفتاحية
            matches = re.finditer(r'(?:[^\n.]*' + re.escape(keyword) + r'[^\n.]*[.\n])', text)
            
            for match in matches:
                risk_text = match.group(0).strip()
                
                # تحديد نوع المخاطرة
                risk_type = "general"
                
                if any(word in risk_text.lower() for word in ["فني", "تقني", "هندسي", "جودة"]):
                    risk_type = "technical"
                elif any(word in risk_text.lower() for word in ["مالي", "تكلفة", "سعر", "تمويل", "ميزانية"]):
                    risk_type = "financial"
                elif any(word in risk_text.lower() for word in ["توريد", "إمداد", "مورد", "تأخير", "تسليم"]):
                    risk_type = "supply_chain"
                elif any(word in risk_text.lower() for word in ["قانوني", "نظامي", "عقد", "التزام", "شرط", "غرامة"]):
                    risk_type = "legal"
                
                # تقدير مستوى الخطورة
                severity = 3  # متوسط افتراضيًا
                
                if any(word in risk_text.lower() for word in ["كبير", "خطير", "جسيم", "عالي"]):
                    severity = 4
                elif any(word in risk_text.lower() for word in ["متوسط"]):
                    severity = 3
                elif any(word in risk_text.lower() for word in ["بسيط", "صغير", "منخفض"]):
                    severity = 2
                
                # تقدير احتمالية الحدوث
                probability = 3  # متوسط افتراضيًا
                
                if any(word in risk_text.lower() for word in ["مؤكد", "حتمي", "دائمًا"]):
                    probability = 5
                elif any(word in risk_text.lower() for word in ["محتمل", "غالبًا"]):
                    probability = 4
                elif any(word in risk_text.lower() for word in ["ممكن", "أحيانًا"]):
                    probability = 3
                elif any(word in risk_text.lower() for word in ["نادر", "غير محتمل"]):
                    probability = 2
                elif any(word in risk_text.lower() for word in ["مستبعد", "غير ممكن"]):
                    probability = 1
                
                # إضافة المخاطرة إذا لم تكن موجودة بالفعل
                if not any(risk["risk"] == risk_text for risk in explicit_risks):
                    explicit_risks.append({
                        "risk": risk_text,
                        "type": risk_type,
                        "severity": severity,
                        "probability": probability,
                        "impact": "غير محدد",
                        "mitigation": "غير محدد"
                    })
        
        return explicit_risks
    
    def _review_and_enhance_risks(self, llm_risks: Dict[str, Any], text: str) -> Dict[str, Any]:
        """
        مراجعة وتعزيز المخاطر المحددة من LLM
        
        المعاملات:
        ----------
        llm_risks : Dict[str, Any]
            نتائج تحليل المخاطر من LLM
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المخاطر المحسنة
        """
        # استخراج المخاطر من قوالب المخاطر
        template_risks = []
        
        # تحديد نوع المشروع
        project_type = self._determine_project_type(text)
        
        # استخراج المخاطر المشتركة
        common_risks = self.risk_templates.get("common_risks", [])
        template_risks.extend(common_risks)
        
        # استخراج المخاطر الخاصة بنوع المشروع
        project_specific_risks = self.risk_templates.get("project_types", {}).get(project_type, [])
        template_risks.extend(project_specific_risks)
        
        # دمج المخاطر من LLM والقوالب
        all_risks = llm_risks.get("all_risks", []).copy()
        
        # إضافة المخاطر من القوالب التي لم تكن موجودة بالفعل
        for template_risk in template_risks:
            if not any(self._is_similar_risk(template_risk, existing_risk) for existing_risk in all_risks):
                all_risks.append(template_risk)
        
        # تحديث تصنيف المخاطر
        technical_risks = [risk for risk in all_risks if risk.get("type") == "technical"]
        financial_risks = [risk for risk in all_risks if risk.get("type") == "financial"]
        supply_chain_risks = [risk for risk in all_risks if risk.get("type") == "supply_chain"]
        legal_risks = [risk for risk in all_risks if risk.get("type") == "legal"]
        
        # حساب متوسط الخطورة
        if all_risks:
            avg_severity = sum(risk.get("severity", 0) for risk in all_risks) / len(all_risks)
        else:
            avg_severity = 0
        
        # إعداد خطة تخفيف المخاطر
        mitigation_plan = llm_risks.get("mitigation_plan", [])
        if not mitigation_plan:
            mitigation_plan = self._generate_mitigation_plan(all_risks)
        
        return {
            "all_risks": all_risks,
            "technical_risks": technical_risks,
            "financial_risks": financial_risks,
            "supply_chain_risks": supply_chain_risks,
            "legal_risks": legal_risks,
            "mitigation_plan": mitigation_plan,
            "avg_severity": avg_severity
        }
    
    def _is_similar_risk(self, risk1: Dict[str, Any], risk2: Dict[str, Any]) -> bool:
        """
        التحقق مما إذا كانت المخاطرتان متشابهتين
        
        المعاملات:
        ----------
        risk1 : Dict[str, Any]
            المخاطرة الأولى
        risk2 : Dict[str, Any]
            المخاطرة الثانية
            
        المخرجات:
        --------
        bool
            True إذا كانت المخاطرتان متشابهتين، False خلاف ذلك
        """
        # التحقق من التشابه في النص
        risk1_text = risk1.get("risk", "").lower()
        risk2_text = risk2.get("risk", "").lower()
        
        # تحويل النصوص إلى مجموعات من الكلمات
        words1 = set(risk1_text.split())
        words2 = set(risk2_text.split())
        
        # حساب معامل جاكارد للتشابه
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        if union == 0:
            return False
        
        jaccard = intersection / union
        
        # إذا كان معامل التشابه أكبر من العتبة، نعتبر المخاطرتين متشابهتين
        return jaccard > 0.3
    
    def _generate_mitigation_plan(self, risks: List[Dict[str, Any]]) -> List[str]:
        """
        إعداد خطة تخفيف المخاطر
        
        المعاملات:
        ----------
        risks : List[Dict[str, Any]]
            قائمة المخاطر
            
        المخرجات:
        --------
        List[str]
            خطة تخفيف المخاطر
        """
        mitigation_plan = []
        
        # ترتيب المخاطر حسب الخطورة
        sorted_risks = sorted(risks, key=lambda x: x.get("severity", 0) * x.get("probability", 0), reverse=True)
        
        # إعداد خطة للمخاطر العالية
        high_risks = [risk for risk in sorted_risks if risk.get("severity", 0) >= 4 or (risk.get("severity", 0) >= 3 and risk.get("probability", 0) >= 4)]
        
        if high_risks:
            mitigation_plan.append("إدارة المخاطر العالية:")
            
            for i, risk in enumerate(high_risks):
                mitigation = risk.get("mitigation", "")
                if mitigation and mitigation != "غير محدد":
                    mitigation_plan.append(f"{i+1}. {risk.get('risk', '')}: {mitigation}")
                else:
                    # إنشاء استراتيجية تخفيف افتراضية
                    default_mitigation = self._generate_default_mitigation(risk)
                    mitigation_plan.append(f"{i+1}. {risk.get('risk', '')}: {default_mitigation}")
        
        # إعداد خطة للمخاطر المتوسطة
        medium_risks = [risk for risk in sorted_risks if risk.get("severity", 0) == 3 and risk.get("probability", 0) <= 3]
        
        if medium_risks:
            mitigation_plan.append("\nإدارة المخاطر المتوسطة:")
            
            for i, risk in enumerate(medium_risks[:3]):  # اختيار أهم 3 مخاطر متوسطة
                mitigation = risk.get("mitigation", "")
                if mitigation and mitigation != "غير محدد":
                    mitigation_plan.append(f"{i+1}. {risk.get('risk', '')}: {mitigation}")
                else:
                    # إنشاء استراتيجية تخفيف افتراضية
                    default_mitigation = self._generate_default_mitigation(risk)
                    mitigation_plan.append(f"{i+1}. {risk.get('risk', '')}: {default_mitigation}")
        
        # إضافة استراتيجيات عامة
        mitigation_plan.extend([
            "\nاستراتيجيات عامة لإدارة المخاطر:",
            "- إعداد سجل المخاطر ومراجعته بشكل دوري",
            "- تعيين مسؤول لإدارة المخاطر ومتابعة خطط التخفيف",
            "- إعداد خطط طوارئ للمخاطر العالية",
            "- التواصل المستمر مع العميل والموردين لتحديد المخاطر المحتملة مبكرًا",
            "- توثيق الدروس المستفادة من المشاريع السابقة"
        ])
        
        return mitigation_plan
    
    def _generate_default_mitigation(self, risk: Dict[str, Any]) -> str:
        """
        إنشاء استراتيجية تخفيف افتراضية للمخاطرة
        
        المعاملات:
        ----------
        risk : Dict[str, Any]
            المخاطرة
            
        المخرجات:
        --------
        str
            استراتيجية التخفيف
        """
        risk_type = risk.get("type", "general")
        
        if risk_type == "technical":
            return "إجراء مراجعة فنية مفصلة، والاستعانة بخبراء متخصصين، وإعداد خطة اختبار شاملة."
        elif risk_type == "financial":
            return "إعداد ميزانية احتياطية، ومراجعة التكاليف بشكل دوري، وتأمين مصادر تمويل بديلة."
        elif risk_type == "supply_chain":
            return "تحديد موردين بدلاء، وإعداد مخزون احتياطي من المواد الحرجة، والتعاقد المبكر مع الموردين الرئيسيين."
        elif risk_type == "legal":
            return "مراجعة العقد من قبل مستشار قانوني، وتوثيق جميع التغييرات والموافقات، والالتزام الدقيق بالمتطلبات القانونية."
        else:
            return "إعداد خطة إدارة مخاطر مفصلة، وتعيين فريق لمتابعة المخاطر، وإجراء مراجعات دورية."
    
    def _load_risk_templates(self) -> Dict[str, Any]:
        """
        تحميل قوالب المخاطر
        
        المخرجات:
        --------
        Dict[str, Any]
            قوالب المخاطر
        """
        try:
            file_path = 'data/templates/risk_template.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"ملف قوالب المخاطر غير موجود: {file_path}")
                # إنشاء قوالب افتراضية
                return self._create_default_risk_templates()
        except Exception as e:
            logger.error(f"فشل في تحميل قوالب المخاطر: {str(e)}")
            return self._create_default_risk_templates()
    
    def _create_default_risk_templates(self) -> Dict[str, Any]:
        """
        إنشاء قوالب افتراضية للمخاطر
        
        المخرجات:
        --------
        Dict[str, Any]
            قوالب افتراضية للمخاطر
        """
        return {
            "common_risks": [
                {
                    "risk": "تأخر في تسليم المواد من الموردين",
                    "type": "supply_chain",
                    "severity": 4,
                    "probability": 3,
                    "impact": "تأخير في جدول المشروع وزيادة التكاليف",
                    "mitigation": "تحديد موردين بدلاء وإعداد مخزون احتياطي من المواد الحرجة"
                },
                {
                    "risk": "تغييرات في نطاق العمل من قبل العميل",
                    "type": "technical",
                    "severity": 3,
                    "probability": 4,
                    "impact": "زيادة في التكاليف وتأخير في الجدول الزمني",
                    "mitigation": "توثيق نطاق العمل بدقة وإعداد إجراءات واضحة لإدارة التغييرات"
                },
                {
                    "risk": "نقص في العمالة الماهرة",
                    "type": "technical",
                    "severity": 3,
                    "probability": 3,
                    "impact": "انخفاض جودة العمل وتأخير في الجدول الزمني",
                    "mitigation": "التخطيط المبكر للموارد البشرية والتعاقد مع مقاولي الباطن المؤهلين"
                },
                {
                    "risk": "مشاكل في التدفق النقدي",
                    "type": "financial",
                    "severity": 4,
                    "probability": 3,
                    "impact": "عدم القدرة على تمويل المشروع وتأخير في التنفيذ",
                    "mitigation": "إعداد خطة تدفق نقدي دقيقة وتأمين تسهيلات ائتمانية"
                },
                {
                    "risk": "زيادة في أسعار المواد والخدمات",
                    "type": "financial",
                    "severity": 3,
                    "probability": 4,
                    "impact": "زيادة التكاليف وانخفاض هامش الربح",
                    "mitigation": "تضمين بند تعديل الأسعار في العقود وإعداد ميزانية احتياطية"
                },
                {
                    "risk": "تأخر في الحصول على التصاريح والموافقات",
                    "type": "legal",
                    "severity": 4,
                    "probability": 3,
                    "impact": "تأخير في بدء المشروع وزيادة التكاليف",
                    "mitigation": "بدء عملية الحصول على التصاريح مبكرًا والتواصل المستمر مع الجهات المعنية"
                },
                {
                    "risk": "نزاعات تعاقدية مع العميل أو المقاولين",
                    "type": "legal",
                    "severity": 4,
                    "probability": 2,
                    "impact": "تأخير في المشروع وتكاليف قانونية",
                    "mitigation": "صياغة العقود بدقة وتوثيق جميع التغييرات والموافقات"
                }
            ],
            "project_types": {
                "construction": [
                    {
                        "risk": "ظروف موقع غير متوقعة",
                        "type": "technical",
                        "severity": 4,
                        "probability": 3,
                        "impact": "زيادة في التكاليف وتأخير في الجدول الزمني",
                        "mitigation": "إجراء دراسات جيوتقنية شاملة وزيارات ميدانية للموقع"
                    },
                    {
                        "risk": "مشاكل في جودة المواد وعدم مطابقتها للمواصفات",
                        "type": "technical",
                        "severity": 4,
                        "probability": 3,
                        "impact": "إعادة العمل وتأخير في الجدول الزمني",
                        "mitigation": "تطبيق إجراءات فحص الجودة واختيار موردين موثوقين"
                    },
                    {
                        "risk": "حوادث السلامة في موقع العمل",
                        "type": "technical",
                        "severity": 5,
                        "probability": 2,
                        "impact": "إصابات للعاملين وتوقف العمل والمسؤولية القانونية",
                        "mitigation": "تنفيذ خطة سلامة شاملة وتدريب العاملين على إجراءات السلامة"
                    }
                ],
                "infrastructure": [
                    {
                        "risk": "تعارض مع مرافق تحت الأرض",
                        "type": "technical",
                        "severity": 4,
                        "probability": 3,
                        "impact": "إعادة التصميم وتأخير في الجدول الزمني",
                        "mitigation": "إجراء مسح شامل للمرافق تحت الأرض قبل بدء العمل"
                    },
                    {
                        "risk": "تأثير على حركة المرور والمناطق المحيطة",
                        "type": "technical",
                        "severity": 3,
                        "probability": 4,
                        "impact": "شكاوى من السكان والسلطات وتأخير في العمل",
                        "mitigation": "إعداد خطة إدارة حركة المرور والتواصل مع المجتمع المحلي"
                    },
                    {
                        "risk": "متطلبات بيئية غير متوقعة",
                        "type": "legal",
                        "severity": 4,
                        "probability": 3,
                        "impact": "تأخير في المشروع وتكاليف إضافية",
                        "mitigation": "إجراء تقييم بيئي شامل والتواصل مع الجهات البيئية"
                    }
                ],
                "technology": [
                    {
                        "risk": "مشاكل في تكامل النظام",
                        "type": "technical",
                        "severity": 4,
                        "probability": 3,
                        "impact": "عدم عمل النظام بشكل صحيح وتأخير في التسليم",
                        "mitigation": "إجراء اختبارات تكامل شاملة وإشراك مختصين في التكامل"
                    },
                    {
                        "risk": "تغيير في التكنولوجيا أثناء المشروع",
                        "type": "technical",
                        "severity": 3,
                        "probability": 3,
                        "impact": "تقادم الحلول المقترحة وزيادة التكاليف",
                        "mitigation": "اعتماد تقنيات مستقرة ومرونة في التصميم"
                    },
                    {
                        "risk": "مشاكل في أمن المعلومات",
                        "type": "technical",
                        "severity": 4,
                        "probability": 3,
                        "impact": "اختراقات أمنية ومسؤولية قانونية",
                        "mitigation": "تنفيذ معايير أمنية صارمة وإجراء اختبارات اختراق"
                    }
                ],
                "consulting": [
                    {
                        "risk": "عدم وضوح متطلبات العميل",
                        "type": "technical",
                        "severity": 3,
                        "probability": 4,
                        "impact": "إعادة العمل وعدم رضا العميل",
                        "mitigation": "توثيق المتطلبات بشكل تفصيلي واجتماعات منتظمة مع العميل"
                    },
                    {
                        "risk": "نقص في المعلومات اللازمة",
                        "type": "technical",
                        "severity": 3,
                        "probability": 3,
                        "impact": "تأخير في المشروع ومخرجات غير دقيقة",
                        "mitigation": "تحديد المعلومات المطلوبة مبكرًا والتواصل مع مصادر البيانات"
                    },
                    {
                        "risk": "مشاكل في قبول التسليمات",
                        "type": "technical",
                        "severity": 3,
                        "probability": 3,
                        "impact": "إعادة العمل وتأخير في الدفعات",
                        "mitigation": "تحديد معايير القبول بوضوح ومراجعات منتظمة مع العميل"
                    }
                ],
                "general": [
                    {
                        "risk": "مخاطر القوة القاهرة (كوارث طبيعية، أوبئة)",
                        "type": "technical",
                        "severity": 5,
                        "probability": 1,
                        "impact": "توقف المشروع بالكامل",
                        "mitigation": "إعداد خطة طوارئ وتضمين بند القوة القاهرة في العقود"
                    },
                    {
                        "risk": "تغييرات في اللوائح والأنظمة",
                        "type": "legal",
                        "severity": 3,
                        "probability": 2,
                        "impact": "تعديلات في التصميم وزيادة التكاليف",
                        "mitigation": "متابعة التحديثات التنظيمية والتشاور مع المستشارين القانونيين"
                    },
                    {
                        "risk": "مشاكل في التواصل مع أصحاب المصلحة",
                        "type": "technical",
                        "severity": 3,
                        "probability": 3,
                        "impact": "تأخيرات وسوء فهم وعدم رضا",
                        "mitigation": "إعداد خطة تواصل شاملة واجتماعات منتظمة مع أصحاب المصلحة"
                    }
                ]
            }
        }