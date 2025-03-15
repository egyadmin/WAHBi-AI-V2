import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show_local_content():
    """
    عرض صفحة تحليل المحتوى المحلي
    """
    st.subheader("تحليل وتحسين المحتوى المحلي")
    
    # إنشاء القائمة الجانبية للخيارات
    options = st.sidebar.radio(
        "اختر القسم",
        ["تحليل المحتوى المحلي", "حاسبة المحتوى المحلي", "الموردون المحليون", "متطلبات رؤية 2030"]
    )
    
    if options == "تحليل المحتوى المحلي":
        show_local_content_analysis()
    elif options == "حاسبة المحتوى المحلي":
        show_local_content_calculator()
    elif options == "الموردون المحليون":
        show_local_vendors()
    elif options == "متطلبات رؤية 2030":
        show_vision_requirements()

def show_local_content_analysis():
    """
    عرض تحليل المحتوى المحلي
    """
    st.markdown("## تحليل المحتوى المحلي")
    
    # عرض بيانات أداء المحتوى المحلي عبر المشاريع السابقة
    st.markdown("### أداء المحتوى المحلي في المشاريع السابقة")
    
    # إنشاء بيانات توضيحية
    projects_data = {
        "المشروع": [
            "مشروع توسعة شبكة الطرق - الرياض",
            "بناء المدارس - المنطقة الشرقية",
            "تطوير البنية التحتية - جدة",
            "تحديث شبكة المياه - الدمام",
            "بناء المستشفى التخصصي - مكة",
            "إنشاء مركز البيانات - الرياض",
            "توسعة المطار - أبها",
            "تطوير الحدائق العامة - المدينة"
        ],
        "المحتوى المحلي المطلوب (%)": [40, 35, 45, 40, 50, 30, 45, 35],
        "المحتوى المحلي المحقق (%)": [47, 39, 52, 38, 53, 42, 48, 41],
        "القيمة (مليون ريال)": [120, 80, 150, 60, 200, 90, 110, 40]
    }
    
    projects_df = pd.DataFrame(projects_data)
    projects_df["الفرق"] = projects_df["المحتوى المحلي المحقق (%)"] - projects_df["المحتوى المحلي المطلوب (%)"]
    projects_df["حالة الامتثال"] = np.where(projects_df["الفرق"] >= 0, "ملتزم", "غير ملتزم")
    
    # عرض البيانات
    st.dataframe(projects_df, use_container_width=True)
    
    # رسم بياني لمقارنة المحتوى المحلي المطلوب والمحقق
    st.markdown("### مقارنة المحتوى المحلي المطلوب والمحقق")
    
    fig1 = go.Figure()
    
    fig1.add_trace(go.Bar(
        x=projects_df["المشروع"],
        y=projects_df["المحتوى المحلي المطلوب (%)"],
        name="المطلوب",
        marker_color='#1976D2'
    ))
    
    fig1.add_trace(go.Bar(
        x=projects_df["المشروع"],
        y=projects_df["المحتوى المحلي المحقق (%)"],
        name="المحقق",
        marker_color='#43A047'
    ))
    
    fig1.update_layout(
        title="مقارنة نسب المحتوى المحلي المطلوبة والمحققة",
        xaxis_title="المشروع",
        yaxis_title="نسبة المحتوى المحلي (%)",
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # تحليل مكونات المحتوى المحلي
    st.markdown("### مكونات المحتوى المحلي (متوسط المشاريع)")
    
    components_data = {
        "المكون": ["العمالة المحلية", "المواد المحلية", "الخدمات المحلية", "الآلات والمعدات", "التدريب والتأهيل"],
        "النسبة (%)": [65, 45, 52, 38, 42]
    }
    
    components_df = pd.DataFrame(components_data)
    
    fig2 = px.pie(
        components_df, 
        values="النسبة (%)", 
        names="المكون",
        title="توزيع مكونات المحتوى المحلي",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig2.update_traces(textposition="inside", textinfo="percent+label")
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # تحليل اتجاهات المحتوى المحلي
    st.markdown("### اتجاهات المحتوى المحلي")
    
    years = [2020, 2021, 2022, 2023, 2024, 2025]
    trend_data = {
        "السنة": years,
        "متوسط المحتوى المحلي (%)": [42, 46, 51, 57, 63, 68],
        "الهدف (%)": [40, 45, 50, 55, 60, 70]
    }
    
    trend_df = pd.DataFrame(trend_data)
    
    fig3 = go.Figure()
    
    fig3.add_trace(go.Scatter(
        x=trend_df["السنة"],
        y=trend_df["متوسط المحتوى المحلي (%)"],
        mode='lines+markers',
        name="المحقق",
        line=dict(color='#43A047', width=3)
    ))
    
    fig3.add_trace(go.Scatter(
        x=trend_df["السنة"],
        y=trend_df["الهدف (%)"],
        mode='lines+markers',
        name="الهدف",
        line=dict(color='#1976D2', width=3, dash='dash')
    ))
    
    fig3.update_layout(
        title="اتجاهات المحتوى المحلي مقارنة بالأهداف",
        xaxis_title="السنة",
        yaxis_title="نسبة المحتوى المحلي (%)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig3, use_container_width=True)

def show_local_content_calculator():
    """
    عرض حاسبة المحتوى المحلي
    """
    st.markdown("## حاسبة المحتوى المحلي")
    
    st.markdown("""
    هذه الحاسبة تساعدك على تقدير نسبة المحتوى المحلي لمشروعك بناءً على مكونات المشروع المختلفة.
    يرجى إدخال القيم التقديرية لكل مكون.
    """)
    
    # قسم إدخال البيانات
    st.markdown("### بيانات المشروع")
    
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input("اسم المشروع", "مشروع جديد")
        total_budget = st.number_input("إجمالي قيمة المشروع (مليون ريال)", min_value=1.0, max_value=1000.0, value=100.0)
    
    with col2:
        local_content_target = st.number_input("نسبة المحتوى المحلي المستهدفة (%)", min_value=10, max_value=100, value=50)
        project_duration = st.number_input("مدة المشروع (بالأشهر)", min_value=1, max_value=60, value=12)
    
    # مكونات المحتوى المحلي
    st.markdown("### مكونات المشروع")
    
    # العمالة
    st.markdown("#### العمالة")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        labor_local_percentage = st.slider("نسبة العمالة المحلية (%)", 0, 100, 60)
    
    with col2:
        labor_cost_percentage = st.slider("نسبة تكلفة العمالة من إجمالي المشروع (%)", 0, 100, 30)
    
    with col3:
        labor_cost = total_budget * (labor_cost_percentage / 100)
        labor_local_value = labor_cost * (labor_local_percentage / 100)
        
        st.metric(
            label="قيمة العمالة المحلية (مليون ريال)",
            value=f"{labor_local_value:.2f}"
        )
    
    # المواد
    st.markdown("#### المواد")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        materials_local_percentage = st.slider("نسبة المواد المحلية (%)", 0, 100, 40)
    
    with col2:
        materials_cost_percentage = st.slider("نسبة تكلفة المواد من إجمالي المشروع (%)", 0, 100, 40)
    
    with col3:
        materials_cost = total_budget * (materials_cost_percentage / 100)
        materials_local_value = materials_cost * (materials_local_percentage / 100)
        
        st.metric(
            label="قيمة المواد المحلية (مليون ريال)",
            value=f"{materials_local_value:.2f}"
        )
    
    # الخدمات
    st.markdown("#### الخدمات")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        services_local_percentage = st.slider("نسبة الخدمات المحلية (%)", 0, 100, 50)
    
    with col2:
        services_cost_percentage = st.slider("نسبة تكلفة الخدمات من إجمالي المشروع (%)", 0, 100, 20)
    
    with col3:
        services_cost = total_budget * (services_cost_percentage / 100)
        services_local_value = services_cost * (services_local_percentage / 100)
        
        st.metric(
            label="قيمة الخدمات المحلية (مليون ريال)",
            value=f"{services_local_value:.2f}"
        )
    
    # المعدات
    st.markdown("#### المعدات والآلات")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        equipment_local_percentage = st.slider("نسبة المعدات المحلية (%)", 0, 100, 25)
    
    with col2:
        equipment_cost_percentage = st.slider("نسبة تكلفة المعدات من إجمالي المشروع (%)", 0, 100, 10)
    
    with col3:
        equipment_cost = total_budget * (equipment_cost_percentage / 100)
        equipment_local_value = equipment_cost * (equipment_local_percentage / 100)
        
        st.metric(
            label="قيمة المعدات المحلية (مليون ريال)",
            value=f"{equipment_local_value:.2f}"
        )
    
    # حساب نسبة المحتوى المحلي الإجمالية
    total_local_value = labor_local_value + materials_local_value + services_local_value + equipment_local_value
    actual_local_content = (total_local_value / total_budget) * 100
    
    st.markdown("### نتائج حساب المحتوى المحلي")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="إجمالي قيمة المشروع (مليون ريال)",
            value=f"{total_budget:.2f}"
        )
    
    with col2:
        st.metric(
            label="قيمة المحتوى المحلي (مليون ريال)",
            value=f"{total_local_value:.2f}"
        )
    
    with col3:
        st.metric(
            label="نسبة المحتوى المحلي المحققة (%)",
            value=f"{actual_local_content:.2f}",
            delta=f"{actual_local_content - local_content_target:.2f}"
        )
    
    # رسم بياني لتوزيع المحتوى المحلي
    components_values = [labor_local_value, materials_local_value, services_local_value, equipment_local_value]
    components_labels = ["العمالة", "المواد", "الخدمات", "المعدات والآلات"]
    
    fig = px.pie(
        names=components_labels,
        values=components_values,
        title="توزيع قيمة المحتوى المحلي حسب المكونات",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig.update_traces(textposition="inside", textinfo="percent+value")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # حالة الامتثال للمتطلبات
    st.markdown("### حالة الامتثال لمتطلبات المحتوى المحلي")
    
    if actual_local_content >= local_content_target:
        st.success(f"المشروع يلبي متطلبات المحتوى المحلي (الفائض: {actual_local_content - local_content_target:.2f}%)")
    else:
        st.error(f"المشروع لا يلبي متطلبات المحتوى المحلي (العجز: {local_content_target - actual_local_content:.2f}%)")
        
        # توصيات لتحسين نسبة المحتوى المحلي
        st.markdown("### توصيات لتحسين نسبة المحتوى المحلي")
        
        recommendations = []
        
        if labor_local_percentage < 70:
            recommendations.append("زيادة نسبة العمالة المحلية من خلال التوظيف المباشر أو التعاقد مع شركات محلية.")
        
        if materials_local_percentage < 50:
            recommendations.append("زيادة نسبة المواد المحلية من خلال البحث عن موردين محليين أو استبدال المواد المستوردة بمواد محلية.")
        
        if services_local_percentage < 60:
            recommendations.append("الاعتماد بشكل أكبر على مقدمي الخدمات المحليين والاستعانة بالشركات الوطنية.")
        
        if equipment_local_percentage < 30:
            recommendations.append("محاولة استئجار المعدات من مصادر محلية بدلاً من شرائها من الخارج.")
        
        for i, rec in enumerate(recommendations):
            st.markdown(f"{i+1}. {rec}")
        
        if not recommendations:
            st.markdown("يمكن تحسين النسبة من خلال إعادة توزيع مكونات المشروع وزيادة الاعتماد على المصادر المحلية.")

def show_local_vendors():
    """
    عرض الموردين المحليين
    """
    st.markdown("## قاعدة بيانات الموردين المحليين")
    
    # إنشاء بيانات توضيحية للموردين
    vendors_data = {
        "اسم المورد": [
            "شركة الصناعات السعودية",
            "مؤسسة الخليج للمقاولات",
            "شركة الرياض للإنشاءات",
            "الشركة العربية للمعدات",
            "مصنع المنتجات الإسمنتية",
            "شركة تقنيات البناء",
            "مؤسسة المدار للتوريدات",
            "شركة البنية التحتية المتكاملة",
            "مصنع الصلب السعودي",
            "شركة الأنابيب الوطنية"
        ],
        "القطاع": [
            "صناعة", "مقاولات", "إنشاءات", "معدات", "مواد بناء", 
            "تقنيات بناء", "توريدات", "بنية تحتية", "صناعات معدنية", "أنابيب"
        ],
        "المنطقة": [
            "الرياض", "الشرقية", "مكة المكرمة", "المدينة المنورة", "القصيم",
            "الشرقية", "الرياض", "جدة", "ينبع", "الجبيل"
        ],
        "تصنيف نطاقات": [
            "بلاتيني", "أخضر مرتفع", "أخضر متوسط", "بلاتيني", "أخضر مرتفع",
            "أخضر متوسط", "أخضر منخفض", "بلاتيني", "أخضر مرتفع", "أخضر متوسط"
        ],
        "نسبة السعودة (%)": [
            65, 42, 35, 55, 38, 30, 25, 60, 45, 40
        ],
        "التقييم": [
            4.8, 4.2, 3.9, 4.6, 4.0, 3.7, 3.5, 4.5, 4.3, 4.1
        ]
    }
    
    vendors_df = pd.DataFrame(vendors_data)
    
    # البحث في قاعدة البيانات
    st.markdown("### البحث في قاعدة بيانات الموردين")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_name = st.text_input("البحث باسم المورد", "")
    
    with col2:
        selected_sector = st.selectbox(
            "القطاع",
            ["الكل"] + sorted(vendors_df["القطاع"].unique().tolist())
        )
    
    with col3:
        selected_region = st.selectbox(
            "المنطقة",
            ["الكل"] + sorted(vendors_df["المنطقة"].unique().tolist())
        )
    
    # تطبيق التصفية
    filtered_df = vendors_df.copy()
    
    if search_name:
        filtered_df = filtered_df[filtered_df["اسم المورد"].str.contains(search_name, case=False)]
    
    if selected_sector != "الكل":
        filtered_df = filtered_df[filtered_df["القطاع"] == selected_sector]
    
    if selected_region != "الكل":
        filtered_df = filtered_df[filtered_df["المنطقة"] == selected_region]
    
    # عرض نتائج البحث
    st.markdown(f"### نتائج البحث ({len(filtered_df)} مورد)")
    st.dataframe(filtered_df, use_container_width=True)
    
    # عرض إحصائيات الموردين
    st.markdown("### إحصائيات الموردين المحليين")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # توزيع الموردين حسب المنطقة
        region_counts = vendors_df["المنطقة"].value_counts().reset_index()
        region_counts.columns = ["المنطقة", "عدد الموردين"]
        
        fig1 = px.pie(
            region_counts, 
            values="عدد الموردين", 
            names="المنطقة",
            title="توزيع الموردين حسب المنطقة",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig1.update_traces(textposition="inside", textinfo="percent+label")
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # توزيع الموردين حسب تصنيف نطاقات
        nitaqat_counts = vendors_df["تصنيف نطاقات"].value_counts().reset_index()
        nitaqat_counts.columns = ["تصنيف نطاقات", "عدد الموردين"]
        
        # ترتيب تصنيف نطاقات
        nitaqat_order = {"بلاتيني": 1, "أخضر مرتفع": 2, "أخضر متوسط": 3, "أخضر منخفض": 4, "أصفر": 5, "أحمر": 6}
        nitaqat_counts["الترتيب"] = nitaqat_counts["تصنيف نطاقات"].map(nitaqat_order)
        nitaqat_counts = nitaqat_counts.sort_values("الترتيب")
        
        # اختيار الألوان حسب التصنيف
        nitaqat_colors = {
            "بلاتيني": "#7B68EE", "أخضر مرتفع": "#228B22", "أخضر متوسط": "#32CD32", 
            "أخضر منخفض": "#90EE90", "أصفر": "#FFD700", "أحمر": "#FF4500"
        }
        
        fig2 = px.bar(
            nitaqat_counts, 
            x="تصنيف نطاقات", 
            y="عدد الموردين",
            color="تصنيف نطاقات",
            color_discrete_map=nitaqat_colors,
            title="توزيع الموردين حسب تصنيف نطاقات"
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # قسم إضافة مورد جديد
    st.markdown("### إضافة مورد جديد")
    
    with st.expander("إضافة مورد جديد إلى قاعدة البيانات"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_vendor_name = st.text_input("اسم المورد")
            new_vendor_sector = st.selectbox("القطاع", sorted(vendors_df["القطاع"].unique().tolist()))
            new_vendor_region = st.selectbox("المنطقة", sorted(vendors_df["المنطقة"].unique().tolist()))
        
        with col2:
            new_vendor_nitaqat = st.selectbox(
                "تصنيف نطاقات",
                ["بلاتيني", "أخضر مرتفع", "أخضر متوسط", "أخضر منخفض", "أصفر", "أحمر"]
            )
            new_vendor_saudization = st.slider("نسبة السعودة (%)", 0, 100, 30)
            new_vendor_rating = st.slider("التقييم", 1.0, 5.0, 3.5, 0.1)
        
        if st.button("إضافة المورد"):
            st.success(f"تم إضافة المورد {new_vendor_name} بنجاح!")

def show_vision_requirements():
    """
    عرض متطلبات رؤية 2030
    """
    st.markdown("## متطلبات المحتوى المحلي في رؤية السعودية 2030")
    
    # نص توضيحي
    st.markdown("""
    تعد زيادة المحتوى المحلي أحد الأهداف الاستراتيجية الرئيسية لرؤية السعودية 2030، وذلك من خلال:
    
    - تعزيز المحتوى المحلي في المشتريات الحكومية
    - دعم الصناعات الوطنية والمنتجات المحلية
    - توطين الوظائف والتقنيات
    - تطوير سلاسل الإمداد المحلية
    - تعزيز المشاركة والاستثمار من القطاع الخاص
    """)
    
    # الأهداف الرئيسية
    st.markdown("### الأهداف الرئيسية للمحتوى المحلي في رؤية 2030")
    
    goals_data = {
        "المؤشر": [
            "نسبة المحتوى المحلي في القطاع غير النفطي",
            "نسبة الإنفاق المحلي في المشتريات الحكومية",
            "نسبة توطين الوظائف في القطاع الخاص",
            "عدد المنشآت الصغيرة والمتوسطة المشاركة في سلاسل الإمداد",
            "نسبة مساهمة المنشآت الصغيرة والمتوسطة في الناتج المحلي"
        ],
        "الوضع الحالي": [35, 45, 26, 1200, 22],
        "المستهدف 2025": [50, 60, 35, 3000, 30],
        "المستهدف 2030": [70, 80, 60, 5000, 35]
    }
    
    goals_df = pd.DataFrame(goals_data)
    
    st.table(goals_df)
    
    # رسم بياني للأهداف
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=goals_df["المؤشر"],
        y=goals_df["الوضع الحالي"],
        name="الوضع الحالي",
        marker_color='#1976D2'
    ))
    
    fig.add_trace(go.Bar(
        x=goals_df["المؤشر"],
        y=goals_df["المستهدف 2025"],
        name="المستهدف 2025",
        marker_color='#FFC107'
    ))
    
    fig.add_trace(go.Bar(
        x=goals_df["المؤشر"],
        y=goals_df["المستهدف 2030"],
        name="المستهدف 2030",
        marker_color='#43A047'
    ))
    
    fig.update_layout(
        title="مؤشرات المحتوى المحلي في رؤية 2030",
        xaxis_title="المؤشر",
        yaxis_title="القيمة (%)",
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
# متطلبات المحتوى المحلي حسب القطاع
st.markdown("### متطلبات المحتوى المحلي حسب القطاع")

# بيانات القطاعات
sectors_data = {
    "القطاع": ["النفط والغاز", "الكهرباء", "المياه", "الاتصالات", "النقل", "البناء والتشييد"],
    "نسبة المحتوى المحلي المطلوبة": ["50%", "40%", "45%", "35%", "30%", "25%"]
}

# إنشاء DataFrame
df = pd.DataFrame(sectors_data)

# عرض الجدول في Streamlit
st.dataframe(df)