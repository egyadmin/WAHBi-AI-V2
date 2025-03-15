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
        for category