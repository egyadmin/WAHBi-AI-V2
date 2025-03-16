"""
مخطط المشتريات
يقوم بإعداد خطة المشتريات الأمثل بناءً على متطلبات المشروع وقاعدة بيانات الموردين
"""

import logging
import datetime
from typing import Dict, List, Any, Tuple, Optional, Union
from collections import defaultdict

logger = logging.getLogger(__name__)

class ProcurementPlanner:
    """
    مخطط المشتريات
    """
    
    def __init__(self, suppliers_db, config=None):
        """
        تهيئة مخطط المشتريات
        
        المعاملات:
        ----------
        suppliers_db : SuppliersDatabase
            قاعدة بيانات الموردين
        config : Dict, optional
            إعدادات مخطط المشتريات
        """
        self.config = config or {}
        self.suppliers_db = suppliers_db
        
        logger.info("تم تهيئة مخطط المشتريات")
    
    def generate_plan(self, local_content_data: Dict[str, Any], 
                     suppliers_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        إعداد خطة المشتريات
        
        المعاملات:
        ----------
        local_content_data : Dict[str, Any]
            بيانات المحتوى المحلي
        suppliers_data : Dict[str, Any]
            بيانات الموردين
            
        المخرجات:
        --------
        Dict[str, Any]
            خطة المشتريات
        """
        try:
            logger.info("بدء إعداد خطة المشتريات")
            
            # استخراج المواد المطلوبة
            required_materials = local_content_data.get("required_materials", [])
            
            # استخراج الموردين المحليين
            local_suppliers = suppliers_data.get("local_suppliers", [])
            
            # إعداد خطة المشتريات
            procurement_plan = self._prepare_procurement_plan(required_materials, local_suppliers)
            
            # حساب المؤشرات الرئيسية
            stats = self._calculate_procurement_stats(procurement_plan)
            
            # إضافة استراتيجية المشتريات
            procurement_strategy = self._generate_procurement_strategy(
                procurement_plan, 
                local_content_data.get("estimated_local_content", 0),
                local_content_data.get("required_local_content", 0)
            )
            
            # إعداد النتائج
            results = {
                "items": procurement_plan,
                "stats": stats,
                "procurement_strategy": procurement_strategy
            }
            
            logger.info(f"اكتملت خطة المشتريات: {len(procurement_plan)} عنصر")
            return results
            
        except Exception as e:
            logger.error(f"فشل في إعداد خطة المشتريات: {str(e)}")
            return {
                "items": [],
                "stats": {},
                "procurement_strategy": {},
                "error": str(e)
            }
    
    def _prepare_procurement_plan(self, required_materials: List[Dict[str, Any]], 
                                local_suppliers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        إعداد خطة المشتريات التفصيلية
        
        المعاملات:
        ----------
        required_materials : List[Dict[str, Any]]
            المواد المطلوبة
        local_suppliers : List[Dict[str, Any]]
            الموردين المحليين
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            خطة المشتريات
        """
        procurement_items = []
        
        # تاريخ البدء الافتراضي (اليوم)
        start_date = datetime.datetime.now()
        
        # معالجة كل مادة
        for material in required_materials:
            material_name = material.get("name", "")
            if not material_name:
                continue
            
            # البحث عن الموردين لهذه المادة
            material_suppliers = []
            for supplier in local_suppliers:
                if material_name in supplier.get("materials", []):
                    material_suppliers.append(supplier)
            
            # تحديد مصدر التوريد
            if material_suppliers:
                # المورد المحلي الأكثر موثوقية
                supplier = max(material_suppliers, key=lambda s: s.get("reliability", 0))
                source_type = "local"
                source_name = supplier.get("name", "")
                source_region = supplier.get("region", "")
                lead_time = self._estimate_lead_time(source_region)
                estimated_cost = self._estimate_cost(material, source_type)
            else:
                # توريد من الخارج
                source_type = "import"
                source_name = "مورد خارجي"
                source_region = "دولي"
                lead_time = 60  # تقدير افتراضي: 60 يوم
                estimated_cost = self._estimate_cost(material, source_type)
            
            # تحديد تاريخ التوريد
            delivery_date = start_date + datetime.timedelta(days=lead_time)
            
            # إعداد عنصر المشتريات
            item = {
                "material": material_name,
                "quantity": material.get("quantity", 0),
                "unit": material.get("unit", ""),
                "source_type": source_type,
                "supplier": source_name,
                "region": source_region,
                "lead_time": lead_time,
                "delivery_date": delivery_date.strftime("%Y-%m-%d"),
                "estimated_cost": estimated_cost,
                "local_content_contribution": 100 if source_type == "local" else 0,
                "status": "planned"
            }
            
            procurement_items.append(item)
        
        # ترتيب العناصر حسب تاريخ التوريد
        procurement_items.sort(key=lambda x: x.get("delivery_date", ""))
        
        return procurement_items
    
    def _estimate_lead_time(self, region: str) -> int:
        """
        تقدير وقت التوريد بناءً على المنطقة
        
        المعاملات:
        ----------
        region : str
            المنطقة
            
        المخرجات:
        --------
        int
            وقت التوريد المقدر (بالأيام)
        """
        # قيم افتراضية للمناطق المختلفة
        lead_times = {
            "الرياض": 7,
            "جدة": 10,
            "الدمام": 10,
            "مكة المكرمة": 12,
            "المدينة المنورة": 14,
            "القصيم": 14,
            "حائل": 15,
            "تبوك": 16,
            "عسير": 16,
            "الباحة": 18,
            "جازان": 18,
            "نجران": 20
        }
        
        return lead_times.get(region, 15)  # قيمة افتراضية: 15 يوم
    
    def _estimate_cost(self, material: Dict[str, Any], source_type: str) -> float:
        """
        تقدير تكلفة المادة
        
        المعاملات:
        ----------
        material : Dict[str, Any]
            معلومات المادة
        source_type : str
            نوع المصدر (محلي أو استيراد)
            
        المخرجات:
        --------
        float
            التكلفة المقدرة
        """
        # قيم افتراضية
        base_cost = 1000.0
        
        # تعديل التكلفة بناءً على الكمية
        quantity = float(material.get("quantity", 1))
        if quantity <= 0:
            quantity = 1
        
        cost = base_cost * quantity
        
        # تعديل التكلفة بناءً على المصدر
        if source_type == "import":
            # زيادة التكلفة بنسبة 30% للاستيراد
            cost *= 1.3
        
        return cost
    
    def _calculate_procurement_stats(self, procurement_plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        حساب إحصائيات خطة المشتريات
        
        المعاملات:
        ----------
        procurement_plan : List[Dict[str, Any]]
            خطة المشتريات
            
        المخرجات:
        --------
        Dict[str, Any]
            إحصائيات خطة المشتريات
        """
        stats = {}
        
        # إجمالي العناصر
        stats["total_items"] = len(procurement_plan)
        
        # العناصر المحلية والمستوردة
        local_items = [item for item in procurement_plan if item.get("source_type") == "local"]
        import_items = [item for item in procurement_plan if item.get("source_type") == "import"]
        
        stats["local_items_count"] = len(local_items)
        stats["import_items_count"] = len(import_items)
        
        # نسبة المحتوى المحلي
        if procurement_plan:
            stats["local_content_percentage"] = (len(local_items) / len(procurement_plan)) * 100
        else:
            stats["local_content_percentage"] = 0
        
        # إجمالي التكلفة
        total_cost = sum(item.get("estimated_cost", 0) for item in procurement_plan)
        local_cost = sum(item.get("estimated_cost", 0) for item in local_items)
        import_cost = sum(item.get("estimated_cost", 0) for item in import_items)
        
        stats["total_cost"] = total_cost
        stats["local_cost"] = local_cost
        stats["import_cost"] = import_cost
        
        # نسبة تكلفة المحتوى المحلي
        if total_cost > 0:
            stats["local_cost_percentage"] = (local_cost / total_cost) * 100
        else:
            stats["local_cost_percentage"] = 0
        
        # متوسط وقت التوريد
        if procurement_plan:
            avg_lead_time = sum(item.get("lead_time", 0) for item in procurement_plan) / len(procurement_plan)
            stats["average_lead_time"] = avg_lead_time
        else:
            stats["average_lead_time"] = 0
        
        # توزيع الموردين حسب المنطقة
        region_counts = defaultdict(int)
        for item in procurement_plan:
            if item.get("source_type") == "local":
                region = item.get("region", "غير محدد")
                region_counts[region] += 1
        
        stats["region_distribution"] = dict(region_counts)
        
        return stats
    
    def _generate_procurement_strategy(self, procurement_plan: List[Dict[str, Any]],
                                     estimated_local_content: float,
                                     required_local_content: float) -> Dict[str, Any]:
        """
        إعداد استراتيجية المشتريات
        
        المعاملات:
        ----------
        procurement_plan : List[Dict[str, Any]]
            خطة المشتريات
        estimated_local_content : float
            نسبة المحتوى المحلي المقدرة
        required_local_content : float
            نسبة المحتوى المحلي المطلوبة
            
        المخرجات:
        --------
        Dict[str, Any]
            استراتيجية المشتريات
        """
        strategy = {}
        
        # تحديد النهج العام
        if estimated_local_content >= required_local_content:
            strategy["approach"] = "استراتيجية المشتريات المحلية"
            strategy["description"] = "التركيز على الموردين المحليين لتعزيز المحتوى المحلي والحفاظ على الميزة التنافسية."
        else:
            strategy["approach"] = "استراتيجية تعزيز المحتوى المحلي"
            strategy["description"] = "زيادة الاعتماد على الموردين المحليين واستبدال العناصر المستوردة تدريجياً بمنتجات محلية."
        
        # تحديد الجدول الزمني
        if procurement_plan:
            earliest_date = min(item.get("delivery_date", "2099-12-31") for item in procurement_plan)
            latest_date = max(item.get("delivery_date", "2000-01-01") for item in procurement_plan)
            
            strategy["timeline"] = {
                "start_date": earliest_date,
                "end_date": latest_date,
                "critical_path": self._identify_critical_path(procurement_plan)
            }
        else:
            strategy["timeline"] = {
                "start_date": "غير محدد",
                "end_date": "غير محدد",
                "critical_path": []
            }
        
        # الاعتبارات الرئيسية
        strategy["key_considerations"] = [
            "ضمان الامتثال لمتطلبات المحتوى المحلي",
            "تقليل مخاطر سلسلة الإمداد وتنويع مصادر التوريد",
            "تحسين كفاءة التكلفة والجودة",
            "بناء علاقات طويلة الأمد مع الموردين الرئيسيين"
        ]
        
        # خطة عمل محددة
        strategy["action_plan"] = []
        
        # التعامل مع العناصر المستوردة
        import_items = [item for item in procurement_plan if item.get("source_type") == "import"]
        if import_items:
            strategy["action_plan"].append(
                "البحث عن موردين محليين بديلين للعناصر المستوردة (" + 
                ", ".join([item.get("material", "") for item in import_items[:3]]) +
                (f" وغيرها من {len(import_items) - 3} عناصر" if len(import_items) > 3 else "") +
                ")"
            )
        
        # تحسين أوقات التوريد الطويلة
        long_lead_items = [item for item in procurement_plan if item.get("lead_time", 0) > 30]
        if long_lead_items:
            strategy["action_plan"].append(
                "تقليل أوقات التوريد الطويلة للعناصر الحرجة (" + 
                ", ".join([item.get("material", "") for item in long_lead_items[:3]]) +
                (f" وغيرها من {len(long_lead_items) - 3} عناصر" if len(long_lead_items) > 3 else "") +
                ")"
            )
        
        # التعامل مع العناصر عالية التكلفة
        if procurement_plan:
            avg_cost = sum(item.get("estimated_cost", 0) for item in procurement_plan) / len(procurement_plan)
            high_cost_items = [item for item in procurement_plan if item.get("estimated_cost", 0) > avg_cost * 2]
            
            if high_cost_items:
                strategy["action_plan"].append(
                    "تحليل بدائل خفض التكلفة للعناصر عالية التكلفة (" + 
                    ", ".join([item.get("material", "") for item in high_cost_items[:3]]) +
                    (f" وغيرها من {len(high_cost_items) - 3} عناصر" if len(high_cost_items) > 3 else "") +
                    ")"
                )
        
        # إضافة إجراءات عامة
        strategy["action_plan"].extend([
            "توحيد الطلبات من نفس المورد لتحقيق وفورات الحجم",
            "إعداد خطة طوارئ للموردين الرئيسيين",
            "تطوير نظام لتقييم أداء الموردين",
            "توثيق عمليات الشراء وإنشاء قاعدة بيانات سعرية"
        ])
        
        return strategy
    
    def _identify_critical_path(self, procurement_plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        تحديد المسار الحرج في خطة المشتريات
        
        المعاملات:
        ----------
        procurement_plan : List[Dict[str, Any]]
            خطة المشتريات
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            المسار الحرج
        """
        # تحديد العناصر الحرجة (أطول وقت توريد، أعلى تكلفة، عناصر مستوردة)
        if not procurement_plan:
            return []
        
        # ترتيب العناصر حسب وقت التوريد
        lead_time_sorted = sorted(procurement_plan, key=lambda x: x.get("lead_time", 0), reverse=True)
        
        # أخذ أطول 3 عناصر من حيث وقت التوريد
        critical_items = lead_time_sorted[:3]
        
        # ترتيب العناصر حسب التكلفة
        cost_sorted = sorted(procurement_plan, key=lambda x: x.get("estimated_cost", 0), reverse=True)
        
        # إضافة أعلى 2 عناصر من حيث التكلفة إذا لم تكن موجودة بالفعل
        for item in cost_sorted[:2]:
            if not any(critical.get("material") == item.get("material") for critical in critical_items):
                critical_items.append(item)
        
        return [
            {
                "material": item.get("material", ""),
                "supplier": item.get("supplier", ""),
                "lead_time": item.get("lead_time", 0),
                "delivery_date": item.get("delivery_date", ""),
                "reason": "وقت توريد طويل" if item == lead_time_sorted[0] else 
                         "تكلفة عالية" if item == cost_sorted[0] else 
                         "عنصر حرج"
            }
            for item in critical_items
        ]

