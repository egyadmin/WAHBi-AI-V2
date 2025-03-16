
def _calculate_equipment_costs(self, scope_of_work: List[str], project_duration: int) -> Dict[str, float]:
        """
        حساب تكاليف المعدات
        
        المعاملات:
        ----------
        scope_of_work : List[str]
            نطاق العمل
        project_duration : int
            مدة المشروع بالأشهر
            
        المخرجات:
        --------
        Dict[str, float]
            تكاليف المعدات
        """
        equipment_costs = {}
        
        # تحديد نوع المشروع بناءً على نطاق العمل
        project_type = self._determine_project_type(scope_of_work)
        
        # الحصول على المعدات المطلوبة لهذا النوع من المشاريع
        required_equipment = self.cost_db.get("equipment_requirements", {}).get(project_type, {})
        
        # حساب تكاليف كل نوع من المعدات
        for equipment_type, count in required_equipment.items():
            # الحصول على التكلفة الشهرية
            monthly_cost = self.equipment_costs.get(equipment_type, {}).get("monthly_cost", 0)
            
            # الحصول على نوع التكلفة (شراء أو إيجار)
            cost_type = self.equipment_costs.get(equipment_type, {}).get("cost_type", "إيجار")
            
            if cost_type == "شراء":
                # في حالة الشراء، نستخدم التكلفة الإجمالية وليس الشهرية
                total_cost = self.equipment_costs.get(equipment_type, {}).get("purchase_cost", 0) * count
            else:
                # في حالة الإيجار، نحسب التكلفة الشهرية على مدة المشروع
                total_cost = monthly_cost * count * project_duration
            
            # إضافة التكلفة إلى القاموس
            equipment_costs[equipment_type] = total_cost
        
        return equipment_costs
    
    def _calculate_material_costs(self, quantities: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        حساب تكاليف المواد
        
        المعاملات:
        ----------
        quantities : List[Dict[str, Any]]
            كميات المواد
            
        المخرجات:
        --------
        Dict[str, float]
            تكاليف المواد
        """
        material_costs = {}
        
        # إذا لم تكن هناك كميات، استخدم قيم افتراضية
        if not quantities:
            material_costs = {
                "مواد بناء أساسية": 500000,
                "مواد تشطيب": 300000,
                "مواد كهربائية": 200000,
                "مواد سباكة": 150000,
                "مواد أخرى": 100000
            }
            return material_costs
        
        # تجميع المواد حسب الفئة
        material_categories = {}
        
        for item in quantities:
            description = item.get("description", "")
            quantity = item.get("quantity", 0)
            
            # تحديد فئة المادة
            category = self._determine_material_category(description)
            
            # إضافة الكمية إلى الفئة
            if category in material_categories:
                material_categories[category].append((description, quantity))
            else:
                material_categories[category] = [(description, quantity)]
        
        # حساب تكلفة كل فئة
        for category, items in material_categories.items():
            total_quantity = sum(quantity for _, quantity in items)
            unit_price = self.cost_db.get("material_prices", {}).get(category, 1000)
            
            material_costs[category] = total_quantity * unit_price
        
        return material_costs
    
    def _calculate_indirect_costs(self, labor_costs: Dict[str, float], 
                                 equipment_costs: Dict[str, float], 
                                 material_costs: Dict[str, float],
                                 project_duration: int) -> Dict[str, float]:
        """
        حساب التكاليف غير المباشرة
        
        المعاملات:
        ----------
        labor_costs : Dict[str, float]
            تكاليف العمالة
        equipment_costs : Dict[str, float]
            تكاليف المعدات
        material_costs : Dict[str, float]
            تكاليف المواد
        project_duration : int
            مدة المشروع بالأشهر
            
        المخرجات:
        --------
        Dict[str, float]
            التكاليف غير المباشرة
        """
        indirect_costs = {}
        
        # إجمالي التكاليف المباشرة
        direct_costs = sum(labor_costs.values()) + sum(equipment_costs.values()) + sum(material_costs.values())
        
        # حساب تكاليف الإدارة
        management_percentage = self.config.get("management_percentage", 0.05)
        indirect_costs["تكاليف الإدارة"] = direct_costs * management_percentage
        
        # حساب تكاليف الضمان البنكي
        bank_guarantee_percentage = self.config.get("bank_guarantee_percentage", 0.03)
        indirect_costs["الضمان البنكي"] = direct_costs * bank_guarantee_percentage
        
        # حساب تكاليف التأمين
        insurance_percentage = self.config.get("insurance_percentage", 0.02)
        indirect_costs["التأمين"] = direct_costs * insurance_percentage
        
        # حساب تكاليف الموقع
        site_costs_per_month = self.config.get("site_costs_per_month", 20000)
        indirect_costs["تكاليف الموقع"] = site_costs_per_month * project_duration
        
        # حساب تكاليف النقل
        transportation_percentage = self.config.get("transportation_percentage", 0.04)
        indirect_costs["النقل"] = sum(material_costs.values()) * transportation_percentage
        
        # حساب تكاليف الاختبارات
        testing_percentage = self.config.get("testing_percentage", 0.01)
        indirect_costs["الاختبارات والفحص"] = direct_costs * testing_percentage
        
        return indirect_costs
    
    def _calculate_other_costs(self, project_info: Dict[str, Any]) -> Dict[str, float]:
        """
        حساب التكاليف الأخرى
        
        المعاملات:
        ----------
        project_info : Dict[str, Any]
            معلومات المشروع
            
        المخرجات:
        --------
        Dict[str, float]
            التكاليف الأخرى
        """
        other_costs = {}
        
        # تحديد نوع المشروع
        project_type = project_info.get("sector", "general")
        
        # حساب تكاليف الترخيص
        licensing_cost = self.config.get("licensing_costs", {}).get(project_type, 50000)
        other_costs["تراخيص وتصاريح"] = licensing_cost
        
        # حساب تكاليف الاستشارات
        consulting_percentage = self.config.get("consulting_percentage", 0.03)
        estimated_value = project_info.get("estimated_value", 1000000)
        other_costs["استشارات"] = estimated_value * consulting_percentage
        
        # حساب تكاليف الضمان
        warranty_percentage = self.config.get("warranty_percentage", 0.02)
        other_costs["ضمان وصيانة"] = estimated_value * warranty_percentage
        
        # حساب تكاليف المطابقة
        compliance_costs = self.config.get("compliance_costs", {}).get(project_type, 25000)
        other_costs["مطابقة ومعايير"] = compliance_costs
        
        # حساب تكاليف أخرى متنوعة
        miscellaneous_percentage = self.config.get("miscellaneous_percentage", 0.05)
        other_costs["متنوعة"] = estimated_value * miscellaneous_percentage
        
        return other_costs
    
    def _determine_project_type(self, scope_of_work: List[str]) -> str:
        """
        تحديد نوع المشروع بناءً على نطاق العمل
        
        المعاملات:
        ----------
        scope_of_work : List[str]
            نطاق العمل
            
        المخرجات:
        --------
        str
            نوع المشروع
        """
        # كلمات مفتاحية لكل نوع من المشاريع
        keywords = {
            "building": ["مبنى", "بناء", "تشييد", "عمارة", "هيكل", "مركز"],
            "roads": ["طريق", "جسر", "نفق", "تقاطع", "دوار", "شارع"],
            "infrastructure": ["بنية تحتية", "شبكة", "صرف", "مياه", "كهرباء", "اتصالات"],
            "renovation": ["ترميم", "إصلاح", "صيانة", "تجديد", "تحديث", "تأهيل"],
            "interior": ["تشطيب", "ديكور", "أثاث", "تجهيز", "داخلي", "قواطع"],
            "landscaping": ["تنسيق", "حدائق", "مناظر", "زراعة", "تشجير", "خارجي"]
        }
        
        # حساب عدد الكلمات المفتاحية لكل نوع
        scores = {
            project_type: sum(1 for keyword in keywords_list for item in scope_of_work if keyword in item.lower())
            for project_type, keywords_list in keywords.items()
        }
        
        # تحديد النوع بناءً على أعلى نتيجة
        if not scores or max(scores.values()) == 0:
            return "general"
        
        return max(scores, key=scores.get)
    
    def _determine_material_category(self, description: str) -> str:
        """
        تحديد فئة المادة بناءً على وصفها
        
        المعاملات:
        ----------
        description : str
            وصف المادة
            
        المخرجات:
        --------
        str
            فئة المادة
        """
        # كلمات مفتاحية لكل فئة
        keywords = {
            "مواد بناء أساسية": ["خرسانة", "حديد", "طابوق", "بلوك", "أسمنت", "رمل", "طين", "هيكل"],
            "مواد تشطيب": ["دهان", "بلاط", "سيراميك", "رخام", "جبس", "أسقف", "أرضيات", "زجاج"],
            "مواد كهربائية": ["كهرباء", "أسلاك", "إضاءة", "لوحات", "مفاتيح", "قواطع", "محولات"],
            "مواد سباكة": ["سباكة", "أنابيب", "مواسير", "صرف", "مياه", "خزانات", "صحية"],
            "مواد عزل": ["عزل", "مقاوم", "رطوبة", "حراري", "صوتي", "حريق"],
            "مواد تكييف": ["تكييف", "تبريد", "تدفئة", "تهوية", "مكيفات", "قنوات"]
        }
        
        description_lower = description.lower()
        
        # البحث عن الكلمات المفتاحية في الوصف
        for category, keywords_list in keywords.items():
            for keyword in keywords_list:
                if keyword in description_lower:
                    return category
        
        # إذا لم يتم العثور على مطابقة، إرجاع فئة أخرى
        return "مواد أخرى"
    
    def _determine_profit_margin(self, project_info: Dict[str, Any], 
                               scope_of_work: List[str],
                               total_cost: float) -> float:
        """
        تحديد هامش الربح المناسب
        
        المعاملات:
        ----------
        project_info : Dict[str, Any]
            معلومات المشروع
        scope_of_work : List[str]
            نطاق العمل
        total_cost : float
            إجمالي التكاليف
            
        المخرجات:
        --------
        float
            هامش الربح المناسب (نسبة مئوية)
        """
        # الحصول على هامش الربح الأساسي لنوع المشروع
        project_type = self._determine_project_type(scope_of_work)
        base_margin = self.profit_margins.get(project_type, 15.0)
        
        # تعديل هامش الربح بناءً على القطاع
        sector = project_info.get("sector", "general")
        sector_adjustment = self.profit_margins.get("sector_adjustments", {}).get(sector, 0.0)
        
        # تعديل هامش الربح بناءً على الموقع
        location = project_info.get("location", "").lower()
        location_adjustment = 0.0
        
        if "الرياض" in location or "جدة" in location or "الدمام" in location:
            # المدن الرئيسية: هامش ربح أقل بسبب المنافسة
            location_adjustment = -1.0
        elif "نائية" in location or "بعيدة" in location:
            # المناطق النائية: هامش ربح أعلى
            location_adjustment = 2.0
        
        # تعديل هامش الربح بناءً على حجم المشروع
        size_adjustment = 0.0
        
        if total_cost > 10000000:  # مشروع كبير (أكثر من 10 مليون)
            size_adjustment = -2.0  # هامش ربح أقل للمشاريع الكبيرة
        elif total_cost < 1000000:  # مشروع صغير (أقل من مليون)
            size_adjustment = 3.0  # هامش ربح أعلى للمشاريع الصغيرة
        
        # حساب هامش الربح النهائي
        final_margin = base_margin + sector_adjustment + location_adjustment + size_adjustment
        
        # التأكد من أن هامش الربح في النطاق المعقول
        final_margin = max(8.0, min(25.0, final_margin))
        
        return round(final_margin, 1)
    
    def _generate_cashflow(self, labor_costs: Dict[str, float],
                         equipment_costs: Dict[str, float],
                         material_costs: Dict[str, float],
                         indirect_costs: Dict[str, float],
                         other_costs: Dict[str, float],
                         project_duration: int) -> List[Dict[str, Any]]:
        """
        إعداد توقعات التدفق النقدي
        
        المعاملات:
        ----------
        labor_costs : Dict[str, float]
            تكاليف العمالة
        equipment_costs : Dict[str, float]
            تكاليف المعدات
        material_costs : Dict[str, float]
            تكاليف المواد
        indirect_costs : Dict[str, float]
            التكاليف غير المباشرة
        other_costs : Dict[str, float]
            التكاليف الأخرى
        project_duration : int
            مدة المشروع بالأشهر
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            توقعات التدفق النقدي
        """
        cashflow = []
        
        # إجمالي التكاليف
        total_labor_cost = sum(labor_costs.values())
        total_equipment_cost = sum(equipment_costs.values())
        total_material_cost = sum(material_costs.values())
        total_indirect_cost = sum(indirect_costs.values())
        total_other_cost = sum(other_costs.values())
        
        # إجمالي تكلفة المشروع
        total_cost = total_labor_cost + total_equipment_cost + total_material_cost + total_indirect_cost + total_other_cost
        
        # توزيع التكاليف على أشهر المشروع
        for month in range(1, project_duration + 1):
            # حساب نسبة الإنجاز
            progress = min(1.0, month / project_duration)
            
            # حساب التكاليف لهذا الشهر
            if month == 1:
                # الشهر الأول: تكاليف بداية المشروع عالية
                labor_cost = total_labor_cost * 0.1
                equipment_cost = total_equipment_cost * 0.3
                material_cost = total_material_cost * 0.2
                indirect_cost = total_indirect_cost * (1 / project_duration)
                other_cost = total_other_cost * 0.3
            elif month == project_duration:
                # الشهر الأخير: تكاليف نهاية المشروع
                labor_cost = total_labor_cost * 0.15
                equipment_cost = total_equipment_cost * 0.05
                material_cost = total_material_cost * 0.05
                indirect_cost = total_indirect_cost * (1 / project_duration)
                other_cost = total_other_cost * 0.2
            else:
                # الأشهر الوسطى: توزيع متساوٍ نسبيًا
                remaining_months = project_duration - 2  # باستثناء الشهر الأول والأخير
                labor_cost = total_labor_cost * 0.75 / remaining_months
                equipment_cost = total_equipment_cost * 0.65 / remaining_months
                material_cost = total_material_cost * 0.75 / remaining_months
                indirect_cost = total_indirect_cost * (1 / project_duration)
                other_cost = total_other_cost * 0.5 / remaining_months
            
            # حساب الإيرادات المتوقعة (بافتراض دفعات متساوية)
            expected_revenue = (total_cost * 1.15) / project_duration  # إضافة 15% كهامش ربح
            
            # إضافة بيانات التدفق النقدي لهذا الشهر
            cashflow.append({
                "month": month,
                "labor_cost": labor_cost,
                "equipment_cost": equipment_cost,
                "material_cost": material_cost,
                "indirect_cost": indirect_cost,
                "other_cost": other_cost,
                "total_cost": labor_cost + equipment_cost + material_cost + indirect_cost + other_cost,
                "expected_revenue": expected_revenue,
                "net_cashflow": expected_revenue - (labor_cost + equipment_cost + material_cost + indirect_cost + other_cost),
                "progress_percentage": progress * 100
            })
        
        return cashflow
    
    def _load_cost_database(self) -> Dict[str, Any]:
        """
        تحميل قاعدة بيانات التكاليف
        
        المخرجات:
        --------
        Dict[str, Any]
            قاعدة بيانات التكاليف
        """
        try:
            file_path = 'data/templates/cost_database.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"ملف قاعدة بيانات التكاليف غير موجود: {file_path}")
                # إنشاء قاعدة بيانات افتراضية
                return self._create_default_cost_db()
        except Exception as e:
            logger.error(f"فشل في تحميل قاعدة بيانات التكاليف: {str(e)}")
            return self._create_default_cost_db()
    
    def _load_equipment_costs(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل تكاليف المعدات
        
        المخرجات:
        --------
        Dict[str, Dict[str, Any]]
            تكاليف المعدات
        """
        try:
            file_path = 'data/templates/equipment_costs.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"ملف تكاليف المعدات غير موجود: {file_path}")
                # إنشاء بيانات افتراضية
                return self._create_default_equipment_costs()
        except Exception as e:
            logger.error(f"فشل في تحميل تكاليف المعدات: {str(e)}")
            return self._create_default_equipment_costs()
    
    def _load_labor_costs(self) -> Dict[str, Dict[str, Any]]:
        """
        تحميل تكاليف العمالة
        
        المخرجات:
        --------
        Dict[str, Dict[str, Any]]
            تكاليف العمالة
        """
        try:
            file_path = 'data/templates/labor_costs.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"ملف تكاليف العمالة غير موجود: {file_path}")
                # إنشاء بيانات افتراضية
                return self._create_default_labor_costs()
        except Exception as e:
            logger.error(f"فشل في تحميل تكاليف العمالة: {str(e)}")
            return self._create_default_labor_costs()
    
    def _load_profit_margins(self) -> Dict[str, Any]:
        """
        تحميل معدلات الأرباح النموذجية
        
        المخرجات:
        --------
        Dict[str, Any]
            معدلات الأرباح النموذجية
        """
        try:
            # يمكن أن تكون هذه البيانات جزءًا من قاعدة بيانات التكاليف
            profit_margins = self.cost_db.get("profit_margins", {})
            if profit_margins:
                return profit_margins
            else:
                logger.warning("معدلات الأرباح النموذجية غير موجودة في قاعدة البيانات")
                # إنشاء بيانات افتراضية
                return self._create_default_profit_margins()
        except Exception as e:
            logger.error(f"فشل في تحميل معدلات الأرباح النموذجية: {str(e)}")
            return self._create_default_profit_margins()
    
    def _create_default_cost_db(self) -> Dict[str, Any]:
        """
        إنشاء قاعدة بيانات تكاليف افتراضية
        
        المخرجات:
        --------
        Dict[str, Any]
            قاعدة بيانات تكاليف افتراضية
        """
        return {
            "labor_requirements": {
                "building": {
                    "مهندس مدني": 2,
                    "مهندس معماري": 1,
                    "مهندس كهرباء": 1,
                    "مهندس ميكانيكا": 1,
                    "مراقب": 3,
                    "فني": 10,
                    "عامل": 20
                },
                "roads": {
                    "مهندس مدني": 3,
                    "مهندس مساحة": 2,
                    "مراقب": 4,
                    "فني": 8,
                    "عامل": 30
                },
                "infrastructure": {
                    "مهندس مدني": 2,
                    "مهندس كهرباء": 2,
                    "مهندس ميكانيكا": 2,
                    "مراقب": 4,
                    "فني": 15,
                    "عامل": 25
                },
                "renovation": {
                    "مهندس مدني": 1,
                    "مهندس معماري": 1,
                    "مراقب": 2,
                    "فني": 8,
                    "عامل": 15
                },
                "interior": {
                    "مهندس معماري": 2,
                    "مصمم داخلي": 2,
                    "فني": 12,
                    "عامل": 10
                },
                "landscaping": {
                    "مهندس زراعي": 1,
                    "مصمم مناظر": 1,
                    "فني": 5,
                    "عامل": 15
                },
                "general": {
                    "مهندس": 2,
                    "مراقب": 2,
                    "فني": 5,
                    "عامل": 10
                }
            },
            "equipment_requirements": {
                "building": {
                    "رافعة": {
                "monthly_cost": 30000,
                "purchase_cost": 500000,
                "cost_type": "إيجار",
                "maintenance_cost": 5000
            },
            "خلاطة خرسانة": {
                "monthly_cost": 15000,
                "purchase_cost": 200000,
                "cost_type": "إيجار",
                "maintenance_cost": 3000
            },
            "شاحنة نقل": {
                "monthly_cost": 12000,
                "purchase_cost": 300000,
                "cost_type": "إيجار",
                "maintenance_cost": 4000
            },
            "جرافة": {
                "monthly_cost": 25000,
                "purchase_cost": 450000,
                "cost_type": "إيجار",
                "maintenance_cost": 6000
            },
            "دكاكة": {
                "monthly_cost": 10000,
                "purchase_cost": 180000,
                "cost_type": "إيجار",
                "maintenance_cost": 2500
            },
            "حفارة": {
                "monthly_cost": 28000,
                "purchase_cost": 480000,
                "cost_type": "إيجار",
                "maintenance_cost": 7000
            },
            "مولد كهرباء": {
                "monthly_cost": 8000,
                "purchase_cost": 120000,
                "cost_type": "إيجار",
                "maintenance_cost": 2000
            },
            "معدات رصف": {
                "monthly_cost": 18000,
                "purchase_cost": 350000,
                "cost_type": "إيجار",
                "maintenance_cost": 4500
            },
            "معدات لحام": {
                "monthly_cost": 5000,
                "purchase_cost": 50000,
                "cost_type": "شراء",
                "maintenance_cost": 1000
            },
            "معدات هدم": {
                "monthly_cost": 15000,
                "purchase_cost": 200000,
                "cost_type": "إيجار",
                "maintenance_cost": 3500
            },
            "سقالات": {
                "monthly_cost": 500,
                "purchase_cost": 5000,
                "cost_type": "إيجار",
                "maintenance_cost": 500
            },
            "معدات نجارة": {
                "monthly_cost": 7000,
                "purchase_cost": 80000,
                "cost_type": "شراء",
                "maintenance_cost": 1500
            },
            "معدات دهان": {
                "monthly_cost": 4000,
                "purchase_cost": 40000,
                "cost_type": "شراء",
                "maintenance_cost": 1000
            },
            "معدات ري": {
                "monthly_cost": 6000,
                "purchase_cost": 70000,
                "cost_type": "شراء",
                "maintenance_cost": 1200
            },
            "معدات زراعة": {
                "monthly_cost": 5500,
                "purchase_cost": 65000,
                "cost_type": "شراء",
                "maintenance_cost": 1100
            },
            "معدات يدوية": {
                "monthly_cost": 2000,
                "purchase_cost": 25000,
                "cost_type": "شراء",
                "maintenance_cost": 500
            }
        }
    
    def _create_default_labor_costs(self) -> Dict[str, Dict[str, Any]]:
        """
        إنشاء بيانات تكاليف عمالة افتراضية
        
        المخرجات:
        --------
        Dict[str, Dict[str, Any]]
            بيانات تكاليف عمالة افتراضية
        """
        return {
            "مهندس مدني": {
                "monthly_cost": 15000,
                "nationality": "سعودي",
                "experience_years": 5,
                "availability": "عالية"
            },
            "مهندس معماري": {
                "monthly_cost": 14000,
                "nationality": "سعودي",
                "experience_years": 5,
                "availability": "عالية"
            },
            "مهندس كهرباء": {
                "monthly_cost": 14500,
                "nationality": "سعودي",
                "experience_years": 5,
                "availability": "متوسطة"
            },
            "مهندس ميكانيكا": {
                "monthly_cost": 14800,
                "nationality": "سعودي",
                "experience_years": 5,
                "availability": "متوسطة"
            },
            "مهندس مساحة": {
                "monthly_cost": 13000,
                "nationality": "سعودي",
                "experience_years": 4,
                "availability": "متوسطة"
            },
            "مهندس زراعي": {
                "monthly_cost": 12000,
                "nationality": "سعودي",
                "experience_years": 4,
                "availability": "منخفضة"
            },
            "مصمم داخلي": {
                "monthly_cost": 12500,
                "nationality": "سعودي",
                "experience_years": 4,
                "availability": "متوسطة"
            },
            "مصمم مناظر": {
                "monthly_cost": 12000,
                "nationality": "سعودي",
                "experience_years": 4,
                "availability": "منخفضة"
            },
            "مراقب": {
                "monthly_cost": 9000,
                "nationality": "سعودي",
                "experience_years": 8,
                "availability": "عالية"
            },
            "فني": {
                "monthly_cost": 6000,
                "nationality": "غير سعودي",
                "experience_years": 10,
                "availability": "عالية"
            },
            "عامل": {
                "monthly_cost": 3500,
                "nationality": "غير سعودي",
                "experience_years": 5,
                "availability": "عالية"
            },
            "مهندس": {
                "monthly_cost": 14000,
                "nationality": "سعودي",
                "experience_years": 5,
                "availability": "عالية"
            }
        }
    
    def _create_default_profit_margins(self) -> Dict[str, Any]:
        """
        إنشاء بيانات معدلات أرباح افتراضية
        
        المخرجات:
        --------
        Dict[str, Any]
            بيانات معدلات أرباح افتراضية
        """
        return {
            "building": 15.0,
            "roads": 12.0,
            "infrastructure": 14.0,
            "renovation": 18.0,
            "interior": 20.0,
            "landscaping": 22.0,
            "general": 15.0,
            "sector_adjustments": {
                "حكومي": -2.0,
                "خاص": 2.0,
                "نفط وغاز": 3.0,
                "صناعي": 1.0,
                "تجاري": 0.0,
                "سكني": -1.0
            }
        }ة": 1,
                    "خلاطة خرسانة": 2,
                    "شاحنة نقل": 3,
                    "مولد كهرباء": 2,
                    "معدات يدوية": 10
                },
                "roads": {
                    "جرافة": 2,
                    "دكاكة": 3,
                    "شاحنة نقل": 5,
                    "معدات رصف": 2,
                    "معدات يدوية": 10
                },
                "infrastructure": {
                    "حفارة": 3,
                    "شاحنة نقل": 4,
                    "مولد كهرباء": 2,
                    "معدات لحام": 5,
                    "معدات يدوية": 15
                },
                "renovation": {
                    "سقالات": 20,
                    "شاحنة نقل": 1,
                    "مولد كهرباء": 1,
                    "معدات هدم": 3,
                    "معدات يدوية": 10
                },
                "interior": {
                    "معدات نجارة": 5,
                    "معدات دهان": 5,
                    "سقالات": 10,
                    "مولد كهرباء": 1,
                    "معدات يدوية": 15
                },
                "landscaping": {
                    "جرافة صغيرة": 1,
                    "معدات حفر": 3,
                    "معدات ري": 5,
                    "معدات زراعة": 5,
                    "شاحنة نقل": 1
                },
                "general": {
                    "شاحنة نقل": 1,
                    "مولد كهرباء": 1,
                    "معدات يدوية": 5
                }
            },
            "material_prices": {
                "مواد بناء أساسية": 1000,
                "مواد تشطيب": 1500,
                "مواد كهربائية": 2000,
                "مواد سباكة": 1800,
                "مواد عزل": 2200,
                "مواد تكييف": 2500,
                "مواد أخرى": 1200
            },
            "profit_margins": {
                "building": 15.0,
                "roads": 12.0,
                "infrastructure": 14.0,
                "renovation": 18.0,
                "interior": 20.0,
                "landscaping": 22.0,
                "general": 15.0,
                "sector_adjustments": {
                    "حكومي": -2.0,
                    "خاص": 2.0,
                    "نفط وغاز": 3.0,
                    "صناعي": 1.0,
                    "تجاري": 0.0,
                    "سكني": -1.0
                }
            }
        }
    
    def _create_default_equipment_costs(self) -> Dict[str, Dict[str, Any]]:
        """
        إنشاء بيانات تكاليف معدات افتراضية
        
        المخرجات:
        --------
        Dict[str, Dict[str, Any]]
            بيانات تكاليف معدات افتراضية
        """
        return {
            "رافع"""
محلل تقدير التكاليف للمناقصات
يقوم بتحليل وتقدير تكاليف المشروع وإعداد ميزانية تقديرية
"""

import re
import json
import logging
import os
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional, Union
import numpy as np

logger = logging.getLogger(__name__)

class CostEstimator:
    """
    محلل تقدير التكاليف للمناقصات
    """
    
    def __init__(self, config=None):
        """
        تهيئة محلل التكاليف
        
        المعاملات:
        ----------
        config : Dict, optional
            إعدادات المحلل
        """
        self.config = config or {}
        
        # تحميل قواعد بيانات التكاليف
        self.cost_db = self._load_cost_database()
        self.equipment_costs = self._load_equipment_costs()
        self.labor_costs = self._load_labor_costs()
        
        # تحميل معدلات الأرباح النموذجية
        self.profit_margins = self._load_profit_margins()
        
        logger.info("تم تهيئة محلل تقدير التكاليف")
    
    def estimate(self, extracted_text: str) -> Dict[str, Any]:
        """
        تقدير تكاليف المشروع من نص المناقصة
        
        المعاملات:
        ----------
        extracted_text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        Dict[str, Any]
            تقديرات التكاليف
        """
        try:
            logger.info("بدء تقدير تكاليف المشروع")
            
            # استخراج معلومات المشروع
            project_info = self._extract_project_info(extracted_text)
            
            # استخراج نطاق العمل
            scope_of_work = self._extract_scope_of_work(extracted_text)
            
            # استخراج المدة الزمنية
            project_duration = self._extract_project_duration(extracted_text)
            
            # استخراج الكميات والبنود
            quantities = self._extract_quantities(extracted_text)
            
            # حساب تكاليف العمالة
            labor_costs = self._calculate_labor_costs(scope_of_work, project_duration)
            
            # حساب تكاليف المعدات
            equipment_costs = self._calculate_equipment_costs(scope_of_work, project_duration)
            
            # حساب تكاليف المواد
            material_costs = self._calculate_material_costs(quantities)
            
            # حساب التكاليف غير المباشرة
            indirect_costs = self._calculate_indirect_costs(
                labor_costs, equipment_costs, material_costs, project_duration
            )
            
            # حساب التكاليف الأخرى
            other_costs = self._calculate_other_costs(project_info)
            
            # إجمالي التكاليف
            total_cost = sum([
                sum(labor_costs.values()),
                sum(equipment_costs.values()),
                sum(material_costs.values()),
                sum(indirect_costs.values()),
                sum(other_costs.values())
            ])
            
            # تحديد هامش الربح المناسب
            profit_margin = self._determine_profit_margin(
                project_info, scope_of_work, total_cost
            )
            
            # حساب قيمة العرض المقترحة
            profit_amount = total_cost * (profit_margin / 100)
            proposed_bid = total_cost + profit_amount
            
            # إعداد توقعات التدفق النقدي
            cashflow = self._generate_cashflow(
                labor_costs, equipment_costs, material_costs, 
                indirect_costs, other_costs, project_duration
            )
            
            # إعداد النتائج
            results = {
                "total_cost": total_cost,
                "profit_margin": profit_margin,
                "profit_amount": profit_amount,
                "proposed_bid": proposed_bid,
                "project_duration": project_duration,
                "breakdown": {
                    "labor": labor_costs,
                    "equipment": equipment_costs,
                    "material": material_costs,
                    "indirect": indirect_costs,
                    "other": other_costs
                },
                "cashflow": cashflow,
                "project_info": project_info,
                "scope_of_work": scope_of_work
            }
            
            logger.info(f"اكتمل تقدير التكاليف: {total_cost:,.2f} ريال، هامش ربح {profit_margin:.1f}%")
            return results
            
        except Exception as e:
            logger.error(f"فشل في تقدير التكاليف: {str(e)}")
            return {
                "total_cost": 0,
                "profit_margin": 0,
                "profit_amount": 0,
                "proposed_bid": 0,
                "project_duration": 0,
                "breakdown": {
                    "labor": {},
                    "equipment": {},
                    "material": {},
                    "indirect": {},
                    "other": {}
                },
                "cashflow": [],
                "error": str(e)
            }
    
    def _extract_project_info(self, text: str) -> Dict[str, Any]:
        """
        استخراج معلومات المشروع من النص
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        Dict[str, Any]
            معلومات المشروع
        """
        info = {
            "title": "غير محدد",
            "location": "غير محدد",
            "client": "غير محدد",
            "sector": "غير محدد",
            "estimated_value": 0
        }
        
        # البحث عن عنوان المشروع
        title_patterns = [
            r'اسم المشروع[:\s]+(.*?)(?:\n|$)',
            r'عنوان المشروع[:\s]+(.*?)(?:\n|$)',
            r'مسمى المشروع[:\s]+(.*?)(?:\n|$)',
            r'المشروع[:\s]+(.*?)(?:\n|$)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info["title"] = match.group(1).strip()
                break
        
        # البحث عن موقع المشروع
        location_patterns = [
            r'موقع المشروع[:\s]+(.*?)(?:\n|$)',
            r'الموقع[:\s]+(.*?)(?:\n|$)',
            r'المدينة[:\s]+(.*?)(?:\n|$)',
            r'المنطقة[:\s]+(.*?)(?:\n|$)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info["location"] = match.group(1).strip()
                break
        
        # البحث عن العميل
        client_patterns = [
            r'العميل[:\s]+(.*?)(?:\n|$)',
            r'صاحب العمل[:\s]+(.*?)(?:\n|$)',
            r'الجهة المالكة[:\s]+(.*?)(?:\n|$)',
            r'الجهة المعلنة[:\s]+(.*?)(?:\n|$)'
        ]
        
        for pattern in client_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info["client"] = match.group(1).strip()
                break
        
        # البحث عن القطاع
        sector_patterns = [
            r'القطاع[:\s]+(.*?)(?:\n|$)',
            r'نوع المشروع[:\s]+(.*?)(?:\n|$)',
            r'فئة المشروع[:\s]+(.*?)(?:\n|$)',
            r'تصنيف المشروع[:\s]+(.*?)(?:\n|$)'
        ]
        
        for pattern in sector_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info["sector"] = match.group(1).strip()
                break
        
        # البحث عن القيمة التقديرية
        value_patterns = [
            r'القيمة التقديرية[:\s]+.*?(\d[\d,\.]+)\s*ريال',
            r'التكلفة التقديرية[:\s]+.*?(\d[\d,\.]+)\s*ريال',
            r'الميزانية التقديرية[:\s]+.*?(\d[\d,\.]+)\s*ريال',
            r'قيمة المشروع[:\s]+.*?(\d[\d,\.]+)\s*ريال'
        ]
        
        for pattern in value_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value_str = match.group(1).replace(',', '')
                try:
                    info["estimated_value"] = float(value_str)
                except ValueError:
                    pass
                break
        
        return info
    
    def _extract_scope_of_work(self, text: str) -> List[str]:
        """
        استخراج نطاق العمل من النص
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[str]
            قائمة ببنود نطاق العمل
        """
        scope_items = []
        
        # البحث عن قسم نطاق العمل
        scope_section_patterns = [
            r'نطاق العمل.*?(?=\n\n|\Z)',
            r'وصف المشروع.*?(?=\n\n|\Z)',
            r'وصف الأعمال.*?(?=\n\n|\Z)',
            r'الأعمال المطلوبة.*?(?=\n\n|\Z)',
            r'بنود الأعمال.*?(?=\n\n|\Z)'
        ]
        
        scope_section = ""
        for pattern in scope_section_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                scope_section = match.group(0)
                break
        
        if not scope_section:
            # إذا لم نجد قسمًا محددًا، نحاول البحث عن قائمة بنقاط
            bullet_lists = re.findall(r'(?:^|\n)(?:[•\-*]\s+.*(?:\n|$))+', text)
            if bullet_lists:
                longest_list = max(bullet_lists, key=len)
                scope_section = longest_list
        
        # استخراج العناصر من القسم
        if scope_section:
            # البحث عن القوائم بنقاط
            bullet_items = re.findall(r'[•\-*]\s+(.*?)(?:\n|$)', scope_section)
            if bullet_items:
                scope_items.extend([item.strip() for item in bullet_items if item.strip()])
            
            # إذا لم نجد قوائم بنقاط، نقسم النص إلى فقرات
            if not scope_items:
                paragraphs = re.split(r'\n\s*\n', scope_section)
                for paragraph in paragraphs[1:]:  # تخطي العنوان
                    if paragraph.strip():
                        scope_items.append(paragraph.strip())
        
        # إذا لم نتمكن من استخراج أي عناصر، نستخدم القيم الافتراضية
        if not scope_items:
            # التخمين بناءً على عنوان المشروع
            project_info = self._extract_project_info(text)
            title = project_info.get("title", "").lower()
            
            # تخمين نطاق العمل بناءً على الكلمات المفتاحية في العنوان
            if any(word in title for word in ["بناء", "تشييد", "إنشاء", "مبنى"]):
                scope_items = [
                    "أعمال الحفر والردم",
                    "أعمال الخرسانة",
                    "أعمال البناء",
                    "أعمال التشطيبات",
                    "أعمال الكهرباء",
                    "أعمال السباكة",
                    "أعمال التكييف"
                ]
            elif any(word in title for word in ["طريق", "جسر", "كوبري", "نفق"]):
                scope_items = [
                    "أعمال الحفر والردم",
                    "أعمال الأساسات",
                    "أعمال الخرسانة",
                    "أعمال الأسفلت",
                    "أعمال الإنارة",
                    "أعمال التصريف"
                ]
            elif any(word in title for word in ["صيانة", "تأهيل", "ترميم"]):
                scope_items = [
                    "أعمال الفحص والتقييم",
                    "أعمال الصيانة الوقائية",
                    "أعمال الإصلاح",
                    "أعمال الاستبدال",
                    "أعمال التنظيف"
                ]
            else:
                scope_items = [
                    "أعمال التحضير والتجهيز",
                    "أعمال التنفيذ",
                    "أعمال التشطيب",
                    "أعمال الاختبار والتشغيل",
                    "أعمال التسليم"
                ]
        
        return scope_items
    
    def _extract_project_duration(self, text: str) -> int:
        """
        استخراج المدة الزمنية للمشروع بالأشهر
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        int
            مدة المشروع بالأشهر
        """
        # البحث عن المدة الزمنية
        duration_patterns = [
            r'مدة المشروع[:\s]+(\d+)\s*(?:شهر|أشهر|شهور)',
            r'مدة التنفيذ[:\s]+(\d+)\s*(?:شهر|أشهر|شهور)',
            r'مدة العقد[:\s]+(\d+)\s*(?:شهر|أشهر|شهور)',
            r'المدة الزمنية[:\s]+(\d+)\s*(?:شهر|أشهر|شهور)',
            r'فترة التنفيذ[:\s]+(\d+)\s*(?:شهر|أشهر|شهور)',
            
            # البحث عن المدة بالأيام
            r'مدة المشروع[:\s]+(\d+)\s*(?:يوم|أيام)',
            r'مدة التنفيذ[:\s]+(\d+)\s*(?:يوم|أيام)',
            r'مدة العقد[:\s]+(\d+)\s*(?:يوم|أيام)',
            r'المدة الزمنية[:\s]+(\d+)\s*(?:يوم|أيام)',
            r'فترة التنفيذ[:\s]+(\d+)\s*(?:يوم|أيام)',
            
            # البحث عن المدة بالسنوات
            r'مدة المشروع[:\s]+(\d+)\s*(?:سنة|سنوات)',
            r'مدة التنفيذ[:\s]+(\d+)\s*(?:سنة|سنوات)',
            r'مدة العقد[:\s]+(\d+)\s*(?:سنة|سنوات)',
            r'المدة الزمنية[:\s]+(\d+)\s*(?:سنة|سنوات)',
            r'فترة التنفيذ[:\s]+(\d+)\s*(?:سنة|سنوات)'
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                duration = int(match.group(1))
                
                # تحويل المدة إلى أشهر
                if "يوم" in pattern or "أيام" in pattern:
                    return max(1, round(duration / 30))
                elif "سنة" in pattern or "سنوات" in pattern:
                    return duration * 12
                else:
                    return duration
        
        # إذا لم نتمكن من استخراج المدة، نستخدم قيمة افتراضية
        return 12  # قيمة افتراضية: 12 شهر
    
    def _extract_quantities(self, text: str) -> List[Dict[str, Any]]:
        """
        استخراج الكميات والبنود من النص
        
        المعاملات:
        ----------
        text : str
            النص المستخرج من المناقصة
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة بالكميات والبنود
        """
        quantities = []
        
        # البحث عن جداول الكميات
        table_sections = self._extract_tables(text)
        
        for section in table_sections:
            # تقسيم الجدول إلى أسطر
            lines = section.strip().split('\n')
            
            # تخطي العنوان
            for i in range(1, len(lines)):
                line = lines[i].strip()
                if not line:
                    continue
                
                # تقسيم السطر إلى أعمدة
                if '|' in line:
                    columns = [col.strip() for col in line.split('|')]
                else:
                    # محاولة تقسيم بناءً على المسافات المتعددة
                    columns = re.split(r'\s{2,}', line)
                
                if len(columns) < 2:
                    continue
                
                # استخراج البيانات
                item = {}
                
                # تحديد الأعمدة المختلفة بناءً على طول القائمة والكلمات المفتاحية
                if len(columns) >= 4:
                    # افتراض: رقم البند | الوصف | الكمية | الوحدة
                    item = {
                        "id": columns[0],
                        "description": columns[1],
                        "quantity": self._extract_number(columns[2]),
                        "unit": columns[3] if len(columns) > 3 else ""
                    }
                elif len(columns) == 3:
                    # افتراض: الوصف | الكمية | الوحدة
                    item = {
                        "description": columns[0],
                        "quantity": self._extract_number(columns[1]),
                        "unit": columns[2]
                    }
                elif len(columns) == 2:
                    # افتراض: الوصف | الكمية
                    item = {
                        "description": columns[0],
                        "quantity": self._extract_number(columns[1]),
                        "unit": ""
                    }
                
                # إضافة العنصر إذا كان يحتوي على وصف وكمية صالحة
                if item.get("description") and item.get("quantity", 0) > 0:
                    quantities.append(item)
        
        # إذا لم نتمكن من استخراج أي كميات، نستخرج من النص العادي
        if not quantities:
            # البحث عن الكميات في النص
            quantity_matches = re.finditer(r'(?:توريد|تركيب|تنفيذ)\s+(\d+(?:,\d+)?(?:\.\d+)?)\s+(\w+)\s+(?:من|لـ|ل)\s+(.+?)(?:\.|\n)', text)
            
            for match in quantity_matches:
                quantities.append({
                    "description": match.group(3).strip(),
                    "quantity": self._extract_number(match.group(1)),
                    "unit": match.group(2).strip()
                })
        
        return quantities
    
    def _extract_number(self, text: str) -> float:
        """
        استخراج رقم من نص
        
        المعاملات:
        ----------
        text : str
            النص المحتوي على الرقم
            
        المخرجات:
        --------
        float
            الرقم المستخرج
        """
        if not text:
            return 0
        
        # إزالة الفواصل وتحويل النص إلى رقم
        text = text.replace(',', '')
        match = re.search(r'\d+(?:\.\d+)?', text)
        
        if match:
            try:
                return float(match.group(0))
            except ValueError:
                pass
        
        return 0
    
    def _calculate_labor_costs(self, scope_of_work: List[str], project_duration: int) -> Dict[str, float]:
        """
        حساب تكاليف العمالة
        
        المعاملات:
        ----------
        scope_of_work : List[str]
            نطاق العمل
        project_duration : int
            مدة المشروع بالأشهر
            
        المخرجات:
        --------
        Dict[str, float]
            تكاليف العمالة
        """
        labor_costs = {}
        
        # تحديد نوع المشروع بناءً على نطاق العمل
        project_type = self._determine_project_type(scope_of_work)
        
        # الحصول على العمالة المطلوبة لهذا النوع من المشاريع
        required_labor = self.cost_db.get("labor_requirements", {}).get(project_type, {})
        
        # حساب تكاليف كل نوع من العمالة
        for labor_type, count in required_labor.items():
            # الحصول على التكلفة الشهرية
            monthly_cost = self.labor_costs.get(labor_type, {}).get("monthly_cost", 0)
            
            # حساب التكلفة الإجمالية
            total_cost = count * monthly_cost * project_duration
            
            # إضافة التكلفة إلى القاموس
            labor_costs[labor_type] = total_cost
        
        return labor_costs
    
    def _calculate_equipment_costs(self, scope_of_work: List[str], project_duration: int) -> Dict[str, float]:
        """
        حساب تكاليف المعدات بناءً على نطاق العمل ومدة المشروع.

        المعاملات:
        ----------
        scope_of_work : List[str]
            قائمة تحتوي على الأعمال المطلوبة في المشروع.
        project_duration : int
            مدة المشروع بالأشهر.
            
        المخرجات:
        --------
        Dict[str, float]
            قاموس يحتوي على تكلفة كل نوع من المعدات المطلوبة في المشروع.
        """
        equipment_costs = {}

        # قائمة أسعار المعدات بناءً على نوع العمل (يمكن توسيعها حسب الحاجة)
        equipment_prices = {
            "حفار": 5000,   # تكلفة يومية للحفار
            "رافعة": 8000,  # تكلفة يومية للرافعة
            "خلاطة خرسانة": 3000, # تكلفة يومية للخلاطة
            "شاحنة نقل": 2000,  # تكلفة يومية لشاحنة النقل
            "مولد كهربائي": 1500 # تكلفة يومية للمولد الكهربائي
        }

        # عدد الأيام التشغيلية شهريًا (فرضًا 22 يوم عمل في الشهر)
        working_days_per_month = 22
        total_days = project_duration * working_days_per_month

        # تحديد المعدات المطلوبة بناءً على نطاق العمل
        for work in scope_of_work:
            for equipment, daily_cost in equipment_prices.items():
                if equipment in work:
                    # إذا كانت المعدات مطلوبة، نحسب التكلفة الإجمالية لمدة المشروع
                    equipment_costs[equipment] = total_days * daily_cost
        
        return equipment_costs
