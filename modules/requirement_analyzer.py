import re
import os
import json
import numpy as np
from typing import Dict, List, Any
from datetime import datetime

# استيراد نماذج الذكاء الاصطناعي
from modules.ai_models import LLMProcessor


class RequirementAnalyzer:
    """
    فئة لتحليل متطلبات المناقصة وتقييمها
    """

    def __init__(self, use_ai: bool = True):
        """
        تهيئة محلل المتطلبات
        """
        self.use_ai = use_ai

        # تحميل قاعدة بيانات المتطلبات القياسية
        self.standard_requirements = self._load_standard_requirements()

        # تحميل معايير التقييم
        self.evaluation_criteria = self._load_evaluation_criteria()

        # إنشاء معالج نماذج الذكاء الاصطناعي إذا تم تفعيله
        if self.use_ai:
            self.llm_processor = LLMProcessor()

    def _load_standard_requirements(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        تحميل قاعدة بيانات المتطلبات القياسية
        """
        return {
            "عام": [
                {
                    "id": "G001",
                    "title": "شهادات الاعتماد",
                    "description": "يجب أن يكون المورد/المقاول حاصل على الشهادات والاعتمادات الضرورية للعمل",
                    "importance": "عالية",
                    "category": "إدارية"
                },
                {
                    "id": "G002",
                    "title": "الخبرة السابقة",
                    "description": "يجب أن يكون لدى المورد/المقاول خبرة سابقة في أعمال مماثلة",
                    "importance": "عالية",
                    "category": "فنية"
                }
            ]
        }

    def _load_evaluation_criteria(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل معايير التقييم للمتطلبات
        """
        return {
            "فنية": {
                "weight": 0.6,
                "subcriteria": {
                    "جودة الحلول المقترحة": 0.3,
                    "الخبرة في مشاريع مماثلة": 0.25,
                    "الكوادر الفنية": 0.25,
                    "المنهجية وخطة العمل": 0.2
                }
            },
            "مالية": {
                "weight": 0.3,
                "subcriteria": {
                    "السعر الإجمالي": 0.7,
                    "تفاصيل التكاليف": 0.2,
                    "شروط الدفع": 0.1
                }
            }
        }

    def analyze(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل البيانات المستخرجة وتقييم المتطلبات
        """
        analysis_results = {
            "requirements": [],
            "compliance": {},
            "gaps": [],
            "risks": [],
            "recommendations": [],
            "evaluation": {}
        }

        # استخراج المتطلبات من البيانات المستخرجة
        requirements = extracted_data.get("requirements", [])

        # تحليل الامتثال للمتطلبات القياسية
        compliance_results = self._analyze_compliance(requirements)
        analysis_results["compliance"] = compliance_results

        # تحديد الفجوات في المتطلبات
        gaps = self._identify_gaps(requirements, extracted_data)
        analysis_results["gaps"] = gaps

        # تحليل المخاطر المتعلقة بالمتطلبات
        risks = self._analyze_risks(requirements, extracted_data)
        analysis_results["risks"] = risks

        # إعداد التوصيات
        recommendations = self._generate_recommendations(requirements, compliance_results, gaps, risks, extracted_data)
        analysis_results["recommendations"] = recommendations

        return analysis_results

    def _analyze_compliance(self, requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        تحليل امتثال المتطلبات للمعايير القياسية
        """
        compliance_results = {
            "compliant": [],
            "missing": [],
            "compliance_rate": 0.0
        }

        standard_reqs = self.standard_requirements["عام"]

        for std_req in standard_reqs:
            found = any(std_req["title"].lower() in req.get("title", "").lower() for req in requirements)
            if found:
                compliance_results["compliant"].append(std_req)
            else:
                compliance_results["missing"].append(std_req)

        total_std_reqs = len(standard_reqs)
        if total_std_reqs > 0:
            compliance_results["compliance_rate"] = round(
                len(compliance_results["compliant"]) / total_std_reqs * 100, 2
            )

        return compliance_results

    def _identify_gaps(self, requirements: List[Dict[str, Any]], extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        تحديد الفجوات في المتطلبات
        """
        gaps = []

        for missing_req in self.standard_requirements.get("عام", []):
            if not any(missing_req["title"].lower() in req.get("title", "").lower() for req in requirements):
                gaps.append({
                    "type": "متطلب قياسي مفقود",
                    "requirement": missing_req,
                    "severity": "عالية"
                })

        return gaps

    def _analyze_risks(self, requirements: List[Dict[str, Any]], extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        تحليل المخاطر المتعلقة بالمتطلبات
        """
        risks = []

        # مخاطر وجود متطلبات غامضة
        vague_requirements = [req for req in requirements if len(req.get("description", "")) < 30]
        if vague_requirements:
            risks.append({
                "title": "متطلبات غير واضحة",
                "severity": "عالية",
                "impact": "قد يؤدي إلى نزاعات وتأخير في التنفيذ"
            })

        return risks

    def _generate_recommendations(self, requirements: List[Dict[str, Any]], compliance_results: Dict[str, Any],
                                  gaps: List[Dict[str, Any]], risks: List[Dict[str, Any]],
                                  extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        إعداد توصيات لتحسين المتطلبات
        """
        recommendations = []

        # توصيات لسد الفجوات
        for gap in gaps:
            recommendations.append({
                "title": f"معالجة فجوة: {gap['type']}",
                "priority": "عالية"
            })

        # توصيات لمعالجة المخاطر
        for risk in risks:
            recommendations.append({
                "title": f"معالجة خطر: {risk['title']}",
                "priority": "عالية"
            })

        return recommendations
