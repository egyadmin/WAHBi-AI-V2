import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import os

def show_tender_analysis():
    """
    عرض صفحة تحليل المناقصات
    """
    st.subheader("تحليل المناقصات")
    
    # تقسيم الشاشة إلى جزئين
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # قسم رفع الملفات
        st.markdown("### رفع ملفات المناقصة")
        
        uploaded_files = st.file_uploader(
            "قم برفع ملفات المناقصة (PDF, DOCX, XLSX)",
            type=["pdf", "docx", "xlsx", "csv", "json"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            st.success(f"تم رفع {len(uploaded_files)} ملفات بنجاح")
            
            # عرض قائمة الملفات
            st.markdown("### الملفات المرفوعة")
            for file in uploaded_files:
                st.markdown(f"- {file.name} ({file.size / 1024:.1f} KB)")
        
        # خيارات التحليل
        st.markdown("### خيارات التحليل")
        
        analysis_options = st.multiselect(
            "اختر أنواع التحليل",
            [
                "استخراج المتطلبات الرئيسية",
                "تحليل التكاليف التقديرية",
                "تحليل المخاطر",
                "تحليل المحتوى المحلي",
                "تحليل سلاسل الإمداد",
                "التحليل الزمني",
                "توقع احتمالية النجاح"
            ],
            default=["استخراج المتطلبات الرئيسية", "تحليل التكاليف التقديرية"]
        )
        
        # زر بدء التحليل
        if st.button("بدء التحليل"):
            if not uploaded_files:
                st.error("يرجى رفع ملفات المناقصة أولاً")
            elif not analysis_options:
                st.error("يرجى اختيار نوع التحليل المطلوب")
            else:
                # هنا سيتم استدعاء عمليات التحليل الفعلية
                # نستخدم هنا بيانات توضيحية للعرض فقط
                with st.spinner("جاري تحليل المناقصة... قد تستغرق العملية بضع دقائق..."):
                    # محاكاة وقت المعالجة
                    import time
                    time.sleep(2)
                    
                    # تخزين نتائج التحليل في حالة الجلسة
                    st.session_state.analysis_results = {
                        "tender_id": "T-2025-" + str(np.random.randint(1000, 9999)),
                        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "requirements": [
                            "توريد وتركيب معدات البنية التحتية",
                            "صيانة الشبكات لمدة سنتين",
                            "تدريب الموظفين على الأنظمة الجديدة",
                            "توفير قطع الغيار اللازمة",
                            "الالتزام بمعايير الجودة ISO 9001"
                        ],
                        "cost_estimate": {
                            "total": np.random.uniform(80, 150, 1)[0].round(2),
                            "breakdown": {
                                "مواد": np.random.uniform(30, 60, 1)[0].round(2),
                                "عمالة": np.random.uniform(20, 40, 1)[0].round(2),
                                "معدات": np.random.uniform(10, 30, 1)[0].round(2),
                                "إدارة": np.random.uniform(5, 15, 1)[0].round(2),
                                "أخرى": np.random.uniform(5, 10, 1)[0].round(2)
                            }
                        },
                        "risks": [
                            {"name": "تأخر التوريدات", "probability": 0.4, "impact": 0.7, "score": 0.28},
                            {"name": "تغيير المواصفات", "probability": 0.3, "impact": 0.6, "score": 0.18},
                            {"name": "نقص العمالة الماهرة", "probability": 0.5, "impact": 0.5, "score": 0.25},
                            {"name": "تقلبات أسعار المواد", "probability": 0.6, "impact": 0.4, "score": 0.24},
                            {"name": "ظروف جوية غير مناسبة", "probability": 0.2, "impact": 0.3, "score": 0.06}
                        ],
                        "local_content": {
                            "estimated_percentage": np.random.uniform(50, 80, 1)[0].round(2),
                            "required_percentage": np.random.uniform(40, 60, 1)[0].round(2),
                            "breakdown": {
                                "عمالة محلية": np.random.uniform(60, 90, 1)[0].round(2),
                                "مواد محلية": np.random.uniform(40, 70, 1)[0].round(2),
                                "خدمات محلية": np.random.uniform(50, 80, 1)[0].round(2),
                                "تدريب وتطوير": np.random.uniform(30, 60, 1)[0].round(2)
                            }
                        },
                        "success_probability": np.random.uniform(60, 90, 1)[0].round(2)
                    }
                    
                    st.success("تم الانتهاء من تحليل المناقصة بنجاح!")
    
    with col2:
        # عرض نتائج التحليل إذا كانت متوفرة
        if "analysis_results" in st.session_state and st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # عرض معلومات المناقصة
            st.markdown("### معلومات المناقصة")
            st.markdown(f"**رقم المناقصة:** {results['tender_id']}")
            st.markdown(f"**تاريخ التحليل:** {results['analyzed_at']}")
            
            # تبويب لعرض مختلف أنواع التحليل
            tabs = st.tabs([
                "المتطلبات", 
                "التكاليف", 
                "المخاطر", 
                "المحتوى المحلي", 
                "احتمالية النجاح"
            ])
            
            # تبويب المتطلبات
            with tabs[0]:
                st.markdown("### المتطلبات الرئيسية للمناقصة")
                for i, req in enumerate(results["requirements"]):
                    st.markdown(f"{i+1}. {req}")
            
            # تبويب التكاليف
            with tabs[1]:
                st.markdown("### تحليل التكاليف التقديرية")
                
                # إجمالي التكلفة
                st.markdown(f"**إجمالي التكلفة التقديرية:** {results['cost_estimate']['total']} مليون ريال")
                
                # رسم بياني لتوزيع التكاليف
                cost_data = {
                    "الفئة": list(results["cost_estimate"]["breakdown"].keys()),
                    "القيمة (مليون ريال)": list(results["cost_estimate"]["breakdown"].values())
                }
                
                cost_df = pd.DataFrame(cost_data)
                
                fig = px.pie(
                    cost_df, 
                    values="القيمة (مليون ريال)", 
                    names="الفئة",
                    title="توزيع التكاليف التقديرية",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # تبويب المخاطر
            with tabs[2]:
                st.markdown("### تحليل المخاطر")
                
                # جدول المخاطر
                risk_data = pd.DataFrame(results["risks"])
                risk_data.columns = ["المخاطرة", "الاحتمالية", "التأثير", "الدرجة"]
                
                st.table(risk_data.style.format({
                    "الاحتمالية": "{:.1%}",
                    "التأثير": "{:.1%}",
                    "الدرجة": "{:.1%}"
                }))
                
                # مصفوفة المخاطر
                st.markdown("### مصفوفة المخاطر")
                
                fig = px.scatter(
                    risk_data, 
                    x="الاحتمالية", 
                    y="التأثير",
                    size="الدرجة",
                    text="المخاطرة",
                    size_max=60,
                    color="الدرجة",
                    color_continuous_scale=px.colors.sequential.Reds,
                    title="مصفوفة المخاطر",
                    range_x=[0, 1],
                    range_y=[0, 1]
                )
                
                fig.update_traces(textposition="top center")
                fig.update_layout(
                    xaxis_title="احتمالية الحدوث",
                    yaxis_title="مستوى التأثير"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # تبويب المحتوى المحلي
            with tabs[3]:
                st.markdown("### تحليل المحتوى المحلي")
                
                # نسب المحتوى المحلي
                est_pct = results["local_content"]["estimated_percentage"]
                req_pct = results["local_content"]["required_percentage"]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # متطلبات المحتوى المحلي
                    st.markdown(f"**نسبة المحتوى المحلي المطلوبة:** {req_pct}%")
                    st.progress(req_pct / 100)
                
                with col2:
                    # النسبة المتوقعة
                    st.markdown(f"**نسبة المحتوى المحلي المتوقعة:** {est_pct}%")
                    st.progress(est_pct / 100)
                    
                    # حالة المحتوى المحلي (هل يلبي المتطلبات)
                    if est_pct >= req_pct:
                        st.success(f"المحتوى المحلي المتوقع يتجاوز المتطلبات بنسبة {est_pct - req_pct:.1f}%")
                    else:
                        st.error(f"المحتوى المحلي المتوقع أقل من المتطلبات بنسبة {req_pct - est_pct:.1f}%")
                
                # رسم بياني لمكونات المحتوى المحلي
                local_data = {
                    "الفئة": list(results["local_content"]["breakdown"].keys()),
                    "النسبة (%)": list(results["local_content"]["breakdown"].values())
                }
                
                local_df = pd.DataFrame(local_data)
                
                fig = px.bar(
                    local_df, 
                    x="الفئة", 
                    y="النسبة (%)",
                    color="النسبة (%)",
                    color_continuous_scale=px.colors.sequential.Viridis,
                    title="مكونات المحتوى المحلي حسب الفئة"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # تبويب احتمالية النجاح
            with tabs[4]:
                st.markdown("### توقع احتمالية النجاح")
                
                # عرض احتمالية النجاح
                success_prob = results["success_probability"]
                
                # اختيار اللون حسب النسبة
                color = "green" if success_prob >= 80 else "orange" if success_prob >= 60 else "red"
                
                st.markdown(f"<h1 style='text-align: center; color: {color};'>{success_prob}%</h1>", unsafe_allow_html=True)
                st.progress(success_prob / 100)
                
                # نصائح لتحسين الاحتمالية
                st.markdown("### توصيات لتحسين فرص النجاح")
                
                recommendations = [
                    "زيادة نسبة المحتوى المحلي بنسبة 5-10%",
                    "تعزيز فريق المشروع بخبرات في مجال التقنية",
                    "البحث عن موردين محليين بديلين للمواد الرئيسية",
                    "وضع خطة واضحة للتعامل مع المخاطر ذات التأثير العالي",
                    "تقديم حلول مبتكرة في المجالات التقنية"
                ]
                
                for rec in recommendations:
                    st.markdown(f"- {rec}")
                
                # زر لحفظ التقرير
                if st.button("حفظ تقرير التحليل"):
                    st.session_state.latest_analysis = results
                    st.success("تم حفظ تقرير التحليل بنجاح!")
        else:
            # توجيهات للمستخدم
            st.info("قم برفع ملفات المناقصة واختر خيارات التحليل المطلوبة، ثم اضغط على زر 'بدء التحليل' لعرض النتائج هنا.")
            
            # عرض مثال توضيحي
            st.markdown("### مثال توضيحي لنتائج التحليل")
            st.image("https://via.placeholder.com/800x500?text=مثال+لنتائج+تحليل+المناقصة", caption="مثال لنتائج تحليل المناقصة")

# اختبار مستقل للصفحة
if __name__ == "__main__":
    st.set_page_config(
        page_title="نظام تحليل المناقصات - تحليل المناقصات",
        page_icon="📊",
        layout="wide",
    )
    show_tender_analysis()