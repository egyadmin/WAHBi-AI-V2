import os
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Union, Tuple, Optional
from datetime import datetime

class SupplyChainAnalyzer:
    """
    فئة لتحليل سلسلة الإمداد في المناقصات
    """
    
    def __init__(self):
        """
        تهيئة محلل سلسلة الإمداد
        """
        # تحميل قاعدة بيانات الموردين
        self.suppliers_db = self._load_suppliers_database()
        
        # تحميل قاعدة بيانات المواد
        self.materials_db = self._load_materials_database()
        
        # تحميل قاعدة بيانات المخاطر
        self.risks_db = self._load_risks_database()
    
    def _load_suppliers_database(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل قاعدة بيانات الموردين
        """
        # في التطبيق الفعلي، قد تُحمل هذه البيانات من ملف أو قاعدة بيانات
        return {
            "supplier1": {
                "id": "S001",
                "name": "شركة المواد الإنشائية السعودية",
                "sector": "الإنشاءات",
                "location": "الرياض",
                "categories": ["مواد بناء", "حديد", "أسمنت", "خرسانة"],
                "local_content_percentage": 85,
                "rating": 4.5,
                "contact": {
                    "email": "info@saudiconstruction.com",
                    "phone": "+966-11-XXXXXXX",
                    "website": "www.saudiconstruction.com"
                },
                "certifications": ["ISO 9001", "شهادة المحتوى المحلي"],
                "historical_performance": {
                    "on_time_delivery": 92,
                    "quality": 90,
                    "cost": 85
                }
            },
            "supplier2": {
                "id": "S002",
                "name": "شركة التقنية السعودية",
                "sector": "تقنية المعلومات",
                "location": "جدة",
                "categories": ["أجهزة حاسب", "برمجيات", "شبكات", "أمن معلومات"],
                "local_content_percentage": 65,
                "rating": 4.2,
                "contact": {
                    "email": "info@sauditech.com",
                    "phone": "+966-12-XXXXXXX",
                    "website": "www.sauditech.com"
                },
                "certifications": ["ISO 27001", "شهادة المحتوى المحلي"],
                "historical_performance": {
                    "on_time_delivery": 88,
                    "quality": 92,
                    "cost": 80
                }
            },
            "supplier3": {
                "id": "S003",
                "name": "مصنع المعادن السعودي",
                "sector": "الصناعة",
                "location": "الدمام",
                "categories": ["معادن", "ألمنيوم", "نحاس", "فولاذ"],
                "local_content_percentage": 92,
                "rating": 4.3,
                "contact": {
                    "email": "info@saudimetal.com",
                    "phone": "+966-13-XXXXXXX",
                    "website": "www.saudimetal.com"
                },
                "certifications": ["ISO 9001", "ISO 14001", "شهادة المحتوى المحلي"],
                "historical_performance": {
                    "on_time_delivery": 90,
                    "quality": 91,
                    "cost": 82
                }
            }
        }
    
    def _load_materials_database(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل قاعدة بيانات المواد
        """
        # في التطبيق الفعلي، قد تُحمل هذه البيانات من ملف أو قاعدة بيانات
        return {
            "material1": {
                "id": "M001",
                "name": "حديد تسليح",
                "category": "مواد بناء",
                "local_manufacturers": ["مصنع المعادن السعودي", "شركة حديد الراجحي"],
                "average_price": 3000,  # ريال سعودي للطن
                "lead_time": 14,  # بالأيام
                "risk_level": "متوسط",
                "local_content_percentage": 90
            },
            "material2": {
                "id": "M002",
                "name": "أسمنت بورتلاندي",
                "category": "مواد بناء",
                "local_manufacturers": ["شركة أسمنت اليمامة", "شركة أسمنت السعودية"],
                "average_price": 15,  # ريال سعودي للكيس
                "lead_time": 7,  # بالأيام
                "risk_level": "منخفض",
                "local_content_percentage": 100
            },
            "material3": {
                "id": "M003",
                "name": "خادم حاسوبي",
                "category": "تقنية معلومات",
                "local_manufacturers": ["شركة التقنية السعودية"],
                "average_price": 15000,  # ريال سعودي للوحدة
                "lead_time": 30,  # بالأيام
                "risk_level": "عالي",
                "local_content_percentage": 60
            }
        }
    
    def _load_risks_database(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل قاعدة بيانات المخاطر
        """
        # في التطبيق الفعلي، قد تُحمل هذه البيانات من ملف أو قاعدة بيانات
        return {
            "risk1": {
                "id": "R001",
                "title": "انقطاع سلسلة التوريد",
                "description": "عدم قدرة الموردين على توفير المواد في الوقت المحدد",
                "probability": "متوسط",
                "impact": "عالي",
                "mitigation": [
                    "وجود موردين بدلاء",
                    "الاحتفاظ بمخزون استراتيجي",
                    "التعاقد طويل الأمد مع الموردين الرئيسيين"
                ],
                "sector": "عام"
            },
            "risk2": {
                "id": "R002",
                "title": "تقلبات الأسعار",
                "description": "تغيرات كبيرة في أسعار المواد الخام",
                "probability": "عالي",
                "impact": "متوسط",
                "mitigation": [
                    "تثبيت الأسعار في العقود",
                    "استخدام آليات التحوط",
                    "تنويع مصادر التوريد"
                ],
                "sector": "عام"
            },
            "risk3": {
                "id": "R003",
                "title": "عدم الامتثال للمحتوى المحلي",
                "description": "عدم قدرة الموردين على تلبية متطلبات المحتوى المحلي",
                "probability": "متوسط",
                "impact": "عالي",
                "mitigation": [
                    "اختيار موردين مؤهلين بنسبة محتوى محلي عالية",
                    "دعم الموردين المحليين لزيادة قدراتهم",
                    "تطوير برامج تأهيل للموردين المحليين"
                ],
                "sector": "عام"
            }
        }
    
    def get_suppliers_database(self) -> pd.DataFrame:
        """
        الحصول على قاعدة بيانات الموردين كـ DataFrame
        """
        suppliers_list = []
        
        for supplier_id, supplier_data in self.suppliers_db.items():
            supplier_info = {
                "id": supplier_data["id"],
                "name": supplier_data["name"],
                "sector": supplier_data["sector"],
                "location": supplier_data["location"],
                "categories": ", ".join(supplier_data["categories"]),
                "local_content_percentage": supplier_data["local_content_percentage"],
                "rating": supplier_data["rating"]
            }
            suppliers_list.append(supplier_info)
        
        return pd.DataFrame(suppliers_list)
    
    def analyze(self, extracted_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        تحليل سلسلة الإمداد بناءً على البيانات المستخرجة
        
        المعاملات:
        ----------
        extracted_data : Dict[str, Any]
            البيانات المستخرجة من المستندات
        **kwargs : Dict[str, Any]
            معاملات إضافية مثل نوع المشروع، الميزانية، الموقع، المدة
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل سلسلة الإمداد
        """
        supply_chain_results = {
            "potential_suppliers": [],
            "needed_materials": [],
            "risks": [],
            "optimization": [],
            "local_content_impact": {}
        }
        
        # تحديد نوع المشروع والقطاع
        project_type = kwargs.get("project_type", "")
        sector = self._determine_sector(project_type, extracted_data)
        
        # استخراج معلومات سلسلة الإمداد من البيانات
        supply_chain_info = self._extract_supply_chain_info(extracted_data)
        
        # تحديد المواد المطلوبة
        needed_materials = self._identify_needed_materials(extracted_data, supply_chain_info, sector)
        supply_chain_results["needed_materials"] = needed_materials
        
        # تحديد الموردين المحتملين
        potential_suppliers = self._identify_potential_suppliers(needed_materials, sector)
        supply_chain_results["potential_suppliers"] = potential_suppliers
        
        # تحليل المخاطر
        risks = self._analyze_risks(needed_materials, potential_suppliers, sector)
        supply_chain_results["risks"] = risks
        
        # اقتراحات لتحسين سلسلة الإمداد
        optimization = self._generate_optimization_suggestions(
            needed_materials, potential_suppliers, risks, sector
        )
        supply_chain_results["optimization"] = optimization
        
        # تحليل تأثير سلسلة الإمداد على المحتوى المحلي
        local_content_impact = self._analyze_local_content_impact(
            needed_materials, potential_suppliers
        )
        supply_chain_results["local_content_impact"] = local_content_impact
        
        return supply_chain_results
    
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
            "صناعة": "الصناعة",
            "مصانع": "الصناعة",
            "تجارة": "التجارة",
            "أسواق": "التجارة"
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
    
    def _extract_supply_chain_info(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        استخراج معلومات سلسلة الإمداد من البيانات المستخرجة
        """
        supply_chain_info = {
            "mentioned_suppliers": [],
            "mentioned_materials": [],
            "supply_chain_requirements": []
        }
        
        # استخراج الموردين المذكورين
        if "supply_chain" in extracted_data and "suppliers" in extracted_data["supply_chain"]:
            supply_chain_info["mentioned_suppliers"] = extracted_data["supply_chain"]["suppliers"]
        
        # استخراج المواد المذكورة
        if "supply_chain" in extracted_data and "materials" in extracted_data["supply_chain"]:
            supply_chain_info["mentioned_materials"] = extracted_data["supply_chain"]["materials"]
        
        # استخراج متطلبات سلسلة الإمداد
        if "requirements" in extracted_data:
            for req in extracted_data["requirements"]:
                if any(keyword in req.get("title", "").lower() for keyword in ["سلسلة", "إمداد", "توريد", "مورد"]):
                    supply_chain_info["supply_chain_requirements"].append(req)
                elif any(keyword in req.get("description", "").lower() for keyword in ["سلسلة", "إمداد", "توريد", "مورد"]):
                    supply_chain_info["supply_chain_requirements"].append(req)
        
        return supply_chain_info
    
    def _identify_needed_materials(self, extracted_data: Dict[str, Any], 
                            supply_chain_info: Dict[str, Any], sector: str) -> List[Dict[str, Any]]:
        """
        تحديد المواد المطلوبة للمشروع
        """
        needed_materials = []
        
        # إضافة المواد المذكورة صراحةً
        for material in supply_chain_info["mentioned_materials"]:
            material_info = {
                "name": material["name"],
                "source": "مذكور صراحةً",
                "context": material.get("context", ""),
                "quantity": "غير محدد",
                "local_availability": "غير معروف"
            }
            
            # البحث عن المادة في قاعدة البيانات
            for db_material_id, db_material in self.materials_db.items():
                if material["name"].lower() in db_material["name"].lower() or db_material["name"].lower() in material["name"].lower():
                    material_info.update({
                        "id": db_material["id"],
                        "category": db_material["category"],
                        "local_manufacturers": db_material["local_manufacturers"],
                        "average_price": db_material["average_price"],
                        "lead_time": db_material["lead_time"],
                        "risk_level": db_material["risk_level"],
                        "local_content_percentage": db_material["local_content_percentage"],
                        "local_availability": "متوفر محلياً" if db_material["local_manufacturers"] else "غير متوفر محلياً"
                    })
                    break
            
            needed_materials.append(material_info)
        
        # إضافة مواد إضافية بناءً على القطاع
        if sector == "الإنشاءات" and not any(material["name"].lower() == "حديد تسليح" for material in needed_materials):
            if "material1" in self.materials_db:
                material = self.materials_db["material1"]
                needed_materials.append({
                    "id": material["id"],
                    "name": material["name"],
                    "category": material["category"],
                    "source": "مقترح بناءً على القطاع",
                    "local_manufacturers": material["local_manufacturers"],
                    "average_price": material["average_price"],
                    "lead_time": material["lead_time"],
                    "risk_level": material["risk_level"],
                    "local_content_percentage": material["local_content_percentage"],
                    "quantity": "غير محدد",
                    "local_availability": "متوفر محلياً" if material["local_manufacturers"] else "غير متوفر محلياً"
                })
        
        if sector == "الإنشاءات" and not any(material["name"].lower() == "أسمنت" for material in needed_materials):
            if "material2" in self.materials_db:
                material = self.materials_db["material2"]
                needed_materials.append({
                    "id": material["id"],
                    "name": material["name"],
                    "category": material["category"],
                    "source": "مقترح بناءً على القطاع",
                    "local_manufacturers": material["local_manufacturers"],
                    "average_price": material["average_price"],
                    "lead_time": material["lead_time"],
                    "risk_level": material["risk_level"],
                    "local_content_percentage": material["local_content_percentage"],
                    "quantity": "غير محدد",
                    "local_availability": "متوفر محلياً" if material["local_manufacturers"] else "غير متوفر محلياً"
                })
        
        if sector == "تقنية المعلومات" and not any(material["name"].lower() == "خادم" for material in needed_materials):
            if "material3" in self.materials_db:
                material = self.materials_db["material3"]
                needed_materials.append({
                    "id": material["id"],
                    "name": material["name"],
                    "category": material["category"],
                    "source": "مقترح بناءً على القطاع",
                    "local_manufacturers": material["local_manufacturers"],
                    "average_price": material["average_price"],
                    "lead_time": material["lead_time"],
                    "risk_level": material["risk_level"],
                    "local_content_percentage": material["local_content_percentage"],
                    "quantity": "غير محدد",
                    "local_availability": "متوفر محلياً" if material["local_manufacturers"] else "غير متوفر محلياً"
                })
        
        return needed_materials
    
    def _identify_potential_suppliers(self, needed_materials: List[Dict[str, Any]], 
                                sector: str) -> List[Dict[str, Any]]:
        """
        تحديد الموردين المحتملين
        """
        potential_suppliers = []
        material_categories = set()
        
        # جمع فئات المواد المطلوبة
        for material in needed_materials:
            if "category" in material:
                material_categories.add(material["category"])
        
        # تحديد الموردين المحتملين بناءً على المواد المطلوبة والقطاع
        for supplier_id, supplier_data in self.suppliers_db.items():
            # التحقق من القطاع
            if supplier_data["sector"] == sector or supplier_data["sector"] == "عام":
                # التحقق من فئات المواد
                supplier_categories = set(supplier_data["categories"])
                
                if material_categories.intersection(supplier_categories) or not material_categories:
                    supplier_info = {
                        "id": supplier_data["id"],
                        "name": supplier_data["name"],
                        "sector": supplier_data["sector"],
                        "location": supplier_data["location"],
                        "categories": supplier_data["categories"],
                        "local_content_percentage": supplier_data["local_content_percentage"],
                        "rating": supplier_data["rating"],
                        "contact": supplier_data["contact"],
                        "certifications": supplier_data["certifications"],
                        "historical_performance": supplier_data["historical_performance"],
                        "match_score": self._calculate_supplier_match_score(supplier_data, needed_materials, sector)
                    }
                    
                    potential_suppliers.append(supplier_info)
        
        # ترتيب الموردين المحتملين بناءً على درجة التطابق
        potential_suppliers = sorted(potential_suppliers, key=lambda x: x["match_score"], reverse=True)
        
        return potential_suppliers
    
    def _calculate_supplier_match_score(self, supplier_data: Dict[str, Any], 
                                 needed_materials: List[Dict[str, Any]], sector: str) -> float:
        """
        حساب درجة تطابق المورد مع متطلبات المشروع
        """
        match_score = 0.0
        
        # درجة تطابق القطاع
        if supplier_data["sector"] == sector:
            match_score += 0.3
        elif supplier_data["sector"] == "عام":
            match_score += 0.1
        
        # درجة تطابق فئات المواد
        material_categories = set()
        for material in needed_materials:
            if "category" in material:
                material_categories.add(material["category"])
        
        supplier_categories = set(supplier_data["categories"])
        category_match_ratio = 0.0
        
        if material_categories and supplier_categories:
            common_categories = material_categories.intersection(supplier_categories)
            category_match_ratio = len(common_categories) / len(material_categories)
        
        match_score += 0.3 * category_match_ratio
        
        # درجة المحتوى المحلي
        local_content_score = min(supplier_data["local_content_percentage"] / 100, 1.0)
        match_score += 0.2 * local_content_score
        
        # درجة التقييم
        rating_score = min(supplier_data["rating"] / 5, 1.0)
        match_score += 0.1 * rating_score
        
        # درجة الأداء السابق
        if "historical_performance" in supplier_data:
            performance = supplier_data["historical_performance"]
            performance_score = (
                performance.get("on_time_delivery", 0) +
                performance.get("quality", 0) +
                performance.get("cost", 0)
            ) / 300  # تقسيم على 300 لتحويلها إلى نسبة مئوية (ثلاثة معايير بحد أقصى 100 لكل منهم)
            
            match_score += 0.1 * performance_score
        
        return round(match_score, 2)
    
    def _analyze_risks(self, needed_materials: List[Dict[str, Any]], 
                 potential_suppliers: List[Dict[str, Any]], sector: str) -> List[Dict[str, Any]]:
        """
        تحليل مخاطر سلسلة الإمداد
        """
        risks = []
        
        # إضافة المخاطر العامة
        for risk_id, risk_data in self.risks_db.items():
            if risk_data["sector"] == "عام" or risk_data["sector"] == sector:
                risks.append(risk_data)
        
        # تحليل مخاطر المواد
        high_risk_materials = [material for material in needed_materials if material.get("risk_level") == "عالي"]
        if high_risk_materials:
            material_names = [material["name"] for material in high_risk_materials]
            risks.append({
                "id": "R101",
                "title": "مواد عالية المخاطر",
                "description": f"المشروع يتطلب مواد عالية المخاطر: {', '.join(material_names)}",
                "probability": "عالي",
                "impact": "عالي",
                "mitigation": [
                    "تأمين بدائل محلية للمواد عالية المخاطر",
                    "التعاقد المسبق مع الموردين",
                    "الاحتفاظ بمخزون استراتيجي"
                ],
                "sector": sector
            })
        
        # تحليل مخاطر المواد غير المتوفرة محلياً
        non_local_materials = [material for material in needed_materials if material.get("local_availability") == "غير متوفر محلياً"]
        if non_local_materials:
            material_names = [material["name"] for material in non_local_materials]
            risks.append({
                "id": "R102",
                "title": "مواد غير متوفرة محلياً",
                "description": f"المشروع يتطلب مواد غير متوفرة محلياً: {', '.join(material_names)}",
                "probability": "متوسط",
                "impact": "عالي",
                "mitigation": [
                    "البحث عن بدائل محلية",
                    "تطوير قدرات مصنِّعين محليين",
                    "التخطيط المسبق للاستيراد"
                ],
                "sector": sector
            })
        
        # تحليل مخاطر الموردين
        if not potential_suppliers:
            risks.append({
                "id": "R103",
                "title": "عدم توفر موردين مناسبين",
                "description": "لم يتم العثور على موردين مناسبين لتلبية متطلبات المشروع",
                "probability": "عالي",
                "impact": "عالي",
                "mitigation": [
                    "توسيع نطاق البحث عن موردين",
                    "تعديل متطلبات المشروع",
                    "تطوير قدرات موردين محليين"
                ],
                "sector": sector
            })
        elif len(potential_suppliers) < 3:
            risks.append({
                "id": "R104",
                "title": "عدد محدود من الموردين",
                "description": f"عدد محدود من الموردين المناسبين: {len(potential_suppliers)}",
                "probability": "متوسط",
                "impact": "متوسط",
                "mitigation": [
                    "توسيع نطاق البحث عن موردين إضافيين",
                    "تطوير استراتيجية للتعامل مع الموردين المتاحين",
                    "النظر في خيارات بديلة"
                ],
                "sector": sector
            })
        
        # تحليل مخاطر المحتوى المحلي
        local_content_percentages = [material.get("local_content_percentage", 0) for material in needed_materials if "local_content_percentage" in material]
        if local_content_percentages:
            avg_local_content = sum(local_content_percentages) / len(local_content_percentages)
            
            if avg_local_content < 50:
                risks.append({
                    "id": "R105",
                    "title": "انخفاض نسبة المحتوى المحلي",
                    "description": f"متوسط نسبة المحتوى المحلي للمواد المطلوبة منخفض: {avg_local_content:.1f}%",
                    "probability": "عالي",
                    "impact": "عالي",
                    "mitigation": [
                        "زيادة الاعتماد على الموردين المحليين",
                        "تطوير قدرات المصنِّعين المحليين",
                        "البحث عن بدائل محلية للمواد المستوردة"
                    ],
                    "sector": sector
                })
        
        return risks
    
    def _generate_optimization_suggestions(self, needed_materials: List[Dict[str, Any]],
                                      potential_suppliers: List[Dict[str, Any]],
                                      risks: List[Dict[str, Any]], sector: str) -> List[str]:
        """
        إعداد اقتراحات لتحسين سلسلة الإمداد
        """
        optimization_suggestions = []
        
        # اقتراحات لتحسين موثوقية سلسلة الإمداد
        optimization_suggestions.append(
            "تعزيز موثوقية سلسلة الإمداد من خلال توفير مصادر بديلة للمواد الحرجة"
        )
        
        # اقتراحات لزيادة المحتوى المحلي
        local_content_percentages = [material.get("local_content_percentage", 0) for material in needed_materials if "local_content_percentage" in material]
        if local_content_percentages:
            avg_local_content = sum(local_content_percentages) / len(local_content_percentages)
            
            if avg_local_content < 70:
                optimization_suggestions.append(
                    f"زيادة نسبة المحتوى المحلي من {avg_local_content:.1f}% إلى 70% على الأقل من خلال التعاون مع موردين محليين"
                )
        
        # اقتراحات لخفض التكاليف
        optimization_suggestions.append(
            "خفض تكاليف سلسلة الإمداد من خلال التعاقد طويل الأمد مع الموردين الرئيسيين"
        )
        
        # اقتراحات لتقليل المخاطر العالية
        high_risks = [risk for risk in risks if risk.get("impact") == "عالي"]
        if high_risks:
            optimization_suggestions.append(
                f"تطوير استراتيجية للتخفيف من المخاطر العالية في سلسلة الإمداد ({len(high_risks)} مخاطر)"
            )
        
        # اقتراحات لتحسين الجودة
        optimization_suggestions.append(
            "تحسين جودة المواد من خلال اختيار موردين ذوي تقييمات عالية ومراقبة الجودة بشكل مستمر"
        )
        
        # اقتراحات خاصة بالقطاع
        if sector == "الإنشاءات":
            optimization_suggestions.append(
                "تطوير علاقات استراتيجية مع موردي مواد البناء الرئيسية (الحديد، الأسمنت، الخرسانة) لضمان استمرارية التوريد"
            )
        elif sector == "تقنية المعلومات":
            optimization_suggestions.append(
                "بناء شراكات مع الشركات التقنية المحلية لتطوير حلول مخصصة تلبي احتياجات المشروع وتزيد المحتوى المحلي"
            )
        
        # اقتراحات عامة
        optimization_suggestions.extend([
            "تطبيق نظام إدارة المخزون الأمثل (Just-in-Time) لتقليل تكاليف التخزين وزيادة الكفاءة",
            "تطوير منظومة تتبع رقمية لمراقبة سلسلة الإمداد بشكل فعال",
            "تدريب وتأهيل الموردين المحليين لتلبية متطلبات الجودة العالمية"
        ])
        
        return optimization_suggestions
    
    def _analyze_local_content_impact(self, needed_materials: List[Dict[str, Any]],
                                potential_suppliers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        تحليل تأثير سلسلة الإمداد على المحتوى المحلي
        """
        local_content_impact = {
            "overall_percentage": 0.0,
            "materials_local_content": 0.0,
            "suppliers_local_content": 0.0,
            "recommendations": []
        }
        
        # حساب متوسط نسبة المحتوى المحلي للمواد
        local_content_percentages = [material.get("local_content_percentage", 0) for material in needed_materials if "local_content_percentage" in material]
        if local_content_percentages:
            materials_local_content = sum(local_content_percentages) / len(local_content_percentages)
            local_content_impact["materials_local_content"] = round(materials_local_content, 2)
        
        # حساب متوسط نسبة المحتوى المحلي للموردين
        supplier_local_content_percentages = [supplier.get("local_content_percentage", 0) for supplier in potential_suppliers]
        if supplier_local_content_percentages:
            suppliers_local_content = sum(supplier_local_content_percentages) / len(supplier_local_content_percentages)
            local_content_impact["suppliers_local_content"] = round(suppliers_local_content, 2)
        
        # حساب النسبة الإجمالية للمحتوى المحلي
        overall_percentage = (
            local_content_impact["materials_local_content"] * 0.7 +
            local_content_impact["suppliers_local_content"] * 0.3
        )
        local_content_impact["overall_percentage"] = round(overall_percentage, 2)
        
        # إعداد توصيات لتحسين نسبة المحتوى المحلي
        if overall_percentage < 50:
            local_content_impact["recommendations"].append(
                "زيادة الاعتماد على الموردين المحليين ذوي نسبة محتوى محلي عالية"
            )
        
        if local_content_impact["materials_local_content"] < 50:
            local_content_impact["recommendations"].append(
                "البحث عن بدائل محلية للمواد المستوردة أو ذات نسبة محتوى محلي منخفضة"
            )
        
        local_content_impact["recommendations"].extend([
            "تطوير قدرات المصنِّعين المحليين لزيادة نسبة المحتوى المحلي",
            "الاستفادة من برامج دعم المحتوى المحلي المقدمة من هيئة المحتوى المحلي والمشتريات الحكومية",
            "تطبيق معايير تفضيل المنتجات المحلية في المناقصات والمشتريات"
        ])
        
        return local_content_impact