# الحصول على معلومات العمالة
            labor = project_data.get("labor", [])
            
            # الحصول على معلومات الخدمات
            services = project_data.get("services", [])
            
            # حساب نسبة المحتوى المحلي للمواد
            materials_local_content = self._calculate_materials_local_content(materials, sector)
            
            # حساب نسبة المحتوى المحلي للعمالة
            labor_local_content = self._calculate_labor_local_content(labor)
            
            # حساب نسبة المحتوى المحلي للخدمات
            services_local_content = self._calculate_services_local_content(services, sector)
            
            # حساب نسبة المحتوى المحلي الإجمالية
            total_local_content = self._calculate_total_local_content(
                materials_local_content,
                labor_local_content,
                services_local_content,
                sector
            )
            
            # تحديد النسبة المستهدفة للمحتوى المحلي
            target_local_content = self._get_target_local_content(sector)
            
            # تقييم الامتثال
            compliance_status = "مستوفي" if total_local_content >= target_local_content else "غير مستوفي"
            
            # إعداد النتائج
            results = {
                "total_local_content": total_local_content,
                "target_local_content": target_local_content,
                "compliance_status": compliance_status,
                "materials_local_content": materials_local_content,
                "labor_local_content": labor_local_content,
                "services_local_content": services_local_content,
                "details": {
                    "materials": self._get_materials_details(materials),
                    "labor": self._get_labor_details(labor),
                    "services": self._get_services_details(services)
                },
                "recommendations": self._generate_recommendations(
                    total_local_content,
                    target_local_content,
                    materials_local_content,
                    labor_local_content,
                    services_local_content,
                    sector
                )
            }
            
            logger.info(f"اكتمل حساب نسب المحتوى المحلي: إجمالي {total_local_content:.1f}%، مستهدف {target_local_content:.1f}%")
            return results
            
        except Exception as e:
            logger.error(f"فشل في حساب نسب المحتوى المحلي: {str(e)}")
            return {
                "total_local_content": 0,
                "target_local_content": 0,
                "compliance_status": "غير مستوفي",
                "materials_local_content": 0,
                "labor_local_content": 0,
                "services_local_content": 0,
                "details": {},
                "recommendations": [],
                "error": str(e)
            }
    
    def _calculate_materials_local_content(self, materials: List[Dict[str, Any]], sector: str) -> float:
        """
        حساب نسبة المحتوى المحلي للمواد
        
        المعاملات:
        ----------
        materials : List[Dict[str, Any]]
            قائمة المواد
        sector : str
            القطاع
            
        المخرجات:
        --------
        float
            نسبة المحتوى المحلي للمواد
        """
        if not materials:
            return 0.0
        
        total_cost = 0.0
        local_cost = 0.0
        
        for material in materials:
            cost = material.get("cost", 0)
            local_percentage = material.get("local_percentage", 0)
            
            total_cost += cost
            local_cost += cost * (local_percentage / 100)
        
        if total_cost == 0:
            return 0.0
        
        # تطبيق المعاملات حسب القطاع
        sector_weight = self.calculation_rules.get("sector_weights", {}).get(sector, {}).get("materials", 1.0)
        
        local_content = (local_cost / total_cost) * 100 * sector_weight
        return min(100.0, local_content)
    
    def _calculate_labor_local_content(self, labor: List[Dict[str, Any]]) -> float:
        """
        حساب نسبة المحتوى المحلي للعمالة
        
        المعاملات:
        ----------
        labor : List[Dict[str, Any]]
            قائمة العمالة
            
        المخرجات:
        --------
        float
            نسبة المحتوى المحلي للعمالة
        """
        if not labor:
            return 0.0
        
        total_cost = 0.0
        local_cost = 0.0
        
        for worker in labor:
            cost = worker.get("cost", 0)
            is_saudi = worker.get("is_saudi", False)
            
            total_cost += cost
            if is_saudi:
                local_cost += cost
        
        if total_cost == 0:
            return 0.0
        
        local_content = (local_cost / total_cost) * 100
        return min(100.0, local_content)
    
    def _calculate_services_local_content(self, services: List[Dict[str, Any]], sector: str) -> float:
        """
        حساب نسبة المحتوى المحلي للخدمات
        
        المعاملات:
        ----------
        services : List[Dict[str, Any]]
            قائمة الخدمات
        sector : str
            القطاع
            
        المخرجات:
        --------
        float
            نسبة المحتوى المحلي للخدمات
        """
        if not services:
            return 0.0
        
        total_cost = 0.0
        local_cost = 0.0
        
        for service in services:
            cost = service.get("cost", 0)
            local_percentage = service.get("local_percentage", 0)
            
            total_cost += cost
            local_cost += cost * (local_percentage / 100)
        
        if total_cost == 0:
            return 0.0
        
        # تطبيق المعاملات حسب القطاع
        sector_weight = self.calculation_rules.get("sector_weights", {}).get(sector, {}).get("services", 1.0)
        
        local_content = (local_cost / total_cost) * 100 * sector_weight
        return min(100.0, local_content)
    
    def _calculate_total_local_content(self, materials_local_content: float,
                                      labor_local_content: float,
                                      services_local_content: float,
                                      sector: str) -> float:
        """
        حساب نسبة المحتوى المحلي الإجمالية
        
        المعاملات:
        ----------
        materials_local_content : float
            نسبة المحتوى المحلي للمواد
        labor_local_content : float
            نسبة المحتوى المحلي للعمالة
        services_local_content : float
            نسبة المحتوى المحلي للخدمات
        sector : str
            القطاع
            
        المخرجات:
        --------
        float
            نسبة المحتوى المحلي الإجمالية
        """
        # الحصول على أوزان القطاع
        sector_weights = self.calculation_rules.get("sector_weights", {}).get(sector, {})
        
        materials_weight = sector_weights.get("materials_weight", 0.5)
        labor_weight = sector_weights.get("labor_weight", 0.3)
        services_weight = sector_weights.get("services_weight", 0.2)
        
        # حساب المتوسط المرجح
        total_local_content = (
            materials_local_content * materials_weight +
            labor_local_content * labor_weight +
            services_local_content * services_weight
        )
        
        return min(100.0, total_local_content)
    
    def _get_target_local_content(self, sector: str) -> float:
        """
        تحديد النسبة المستهدفة للمحتوى المحلي
        
        المعاملات:
        ----------
        sector : str
            القطاع
            
        المخرجات:
        --------
        float
            النسبة المستهدفة للمحتوى المحلي
        """
        # الحصول على النسبة المستهدفة حسب القطاع
        sector_targets = self.calculation_rules.get("sector_targets", {})
        
        target = sector_targets.get(sector, 0.0)
        if target > 0:
            return target
        
        # إذا لم يكن هناك هدف محدد للقطاع، استخدم الهدف الافتراضي
        return self.calculation_rules.get("default_target", 30.0)
    
    def _get_materials_details(self, materials: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        الحصول على تفاصيل المواد
        
        المعاملات:
        ----------
        materials : List[Dict[str, Any]]
            قائمة المواد
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            تفاصيل المواد
        """
        details = []
        
        for material in materials:
            details.append({
                "name": material.get("name", ""),
                "cost": material.get("cost", 0),
                "local_percentage": material.get("local_percentage", 0),
                "local_amount": material.get("cost", 0) * material.get("local_percentage", 0) / 100,
                "manufacturer": material.get("manufacturer", ""),
                "country_of_origin": material.get("country_of_origin", "")
            })
        
        return details
    
    def _get_labor_details(self, labor: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        الحصول على تفاصيل العمالة
        
        المعاملات:
        ----------
        labor : List[Dict[str, Any]]
            قائمة العمالة
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            تفاصيل العمالة
        """
        details = []
        
        for worker in labor:
            details.append({
                "position": worker.get("position", ""),
                "cost": worker.get("cost", 0),
                "is_saudi": worker.get("is_saudi", False),
                "local_amount": worker.get("cost", 0) if worker.get("is_saudi", False) else 0,
                "qualification": worker.get("qualification", ""),
                "experience": worker.get("experience", "")
            })
        
        return details
    
    def _get_services_details(self, services: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        الحصول على تفاصيل الخدمات
        
        المعاملات:
        ----------
        services : List[Dict[str, Any]]
            قائمة الخدمات
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            تفاصيل الخدمات
        """
        details = []
        
        for service in services:
            details.append({
                "name": service.get("name", ""),
                "cost": service.get("cost", 0),
                "local_percentage": service.get("local_percentage", 0),
                "local_amount": service.get("cost", 0) * service.get("local_percentage", 0) / 100,
                "provider": service.get("provider", ""),
                "description": service.get("description", "")
            })
        
        return details
    
    def _generate_recommendations(self, total_local_content: float,
                                target_local_content: float,
                                materials_local_content: float,
                                labor_local_content: float,
                                services_local_content: float,
                                sector: str) -> List[str]:
        """
        إنشاء توصيات لتحسين نسبة المحتوى المحلي
        
        المعاملات:
        ----------
        total_local_content : float
            نسبة المحتوى المحلي الإجمالية
        target_local_content : float
            النسبة المستهدفة للمحتوى المحلي
        materials_local_content : float
            نسبة المحتوى المحلي للمواد
        labor_local_content : float
            نسبة المحتوى المحلي للعمالة
        services_local_content : float
            نسبة المحتوى المحلي للخدمات
        sector : str
            القطاع
            
        المخرجات:
        --------
        List[str]
            قائمة التوصيات
        """
        recommendations = []
        
        # التحقق مما إذا كانت النسبة الإجمالية تلبي الهدف
        if total_local_content < target_local_content:
            gap = target_local_content - total_local_content
            recommendations.append(f"زيادة نسبة المحتوى المحلي الإجمالية بمقدار {gap:.1f}% لتلبية الهدف المطلوب.")
            
            # تحديد أي المكونات تحتاج إلى تحسين
            sector_weights = self.calculation_rules.get("sector_weights", {}).get(sector, {})
            materials_weight = sector_weights.get("materials_weight", 0.5)
            labor_weight = sector_weights.get("labor_weight", 0.3)
            services_weight = sector_weights.get("services_weight", 0.2)
            
            # تقييم المكونات
            component_gaps = [
                ("المواد", materials_local_content, materials_weight),
                ("العمالة", labor_local_content, labor_weight),
                ("الخدمات", services_local_content, services_weight)
            ]
            
            # ترتيب المكونات حسب الفجوة المرجحة (أكبر فجوة في المساهمة)
            component_gaps.sort(key=lambda x: (100 - x[1]) * x[2], reverse=True)
            
            # إضافة توصيات محددة للمكونات ذات الأولوية
            for component, content, weight in component_gaps:
                if component == "المواد" and content < 70:
                    recommendations.append(f"زيادة نسبة المحتوى المحلي للمواد من {content:.1f}% إلى ما لا يقل عن 70% من خلال:")
                    recommendations.append("  - البحث عن موردين محليين للمواد الأساسية")
                    recommendations.append("  - استبدال المواد المستوردة ببدائل محلية الصنع")
                    recommendations.append("  - التعاون مع المصنعين المحليين لتطوير المنتجات المطلوبة")
                
                elif component == "العمالة" and content < 60:
                    recommendations.append(f"زيادة نسبة المحتوى المحلي للعمالة من {content:.1f}% إلى ما لا يقل عن 60% من خلال:")
                    recommendations.append("  - توظيف المزيد من الكوادر السعودية")
                    recommendations.append("  - تدريب وتأهيل الكوادر الوطنية للوظائف الفنية")
                    recommendations.append("  - الاستفادة من برامج دعم التوظيف المقدمة من هدف وصندوق تنمية الموارد البشرية")
                
                elif component == "الخدمات" and content < 50:
                    recommendations.append(f"زيادة نسبة المحتوى المحلي للخدمات من {content:.1f}% إلى ما لا يقل عن 50% من خلال:")
                    recommendations.append("  - التعاقد مع شركات خدمات محلية")
                    recommendations.append("  - الاستعانة بمكاتب استشارية سعودية")
                    recommendations.append("  - تطوير القدرات المحلية في مجالات الخدمات المتخصصة")
        
        else:
            recommendations.append(f"نسبة المحتوى المحلي الحالية ({total_local_content:.1f}%) تلبي الهدف المطلوب ({target_local_content:.1f}%).")
            recommendations.append("للحفاظ على هذا المستوى وتحسينه:")
            recommendations.append("  - توثيق مصادر المواد والخدمات المحلية بشكل دقيق")
            recommendations.append("  - مراجعة خطة المحتوى المحلي بانتظام")
            recommendations.append("  - بناء علاقات طويلة الأمد مع الموردين المحليين")
        
        # توصيات عامة
        recommendations.append("\nتوصيات عامة لتعزيز المحتوى المحلي:")
        recommendations.append("  - الاستفادة من برامج ومبادرات هيئة المحتوى المحلي وتنمية القطاع الخاص")
        recommendations.append("  - المشاركة في المعارض والفعاليات المحلية للتعرف على الموردين المحليين")
        recommendations.append("  - الاستثمار في نقل التقنية وتوطينها")
        recommendations.append("  - تطوير قاعدة بيانات للموردين المحليين وتحديثها بانتظام")
        
        return recommendations
    
    def _load_calculation_rules(self) -> Dict[str, Any]:
        """
        تحميل قواعد حساب المحتوى المحلي
        
        المخرجات:
        --------
        Dict[str, Any]
            قواعد حساب المحتوى المحلي
        """
        try:
            file_path = 'data/templates/local_content_calculation_rules.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"ملف قواعد حساب المحتوى المحلي غير موجود: {file_path}")
                # إنشاء قواعد افتراضية
                return self._create_default_calculation_rules()
        except Exception as e:
            logger.error(f"فشل في تحميل قواعد حساب المحتوى المحلي: {str(e)}")
            return self._create_default_calculation_rules()
    
    def _create_default_calculation_rules(self) -> Dict[str, Any]:
        """
        إنشاء قواعد حساب المحتوى المحلي الافتراضية
        
        المخرجات:
        --------
        Dict[str, Any]
            قواعد حساب المحتوى المحلي الافتراضية
        """
        return {
            "default_target": 30.0,
            "sector_targets": {
                "oil_and_gas": 40.0,
                "petrochemicals": 35.0,
                "energy": 35.0,
                "water": 25.0,
                "construction": 20.0,
                "infrastructure": 25.0,
                "transportation": 30.0,
                "telecommunications": 20.0,
                "healthcare": 25.0,
                "education": 35.0,
                "tourism": 30.0,
                "military": 50.0,
                "industrial": 35.0,
                "commercial": 25.0,
                "residential": 20.0,
                "general": 30.0
            },
            "sector_weights": {
                "oil_and_gas": {
                    "materials_weight": 0.6,
                    "labor_weight": 0.25,
                    "services_weight": 0.15,
                    "materials": 1.1,
                    "services": 0.9
                },
                "construction": {
                    "materials_weight": 0.5,
                    "labor_weight": 0.35,
                    "services_weight": 0.15,
                    "materials": 1.0,
                    "services": 1.0
                },
                "infrastructure": {
                    "materials_weight": 0.55,
                    "labor_weight": 0.3,
                    "services_weight": 0.15,
                    "materials": 1.0,
                    "services": 1.0
                },
                "telecommunications": {
                    "materials_weight": 0.4,
                    "labor_weight": 0.3,
                    "services_weight": 0.3,
                    "materials": 0.9,
                    "services": 1.1
                },
                "healthcare": {
                    "materials_weight": 0.4,
                    "labor_weight": 0.4,
                    "services_weight": 0.2,
                    "materials": 0.9,
                """
حاسبة نسب المحتوى المحلي
تقوم بحساب نسب المحتوى المحلي وفقًا للوائح هيئة المحتوى المحلي وتنمية القطاع الخاص
"""

import logging
import json
import os
from typing import Dict, List, Any, Tuple, Optional, Union

logger = logging.getLogger(__name__)

class LocalContentCalculator:
    """
    حاسبة نسب المحتوى المحلي
    """
    
    def __init__(self, config=None):
        """
        تهيئة حاسبة المحتوى المحلي
        
        المعاملات:
        ----------
        config : Dict, optional
            إعدادات الحاسبة
        """
        self.config = config or {}
        
        # تحميل قواعد حساب المحتوى المحلي
        self.calculation_rules = self._load_calculation_rules()
        
        logger.info("تم تهيئة حاسبة المحتوى المحلي")
    
    def calculate(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        حساب نسب المحتوى المحلي للمشروع
        
        المعاملات:
        ----------
        project_data : Dict[str, Any]
            بيانات المشروع
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج حساب المحتوى المحلي
        """
        try:
            logger.info("بدء حساب نسب المحتوى المحلي")
            
            # الحصول على معلومات القطاع
            sector = project_data.get("sector", "general")
            
            # الحصول على معلومات المواد
            materials = project_data.get("materials", [])