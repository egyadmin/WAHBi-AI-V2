import os
import re
import json
import datetime
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Union, Tuple, Optional
from datetime import datetime, timedelta

class ScheduleAnalyzer:
    """
    فئة لتحليل الجدول الزمني للمناقصات
    """
    
    def __init__(self):
        """
        تهيئة محلل الجدول الزمني
        """
        # تحميل قوالب الجداول الزمنية
        self.schedule_templates = self._load_schedule_templates()
        
        # تحميل معايير تقييم الجداول الزمنية
        self.evaluation_criteria = self._load_evaluation_criteria()
        
        # تحميل قاعدة بيانات المشاريع السابقة
        self.historical_projects = self._load_historical_projects()
    
    def _load_schedule_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل قوالب الجداول الزمنية حسب نوع المشروع
        """
        # في التطبيق الفعلي، قد تُحمل هذه البيانات من ملف أو قاعدة بيانات
        return {
            "الإنشاءات": {
                "phases": [
                    {
                        "name": "التخطيط والتصميم",
                        "duration_percentage": 0.15,
                        "activities": [
                            "إعداد المخططات الأولية",
                            "الحصول على الموافقات",
                            "إعداد المخططات التفصيلية",
                            "تصميم الأنظمة الكهربائية والميكانيكية",
                            "إعداد جداول الكميات"
                        ]
                    },
                    {
                        "name": "التجهيز والتعاقد",
                        "duration_percentage": 0.10,
                        "activities": [
                            "إعداد وثائق العطاء",
                            "طرح العطاء",
                            "تقييم العروض",
                            "توقيع العقود مع المقاولين",
                            "تجهيز الموقع"
                        ]
                    },
                    {
                        "name": "الأعمال الإنشائية",
                        "duration_percentage": 0.50,
                        "activities": [
                            "أعمال الحفر والأساسات",
                            "أعمال الهيكل الخرساني",
                            "أعمال البناء",
                            "أعمال التشطيبات الخارجية",
                            "أعمال التشطيبات الداخلية"
                        ]
                    },
                    {
                        "name": "الأنظمة والمرافق",
                        "duration_percentage": 0.15,
                        "activities": [
                            "تركيب الأنظمة الكهربائية",
                            "تركيب الأنظمة الميكانيكية",
                            "تركيب أنظمة التكييف",
                            "تركيب أنظمة السباكة",
                            "تركيب أنظمة الحريق والإنذار"
                        ]
                    },
                    {
                        "name": "الاختبار والتسليم",
                        "duration_percentage": 0.10,
                        "activities": [
                            "اختبار الأنظمة",
                            "تشغيل تجريبي",
                            "إصلاح الملاحظات",
                            "التسليم المبدئي",
                            "التسليم النهائي"
                        ]
                    }
                ],
                "critical_activities": [
                    "إعداد المخططات التفصيلية",
                    "أعمال الحفر والأساسات",
                    "أعمال الهيكل الخرساني",
                    "تركيب الأنظمة الكهربائية",
                    "اختبار الأنظمة"
                ]
            },
            "تقنية المعلومات": {
                "phases": [
                    {
                        "name": "التحليل والتخطيط",
                        "duration_percentage": 0.15,
                        "activities": [
                            "تحليل المتطلبات",
                            "دراسة الجدوى",
                            "تحديد نطاق المشروع",
                            "إعداد خطة المشروع",
                            "تحديد الموارد اللازمة"
                        ]
                    },
                    {
                        "name": "التصميم",
                        "duration_percentage": 0.20,
                        "activities": [
                            "تصميم هيكل النظام",
                            "تصميم قاعدة البيانات",
                            "تصميم واجهات المستخدم",
                            "تصميم الخوارزميات",
                            "توثيق التصميم"
                        ]
                    },
                    {
                        "name": "التطوير",
                        "duration_percentage": 0.40,
                        "activities": [
                            "تطوير النظام الأساسي",
                            "تطوير قاعدة البيانات",
                            "تطوير واجهات المستخدم",
                            "تطوير وحدات النظام",
                            "تكامل الوحدات"
                        ]
                    },
                    {
                        "name": "الاختبار",
                        "duration_percentage": 0.15,
                        "activities": [
                            "اختبار الوحدات",
                            "اختبار التكامل",
                            "اختبار النظام",
                            "اختبار القبول",
                            "إصلاح الأخطاء"
                        ]
                    },
                    {
                        "name": "النشر والتدريب",
                        "duration_percentage": 0.10,
                        "activities": [
                            "إعداد بيئة الإنتاج",
                            "نشر النظام",
                            "تدريب المستخدمين",
                            "إعداد وثائق المستخدم",
                            "الدعم الأولي"
                        ]
                    }
                ],
                "critical_activities": [
                    "تحليل المتطلبات",
                    "تصميم هيكل النظام",
                    "تطوير النظام الأساسي",
                    "تكامل الوحدات",
                    "اختبار القبول"
                ]
            },
            "عام": {
                "phases": [
                    {
                        "name": "التخطيط",
                        "duration_percentage": 0.15,
                        "activities": [
                            "تحديد الأهداف",
                            "تحديد النطاق",
                            "تحديد الموارد",
                            "تحديد الميزانية",
                            "إعداد خطة المشروع"
                        ]
                    },
                    {
                        "name": "التنفيذ",
                        "duration_percentage": 0.60,
                        "activities": [
                            "توفير الموارد",
                            "تنفيذ الأنشطة",
                            "مراقبة التقدم",
                            "إدارة المخاطر",
                            "ضبط الجودة"
                        ]
                    },
                    {
                        "name": "الإغلاق",
                        "duration_percentage": 0.25,
                        "activities": [
                            "اختبار المخرجات",
                            "تسليم المخرجات",
                            "توثيق الدروس المستفادة",
                            "إغلاق العقود",
                            "إغلاق المشروع"
                        ]
                    }
                ],
                "critical_activities": [
                    "تحديد النطاق",
                    "توفير الموارد",
                    "تنفيذ الأنشطة",
                    "اختبار المخرجات",
                    "تسليم المخرجات"
                ]
            }
        }
    
    def _load_evaluation_criteria(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل معايير تقييم الجداول الزمنية
        """
        # في التطبيق الفعلي، قد تُحمل هذه البيانات من ملف أو قاعدة بيانات
        return {
            "realism": {
                "weight": 0.3,
                "criteria": [
                    "توافق مدة المشروع مع مشاريع مماثلة",
                    "توافق توزيع الموارد مع الأنشطة",
                    "مراعاة العوامل الخارجية والمخاطر"
                ]
            },
            "completeness": {
                "weight": 0.2,
                "criteria": [
                    "شمولية الأنشطة",
                    "تحديد المعالم الرئيسية",
                    "تحديد نقاط التسليم"
                ]
            },
            "resource_allocation": {
                "weight": 0.2,
                "criteria": [
                    "توزيع مناسب للموارد",
                    "تجنب تحميل زائد للموارد",
                    "تحديد المسؤوليات"
                ]
            },
            "risk_management": {
                "weight": 0.15,
                "criteria": [
                    "تضمين احتياطيات زمنية",
                    "تحديد المسار الحرج",
                    "خطط بديلة للأنشطة الحرجة"
                ]
            },
            "flexibility": {
                "weight": 0.15,
                "criteria": [
                    "قابلية التعديل والتحديث",
                    "آلية للتعامل مع التغييرات",
                    "مراقبة التقدم وتقييمه"
                ]
            }
        }
    
    def _load_historical_projects(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل بيانات المشاريع السابقة للمقارنة
        """
        # في التطبيق الفعلي، قد تُحمل هذه البيانات من ملف أو قاعدة بيانات
        return {
            "الإنشاءات": {
                "small": {
                    "avg_duration": 12,  # متوسط المدة بالأشهر
                    "min_duration": 6,
                    "max_duration": 18
                },
                "medium": {
                    "avg_duration": 24,
                    "min_duration": 18,
                    "max_duration": 36
                },
                "large": {
                    "avg_duration": 48,
                    "min_duration": 36,
                    "max_duration": 60
                }
            },
            "تقنية المعلومات": {
                "small": {
                    "avg_duration": 6,
                    "min_duration": 3,
                    "max_duration": 9
                },
                "medium": {
                    "avg_duration": 12,
                    "min_duration": 9,
                    "max_duration": 18
                },
                "large": {
                    "avg_duration": 24,
                    "min_duration": 18,
                    "max_duration": 36
                }
            },
            "عام": {
                "small": {
                    "avg_duration": 6,
                    "min_duration": 3,
                    "max_duration": 12
                },
                "medium": {
                    "avg_duration": 12,
                    "min_duration": 9,
                    "max_duration": 24
                },
                "large": {
                    "avg_duration": 24,
                    "min_duration": 18,
                    "max_duration": 36
                }
            }
        }
    
    def analyze(self, extracted_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        تحليل الجدول الزمني بناءً على البيانات المستخرجة
        
        المعاملات:
        ----------
        extracted_data : Dict[str, Any]
            البيانات المستخرجة من المستندات
        **kwargs : Dict[str, Any]
            معاملات إضافية مثل نوع المشروع، الميزانية، تاريخ البدء، المدة
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل الجدول الزمني
        """
        results = {
            "phases": [],
            "critical_path": [],
            "milestones": [],
            "evaluation": {},
            "optimization": [],
            "risks": []
        }
        
        # تحديد نوع المشروع والقطاع
        project_type = kwargs.get("project_type", "")
        sector = self._determine_sector(project_type, extracted_data)
        
        # استخراج معلومات الجدول الزمني من البيانات المستخرجة
        schedule_info = self._extract_schedule_info(extracted_data)
        
        # تحديد حجم المشروع
        project_size = self._determine_project_size(kwargs.get("budget", 0), schedule_info.get("duration", 0))
        
        # إعداد الجدول الزمني
        phases = self._prepare_schedule(schedule_info, sector, project_size, kwargs)
        results["phases"] = phases
        
        # تحديد المسار الحرج
        critical_path = self._identify_critical_path(phases, sector)
        results["critical_path"] = critical_path
        
        # تحديد المعالم الرئيسية
        milestones = self._identify_milestones(phases, schedule_info)
        results["milestones"] = milestones
        
        # تقييم الجدول الزمني
        evaluation = self._evaluate_schedule(phases, schedule_info, sector, project_size)
        results["evaluation"] = evaluation
        
        # اقتراحات لتحسين الجدول الزمني
        optimization = self._generate_optimization_suggestions(phases, evaluation, schedule_info)
        results["optimization"] = optimization
        
        # تحليل المخاطر المتعلقة بالجدول الزمني
        risks = self._analyze_schedule_risks(phases, schedule_info, sector)
        results["risks"] = risks
        
        return results
    
    def _determine_sector(self, project_type: str, extracted_data: Dict[str, Any]) -> str:
        """
        تحديد القطاع بناءً على نوع المشروع والبيانات المستخرجة
        """
        # قاموس لتحويل أنواع المشاريع الشائعة إلى قطاعات
        project_to_sector = {
            "إنشاءات": "الإنشاءات",
            "مباني": "الإنشاءات",
            "طرق": "الإنشاءات",
            "جسور": "الإنشاءات",
            "تقنية معلومات": "تقنية المعلومات",
            "برمجيات": "تقنية المعلومات",
            "تطبيقات": "تقنية المعلومات"
        }
        
        # محاولة تحديد القطاع من نوع المشروع
        if project_type:
            for key, value in project_to_sector.items():
                if key in project_type.lower():
                    return value
        
        # إذا لم يتم تحديد القطاع من نوع المشروع، نحاول تحديده من البيانات المستخرجة
        if "text" in extracted_data:
            text = extracted_data["text"].lower()
            sector_scores = {}
            
            for key, value in project_to_sector.items():
                score = text.count(key.lower())
                if value not in sector_scores:
                    sector_scores[value] = 0
                sector_scores[value] += score
            
            # اختيار القطاع الأكثر ذكراً
            if sector_scores:
                max_sector = max(sector_scores, key=sector_scores.get)
                if sector_scores[max_sector] > 0:
                    return max_sector
        
        # القطاع الافتراضي إذا لم نتمكن من تحديده
        return "عام"
    
    def _extract_schedule_info(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        استخراج معلومات الجدول الزمني من البيانات المستخرجة
        """
        schedule_info = {
            "start_date": None,
            "end_date": None,
            "duration": None,
            "activities": [],
            "milestones": [],
            "dependencies": []
        }
        
        # استخراج التواريخ من البيانات المستخرجة
        if "dates" in extracted_data:
            dates = extracted_data["dates"]
            
            for date_info in dates:
                date_type = date_info.get("type", "")
                date_str = date_info.get("date", "")
                
                if not date_str:
                    continue
                
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                    
                    if "بداية" in date_type.lower() or "بدأ" in date_type.lower() or "انطلاق" in date_type.lower():
                        if schedule_info["start_date"] is None or date_obj < schedule_info["start_date"]:
                            schedule_info["start_date"] = date_obj
                    
                    if "نهاية" in date_type.lower() or "انتهاء" in date_type.lower() or "إغلاق" in date_type.lower():
                        if schedule_info["end_date"] is None or date_obj > schedule_info["end_date"]:
                            schedule_info["end_date"] = date_obj
                    
                    # إذا كان هناك نوع تاريخ محدد للمعالم الرئيسية
                    if "معلم" in date_type.lower() or "محطة" in date_type.lower() or "مرحلة" in date_type.lower() or "تسليم" in date_type.lower():
                        schedule_info["milestones"].append({
                            "name": date_type,
                            "date": date_obj,
                            "description": date_info.get("context", "")
                        })
                except Exception as e:
                    print(f"Error parsing date: {date_str}, {str(e)}")
        
        # حساب المدة إذا كان هناك تاريخ بداية ونهاية
        if schedule_info["start_date"] and schedule_info["end_date"]:
            delta = schedule_info["end_date"] - schedule_info["start_date"]
            schedule_info["duration"] = delta.days // 30  # تقريب المدة إلى الأشهر
        
        # استخراج الأنشطة من المتطلبات
        if "requirements" in extracted_data:
            for req in extracted_data["requirements"]:
                if "زمني" in req.get("category", "").lower() or "جدول" in req.get("title", "").lower() or "مدة" in req.get("title", "").lower():
                    activity = {
                        "name": req.get("title", ""),
                        "description": req.get("description", ""),
                        "duration": None  # سيتم تقديره لاحقاً
                    }
                    
                    # محاولة استخراج المدة من الوصف
                    duration_match = re.search(r'(\d+)\s+(يوم|أيام|أسبوع|أسابيع|شهر|شهور|سنة|سنوات)', req.get("description", "").lower())
                    if duration_match:
                        duration_value = int(duration_match.group(1))
                        duration_unit = duration_match.group(2)
                        
                        # تحويل المدة إلى أيام
                        if "يوم" in duration_unit:
                            activity["duration"] = duration_value
                        elif "أسبوع" in duration_unit:
                            activity["duration"] = duration_value * 7
                        elif "شهر" in duration_unit:
                            activity["duration"] = duration_value * 30
                        elif "سنة" in duration_unit:
                            activity["duration"] = duration_value * 365
                    
                    schedule_info["activities"].append(activity)
        
        # استخراج المعالم الرئيسية من النص
        if "text" in extracted_data:
            text = extracted_data["text"].lower()
            milestone_patterns = [
                r'(معلم|محطة|مرحلة|تسليم)[^:]*:(.*?)(?=\n|$)',
                r'(معلم|محطة|مرحلة|تسليم)[^:]*بتاريخ[^:]*:(.*?)(?=\n|$)'
            ]
            
            for pattern in milestone_patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    milestone_type = match.group(1).strip()
                    milestone_description = match.group(2).strip()
                    
                    # محاولة استخراج التاريخ من الوصف
                    date_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', milestone_description)
                    if date_match:
                        day = int(date_match.group(1))
                        month = int(date_match.group(2))
                        year = int(date_match.group(3))
                        
                        if year < 100:
                            year += 2000
                        
                        try:
                            date_obj = datetime(year, month, day).date()
                            
                            # التحقق من عدم وجود هذا المعلم مسبقاً
                            if not any(milestone["description"] == milestone_description for milestone in schedule_info["milestones"]):
                                schedule_info["milestones"].append({
                                    "name": milestone_type,
                                    "date": date_obj,
                                    "description": milestone_description
                                })
                        except Exception as e:
                            print(f"Error parsing milestone date: {day}/{month}/{year}, {str(e)}")
        
        # استخراج المدة الإجمالية من النص إذا لم يتم تحديدها مسبقاً
        if schedule_info["duration"] is None and "text" in extracted_data:
            text = extracted_data["text"].lower()
            duration_patterns = [
                r'مدة المشروع[^:]*:?\s*(\d+)\s+(يوم|أيام|أسبوع|أسابيع|شهر|شهور|سنة|سنوات)',
                r'مدة التنفيذ[^:]*:?\s*(\d+)\s+(يوم|أيام|أسبوع|أسابيع|شهر|شهور|سنة|سنوات)',
                r'المدة الزمنية[^:]*:?\s*(\d+)\s+(يوم|أيام|أسبوع|أسابيع|شهر|شهور|سنة|سنوات)'
            ]
            
            for pattern in duration_patterns:
                match = re.search(pattern, text)
                if match:
                    duration_value = int(match.group(1))
                    duration_unit = match.group(2)
                    
                    # تحويل المدة إلى أشهر
                    if "يوم" in duration_unit:
                        schedule_info["duration"] = duration_value / 30
                    elif "أسبوع" in duration_unit:
                        schedule_info["duration"] = duration_value / 4
                    elif "شهر" in duration_unit:
                        schedule_info["duration"] = duration_value
                    elif "سنة" in duration_unit:
                        schedule_info["duration"] = duration_value * 12
                    
                    break
        
        return schedule_info
    
    def _determine_project_size(self, budget: float, duration: int) -> str:
        """
        تحديد حجم المشروع بناءً على الميزانية والمدة
        """
        if budget == 0 and duration == 0:
            return "medium"
        
        # تحديد الحجم بناءً على الميزانية
        size_by_budget = "medium"
        if budget > 10000000:  # أكثر من 10 مليون ريال
            size_by_budget = "large"
        elif budget < 1000000:  # أقل من مليون ريال
            size_by_budget = "small"
        
        # تحديد الحجم بناءً على المدة
        size_by_duration = "medium"
        if duration > 24:  # أكثر من 24 شهر
            size_by_duration = "large"
        elif duration < 6:  # أقل من 6 أشهر
            size_by_duration = "small"
        
        # اختيار الحجم الأكبر
        if size_by_budget == "large" or size_by_duration == "large":
            return "large"
        elif size_by_budget == "small" and size_by_duration == "small":
            return "small"
        else:
            return "medium"
    
    def _prepare_schedule(self, schedule_info: Dict[str, Any], sector: str, project_size: str, kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        إعداد الجدول الزمني بناءً على المعلومات المستخرجة والقوالب
        """
        # استخدام قالب الجدول الزمني المناسب للقطاع
        schedule_template = self.schedule_templates.get(sector, self.schedule_templates["عام"])
        
        # تحديد تاريخ البدء
        start_date = schedule_info.get("start_date")
        if start_date is None:
            start_date = kwargs.get("start_date", datetime.now().date())
        
        # تحديد المدة الإجمالية
        duration = schedule_info.get("duration")
        if duration is None:
            duration = kwargs.get("duration", 0)
            
            # إذا لم يتم تحديد المدة، استخدام متوسط المدة من بيانات المشاريع السابقة
            if duration == 0 and sector in self.historical_projects and project_size in self.historical_projects[sector]:
                duration = self.historical_projects[sector][project_size]["avg_duration"]
        
        # إعداد المراحل
        phases = []
        current_start_date = start_date
        
        for phase_template in schedule_template["phases"]:
            phase_duration = int(duration * phase_template["duration_percentage"])
            if phase_duration < 1:
                phase_duration = 1  # الحد الأدنى للمدة هو شهر واحد
            
            phase_end_date = current_start_date + timedelta(days=phase_duration * 30)
            
            # إعداد الأنشطة
            activities = []
            activity_duration = phase_duration // len(phase_template["activities"])
            if activity_duration < 1:
                activity_duration = 1
            
            activity_start_date = current_start_date
            
            for activity_name in phase_template["activities"]:
                activity_end_date = activity_start_date + timedelta(days=activity_duration * 30)
                
                activity = {
                    "name": activity_name,
                    "start_date": activity_start_date.strftime("%Y-%m-%d"),
                    "end_date": activity_end_date.strftime("%Y-%m-%d"),
                    "duration": activity_duration
                }
                
                activities.append(activity)
                activity_start_date = activity_end_date
            
            phase = {
                "name": phase_template["name"],
                "start_date": current_start_date.strftime("%Y-%m-%d"),
                "end_date": phase_end_date.strftime("%Y-%m-%d"),
                "duration": phase_duration,
                "activities": activities
            }
            
            phases.append(phase)
            current_start_date = phase_end_date
        
        return phases
    
    def _identify_critical_path(self, phases: List[Dict[str, Any]], sector: str) -> List[str]:
        """
        تحديد المسار الحرج في الجدول الزمني
        """
        # استخدام قائمة الأنشطة الحرجة من القالب
        schedule_template = self.schedule_templates.get(sector, self.schedule_templates["عام"])
        template_critical_activities = schedule_template.get("critical_activities", [])
        
        # تجميع كل الأنشطة من جميع المراحل
        all_activities = []
        for phase in phases:
            for activity in phase.get("activities", []):
                all_activities.append({
                    "phase": phase["name"],
                    "name": activity["name"],
                    "start_date": activity["start_date"],
                    "end_date": activity["end_date"],
                    "duration": activity["duration"]
                })
        
        # تحديد الأنشطة الحرجة
        critical_path = []
        
        # إضافة الأنشطة من القالب إذا وجدت
        for template_activity in template_critical_activities:
            for activity in all_activities:
                if template_activity in activity["name"]:
                    critical_activity = f"{activity['phase']} - {activity['name']}"
                    if critical_activity not in critical_path:
                        critical_path.append(critical_activity)
        
        # إذا لم يتم العثور على أنشطة حرجة، استخدام الأنشطة ذات المدة الأطول
        if not critical_path:
            sorted_activities = sorted(all_activities, key=lambda x: x["duration"], reverse=True)
            for activity in sorted_activities[:5]:  # اختيار أطول 5 أنشطة
                critical_activity = f"{activity['phase']} - {activity['name']}"
                critical_path.append(critical_activity)
        
        return critical_path
    
    def _identify_milestones(self, phases: List[Dict[str, Any]], schedule_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        تحديد المعالم الرئيسية في الجدول الزمني
        """
        milestones = []
        
        # إضافة المعالم المستخرجة من البيانات
        for milestone in schedule_info.get("milestones", []):
            milestones.append({
                "name": milestone.get("name", "معلم"),
                "date": milestone.get("date").strftime("%Y-%m-%d") if isinstance(milestone.get("date"), datetime) else milestone.get("date"),
                "description": milestone.get("description", ""),
                "source": "مستخرج"
            })
        
        # إضافة بداية ونهاية كل مرحلة كمعالم
        for phase in phases:
            # إضافة بداية المرحلة
            start_milestone = {
                "name": f"بداية {phase['name']}",
                "date": phase["start_date"],
                "description": f"تاريخ بدء مرحلة {phase['name']}",
                "source": "مولد"
            }
            milestones.append(start_milestone)
            
            # إضافة نهاية المرحلة
            end_milestone = {
                "name": f"نهاية {phase['name']}",
                "date": phase["end_date"],
                "description": f"تاريخ انتهاء مرحلة {phase['name']}",
                "source": "مولد"
            }
            milestones.append(end_milestone)
        
        # ترتيب المعالم حسب التاريخ
        try:
            milestones = sorted(milestones, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))
        except Exception as e:
            print(f"Error sorting milestones: {str(e)}")
        
        return milestones
    
    def _evaluate_schedule(self, phases: List[Dict[str, Any]], schedule_info: Dict[str, Any], sector: str, project_size: str) -> Dict[str, Any]:
        """
        تقييم الجدول الزمني
        """
        evaluation = {
            "overall_score": 0.0,
            "criteria_scores": {},
            "comments": []
        }
        
        # حساب المدة الإجمالية
        total_duration = sum(phase["duration"] for phase in phases)
        
        # تقييم واقعية الجدول الزمني
        realism_score = self._evaluate_realism(total_duration, sector, project_size)
        evaluation["criteria_scores"]["realism"] = realism_score
        
        # تقييم اكتمال الجدول الزمني
        completeness_score = self._evaluate_completeness(phases, schedule_info)
        evaluation["criteria_scores"]["completeness"] = completeness_score
        
        # تقييم توزيع الموارد
        resource_score = self._evaluate_resource_allocation(phases)
        evaluation["criteria_scores"]["resource_allocation"] = resource_score
        
        # تقييم إدارة المخاطر
        risk_score = self._evaluate_risk_management(phases, schedule_info)
        evaluation["criteria_scores"]["risk_management"] = risk_score
        
        # تقييم المرونة
        flexibility_score = self._evaluate_flexibility(phases, schedule_info)
        evaluation["criteria_scores"]["flexibility"] = flexibility_score
        
        # حساب التقييم الإجمالي
        overall_score = 0.0
        for criterion, score in evaluation["criteria_scores"].items():
            weight = self.evaluation_criteria[criterion]["weight"]
            overall_score += score * weight
        
        evaluation["overall_score"] = round(overall_score, 2)
        
        # إضافة تعليقات
        if overall_score >= 0.8:
            evaluation["comments"].append("الجدول الزمني واقعي ومكتمل ويتضمن توزيعاً جيداً للموارد")
        elif overall_score >= 0.6:
            evaluation["comments"].append("الجدول الزمني جيد بشكل عام لكنه يحتاج إلى بعض التحسينات")
        else:
            evaluation["comments"].append("الجدول الزمني يحتاج إلى مراجعة شاملة وتحسينات كبيرة")
        
        if realism_score < 0.6:
            evaluation["comments"].append("المدة الإجمالية للمشروع غير واقعية مقارنة بمشاريع مماثلة")
        
        if completeness_score < 0.6:
            evaluation["comments"].append("الجدول الزمني يفتقر إلى بعض الأنشطة الهامة أو المعالم الرئيسية")
        
        if resource_score < 0.6:
            evaluation["comments"].append("توزيع الموارد غير متوازن وقد يؤدي إلى تأخير في المشروع")
        
        if risk_score < 0.6:
            evaluation["comments"].append("الجدول الزمني لا يتضمن احتياطيات كافية للتعامل مع المخاطر")
        
        if flexibility_score < 0.6:
            evaluation["comments"].append("الجدول الزمني يفتقر إلى المرونة اللازمة للتعامل مع التغييرات")
        
        return evaluation
    
    def _evaluate_realism(self, total_duration: int, sector: str, project_size: str) -> float:
        """
        تقييم واقعية الجدول الزمني
        """
        # المقارنة مع بيانات المشاريع السابقة
        if sector in self.historical_projects and project_size in self.historical_projects[sector]:
            historical_data = self.historical_projects[sector][project_size]
            avg_duration = historical_data["avg_duration"]
            min_duration = historical_data["min_duration"]
            max_duration = historical_data["max_duration"]
            
            # إذا كانت المدة ضمن النطاق المقبول
            if min_duration <= total_duration <= max_duration:
                # حساب الفرق بين المدة والمتوسط
                diff = abs(total_duration - avg_duration) / (max_duration - min_duration)
                score = 1.0 - diff
                return max(0.5, score)  # الحد الأدنى للتقييم هو 0.5
            else:
                # إذا كانت المدة خارج النطاق المقبول
                return 0.3
        
        # إذا لم تتوفر بيانات للمقارنة
        return 0.5
    
    def _evaluate_completeness(self, phases: List[Dict[str, Any]], schedule_info: Dict[str, Any]) -> float:
        """
        تقييم اكتمال الجدول الزمني
        """
        # حساب عدد المراحل والأنشطة والمعالم
        num_phases = len(phases)
        num_activities = sum(len(phase.get("activities", [])) for phase in phases)
        num_milestones = len(schedule_info.get("milestones", []))
        
        # تقييم اكتمال المراحل
        phases_score = min(1.0, num_phases / 5)  # افتراض أن 5 مراحل هو العدد المثالي
        
        # تقييم اكتمال الأنشطة
        activities_score = min(1.0, num_activities / 20)  # افتراض أن 20 نشاط هو العدد المثالي
        
        # تقييم اكتمال المعالم
        milestones_score = min(1.0, num_milestones / 10)  # افتراض أن 10 معالم هو العدد المثالي
        
        # حساب التقييم الإجمالي للاكتمال
        completeness_score = (phases_score * 0.3) + (activities_score * 0.5) + (milestones_score * 0.2)
        
        return round(completeness_score, 2)
    
    def _evaluate_resource_allocation(self, phases: List[Dict[str, Any]]) -> float:
        """
        تقييم توزيع الموارد في الجدول الزمني
        """
        # في التطبيق الفعلي، هذا يحتاج إلى بيانات أكثر عن الموارد
        # هذا تقييم مبسط بناءً على توزيع المدة على المراحل
        
        # حساب إجمالي المدة
        total_duration = sum(phase["duration"] for phase in phases)
        
        # حساب الانحراف المعياري لمدة المراحل
        durations = [phase["duration"] for phase in phases]
        mean_duration = total_duration / len(phases)
        variance = sum((d - mean_duration) ** 2 for d in durations) / len(phases)
        std_dev = variance ** 0.5
        
        # حساب معامل الاختلاف (نسبة الانحراف المعياري إلى المتوسط)
        coef_of_variation = std_dev / mean_duration if mean_duration > 0 else 0
        
        # حساب التقييم: كلما قل معامل الاختلاف، كان التوزيع أكثر توازناً
        resource_score = max(0, 1.0 - coef_of_variation)
        
        return round(resource_score, 2)
    
    def _evaluate_risk_management(self, phases: List[Dict[str, Any]], schedule_info: Dict[str, Any]) -> float:
        """
        تقييم إدارة المخاطر في الجدول الزمني
        """
        # في التطبيق الفعلي، هذا يحتاج إلى بيانات أكثر عن المخاطر
        # هذا تقييم مبسط بناءً على وجود احتياطيات زمنية
        
        # حساب نسبة الاحتياطي الزمني المقدرة
        total_duration = sum(phase["duration"] for phase in phases)
        estimated_buffer = total_duration * 0.1  # افتراض أن 10% من المدة الكلية يجب أن تكون احتياطي
        actual_buffer = 0
        
        # البحث عن أنشطة أو مراحل تمثل احتياطيات
        for phase in phases:
            phase_name = phase["name"].lower()
            if "احتياطي" in phase_name or "طوارئ" in phase_name:
                actual_buffer += phase["duration"]
            
            for activity in phase.get("activities", []):
                activity_name = activity["name"].lower()
                if "احتياطي" in activity_name or "طوارئ" in activity_name:
                    actual_buffer += activity["duration"]
        
        # حساب نسبة الاحتياطي الفعلي إلى المقدر
        buffer_ratio = actual_buffer / estimated_buffer if estimated_buffer > 0 else 0
        buffer_score = min(1.0, buffer_ratio)
        
        # حساب تقييم المسار الحرج
        critical_path_identified = 1.0 if len(schedule_info.get("critical_path", [])) > 0 else 0.0
        
        # حساب التقييم الإجمالي لإدارة المخاطر
        risk_score = (buffer_score * 0.6) + (critical_path_identified * 0.4)
        
        return round(risk_score, 2)
    
    def _evaluate_flexibility(self, phases: List[Dict[str, Any]], schedule_info: Dict[str, Any]) -> float:
        """
        تقييم مرونة الجدول الزمني
        """
        # في التطبيق الفعلي، هذا يحتاج إلى بيانات أكثر عن آليات التعديل والمراقبة
        # هذا تقييم مبسط بناءً على وجود فترات مراجعة وتقييم
        
        # البحث عن أنشطة تتعلق بالمراجعة والتقييم
        review_activities = 0
        total_activities = 0
        
        for phase in phases:
            for activity in phase.get("activities", []):
                total_activities += 1
                activity_name = activity["name"].lower()
                if "مراجعة" in activity_name or "تقييم" in activity_name or "متابعة" in activity_name:
                    review_activities += 1
        
        # حساب نسبة أنشطة المراجعة والتقييم
        review_ratio = review_activities / total_activities if total_activities > 0 else 0
        review_score = min(1.0, review_ratio * 5)  # افتراض أن 20% من الأنشطة يجب أن تكون للمراجعة والتقييم
        
        # حساب التقييم الإجمالي للمرونة
        flexibility_score = review_score
        
        return round(flexibility_score, 2)
    
    def _generate_optimization_suggestions(self, phases: List[Dict[str, Any]], evaluation: Dict[str, Any], schedule_info: Dict[str, Any]) -> List[str]:
        """
        إعداد اقتراحات لتحسين الجدول الزمني
        """
        optimization_suggestions = []
        
        # اقتراحات بناءً على التقييم
        criteria_scores = evaluation.get("criteria_scores", {})
        
        # اقتراحات لتحسين واقعية الجدول الزمني
        if criteria_scores.get("realism", 1.0) < 0.6:
            optimization_suggestions.append(
                "مراجعة المدة الإجمالية للمشروع ومقارنتها بمشاريع مماثلة للتأكد من واقعيتها"
            )
        
        # اقتراحات لتحسين اكتمال الجدول الزمني
        if criteria_scores.get("completeness", 1.0) < 0.6:
            optimization_suggestions.append(
                "تفصيل الأنشطة بشكل أكبر وإضافة المعالم الرئيسية لكل مرحلة"
            )
        
        # اقتراحات لتحسين توزيع الموارد
        if criteria_scores.get("resource_allocation", 1.0) < 0.6:
            optimization_suggestions.append(
                "تحسين توزيع الموارد بين المراحل المختلفة وتجنب التحميل الزائد للموارد"
            )
        
        # اقتراحات لتحسين إدارة المخاطر
        if criteria_scores.get("risk_management", 1.0) < 0.6:
            optimization_suggestions.append(
                "إضافة احتياطيات زمنية كافية للتعامل مع المخاطر المحتملة وتأخيرات المشروع"
            )
            optimization_suggestions.append(
                "تحديد المسار الحرج بوضوح وإعداد خطط بديلة للأنشطة الحرجة"
            )
        
        # اقتراحات لتحسين المرونة
        if criteria_scores.get("flexibility", 1.0) < 0.6:
            optimization_suggestions.append(
                "إضافة نقاط مراجعة وتقييم دورية للتأكد من سير المشروع وفق الخطة"
            )
            optimization_suggestions.append(
                "تطوير آلية واضحة للتعامل مع التغييرات وتحديث الجدول الزمني"
            )
        
        # اقتراحات عامة
        optimization_suggestions.extend([
            "استخدام أدوات إدارة المشاريع لمتابعة التقدم ومقارنته بالخطة الموضوعة",
            "تحديد المسؤوليات بوضوح لكل نشاط من أنشطة المشروع",
            "تحليل المسار الحرج وتقليل الاعتمادية بين الأنشطة لتقليل مخاطر التأخير"
        ])
        
        return optimization_suggestions
    
    def _analyze_schedule_risks(self, phases: List[Dict[str, Any]], schedule_info: Dict[str, Any], sector: str) -> List[Dict[str, Any]]:
        """
        تحليل المخاطر المتعلقة بالجدول الزمني
        """
        risks = []
        
        # مخاطر تتعلق بالمدة الإجمالية
        total_duration = sum(phase["duration"] for phase in phases)
        
        if sector in self.historical_projects:
            historical_data = self.historical_projects[sector]["medium"]  # افتراض حجم متوسط
            avg_duration = historical_data["avg_duration"]
            
            if total_duration < avg_duration * 0.7:
                risks.append({
                    "title": "مدة قصيرة جداً",
                    "description": "المدة الإجمالية للمشروع أقل بكثير من متوسط مدة مشاريع مماثلة",
                    "probability": "عالية",
                    "impact": "عالي",
                    "mitigation": [
                        "إعادة تقدير المدة الإجمالية بناءً على مشاريع مماثلة",
                        "تحديد الأنشطة التي يمكن تنفيذها بشكل متوازٍ لتقليل المدة",
                        "توفير موارد إضافية لتسريع تنفيذ الأنشطة الحرجة"
                    ]
                })
            elif total_duration > avg_duration * 1.3:
                risks.append({
                    "title": "مدة طويلة جداً",
                    "description": "المدة الإجمالية للمشروع أطول بكثير من متوسط مدة مشاريع مماثلة",
                    "probability": "متوسطة",
                    "impact": "متوسط",
                    "mitigation": [
                        "مراجعة تقديرات المدة لكل نشاط والتأكد من دقتها",
                        "تحليل الأنشطة غير الضرورية وإمكانية حذفها أو دمجها",
                        "تحسين كفاءة العمليات لتقليل المدة الإجمالية"
                    ]
                })
        
        # مخاطر تتعلق بالمسار الحرج
        if not schedule_info.get("critical_path"):
            risks.append({
                "title": "عدم تحديد المسار الحرج",
                "description": "لم يتم تحديد المسار الحرج في الجدول الزمني",
                "probability": "عالية",
                "impact": "عالي",
                "mitigation": [
                    "تحديد المسار الحرج باستخدام طريقة المسار الحرج (CPM)",
                    "إضافة احتياطيات زمنية للأنشطة الحرجة",
                    "مراقبة الأنشطة الحرجة بشكل مكثف"
                ]
            })
        
        # مخاطر تتعلق بالاحتياطيات الزمنية
        buffer_found = False
        for phase in phases:
            phase_name = phase["name"].lower()
            if "احتياطي" in phase_name or "طوارئ" in phase_name:
                buffer_found = True
                break
            
            for activity in phase.get("activities", []):
                activity_name = activity["name"].lower()
                if "احتياطي" in activity_name or "طوارئ" in activity_name:
                    buffer_found = True
                    break
            
            if buffer_found:
                break
        
        if not buffer_found:
            risks.append({
                "title": "عدم وجود احتياطيات زمنية",
                "description": "لم يتم تضمين احتياطيات زمنية في الجدول الزمني للتعامل مع المخاطر والتأخيرات",
                "probability": "عالية",
                "impact": "عالي",
                "mitigation": [
                    "إضافة احتياطيات زمنية بنسبة 10-15% من المدة الإجمالية",
                    "توزيع الاحتياطيات على الأنشطة الحرجة",
                    "إضافة معالم للمراجعة وإعادة التقييم"
                ]
            })
        
        # مخاطر تتعلق بتداخل الأنشطة
        activities_count = sum(len(phase.get("activities", [])) for phase in phases)
        phases_count = len(phases)
        
        if activities_count > 0 and phases_count > 0:
            avg_activities_per_phase = activities_count / phases_count
            
            if avg_activities_per_phase > 7:
                risks.append({
                    "title": "تداخل كبير في الأنشطة",
                    "description": "عدد كبير من الأنشطة المتداخلة في كل مرحلة قد يؤدي إلى صعوبة في الإدارة والتنفيذ",
                    "probability": "متوسطة",
                    "impact": "متوسط",
                    "mitigation": [
                        "تقسيم المراحل الكبيرة إلى مراحل أصغر",
                        "تحديد أولويات الأنشطة وتسلسلها بوضوح",
                        "تخصيص موارد كافية لإدارة الأنشطة المتداخلة"
                    ]
                })
        
        # مخاطر خاصة بالقطاع
        if sector == "الإنشاءات":
            risks.append({
                "title": "تأثير الظروف الجوية",
                "description": "قد تؤثر الظروف الجوية على الأنشطة الخارجية وتؤدي إلى تأخير المشروع",
                "probability": "متوسطة",
                "impact": "متوسط",
                "mitigation": [
                    "تضمين احتياطيات زمنية للظروف الجوية",
                    "جدولة الأنشطة الخارجية في الفترات المناسبة من السنة",
                    "إعداد خطط بديلة للأنشطة المتأثرة بالظروف الجوية"
                ]
            })
        elif sector == "تقنية المعلومات":
            risks.append({
                "title": "تغيير المتطلبات",
                "description": "قد تتغير متطلبات المشروع أثناء التنفيذ مما يؤدي إلى تأخير الجدول الزمني",
                "probability": "عالية",
                "impact": "عالي",
                "mitigation": [
                    "توثيق المتطلبات بشكل دقيق والحصول على موافقة العميل",
                    "استخدام منهجية مرنة تسمح بالتكيف مع التغييرات",
                    "تضمين احتياطيات زمنية للتعامل مع تغييرات المتطلبات"
                ]
            })
        
        return risks