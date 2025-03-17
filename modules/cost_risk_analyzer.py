"""
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
                        "risk_level": risk_level,
                        "impact": "تأثير على هامش الربح وزيادة التكاليف ال