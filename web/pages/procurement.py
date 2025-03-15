import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_procurement():
    """
    عرض صفحة إدارة المشتريات والعقود
    """
    st.subheader("إدارة المشتريات والعقود")
    
    # الخيارات الفرعية
    tabs = st.tabs(["العقود النشطة", "أوامر الشراء", "المناقصات الداخلية", "تقييم الموردين"])
    
    # تبويب العقود النشطة
    with tabs[0]:
        show_active_contracts()
    
    # تبويب أوامر الشراء
    with tabs[1]:
        show_purchase_orders()
    
    # تبويب المناقصات الداخلية
    with tabs[2]:
        show_internal_tenders()
    
    # تبويب تقييم الموردين
    with tabs[3]:
        show_vendor_evaluation()

def show_active_contracts():
    """
    عرض بيانات العقود النشطة
    """
    st.markdown("## العقود النشطة")
    
    # إنشاء بيانات توضيحية للعقود
    current_date = datetime.now().date()
    
    contracts_data = {
        "رقم العقد": ["C-2025-1001", "C-2025-1042", "C-2024-0987", "C-2024-0912", "C-2025-1123", 
                     "C-2024-0875", "C-2025-1088", "C-2025-1156", "C-2024-0932", "C-2025-1201"],
        "المورد": ["شركة الصناعات السعودية", "مؤسسة الخليج للمقاولات", "شركة الرياض للإنشاءات",
                  "الشركة العربية للمعدات", "مصنع المنتجات الإسمنتية", "شركة تقنيات البناء",
                  "مؤسسة المدار للتوريدات", "شركة البنية التحتية المتكاملة", "مصنع الصلب السعودي",
                  "شركة الأنابيب الوطنية"],
        "نوع العقد": ["توريد مواد", "مقاولات", "خدمات هندسية", "تأجير معدات", "توريد مواد",
                     "خدمات فنية", "توريد مواد", "مقاولات", "توريد مواد", "توريد مواد"],
        "تاريخ البدء": [
            current_date - timedelta(days=120),
            current_date - timedelta(days=90),
            current_date - timedelta(days=210),
            current_date - timedelta(days=180),
            current_date - timedelta(days=60),
            current_date - timedelta(days=240),
            current_date - timedelta(days=45),
            current_date - timedelta(days=30),
            current_date - timedelta(days=150),
            current_date - timedelta(days=15)
        ],
        "تاريخ الانتهاء": [
            current_date + timedelta(days=245),
            current_date + timedelta(days=270),
            current_date + timedelta(days=155),
            current_date + timedelta(days=185),
            current_date + timedelta(days=305),
            current_date + timedelta(days=125),
            current_date + timedelta(days=320),
            current_date + timedelta(days=335),
            current_date + timedelta(days=215),
            current_date + timedelta(days=350)
        ],
        "القيمة (مليون ريال)": [12.5, 28.7, 8.3, 6.2, 9.1, 5.4, 7.8, 15.6, 11.2, 10.9],
        "نسبة الإنجاز (%)": [45, 30, 75, 65, 20, 80, 15, 10, 60, 5]
    }
    
    # إنشاء DataFrame
    contracts_df = pd.DataFrame(contracts_data)
    
    # إضافة المدة المتبقية
    contracts_df["المدة المتبقية (يوم)"] = (contracts_df["تاريخ الانتهاء"] - current_date).dt.days
    
    # تصنيف الحالة
    conditions = [
        (contracts_df["المدة المتبقية (يوم)"] < 30),
        (contracts_df["المدة المتبقية (يوم)"] < 90),
        (contracts_df["المدة المتبقية (يوم)"] >= 90)
    ]
    values = ["على وشك الانتهاء", "متوسطة", "طويلة الأجل"]
    colors = ["#D32F2F", "#FFC107", "#4CAF50"]
    
    contracts_df["حالة العقد"] = np.select(conditions, values)
    
    # عرض فلاتر البحث
    col1, col2, col3 = st.columns(3)
    
    with col1:
        contract_type_filter = st.selectbox(
            "نوع العقد",
            ["الكل"] + sorted(contracts_df["نوع العقد"].unique().tolist())
        )
    
    with col2:
        status_filter = st.selectbox(
            "حالة العقد",
            ["الكل"] + sorted(contracts_df["حالة العقد"].unique().tolist())
        )
    
    with col3:
        min_value = st.number_input("الحد الأدنى للقيمة (مليون ريال)", 0.0, 50.0, 0.0)
    
    # تطبيق الفلاتر
    filtered_df = contracts_df.copy()
    
    if contract_type_filter != "الكل":
        filtered_df = filtered_df[filtered_df["نوع العقد"] == contract_type_filter]
    
    if status_filter != "الكل":
        filtered_df = filtered_df[filtered_df["حالة العقد"] == status_filter]
    
    if min_value > 0:
        filtered_df = filtered_df[filtered_df["القيمة (مليون ريال)"] >= min_value]
    
    # عرض العقود المصفاة
    st.dataframe(filtered_df, use_container_width=True)
    
    # تحليلات العقود
    st.markdown("### تحليلات العقود")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # توزيع العقود حسب النوع
        type_distribution = contracts_df.groupby("نوع العقد")["القيمة (مليون ريال)"].sum().reset_index()
        
        fig1 = px.pie(
            type_distribution,
            values="القيمة (مليون ريال)",
            names="نوع العقد",
            title="توزيع قيمة العقود حسب النوع",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig1.update_traces(textposition="inside", textinfo="percent+label")
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # توزيع العقود حسب الحالة
        status_distribution = contracts_df.groupby("حالة العقد").agg({
            "رقم العقد": "count",
            "القيمة (مليون ريال)": "sum"
        }).reset_index()
        
        status_distribution.columns = ["الحالة", "عدد العقود", "إجمالي القيمة (مليون ريال)"]
        
        # ترتيب الحالات
        status_order = {"على وشك الانتهاء": 1, "متوسطة": 2, "طويلة الأجل": 3}
        status_distribution["الترتيب"] = status_distribution["الحالة"].map(status_order)
        status_distribution = status_distribution.sort_values("الترتيب")
        
        # اختيار الألوان حسب الحالة
        status_colors = {"على وشك الانتهاء": "#D32F2F", "متوسطة": "#FFC107", "طويلة الأجل": "#4CAF50"}
        
        fig2 = px.bar(
            status_distribution,
            x="الحالة",
            y="إجمالي القيمة (مليون ريال)",
            color="الحالة",
            text="عدد العقود",
            title="توزيع العقود حسب المدة المتبقية",
            color_discrete_map=status_colors
        )
        
        fig2.update_traces(texttemplate="%{text} عقد", textposition="outside")
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # العقود القريبة من الانتهاء
    st.markdown("### العقود على وشك الانتهاء")
    
    expiring_contracts = contracts_df[contracts_df["المدة المتبقية (يوم)"] < 30].sort_values("المدة المتبقية (يوم)")
    
    if not expiring_contracts.empty:
        for _, contract in expiring_contracts.iterrows():
            st.markdown(f"""
            **{contract['رقم العقد']} - {contract['المورد']}**  
            **نوع العقد:** {contract['نوع العقد']}  
            **المدة المتبقية:** {contract['المدة المتبقية (يوم)']} يوم  
            **نسبة الإنجاز:** {contract['نسبة الإنجاز (%)']}%  
            **القيمة:** {contract['القيمة (مليون ريال)']} مليون ريال
            """)
            
            # شريط التقدم
            st.progress(contract['نسبة الإنجاز (%)'] / 100)
            st.markdown("---")
    else:
        st.info("لا توجد عقود على وشك الانتهاء خلال الشهر القادم")

def show_purchase_orders():
    """
    عرض أوامر الشراء
    """
    st.markdown("## أوامر الشراء")
    
    # إنشاء بيانات توضيحية لأوامر الشراء
    current_date = datetime.now().date()
    
    po_data = {
        "رقم أمر الشراء": [f"PO-{2025}-{i:04d}" for i in range(1001, 1011)],
        "المورد": [
            "شركة الصناعات السعودية", "مؤسسة الخليج للمقاولات", "شركة الرياض للإنشاءات",
            "الشركة العربية للمعدات", "مصنع المنتجات الإسمنتية", "شركة تقنيات البناء",
            "مؤسسة المدار للتوريدات", "شركة البنية التحتية المتكاملة", "مصنع الصلب السعودي",
            "شركة الأنابيب الوطنية"
        ],
        "المشروع": [
            "مشروع توسعة شبكة الطرق", "بناء المدارس", "تطوير البنية التحتية",
            "تحديث شبكة المياه", "بناء المستشفى التخصصي", "إنشاء مركز البيانات",
            "توسعة المطار", "تطوير الحدائق العامة", "بناء المجمع السكني",
            "تطوير شبكة الصرف الصحي"
        ],
        "تاريخ الطلب": [
            current_date - timedelta(days=np.random.randint(5, 60)) for _ in range(10)
        ],
        "تاريخ التسليم المتوقع": [
            current_date + timedelta(days=np.random.randint(5, 45)) for _ in range(10)
        ],
        "القيمة (ريال)": [
            np.random.randint(50000, 5000000) for _ in range(10)
        ],
        "الحالة": np.random.choice(
            ["جديد", "قيد المعالجة", "تم الشحن", "تم الاستلام", "مغلق"],
            size=10,
            p=[0.2, 0.3, 0.2, 0.2, 0.1]
        )
    }
    
    # إنشاء DataFrame
    po_df = pd.DataFrame(po_data)
    
    # عرض فلاتر البحث
    col1, col2 = st.columns(2)
    
    with col1:
        status_filter = st.selectbox(
            "حالة أمر الشراء",
            ["الكل"] + sorted(po_df["الحالة"].unique().tolist())
        )
    
    with col2:
        vendor_filter = st.selectbox(
            "المورد",
            ["الكل"] + sorted(po_df["المورد"].unique().tolist())
        )
    
    # تطبيق الفلاتر
    filtered_po = po_df.copy()
    
    if status_filter != "الكل":
        filtered_po = filtered_po[filtered_po["الحالة"] == status_filter]
    
    if vendor_filter != "الكل":
        filtered_po = filtered_po[filtered_po["المورد"] == vendor_filter]
    
    # عرض أوامر الشراء المصفاة
    st.dataframe(filtered_po, use_container_width=True)
    
    # تحليلات أوامر الشراء
    st.markdown("### تحليلات أوامر الشراء")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # توزيع أوامر الشراء حسب الحالة
        status_counts = po_df.groupby("الحالة").size().reset_index(name="العدد")
        
        fig1 = px.pie(
            status_counts,
            values="العدد",
            names="الحالة",
            title="توزيع أوامر الشراء حسب الحالة",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig1.update_traces(textposition="inside", textinfo="percent+label")
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # قيمة أوامر الشراء حسب المورد
        vendor_values = po_df.groupby("المورد")["القيمة (ريال)"].sum().reset_index()
        vendor_values = vendor_values.sort_values("القيمة (ريال)", ascending=False).head(5)
        
        fig2 = px.bar(
            vendor_values,
            x="المورد",
            y="القيمة (ريال)",
            title="أعلى 5 موردين حسب قيمة أوامر الشراء",
            color="القيمة (ريال)",
            color_continuous_scale="Viridis"
        )
        
        fig2.update_yaxes(title_text="القيمة (ريال)")
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # إضافة أمر شراء جديد
    st.markdown("### إضافة أمر شراء جديد")
    
    with st.expander("إضافة أمر شراء جديد"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_vendor = st.selectbox("المورد", sorted(po_df["المورد"].unique().tolist()))
            new_project = st.selectbox("المشروع", sorted(po_df["المشروع"].unique().tolist()))
            new_value = st.number_input("القيمة (ريال)", min_value=1000, max_value=10000000, value=100000)
        
        with col2:
            new_delivery_date = st.date_input("تاريخ التسليم المتوقع", value=current_date + timedelta(days=30))
            new_description = st.text_area("وصف الطلب", height=100)
        
        if st.button("إضافة أمر الشراء"):
            st.success(f"تم إضافة أمر الشراء بنجاح للمورد {new_vendor} بقيمة {new_value:,} ريال")

def show_internal_tenders():
    """
    عرض المناقصات الداخلية
    """
    st.markdown("## المناقصات الداخلية")
    
    # إنشاء بيانات توضيحية للمناقصات الداخلية
    current_date = datetime.now().date()
    
    tenders_data = {
        "رقم المناقصة": [f"IT-{2025}-{i:04d}" for i in range(1001, 1009)],
        "العنوان": [
            "توريد معدات بناء ثقيلة",
            "شراء مواد إنشائية",
            "خدمات نقل وشحن",
            "توريد أنظمة تكييف",
            "خدمات تركيب كهربائية",
            "توريد محولات كهربائية",
            "خدمات أمن وسلامة",
            "توريد أنظمة مراقبة"
        ],
        "المشروع": [
            "مشروع توسعة شبكة الطرق", "بناء المدارس", "تطوير البنية التحتية",
            "تحديث شبكة المياه", "بناء المستشفى التخصصي", "إنشاء مركز البيانات",
            "توسعة المطار", "تطوير الحدائق العامة"
        ],
        "تاريخ النشر": [current_date - timedelta(days=np.random.randint(5, 30)) for _ in range(8)],
        "الموعد النهائي": [current_date + timedelta(days=np.random.randint(10, 45)) for _ in range(8)],
        "القيمة التقديرية (ريال)": [
            np.random.randint(200000, 10000000) for _ in range(8)
        ],
        "عدد العروض المستلمة": [np.random.randint(0, 10) for _ in range(8)],
        "الحالة": np.random.choice(
            ["مفتوحة", "مغلقة", "قيد التقييم", "تم الترسية", "ملغاة"],
            size=8,
            p=[0.4, 0.1, 0.2, 0.2, 0.1]
        )
    }
    
    # إنشاء DataFrame
    tenders_df = pd.DataFrame(tenders_data)
    
    # عرض فلاتر البحث
    col1, col2 = st.columns(2)
    
    with col1:
        status_filter = st.selectbox(
            "حالة المناقصة",
            ["الكل"] + sorted(tenders_df["الحالة"].unique().tolist())
        )
    
    with col2:
        project_filter = st.selectbox(
            "المشروع",
            ["الكل"] + sorted(tenders_df["المشروع"].unique().tolist())
        )
    
    # تطبيق الفلاتر
    filtered_tenders = tenders_df.copy()
    
    if status_filter != "الكل":
        filtered_tenders = filtered_tenders[filtered_tenders["الحالة"] == status_filter]
    
    if project_filter != "الكل":
        filtered_tenders = filtered_tenders[filtered_tenders["المشروع"] == project_filter]
    
    # عرض المناقصات المصفاة
    st.dataframe(filtered_tenders, use_container_width=True)
    
    # تحليلات المناقصات
    st.markdown("### تحليلات المناقصات الداخلية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # توزيع المناقصات حسب الحالة
        status_counts = tenders_df.groupby("الحالة").size().reset_index(name="العدد")
        
        fig1 = px.pie(
            status_counts,
            values="العدد",
            names="الحالة",
            title="توزيع المناقصات حسب الحالة",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig1.update_traces(textposition="inside", textinfo="percent+label")
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # متوسط عدد العروض حسب نوع المناقصة
        tenders_df["نوع المناقصة"] = tenders_df["العنوان"].apply(
            lambda x: "توريد" if "توريد" in x else "خدمات" if "خدمات" in x else "أخرى"
        )
        
        avg_offers = tenders_df.groupby("نوع المناقصة")["عدد العروض المستلمة"].mean().reset_index()
        avg_offers["عدد العروض المستلمة"] = avg_offers["عدد العروض المستلمة"].round(1)
        
        fig2 = px.bar(
            avg_offers,
            x="نوع المناقصة",
            y="عدد العروض المستلمة",
            title="متوسط عدد العروض حسب نوع المناقصة",
            color="نوع المناقصة",
            text="عدد العروض المستلمة"
        )
        
        fig2.update_traces(texttemplate="%{text}", textposition="outside")
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # المناقصات القريبة من الإغلاق
    st.markdown("### المناقصات القريبة من الموعد النهائي")
    
    closing_soon = tenders_df[
        (tenders_df["الموعد النهائي"] > current_date) & 
        (tenders_df["الموعد النهائي"] <= current_date + timedelta(days=7)) &
        (tenders_df["الحالة"] == "مفتوحة")
    ].sort_values("الموعد النهائي")
    
    if not closing_soon.empty:
        for _, tender in closing_soon.iterrows():
            days_left = (tender["الموعد النهائي"] - current_date).days
            
            st.markdown(f"""
            **{tender['رقم المناقصة']} - {tender['العنوان']}**  
            **المشروع:** {tender['المشروع']}  
            **الموعد النهائي:** {tender['الموعد النهائي'].strftime('%Y/%m/%d')} ({days_left} أيام متبقية)  
            **القيمة التقديرية:** {tender['القيمة التقديرية (ريال)']:,} ريال  
            **العروض المستلمة حتى الآن:** {tender['عدد العروض المستلمة']}
            """)
            st.markdown("---")
    else:
        st.info("لا توجد مناقصات على وشك الإغلاق خلال الأسبوع القادم")

def show_vendor_evaluation():
    """
    عرض تقييم الموردين
    """
    st.markdown("## تقييم الموردين")
    
    # إنشاء بيانات توضيحية لتقييم الموردين
    vendors_eval_data = {
        "المورد": [
            "شركة الصناعات السعودية", "مؤسسة الخليج للمقاولات", "شركة الرياض للإنشاءات",
            "الشركة العربية للمعدات", "مصنع المنتجات الإسمنتية", "شركة تقنيات البناء",
            "مؤسسة المدار للتوريدات", "شركة البنية التحتية المتكاملة", "مصنع الصلب السعودي",
            "شركة الأنابيب الوطنية"
        ],
        "الفئة": [
            "مواد بناء", "مقاولات", "خدمات هندسية", "معدات", "مواد خام", 
            "تقنيات", "مواد متنوعة", "بنية تحتية", "صناعات معدنية", "أنابيب"
        ],
        "جودة المنتجات (5)": [4.5, 3.8, 4.2, 3.2, 4.7, 3.5, 3.9, 4.3, 4.6, 4.1],
        "الالتزام بالمواعيد (5)": [4.2, 3.5, 4.0, 2.8, 4.5, 3.7, 3.6, 4.4, 4.3, 3.9],
        "التنافسية السعرية (5)": [3.8, 4.2, 3.5, 4.6, 3.7, 4.1, 4.4, 3.8, 3.6, 4.0],
        "الاستجابة والتواصل (5)": [4.3, 3.9, 4.5, 3.5, 4.2, 3.6, 3.8, 4.1, 4.4, 4.0],
        "نسبة المحتوى المحلي (%)": [85, 92, 78, 65, 100, 70, 88, 75, 95, 82],
        "عدد المشاريع المنفذة": [12, 8, 10, 5, 7, 6, 4, 9, 11, 8]
    }
    
    # إنشاء DataFrame
    vendors_eval_df = pd.DataFrame(vendors_eval_data)
    
    # حساب التقييم العام
    eval_weights = {
        "جودة المنتجات (5)": 0.35,
        "الالتزام بالمواعيد (5)": 0.25,
        "التنافسية السعرية (5)": 0.2,
        "الاستجابة والتواصل (5)": 0.2
    }
    
    # حساب التقييم المرجح
    for col, weight in eval_weights.items():
        vendors_eval_df[f"{col} (مرجح)"] = vendors_eval_df[col] * weight
    
    vendors_eval_df["التقييم العام"] = vendors_eval_df[[f"{col} (مرجح)" for col in eval_weights.keys()]].sum(axis=1)
    
    # تصنيف الموردين
    conditions = [
        (vendors_eval_df["التقييم العام"] >= 4.5),
        (vendors_eval_df["التقييم العام"] >= 4.0),
        (vendors_eval_df["التقييم العام"] >= 3.5),
        (vendors_eval_df["التقييم العام"] >= 3.0),
        (vendors_eval_df["التقييم العام"] < 3.0)
    ]
    values = ["ممتاز", "جيد جداً", "جيد", "مقبول", "ضعيف"]
    vendors_eval_df["التصنيف"] = np.select(conditions, values)
    
    # عرض مقارنة الموردين
    st.markdown("### مقارنة تقييمات الموردين")
    
    selected_vendors = st.multiselect(
        "اختر الموردين للمقارنة",
        vendors_eval_df["المورد"].tolist(),
        default=vendors_eval_df["المورد"].tolist()[:5]
    )
    
    if selected_vendors:
        # تصفية البيانات
        selected_df = vendors_eval_df[vendors_eval_df["المورد"].isin(selected_vendors)]
        
# تصفية البيانات
if selected_vendors:
    selected_df = vendors_eval_df[vendors_eval_df["المورد"].isin(selected_vendors)]
    st.dataframe(selected_df)
else:
    st.write("يرجى اختيار مورد لعرض البيانات.")