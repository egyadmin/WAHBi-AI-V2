"""
قاعدة بيانات الموردين المحليين
يوفر واجهة للوصول إلى بيانات الموردين والمنتجات المحلية
"""

import json
import logging
import os
import re
from typing import Dict, List, Any, Tuple, Optional, Union
from collections import defaultdict

logger = logging.getLogger(__name__)

class SuppliersDatabase:
    """
    قاعدة بيانات الموردين المحليين
    """
    
    def __init__(self, config=None):
        """
        تهيئة قاعدة بيانات الموردين
        
        المعاملات:
        ----------
        config : Dict, optional
            إعدادات قاعدة البيانات
        """
        self.config = config or {}
        
        # تحميل بيانات الموردين
        self.suppliers = self._load_suppliers()
        
        # تحميل بيانات المنتجات
        self.products = self._load_products()
        
        # تهيئة فهارس البحث
        self._initialize_indexes()
        
        logger.info(f"تم تهيئة قاعدة بيانات الموردين: {len(self.suppliers)} مورد")
    
    def search_suppliers(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        البحث عن الموردين
        
        المعاملات:
        ----------
        query : str
            استعلام البحث
        category : str, optional
            فئة المورد
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة الموردين المطابقين
        """
        results = []
        
        # تنظيف الاستعلام
        query = query.lower().strip()
        
        # البحث عن الموردين المطابقين
        for supplier in self.suppliers:
            # التحقق من الفئة إذا تم تحديدها
            if category and category != "الكل" and supplier.get("category") != category:
                continue
            
            # البحث في اسم المورد
            if query in supplier.get("name", "").lower():
                results.append(supplier)
                continue
            
            # البحث في المنطقة
            if query in supplier.get("region", "").lower():
                results.append(supplier)
                continue
            
            # البحث في المنتجات
            if any(query in product.lower() for product in supplier.get("products", [])):
                results.append(supplier)
                continue
        
        return results
    
    def find_matching_suppliers(self, materials: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        البحث عن الموردين المطابقين للمواد المطلوبة
        
        المعاملات:
        ----------
        materials : List[Dict[str, Any]]
            قائمة المواد المطلوبة
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج البحث
        """
        results = {
            "local_suppliers": [],
            "material_coverage": {},
            "region_distribution": {},
            "summary": {}
        }
        
        material_suppliers = {}
        all_matching_suppliers = []
        
        # البحث عن الموردين المطابقين لكل مادة
        for material in materials:
            material_name = material.get("name", "")
            if not material_name:
                continue
            
            # البحث عن المنتجات المطابقة
            matching_products = []
            for product_id, product in self.products.items():
                similarity = self._calculate_similarity(material_name, product.get("name", ""))
                if similarity > 0.7:  # عتبة التشابه
                    matching_products.append((product_id, similarity))
            
            # ترتيب المنتجات حسب التشابه
            matching_products.sort(key=lambda x: x[1], reverse=True)
            
            # البحث عن الموردين لهذه المنتجات
            suppliers_for_material = []
            for product_id, similarity in matching_products[:5]:  # أفضل 5 منتجات
                product_suppliers = self.product_suppliers.get(product_id, [])
                for supplier_id in product_suppliers:
                    supplier = next((s for s in self.suppliers if s.get("id") == supplier_id), None)
                    if supplier:
                        suppliers_for_material.append(supplier)
                        all_matching_suppliers.append(supplier)
            
            # إزالة التكرارات
            unique_suppliers = []
            supplier_ids = set()
            for supplier in suppliers_for_material:
                supplier_id = supplier.get("id")
                if supplier_id not in supplier_ids:
                    supplier_ids.add(supplier_id)
                    unique_suppliers.append(supplier)
            
            # تخزين الموردين لهذه المادة
            material_suppliers[material_name] = unique_suppliers
            
            # حساب نسبة التغطية
            coverage = min(100.0, len(unique_suppliers) * 20.0)  # كل مورد يغطي 20% بحد أقصى 100%
            results["material_coverage"][material_name] = coverage
        
        # إزالة التكرارات من قائمة الموردين
        unique_matching_suppliers = []
        supplier_ids = set()
        for supplier in all_matching_suppliers:
            supplier_id = supplier.get("id")
            if supplier_id not in supplier_ids:
                supplier_ids.add(supplier_id)
                
                # إضافة معلومات المواد التي يوفرها المورد
                supplier_materials = []
                for material_name, suppliers in material_suppliers.items():
                    if any(s.get("id") == supplier_id for s in suppliers):
                        supplier_materials.append(material_name)
                
                supplier_copy = supplier.copy()
                supplier_copy["materials"] = supplier_materials
                
                unique_matching_suppliers.append(supplier_copy)
        
        # ترتيب الموردين حسب عدد المواد وتصنيف الموثوقية
        unique_matching_suppliers.sort(
            key=lambda s: (len(s.get("materials", [])), s.get("reliability", 0)),
            reverse=True
        )
        
        # إضافة الموردين المطابقين
        results["local_suppliers"] = unique_matching_suppliers
        
        # حساب توزيع المناطق
        region_counts = defaultdict(int)
        for supplier in unique_matching_suppliers:
            region = supplier.get("region", "غير محدد")
            region_counts[region] += 1
        
        results["region_distribution"] = dict(region_counts)
        
        # إعداد ملخص
        results["summary"] = {
            "total_materials": len(materials),
            "materials_with_suppliers": len(material_suppliers),
            "total_matching_suppliers": len(unique_matching_suppliers),
            "average_coverage": sum(results["material_coverage"].values()) / max(1, len(results["material_coverage"]))
        }
        
        return results
    
    def get_total_suppliers(self) -> int:
        """
        الحصول على إجمالي عدد الموردين
        
        المخرجات:
        --------
        int
            إجمالي عدد الموردين
        """
        return len(self.suppliers)
    
    def get_total_products(self) -> int:
        """
        الحصول على إجمالي عدد المنتجات
        
        المخرجات:
        --------
        int
            إجمالي عدد المنتجات
        """
        return len(self.products)
    
    def get_covered_regions(self) -> int:
        """
        الحصول على عدد المناطق المغطاة
        
        المخرجات:
        --------
        int
            عدد المناطق المغطاة
        """
        regions = set(supplier.get("region", "") for supplier in self.suppliers if supplier.get("region"))
        return len(regions)
    
    def get_suppliers_by_region(self) -> Dict[str, int]:
        """
        الحصول على توزيع الموردين حسب المنطقة
        
        المخرجات:
        --------
        Dict[str, int]
            توزيع الموردين حسب المنطقة
        """
        region_counts = defaultdict(int)
        for supplier in self.suppliers:
            region = supplier.get("region", "غير محدد")
            region_counts[region] += 1
        
        return dict(region_counts)
    
    def get_suppliers_by_category(self) -> Dict[str, int]:
        """
        الحصول على توزيع الموردين حسب الفئة
        
        المخرجات:
        --------
        Dict[str, int]
            توزيع الموردين حسب الفئة
        """
        category_counts = defaultdict(int)
        for supplier in self.suppliers:
            category = supplier.get("category", "غير محدد")
            category_counts[category] += 1
        
        return dict(category_counts)
    
    def _load_suppliers(self) -> List[Dict[str, Any]]:
        """
        تحميل بيانات الموردين
        
        المخرجات:
        --------
        List[Dict[str, Any]]
            بيانات الموردين
        """
        try:
            file_path = 'data/templates/local_suppliers.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    suppliers = json.load(f)
                
                # إضافة معرف فريد لكل مورد إذا لم يكن موجودًا
                for i, supplier in enumerate(suppliers):
                    if "id" not in supplier:
                        supplier["id"] = f"S{i+1:04d}"
                
                return suppliers
            else:
                logger.warning(f"ملف بيانات الموردين غير موجود: {file_path}")
                # إنشاء بيانات افتراضية
                return self._create_default_suppliers()
        except Exception as e:
            logger.error(f"فشل في تحميل بيانات الموردين: {str(e)}")
            return self._create_default_suppliers()
    
    def _load_products(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل بيانات المنتجات
        
        المخرجات:
        --------
        Dict[str, Dict[str, Any]]
            بيانات المنتجات
        """
        try:
            file_path = 'data/templates/local_materials.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    materials = json.load(f)
                
                products = {}
                for i, material in enumerate(materials):
                    product_id = f"P{i+1:04d}"
                    products[product_id] = {
                        "id": product_id,
                        "name": material.get("name", ""),
                        "category": material.get("category", ""),
                        "availability_percentage": material.get("availability_percentage", 0)
                    }
                
                return products
            else:
                logger.warning(f"ملف بيانات المنتجات غير موجود: {file_path}")
                # إنشاء بيانات افتراضية
                return self._create_default_products()
        except Exception as e:
            logger.error(f"فشل في تحميل بيانات المنتجات: {str(e)}")
            return self._create_default_products()
    
    def _initialize_indexes(self):
        """
        تهيئة فهارس البحث
        """
        # إنشاء فهرس للمنتجات حسب المورد
        self.supplier_products = defaultdict(list)
        
        # إنشاء فهرس للموردين حسب المنتج
        self.product_suppliers = defaultdict(list)
        
        # ربط المنتجات بالموردين
        for supplier in self.suppliers:
            supplier_id = supplier.get("id")
            supplier_products = supplier.get("products", [])
            
            for product_name in supplier_products:
                # البحث عن المنتج المطابق
                matching_product_id = None
                best_similarity = 0
                
                for product_id, product in self.products.items():
                    similarity = self._calculate_similarity(product_name, product.get("name", ""))
                    if similarity > 0.7 and similarity > best_similarity:  # عتبة التشابه
                        best_similarity = similarity
                        matching_product_id = product_id
                
                if matching_product_id:
                    self.supplier_products[supplier_id].append(matching_product_id)
                    self.product_suppliers[matching_product_id].append(supplier_id)
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """
        حساب درجة التشابه بين سلسلتين
        
        المعاملات:
        ----------
        str1 : str
            السلسلة الأولى
        str2 : str
            السلسلة الثانية
            
        المخرجات:
        --------
        float
            درجة التشابه (0 إلى 1)
        """
        # تنظيف السلاسل
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()
        
        # تحويل السلاسل إلى مجموعات من الكلمات
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        # حساب معامل جاكارد
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def _create_default_suppliers(self) -> List[Dict[str, Any]]:
        """
        إنشاء بيانات افتراضية للموردين
        
        المخرجات:
        --------
        List[Dict[str, Any]]
            بيانات افتراضية للموردين
        """
        return [
            {
                "id": "S0001",
                "name": "شركة الراجحي للحديد",
                "region": "الرياض",
                "category": "مواد بناء",
                "products": ["حديد تسليح", "حديد مجلفن"],
                "reliability": 4.5,
                "contact": "info@siec.sa",
                "nitaqat_category": "أخضر مرتفع"
            },
            {
                "id": "S0004",
                "name": "شركة الزامل للتكييف",
                "region": "الدمام",
                "category": "تكييف",
                "products": ["وحدات تكييف", "معدات تبريد", "أجهزة تهوية"],
                "reliability": 4.8,
                "contact": "info@zamil-ac.sa",
                "nitaqat_category": "بلاتيني"
            },
            {
                "id": "S0005",
                "name": "شركة امجاد للسباكة",
                "region": "الرياض",
                "category": "سباكة",
                "products": ["أنابيب مياه", "خزانات مياه", "مواسير صرف"],
                "reliability": 3.9,
                "contact": "info@amjad-plumbing.sa",
                "nitaqat_category": "أخضر متوسط"
            },
            {
                "id": "S0006",
                "name": "مصنع الخليج للزجاج",
                "region": "جدة",
                "category": "مواد بناء",
                "products": ["زجاج", "ألواح زجاجية", "واجهات زجاجية"],
                "reliability": 4.0,
                "contact": "info@gulf-glass.sa",
                "nitaqat_category": "أخضر مرتفع"
            },
            {
                "id": "S0007",
                "name": "مؤسسة الديار للدهانات",
                "region": "الرياض",
                "category": "مواد بناء",
                "products": ["دهانات", "طلاء جدران", "عوازل"],
                "reliability": 3.7,
                "contact": "info@aldiyar-paints.sa",
                "nitaqat_category": "أخضر منخفض"
            },
            {
                "id": "S0008",
                "name": "شركة الأثاث المكتبي المتحدة",
                "region": "الرياض",
                "category": "أثاث",
                "products": ["أثاث مكتبي", "كراسي", "طاولات", "خزائن"],
                "reliability": 4.1,
                "contact": "info@united-furniture.sa",
                "nitaqat_category": "أخضر مرتفع"
            },
            {
                "id": "S0009",
                "name": "شركة ابن غنيم للنجارة",
                "region": "الدمام",
                "category": "نجارة",
                "products": ["أبواب خشبية", "نوافذ خشبية", "أثاث منزلي"],
                "reliability": 4.3,
                "contact": "info@ibnghonaim.sa",
                "nitaqat_category": "أخضر مرتفع"
            },
            {
                "id": "S0010",
                "name": "الشركة العربية للألمنيوم",
                "region": "جدة",
                "category": "ألمنيوم",
                "products": ["نوافذ ألمنيوم", "أبواب ألمنيوم", "واجهات ألمنيوم"],
                "reliability": 4.4,
                "contact": "info@arabian-aluminum.sa",
                "nitaqat_category": "بلاتيني"
            }
        ]
    
    def _create_default_products(self) -> Dict[str, Dict[str, Any]]:
        """
        إنشاء بيانات افتراضية للمنتجات
        
        المخرجات:
        --------
        Dict[str, Dict[str, Any]]
            بيانات افتراضية للمنتجات
        """
        products = {
            "P0001": {"id": "P0001", "name": "حديد تسليح", "category": "مواد بناء", "availability_percentage": 90.0},
            "P0002": {"id": "P0002", "name": "أسمنت", "category": "مواد بناء", "availability_percentage": 95.0},
            "P0003": {"id": "P0003", "name": "خرسانة جاهزة", "category": "مواد بناء", "availability_percentage": 100.0},
            "P0004": {"id": "P0004", "name": "بلاط", "category": "مواد بناء", "availability_percentage": 80.0},
            "P0005": {"id": "P0005", "name": "رخام", "category": "مواد بناء", "availability_percentage": 60.0},
            "P0006": {"id": "P0006", "name": "دهانات", "category": "مواد بناء", "availability_percentage": 75.0},
            "P0007": {"id": "P0007", "name": "زجاج", "category": "مواد بناء", "availability_percentage": 50.0},
            "P0008": {"id": "P0008", "name": "أسلاك كهربائية", "category": "كهرباء", "availability_percentage": 60.0},
            "P0009": {"id": "P0009", "name": "لوحات كهربائية", "category": "كهرباء", "availability_percentage": 55.0},
            "P0010": {"id": "P0010", "name": "مفاتيح كهربائية", "category": "كهرباء", "availability_percentage": 45.0},
            "P0011": {"id": "P0011", "name": "أنابيب مياه", "category": "سباكة", "availability_percentage": 70.0},
            "P0012": {"id": "P0012", "name": "خزانات مياه", "category": "سباكة", "availability_percentage": 95.0},
            "P0013": {"id": "P0013", "name": "مواسير صرف", "category": "سباكة", "availability_percentage": 85.0},
            "P0014": {"id": "P0014", "name": "وحدات تكييف", "category": "تكييف", "availability_percentage": 30.0},
            "P0015": {"id": "P0015", "name": "معدات تبريد", "category": "تكييف", "availability_percentage": 25.0},
            "P0016": {"id": "P0016", "name": "أجهزة تهوية", "category": "تكييف", "availability_percentage": 40.0},
            "P0017": {"id": "P0017", "name": "أثاث مكتبي", "category": "أثاث", "availability_percentage": 70.0},
            "P0018": {"id": "P0018", "name": "أثاث منزلي", "category": "أثاث", "availability_percentage": 65.0},
            "P0019": {"id": "P0019", "name": "أبواب خشبية", "category": "نجارة", "availability_percentage": 80.0},
            "P0020": {"id": "P0020", "name": "نوافذ ألمنيوم", "category": "ألمنيوم", "availability_percentage": 75.0}
        }
        
        return productsrajhi-steel.sa",
                "nitaqat_category": "بلاتيني"
            },
            {
                "id": "S0002",
                "name": "اسمنت اليمامة",
                "region": "الرياض",
                "category": "مواد بناء",
                "products": ["أسمنت", "خرسانة جاهزة"],
                "reliability": 4.7,
                "contact": "info@yamama-cement.sa",
                "nitaqat_category": "بلاتيني"
            },
            {
                "id": "S0003",
                "name": "الشركة السعودية للصناعات الكهربائية",
                "region": "جدة",
                "category": "كهرباء",
                "products": ["أسلاك كهربائية", "لوحات كهربائية", "مفاتيح كهربائية"],
                "reliability": 4.2,
                "contact": "info@