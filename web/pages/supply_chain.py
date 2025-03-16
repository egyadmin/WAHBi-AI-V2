import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show_supply_chain():
    """
    عرض صفحة تحليل سلاسل الإمداد
    """
    st.subheader("إدارة سلاسل الإمداد")
    
    # إنشاء القائمة الجانبية للخيارات
    options = st.sidebar.radio(
        "اختر القسم",
        ["تحليل الموردين", "تحليل المخاطر", "التكاليف والتسعير", "التحسين والتوقعات"]
    )
    
    if options == "تحليل الموردين":
        show_vendor_analysis()
    elif options == "تحليل المخاطر":
        show_risk_analysis()
    elif options == "التكاليف والتسعير":
        show_cost_pricing()
    elif options == "التحسين والتوقعات":
        show_optimization()

def show_vendor_analysis():
    """
    عرض تحليل الموردين
    """
    st.markdown("## تحليل الموردين")
    
    # إنشاء بيانات توضيحية للموردين
    vendor_data = {
        "المورد": [
            "شركة الصناعات السعودية", 
            "مؤسسة الخليج للمقاولات", 
            "شركة الرياض للإنشاءات",
            "الشركة العربية للمعدات",
            "مصنع المنتجات الإسمنتية",
            "شركة تقنيات البناء",
            "مؤسسة المدار للتوريدات",
            "شركة البنية التحتية المتكاملة"
        ],
        "الفئة": [
            "مواد بناء", 
            "مقاولات", 
            "خدمات هندسية",
            "معدات",
            "مواد خام",
            "تقنيات",
            "مواد متنوعة",
            "خدمات هندسية"
        ],
        "قيمة التوريدات (مليون ريال)": [25.4, 18.2, 12.7, 9.8, 8.5, 7.3, 6.1, 5.8],
        "نسبة المحتوى المحلي (%)": [85, 92, 78, 65, 100, 70, 88, 75],
        "متوسط وقت التسليم (أيام)": [14, 30, 21, 45, 7, 15, 10, 25],
        "التقييم العام (5)": [4.2, 3.8, 4.5, 3.5, 4.0, 4.3, 3.7, 4.1]
    }
    
    vendor_df = pd.DataFrame(vendor_data)
    
    # عرض بيانات الموردين
    st.markdown("### بيانات الموردين الرئيسيين")
    st.dataframe(vendor_df, use_container_width=True)
    
    # تحليلات الموردين
    col1, col2 = st.columns(2)
    
    with col1:
        # توزيع الموردين حسب الفئة
        st.markdown("### توزيع الموردين حسب الفئة")
        
        category_counts = vendor_df.groupby("الفئة")["قيمة التوريدات (مليون ريال)"].sum().reset_index()
        
        fig1 = px.pie(
            category_counts, 
            values="قيمة التوريدات (مليون ريال)", 
            names="الفئة",
            title="توزيع قيمة التوريدات حسب الفئة",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig1.update_traces(textposition="inside", textinfo="percent+label")
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # تقييم الموردين مقابل نسبة المحتوى المحلي
        st.markdown("### تقييم الموردين مقابل نسبة المحتوى المحلي")
        
        fig2 = px.scatter(
            vendor_df, 
            x="نسبة المحتوى المحلي (%)", 
            y="التقييم العام (5)",
            size="قيمة التوريدات (مليون ريال)",
            color="الفئة",
            hover_name="المورد",
            title="تقييم الموردين مقابل نسبة المحتوى المحلي",
            size_max=50
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # تحليل أوقات التسليم
    st.markdown("### تحليل أوقات التسليم")
    
    fig3 = px.bar(
        vendor_df.sort_values("متوسط وقت التسليم (أيام)"), 
        x="المورد", 
        y="متوسط وقت التسليم (أيام)",
        color="متوسط وقت التسليم (أيام)",
        color_continuous_scale="Viridis",
        title="متوسط وقت التسليم حسب المورد"
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # توصيات تحسين سلسلة الإمداد
    st.markdown("### توصيات لتحسين سلسلة الإمداد")
    
    recommendations = [
        "تنويع قاعدة الموردين في فئة المعدات لتقليل المخاطر",
        "العمل مع الموردين لتحسين أوقات التسليم خاصة مع الشركة العربية للمعدات",
        "زيادة الاعتماد على الموردين ذوي نسب المحتوى المحلي الأعلى",
        "وضع خطة لتقليل الاعتماد على الموردين ذوي التقييم المنخفض",
        "تطوير برنامج لتحسين أداء الموردين من خلال التدريب والدعم الفني"
    ]
    
    for i, rec in enumerate(recommendations):
        st.markdown(f"{i+1}. {rec}")

def show_risk_analysis():
    """
    عرض تحليل مخاطر سلسلة الإمداد
    """
    st.markdown("## تحليل مخاطر سلسلة الإمداد")
    
    # إنشاء بيانات توضيحية للمخاطر
    risk_data = {
        "المخاطرة": [
            "تأخر توريد المواد الرئيسية",
            "ارتفاع تكلفة المواد الخام",
            "تعطل وسائل النقل",
            "مشاكل جودة المنتجات",
            "نقص في المخزون",
            "تغير متطلبات المشروع",
            "مخاطر تقلبات العملة",
            "أزمات الموردين المالية",
            "الكوارث الطبيعية",
            "المخاطر السياسية والتشريعية"
        ],
        "الاحتمالية": [0.4, 0.6, 0.3, 0.5, 0.4, 0.7, 0.2, 0.3, 0.1, 0.2],
        "التأثير": [0.7, 0.6, 0.5, 0.8, 0.6, 0.5, 0.4, 0.7, 0.9, 0.8],
        "الفئة": [
            "توريد", "تكلفة", "لوجستيات", "جودة", "تخطيط",
            "متطلبات", "مالية", "موردين", "خارجية", "تنظيمية"
        ]
    }
    
    risk_df = pd.DataFrame(risk_data)
    
    # إضافة درجة المخاطرة
    risk_df["درجة المخاطرة"] = risk_df["الاحتمالية"] * risk_df["التأثير"]
    
    # تصنيف المخاطر
    conditions = [
        (risk_df["درجة المخاطرة"] >= 0.4),
        (risk_df["درجة المخاطرة"] >= 0.2),
        (risk_df["درجة المخاطرة"] < 0.2)
    ]
    values = ["عالية", "متوسطة", "منخفضة"]
    risk_df["مستوى المخاطرة"] = np.select(conditions, values)
    
    # عرض مصفوفة المخاطر
    st.markdown("### مصفوفة مخاطر سلسلة الإمداد")
    
    fig1 = px.scatter(
        risk_df, 
        x="الاحتمالية", 
        y="التأثير",
        color="مستوى المخاطرة",
        size="درجة المخاطرة",
        hover_name="المخاطرة",
        text="المخاطرة",
        color_discrete_map={"عالية": "#FF5733", "متوسطة": "#FFC300", "منخفضة": "#33FF57"},
        title="مصفوفة تحليل المخاطر",
        size_max=50
    )
    
    fig1.update_layout(
        xaxis_title="احتمالية الحدوث",
        yaxis_title="مستوى التأثير",
        xaxis=dict(range=[0, 1]),
        yaxis=dict(range=[0, 1])
    )
    
    fig1.update_traces(
        textposition="top center",
        textfont=dict(size=10)
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # عرض جدول المخاطر
    st.markdown("### قائمة المخاطر مرتبة حسب درجة الخطورة")
    
    sorted_risks = risk_df.sort_values("درجة المخاطرة", ascending=False)
    
    # تنسيق العرض
    formatted_risks = sorted_risks.copy()
    formatted_risks["الاحتمالية"] = formatted_risks["الاحتمالية"].apply(lambda x: f"{x:.1%}")
    formatted_risks["التأثير"] = formatted_risks["التأثير"].apply(lambda x: f"{x:.1%}")
    formatted_risks["درجة المخاطرة"] = formatted_risks["درجة المخاطرة"].apply(lambda x: f"{x:.1%}")
    
    st.dataframe(formatted_risks, use_container_width=True)
    
    # المخاطر حسب الفئة
    st.markdown("### المخاطر حسب الفئة")
    
    category_risks = risk_df.groupby("الفئة")["درجة المخاطرة"].mean().reset_index()
    category_risks = category_risks.sort_values("درجة المخاطرة", ascending=False)
    
    fig2 = px.bar(
        category_risks,
        x="الفئة",
        y="درجة المخاطرة",
        color="درجة المخاطرة",
        color_continuous_scale="Reds",
        title="متوسط درجة المخاطرة حسب الفئة"
    )
    
    fig2.update_layout(yaxis_tickformat=".1%")
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # استراتيجيات تخفيف المخاطر
    st.markdown("### استراتيجيات تخفيف المخاطر ذات الأولوية العالية")
    
    high_risks = sorted_risks[sorted_risks["مستوى المخاطرة"] == "عالية"]
    
    mitigation_strategies = {
        "تأخر توريد المواد الرئيسية": "إنشاء قاعدة موردين بديلة وتطوير خطط طوارئ للتوريد",
        "ارتفاع تكلفة المواد الخام": "توقيع عقود طويلة الأجل وتأمين أسعار ثابتة",
        "مشاكل جودة المنتجات": "تعزيز نظام فحص الجودة وتطوير معايير قبول صارمة",
        "تغير متطلبات المشروع": "تحسين عمليات إدارة التغيير وتوثيق المتطلبات بشكل أفضل",
        "أزمات الموردين المالية": "تقييم الصحة المالية للموردين بشكل دوري واستخدام ضمانات التنفيذ",
        "الكوارث الطبيعية": "تطوير خطط استمرارية الأعمال واستخدام موردين من مناطق جغرافية متنوعة"
    }
    
    for _, risk in high_risks.iterrows():
        risk_name = risk["المخاطرة"]
        strategy = mitigation_strategies.get(risk_name, "وضع استراتيجية مخصصة للتخفيف من هذه المخاطر")
        
        st.markdown(f"**{risk_name}** (درجة المخاطرة: {risk['درجة المخاطرة']})")
        st.markdown(f"*استراتيجية التخفيف:* {strategy}")
        st.markdown("---")

def show_cost_pricing():
    """
    عرض تحليل التكاليف والتسعير
    """
    st.markdown("## تحليل التكاليف والتسعير")
    
    # إنشاء بيانات توضيحية للمواد
    materials_data = {
        "المادة": [
            "حديد تسليح", 
            "إسمنت", 
            "خرسانة جاهزة", 
            "طوب", 
            "رمل", 
            "خشب", 
            "مواد عازلة", 
            "كابلات كهربائية",
            "أنابيب",
            "أصباغ"
        ],
        "متوسط السعر (ريال/وحدة)": [3200, 15, 240, 2.5, 75, 1200, 85, 120, 160, 65],
        "الكمية المتوقعة": [150, 8000, 1200, 25000, 350, 200, 750, 2000, 1500, 300],
        "نسبة التغير السعري (%)": [12, 5, 8, 2, 3, 15, 7, 10, 6, 4],
        "المصدر": [
            "محلي", "محلي", "محلي", "محلي", "محلي", 
            "مستورد", "مستورد", "محلي", "محلي", "مستورد"
        ]
    }
    
    materials_df = pd.DataFrame(materials_data)
    
    # حساب إجمالي التكلفة
    materials_df["إجمالي التكلفة (ريال)"] = materials_df["متوسط السعر (ريال/وحدة)"] * materials_df["الكمية المتوقعة"]
    
    # حساب تأثير التغير السعري
    materials_df["تأثير التغير السعري (ريال)"] = materials_df["إجمالي التكلفة (ريال)"] * (materials_df["نسبة التغير السعري (%)"] / 100)
    
    # عرض بيانات المواد
    st.markdown("### تحليل تكاليف المواد الرئيسية")
    
    # تنسيق العرض
    formatted_materials = materials_df.copy()
    formatted_materials["إجمالي التكلفة (ريال)"] = formatted_materials["إجمالي التكلفة (ريال)"].map(lambda x: f"{x:,.0f}")
    formatted_materials["تأثير التغير السعري (ريال)"] = formatted_materials["تأثير التغير السعري (ريال)"].map(lambda x: f"{x:,.0f}")
    
    st.dataframe(formatted_materials, use_container_width=True)
    
    # إجمالي التكاليف والمؤشرات
    total_cost = materials_df["إجمالي التكلفة (ريال)"].sum()
    total_price_impact = materials_df["تأثير التغير السعري (ريال)"].sum()
    avg_price_change = materials_df["نسبة التغير السعري (%)"].mean()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="إجمالي تكلفة المواد (ريال)",
            value=f"{total_cost:,.0f}"
        )
    
    with col2:
        st.metric(
            label="تأثير التغير السعري (ريال)",
            value=f"{total_price_impact:,.0f}",
            delta=f"{total_price_impact / total_cost:.1%}"
        )
    
    with col3:
        st.metric(
            label="متوسط نسبة التغير السعري",
            value=f"{avg_price_change:.1f}%"
        )
    
    # توزيع التكاليف حسب المواد
    st.markdown("### توزيع تكاليف المواد")
    
    fig1 = px.pie(
        materials_df, 
        values="إجمالي التكلفة (ريال)", 
        names="المادة",
        title="توزيع تكاليف المواد",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig1.update_traces(textposition="inside", textinfo="percent+label")
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # تأثير التغير السعري حسب المادة
    st.markdown("### تأثير التغير السعري حسب المادة")
    
    sorted_impact = materials_df.sort_values("تأثير التغير السعري (ريال)", ascending=False)
    
    fig2 = px.bar(
        sorted_impact,
        x="المادة",
        y="تأثير التغير السعري (ريال)",
        color="نسبة التغير السعري (%)",
        color_continuous_scale="Reds",
        title="تأثير التغير السعري حسب المادة"
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # مقارنة المواد المحلية والمستوردة
    st.markdown("### مقارنة المواد المحلية والمستوردة")
    
    source_comparison = materials_df.groupby("المصدر").agg({
        "إجمالي التكلفة (ريال)": "sum",
        "تأثير التغير السعري (ريال)": "sum",
        "المادة": "count"
    }).reset_index()
    
    source_comparison.columns = ["المصدر", "إجمالي التكلفة (ريال)", "تأثير التغير السعري (ريال)", "عدد المواد"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # نسبة التكلفة حسب المصدر
        fig3 = px.pie(
            source_comparison, 
            values="إجمالي التكلفة (ريال)", 
            names="المصدر",
            title="توزيع التكاليف: محلي مقابل مستورد",
            color_discrete_map={"محلي": "#1976D2", "مستورد": "#D32F2F"}
        )
        
        fig3.update_traces(textposition="inside", textinfo="percent+label")
        
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # متوسط تأثير التغير السعري حسب المصدر
        source_comparison["متوسط تأثير التغير لكل مادة"] = source_comparison["تأثير التغير السعري (ريال)"] / source_comparison["عدد المواد"]
        
        fig4 = px.bar(
            source_comparison,
            x="المصدر",
            y="متوسط تأثير التغير لكل مادة",
            color="المصدر",
            title="متوسط تأثير التغير السعري حسب المصدر",
            color_discrete_map={"محلي": "#1976D2", "مستورد": "#D32F2F"}
        )
        
        st.plotly_chart(fig4, use_container_width=True)
    
    # توصيات لتحسين التكاليف
    st.markdown("### توصيات لتحسين التكاليف")
    
    recommendations = [
        "إبرام عقود طويلة الأجل للمواد ذات التغير السعري المرتفع (الحديد والخشب)",
        "البحث عن موردين محليين بديلين للمواد المستوردة لتقليل تأثير تقلبات الأسعار",
        "شراء المواد ذات الاستهلاك العالي بكميات كبيرة للحصول على خصومات الكمية",
        "تطوير استراتيجية تخزين للمواد ذات التأثير السعري المرتفع",
        "استخدام نماذج التنبؤ لتوقيت الشراء بشكل أفضل وتجنب فترات ارتفاع الأسعار"
    ]
    
    for i, rec in enumerate(recommendations):
        st.markdown(f"{i+1}. {rec}")

def show_optimization():
    """
    عرض تحسين سلسلة الإمداد والتوقعات
    """
    st.markdown("## تحسين سلسلة الإمداد والتوقعات")
    
    # 1. تحسين المخزون
    st.markdown("### تحسين مستويات المخزون")
    
    # إنشاء بيانات توضيحية للمخزون
    inventory_data = {
        "المادة": [
            "حديد تسليح", "إسمنت", "خرسانة جاهزة", "طوب", "رمل", 
            "خشب", "مواد عازلة", "كابلات كهربائية", "أنابيب", "أصباغ"
        ],
        "المخزون الحالي": [35, 1200, 80, 8000, 120, 45, 200, 450, 320, 85],
        "الحد الأدنى المطلوب": [20, 800, 60, 5000, 100, 30, 150, 300, 250, 50],
        "الحد الأقصى": [50, 2000, 120, 12000, 200, 60, 300, 600, 400, 120],
        "متوسط الاستهلاك اليومي": [2, 60, 10, 400, 8, 3, 12, 25, 15, 5],
        "وقت إعادة الطلب (أيام)": [15, 7, 3, 10, 5, 20, 15, 12, 10, 8]
    }
    
    inventory_df = pd.DataFrame(inventory_data)
    
    # حساب مؤشرات المخزون
    inventory_df["أيام التغطية المتبقية"] = inventory_df["المخزون الحالي"] / inventory_df["متوسط الاستهلاك اليومي"]
    inventory_df["حالة المخزون"] = np.where(
        inventory_df["المخزون الحالي"] < inventory_df["الحد الأدنى المطلوب"],
        "منخفض",
        np.where(
            inventory_df["المخزون الحالي"] > inventory_df["الحد الأقصى"],
            "مرتفع",
            "مناسب"
        )
    )
    
    inventory_df["توصية"] = np.where(
        inventory_df["أيام التغطية المتبقية"] < inventory_df["وقت إعادة الطلب (أيام)"],
        "يجب الطلب الآن",
        "المخزون كافي"
    )
    
    # تنسيق العرض
    formatted_inventory = inventory_df.copy()
    formatted_inventory["أيام التغطية المتبقية"] = formatted_inventory["أيام التغطية المتبقية"].round(1)
    
    # عرض بيانات المخزون
    st.dataframe(formatted_inventory, use_container_width=True)
    
    # تحليل حالة المخزون
    col1, col2 = st.columns(2)
    
    with col1:
        # مخطط حالة المخزون
        status_counts = inventory_df["حالة المخزون"].value_counts().reset_index()
        status_counts.columns = ["الحالة", "العدد"]
        
        fig1 = px.pie(
            status_counts, 
            values="العدد", 
            names="الحالة",
            title="توزيع حالة المخزون",
            color_discrete_map={
                "منخفض": "#D32F2F", 
                "مناسب": "#43A047", 
                "مرتفع": "#FFC107"
            }
        )
        
        fig1.update_traces(textposition="inside", textinfo="percent+label")
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # أيام التغطية للمواد
        st.markdown("### أيام التغطية المتبقية للمخزون")
        
        fig2 = px.bar(
            inventory_df.sort_values("أيام التغطية المتبقية"),
            x="المادة",
            y="أيام التغطية المتبقية",
            color="حالة المخزون",
            title="أيام التغطية المتبقية للمخزون",
            color_discrete_map={
                "منخفض": "#D32F2F", 
                "مناسب": "#43A047", 
                "مرتفع": "#FFC107"
            }
        )
        
        # إضافة خط لوقت إعادة الطلب
        for i, row in inventory_df.iterrows():
            fig2.add_shape(
                type="line",
                x0=i-0.4,
                x1=i+0.4,
                y0=row["وقت إعادة الطلب (أيام)"],
                y1=row["وقت إعادة الطلب (أيام)"],
                line=dict(color="red", width=2, dash="dash")
            )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # 2. تحليل التوقعات المستقبلية
    st.markdown("### التوقعات المستقبلية للطلب والأسعار")
    
    # إنشاء بيانات توضيحية للتوقعات
    months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", 
              "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
    
forecast_data = {
    "الشهر": months,
    "الطلب المتوقع (طن)": [250, 265, 280, 300]  # تأكد من إغلاق القوس
}
