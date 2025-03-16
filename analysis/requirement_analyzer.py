# إذا كانت الجملة الأولى طويلة، اختصرها
        if len(first_sentence) > 50:
            if ":" in first_sentence:
                # استخدام النص قبل العلامة : كعنوان
                title = first_sentence.split(":")[0].strip()
            else:
                # اختصار الجملة الأولى
                words = first_sentence.split()
                title = " ".join(words[:7]) + "..."
        else:
            title = first_sentence
        
        return title
    
    def _categorize_requirements(self, requirements: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        تصنيف المتطلبات إلى فئات
        
        المعاملات:
        ----------
        requirements : List[Dict[str, Any]]
            قائمة المتطلبات
            
        المخرجات:
        --------
        Dict[str, List[Dict[str, Any]]]
            المتطلبات مصنفة حسب الفئة
        """
        categorized = {
            "technical": [],
            "financial": [],
            "legal": []
        }
        
        for req in requirements:
            description = req.get("description", "").lower()
            title = req.get("title", "").lower()
            text = title + " " + description
            
            # تحديد الفئة بناءً على الكلمات المفتاحية
            if any(keyword in text for keyword in ["فني", "تقني", "هندسي", "مواصفات", "جودة", "معايير", "أداء", "تصميم", "مخطط"]):
                req["category"] = "technical"
                categorized["technical"].append(req)
            elif any(keyword in text for keyword in ["مالي", "سعر", "تكلفة", "دفع", "ضمان", "تأمين", "غرامة", "ميزانية", "ضريبة", "محاسبة"]):
                req["category"] = "financial"
                categorized["financial"].append(req)
            elif any(keyword in text for keyword in ["قانوني", "شرط", "عقد", "التزام", "تعاقد", "نظام", "لائحة", "تشريع", "ترخيص", "حقوق"]):
                req["category"] = "legal"
                categorized["legal"].append(req)
            else:
                # إذا لم يتطابق مع أي فئة، افترض أنه متطلب فني
                req["category"] = "technical"
                categorized["technical"].append(req)
        
        return categorized
    
    def _analyze_importance_difficulty(self, categorized_requirements: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        تحليل أهمية وصعوبة المتطلبات
        
        المعاملات:
        ----------
        categorized_requirements : Dict[str, List[Dict[str, Any]]]
            المتطلبات مصنفة حسب الفئة
            
        المخرجات:
        --------
        Dict[str, List[Dict[str, Any]]]
            المتطلبات بعد تحليل الأهمية والصعوبة
        """
        analyzed = {}
        
        for category, reqs in categorized_requirements.items():
            analyzed_reqs = []
            
            for req in reqs:
                # تحليل الأهمية
                req["importance"] = self._determine_importance(req)
                
                # تحليل صعوبة التنفيذ
                req["difficulty"] = self._determine_difficulty(req)
                
                # تحديد الفجوات
                req["gaps"] = self._identify_gaps(req)
                
                # اقتراح تحسينات
                req["improvements"] = self._suggest_improvements(req)
                
                analyzed_reqs.append(req)
            
            analyzed[category] = analyzed_reqs
        
        return analyzed
    
    def _determine_importance(self, requirement: Dict[str, Any]) -> str:
        """
        تحديد أهمية المتطلب
        
        المعاملات:
        ----------
        requirement : Dict[str, Any]
            المتطلب
            
        المخرجات:
        --------
        str
            درجة الأهمية
        """
        text = requirement.get("description", "").lower()
        
        # البحث عن كلمات تدل على الإلزامية
        if any(keyword in text for keyword in ["يجب", "إلزامي", "ضروري", "لا بد", "لابد", "مطلوب", "يلتزم", "ملزم"]):
            return "إلزامي"
        
        # البحث عن كلمات تدل على الأهمية الثانوية
        elif any(keyword in text for keyword in ["يفضل", "مرغوب", "محبذ", "يحبذ", "يستحسن"]):
            return "ثانوي"
        
        # إذا لم يتطابق مع أي حالة، افترض أنه متطلب عادي
        else:
            return "عادي"
    
    def _determine_difficulty(self, requirement: Dict[str, Any]) -> int:
        """
        تحديد صعوبة تنفيذ المتطلب
        
        المعاملات:
        ----------
        requirement : Dict[str, Any]
            المتطلب
            
        المخرجات:
        --------
        int
            درجة الصعوبة (1-5)
        """
        text = requirement.get("description", "").lower()
        category = requirement.get("category", "")
        importance = requirement.get("importance", "")
        
        # تعيين درجة صعوبة أساسية
        base_difficulty = 3  # متوسط
        
        # زيادة الصعوبة للمتطلبات الإلزامية
        if importance == "إلزامي":
            base_difficulty += 1
        
        # زيادة الصعوبة بناءً على طول النص
        if len(text) > 200:
            base_difficulty += 0.5
        
        # زيادة الصعوبة بناءً على الكلمات المفتاحية
        if any(keyword in text for keyword in ["معقد", "صعب", "متقدم", "عالي", "متطور", "خبير", "مخصص", "خاص"]):
            base_difficulty += 1
        
        # تخفيض الصعوبة للمتطلبات البسيطة
        if any(keyword in text for keyword in ["بسيط", "سهل", "عادي", "أساسي", "تقليدي"]):
            base_difficulty -= 1
        
        # ضبط الصعوبة في النطاق 1-5
        return max(1, min(5, round(base_difficulty)))
    
    def _identify_gaps(self, requirement: Dict[str, Any]) -> str:
        """
        تحديد الفجوات في المتطلب
        
        المعاملات:
        ----------
        requirement : Dict[str, Any]
            المتطلب
            
        المخرجات:
        --------
        str
            الفجوات المحددة
        """
        text = requirement.get("description", "")
        
        gaps = []
        
        # التحقق من وضوح المتطلب
        if len(text) < 50:
            gaps.append("وصف قصير وغير مفصل")
        
        # التحقق من وجود معايير قياس
        if not any(keyword in text.lower() for keyword in ["معيار", "قياس", "مؤشر", "مستوى", "نسبة", "كمية", "عدد"]):
            gaps.append("لا يحتوي على معايير قياس واضحة")
        
        # التحقق من وجود توصيف زمني
        if not any(keyword in text.lower() for keyword in ["مدة", "فترة", "خلال", "زمن", "تاريخ", "موعد", "يوم", "أسبوع", "شهر"]):
            gaps.append("لا يحدد إطار زمني")
        
        # التحقق من وجود مسؤولية تنفيذ
        if not any(keyword in text.lower() for keyword in ["مسؤول", "مسؤولية", "مقاول", "مورد", "مقدم", "طرف", "مكلف"]):
            gaps.append("لا يحدد المسؤولية عن التنفيذ")
        
        # إرجاع الفجوات
        if gaps:
            return "، ".join(gaps)
        else:
            return "لا توجد فجوات واضحة"
    
    def _suggest_improvements(self, requirement: Dict[str, Any]) -> str:
        """
        اقتراح تحسينات للمتطلب
        
        المعاملات:
        ----------
        requirement : Dict[str, Any]
            المتطلب
            
        المخرجات:
        --------
        str
            التحسينات المقترحة
        """
        gaps = requirement.get("gaps", "")
        category = requirement.get("category", "")
        
        improvements = []
        
        # اقتراح تحسينات بناءً على الفجوات
        if "وصف قصير" in gaps:
            improvements.append("توضيح المتطلب بشكل أكثر تفصيلاً")
        
        if "معايير قياس" in gaps:
            improvements.append("إضافة معايير قياس كمية ونوعية")
        
        if "إطار زمني" in gaps:
            improvements.append("تحديد إطار زمني واضح للتنفيذ")
        
        if "المسؤولية" in gaps:
            improvements.append("تحديد المسؤولية عن التنفيذ بوضوح")
        
        # اقتراح تحسينات بناءً على الفئة
        if category == "technical":
            if not improvements:
                improvements.append("إضافة مراجع للمعايير الفنية والمواصفات")
        elif category == "financial":
            if not improvements:
                improvements.append("توضيح آلية الدفع والتسعير")
        elif category == "legal":
            if not improvements:
                improvements.append("إضافة المرجعية القانونية والتنظيمية")
        
        # إرجاع التحسينات
        if improvements:
            return "، ".join(improvements)
        else:
            return "المتطلب واضح ومكتمل"
    
    def _extract_local_content_requirements(self, text: str) -> List[Dict[str, Any]]:
        """
        استخراج متطلبات المحتوى المحلي
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة متطلبات المحتوى المحلي
        """
        # الكلمات المفتاحية للمحتوى المحلي
        local_content_keywords = [
            "المحتوى المحلي", "التوطين", "السعودة", "المنتجات المحلية", 
            "الصناعة المحلية", "نسبة المحتوى", "المكون المحلي", "منشأ محلي",
            "نطاقات", "توظيف السعوديين", "توظيف المواطنين", "القيمة المضافة المحلية"
        ]
        
        local_content_requirements = []
        
        # البحث عن أقسام المحتوى المحلي
        for keyword in local_content_keywords:
            pattern = rf"((?:{keyword}|{keyword.upper()}).*?(?:\n\n|\Z))"
            matches = re.finditer(pattern, text, re.DOTALL)
            
            for match in matches:
                section_text = match.group(1).strip()
                
                # استخراج النسب المئوية
                percentage_matches = re.findall(r'(\d+(?:\.\d+)?)(?:\s*%|\s*في المائة|\s*بالمائة)', section_text)
                
                if percentage_matches:
                    for percentage in percentage_matches:
                        requirement = {
                            "title": f"متطلب المحتوى المحلي - {percentage}%",
                            "description": section_text,
                            "category": "local_content",
                            "importance": "إلزامي",
                            "percentage": float(percentage),
                            "difficulty": 4,  # افتراضي: صعوبة عالية
                            "gaps": self._identify_gaps({"description": section_text}),
                            "improvements": "توضيح آلية حساب وتوثيق نسبة المحتوى المحلي"
                        }
                        local_content_requirements.append(requirement)
                else:
                    # إذا لم يتم العثور على نسب، أضف المتطلب بدون نسبة
                    requirement = {
                        "title": "متطلب المحتوى المحلي",
                        "description": section_text,
                        "category": "local_content",
                        "importance": "إلزامي",
                        "difficulty": 3,  # افتراضي: صعوبة متوسطة
                        "gaps": "لا يحدد نسبة محتوى محلي واضحة",
                        "improvements": "تحديد نسبة المحتوى المحلي المطلوبة بشكل صريح"
                    }
                    local_content_requirements.append(requirement)
        
        # إزالة التكرارات
        unique_requirements = []
        descriptions = set()
        
        for req in local_content_requirements:
            desc = req["description"]
            if desc not in descriptions:
                descriptions.add(desc)
                unique_requirements.append(req)
        
        return unique_requirements
    
    def _generate_requirements_summary(self, categorized_requirements: Dict[str, List[Dict[str, Any]]],
                                     local_content_requirements: List[Dict[str, Any]],
                                     total_count: int, mandatory_count: int, avg_difficulty: float) -> str:
        """
        إعداد ملخص المتطلبات
        
        المعاملات:
        ----------
        categorized_requirements : Dict[str, List[Dict[str, Any]]]
            المتطلبات مصنفة حسب الفئة
        local_content_requirements : List[Dict[str, Any]]
            متطلبات المحتوى المحلي
        total_count : int
            إجمالي عدد المتطلبات
        mandatory_count : int
            عدد المتطلبات الإلزامية
        avg_difficulty : float
            متوسط صعوبة التنفيذ
            
        المخرجات:
        --------
        str
            ملخص المتطلبات
        """
        # إعداد الملخص
        summary = f"تم تحليل {total_count} متطلب، منها {mandatory_count} متطلب إلزامي. "
        
        # توزيع المتطلبات حسب الفئة
        tech_count = len(categorized_requirements.get("technical", []))
        fin_count = len(categorized_requirements.get("financial", []))
        legal_count = len(categorized_requirements.get("legal", []))
        local_count = len(local_content_requirements)
        
        summary += f"تتوزع المتطلبات إلى {tech_count} متطلب فني، و{fin_count} متطلب مالي، و{legal_count} متطلب قانوني، و{local_count} متطلب للمحتوى المحلي. "
        
        # صعوبة التنفيذ
        if avg_difficulty >= 4:
            summary += "متوسط صعوبة تنفيذ المتطلبات مرتفع، مما يشير إلى تعقيد المشروع. "
        elif avg_difficulty >= 3:
            summary += "متوسط صعوبة تنفيذ المتطلبات متوسط. "
        else:
            summary += "متوسط صعوبة تنفيذ المتطلبات منخفض، مما يشير إلى إمكانية تنفيذ المشروع بسهولة نسبية. "
        
        # متطلبات المحتوى المحلي
        if local_count > 0:
            local_percentages = [req.get("percentage", 0) for req in local_content_requirements if "percentage" in req]
            if local_percentages:
                max_percentage = max(local_percentages)
                summary += f"يتطلب المشروع تحقيق نسبة محتوى محلي لا تقل عن {max_percentage}%. "
            else:
                summary += "يتضمن المشروع متطلبات للمحتوى المحلي، لكن النسبة المطلوبة غير محددة بوضوح. "
        else:
            summary += "لم يتم تحديد متطلبات واضحة للمحتوى المحلي. "
        
        # تقييم عام
        if mandatory_count / total_count > 0.7:
            summary += "نسبة المتطلبات الإلزامية مرتفعة، مما يشير إلى تشدد في شروط المناقصة. "
        
        if avg_difficulty > 3.5 and mandatory_count / total_count > 0.6:
            summary += "يجب الانتباه إلى ارتفاع صعوبة التنفيذ ونسبة المتطلبات الإلزامية، مما قد يزيد من مخاطر المشروع."
        
        return summary
    
    def _generate_template_requirements(self) -> List[Dict[str, Any]]:
        """
        إنشاء متطلبات افتراضية من القوالب
        
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة المتطلبات الافتراضية
        """
        # إنشاء نسخة من قوالب المتطلبات
        requirements = []
        
        # إضافة متطلبات من كل فئة
        for category, templates in self.requirement_templates.items():
            for template in templates:
                requirement = template.copy()
                requirement["category"] = category
                requirements.append(requirement)
        
        return requirements
    
    def _clean_requirements(self, requirements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        تنظيف وتوحيد المتطلبات
        
        المعاملات:
        ----------
        requirements : List[Dict[str, Any]]
            قائمة المتطلبات
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة المتطلبات المنظفة
        """
        cleaned = []
        descriptions = set()
        
        for req in requirements:
            # تنظيف الوصف
            if "description" in req:
                req["description"] = req["description"].strip()
            
            # تجاهل المتطلبات المكررة
            if req.get("description", "") in descriptions:
                continue
            
            # إضافة الوصف إلى مجموعة الأوصاف
            descriptions.add(req.get("description", ""))
            
            # التأكد من وجود عنوان
            if "title" not in req or not req["title"]:
                req["title"] = self._extract_requirement_title(req.get("description", ""))
            
            # إضافة المتطلب إلى القائمة المنظفة
            cleaned.append(req)
        
        return cleaned
    
    def _load_requirement_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        تحميل قوالب المتطلبات
        
        المخرجات:
        --------
        Dict[str, List[Dict[str, Any]]]
            قوالب المتطلبات
        """
        try:
            file_path = 'data/templates/requirement_templates.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"ملف قوالب المتطلبات غير موجود: {file_path}")
                # إنشاء قوالب افتراضية
                return self._create_default_requirement_templates()
        except Exception as e:
            logger.error(f"فشل في تحميل قوالب المتطلبات: {str(e)}")
            return self._create_default_requirement_templates()
    
    def _create_default_requirement_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        إنشاء قوالب متطلبات افتراضية
        
        المخرجات:
        --------
        Dict[str, List[Dict[str, Any]]]
            قوالب المتطلبات الافتراضية
        """
        templates = {
            "technical": [
                {
                    "title": "مؤهلات وخبرات الفريق الفني",
                    "description": "يجب توفير فريق فني مؤهل ذو خبرة لا تقل عن 5 سنوات في مجال المشروع، مع تقديم السير الذاتية للمهندسين الرئيسيين.",
                    "importance": "إلزامي",
                    "difficulty": 3
                },
                {
                    "title": "جودة المواد والمعدات",
                    "description": "يجب استخدام مواد ومعدات ذات جودة عالية ومطابقة للمواصفات القياسية السعودية والعالمية، مع تقديم شهادات الجودة والمنشأ.",
                    "importance": "إلزامي",
                    "difficulty": 4
                },
                {
                    "title": "خطة العمل والجدول الزمني",
                    "description": "تقديم خطة عمل تفصيلية وجدول زمني لتنفيذ المشروع، موضحاً المراحل الرئيسية والمدد الزمنية لكل مرحلة.",
                    "importance": "إلزامي",
                    "difficulty": 3
                },
                {
                    "title": "ضمان الأعمال",
                    "description": "تقديم ضمان للأعمال المنفذة لمدة لا تقل عن سنة من تاريخ الاستلام النهائي، مع الالتزام بإصلاح أي عيوب خلال فترة الضمان.",
                    "importance": "إلزامي",
                    "difficulty": 2
                },
                {
                    "title": "الصيانة الدورية",
                    "description": "يفضل تقديم برنامج للصيانة الدورية بعد انتهاء فترة الضمان، مع تحديد التكاليف والخدمات المشمولة.",
                    "importance": "ثانوي",
                    "difficulty": 2
                }
            ],
            "financial": [
                {
                    "title": "العرض المالي",
                    "description": "تقديم عرض مالي مفصل يوضح تكاليف كل بند من بنود المشروع، مع بيان القيمة الإجمالية شاملة ضريبة القيمة المضافة.",
                    "importance": "إلزامي",
                    "difficulty": 3
                },
                {
                    "title": "الضمان الابتدائي",
                    "description": "تقديم ضمان ابتدائي بنسبة 2% من قيمة العرض، ساري المفعول لمدة 90 يوماً من تاريخ فتح المظاريف.",
                    "importance": "إلزامي",
                    "difficulty": 2
                },
                {
                    "title": "الضمان النهائي",
                    "description": "تقديم ضمان نهائي بنسبة 5% من قيمة العقد عند الترسية، ساري المفعول حتى انتهاء فترة الضمان.",
                    "importance": "إلزامي",
                    "difficulty": 2
                },
                {
                    "title": "شروط الدفع",
                    "description": "يتم الدفع على دفعات مرحلية حسب نسب الإنجاز، مع احتجاز نسبة 10% من كل دفعة كضمان حسن التنفيذ.",
                    "importance": "إلزامي",
                    "difficulty": 2
                },
                {
                    "title": "غرامات التأخير",
                    "description": "تفرض غرامة تأخير بنسبة 1% من قيمة العقد عن كل أسبوع تأخير، بحد أقصى 10% من القيمة الإجمالية للعقد.",
                    "importance": "إلزامي",
                    "difficulty": 3
                }
            ],
            "legal": [
                {
                    "title": "السجل التجاري",
                    "description": "يجب أن يكون المتقدم حاصلاً على سجل تجاري ساري المفعول في نفس مجال المناقصة.",
                    "importance": "إلزامي",
                    "difficulty": 1
                },
                {
                    "title": "تصنيف المقاولين",
                    "description": "يجب أن يكون المقاول مصنفاً لدى وزارة الشؤون البلدية والقروية والإسكان في المجال المطلوب وبدرجة لا تقل عن الثالثة.",
                    "importance": "إلزامي",
                    "difficulty": 2
                },
                {
                    "title": "التأمينات",
                    "description": "تقديم شهادة من المؤسسة العامة للتأمينات الاجتماعية تثبت الوفاء بالالتزامات تجاه المؤسسة.",
                    "importance": "إلزامي",
                    "difficulty": 1
                },
                {
                    "title": "الزكاة والدخل",
                    "description": "تقديم شهادة من هيئة الزكاة والضريبة والجمارك تثبت سداد المستحقات.",
                    "importance": "إلزامي",
                    "difficulty": 1
                },
                {
                    "title": "نظام المنافسات والمشتريات",
                    "description": "الالتزام بأحكام نظام المنافسات والمشتريات الحكومية ولائحته التنفيذية.",
                    "importance": "إلزامي",
                    "difficulty": 2
                }
            ]
        }
        
        return templates"""
محلل متطلبات المناقصات
يقوم باستخراج وتحليل وتصنيف متطلبات المناقصات
"""

import re
import logging
import json
import os
from typing import Dict, List, Any, Tuple, Optional, Union
import numpy as np

logger = logging.getLogger(__name__)

class RequirementAnalyzer:
    """
    محلل متطلبات المناقصات
    """
    
    def __init__(self, model_loader, arabic_nlp, config=None):
        """
        تهيئة محلل المتطلبات
        
        المعاملات:
        ----------
        model_loader : ModelLoader
            محمّل النماذج المستخدمة للتحليل
        arabic_nlp : ArabicNLP
            أدوات معالجة اللغة العربية
        config : Dict, optional
            إعدادات المحلل
        """
        self.config = config or {}
        self.model_loader = model_loader
        self.arabic_nlp = arabic_nlp
        
        # تحميل النماذج
        self.ner_model = None
        if hasattr(model_loader, 'get_ner_model'):
            try:
                self.ner_model = model_loader.get_ner_model()
                logger.info("تم تحميل نموذج التعرف على الكيانات المسماة")
            except Exception as e:
                logger.warning(f"فشل في تحميل نموذج التعرف على الكيانات المسماة: {str(e)}")
        
        # تحميل قوالب المتطلبات
        self.requirement_templates = self._load_requirement_templates()
        
        logger.info("تم تهيئة محلل المتطلبات")
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        تحليل متطلبات المناقصة من النص
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المتطلبات
        """
        try:
            logger.info("بدء تحليل متطلبات المناقصة")
            
            # استخراج المتطلبات من النص
            requirements = self._extract_requirements(text)
            
            # تصنيف المتطلبات
            categorized_requirements = self._categorize_requirements(requirements)
            
            # تحليل الأهمية والصعوبة
            analyzed_requirements = self._analyze_importance_difficulty(categorized_requirements)
            
            # تحليل متطلبات المحتوى المحلي
            local_content_requirements = self._extract_local_content_requirements(text)
            
            # تحديد عدد المتطلبات الإلزامية
            mandatory_count = sum(1 for req in requirements if req.get("importance", "") == "إلزامي")
            
            # حساب متوسط صعوبة التنفيذ
            difficulty_values = [req.get("difficulty", 3) for req in requirements if req.get("difficulty", 0) > 0]
            avg_difficulty = np.mean(difficulty_values) if difficulty_values else 3.0
            
            # حساب نسبة متطلبات المحتوى المحلي
            total_count = len(requirements)
            local_content_percentage = (len(local_content_requirements) / total_count * 100) if total_count > 0 else 0
            
            # إعداد ملخص المتطلبات
            summary = self._generate_requirements_summary(
                analyzed_requirements, local_content_requirements, total_count, mandatory_count, avg_difficulty
            )
            
            # إعداد النتائج
            results = {
                "summary": summary,
                "technical": analyzed_requirements.get("technical", []),
                "financial": analyzed_requirements.get("financial", []),
                "legal": analyzed_requirements.get("legal", []),
                "local_content": local_content_requirements,
                "total_count": total_count,
                "mandatory_count": mandatory_count,
                "avg_difficulty": avg_difficulty,
                "local_content_percentage": local_content_percentage
            }
            
            logger.info(f"اكتمل تحليل المتطلبات: {total_count} متطلبات، {mandatory_count} إلزامية")
            return results
            
        except Exception as e:
            logger.error(f"فشل في تحليل المتطلبات: {str(e)}")
            return {
                "summary": "حدث خطأ أثناء تحليل المتطلبات",
                "technical": [],
                "financial": [],
                "legal": [],
                "local_content": [],
                "total_count": 0,
                "mandatory_count": 0,
                "avg_difficulty": 0,
                "local_content_percentage": 0,
                "error": str(e)
            }
    
    def _extract_requirements(self, text: str) -> List[Dict[str, Any]]:
        """
        استخراج المتطلبات من النص
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة المتطلبات المستخرجة
        """
        requirements = []
        
        # البحث عن قسم المتطلبات أو الشروط
        requirement_sections = self._find_requirement_sections(text)
        
        # إذا لم يتم العثور على أقسام للمتطلبات، استخدم النص كاملاً
        if not requirement_sections:
            requirement_sections = [text]
        
        # معالجة كل قسم
        for section in requirement_sections:
            # استخراج المتطلبات من النص
            section_requirements = self._parse_requirements_text(section)
            
            # دمج المتطلبات المستخرجة
            requirements.extend(section_requirements)
        
        # إذا لم يتم العثور على متطلبات، استخدم القوالب
        if not requirements:
            requirements = self._generate_template_requirements()
        
        # تنظيف وتوحيد المتطلبات
        requirements = self._clean_requirements(requirements)
        
        return requirements
    
    def _find_requirement_sections(self, text: str) -> List[str]:
        """
        البحث عن أقسام المتطلبات في النص
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[str]
            أقسام المتطلبات المستخرجة
        """
        sections = []
        
        # الكلمات المفتاحية لأقسام المتطلبات
        section_keywords = [
            "المتطلبات", "الشروط", "المواصفات", "نطاق العمل", 
            "البنود", "المعايير", "الالتزامات", "المؤهلات", 
            "التأهيل", "الواجبات", "نطاق الأعمال", "الخدمات المطلوبة"
        ]
        
        # البحث عن أقسام المتطلبات
        for keyword in section_keywords:
            pattern = rf"((?:{keyword}|{keyword.upper()})[:\s].*?)(?:^(?:{section_keywords[0]}|{section_keywords[0].upper()})[:\s]|\Z)"
            matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL)
            
            for match in matches:
                section_text = match.group(1).strip()
                if len(section_text) > 50:  # تجاهل الأقسام القصيرة جدًا
                    sections.append(section_text)
        
        # البحث عن قوائم البنود
        bullet_lists = re.findall(r'(?:^|\n)(?:[•\-*]\s+.*(?:\n|$))+', text, re.MULTILINE)
        
        for bullet_list in bullet_lists:
            if len(bullet_list) > 100:  # تجاهل القوائم القصيرة
                sections.append(bullet_list)
        
        # البحث عن قوائم مرقمة
        numbered_lists = re.findall(r'(?:^|\n)(?:\d+[.)\s]+.*(?:\n|$))+', text, re.MULTILINE)
        
        for numbered_list in numbered_lists:
            if len(numbered_list) > 100:  # تجاهل القوائم القصيرة
                sections.append(numbered_list)
        
        return sections
    
    def _parse_requirements_text(self, text: str) -> List[Dict[str, Any]]:
        """
        تحليل نص المتطلبات لاستخراج المتطلبات الفردية
        
        المعاملات:
        ----------
        text : str
            نص قسم المتطلبات
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة المتطلبات المستخرجة
        """
        requirements = []
        
        # استخراج المتطلبات من القوائم النقطية
        bullet_items = re.findall(r'[•\-*]\s+(.*?)(?:\n[•\-*]|\n\n|\Z)', text, re.DOTALL)
        
        for item in bullet_items:
            item = item.strip()
            if len(item) > 10:  # تجاهل العناصر القصيرة جدًا
                requirements.append({
                    "title": self._extract_requirement_title(item),
                    "description": item,
                    "source": "bullet_list"
                })
        
        # استخراج المتطلبات من القوائم المرقمة
        numbered_items = re.findall(r'(\d+)[.)\s]+(.*?)(?:\n\d+[.)\s]|\n\n|\Z)', text, re.DOTALL)
        
        for num, item in numbered_items:
            item = item.strip()
            if len(item) > 10:  # تجاهل العناصر القصيرة جدًا
                requirements.append({
                    "title": self._extract_requirement_title(item),
                    "description": item,
                    "source": "numbered_list",
                    "number": int(num)
                })
        
        # استخراج المتطلبات من الفقرات
        if not requirements:
            paragraphs = re.split(r'\n\s*\n', text)
            
            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                if len(paragraph) > 50 and len(paragraph) < 500:  # تجاهل الفقرات القصيرة جدًا أو الطويلة جدًا
                    # تحقق مما إذا كانت الفقرة تحتوي على عبارات المتطلبات
                    if any(keyword in paragraph.lower() for keyword in ["يجب", "ضرورة", "إلزامي", "مطلوب", "يلتزم", "لا بد", "لابد", "شرط", "اشتراط"]):
                        requirements.append({
                            "title": self._extract_requirement_title(paragraph),
                            "description": paragraph,
                            "source": "paragraph"
                        })
        
        return requirements
    
    import re

    def _extract_requirement_title(self, text: str) -> str:
        """
        استخراج عنوان المتطلب من النص.

        المعاملات:
        ----------
        text : str
            نص المتطلب.

        المخرجات:
        --------
        str
            عنوان المتطلب المستخرج.
        """
        # تنظيف النص وإزالة أي فراغات زائدة
        text = text.strip()

        # محاولة استخراج العنوان من بداية النص باستخدام الجملة الأولى
        first_sentence = re.split(r'[.!?،؛]', text)[0].strip()

        # إذا كان النص قصيرًا جدًا، نعيده كما هو
        if len(first_sentence) < 5:
            return text
        
        # التحقق من أن العنوان لا يحتوي على أرقام أو رموز غير مفهومة
        if re.search(r'\d', first_sentence):
            return text  # إذا كان هناك أرقام، نعيد النص الأصلي

        return first_sentence


