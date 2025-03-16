}
    
    def calculate(self, extracted_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        حساب نسبة المحتوى المحلي بناءً على البيانات المستخرجة من المستندات
        
        المعاملات:
        ----------
        extracted_data : Dict[str, Any]
            البيانات المستخرجة من المستندات
        **kwargs : Dict[str, Any]
            معاملات إضافية مثل نوع المشروع، الميزانية، الموقع، المدة
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج حساب المحتوى المحلي
        """
        # تهيئة نتائج حساب المحتوى المحلي
        local_content_results = {
            "overall_percentage": 0.0,
            "breakdown": {},
            "requirements": [],
            "recommendations": [],
            "nitaqat_analysis": {},
        }
        
        # تحديد نوع المشروع والقطاع
        project_type = kwargs.get("project_type", "")
        sector = self._determine_sector(project_type, extracted_data)
        
        # استخراج متطلبات المحتوى المحلي من البيانات
        local_content_info = self._extract_local_content_info(extracted_data)
        
        # حساب المحتوى المحلي بناءً على القطاع
        sector_data = self.local_content_data["sectors"].get(sector, self.local_content_data["sectors"]["عام"])
        
        # تحليل القوى العاملة (الموارد البشرية)
        manpower_analysis = self._analyze_manpower(extracted_data, sector_data)
        local_content_results["breakdown"]["manpower"] = manpower_analysis["percentage"]
        
        # تحليل المواد
        materials_analysis = self._analyze_materials(extracted_data, sector_data)
        local_content_results["breakdown"]["materials"] = materials_analysis["percentage"]
        
        # تحليل الخدمات
        services_analysis = self._analyze_services(extracted_data, sector_data)
        local_content_results["breakdown"]["services"] = services_analysis["percentage"]
        
        # حساب النسبة الإجمالية للمحتوى المحلي
        weights = sector_data["weights"]
        overall_percentage = (
            weights["manpower"] * manpower_analysis["percentage"] +
            weights["materials"] * materials_analysis["percentage"] +
            weights["services"] * services_analysis["percentage"]
        )
        
        local_content_results["overall_percentage"] = round(overall_percentage, 2)
        
        # تحليل الامتثال لمتطلبات نطاقات
        nitaqat_analysis = self._analyze_nitaqat_compliance(extracted_data, sector)
        local_content_results["nitaqat_analysis"] = nitaqat_analysis
        
        # إعداد متطلبات المحتوى المحلي
        requirements = self._prepare_local_content_requirements(sector_data, local_content_info)
        local_content_results["requirements"] = requirements
        
        # إعداد توصيات لتحسين المحتوى المحلي
        recommendations = self._generate_recommendations(
            overall_percentage, 
            sector_data, 
            manpower_analysis, 
            materials_analysis, 
            services_analysis,
            nitaqat_analysis
        )
        local_content_results["recommendations"] = recommendations
        
        return local_content_results
    
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
            "تطبيقات": "تقنية المعلومات",
            "اتصالات": "الاتصالات",
            "صحة": "الصحة",
            "مستشفى": "الصحة",
            "طبي": "الصحة",
            "تعليم": "التعليم",
            "مدارس": "التعليم",
            "جامعات": "التعليم",
            "نقل": "النقل",
            "مواصلات": "النقل",
            "طاقة": "الطاقة",
            "كهرباء": "الطاقة",
            "مياه": "المياه",
            "صرف صحي": "المياه",
            "بيئة": "البيئة",
            "صناعة": "الصناعة",
            "مصانع": "الصناعة",
            "تجارة": "التجارة",
            "أسواق": "التجارة",
            "سياحة": "السياحة",
            "فنادق": "السياحة",
            "مالية": "الخدمات المالية",
            "بنوك": "الخدمات المالية"
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
            
            for sector in self.sectors:
                score = text.count(sector.lower())
                sector_scores[sector] = score
            
            # اختيار القطاع الأكثر ذكراً
            if sector_scores:
                max_sector = max(sector_scores, key=sector_scores.get)
                if sector_scores[max_sector] > 0:
                    return max_sector
        
        # القطاع الافتراضي إذا لم نتمكن من تحديده
        return "عام"
    
    def _extract_local_content_info(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        استخراج معلومات المحتوى المحلي من البيانات المستخرجة
        """
        local_content_info = {
            "mentioned_percentage": None,
            "requirements": [],
            "companies": []
        }
        
        # استخراج النسبة المذكورة للمحتوى المحلي
        if "local_content" in extracted_data and extracted_data["local_content"]:
            local_content_data = extracted_data["local_content"]
            
            # استخراج النسب المئوية
            percentages = local_content_data.get("percentages", [])
            if percentages:
                # اختيار أعلى نسبة مذكورة
                max_percentage = max(percentages, key=lambda x: x["value"])
                local_content_info["mentioned_percentage"] = max_percentage["value"]
            
            # استخراج المتطلبات
            requirements = local_content_data.get("requirements", [])
            local_content_info["requirements"] = requirements
        
        # استخراج الشركات المحلية المذكورة
        if "entities" in extracted_data and "organizations" in extracted_data["entities"]:
            organizations = extracted_data["entities"]["organizations"]
            
            for org in organizations:
                org_name = org["name"].lower()
                
                # البحث في قاعدة بيانات الشركات المحلية
                for company_id, company_data in self.local_companies.items():
                    company_name = company_data["name"].lower()
                    
                    # إذا وجدنا تطابق
                    if company_name in org_name or org_name in company_name:
                        local_content_info["companies"].append(company_data)
        
        return local_content_info
    
    def _analyze_manpower(self, extracted_data: Dict[str, Any], sector_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل المحتوى المحلي للقوى العاملة
        """
        manpower_analysis = {
            "percentage": 0.0,
            "saudi_employees": 0,
            "expat_employees": 0,
            "total_employees": 0
        }
        
        # استخراج معلومات الموظفين من البيانات
        saudi_keywords = ["سعودي", "مواطن", "توطين", "سعودة"]
        expat_keywords = ["أجنبي", "وافد", "غير سعودي"]
        
        # لدينا بعض البيانات الافتراضية للتوضيح
        saudi_count = 0
        expat_count = 0
        
        # إذا كانت هناك شركات معروفة في البيانات المستخرجة، نستخدم نسب التوطين الخاصة بها
        if "entities" in extracted_data and "organizations" in extracted_data["entities"]:
            organizations = extracted_data["entities"]["organizations"]
            
            for org in organizations:
                org_name = org["name"].lower()
                
                for company_id, company_data in self.local_companies.items():
                    company_name = company_data["name"].lower()
                    
                    if company_name in org_name or org_name in company_name:
                        saudi_percentage = company_data["saudi_employees_percentage"] / 100
                        saudi_count += 50 * saudi_percentage  # افتراض 50 موظف كمتوسط
                        expat_count += 50 * (1 - saudi_percentage)
        
        # إذا لم نجد شركات معروفة، نحاول تقدير النسب من النص
        if saudi_count == 0 and expat_count == 0 and "text" in extracted_data:
            text = extracted_data["text"].lower()
            
            # عدد مرات ذكر الموظفين السعوديين
            saudi_mentions = sum(text.count(keyword) for keyword in saudi_keywords)
            
            # عدد مرات ذكر الموظفين الأجانب
            expat_mentions = sum(text.count(keyword) for keyword in expat_keywords)
            
            # تقدير تقريبي للنسب
            total_mentions = saudi_mentions + expat_mentions
            if total_mentions > 0:
                saudi_ratio = saudi_mentions / total_mentions
                saudi_count = int(100 * saudi_ratio)
                expat_count = 100 - saudi_count
        
        # إذا لم نتمكن من تقدير النسب، نستخدم قيمة افتراضية
        if saudi_count == 0 and expat_count == 0:
            # القيمة الافتراضية بناءً على متوسط نسب التوطين في القطاع
            if "الإنشاءات" in sector_data:
                saudi_count = 25
            elif "تقنية المعلومات" in sector_data:
                saudi_count = 35
            else:
                saudi_count = 30
            
            expat_count = 100 - saudi_count
        
        # حساب النسبة المئوية للمحتوى المحلي في القوى العاملة
        total_count = saudi_count + expat_count
        
        if total_count > 0:
            manpower_analysis["saudi_employees"] = saudi_count
            manpower_analysis["expat_employees"] = expat_count
            manpower_analysis["total_employees"] = total_count
            
            # حساب النسبة المئوية باستخدام الأوزان
            manpower_percentage = (
                self.local_content_data["manpower_categories"]["saudi_employee"] * saudi_count +
                self.local_content_data["manpower_categories"]["expat_employee"] * expat_count
            ) / total_count * 100
            
            manpower_analysis["percentage"] = round(manpower_percentage, 2)
        
        return manpower_analysis
    
    def _analyze_materials(self, extracted_data: Dict[str, Any], sector_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل المحتوى المحلي للمواد
        """
        materials_analysis = {
            "percentage": 0.0,
            "local_manufacturing": 0,
            "local_assembly": 0,
            "imported_with_local_value_add": 0,
            "fully_imported": 0,
            "total_materials": 0
        }
        
        # كلمات دلالية للفئات المختلفة من المواد
        local_manufacturing_keywords = ["تصنيع محلي", "منتج محلي", "صناعة محلية", "صنع في السعودية", "منشأ سعودي"]
        local_assembly_keywords = ["تجميع محلي", "مجمع محلياً", "تم تجميعه في السعودية"]
        imported_with_local_value_keywords = ["قيمة مضافة محلية", "معالجة محلية", "قيمة محلية"]
        fully_imported_keywords = ["مستورد", "استيراد كامل", "منتج أجنبي", "صنع في الخارج"]
        
        # تقدير نسب المواد من النص
        if "text" in extracted_data:
            text = extracted_data["text"].lower()
            
            # عدد مرات ذكر كل فئة
            local_manufacturing_count = sum(text.count(keyword) for keyword in local_manufacturing_keywords)
            local_assembly_count = sum(text.count(keyword) for keyword in local_assembly_keywords)
            imported_with_local_value_count = sum(text.count(keyword) for keyword in imported_with_local_value_keywords)
            fully_imported_count = sum(text.count(keyword) for keyword in fully_imported_keywords)
            
            # إجمالي عدد المرات
            total_count = (local_manufacturing_count + local_assembly_count +
                      imported_with_local_value_count + fully_imported_count)
            
            if total_count > 0:
                materials_analysis["local_manufacturing"] = local_manufacturing_count
                materials_analysis["local_assembly"] = local_assembly_count
                materials_analysis["imported_with_local_value_add"] = imported_with_local_value_count
                materials_analysis["fully_imported"] = fully_imported_count
                materials_analysis["total_materials"] = total_count
        
        # إذا لم نتمكن من تقدير النسب، نستخدم قيم افتراضية بناءً على القطاع
        if materials_analysis["total_materials"] == 0:
            if "الإنشاءات" in sector_data:
                materials_analysis["local_manufacturing"] = 30
                materials_analysis["local_assembly"] = 20
                materials_analysis["imported_with_local_value_add"] = 15
                materials_analysis["fully_imported"] = 35
            elif "تقنية المعلومات" in sector_data:
                materials_analysis["local_manufacturing"] = 10
                materials_analysis["local_assembly"] = 25
                materials_analysis["imported_with_local_value_add"] = 15
                materials_analysis["fully_imported"] = 50
            else:
                materials_analysis["local_manufacturing"] = 20
                materials_analysis["local_assembly"] = 20
                materials_analysis["imported_with_local_value_add"] = 15
                materials_analysis["fully_imported"] = 45
                
            materials_analysis["total_materials"] = (
                materials_analysis["local_manufacturing"] +
                materials_analysis["local_assembly"] +
                materials_analysis["imported_with_local_value_add"] +
                materials_analysis["fully_imported"]
            )
        
        # حساب النسبة المئوية للمحتوى المحلي في المواد
        total_materials = materials_analysis["total_materials"]
        
        if total_materials > 0:
            material_categories = self.local_content_data["material_categories"]
            materials_percentage = (
                material_categories["local_manufacturing"] * materials_analysis["local_manufacturing"] +
                material_categories["local_assembly"] * materials_analysis["local_assembly"] +
                material_categories["imported_with_local_value_add"] * materials_analysis["imported_with_local_value_add"] +
                material_categories["fully_imported"] * materials_analysis["fully_imported"]
            ) / total_materials * 100
            
            materials_analysis["percentage"] = round(materials_percentage, 2)
        
        return materials_analysis
    
    def _analyze_services(self, extracted_data: Dict[str, Any], sector_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل المحتوى المحلي للخدمات
        """
        services_analysis = {
            "percentage": 0.0,
            "local_service_provider": 0,
            "joint_venture": 0,
            "foreign_provider_with_local_partner": 0,
            "foreign_provider": 0,
            "total_services": 0
        }
        
        # كلمات دلالية للفئات المختلفة من الخدمات
        local_provider_keywords = ["مزود خدمة محلي", "شركة محلية", "شركة سعودية", "مؤسسة محلية"]
        joint_venture_keywords = ["مشروع مشترك", "شراكة", "تحالف", "ائتلاف"]
        foreign_with_local_keywords = ["شريك محلي", "وكيل محلي", "وكيل سعودي", "تمثيل محلي"]
        foreign_provider_keywords = ["مزود خدمة أجنبي", "شركة أجنبية", "مقاول أجنبي"]
        
        # تقدير نسب الخدمات من النص
        if "text" in extracted_data:
            text = extracted_data["text"].lower()
            
            # عدد مرات ذكر كل فئة
            local_provider_count = sum(text.count(keyword) for keyword in local_provider_keywords)
            joint_venture_count = sum(text.count(keyword) for keyword in joint_venture_keywords)
            foreign_with_local_count = sum(text.count(keyword) for keyword in foreign_with_local_keywords)
            foreign_provider_count = sum(text.count(keyword) for keyword in foreign_provider_keywords)
            
            # إجمالي عدد المرات
            total_count = (local_provider_count + joint_venture_count +
                      foreign_with_local_count + foreign_provider_count)
            
            if total_count > 0:
                services_analysis["local_service_provider"] = local_provider_count
                services_analysis["joint_venture"] = joint_venture_count
                services_analysis["foreign_provider_with_local_partner"] = foreign_with_local_count
                services_analysis["foreign_provider"] = foreign_provider_count
                services_analysis["total_services"] = total_count
        
        # إذا لم نتمكن من تقدير النسب، نستخدم قيم افتراضية بناءً على القطاع
        if services_analysis["total_services"] == 0:
            if "الإنشاءات" in sector_data:
                services_analysis["local_service_provider"] = 35
                services_analysis["joint_venture"] = 25
                services_analysis["foreign_provider_with_local_partner"] = 20
                services_analysis["foreign_provider"] = 20
            elif "تقنية المعلومات" in sector_data:
                services_analysis["local_service_provider"] = 30
                services_analysis["joint_venture"] = 20
                services_analysis["foreign_provider_with_local_partner"] = 25
                services_analysis["foreign_provider"] = 25
            else:
                services_analysis["local_service_provider"] = 30
                services_analysis["joint_venture"] = 25
                services_analysis["foreign_provider_with_local_partner"] = 20
                services_analysis["foreign_provider"] = 25
                
            services_analysis["total_services"] = (
                services_analysis["local_service_provider"] +
                services_analysis["joint_venture"] +
                services_analysis["foreign_provider_with_local_partner"] +
                services_analysis["foreign_provider"]
            )
        
        # حساب النسبة المئوية للمحتوى المحلي في الخدمات
        total_services = services_analysis["total_services"]
        
        if total_services > 0:
            service_categories = self.local_content_data["service_categories"]
            services_percentage = (
                service_categories["local_service_provider"] * services_analysis["local_service_provider"] +
                service_categories["joint_venture"] * services_analysis["joint_venture"] +
                service_categories["foreign_provider_with_local_partner"] * services_analysis["foreign_provider_with_local_partner"] +
                service_categories["foreign_provider"] * services_analysis["foreign_provider"]
            ) / total_services * 100
            
            services_analysis["percentage"] = round(services_percentage, 2)
        
        return services_analysis
    
    def _analyze_nitaqat_compliance(self, extracted_data: Dict[str, Any], sector: str) -> Dict[str, Any]:
        """
        تحليل الامتثال لمتطلبات نطاقات
        """
        nitaqat_analysis = {
            "compliant": False,
            "nitaqat_category": "غير محدد",
            "company_size": "غير محدد",
            "required_saudi_percentage": 0,
            "estimated_saudi_percentage": 0
        }
        
        # تحديد حجم الشركة بناءً على القيمة التقديرية للمشروع
        project_value = 0
        if "financial_data" in extracted_data and "total_cost" in extracted_data["financial_data"]:
            project_value = extracted_data["financial_data"]["total_cost"]["value"]
        
        if project_value == 0 and "text" in extracted_data:
            # محاولة استخراج قيمة المشروع من النص
            text = extracted_data["text"].lower()
            value_patterns = [
                r'قيمة المشروع[^\d]*([\d.,]+)[^\d]*(ريال|ر\.س)',
                r'قيمة العقد[^\d]*([\d.,]+)[^\d]*(ريال|ر\.س)',
                r'القيمة الإجمالية[^\d]*([\d.,]+)[^\d]*(ريال|ر\.س)'
            ]
            
            for pattern in value_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    try:
                        project_value = float(matches[0][0].replace(',', ''))
                        break
                    except:
                        pass
        
        # تحديد حجم الشركة بناءً على قيمة المشروع
        company_size = "صغيرة"
        if project_value >= 10000000:  # أكثر من 10 مليون ريال
            company_size = "كبيرة"
        elif project_value >= 3000000:  # بين 3 و 10 مليون ريال
            company_size = "متوسطة"
        
        nitaqat_analysis["company_size"] = company_size
        
        # تحديد نسبة التوطين المطلوبة
        if sector in self.nitaqat_data and company_size in self.nitaqat_data[sector]:
            # نفترض أننا نريد الامتثال للفئة الخضراء المتوسطة
            required_percentage = (
                self.nitaqat_data[sector][company_size]["أخضر متوسط"]["min"] +
                self.nitaqat_data[sector][company_size]["أخضر متوسط"]["max"]
            ) / 2
            
            nitaqat_analysis["required_saudi_percentage"] = required_percentage
        else:
            # قيمة افتراضية
            nitaqat_analysis["required_saudi_percentage"] = 20
        
        # تقدير نسبة التوطين الفعلية
        estimated_saudi_percentage = 0
        
        # إذا كانت هناك شركات معروفة في البيانات المستخرجة، نستخدم نسبة التوطين الخاصة بها
        if "entities" in extracted_data and "organizations" in extracted_data["entities"]:
            organizations = extracted_data["entities"]["organizations"]
            
            for org in organizations:
                org_name = org["name"].lower()
                
                for company_id, company_data in self.local_companies.items():
                    company_name = company_data["name"].lower()
                    
                    if company_name in org_name or org_name in company_name:
                        estimated_saudi_percentage = company_data["saudi_employees_percentage"]
                        nitaqat_analysis["nitaqat_category"] = company_data["nitaqat_category"]
                        break
        
        # إذا لم نتمكن من تقدير النسبة، نستخدم قيمة افتراضية
        if estimated_saudi_percentage == 0:
            if "الإنشاءات" in sector:
                estimated_saudi_percentage = 15
            elif "تقنية المعلومات" in sector:
                estimated_saudi_percentage = 25
            else:
                estimated_saudi_percentage = 20
        
        nitaqat_analysis["estimated_saudi_percentage"] = estimated_saudi_percentage
        
        # تحديد فئة نطاقات والامتثال
        if sector in self.nitaqat_data and company_size in self.nitaqat_data[sector]:
            for category, range_data in self.nitaqat_data[sector][company_size].items():
                if range_data["min"] <= estimated_saudi_percentage <= range_data["max"]:
                    nitaqat_analysis["nitaqat_category"] = category
                    break
        
        # تحديد الامتثال
        nitaqat_analysis["compliant"] = (
            nitaqat_analysis["nitaqat_category"] != "أحمر" and
            estimated_saudi_percentage >= nitaqat_analysis["required_saudi_percentage"]
        )
        
        return nitaqat_analysis
    
    def _prepare_local_content_requirements(self, sector_data: Dict[str, Any], local_content_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        إعداد متطلبات المحتوى المحلي
        """
        requirements = []
        
        # الحد الأدنى للمimport os
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Union, Tuple, Optional
from datetime import datetime

class LocalContentCalculator:
    """
    فئة لحساب وتحليل المحتوى المحلي في المناقصات
    """
    
    def __init__(self):
        """
        تهيئة حاسبة المحتوى المحلي
        """
        # تحميل بيانات المحتوى المحلي
        self.local_content_data = self._load_local_content_data()
        
        # تحميل قاعدة بيانات الشركات المحلية
        self.local_companies = self._load_local_companies()
        
        # تحميل نطاقات الشركات
        self.nitaqat_data = self._load_nitaqat_data()
        
        # قائمة القطاعات
        self.sectors = [
            "الإنشاءات", "تقنية المعلومات", "الاتصالات", "الصحة",
            "التعليم", "النقل", "الطاقة", "المياه", "البيئة",
            "الصناعة", "التجارة", "السياحة", "الخدمات المالية"
        ]
    
    def _load_local_content_data(self) -> Dict[str, Any]:
        """
        تحميل بيانات المحتوى المحلي
        """
        # في التطبيق الفعلي، قد تُحمل هذه البيانات من ملف أو قاعدة بيانات
        return {
            "sectors": {
                "الإنشاءات": {
                    "min_percentage": 30,
                    "target_percentage": 60,
                    "weights": {
                        "manpower": 0.35,
                        "materials": 0.45,
                        "services": 0.2
                    }
                },
                "تقنية المعلومات": {
                    "min_percentage": 25,
                    "target_percentage": 50,
                    "weights": {
                        "manpower": 0.55,
                        "materials": 0.15,
                        "services": 0.3
                    }
                },
                "عام": {
                    "min_percentage": 20,
                    "target_percentage": 40,
                    "weights": {
                        "manpower": 0.4,
                        "materials": 0.3,
                        "services": 0.3
                    }
                }
            },
            "material_categories": {
                "local_manufacturing": 1.0,
                "local_assembly": 0.7,
                "imported_with_local_value_add": 0.4,
                "fully_imported": 0.0
            },
            "manpower_categories": {
                "saudi_employee": 1.0,
                "expat_employee": 0.0
            },
            "service_categories": {
                "local_service_provider": 1.0,
                "joint_venture": 0.6,
                "foreign_provider_with_local_partner": 0.3,
                "foreign_provider": 0.0
            }
        }
    
    def _load_local_companies(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل قاعدة بيانات الشركات المحلية
        """
        # في التطبيق الفعلي، قد تُحمل هذه البيانات من ملف أو قاعدة بيانات
        return {
            "company1": {
                "name": "شركة البناء السعودية",
                "cr_number": "1010XXXXXX",
                "sector": "الإنشاءات",
                "local_content_certificate": True,
                "saudi_employees_percentage": 35,
                "nitaqat_category": "أخضر متوسط",
                "local_content_percentage": 45
            },
            "company2": {
                "name": "شركة تقنية المستقبل",
                "cr_number": "1020XXXXXX",
                "sector": "تقنية المعلومات",
                "local_content_certificate": True,
                "saudi_employees_percentage": 42,
                "nitaqat_category": "أخضر مرتفع",
                "local_content_percentage": 52
            },
            "company3": {
                "name": "مصنع المنتجات المعدنية",
                "cr_number": "1030XXXXXX",
                "sector": "الصناعة",
                "local_content_certificate": True,
                "saudi_employees_percentage": 28,
                "nitaqat_category": "أخضر منخفض",
                "local_content_percentage": 61
            }
        }
    
    def _load_nitaqat_data(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل بيانات نطاقات الشركات
        """
        # في التطبيق الفعلي، قد تُحمل هذه البيانات من ملف أو قاعدة بيانات
        return {
            "الإنشاءات": {
                "صغيرة": {
                    "أحمر": {"min": 0, "max": 5},
                    "أخضر منخفض": {"min": 6, "max": 10},
                    "أخضر متوسط": {"min": 11, "max": 15},
                    "أخضر مرتفع": {"min": 16, "max": 25},
                    "بلاتيني": {"min": 26, "max": 100}
                },
                "متوسطة": {
                    "أحمر": {"min": 0, "max": 7},
                    "أخضر منخفض": {"min": 8, "max": 14},
                    "أخضر متوسط": {"min": 15, "max": 20},
                    "أخضر مرتفع": {"min": 21, "max": 30},
                    "بلاتيني": {"min": 31, "max": 100}
                },
                "كبيرة": {
                    "أحمر": {"min": 0, "max": 9},
                    "أخضر منخفض": {"min": 10, "max": 16},
                    "أخضر متوسط": {"min": 17, "max": 23},
                    "أخضر مرتفع": {"min": 24, "max": 35},
                    "بلاتيني": {"min": 36, "max": 100}
                }
            },
            "تقنية المعلومات": {
                "صغيرة": {
                    "أحمر": {"min": 0, "max": 6},
                    "أخضر منخفض": {"min": 7, "max": 12},
                    "أخضر متوسط": {"min": 13, "max": 19},
                    "أخضر مرتفع": {"min": 20, "max": 29},
                    "بلاتيني": {"min": 30, "max": 100}
                },
                "متوسطة": {
                    "أحمر": {"min": 0, "max": 13},
                    "أخضر منخفض": {"min": 14, "max": 20},
                    "أخضر متوسط": {"min": 21, "max": 27},
                    "أخضر مرتفع": {"min": 28, "max": 35},
                    "بلاتيني": {"min": 36, "max": 100}
                },
                "كبيرة": {
                    "أحمر": {"min": 0, "max": 17},
                    "أخضر منخفض": {"min": 18, "max": 25},
                    "أخضر متوسط": {"min": 26, "max": 33},
                    "أخضر مرتفع": {"min": 34, "max": 40},
                    "بلاتيني": {"min": 41, "max": 100}
                }
            }
        }