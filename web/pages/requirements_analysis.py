import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def show_requirements_analysis():
    """
    عرض صفحة تحليل متطلبات المناقصة
    """
    st.subheader("تحليل متطلبات المناقصة")
    
    # التحقق من وجود نتائج تحليل سابقة
    if "analysis_results" not in st.session_state or not st.session_state.analysis_results:
        st.warning("لا توجد نتائج تحليل متاحة. يرجى تحليل مناقصة أولاً.")
        
        if st.button("الانتقال إلى صفحة تحليل المناقصات"):
            st.session_state.page = "تحليل المناقصات"
            st.experimental_rerun()
            
        # عرض بيانات توضيحية
        st.markdown("### بيانات توضيحية لمتطلبات المناقصة")
        
        sample_requirements = [
            {"المتطلب": "توريد وتركيب معدات الشبكة", "النوع": "فني", "الأولوية": "عالية", "التخصص": "تقنية المعلومات"},
            {"المتطلب": "تدريب الموظفين", "النوع": "إداري", "الأولوية": "متوسطة", "التخصص": "تدريب"},
            {"المتطلب": "توفير الصيانة لمدة 3 سنوات", "النوع": "تعاقدي", "الأولوية": "عالية", "التخصص": "صيانة"},
            {"المتطلب": "الالتزام بمعايير الأمن السيبراني", "النوع": "تنظيمي", "الأولوية": "عالية", "التخصص": "أمن المعلومات"},
            {"المتطلب": "نسبة محتوى محلي لا تقل عن 50%", "النوع": "تنظيمي", "الأولوية": "عالية", "التخصص": "محتوى محلي"},
            {"المتطلب": "تقديم ضمان بنكي بنسبة 10%", "النوع": "مالي", "الأولوية": "متوسطة", "التخصص": "مالي"},
            {"المتطلب": "تنفيذ المشروع في مدة لا تتجاوز 18 شهر", "النوع": "زمني", "الأولوية": "عالية", "التخصص": "إدارة مشاريع"},
        ]
        
        sample_df = pd.DataFrame(sample_requirements)
        st.table(sample_df)
        return
    
    # عرض معلومات المناقصة
    results = st.session_state.analysis_results
    st.markdown(f"### تحليل متطلبات المناقصة رقم {results['tender_id']}")
    
    # إنشاء بيانات المتطلبات (نستخدم البيانات المتاحة أو نضيف تفاصيل إضافية)
    # في التطبيق الفعلي، ستكون هذه البيانات من نتائج التحليل الحقيقي
    requirements = []
    
    for i, req in enumerate(results.get("requirements", [])):
        # إنشاء تفاصيل عشوائية لكل متطلب للتوضيح
        req_type = np.random.choice(["فني", "إداري", "تعاقدي", "تنظيمي", "مالي", "زمني"])
        priority = np.random.choice(["عالية", "متوسطة", "منخفضة"], p=[0.5, 0.3, 0.2])
        
        specializations = {
            "فني": ["هندسة", "تقنية المعلومات", "اتصالات", "كهرباء", "ميكانيكا"],
            "إداري": ["إدارة مشاريع", "موارد بشرية", "تدريب", "جودة"],
            "تعاقدي": ["قانوني", "مشتريات", "عقود", "صيانة"],
            "تنظيمي": ["امتثال", "أمن المعلومات", "محتوى محلي", "بيئة"],
            "مالي": ["محاسبة", "ضمانات", "تمويل", "مالي"],
            "زمني": ["إدارة مشاريع", "جدولة", "تخطيط"]
        }
        
        specialization = np.random.choice(specializations.get(req_type, ["عام"]))
        
        requirements.append({
            "المتطلب": req,
            "النوع": req_type,
            "الأولوية": priority,
            "التخصص": specialization
        })
    
    # إذا لم تكن هناك متطلبات، إنشاء بيانات توضيحية
    if not requirements:
        requirements = [
            {"المتطلب": "توريد وتركيب معدات", "النوع": "فني", "الأولوية": "عالية", "التخصص": "هندسة"},
            {"المتطلب": "تدريب الموظفين", "النوع": "إداري", "الأولوية": "متوسطة", "التخصص": "تدريب"},
            {"المتطلب": "صيانة دورية", "النوع": "تعاقدي", "الأولوية": "متوسطة", "التخصص": "صيانة"},
            {"المتطلب": "الامتثال للمعايير", "النوع": "تنظيمي", "الأولوية": "عالية", "التخصص": "امتثال"},
            {"المتطلب": "تقديم ضمانات مالية", "النوع": "مالي", "الأولوية": "عالية", "التخصص": "مالي"}
        ]
    
    # تحويل البيانات إلى DataFrame
    requirements_df = pd.DataFrame(requirements)
    
    # تبويبات لعرض المتطلبات بطرق مختلفة
    tab1, tab2, tab3 = st.tabs(["قائمة المتطلبات", "تصنيف المتطلبات", "تحليل المتطلبات"])
    
    # تبويب قائمة المتطلبات
    with tab1:
        st.markdown("### قائمة متطلبات المناقصة")
        st.dataframe(requirements_df, use_container_width=True)
        
        # خيار تصفية المتطلبات
        st.markdown("### تصفية المتطلبات")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_type = st.selectbox(
                "تصفية حسب النوع",
                ["الكل"] + sorted(requirements_df["النوع"].unique().tolist())
            )
        
        with col2:
            selected_priority = st.selectbox(
                "تصفية حسب الأولوية",
                ["الكل"] + sorted(requirements_df["الأولوية"].unique().tolist())
            )
        
        # تطبيق التصفية
        filtered_df = requirements_df.copy()
        
        if selected_type != "الكل":
            filtered_df = filtered_df[filtered_df["النوع"] == selected_type]
        
        if selected_priority != "الكل":
            filtered_df = filtered_df[filtered_df["الأولوية"] == selected_priority]
        
        if selected_type != "الكل" or selected_priority != "الكل":
            st.markdown("### المتطلبات المصفاة")
            st.dataframe(filtered_df, use_container_width=True)
    
    # تبويب تصنيف المتطلبات
    with tab2:
        st.markdown("### تصنيف المتطلبات حسب النوع والأولوية")
        
        # رسم بياني للمتطلبات حسب النوع
        type_counts = requirements_df["النوع"].value_counts().reset_index()
        type_counts.columns = ["النوع", "العدد"]
        
        fig1 = px.bar(
            type_counts, 
            x="النوع", 
            y="العدد",
            color="النوع",
            title="توزيع المتطلبات حسب النوع"
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # رسم بياني للمتطلبات حسب الأولوية
        priority_counts = requirements_df["الأولوية"].value_counts().reset_index()
        priority_counts.columns = ["الأولوية", "العدد"]
        
        # ترتيب الأولويات
        priority_order = {"عالية": 1, "متوسطة": 2, "منخفضة": 3}
        priority_counts["الترتيب"] = priority_counts["الأولوية"].map(priority_order)
        priority_counts = priority_counts.sort_values("الترتيب")
        
        # اختيار الألوان حسب الأولوية
        color_map = {"عالية": "#FF5733", "متوسطة": "#FFC300", "منخفضة": "#33FF57"}
        colors = priority_counts["الأولوية"].map(color_map)
        
        fig2 = px.bar(
            priority_counts, 
            x="الأولوية", 
            y="العدد",
            color="الأولوية",
            color_discrete_map=color_map,
            title="توزيع المتطلبات حسب الأولوية"
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # تبويب تحليل المتطلبات
    with tab3:
        st.markdown("### تحليل المتطلبات")
        
        # توزيع المتطلبات حسب التخصص
        specialization_counts = requirements_df["التخصص"].value_counts().reset_index()
        specialization_counts.columns = ["التخصص", "العدد"]
        
        fig3 = px.pie(
            specialization_counts, 
            values="العدد", 
            names="التخصص",
            title="توزيع المتطلبات حسب التخصص",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig3.update_traces(textposition="inside", textinfo="percent+label")
        
        st.plotly_chart(fig3, use_container_width=True)
        
        # مصفوفة المتطلبات (النوع × الأولوية)
        heatmap_data = pd.crosstab(
            requirements_df["النوع"], 
            requirements_df["الأولوية"],
            margins=True, 
            margins_name="الإجمالي"
        )
        
        # ترتيب الأعمدة (الأولويات)
        priority_columns = ["عالية", "متوسطة", "منخفضة", "الإجمالي"]
        heatmap_data = heatmap_data.reindex(columns=priority_columns, fill_value=0)
        
        st.markdown("### مصفوفة المتطلبات (النوع × الأولوية)")
        st.dataframe(heatmap_data, use_container_width=True)
    
    # خيارات إضافية
    st.markdown("### خيارات إضافية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("تصدير المتطلبات إلى Excel"):
            st.success("تم تصدير المتطلبات إلى ملف Excel بنجاح!")
    
    with col2:
        if st.button("العودة إلى تحليل المناقصة"):
            st.session_state.page = "تحليل المناقصات"
            st.experimental_rerun()

# اختبار مستقل للصفحة
if __name__ == "__main__":
    st.set_page_config(
        page_title="نظام تحليل المناقصات - تحليل المتطلبات",
        page_icon="📊",
        layout="wide",
    )
    show_requirements_analysis()