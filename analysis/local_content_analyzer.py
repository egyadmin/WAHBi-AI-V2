نسبة توفر المادة محلياً (0 إلى 100)
        """
        # البحث في قاعدة بيانات المواد المحلية
        material_name = material_name.lower()
        
        # مطابقة الاسم بالكامل
        for local_material in self.local_materials_db:
            if local_material.get('name', '').lower() == material_name:
                return local_material.get('availability_percentage', 100.0)
        
        # مطابقة جزئية
        matches = []
        for local_material in self.local_materials_db:
            local_name = local_material.get('name', '').lower()
            # حساب درجة التشابه البسيط
            similarity = self._simple_similarity(material_name, local_name)
            if similarity > 0.7:  # عتبة التشابه
                matches.append((local_material, similarity))
        
        if matches:
            # ترتيب المطابقات حسب درجة التشابه
            matches.sort(key=lambda x: x[1], reverse=True)
            return matches[0][0].get('availability_percentage', 0.0)
        
        # إذا لم يتم العثور على مطابقات، نفترض نسبة منخفضة
        return 20.0  # قيمة افتراضية منخفضة
    
    def _simple_similarity(self, str1: str, str2: str) -> float:
        """
        حساب درجة التشابه البسيط بين سلسلتين
        
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
        str1 = str1.strip().lower()
        str2 = str2.strip().lower()
        
        # تحويل السلاسل إلى مجموعات من الكلمات
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        # حساب معامل جاكارد
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def _extract_tables(self, text: str) -> List[str]:
        """
        استخراج أقسام الجداول من النص
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[str]
            قائمة بأقسام الجداول
        """
        # بحث بسيط عن أقسام الجداول
        # البحث عن أقسام تبدأ بعناوين مثل "جدول المواصفات" أو "قائمة الكميات"
        table_headers = [
            "جدول المواصفات",
            "جدول الكميات",
            "قائمة المواد",
            "قائمة الكميات",
            "جدول المنتجات",
            "المواد المطلوبة",
            "قائمة البنود",
            "بنود المناقصة"
        ]
        
        tables = []
        for header in table_headers:
            # البحث عن أقسام تبدأ بالعنوان المحدد
            matches = re.finditer(f"{header}.*?(?=\n\n|\Z)", text, re.DOTALL)
            for match in matches:
                table_section = match.group(0)
                if len(table_section.split('\n')) > 2:  # التأكد من أن القسم يحتوي على أكثر من سطرين
                    tables.append(table_section)
        
        # البحث عن أنماط الجداول (أسطر تحتوي على عدة عناصر مفصولة بـ | أو مسافات متعددة)
        table_pattern = r'(?:\n|^)((?:[^\n]+\|[^\n]+\|[^\n]+\n){3,})'
        table_matches = re.finditer(table_pattern, text)
        for match in table_matches:
            tables.append(match.group(1))
        
        return tables
    
    def _parse_table_for_materials(self, table_text: str) -> List[Dict[str, Any]]:
        """
        تحليل نص الجدول لاستخراج المواد
        
        المعاملات:
        ----------
        table_text : str
            نص الجدول
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة بالمواد المستخرجة
        """
        items = []
        
        # تقسيم الجدول إلى أسطر
        lines = table_text.strip().split('\n')
        
        # تحديد الأعمدة من السطر الأول (العناوين)
        if len(lines) < 2:
            return []
        
        # تعرف على العناوين
        headers = lines[0].strip()
        header_cols = []
        
        # البحث عن أعمدة محتملة للمواد والكميات
        name_col_idx = -1
        quantity_col_idx = -1
        unit_col_idx = -1
        
        # تقسيم العناوين إما بفواصل | أو مسافات متعددة
        if '|' in headers:
            header_cols = [col.strip() for col in headers.split('|')]
        else:
            # محاولة تقسيم بناءً على المسافات المتعددة
            header_cols = re.split(r'\s{2,}', headers)
        
        # تحديد أعمدة المواد والكميات والوحدات
        for i, col in enumerate(header_cols):
            col_lower = col.lower()
            if any(term in col_lower for term in ['اسم', 'وصف', 'البند', 'المادة', 'منتج']):
                name_col_idx = i
            elif any(term in col_lower for term in ['كمية', 'العدد']):
                quantity_col_idx = i
            elif any(term in col_lower for term in ['وحدة', 'القياس']):
                unit_col_idx = i
        
        # إذا لم نتمكن من العثور على عمود الاسم، نحاول استخدام نهج بديل
        if name_col_idx == -1:
            # افتراض أن العمود الأول يحتوي على الاسم
            name_col_idx = 0
        
        # معالجة كل سطر في الجدول (نبدأ من السطر الثاني لتخطي العناوين)
        for i in range(1, len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            
            # تقسيم السطر إلى أعمدة
            cols = []
            if '|' in line:
                cols = [col.strip() for col in line.split('|')]
            else:
                # محاولة تقسيم بناءً على المسافات المتعددة
                cols = re.split(r'\s{2,}', line)
            
            # تخطي الأسطر القصيرة جدًا
            if len(cols) < 2:
                continue
            
            # استخراج المعلومات المطلوبة
            name = cols[name_col_idx] if name_col_idx < len(cols) else ""
            
            # تنظيف الاسم
            name = re.sub(r'\d+', '', name).strip()
            
            # استخراج الكمية والوحدة إذا كانت متوفرة
            quantity = ""
            if quantity_col_idx != -1 and quantity_col_idx < len(cols):
                quantity = cols[quantity_col_idx]
                
                # محاولة تحويل الكمية إلى رقم
                try:
                    quantity = float(re.search(r'\d+(?:\.\d+)?', quantity).group(0))
                except (ValueError, AttributeError):
                    quantity = ""
            
            unit = ""
            if unit_col_idx != -1 and unit_col_idx < len(cols):
                unit = cols[unit_col_idx]
            
            # إضافة المادة إلى القائمة إذا كان الاسم غير فارغ
            if name:
                items.append({
                    "name": name,
                    "quantity": quantity,
                    "unit": unit,
                    "source": "table"
                })
        
        return items
    
    def _extract_materials_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        استخراج المواد من النص العادي
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة بالمواد المستخرجة
        """
        items = []
        
        # البحث عن قوائم بنقاط
        bullet_lists = re.findall(r'(?<=\n)(?:[-•*]\s+[^\n]+(?:\n|$))+', text)
        
        for bullet_list in bullet_lists:
            # تقسيم القائمة إلى عناصر
            list_items = re.findall(r'[-•*]\s+([^\n]+)(?:\n|$)', bullet_list)
            
            # معالجة كل عنصر
            for item in list_items:
                # البحث عن الكمية والوحدة في العنصر
                quantity_match = re.search(r'(\d+(?:\.\d+)?)\s*([كمقطعةوحدةمترطنكجم]*)', item)
                
                quantity = ""
                unit = ""
                name = item
                
                if quantity_match:
                    quantity = quantity_match.group(1)
                    unit = quantity_match.group(2)
                    # إزالة الكمية والوحدة من الاسم
                    name = item.replace(quantity_match.group(0), "").strip()
                
                # تنظيف الاسم
                name = re.sub(r'^[-\s]*', '', name)
                name = re.sub(r'[-\s]*"""
محلل المحتوى المحلي
يقوم بتحليل متطلبات المحتوى المحلي في المناقصات وتقييم نسب المحتوى المحلي
"""

import re
import json
import logging
import os
from typing import Dict, List, Any, Tuple, Optional, Union
import numpy as np

logger = logging.getLogger(__name__)

class LocalContentAnalyzer:
    """
    محلل المحتوى المحلي في المناقصات
    """
    
    def __init__(self, model_loader, config=None):
        """
        تهيئة محلل المحتوى المحلي
        
        المعاملات:
        ----------
        model_loader : ModelLoader
            محمّل النماذج المستخدمة للتحليل
        config : Dict, optional
            إعدادات المحلل
        """
        self.config = config or {}
        self.model_loader = model_loader
        
        # تحميل قوائم المنتجات والمواد المحلية
        self.local_materials_db = self._load_local_materials()
        self.local_suppliers_db = self._load_local_suppliers()
        
        # تحميل قواعد ولوائح المحتوى المحلي
        self.local_content_regulations = self._load_regulations()
        
        # تحميل نموذج تحليل النصوص إذا كان متاحاً
        self.ner_model = None
        if hasattr(model_loader, 'get_ner_model'):
            try:
                self.ner_model = model_loader.get_ner_model()
                logger.info("تم تحميل نموذج التعرف على الكيانات المسماة")
            except Exception as e:
                logger.warning(f"فشل في تحميل نموذج التعرف على الكيانات المسماة: {str(e)}")
        
        logger.info("تم تهيئة محلل المحتوى المحلي")
    
    def analyze(self, extracted_text: str) -> Dict[str, Any]:
        """
        تحليل المحتوى المحلي من نص المناقصة
        
        المعاملات:
        ----------
        extracted_text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المحتوى المحلي
        """
        try:
            logger.info("بدء تحليل المحتوى المحلي")
            
            # استخراج متطلبات المحتوى المحلي
            local_content_requirements = self._extract_local_content_requirements(extracted_text)
            
            # استخراج المواد والمنتجات المطلوبة
            required_materials = self._extract_required_materials(extracted_text)
            
            # تقدير نسبة المحتوى المحلي المتوقعة
            estimated_local_content = self._estimate_local_content(required_materials)
            
            # تحديد النسبة المطلوبة من المحتوى المحلي
            required_local_content = self._get_required_local_content(local_content_requirements, extracted_text)
            
            # تحديد الموردين المحليين المحتملين
            potential_suppliers = self._identify_potential_suppliers(required_materials)
            
            # اقتراح استراتيجيات تحسين المحتوى المحلي
            improvement_strategies = self._generate_improvement_strategies(
                estimated_local_content, 
                required_local_content,
                required_materials
            )
            
            # إعداد النتائج
            results = {
                "estimated_local_content": estimated_local_content,
                "required_local_content": required_local_content,
                "local_content_requirements": local_content_requirements,
                "required_materials": required_materials,
                "potential_suppliers": potential_suppliers,
                "improvement_strategies": improvement_strategies
            }
            
            logger.info(f"اكتمل تحليل المحتوى المحلي: تقدير {estimated_local_content:.1f}%، مطلوب {required_local_content:.1f}%")
            return results
            
        except Exception as e:
            logger.error(f"فشل في تحليل المحتوى المحلي: {str(e)}")
            return {
                "estimated_local_content": 0,
                "required_local_content": 0,
                "local_content_requirements": [],
                "required_materials": [],
                "potential_suppliers": [],
                "improvement_strategies": [
                    "حدث خطأ في تحليل المحتوى المحلي. يرجى التحقق من البيانات المدخلة."
                ],
                "error": str(e)
            }
    
    def _extract_local_content_requirements(self, text: str) -> List[Dict[str, Any]]:
        """
        استخراج متطلبات المحتوى المحلي من نص المناقصة
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة بمتطلبات المحتوى المحلي
        """
        requirements = []
        
        # البحث عن الفقرات المتعلقة بالمحتوى المحلي
        local_content_paragraphs = self._find_local_content_paragraphs(text)
        
        for paragraph in local_content_paragraphs:
            # البحث عن النسب المئوية
            percentage_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(%|في المائة|بالمائة|نسبة)', paragraph)
            
            for match in percentage_matches:
                percentage = float(match[0])
                
                # التحقق مما إذا كانت النسبة في النطاق المعقول للمحتوى المحلي
                if 0 <= percentage <= 100:
                    # تحديد نوع المتطلب
                    req_type = "غير محدد"
                    
                    if re.search(r'الحد الأدنى|الأقل|على الأقل', paragraph):
                        req_type = "الحد الأدنى"
                    elif re.search(r'الحد الأقصى|كحد أقصى', paragraph):
                        req_type = "الحد الأقصى"
                    elif re.search(r'هدف|مستهدف', paragraph):
                        req_type = "مستهدف"
                    
                    # تحديد الفئة
                    category = "عام"
                    
                    if re.search(r'توظيف|عمالة|السعودة|التوطين|الموظفين', paragraph):
                        category = "توظيف"
                    elif re.search(r'خدمات|استشارات', paragraph):
                        category = "خدمات"
                    elif re.search(r'توريد|مواد|منتجات|بضائع', paragraph):
                        category = "منتجات"
                    elif re.search(r'تدريب|تأهيل|تطوير', paragraph):
                        category = "تدريب"
                    
                    # تحديد الإلزامية
                    is_mandatory = bool(re.search(r'إلزامي|يجب|ضروري|لا بد|لابد|مطلوب|يلتزم|ملزم', paragraph))
                    
                    requirements.append({
                        "description": paragraph[:200] + ("..." if len(paragraph) > 200 else ""),
                        "percentage": percentage,
                        "type": req_type,
                        "category": category,
                        "is_mandatory": is_mandatory
                    })
        
        return requirements
    
    def _find_local_content_paragraphs(self, text: str) -> List[str]:
        """
        البحث عن الفقرات المتعلقة بالمحتوى المحلي
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[str]
            قائمة بالفقرات المتعلقة بالمحتوى المحلي
        """
        # تقسيم النص إلى فقرات
        paragraphs = re.split(r'\n\s*\n', text)
        
        # الكلمات المفتاحية للمحتوى المحلي
        local_content_keywords = [
            'المحتوى المحلي',
            'التوطين',
            'المواد المحلية',
            'المنتجات المحلية',
            'نسبة المحتوى',
            'مبادرة المحتوى المحلي',
            'هيئة المحتوى المحلي',
            'منتجات وطنية',
            'صنع في السعودية',
            'المصنّعين المحليين',
            'الموردين المحليين',
            'القيمة المضافة',
            'نقل التقنية',
            'توطين الوظائف',
            'السعودة',
        ]
        
        # البحث عن الفقرات التي تحتوي على كلمات مفتاحية للمحتوى المحلي
        local_content_paragraphs = []
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            # البحث عن الكلمات المفتاحية في الفقرة
            for keyword in local_content_keywords:
                if keyword in paragraph.lower():
                    local_content_paragraphs.append(paragraph)
                    break
        
        return local_content_paragraphs
    
    def _extract_required_materials(self, text: str) -> List[Dict[str, Any]]:
        """
        استخراج المواد والمنتجات المطلوبة من نص المناقصة
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة بالمواد والمنتجات المطلوبة
        """
        required_materials = []
        
        # البحث عن جداول المواصفات والكميات
        tables = self._extract_tables(text)
        
        # البحث عن قوائم المواد في النص
        for table in tables:
            items = self._parse_table_for_materials(table)
            if items:
                required_materials.extend(items)
        
        # البحث عن قوائم المواد في النص العادي
        text_materials = self._extract_materials_from_text(text)
        if text_materials:
            required_materials.extend(text_materials)
        
        # إزالة التكرارات
        unique_materials = []
        material_names = set()
        
        for material in required_materials:
            name = material.get('name', '').lower()
            if name and name not in material_names:
                material_names.add(name)
                unique_materials.append(material)
        
        # تقييم توفر المواد محلياً
        for material in unique_materials:
            material['local_availability'] = self._check_local_availability(material['name'])
        
        return unique_materials
    
    def _check_local_availability(self, material_name: str) -> float:
        """
        تقييم مدى توفر المادة محلياً
        
        المعاملات:
        ----------
        material_name : str
            اسم المادة
            
        المخرجات:
        --------
        float
            نسبة توفر المادة مح, '', name)
                
                # إضافة المادة إلى القائمة إذا كان الاسم غير فارغ
                if name and len(name) > 3:  # تجاهل الأسماء القصيرة جدًا
                    items.append({
                        "name": name,
                        "quantity": quantity,
                        "unit": unit,
                        "source": "text"
                    })
        
        return items
    
    def _estimate_local_content(self, required_materials: List[Dict[str, Any]]) -> float:
        """
        تقدير نسبة المحتوى المحلي المتوقعة
        
        المعاملات:
        ----------
        required_materials : List[Dict[str, Any]]
            قائمة المواد المطلوبة
            
        المخرجات:
        --------
        float
            نسبة المحتوى المحلي المقدرة
        """
        if not required_materials:
            return 0.0
        
        # حساب متوسط توفر المواد محلياً
        availability_sum = sum(material.get('local_availability', 0) for material in required_materials)
        avg_availability = availability_sum / len(required_materials)
        
        # تعديل التقدير بناءً على بيانات إضافية من اللوائح
        base_estimate = avg_availability
        
        # تعديل بناءً على فئة المشروع (مثال افتراضي)
        project_category = self.config.get('project_category', 'general')
        category_adjustment = self.local_content_regulations.get('category_adjustments', {}).get(project_category, 0)
        
        # توليد تقدير نهائي
        final_estimate = min(100.0, max(0.0, base_estimate + category_adjustment))
        
        return round(final_estimate, 1)
    
    def _get_required_local_content(self, local_content_requirements: List[Dict[str, Any]], text: str) -> float:
        """
        تحديد النسبة المطلوبة من المحتوى المحلي
        
        المعاملات:
        ----------
        local_content_requirements : List[Dict[str, Any]]
            متطلبات المحتوى المحلي المستخرجة
        text : str
            النص الكامل للمناقصة
            
        المخرجات:
        --------
        float
            النسبة المطلوبة من المحتوى المحلي
        """
        # البحث في متطلبات المحتوى المحلي المستخرجة
        if local_content_requirements:
            # البحث عن متطلبات الحد الأدنى الإلزامية
            mandatory_mins = [req['percentage'] for req in local_content_requirements 
                              if req['type'] == 'الحد الأدنى' and req['is_mandatory']]
            
            if mandatory_mins:
                return max(mandatory_mins)
        
        # البحث في النص عن النسب المطلوبة
        percentage_pattern = r'(?:نسبة|حد أدنى)[^%\d١٢٣٤٥٦٧٨٩٠]*?(\d+(?:\.\d+)?)\s*%'
        percentage_matches = re.findall(percentage_pattern, text)
        
        if percentage_matches:
            # استخدام أول نسبة مئوية تم العثور عليها
            try:
                return float(percentage_matches[0])
            except ValueError:
                pass
        
        # البحث في اللوائح عن النسبة الافتراضية
        # استخدام قيمة افتراضية إذا لم يتم العثور على نسبة محددة
        return self.local_content_regulations.get('default_percentage', 30.0)
    
    def _identify_potential_suppliers(self, required_materials: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        تحديد الموردين المحليين المحتملين للمواد المطلوبة
        
        المعاملات:
        ----------
        required_materials : List[Dict[str, Any]]
            قائمة المواد المطلوبة
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة الموردين المحتملين
        """
        potential_suppliers = []
        
        # البحث عن موردين لكل مادة
        for material in required_materials:
            material_name = material['name']
            suppliers_for_material = []
            
            # البحث في قاعدة بيانات الموردين
            for supplier in self.local_suppliers_db:
                # التحقق مما إذا كان المورد يوفر هذه المادة
                if any(self._simple_similarity(material_name, product) > 0.6 for product in supplier.get('products', [])):
                    suppliers_for_material.append({
                        "name": supplier.get('name', ''),
                        "region": supplier.get('region', ''),
                        "reliability": supplier.get('reliability', 0),
                        "contact": supplier.get('contact', '')
                    })
            
            # إضافة الموردين المحتملين للمادة
            if suppliers_for_material:
                material['potential_suppliers'] = suppliers_for_material
                
                for supplier in suppliers_for_material:
                    # إضافة المورد إلى القائمة العامة إذا لم يكن موجودًا بالفعل
                    if not any(s.get('name') == supplier['name'] for s in potential_suppliers):
                        supplier_info = supplier.copy()
                        supplier_info['materials'] = [material_name]
                        potential_suppliers.append(supplier_info)
                    else:
                        # إضافة المادة إلى قائمة المواد التي يوفرها المورد
                        for s in potential_suppliers:
                            if s.get('name') == supplier['name'] and material_name not in s.get('materials', []):
                                s.setdefault('materials', []).append(material_name)
        
        # ترتيب الموردين حسب عدد المواد ودرجة الموثوقية
        return sorted(potential_suppliers, 
                      key=lambda s: (len(s.get('materials', [])), s.get('reliability', 0)), 
                      reverse=True)
    
    def _generate_improvement_strategies(self, estimated_local_content: float, 
                                       required_local_content: float,
                                       required_materials: List[Dict[str, Any]]) -> List[str]:
        """
        اقتراح استراتيجيات تحسين المحتوى المحلي
        
        المعاملات:
        ----------
        estimated_local_content : float
            نسبة المحتوى المحلي المقدرة
        required_local_content : float
            نسبة المحتوى المحلي المطلوبة
        required_materials : List[Dict[str, Any]]
            قائمة المواد المطلوبة
            
        المخرجات:
        --------
        List[str]
            استراتيجيات تحسين المحتوى المحلي
        """
        strategies = []
        
        # التحقق مما إذا كانت النسبة المقدرة أقل من النسبة المطلوبة
        if estimated_local_content < required_local_content:
            strategies.append(f"زيادة نسبة المحتوى المحلي من {estimated_local_content:.1f}% إلى {required_local_content:.1f}% على الأقل")
            
            # تحديد المواد ذات التوفر المنخفض محلياً
            low_availability_materials = [m for m in required_materials if m.get('local_availability', 0) < 50]
            
            if low_availability_materials:
                materials_str = ", ".join([m['name'] for m in low_availability_materials[:3]])
                if len(low_availability_materials) > 3:
                    materials_str += f" وغيرها ({len(low_availability_materials) - 3} مواد أخرى)"
                
                strategies.append(f"البحث عن بدائل محلية للمواد التالية: {materials_str}")
            
            # استراتيجيات عامة
            strategies.extend([
                "الشراكة مع شركات محلية لتوفير المواد والخدمات",
                "الاستفادة من برامج دعم المحتوى المحلي المقدمة من هيئة المحتوى المحلي",
                "تدريب وتوظيف كوادر سعودية لزيادة نسبة التوطين",
                "التعاقد مع مصنعين محليين للمساهمة في التصنيع المحلي"
            ])
            
        else:
            strategies.append(f"الحفاظ على نسبة المحتوى المحلي الحالية ({estimated_local_content:.1f}%) التي تفوق المتطلبات ({required_local_content:.1f}%)")
            
            # استراتيجيات للتحسين المستمر
            strategies.extend([
                "توثيق وإبراز نسبة المحتوى المحلي العالية في العرض المقدم",
                "استخدام نسبة المحتوى المحلي كميزة تنافسية في المناقصة",
                "التركيز على رفع جودة المكونات المحلية لتعزيز القيمة المضافة"
            ])
        
        # استراتيجيات لتحسين التوثيق والامتثال
        strategies.extend([
            "توثيق مصادر المواد والخدمات المحلية بشكل دقيق",
            "تطبيق منهجية حساب المحتوى المحلي وفقًا لمتطلبات هيئة المحتوى المحلي",
            "إعداد خطة تفصيلية للمحتوى المحلي ومتابعة تنفيذها خلال المشروع"
        ])
        
        return strategies
    
    def _load_local_materials(self) -> List[Dict[str, Any]]:
        """
        تحميل قاعدة بيانات المواد المحلية
        
        المخرجات:
        --------
        List[Dict[str, Any]]
            قاعدة بيانات المواد المحلية
        """
        try:
            file_path = 'data/templates/local_materials.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"ملف قاعدة بيانات المواد المحلية غير موجود: {file_path}")
                # إنشاء قاعدة بيانات افتراضية
                return self._create_default_materials_db()
        except Exception as e:
            logger.error(f"فشل في تحميل قاعدة بيانات المواد المحلية: {str(e)}")
            return self._create_default_materials_db()
    
    def _load_local_suppliers(self) -> List[Dict[str, Any]]:
        """
        تحميل قاعدة بيانات الموردين المحليين
        
        المخرجات:
        --------
        List[Dict[str, Any]]
            قاعدة بيانات الموردين المحليين
        """
        try:
            file_path = 'data/templates/local_suppliers.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"ملف قاعدة بيانات الموردين المحليين غير موجود: {file_path}")
                # إنشاء قاعدة بيانات افتراضية
                return self._create_default_suppliers_db()
        except Exception as e:
            logger.error(f"فشل في تحميل قاعدة بيانات الموردين المحليين: {str(e)}")
            return self._create_default_suppliers_db()
    
    def _load_regulations(self) -> Dict[str, Any]:
        """
        تحميل لوائح وقواعد المحتوى المحلي
        
        المخرجات:
        --------
        Dict[str, Any]
            لوائح وقواعد المحتوى المحلي
        """
        try:
            file_path = 'data/templates/local_content_regulations.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"ملف لوائح المحتوى المحلي غير موجود: {file_path}")
                # إنشاء لوائح افتراضية
                return self._create_default_regulations()
        except Exception as e:
            logger.error(f"فشل في تحميل لوائح المحتوى المحلي: {str(e)}")
            return self._create_default_regulations()
    
    def _create_default_materials_db(self) -> List[Dict[str, Any]]:
        """
        إنشاء قاعدة بيانات افتراضية للمواد المحلية
        
        المخرجات:
        --------
        List[Dict[str, Any]]
            قاعدة بيانات افتراضية للمواد المحلية
        """
        return [
            {"name": "حديد تسليح", "category": "مواد بناء", "availability_percentage": 90.0},
            {"name": "أسمنت", "category": "مواد بناء", "availability_percentage": 95.0},
            {"name": "خرسانة جاهزة", "category": "مواد بناء", "availability_percentage": 100.0},
            {"name": "بلاط", "category": "مواد بناء", "availability_percentage": 80.0},
            {"name": "رخام", "category": "مواد بناء", "availability_percentage": 60.0},
            {"name": "دهانات", "category": "مواد بناء", "availability_percentage": 75.0},
            {"name": "زجاج", "category": "مواد بناء", "availability_percentage": 50.0},
            {"name": "أسلاك كهربائية", "category": "كهرباء", "availability_percentage": 60.0},
            {"name": "لوحات كهربائية", "category": "كهرباء", "availability_percentage": 55.0},
            {"name": "مفاتيح كهربائية", "category": "كهرباء", "availability_percentage": 45.0},
            {"name": "أنابيب مياه", "category": "سباكة", "availability_percentage": 70.0},
            {"name": "خزانات مياه", "category": "سباكة", "availability_percentage": 95.0},
            {"name": "مواسير صرف", "category": "سباكة", "availability_percentage": 85.0},
            {"name": "وحدات تكييف", "category": "تكييف", "availability_percentage": 30.0},
            {"name": "معدات تبريد", "category": "تكييف", "availability_percentage": 25.0},
            {"name": "أجهزة تهوية", "category": "تكييف", "availability_percentage": 40.0},
            {"name": "أثاث مكتبي", "category": "أثاث", "availability_percentage": 70.0},
            {"name": "أثاث منزلي", "category": "أثاث", "availability_percentage": 65.0},
            {"name": "أبواب خشبية", "category": "نجارة", "availability_percentage": 80.0},
            {"name": "نوافذ ألمنيوم", "category": "ألمنيوم", "availability_percentage": 75.0}
        ]
    
    def _create_default_suppliers_db(self) -> List[Dict[str, Any]]:
        """
        إنشاء قاعدة بيانات افتراضية للموردين المحليين
        
        المخرجات:
        --------
        List[Dict[str, Any]]
            قاعدة بيانات افتراضية للموردين المحليين
        """
        return [
            {
                "name": "شركة الراجحي للحديد",
                "region": "الرياض",
                "category": "مواد بناء",
                "products": ["حديد تسليح", "حديد مجلفن"],
                "reliability": 4.5,
                "contact": "info@rajhi-steel.sa",
                "nitaqat_category": "بلاتيني"
            },
            {
                "name": "شركة امجاد للسباكة",
                "region": "الرياض",
                "category": "سباكة",
                "products": ["أنابيب مياه", "خزانات مياه", "مواسير صرف"],
                "reliability": 3.9,
                "contact": "info@amjad-plumbing.sa",
                "nitaqat_category": "أخضر متوسط"
            },
            {
                "name": "مصنع الخليج للزجاج",
                "region": "جدة",
                "category": "مواد بناء",
                "products": ["زجاج", "ألواح زجاجية", "واجهات زجاجية"],
                "reliability": 4.0,
                "contact": "info@gulf-glass.sa",
                "nitaqat_category": "أخضر مرتفع"
            },
            {
                "name": "مؤسسة الديار للدهانات",
                "region": "الرياض",
                "category": "مواد بناء",
                "products": ["دهانات", "طلاء جدران", "عوازل"],
                "reliability": 3.7,
                "contact": "info@aldiyar-paints.sa",
                "nitaqat_category": "أخضر منخفض"
            },
            {
                "name": "شركة الأثاث المكتبي المتحدة",
                "region": "الرياض",
                "category": "أثاث",
                "products": ["أثاث مكتبي", "كراسي", "طاولات", "خزائن"],
                "reliability": 4.1,
                "contact": "info@united-furniture.sa",
                "nitaqat_category": "أخضر مرتفع"
            },
            {
                "name": "شركة ابن غنيم للنجارة",
                "region": "الدمام",
                "category": "نجارة",
                "products": ["أبواب خشبية", "نوافذ خشبية", "أثاث منزلي"],
                "reliability": 4.3,
                "contact": "info@ibnghonaim.sa",
                "nitaqat_category": "أخضر مرتفع"
            },
            {
                "name": "الشركة العربية للألمنيوم",
                "region": "جدة",
                "category": "ألمنيوم",
                "products": ["نوافذ ألمنيوم", "أبواب ألمنيوم", "واجهات ألمنيوم"],
                "reliability": 4.4,
                "contact": "info@arabian-aluminum.sa",
                "nitaqat_category": "بلاتيني"
            }
        ]
    
    def _create_default_regulations(self) -> Dict[str, Any]:
        """
        إنشاء لوائح افتراضية للمحتوى المحلي
        
        المخرجات:
        --------
        Dict[str, Any]
            لوائح افتراضية للمحتوى المحلي
        """
        return {
            "default_percentage": 30.0,
            "category_adjustments": {
                "construction": 5.0,
                "it": -5.0,
                "manufacturing": 10.0,
                "services": 0.0,
                "general": 0.0
            },
            "sector_requirements": {
                "oil_and_gas": 40.0,
                "electricity": 35.0,
                "water": 25.0,
                "telecommunications": 20.0,
                "transportation": 30.0,
                "healthcare": 25.0,
                "education": 35.0
            },
            "calculation_method": "السعر العرض الذي يحتوي على نسبة أعلى من المحتوى المحلي يحصل على ميزة سعرية تصل إلى 10% من السعر",
            "documentation_requirements": [
                "شهادات المنشأ للمواد والمنتجات",
                "عقود التوريد مع الموردين المحليين",
                "كشوف رواتب الموظفين السعوديين",
                "شهادات تصنيف المقاولين",
                "شهادات نطاقات للتوطين"
            ],
            "reference_documents": [
                "دليل هيئة المحتوى المحلي وتنمية القطاع الخاص",
                "لائحة تفضيل المنتجات المحلية في المشتريات الحكومية",
                "دليل تطبيق آلية الوزن النسبي للمحتوى المحلي في التقييم المالي"
            ],
            "last_updated": "2023-06-15"
        }category": "بلاتيني"
            },
            {
                "name": "اسمنت اليمامة",
                "region": "الرياض",
                "category": "مواد بناء",
                "products": ["أسمنت", "خرسانة جاهزة"],
                "reliability": 4.7,
                "contact": "info@yamama-cement.sa",
                "nitaqat_category": "بلاتيني"
            },
            {
                "name": "الشركة السعودية للصناعات الكهربائية",
                "region": "جدة",
                "category": "كهرباء",
                "products": ["أسلاك كهربائية", "لوحات كهربائية", "مفاتيح كهربائية"],
                "reliability": 4.2,
                "contact": "info@siec.sa",
                "nitaqat_category": "أخضر مرتفع"
            },
            {
                "name": "شركة الزامل للتكييف",
                "region": "الدمام",
                "category": "تكييف",
                "products": ["وحدات تكييف", "معدات تبريد", "أجهزة تهوية"],
                "reliability": 4.8,
                "contact": "info@zamil-ac.sa",
                "nitaqat_"""
محلل المحتوى المحلي
يقوم بتحليل متطلبات المحتوى المحلي في المناقصات وتقييم نسب المحتوى المحلي
"""

import re
import json
import logging
import os
from typing import Dict, List, Any, Tuple, Optional, Union
import numpy as np

logger = logging.getLogger(__name__)

class LocalContentAnalyzer:
    """
    محلل المحتوى المحلي في المناقصات
    """
    
    def __init__(self, model_loader, config=None):
        """
        تهيئة محلل المحتوى المحلي
        
        المعاملات:
        ----------
        model_loader : ModelLoader
            محمّل النماذج المستخدمة للتحليل
        config : Dict, optional
            إعدادات المحلل
        """
        self.config = config or {}
        self.model_loader = model_loader
        
        # تحميل قوائم المنتجات والمواد المحلية
        self.local_materials_db = self._load_local_materials()
        self.local_suppliers_db = self._load_local_suppliers()
        
        # تحميل قواعد ولوائح المحتوى المحلي
        self.local_content_regulations = self._load_regulations()
        
        # تحميل نموذج تحليل النصوص إذا كان متاحاً
        self.ner_model = None
        if hasattr(model_loader, 'get_ner_model'):
            try:
                self.ner_model = model_loader.get_ner_model()
                logger.info("تم تحميل نموذج التعرف على الكيانات المسماة")
            except Exception as e:
                logger.warning(f"فشل في تحميل نموذج التعرف على الكيانات المسماة: {str(e)}")
        
        logger.info("تم تهيئة محلل المحتوى المحلي")
    
    def analyze(self, extracted_text: str) -> Dict[str, Any]:
        """
        تحليل المحتوى المحلي من نص المناقصة
        
        المعاملات:
        ----------
        extracted_text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المحتوى المحلي
        """
        try:
            logger.info("بدء تحليل المحتوى المحلي")
            
            # استخراج متطلبات المحتوى المحلي
            local_content_requirements = self._extract_local_content_requirements(extracted_text)
            
            # استخراج المواد والمنتجات المطلوبة
            required_materials = self._extract_required_materials(extracted_text)
            
            # تقدير نسبة المحتوى المحلي المتوقعة
            estimated_local_content = self._estimate_local_content(required_materials)
            
            # تحديد النسبة المطلوبة من المحتوى المحلي
            required_local_content = self._get_required_local_content(local_content_requirements, extracted_text)
            
            # تحديد الموردين المحليين المحتملين
            potential_suppliers = self._identify_potential_suppliers(required_materials)
            
            # اقتراح استراتيجيات تحسين المحتوى المحلي
            improvement_strategies = self._generate_improvement_strategies(
                estimated_local_content, 
                required_local_content,
                required_materials
            )
            
            # إعداد النتائج
            results = {
                "estimated_local_content": estimated_local_content,
                "required_local_content": required_local_content,
                "local_content_requirements": local_content_requirements,
                "required_materials": required_materials,
                "potential_suppliers": potential_suppliers,
                "improvement_strategies": improvement_strategies
            }
            
            logger.info(f"اكتمل تحليل المحتوى المحلي: تقدير {estimated_local_content:.1f}%، مطلوب {required_local_content:.1f}%")
            return results
            
        except Exception as e:
            logger.error(f"فشل في تحليل المحتوى المحلي: {str(e)}")
            return {
                "estimated_local_content": 0,
                "required_local_content": 0,
                "local_content_requirements": [],
                "required_materials": [],
                "potential_suppliers": [],
                "improvement_strategies": [
                    "حدث خطأ في تحليل المحتوى المحلي. يرجى التحقق من البيانات المدخلة."
                ],
                "error": str(e)
            }
    
    def _extract_local_content_requirements(self, text: str) -> List[Dict[str, Any]]:
        """
        استخراج متطلبات المحتوى المحلي من نص المناقصة
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة بمتطلبات المحتوى المحلي
        """
        requirements = []
        
        # البحث عن الفقرات المتعلقة بالمحتوى المحلي
        local_content_paragraphs = self._find_local_content_paragraphs(text)
        
        for paragraph in local_content_paragraphs:
            # البحث عن النسب المئوية
            percentage_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(%|في المائة|بالمائة|نسبة)', paragraph)
            
            for match in percentage_matches:
                percentage = float(match[0])
                
                # التحقق مما إذا كانت النسبة في النطاق المعقول للمحتوى المحلي
                if 0 <= percentage <= 100:
                    # تحديد نوع المتطلب
                    req_type = "غير محدد"
                    
                    if re.search(r'الحد الأدنى|الأقل|على الأقل', paragraph):
                        req_type = "الحد الأدنى"
                    elif re.search(r'الحد الأقصى|كحد أقصى', paragraph):
                        req_type = "الحد الأقصى"
                    elif re.search(r'هدف|مستهدف', paragraph):
                        req_type = "مستهدف"
                    
                    # تحديد الفئة
                    category = "عام"
                    
                    if re.search(r'توظيف|عمالة|السعودة|التوطين|الموظفين', paragraph):
                        category = "توظيف"
                    elif re.search(r'خدمات|استشارات', paragraph):
                        category = "خدمات"
                    elif re.search(r'توريد|مواد|منتجات|بضائع', paragraph):
                        category = "منتجات"
                    elif re.search(r'تدريب|تأهيل|تطوير', paragraph):
                        category = "تدريب"
                    
                    # تحديد الإلزامية
                    is_mandatory = bool(re.search(r'إلزامي|يجب|ضروري|لا بد|لابد|مطلوب|يلتزم|ملزم', paragraph))
                    
                    requirements.append({
                        "description": paragraph[:200] + ("..." if len(paragraph) > 200 else ""),
                        "percentage": percentage,
                        "type": req_type,
                        "category": category,
                        "is_mandatory": is_mandatory
                    })
        
        return requirements
    
    def _find_local_content_paragraphs(self, text: str) -> List[str]:
        """
        البحث عن الفقرات المتعلقة بالمحتوى المحلي
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[str]
            قائمة بالفقرات المتعلقة بالمحتوى المحلي
        """
        # تقسيم النص إلى فقرات
        paragraphs = re.split(r'\n\s*\n', text)
        
        # الكلمات المفتاحية للمحتوى المحلي
        local_content_keywords = [
            'المحتوى المحلي',
            'التوطين',
            'المواد المحلية',
            'المنتجات المحلية',
            'نسبة المحتوى',
            'مبادرة المحتوى المحلي',
            'هيئة المحتوى المحلي',
            'منتجات وطنية',
            'صنع في السعودية',
            'المصنّعين المحليين',
            'الموردين المحليين',
            'القيمة المضافة',
            'نقل التقنية',
            'توطين الوظائف',
            'السعودة',
        ]
        
        # البحث عن الفقرات التي تحتوي على كلمات مفتاحية للمحتوى المحلي
        local_content_paragraphs = []
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            # البحث عن الكلمات المفتاحية في الفقرة
            for keyword in local_content_keywords:
                if keyword in paragraph.lower():
                    local_content_paragraphs.append(paragraph)
                    break
        
        return local_content_paragraphs
    
    def _extract_required_materials(self, text: str) -> List[Dict[str, Any]]:
        """
        استخراج المواد والمنتجات المطلوبة من نص المناقصة
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة بالمواد والمنتجات المطلوبة
        """
        required_materials = []
        
        # البحث عن جداول المواصفات والكميات
        tables = self._extract_tables(text)
        
        # البحث عن قوائم المواد في النص
        for table in tables:
            items = self._parse_table_for_materials(table)
            if items:
                required_materials.extend(items)
        
        # البحث عن قوائم المواد في النص العادي
        text_materials = self._extract_materials_from_text(text)
        if text_materials:
            required_materials.extend(text_materials)
        
        # إزالة التكرارات
        unique_materials = []
        material_names = set()
        
        for material in required_materials:
            name = material.get('name', '').lower()
            if name and name not in material_names:
                material_names.add(name)
                unique_materials.append(material)
        
        # تقييم توفر المواد محلياً
        for material in unique_materials:
            material['local_availability'] = self._check_local_availability(material['name'])
        
        return unique_materials
    
    def _check_local_availability(self, material_name: str) -> float:
        """
        تقييم مدى توفر المادة محلياً بناءً على قاعدة بيانات أو تحليل البيانات المتاحة.

        المعاملات:
        ----------
        material_name : str
            اسم المادة التي نريد التحقق من توفرها محليًا.

        المخرجات:
        --------
        float
            نسبة توفر المادة محليًا، تتراوح بين 0.0 (غير متوفرة) إلى 1.0 (متوفرة بالكامل).
        """

        # قاعدة بيانات تقديرية لتوفر المواد محليًا (يمكن استبدالها بمصدر بيانات فعلي)
        local_materials = {
            "حديد": 0.95,   # متوفر بنسبة 95%
            "أسمنت": 0.9,   # متوفر بنسبة 90%
            "خشب": 0.7,    # متوفر بنسبة 70%
            "زجاج": 0.6,    # متوفر بنسبة 60%
            "ألمنيوم": 0.85, # متوفر بنسبة 85%
            "بلاستيك": 0.8,  # متوفر بنسبة 80%
            "نحاس": 0.5,    # متوفر بنسبة 50%
            "إلكترونيات متخصصة": 0.3 # متوفر بنسبة 30%
        }

        # البحث عن المادة في القائمة
        for key in local_materials:
            if key in material_name:
                return local_materials[key]

        # إذا لم تكن المادة موجودة في القائمة، نفترض توفرها بنسبة 0.5 كافتراضي
        return 0.5
