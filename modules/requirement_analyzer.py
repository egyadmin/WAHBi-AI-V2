import re
import os
import json
import numpy as np
from typing import Dict, List, Any, Union, Tuple, Optional
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
        
        المعاملات:
        ----------
        use_ai : bool, optional
            استخدام الذكاء الاصطناعي للتحليل المتقدم (افتراضي: True)
        """
        self.use_ai = use_ai
        
        # تحميل قاعدة بيانات المتطلبات القياسية
        self.standard_requirements = self._load_standard_requirements()
        
        # تحميل معايير التقييم
        self.evaluation_criteria = self._load_evaluation_criteria()
        
        # إنشاء معالج نماذج اللغة الكبيرة إذا تم تفعيل استخدام الذكاء الاصطناعي
        if self.use_ai:
            self.llm_processor = LLMProcessor()
    
    def _load_standard_requirements(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        تحميل قاعدة بيانات المتطلبات القياسية
        """
        # في التطبيق الفعلي، قد تُحمل هذه البيانات من ملف أو قاعدة بيانات
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
            ],
            "إنشاءات": [
                {
                    "id": "C001",
                    "title": "تصنيف المقاولين",
                    "description": "يجب أن يكون المقاول مصنف لدى وزارة الشؤون البلدية والقروية والإسكان في المجال والدرجة المطلوبة",
                    "importance": "عالية",
                    "category": "إدارية"
                },
                {
                    "id": "C002",
                    "title": "جودة المواد",
                    "description": "يجب أن تكون جميع المواد المستخدمة مطابقة للمواصفات القياسية السعودية",
                    "importance": "عالية",
                    "category": "فنية"
                }
            ],
            "تقنية معلومات": [
                {
                    "id": "IT001",
                    "title": "شهادة NITCS",
                    "description": "يجب أن يكون المورد حاصل على شهادة المركز الوطني للتصديق الرقمي",
                    "importance": "عالية",
                    "category": "إدارية"
                },
                {
                    "id": "IT002",
                    "title": "متطلبات الأمن السيبراني",
                    "description": "يجب الالتزام بمتطلبات الأمن السيبراني وفق ضوابط الهيئة الوطنية للأمن السيبراني",
                    "importance": "عالية",
                    "category": "فنية"
                }
            ]
        }
    
    def _load_evaluation_criteria(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل معايير التقييم للمتطلبات
        """
        # في التطبيق الفعلي، قد تُحمل هذه البيانات من ملف أو قاعدة بيانات
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
            },
            "المحتوى المحلي": {
                "weight": 0.1,
                "subcriteria": {
                    "نسبة المحتوى المحلي": 0.7,
                    "توظيف الكوادر السعودية": 0.3
                }
            }
        }
    
    def analyze(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل البيانات المستخرجة وتقييم المتطلبات
        
        المعاملات:
        ----------
        extracted_data : Dict[str, Any]
            البيانات المستخرجة من المستند
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المتطلبات
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
        if "requirements" in extracted_data:
            requirements = extracted_data["requirements"]
        else:
            requirements = []
        
        # تصنيف وتنظيم المتطلبات
        categorized_reqs = self._categorize_requirements(requirements)
        analysis_results["categorized_requirements"] = categorized_reqs
        
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
        recommendations = self._generate_recommendations(
            requirements, compliance_results, gaps, risks, extracted_data
        )
        analysis_results["recommendations"] = recommendations
        
        # إعداد تقييم المتطلبات
        if "project_type" in extracted_data:
            project_type = extracted_data["project_type"]
        else:
            project_type = "عام"
            
        evaluation = self._evaluate_requirements(requirements, project_type)
        analysis_results["evaluation"] = evaluation
        
        # استخدام الذكاء الاصطناعي للتحليل المتقدم إذا كان مفعلاً
        if self.use_ai and requirements:
            ai_analysis = self._analyze_with_ai(requirements, extracted_data)
            analysis_results["ai_analysis"] = ai_analysis
        
        # تضمين المتطلبات الكاملة في النتيجة
        analysis_results["requirements"] = requirements
        
        return analysis_results
    
    def _categorize_requirements(self, requirements: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        تصنيف المتطلبات حسب الفئات
        """
        categorized = {}
        
        # تصنيف المتطلبات حسب الفئة
        for req in requirements:
            category = req.get("category", "عامة")
            
            if category not in categorized:
                categorized[category] = []
                
            categorized[category].append(req)
        
        # تصنيف ثانوي حسب الأهمية
        for category in categorized:
            categorized[category] = sorted(
                categorized[category],
                key=lambda x: 0 if x.get("importance", "عادية") == "عالية" else 1
            )
        
        return categorized
    
    def _analyze_compliance(self, requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        تحليل امتثال المتطلبات للمعايير القياسية
        """
        compliance_results = {
            "compliant": [],
            "non_compliant": [],
            "missing": [],
            "compliance_rate": 0.0
        }
        
        # قائمة بالمتطلبات القياسية المهمة للمقارنة
        standard_reqs_flat = []
        for category, reqs in self.standard_requirements.items():
            for req in reqs:
                if req.get("importance", "") == "عالية":
                    standard_reqs_flat.append(req)
        
        # تحليل المتطلبات المستخرجة
        for std_req in standard_reqs_flat:
            found = False
            
            for req in requirements:
                # البحث عن تطابق في العنوان أو الوصف
                title_match = std_req["title"].lower() in req.get("title", "").lower()
                desc_match = std_req["description"].lower() in req.get("description", "").lower()
                
                if title_match or desc_match:
                    found = True
                    compliance_results["compliant"].append({
                        "standard_requirement": std_req,
                        "found_requirement": req
                    })
                    break
            
            if not found:
                compliance_results["missing"].append(std_req)
        
        # حساب نسبة الامتثال
        total_std_reqs = len(standard_reqs_flat)
        if total_std_reqs > 0:
            compliance_rate = len(compliance_results["compliant"]) / total_std_reqs
            compliance_results["compliance_rate"] = round(compliance_rate * 100, 2)
        
        return compliance_results
    
    def _identify_gaps(self, requirements: List[Dict[str, Any]], extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        تحديد الفجوات في المتطلبات
        """
        gaps = []
        
        # تحديد الفجوات بناءً على المتطلبات القياسية المفقودة
        for missing_req in self.standard_requirements.get("عام", []):
            found = False
            
            for req in requirements:
                if missing_req["title"].lower() in req.get("title", "").lower():
                    found = True
                    break
            
            if not found:
                gaps.append({
                    "type": "متطلب قياسي مفقود",
                    "requirement": missing_req,
                    "severity": "عالية" if missing_req.get("importance", "") == "عالية" else "متوسطة",
                    "recommendation": f"إضافة متطلب: {missing_req['title']}"
                })
        
        # تحديد الفجوات في المحتوى المحلي
        if "local_content" in extracted_data:
            local_content = extracted_data["local_content"]
            
            # التحقق من وجود متطلبات المحتوى المحلي
            local_content_req_found = False
            
            for req in requirements:
                if "محتوى محلي" in req.get("title", "").lower() or "محتوى محلي" in req.get("description", "").lower():
                    local_content_req_found = True
                    break
            
            if not local_content_req_found:
                gaps.append({
                    "type": "متطلب محتوى محلي مفقود",
                    "severity": "عالية",
                    "recommendation": "إضافة متطلبات محددة للمحتوى المحلي ونسبة التوطين المطلوبة"
                })
        
        # تحديد الفجوات في تحديد المسؤوليات
        responsibilities_found = False
        for req in requirements:
            if "مسؤولية" in req.get("title", "").lower() or "مسؤولية" in req.get("description", "").lower():
                responsibilities_found = True
                break
        
        if not responsibilities_found:
            gaps.append({
                "type": "تحديد المسؤوليات",
                "severity": "متوسطة",
                "recommendation": "إضافة قسم يحدد مسؤوليات الأطراف بوضوح"
            })
        
        # تحديد الفجوات في آلية فض النزاعات
        dispute_resolution_found = False
        for req in requirements:
            if "نزاع" in req.get("title", "").lower() or "نزاع" in req.get("description", "").lower():
                dispute_resolution_found = True
                break
        
        if not dispute_resolution_found:
            gaps.append({
                "type": "آلية فض النزاعات",
                "severity": "متوسطة",
                "recommendation": "إضافة قسم يوضح آلية فض النزاعات بين الأطراف"
            })
        
        return gaps
    
    def _analyze_risks(self, requirements: List[Dict[str, Any]], extracted_data: Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        تحليل المخاطر المتعلقة بالمتطلبات
        """
        risks = []
        
        # تحليل مخاطر الامتثال للمتطلبات
        vague_requirements = []
        for req in requirements:
            # تحديد المتطلبات الغامضة
            if len(req.get("description", "")) < 30:
                vague_requirements.append(req)
        
        if vague_requirements:
            risks.append({
                "title": "متطلبات غامضة",
                "description": f"تم العثور على {len(vague_requirements)} متطلبات غير محددة بوضوح",
                "severity": "عالية",
                "probability": "عالية",
                "impact": "قد يؤدي إلى نزاعات وتأخير في تنفيذ المشروع",
                "mitigation": "توضيح المتطلبات الغامضة وتحديدها بشكل أكثر دقة"
            })
        
        # تحليل مخاطر المحتوى المحلي
        if "local_content" in extracted_data:
            local_content = extracted_data["local_content"]
            
            # التحقق من وجود نسب محددة للمحتوى المحلي
            local_content_percentage_found = False
            for percentage in local_content.get("percentages", []):
                local_content_percentage_found = True
                break
            
            if not local_content_percentage_found:
                risks.append({
                    "title": "عدم تحديد نسبة المحتوى المحلي",
                    "description": "لم يتم تحديد نسبة واضحة للمحتوى المحلي المطلوب",
                    "severity": "متوسطة",
                    "probability": "عالية",
                    "impact": "قد يؤدي إلى عدم الامتثال لمتطلبات المحتوى المحلي والتعرض للغرامات",
                    "mitigation": "تحديد نسبة المحتوى المحلي المطلوبة بوضوح وآلية التحقق منها"
                })
        
        # تحليل مخاطر الجدول الزمني
        if "dates" in extracted_data:
            dates = extracted_data["dates"]
            
            if len(dates) < 2:
                risks.append({
                    "title": "عدم وضوح الجدول الزمني",
                    "description": "لم يتم تحديد جدول زمني واضح للمشروع",
                    "severity": "عالية",
                    "probability": "متوسطة",
                    "impact": "تأخير في تنفيذ المشروع وصعوبة في متابعة التقدم",
                    "mitigation": "تحديد جدول زمني تفصيلي مع مراحل ومعالم واضحة"
                })
        
        # تحليل مخاطر سلسلة الإمداد
        if "supply_chain" in extracted_data:
            supply_chain = extracted_data["supply_chain"]
            
            if len(supply_chain.get("suppliers", [])) < 2:
                risks.append({
                    "title": "مخاطر سلسلة الإمداد",
                    "description": "لم يتم تحديد موردين بدلاء أو خطة لإدارة مخاطر سلسلة الإمداد",
                    "severity": "عالية",
                    "probability": "متوسطة",
                    "impact": "تأخير في توريد المواد والمعدات المطلوبة",
                    "mitigation": "تحديد موردين بدلاء وخطة لإدارة مخاطر سلسلة الإمداد"
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
                "description": gap.get("recommendation", ""),
                "priority": "عالية" if gap.get("severity", "") == "عالية" else "متوسطة",
                "benefits": "تحسين جودة المتطلبات وتقليل مخاطر النزاعات"
            })
        
        # توصيات للتخفيف من المخاطر
        for risk in risks:
            recommendations.append({
                "title": f"معالجة خطر: {risk['title']}",
                "description": risk.get("mitigation", ""),
                "priority": "عالية" if risk.get("severity", "") == "عالية" else "متوسطة",
                "benefits": "تقليل المخاطر وتحسين فرص نجاح المشروع"
            })
        
        # توصيات لتحسين المحتوى المحلي
        local_content_recommendation = {
            "title": "تحسين متطلبات المحتوى المحلي",
            "description": "تحديد نسبة المحتوى المحلي المطلوبة بوضوح، وتوضيح آلية التحقق والقياس، وتحديد متطلبات توطين الوظائف",
            "priority": "عالية",
            "benefits": "الامتثال لمتطلبات المحتوى المحلي وتحقيق أهداف رؤية 2030",
            "implementation": [
                "تحديد نسبة المحتوى المحلي المطلوبة بدقة",
                "توضيح آلية حساب وقياس نسبة المحتوى المحلي",
                "تحديد متطلبات توظيف الكوادر السعودية",
                "تحديد آلية التحقق من الامتثال لمتطلبات المحتوى المحلي"
            ]
        }
        recommendations.append(local_content_recommendation)
        
        # توصيات لتحسين متطلبات سلسلة الإمداد
        supply_chain_recommendation = {
            "title": "تحسين متطلبات سلسلة الإمداد",
            "description": "تطوير خطة شاملة لإدارة سلسلة الإمداد وتحديد المصادر البديلة",
            "priority": "متوسطة",
            "benefits": "تقليل مخاطر انقطاع سلسلة الإمداد وضمان استمرارية المشروع",
            "implementation": [
                "تحديد الموردين الرئيسيين والبدلاء",
                "وضع خطة للتعامل مع انقطاع سلسلة الإمداد",
                "تحديد المواد والمعدات الحرجة والمصادر البديلة",
                "تطوير إجراءات لمتابعة وتقييم أداء الموردين"
            ]
        }
        recommendations.append(supply_chain_recommendation)
        
        return recommendations
    
    def _evaluate_requirements(self, requirements: List[Dict[str, Any]], project_type: str) -> Dict[str, Any]:
        """
        تقييم المتطلبات وفق معايير التقييم
        """
        evaluation = {
            "scores": {},
            "overall_score": 0.0,
            "comments": []
        }
        
        # تقييم المتطلبات الفنية
        technical_score = self._evaluate_technical_requirements(requirements)
        evaluation["scores"]["فنية"] = technical_score
        
        # تقييم المتطلبات المالية
        financial_score = self._evaluate_financial_requirements(requirements)
        evaluation["scores"]["مالية"] = financial_score
        
        # تقييم متطلبات المحتوى المحلي
        local_content_score = self._evaluate_local_content_requirements(requirements)
        evaluation["scores"]["المحتوى المحلي"] = local_content_score
        
        # حساب التقييم الإجمالي
        weights = {
            "فنية": self.evaluation_criteria["فنية"]["weight"],
            "مالية": self.evaluation_criteria["مالية"]["weight"],
            "المحتوى المحلي": self.evaluation_criteria["المحتوى المحلي"]["weight"]
        }
        
        overall_score = (
            technical_score * weights["فنية"] +
            financial_score * weights["مالية"] +
            local_content_score * weights["المحتوى المحلي"]
        )
        
        evaluation["overall_score"] = round(overall_score, 2)
        
        # إضافة تعليقات
        if overall_score >= 0.8:
            evaluation["comments"].append("المتطلبات شاملة وتغطي جميع الجوانب الرئيسية")
        elif overall_score >= 0.6:
            evaluation["comments"].append("المتطلبات جيدة ولكنها تحتاج إلى بعض التحسينات")
        else:
            evaluation["comments"].append("المتطلبات غير كافية وتحتاج إلى مراجعة شاملة")
        
        if technical_score < 0.6:
            evaluation["comments"].append("المتطلبات الفنية غير كافية وغير واضحة")
        
        if financial_score < 0.6:
            evaluation["comments"].append("المتطلبات المالية غير محددة بوضوح")
        
        if local_content_score < 0.6:
            evaluation["comments"].append("متطلبات المحتوى المحلي غير كافية وتحتاج إلى تحسين")
        
        return evaluation
    
    def _evaluate_technical_requirements(self, requirements: List[Dict[str, Any]]) -> float:
        """
        تقييم المتطلبات الفنية
        """
        # عدد المتطلبات الفنية
        technical_reqs = [req for req in requirements if req.get("category", "") == "فنية"]
        
        if not technical_reqs:
            return 0.0
        
        # تقييم وضوح المتطلبات
        clarity_score = sum(1 for req in technical_reqs if len(req.get("description", "")) > 50) / max(1, len(technical_reqs))
        
        # تقييم اكتمال المتطلبات
        completeness_score = min(1.0, len(technical_reqs) / 10)  # افتراض أن 10 متطلبات تقنية هي الحد الأعلى المثالي
        
        # تقييم تحديد المسؤوليات
        responsibility_score = sum(1 for req in technical_reqs if "مسؤولية" in req.get("description", "").lower()) / max(1, len(technical_reqs))
        
        # حساب النتيجة الإجمالية
        total_score = (clarity_score * 0.4) + (completeness_score * 0.4) + (responsibility_score * 0.2)
        
        return round(total_score, 2)
    
    def _evaluate_financial_requirements(self, requirements: List[Dict[str, Any]]) -> float:
        """
        تقييم المتطلبات المالية
        """
        # عدد المتطلبات المالية
        financial_reqs = [req for req in requirements if req.get("category", "") == "مالية"]
        
        if not financial_reqs:
            return 0.0
        
        # تقييم وضوح المتطلبات
        clarity_score = sum(1 for req in financial_reqs if len(req.get("description", "")) > 50) / max(1, len(financial_reqs))
        
        # تقييم اكتمال المتطلبات
        completeness_score = min(1.0, len(financial_reqs) / 5)  # افتراض أن 5 متطلبات مالية هي الحد الأعلى المثالي
        
        # تقييم تحديد شروط الدفع
        payment_score = sum(1 for req in financial_reqs if "دفع" in req.get("description", "").lower()) / max(1, len(financial_reqs))
        
        # حساب النتيجة الإجمالية
        total_score = (clarity_score * 0.3) + (completeness_score * 0.3) + (payment_score * 0.4)
        
        return round(total_score, 2)
    
    def _evaluate_local_content_requirements(self, requirements: List[Dict[str, Any]]) -> float:
        """
        تقييم متطلبات المحتوى المحلي
        """
        # عدد متطلبات المحتوى المحلي
        local_content_reqs = []
        for req in requirements:
            if req.get("category", "") == "محتوى محلي":
                local_content_reqs.append(req)
            elif "محتوى محلي" in req.get("title", "").lower() or "محتوى محلي" in req.get("description", "").lower():
                local_content_reqs.append(req)
        
        if not local_content_reqs:
            return 0.0
        
        # تقييم وضوح المتطلبات
        clarity_score = sum(1 for req in local_content_reqs if len(req.get("description", "")) > 50) / max(1, len(local_content_reqs))
        
        # تقييم تحديد النسب المطلوبة
        percentage_score = sum(1 for req in local_content_reqs if "%" in req.get("description", "")) / max(1, len(local_content_reqs))
        
        # تقييم آلية التحقق
        verification_score = sum(1 for req in local_content_reqs if "تحقق" in req.get("description", "").lower() or "قياس" in req.get("description", "").lower()) / max(1, len(local_content_reqs))
        
        # حساب النتيجة الإجمالية
        total_score = (clarity_score * 0.2) + (percentage_score * 0.5) + (verification_score * 0.3)
        
        return round(total_score, 2)
    
    def _analyze_with_ai(self, requirements: List[Dict[str, Any]], extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        استخدام الذكاء الاصطناعي لتحليل المتطلبات بشكل متقدم
        """
        ai_analysis = {
            "summary": "",
            "insights": [],
            "recommendations": []
        }
        
        try:
            # إعداد سياق للتحليل
            context = {
                "requirements_count": len(requirements),
                "categories": list(set(req.get("category", "عامة") for req in requirements)),
                "has_local_content": any("محتوى محلي" in req.get("category", "") for req in requirements),
                "text_samples": [req.get("description", "")[:200] for req in requirements[:5]]
            }
            
            # استخدام نموذج LLM لتحليل المتطلبات
            # في التطبيق الفعلي، هذا سيستدعي واجهة برمجة تطبيقات مثل Claude أو OpenAI
            ai_response = self.llm_processor.analyze_requirements(requirements, context)
            
            # معالجة استجابة الذكاء الاصطناعي
            if isinstance(ai_response, dict):
                ai_analysis.update(ai_response)
            
        except Exception as e:
            ai_analysis["error"] = f"حدث خطأ أثناء تحليل المتطلبات باستخدام الذكاء الاصطناعي: {str(e)}"
        
        return ai_analysis