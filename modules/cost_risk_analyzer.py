local_content_percentage = (local_content / total_cost * 100) if total_cost > 0 else 0
        
        # حساب المحتوى المحلي حسب الفئة
        categories = {}
        for item in items:
            category = item.get("category", "أخرى")
            cost = item.get("cost", 0)
            local_contribution = item.get("local_content_contribution", 0)
            local_amount = cost * local_contribution / 100
            
            if category in categories:
                categories[category]["total"] += cost
                categories[category]["local"] += local_amount
            else:
                categories[category] = {
                    "total": cost,
                    "local": local_amount
                }
        
        local_content_by_category = {}
        for category, data in categories.items():
            local_content_by_category[category] = (data["local"] / data["total"] * 100) if data["total"] > 0 else 0
        
        # الهدف المرجعي للمحتوى المحلي
        target_local_content = self.reference_data.get("target_local_content", 40)
        local_content_gap = target_local_content - local_content_percentage
        
        # إمكانية التحسين
        import_items = [item for item in items if item.get("source_type") == "import"]
        improvement_potential = sum(item.get("cost", 0) for item in import_items) / total_cost * 100 if total_cost > 0 else 0
        
        return {
            "local_content_percentage": local_content_percentage,
            "local_content_by_category": local_content_by_category,
            "target_local_content": target_local_content,
            "local_content_gap": local_content_gap,
            "improvement_potential": improvement_potential
        }
    
    def _identify_procurement_improvements(self, procurement_costs: Dict[str, Any],
                                         suppliers_analysis: Dict[str, Any],
                                         local_content_analysis: Dict[str, Any]) -> List[str]:
        """
        تحديد فرص تحسين المشتريات
        
        المعاملات:
        ----------
        procurement_costs : Dict[str, Any]
            تحليل تكاليف المشتريات
        suppliers_analysis : Dict[str, Any]
            تحليل الموردين
        local_content_analysis : Dict[str, Any]
            تحليل المحتوى المحلي
            
        المخرجات:
        --------
        List[str]
            فرص تحسين المشتريات
        """
        improvements = []
        
        # تحسين تكاليف المشتريات
        if procurement_costs["cost_efficiency"] < 0:
            improvements.append("تحسين كفاءة تكاليف المشتريات من خلال إعادة التفاوض مع الموردين وتوحيد الطلبات.")
        
        # تحسين تنوع الموردين
        if suppliers_analysis["supplier_diversity"] < 30:
            improvements.append("زيادة تنوع الموردين لتقليل مخاطر سلسلة الإمداد وتحسين المرونة.")
        
        # تحسين نسبة الموردين المحليين
        if suppliers_analysis["local_percentage"] < 50:
            improvements.append("زيادة نسبة الموردين المحليين لتعزيز المحتوى المحلي وتقليل تكاليف النقل.")
        
        # تحسين المحتوى المحلي
        if local_content_analysis["local_content_gap"] > 0:
            improvements.append(f"سد فجوة المحتوى المحلي البالغة {local_content_analysis['local_content_gap']:.1f}% للوصول إلى الهدف.")
        
        # تحسين تركيز الموردين
        high_concentration = [supplier for supplier, percentage in suppliers_analysis["supplier_concentration"].items() if percentage > 30]
        if high_concentration:
            improvements.append(f"تقليل الاعتماد على الموردين الرئيسيين ({', '.join(high_concentration)}) لتقليل المخاطر.")
        
        # إضافة توصيات عامة
        improvements.extend([
            "تطبيق نظام تقييم الموردين وتحفيز الأداء المتميز.",
            "تحسين عملية التخطيط للمشتريات لتقليل الطلبات العاجلة والتكاليف الإضافية.",
            "تطوير قاعدة بيانات للموردين وتعزيز الشفافية في عملية اختيار الموردين.",
            "الاستفادة من التكنولوجيا لأتمتة عمليات المشتريات وتحسين الكفاءة."
        ])
        
        return improvements
    
    def _generate_procurement_summary(self, procurement_costs: Dict[str, Any],
                                    suppliers_analysis: Dict[str, Any],
                                    local_content_analysis: Dict[str, Any]) -> str:
        """
        إعداد ملخص لتقرير المشتريات
        
        المعاملات:
        ----------
        procurement_costs : Dict[str, Any]
            تحليل تكاليف المشتريات
        suppliers_analysis : Dict[str, Any]
            تحليل الموردين
        local_content_analysis : Dict[str, Any]
            تحليل المحتوى المحلي
            
        المخرجات:
        --------
        str
            ملخص تقرير المشتريات
        """
        summary = "ملخص تقرير المشتريات:\n\n"
        
        # ملخص التكاليف
        summary += "1. تكاليف المشتريات:\n"
        summary += f"   - إجمالي تكاليف المشتريات: {procurement_costs['total_procurement_cost']:,.0f} ريال\n"
        summary += f"   - نسبة المشتريات المحلية: {procurement_costs['local_percentage']:.1f}%\n"
        if procurement_costs['cost_efficiency'] > 0:
            summary += f"   - كفاءة التكلفة: {procurement_costs['cost_efficiency']:.1f}% (وفر عن المتوسط)\n"
        else:
            summary += f"   - كفاءة التكلفة: {-procurement_costs['cost_efficiency']:.1f}% (تجاوز عن المتوسط)\n"
        
        # ملخص الموردين
        summary += "\n2. تحليل الموردين:\n"
        summary += f"   - عدد الموردين: {suppliers_analysis['total_suppliers']}\n"
        summary += f"   - نسبة الموردين المحليين: {suppliers_analysis['local_percentage']:.1f}%\n"
        summary += f"   - تنوع الموردين: {suppliers_analysis['supplier_diversity']:.1f}%\n"
        
        # ملخص المحتوى المحلي
        summary += "\n3. تحليل المحتوى المحلي:\n"
        summary += f"   - نسبة المحتوى المحلي الحالية: {local_content_analysis['local_content_percentage']:.1f}%\n"
        summary += f"   - نسبة المحتوى المحلي المستهدفة: {local_content_analysis['target_local_content']:.1f}%\n"
        summary += f"   - فجوة المحتوى المحلي: {local_content_analysis['local_content_gap']:.1f}%\n"
        summary += f"   - إمكانية تحسين المحتوى المحلي: {local_content_analysis['improvement_potential']:.1f}%\n"
        
        return summary
    
    def _generate_default_mitigation(self, risk: Dict[str, Any]) -> str:
        """
        إنشاء استراتيجية تخفيف افتراضية للمخاطرة
        
        المعاملات:
        ----------
        risk : Dict[str, Any]
            المخاطرة
            
        المخرجات:
        --------
        str
            استراتيجية التخفيف
        """
        # استخراج نوع المخاطرة
        risk_name = risk.get("name", "").lower()
        risk_type = risk.get("type", "").lower()
        
        if "أسعار" in risk_name or "تكلفة" in risk_name:
            return "تأمين عقود توريد بأسعار ثابتة وإعداد ميزانية احتياطية للتغييرات المحتملة في الأسعار."
        elif "دفعات" in risk_name or "تمويل" in risk_name or "سيولة" in risk_name:
            return "وضع شروط دفع واضحة في العقد وتأمين تسهيلات ائتمانية احتياطية وإعداد خطة للتدفق النقدي."
        elif "عملات" in risk_name or "صرف" in risk_name:
            return "استخدام آليات التحوط والتعاقد بالعملة المحلية حيثما أمكن."
        elif risk_type == "financial":
            return "إعداد خطة مالية بديلة وتخصيص احتياطي طوارئ مالي بنسبة مناسبة من قيمة المشروع."
        else:
            return "تحديد وتقييم المخاطر بشكل دوري ووضع خطط بديلة للتعامل معها."
    
    def _generate_overrun_mitigation(self, category: str, deviation_percentage: float) -> str:
        """
        إنشاء استراتيجية تخفيف لتجاوز التكاليف
        
        المعاملات:
        ----------
        category : str
            فئة التكلفة
        deviation_percentage : float
            نسبة التجاوز
            
        المخرجات:
        --------
        str
            استراتيجية التخفيف
        """
        category = category.lower()
        
        if "مواد" in category:
            return "البحث عن موردين بديلين وإعادة التفاوض على الأسعار وتحسين إدارة المخزون."
        elif "عمالة" in category:
            return "تحسين إنتاجية العمالة وإعادة توزيع المهام وتقييم إمكانية الاستعانة بمقاولي الباطن."
        elif "معدات" in category:
            return "تحسين استغلال المعدات ومراجعة خيارات الشراء مقابل الإيجار وتقليل أوقات التوقف."
        elif "مقاولين" in category or "باطن" in category:
            return "مراجعة عقود مقاولي الباطن وإعادة التفاوض على الأسعار وتحسين إدارة العقود."
        elif "إدارة" in category or "غير مباشرة" in category:
            return "ترشيد المصاريف الإدارية وتقليل التكاليف غير المباشرة ومراجعة الهيكل التنظيمي."
        else:
            return "مراجعة بنود التكلفة وتحديد فرص التوفير وتطبيق إجراءات ضبط التكاليف."
    
    def _generate_deviation_recommendation(self, category: str, expected_deviation: float) -> str:
        """
        إنشاء توصية للتعامل مع الانحراف المتوقع
        
        المعاملات:
        ----------
        category : str
            فئة التكلفة
        expected_deviation : float
            الانحراف المتوقع
            
        المخرجات:
        --------
        str
            التوصية
        """
        category = category.lower()
        
        if expected_deviation > 0:
            # توصيات لتجاوز التكاليف
            if "مواد" in category:
                return "مراجعة بدائل المواد وتوحيد المشتريات للاستفادة من وفورات الحجم وتأمين العقود مسبقًا."
            elif "عمالة" in category:
                return "تحسين جدولة العمالة وزيادة الإنتاجية وتقييم إمكانية الاستعانة بمقاولي الباطن."
            elif "معدات" in category:
                return "تحسين إدارة المعدات وزيادة كفاءة الاستخدام ومراجعة خيارات الإيجار بدلاً من الشراء."
            else:
                return "تنفيذ إجراءات ضبط التكاليف ومراقبة الإنفاق بشكل دوري ومراجعة الميزانية."
        else:
            # توصيات للوفر في التكاليف
            if abs(expected_deviation) > 10:
                return "مراجعة تقديرات التكلفة لضمان عدم المبالغة وإعادة توزيع الموارد للأنشطة الحرجة."
            else:
                return "الاستفادة من الوفر المتوقع في تعزيز جودة المشروع أو تغطية تجاوزات محتملة في بنود أخرى."
    
    def _load_reference_data(self) -> Dict[str, Any]:
        """
        تحميل البيانات المرجعية
        
        المخرجات:
        --------
        Dict[str, Any]
            البيانات المرجعية
        """
        try:
            file_path = 'data/templates/cost_reference_data.json'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"ملف البيانات المرجعية غير موجود: {file_path}")
                # إنشاء بيانات مرجعية افتراضية
                return self._create_default_reference_data()
        except Exception as e:
            logger.error(f"فشل في تحميل البيانات المرجعية: {str(e)}")
            return self._create_default_reference_data()
    
    def _create_default_reference_data(self) -> Dict[str, Any]:
        """
        إنشاء بيانات مرجعية افتراضية
        
        المخرجات:
        --------
        Dict[str, Any]
            البيانات المرجعية الافتراضية
        """
        return {
            "avg_direct_percentage": 75.0,
            "avg_indirect_percentage": 25.0,
            "avg_profit_margin": 15.0,
            "avg_cost_revenue_ratio": 85.0,
            "avg_roi": 20.0,
            "avg_procurement_cost": 1000000,
            "target_local_content": 40.0,
            "sector_benchmarks": {
                "construction": {
                    "profit_margin": 12.0,
                    "cost_revenue_ratio": 88.0,
                    "direct_percentage": 80.0
                },
                "infrastructure": {
                    "profit_margin": 10.0,
                    "cost_revenue_ratio": 90.0,
                    "direct_percentage": 85.0
                },
                "services": {
                    "profit_margin": 20.0,
                    "cost_revenue_ratio": 80.0,
                    "direct_percentage": 65.0
                }
            },
            "cost_overrun_statistics": {
                "avg_overrun_percentage": 15.0,
                "materials_overrun": 12.0,
                "labor_overrun": 18.0,
                "equipment_overrun": 10.0
            }
        }                        "deviation_percentage": deviation_percentage,
                        "risk_level": risk_level,
                        "impact": "تأثير على هامش الربح وزيادة التكاليف الإجمالية",
                        "mitigation": self._generate_overrun_mitigation(category, deviation_percentage)
                    })
        
        # ترتيب المخاطر حسب نسبة التجاوز
        return sorted(overrun_risks, key=lambda x: x["deviation_percentage"], reverse=True)
    
    def _analyze_cashflow_risks(self, costs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        تحليل مخاطر التدفق النقدي
        
        المعاملات:
        ----------
        costs : Dict[str, Any]
            بيانات التكاليف
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة مخاطر التدفق النقدي
        """
        cashflow_risks = []
        
        # استخراج بيانات التدفق النقدي
        cashflow = costs.get("cashflow", [])
        
        if not cashflow:
            # إنشاء مخاطر افتراضية للتدفق النقدي
            cashflow_risks = [
                {
                    "type": "تأخر الدفعات",
                    "probability": 0.4,
                    "impact": 0.35,
                    "risk_score": 0.14,
                    "description": "تأخر في استلام الدفعات من العميل",
                    "mitigation": "وضع شروط دفع واضحة في العقد وتوفير تمويل احتياطي"
                },
                {
                    "type": "فجوة تمويلية",
                    "probability": 0.3,
                    "impact": 0.4,
                    "risk_score": 0.12,
                    "description": "عدم كفاية التدفق النقدي لتغطية النفقات في بعض الفترات",
                    "mitigation": "تأمين تسهيلات ائتمانية وتحسين إدارة التدفق النقدي"
                },
                {
                    "type": "تغير أسعار الفائدة",
                    "probability": 0.2,
                    "impact": 0.25,
                    "risk_score": 0.05,
                    "description": "زيادة تكاليف التمويل بسبب ارتفاع أسعار الفائدة",
                    "mitigation": "تأمين قروض بأسعار فائدة ثابتة والتفاوض على شروط تمويل مناسبة"
                }
            ]
        else:
            # تحليل بيانات التدفق النقدي لاستخراج المخاطر
            negative_periods = []
            consecutive_negative = 0
            total_periods = len(cashflow)
            
            for i, period in enumerate(cashflow):
                net_flow = period.get("net_cashflow", 0)
                
                if net_flow < 0:
                    consecutive_negative += 1
                    negative_periods.append(i + 1)  # رقم الفترة (مبتدئًا من 1)
                else:
                    consecutive_negative = 0
            
            # تقييم المخاطر بناءً على التحليل
            if len(negative_periods) > 0:
                risk = {
                    "type": "تدفق نقدي سلبي",
                    "probability": min(0.7, len(negative_periods) / total_periods),
                    "impact": min(0.8, 0.2 + (len(negative_periods) / total_periods) * 0.6),
                    "affected_periods": negative_periods,
                    "description": f"تدفق نقدي سلبي في {len(negative_periods)} فترات من أصل {total_periods}",
                    "mitigation": "تحسين جدولة الدفعات وترشيد النفقات في الفترات الحرجة"
                }
                risk["risk_score"] = risk["probability"] * risk["impact"]
                cashflow_risks.append(risk)
            
            if consecutive_negative >= 2:
                risk = {
                    "type": "تدفق نقدي سلبي متتالي",
                    "probability": min(0.8, 0.3 + (consecutive_negative / total_periods) * 0.5),
                    "impact": min(0.9, 0.4 + (consecutive_negative / total_periods) * 0.5),
                    "consecutive_periods": consecutive_negative,
                    "description": f"تدفق نقدي سلبي متتالي لمدة {consecutive_negative} فترات",
                    "mitigation": "تأمين تمويل احتياطي وإعادة التفاوض على شروط الدفع"
                }
                risk["risk_score"] = risk["probability"] * risk["impact"]
                cashflow_risks.append(risk)
        
        # ترتيب المخاطر حسب درجة المخاطرة
        return sorted(cashflow_risks, key=lambda x: x.get("risk_score", 0), reverse=True)
    
    def _analyze_profit_impact(self, financial_risks: List[Dict[str, Any]], costs: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل تأثير المخاطر على الأرباح
        
        المعاملات:
        ----------
        financial_risks : List[Dict[str, Any]]
            قائمة المخاطر المالية
        costs : Dict[str, Any]
            بيانات التكاليف
            
        المخرجات:
        --------
        Dict[str, Any]
            تحليل تأثير المخاطر على الأرباح
        """
        # استخراج القيمة التعاقدية وإجمالي التكاليف
        contract_value = costs.get("contract_value", 0)
        direct_costs = costs.get("direct", {})
        indirect_costs = costs.get("indirect", {})
        total_cost = sum(direct_costs.values()) + sum(indirect_costs.values())
        
        if contract_value == 0 or total_cost == 0:
            return {
                "expected_profit": 0,
                "profit_margin": 0,
                "risk_adjusted_profit": 0,
                "risk_adjusted_margin": 0,
                "total_risk_impact": 0,
                "probability_of_negative_profit": 0
            }
        
        # حساب الربح المتوقع وهامش الربح
        expected_profit = contract_value - total_cost
        profit_margin = (expected_profit / contract_value) * 100
        
        # حساب إجمالي تأثير المخاطر
        total_risk_impact = sum(risk.get("financial_impact", 0) * risk.get("probability", 0.5) for risk in financial_risks)
        
        # حساب الربح المعدل بالمخاطر
        risk_adjusted_profit = expected_profit - total_risk_impact
        risk_adjusted_margin = (risk_adjusted_profit / contract_value) * 100
        
        # حساب احتمالية الربح السلبي
        if expected_profit > 0:
            probability_of_negative_profit = min(0.95, total_risk_impact / expected_profit)
        else:
            probability_of_negative_profit = 0.95
        
        return {
            "expected_profit": expected_profit,
            "profit_margin": profit_margin,
            "risk_adjusted_profit": risk_adjusted_profit,
            "risk_adjusted_margin": risk_adjusted_margin,
            "total_risk_impact": total_risk_impact,
            "probability_of_negative_profit": probability_of_negative_profit
        }
    
    def _generate_risk_management_plan(self, financial_risks: List[Dict[str, Any]],
                                     cost_overrun_risks: List[Dict[str, Any]],
                                     cashflow_risks: List[Dict[str, Any]]) -> List[str]:
        """
        إعداد خطة إدارة المخاطر المالية
        
        المعاملات:
        ----------
        financial_risks : List[Dict[str, Any]]
            قائمة المخاطر المالية
        cost_overrun_risks : List[Dict[str, Any]]
            قائمة مخاطر تجاوز التكاليف
        cashflow_risks : List[Dict[str, Any]]
            قائمة مخاطر التدفق النقدي
            
        المخرجات:
        --------
        List[str]
            خطة إدارة المخاطر المالية
        """
        management_plan = ["خطة إدارة المخاطر المالية:"]
        
        # إضافة استراتيجيات للمخاطر المالية العامة
        if financial_risks:
            management_plan.append("\n1. إدارة المخاطر المالية العامة:")
            for i, risk in enumerate(financial_risks[:3]):  # أعلى 3 مخاطر
                management_plan.append(f"   - {risk.get('name', risk.get('type', 'مخاطرة'))}: {risk.get('mitigation', '')}")
        
        # إضافة استراتيجيات لمخاطر تجاوز التكاليف
        if cost_overrun_risks:
            management_plan.append("\n2. إدارة مخاطر تجاوز التكاليف:")
            for i, risk in enumerate(cost_overrun_risks[:3]):  # أعلى 3 مخاطر
                management_plan.append(f"   - {risk.get('category', 'فئة تكلفة')}: {risk.get('mitigation', '')}")
        
        # إضافة استراتيجيات لمخاطر التدفق النقدي
        if cashflow_risks:
            management_plan.append("\n3. إدارة مخاطر التدفق النقدي:")
            for i, risk in enumerate(cashflow_risks):
                management_plan.append(f"   - {risk.get('type', 'مخاطرة')}: {risk.get('mitigation', '')}")
        
        # إضافة إجراءات عامة
        management_plan.extend([
            "\n4. إجراءات عامة لإدارة المخاطر المالية:",
            "   - إنشاء احتياطي مالي للطوارئ بنسبة 5-10% من قيمة المشروع",
            "   - مراقبة التكاليف بشكل أسبوعي وتحديث توقعات التدفق النقدي شهريًا",
            "   - تأمين تسهيلات ائتمانية احتياطية للتعامل مع فجوات التدفق النقدي",
            "   - مراجعة عقود التوريد ووضع آليات لمواجهة تقلبات الأسعار",
            "   - إعداد سيناريوهات بديلة وخطط طوارئ للمخاطر المالية العالية"
        ])
        
        return management_plan
    
    def _forecast_monthly_costs(self, costs: Dict[str, Any], forecast_months: int) -> List[Dict[str, Any]]:
        """
        التنبؤ بالتكاليف الشهرية
        
        المعاملات:
        ----------
        costs : Dict[str, Any]
            بيانات التكاليف
        forecast_months : int
            عدد الأشهر المراد التنبؤ بها
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            التنبؤ بالتكاليف الشهرية
        """
        monthly_forecast = []
        
        # استخراج بيانات التكاليف الشهرية السابقة
        historical_monthly = costs.get("monthly", [])
        
        if not historical_monthly and len(historical_monthly) < 3:
            # إذا لم تكن هناك بيانات تاريخية كافية، قم بإنشاء توقعات افتراضية
            direct_costs = costs.get("direct", {})
            indirect_costs = costs.get("indirect", {})
            total_cost = sum(direct_costs.values()) + sum(indirect_costs.values())
            
            # توزيع التكاليف على الأشهر بشكل افتراضي
            monthly_cost = total_cost / forecast_months
            
            for month in range(1, forecast_months + 1):
                # إضافة تذبذب عشوائي للواقعية
                random_factor = 1 + (np.random.random() * 0.2 - 0.1)  # بين 0.9 و 1.1
                
                forecast = {
                    "month": month,
                    "total_cost": monthly_cost * random_factor,
                    "direct_cost": monthly_cost * 0.7 * random_factor,
                    "indirect_cost": monthly_cost * 0.3 * random_factor,
                    "variance": (random_factor - 1) * 100,
                    "cumulative_cost": monthly_cost * random_factor * month
                }
                
                monthly_forecast.append(forecast)
        else:
            # استخدام البيانات التاريخية للتنبؤ
            # حساب متوسط النمو الشهري
            growth_rates = []
            for i in range(1, len(historical_monthly)):
                prev_cost = historical_monthly[i-1].get("total_cost", 0)
                curr_cost = historical_monthly[i].get("total_cost", 0)
                if prev_cost > 0:
                    growth_rate = (curr_cost - prev_cost) / prev_cost
                    growth_rates.append(growth_rate)
            
            # حساب متوسط معدل النمو
            avg_growth_rate = np.mean(growth_rates) if growth_rates else 0.02
            
            # الحصول على آخر تكلفة شهرية
            last_month = historical_monthly[-1]
            last_month_cost = last_month.get("total_cost", 0)
            last_month_direct = last_month.get("direct_cost", last_month_cost * 0.7)
            last_month_indirect = last_month.get("indirect_cost", last_month_cost * 0.3)
            last_month_number = last_month.get("month", 0)
            last_month_cumulative = last_month.get("cumulative_cost", last_month_cost)
            
            # التنبؤ بالأشهر القادمة
            for i in range(1, forecast_months + 1):
                month_number = last_month_number + i
                
                # حساب التكلفة المتوقعة مع إضافة تذبذب عشوائي
                random_factor = 1 + (np.random.random() * 0.1 - 0.05)  # بين 0.95 و 1.05
                growth_factor = (1 + avg_growth_rate) * random_factor
                
                total_cost = last_month_cost * growth_factor ** i
                direct_cost = last_month_direct * growth_factor ** i
                indirect_cost = last_month_indirect * growth_factor ** i
                
                forecast = {
                    "month": month_number,
                    "total_cost": total_cost,
                    "direct_cost": direct_cost,
                    "indirect_cost": indirect_cost,
                    "variance": (growth_factor - 1) * 100,
                    "cumulative_cost": last_month_cumulative + sum(monthly_forecast[j]["total_cost"] for j in range(i-1)) + total_cost
                }
                
                monthly_forecast.append(forecast)
        
        return monthly_forecast
    
    def _forecast_cost_distribution(self, costs: Dict[str, Any], forecast_months: int) -> Dict[str, Any]:
        """
        التنبؤ بتوزيع التكاليف
        
        المعاملات:
        ----------
        costs : Dict[str, Any]
            بيانات التكاليف
        forecast_months : int
            عدد الأشهر المراد التنبؤ بها
            
        المخرجات:
        --------
        Dict[str, Any]
            التنبؤ بتوزيع التكاليف
        """
        # استخراج بيانات توزيع التكاليف
        direct_costs = costs.get("direct", {})
        indirect_costs = costs.get("indirect", {})
        
        if not direct_costs and not indirect_costs:
            # إنشاء توزيع افتراضي للتكاليف
            return {
                "direct": {
                    "مواد": 40,
                    "عمالة": 30,
                    "معدات": 20,
                    "مقاولين": 10
                },
                "indirect": {
                    "إدارة": 40,
                    "منشآت": 25,
                    "تأمين": 20,
                    "أخرى": 15
                },
                "overall": {
                    "مواد": 30,
                    "عمالة": 25,
                    "معدات": 15,
                    "مقاولين": 5,
                    "إدارة": 10,
                    "منشآت": 5,
                    "تأمين": 5,
                    "أخرى": 5
                }
            }
        
        # حساب إجمالي التكاليف
        total_direct = sum(direct_costs.values())
        total_indirect = sum(indirect_costs.values())
        total_cost = total_direct + total_indirect
        
        # حساب توزيع التكاليف المباشرة
        direct_distribution = {}
        for category, amount in direct_costs.items():
            direct_distribution[category] = (amount / total_direct * 100) if total_direct > 0 else 0
        
        # حساب توزيع التكاليف غير المباشرة
        indirect_distribution = {}
        for category, amount in indirect_costs.items():
            indirect_distribution[category] = (amount / total_indirect * 100) if total_indirect > 0 else 0
        
        # حساب التوزيع الإجمالي
        overall_distribution = {}
        for category, amount in direct_costs.items():
            overall_distribution[category] = (amount / total_cost * 100) if total_cost > 0 else 0
        
        for category, amount in indirect_costs.items():
            overall_distribution[category] = (amount / total_cost * 100) if total_cost > 0 else 0
        
        return {
            "direct": direct_distribution,
            "indirect": indirect_distribution,
            "overall": overall_distribution
        }
    
    def _forecast_deviations(self, costs: Dict[str, Any], forecast_months: int) -> List[Dict[str, Any]]:
        """
        التنبؤ بالانحرافات المحتملة
        
        المعاملات:
        ----------
        costs : Dict[str, Any]
            بيانات التكاليف
        forecast_months : int
            عدد الأشهر المراد التنبؤ بها
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            التنبؤ بالانحرافات المحتملة
        """
        deviation_forecast = []
        
        # استخراج التكاليف الفعلية والمخططة
        actual_costs = costs.get("actual", {})
        planned_costs = costs.get("planned", {})
        
        # إذا لم تكن هناك بيانات كافية، قم بإنشاء توقعات افتراضية
        if not actual_costs or not planned_costs:
            # القوائم الافتراضية للفئات
            categories = ["مواد", "عمالة", "معدات", "مقاولين", "إدارة", "منشآت", "تأمين"]
            
            for category in categories:
                # إنشاء انحراف افتراضي
                random_deviation = np.random.normal(0, 5)  # انحراف عشوائي بمتوسط 0 وانحراف معياري 5
                
                deviation_forecast.append({
                    "category": category,
                    "expected_deviation_percentage": random_deviation,
                    "confidence_level": "متوسط",
                    "impact_level": "منخفض" if abs(random_deviation) < 5 else "متوسط" if abs(random_deviation) < 10 else "مرتفع",
                    "recommendation": self._generate_deviation_recommendation(category, random_deviation)
                })
        else:
            # تحليل الانحرافات السابقة واستخدامها للتنبؤ
            for category in set(list(actual_costs.keys()) + list(planned_costs.keys())):
                actual = actual_costs.get(category, 0)
                planned = planned_costs.get(category, 0)
                
                if planned > 0:
                    historical_deviation = ((actual - planned) / planned) * 100
                    
                    # استخدام الانحراف التاريخي للتنبؤ بالانحراف المستقبلي
                    # يمكن إضافة عوامل أخرى هنا للتحسين
                    expected_deviation = historical_deviation * (1 + np.random.normal(0, 0.2))
                    
                    confidence_level = "مرتفع" if abs(historical_deviation) < 5 else "متوسط" if abs(historical_deviation) < 15 else "منخفض"
                    impact_level = "منخفض" if abs(expected_deviation) < 5 else "متوسط" if abs(expected_deviation) < 10 else "مرتفع"
                    
                    deviation_forecast.append({
                        "category": category,
                        "historical_deviation_percentage": historical_deviation,
                        "expected_deviation_percentage": expected_deviation,
                        "confidence_level": confidence_level,
                        "impact_level": impact_level,
                        "recommendation": self._generate_deviation_recommendation(category, expected_deviation)
                    })
        
        # ترتيب الانحرافات حسب القيمة المطلقة للانحراف المتوقع
        return sorted(deviation_forecast, key=lambda x: abs(x["expected_deviation_percentage"]), reverse=True)
    
    def _analyze_procurement_costs(self, procurement_data: Dict[str, Any], costs: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل تكاليف المشتريات
        
        المعاملات:
        ----------
        procurement_data : Dict[str, Any]
            بيانات المشتريات
        costs : Dict[str, Any]
            بيانات التكاليف
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل تكاليف المشتريات
        """
        # استخراج بيانات المشتريات
        items = procurement_data.get("items", [])
        
        if not items:
            return {
                "total_procurement_cost": 0,
                "local_procurement_cost": 0,
                "import_procurement_cost": 0,
                "local_percentage": 0,
                "categories": {},
                "cost_efficiency": 0
            }
        
        # حساب إجمالي تكاليف المشتريات
        total_cost = sum(item.get("cost", 0) for item in items)
        local_cost = sum(item.get("cost", 0) for item in items if item.get("source_type") == "local")
        import_cost = sum(item.get("cost", 0) for item in items if item.get("source_type") == "import")
        
        # حساب توزيع التكاليف حسب الفئة
        categories = {}
        for item in items:
            category = item.get("category", "أخرى")
            cost = item.get("cost", 0)
            
            if category in categories:
                categories[category] += cost
            else:
                categories[category] = cost
        
        # حساب كفاءة التكلفة
        reference_cost = self.reference_data.get("avg_procurement_cost", total_cost * 1.1)
        cost_efficiency = ((reference_cost - total_cost) / reference_cost) * 100 if reference_cost > 0 else 0
        
        return {
            "total_procurement_cost": total_cost,
            "local_procurement_cost": local_cost,
            "import_procurement_cost": import_cost,
            "local_percentage": (local_cost / total_cost * 100) if total_cost > 0 else 0,
            "categories": categories,
            "cost_efficiency": cost_efficiency
        }
    
    def _analyze_suppliers(self, procurement_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل الموردين
        
        المعاملات:
        ----------
        procurement_data : Dict[str, Any]
            بيانات المشتريات
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل الموردين
        """
        # استخراج بيانات الموردين
        suppliers = procurement_data.get("suppliers", [])
        items = procurement_data.get("items", [])
        
        if not suppliers or not items:
            return {
                "total_suppliers": 0,
                "local_suppliers": 0,
                "supplier_diversity": 0,
                "supplier_concentration": {},
                "supplier_performance": []
            }
        
        # حساب إحصائيات الموردين
        total_suppliers = len(suppliers)
        local_suppliers = len([s for s in suppliers if s.get("location", "").startswith("SA")])
        
        # حساب تنوع الموردين
        categories = set(s.get("category", "") for s in suppliers)
        supplier_diversity = len(categories) / max(1, total_suppliers) * 100
        
        # حساب تركيز الموردين
        supplier_items = {}
        for item in items:
            supplier_id = item.get("supplier_id", "")
            cost = item.get("cost", 0)
            
            if supplier_id in supplier_items:
                supplier_items[supplier_id] += cost
            else:
                supplier_items[supplier_id] = cost
        
        total_cost = sum(supplier_items.values())
        supplier_concentration = {}
        
        for supplier_id, cost in supplier_items.items():
            supplier_name = next((s.get("name", supplier_id) for s in suppliers if s.get("id") == supplier_id), supplier_id)
            supplier_concentration[supplier_name] = (cost / total_cost * 100) if total_cost > 0 else 0
        
        # تقييم أداء الموردين
        supplier_performance = []
        for supplier in suppliers:
            performance = {
                "id": supplier.get("id", ""),
                "name": supplier.get("name", ""),
                "reliability": supplier.get("reliability", 3),
                "delivery_time": supplier.get("avg_delivery_time", 30),
                "quality": supplier.get("quality_rating", 3),
                "price_competitiveness": supplier.get("price_rating", 3),
                "overall_rating": (supplier.get("reliability", 3) + supplier.get("quality_rating", 3) + supplier.get("price_rating", 3)) / 3
            }
            supplier_performance.append(performance)
        
        # ترتيب الموردين حسب التقييم العام
        supplier_performance.sort(key=lambda x: x["overall_rating"], reverse=True)
        
        return {
            "total_suppliers": total_suppliers,
            "local_suppliers": local_suppliers,
            "local_percentage": (local_suppliers / total_suppliers * 100) if total_suppliers > 0 else 0,
            "supplier_diversity": supplier_diversity,
            "supplier_concentration": supplier_concentration,
            "supplier_performance": supplier_performance
        }
    
    def _analyze_local_content(self, procurement_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل المحتوى المحلي
        
        المعاملات:
        ----------
        procurement_data : Dict[str, Any]
            بيانات المشتريات
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المحتوى المحلي
        """
        # استخراج بيانات المشتريات
        items = procurement_data.get("items", [])
        
        if not items:
            return {
                "local_content_percentage": 0,
                "local_content_by_category": {},
                "local_content_trend": [],
                "local_content_gap": 0,
                "improvement_potential": 0
            }
        
        # حساب نسبة المحتوى المحلي
        total_cost = sum(item.get("cost", 0) for item in items)
        local_content = sum(item.get("cost", 0) * item.get("local_content_contribution", 0) / 100 for item in items)
        
        local_content_percentage = (local"""
محلل تكاليف ومخاطر المشاريع
يقوم بتحليل التكاليف وتقييم المخاطر المالية للمشاريع
"""

import logging
import json
import os
from typing import Dict, List, Any, Tuple, Optional, Union
import numpy as np
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CostRiskAnalyzer:
    """
    محلل تكاليف ومخاطر المشاريع
    """
    
    def __init__(self, config=None):
        """
        تهيئة محلل التكاليف والمخاطر
        
        المعاملات:
        ----------
        config : Dict, optional
            إعدادات المحلل
        """
        self.config = config or {}
        
        # تحميل بيانات المخاطر والتكاليف المرجعية
        self.reference_data = self._load_reference_data()
        
        logger.info("تم تهيئة محلل تكاليف ومخاطر المشاريع")
    
    def analyze_costs(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل تكاليف المشروع
        
        المعاملات:
        ----------
        project_data : Dict[str, Any]
            بيانات المشروع
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل التكاليف
        """
        try:
            logger.info("بدء تحليل تكاليف المشروع")
            
            # استخراج بيانات التكاليف
            costs = project_data.get("costs", {})
            
            # تحليل هيكل التكاليف
            cost_structure = self._analyze_cost_structure(costs)
            
            # تحليل المؤشرات المالية
            financial_indicators = self._analyze_financial_indicators(costs, project_data)
            
            # تحليل الانحرافات
            deviations = self._analyze_cost_deviations(costs)
            
            # تحديد نقاط القوة والضعف
            strengths_weaknesses = self._identify_cost_strengths_weaknesses(cost_structure, financial_indicators)
            
            # إعداد التوصيات
            recommendations = self._generate_cost_recommendations(strengths_weaknesses, deviations)
            
            # إعداد النتائج
            results = {
                "cost_structure": cost_structure,
                "financial_indicators": financial_indicators,
                "deviations": deviations,
                "strengths_weaknesses": strengths_weaknesses,
                "recommendations": recommendations
            }
            
            logger.info("اكتمل تحليل تكاليف المشروع")
            return results
            
        except Exception as e:
            logger.error(f"فشل في تحليل تكاليف المشروع: {str(e)}")
            return {
                "error": str(e),
                "cost_structure": {},
                "financial_indicators": {},
                "deviations": [],
                "strengths_weaknesses": {"strengths": [], "weaknesses": []},
                "recommendations": []
            }
    
    def analyze_risks(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل مخاطر المشروع
        
        المعاملات:
        ----------
        project_data : Dict[str, Any]
            بيانات المشروع
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المخاطر
        """
        try:
            logger.info("بدء تحليل مخاطر المشروع")
            
            # استخراج بيانات المخاطر
            risks = project_data.get("risks", [])
            costs = project_data.get("costs", {})
            
            # تحليل المخاطر المالية
            financial_risks = self._analyze_financial_risks(risks, costs)
            
            # تحليل مخاطر تجاوز التكاليف
            cost_overrun_risks = self._analyze_cost_overrun_risks(costs)
            
            # تحليل مخاطر التدفق النقدي
            cashflow_risks = self._analyze_cashflow_risks(costs)
            
            # تحليل تأثير المخاطر على الأرباح
            profit_impact = self._analyze_profit_impact(financial_risks, costs)
            
            # إعداد خطة إدارة المخاطر المالية
            risk_management_plan = self._generate_risk_management_plan(
                financial_risks, cost_overrun_risks, cashflow_risks
            )
            
            # إعداد النتائج
            results = {
                "financial_risks": financial_risks,
                "cost_overrun_risks": cost_overrun_risks,
                "cashflow_risks": cashflow_risks,
                "profit_impact": profit_impact,
                "risk_management_plan": risk_management_plan
            }
            
            logger.info("اكتمل تحليل مخاطر المشروع")
            return results
            
        except Exception as e:
            logger.error(f"فشل في تحليل مخاطر المشروع: {str(e)}")
            return {
                "error": str(e),
                "financial_risks": [],
                "cost_overrun_risks": [],
                "cashflow_risks": [],
                "profit_impact": {},
                "risk_management_plan": []
            }
    
    def forecast_costs(self, project_data: Dict[str, Any], forecast_months: int = 12) -> Dict[str, Any]:
        """
        التنبؤ بتكاليف المشروع
        
        المعاملات:
        ----------
        project_data : Dict[str, Any]
            بيانات المشروع
        forecast_months : int, optional
            عدد الأشهر المراد التنبؤ بها (افتراضي: 12)
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج التنبؤ بالتكاليف
        """
        try:
            logger.info(f"بدء التنبؤ بتكاليف المشروع لمدة {forecast_months} أشهر")
            
            # استخراج بيانات التكاليف
            costs = project_data.get("costs", {})
            
            # التنبؤ بالتكاليف الشهرية
            monthly_forecast = self._forecast_monthly_costs(costs, forecast_months)
            
            # التنبؤ بتوزيع التكاليف
            cost_distribution_forecast = self._forecast_cost_distribution(costs, forecast_months)
            
            # التنبؤ بالانحرافات المحتملة
            deviation_forecast = self._forecast_deviations(costs, forecast_months)
            
            # إعداد النتائج
            results = {
                "monthly_forecast": monthly_forecast,
                "cost_distribution_forecast": cost_distribution_forecast,
                "deviation_forecast": deviation_forecast,
                "forecast_period": {
                    "months": forecast_months,
                    "start_date": datetime.now().strftime("%Y-%m-%d"),
                    "end_date": (datetime.now() + timedelta(days=30 * forecast_months)).strftime("%Y-%m-%d")
                }
            }
            
            logger.info("اكتمل التنبؤ بتكاليف المشروع")
            return results
            
        except Exception as e:
            logger.error(f"فشل في التنبؤ بتكاليف المشروع: {str(e)}")
            return {
                "error": str(e),
                "monthly_forecast": [],
                "cost_distribution_forecast": {},
                "deviation_forecast": []
            }
    
    def generate_procurement_report(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        إنشاء تقرير المشتريات
        
        المعاملات:
        ----------
        project_data : Dict[str, Any]
            بيانات المشروع
            
        المخرجات:
        --------
        Dict[str, Any]
            تقرير المشتريات
        """
        try:
            logger.info("بدء إنشاء تقرير المشتريات")
            
            # استخراج بيانات المشتريات
            procurement_data = project_data.get("procurement", {})
            costs = project_data.get("costs", {})
            
            # تحليل تكاليف المشتريات
            procurement_costs = self._analyze_procurement_costs(procurement_data, costs)
            
            # تحليل الموردين
            suppliers_analysis = self._analyze_suppliers(procurement_data)
            
            # تحليل المحتوى المحلي
            local_content_analysis = self._analyze_local_content(procurement_data)
            
            # تحديد فرص التحسين
            improvement_opportunities = self._identify_procurement_improvements(
                procurement_costs, suppliers_analysis, local_content_analysis
            )
            
            # إعداد النتائج
            results = {
                "procurement_costs": procurement_costs,
                "suppliers_analysis": suppliers_analysis,
                "local_content_analysis": local_content_analysis,
                "improvement_opportunities": improvement_opportunities,
                "summary": self._generate_procurement_summary(
                    procurement_costs, suppliers_analysis, local_content_analysis
                )
            }
            
            logger.info("اكتمل إنشاء تقرير المشتريات")
            return results
            
        except Exception as e:
            logger.error(f"فشل في إنشاء تقرير المشتريات: {str(e)}")
            return {
                "error": str(e),
                "procurement_costs": {},
                "suppliers_analysis": {},
                "local_content_analysis": {},
                "improvement_opportunities": [],
                "summary": ""
            }
    
    def _analyze_cost_structure(self, costs: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل هيكل التكاليف
        
        المعاملات:
        ----------
        costs : Dict[str, Any]
            بيانات التكاليف
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل هيكل التكاليف
        """
        # استخراج تفاصيل التكاليف
        direct_costs = costs.get("direct", {})
        indirect_costs = costs.get("indirect", {})
        
        # حساب إجمالي التكاليف
        total_direct = sum(direct_costs.values())
        total_indirect = sum(indirect_costs.values())
        total_cost = total_direct + total_indirect
        
        if total_cost == 0:
            return {
                "total_cost": 0,
                "direct_percentage": 0,
                "indirect_percentage": 0,
                "direct_breakdown": {},
                "indirect_breakdown": {},
                "cost_per_category": {}
            }
        
        # حساب النسب المئوية
        direct_percentage = (total_direct / total_cost) * 100
        indirect_percentage = (total_indirect / total_cost) * 100
        
        # تحليل تفاصيل التكاليف المباشرة
        direct_breakdown = {}
        for category, amount in direct_costs.items():
            direct_breakdown[category] = {
                "amount": amount,
                "percentage_of_direct": (amount / total_direct) * 100 if total_direct > 0 else 0,
                "percentage_of_total": (amount / total_cost) * 100
            }
        
        # تحليل تفاصيل التكاليف غير المباشرة
        indirect_breakdown = {}
        for category, amount in indirect_costs.items():
            indirect_breakdown[category] = {
                "amount": amount,
                "percentage_of_indirect": (amount / total_indirect) * 100 if total_indirect > 0 else 0,
                "percentage_of_total": (amount / total_cost) * 100
            }
        
        # تجميع التكاليف حسب الفئة
        cost_per_category = {}
        for category, amount in direct_costs.items():
            cost_per_category[f"مباشرة - {category}"] = amount
        
        for category, amount in indirect_costs.items():
            cost_per_category[f"غير مباشرة - {category}"] = amount
        
        return {
            "total_cost": total_cost,
            "direct_percentage": direct_percentage,
            "indirect_percentage": indirect_percentage,
            "direct_breakdown": direct_breakdown,
            "indirect_breakdown": indirect_breakdown,
            "cost_per_category": cost_per_category
        }
    
    def _analyze_financial_indicators(self, costs: Dict[str, Any], project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        تحليل المؤشرات المالية
        
        المعاملات:
        ----------
        costs : Dict[str, Any]
            بيانات التكاليف
        project_data : Dict[str, Any]
            بيانات المشروع
            
        المخرجات:
        --------
        Dict[str, Any]
            نتائج تحليل المؤشرات المالية
        """
        # استخراج البيانات المالية
        contract_value = project_data.get("contract_value", 0)
        direct_costs = costs.get("direct", {})
        indirect_costs = costs.get("indirect", {})
        
        # حساب إجمالي التكاليف
        total_direct = sum(direct_costs.values())
        total_indirect = sum(indirect_costs.values())
        total_cost = total_direct + total_indirect
        
        if total_cost == 0 or contract_value == 0:
            return {
                "profit_margin": 0,
                "cost_revenue_ratio": 0,
                "breakeven_point": 0,
                "roi": 0,
                "cost_efficiency": 0
            }
        
        # حساب هامش الربح
        profit = contract_value - total_cost
        profit_margin = (profit / contract_value) * 100
        
        # حساب نسبة التكلفة إلى الإيرادات
        cost_revenue_ratio = (total_cost / contract_value) * 100
        
        # حساب نقطة التعادل
        breakeven_point = total_indirect / (1 - (total_direct / contract_value))
        
        # حساب العائد على الاستثمار
        roi = (profit / total_cost) * 100
        
        # حساب كفاءة التكلفة
        reference_cost_ratio = self.reference_data.get("avg_cost_revenue_ratio", 85)
        cost_efficiency = ((reference_cost_ratio - cost_revenue_ratio) / reference_cost_ratio) * 100
        
        return {
            "profit_margin": profit_margin,
            "cost_revenue_ratio": cost_revenue_ratio,
            "breakeven_point": breakeven_point,
            "roi": roi,
            "cost_efficiency": cost_efficiency
        }
    
    def _analyze_cost_deviations(self, costs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        تحليل انحرافات التكاليف
        
        المعاملات:
        ----------
        costs : Dict[str, Any]
            بيانات التكاليف
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة انحرافات التكاليف
        """
        deviations = []
        
        # استخراج التكاليف الفعلية والمخططة
        actual_costs = costs.get("actual", {})
        planned_costs = costs.get("planned", {})
        
        if not actual_costs or not planned_costs:
            return deviations
        
        # تحليل الانحرافات لكل فئة
        for category in set(list(actual_costs.keys()) + list(planned_costs.keys())):
            actual = actual_costs.get(category, 0)
            planned = planned_costs.get(category, 0)
            
            if planned > 0:
                deviation_amount = actual - planned
                deviation_percentage = (deviation_amount / planned) * 100
                
                deviations.append({
                    "category": category,
                    "planned": planned,
                    "actual": actual,
                    "deviation_amount": deviation_amount,
                    "deviation_percentage": deviation_percentage,
                    "status": "تجاوز" if deviation_amount > 0 else "وفر" if deviation_amount < 0 else "مطابق"
                })
        
        # ترتيب الانحرافات حسب القيمة المطلقة للانحراف
        return sorted(deviations, key=lambda x: abs(x["deviation_amount"]), reverse=True)
    
    def _identify_cost_strengths_weaknesses(self, cost_structure: Dict[str, Any], 
                                         financial_indicators: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        تحديد نقاط القوة والضعف في التكاليف
        
        المعاملات:
        ----------
        cost_structure : Dict[str, Any]
            هيكل التكاليف
        financial_indicators : Dict[str, Any]
            المؤشرات المالية
            
        المخرجات:
        --------
        Dict[str, List[str]]
            نقاط القوة والضعف
        """
        strengths = []
        weaknesses = []
        
        # تحليل هيكل التكاليف
        if cost_structure["direct_percentage"] < self.reference_data.get("avg_direct_percentage", 75):
            strengths.append("نسبة التكاليف المباشرة أقل من المتوسط، مما يشير إلى كفاءة في إدارة الموارد المباشرة.")
        else:
            weaknesses.append("ارتفاع نسبة التكاليف المباشرة عن المتوسط، مما قد يشير إلى الحاجة لتحسين إدارة الموارد المباشرة.")
        
        # تحليل المؤشرات المالية
        if financial_indicators["profit_margin"] > self.reference_data.get("avg_profit_margin", 15):
            strengths.append("هامش ربح أعلى من المتوسط، مما يدل على كفاءة التسعير وإدارة التكاليف.")
        else:
            weaknesses.append("انخفاض هامش الربح عن المتوسط، مما يستدعي مراجعة استراتيجية التسعير وضبط التكاليف.")
        
        if financial_indicators["cost_revenue_ratio"] < self.reference_data.get("avg_cost_revenue_ratio", 85):
            strengths.append("نسبة التكلفة إلى الإيرادات أقل من المتوسط، مما يشير إلى كفاءة في إدارة التكاليف.")
        else:
            weaknesses.append("ارتفاع نسبة التكلفة إلى الإيرادات عن المتوسط، مما يستدعي ضبط التكاليف.")
        
        if financial_indicators["roi"] > self.reference_data.get("avg_roi", 20):
            strengths.append("العائد على الاستثمار أعلى من المتوسط، مما يدل على كفاءة استغلال الموارد المالية.")
        else:
            weaknesses.append("انخفاض العائد على الاستثمار عن المتوسط، مما يستدعي مراجعة توزيع الموارد المالية.")
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses
        }
    
    def _generate_cost_recommendations(self, strengths_weaknesses: Dict[str, List[str]], 
                                     deviations: List[Dict[str, Any]]) -> List[str]:
        """
        إعداد توصيات لتحسين التكاليف
        
        المعاملات:
        ----------
        strengths_weaknesses : Dict[str, List[str]]
            نقاط القوة والضعف
        deviations : List[Dict[str, Any]]
            انحرافات التكاليف
            
        المخرجات:
        --------
        List[str]
            قائمة التوصيات
        """
        recommendations = []
        
        # توصيات بناءً على نقاط الضعف
        for weakness in strengths_weaknesses.get("weaknesses", []):
            if "هامش الربح" in weakness:
                recommendations.append("مراجعة استراتيجية التسعير وتحديد فرص زيادة الإيرادات.")
            
            if "التكاليف المباشرة" in weakness:
                recommendations.append("تحسين إدارة الموارد المباشرة وتقليل الهدر في المواد والعمالة.")
            
            if "نسبة التكلفة إلى الإيرادات" in weakness:
                recommendations.append("تطبيق استراتيجيات ضبط التكاليف وتحسين كفاءة العمليات.")
            
            if "العائد على الاستثمار" in weakness:
                recommendations.append("إعادة توزيع الموارد المالية وتوجيهها نحو الأنشطة ذات العائد الأعلى.")
        
        # توصيات بناءً على انحرافات التكاليف
        high_deviations = [dev for dev in deviations if dev["status"] == "تجاوز" and dev["deviation_percentage"] > 10]
        
        if high_deviations:
            recommendations.append("معالجة فورية للتجاوزات الكبيرة في التكاليف، خاصة في الفئات التالية:")
            for i, deviation in enumerate(high_deviations[:3]):
                recommendations.append(f"  - {deviation['category']}: تجاوز بنسبة {deviation['deviation_percentage']:.1f}%")
        
        # توصيات عامة
        recommendations.extend([
            "تنفيذ نظام متكامل لمراقبة التكاليف ومتابعتها بشكل دوري.",
            "تحليل سلسلة القيمة لتحديد الأنشطة غير الضرورية وتقليل تكاليفها.",
            "تطبيق مبدأ التحسين المستمر في إدارة التكاليف ومراجعتها دوريًا."
        ])
        
        return recommendations
    
    def _analyze_financial_risks(self, risks: List[Dict[str, Any]], costs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        تحليل المخاطر المالية
        
        المعاملات:
        ----------
        risks : List[Dict[str, Any]]
            قائمة المخاطر
        costs : Dict[str, Any]
            بيانات التكاليف
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة المخاطر المالية
        """
        financial_risks = []
        
        # فلترة المخاطر المالية
        for risk in risks:
            if risk.get("type") == "financial" or risk.get("category") == "financial":
                financial_risks.append(risk)
        
        # إذا لم تكن هناك مخاطر مالية محددة، قم بإنشاء مخاطر افتراضية
        if not financial_risks:
            # حساب إجمالي التكاليف
            direct_costs = costs.get("direct", {})
            indirect_costs = costs.get("indirect", {})
            total_cost = sum(direct_costs.values()) + sum(indirect_costs.values())
            
            # إنشاء مخاطر افتراضية
            financial_risks = [
                {
                    "name": "ارتفاع أسعار المواد",
                    "type": "financial",
                    "probability": 0.4,
                    "impact": 0.3,
                    "risk_score": 0.12,
                    "financial_impact": total_cost * 0.05,
                    "description": "ارتفاع غير متوقع في أسعار المواد الأساسية",
                    "mitigation": "تأمين عقود توريد بأسعار ثابتة لفترات طويلة"
                },
                {
                    "name": "تأخر الدفعات",
                    "type": "financial",
                    "probability": 0.3,
                    "impact": 0.4,
                    "risk_score": 0.12,
                    "financial_impact": total_cost * 0.03,
                    "description": "تأخر في استلام الدفعات من العميل",
                    "mitigation": "وضع شروط دفع واضحة في العقد وتوفير تمويل احتياطي"
                },
                {
                    "name": "تقلبات أسعار العملات",
                    "type": "financial",
                    "probability": 0.25,
                    "impact": 0.25,
                    "risk_score": 0.0625,
                    "financial_impact": total_cost * 0.02,
                    "description": "تقلبات في أسعار صرف العملات للمشتريات الدولية",
                    "mitigation": "استخدام آليات التحوط وتفضيل المشتريات المحلية"
                }
            ]
        
        # إثراء بيانات المخاطر المالية
        for risk in financial_risks:
            # حساب درجة المخاطرة إذا لم تكن موجودة
            if "risk_score" not in risk:
                probability = risk.get("probability", 0.5)
                impact = risk.get("impact", 0.5)
                risk["risk_score"] = probability * impact
            
            # تقدير التأثير المالي إذا لم يكن موجودًا
            if "financial_impact" not in risk:
                # حساب إجمالي التكاليف
                direct_costs = costs.get("direct", {})
                indirect_costs = costs.get("indirect", {})
                total_cost = sum(direct_costs.values()) + sum(indirect_costs.values())
                
                risk["financial_impact"] = total_cost * risk["impact"] * 0.1
            
            # إضافة استراتيجية تخفيف إذا لم تكن موجودة
            if "mitigation" not in risk:
                risk["mitigation"] = self._generate_default_mitigation(risk)
        
        # ترتيب المخاطر حسب درجة المخاطرة
        return sorted(financial_risks, key=lambda x: x.get("risk_score", 0), reverse=True)
    
    def _analyze_cost_overrun_risks(self, costs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        تحليل مخاطر تجاوز التكاليف
        
        المعاملات:
        ----------
        costs : Dict[str, Any]
            بيانات التكاليف
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة مخاطر تجاوز التكاليف
        """
        # استخراج التكاليف الفعلية والمخططة
        actual_costs = costs.get("actual", {})
        planned_costs = costs.get("planned", {})
        
        overrun_risks = []
        
        if not actual_costs or not planned_costs:
            return overrun_risks
        
        # تحليل الانحرافات لكل فئة وتحديد المخاطر
        for category in set(list(actual_costs.keys()) + list(planned_costs.keys())):
            actual = actual_costs.get(category, 0)
            planned = planned_costs.get(category, 0)
            
            if planned > 0:
                deviation_percentage = ((actual - planned) / planned) * 100
                
                # إذا كان هناك تجاوز، أضف المخاطرة
                if deviation_percentage > 5:
                    risk_level = "مرتفع" if deviation_percentage > 20 else "متوسط" if deviation_percentage > 10 else "منخفض"
                    
                    overrun_risks.append({
                        "category": category,
                        "planned": planned,
                        "actual": actual,
                        "deviation_percentage": deviation_percentage,