import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def create_sample_tenders_data():
    """
    إنشاء بيانات توضيحية للمناقصات
    """
    # تواريخ عشوائية خلال الشهرين القادمين
    today = datetime.now().date()
    dates = [today + timedelta(days=np.random.randint(1, 60)) for _ in range(20)]
    
    # حالات المناقصات
    statuses = ['جديدة', 'قيد التحليل', 'جاهزة للتقديم', 'تم التقديم', 'انتهت']
    
    # الجهات
    agencies = [
        'وزارة الإسكان', 'وزارة النقل', 'أمانة الرياض', 'الهيئة الملكية', 
        'وزارة الصحة', 'وزارة التعليم', 'شركة أرامكو', 'شركة سابك', 
        'هيئة المدن الصناعية', 'الهيئة العامة للترفيه'
    ]
    
    # القطاعات
    sectors = ['البنية التحتية', 'المباني', 'الطرق', 'الطاقة', 'المياه', 'الصحة', 'التعليم', 'الصناعة']
    
    # إنشاء البيانات
    data = {
        'رقم المناقصة': [f"T-{2025}-{np.random.randint(1000, 9999)}" for _ in range(20)],
        'الجهة': [np.random.choice(agencies) for _ in range(20)],
        'اسم المشروع': [
            'إنشاء طريق دائري', 'تطوير شبكة مياه', 'بناء مدرسة', 'تجديد مستشفى',
            'إنشاء حديقة عامة', 'تطوير منطقة صناعية', 'صيانة طرق', 'بناء مركز تجاري',
            'تطوير بنية تحتية', 'إنشاء محطة تحلية', 'بناء مجمع سكني', 'تطوير مركز أبحاث',
            'صيانة شبكة كهرباء', 'إنشاء ملاعب رياضية', 'تطوير مطار', 'إنشاء مبنى إداري',
            'تطوير شبكة اتصالات', 'بناء مركز ثقافي', 'إنشاء محطة طاقة شمسية', 'تطوير منطقة ساحلية'
        ],
        'القيمة التقديرية (مليون)': np.random.uniform(10, 200, 20).round(1),
        'الموعد النهائي': dates,
        'حالة المناقصة': [np.random.choice(statuses, p=[0.3, 0.3, 0.2, 0.1, 0.1]) for _ in range(20)],
        'المحتوى المحلي المطلوب': [np.random.randint(30, 70) for _ in range(20)],
        'القطاع': [np.random.choice(sectors) for _ in range(20)]
    }
    
    return pd.DataFrame(data)

def show_home_page():
    """
    عرض الصفحة الرئيسية مع لوحة المعلومات
    """
    # بيانات توضيحية للمناقصات النشطة
    active_tenders = create_sample_tenders_data()
    
    # عرض المؤشرات الرئيسية
    st.subheader("المؤشرات الرئيسية")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="المناقصات النشطة",
            value=f"{len(active_tenders)}",
            delta="3 ↑"
        )
    
    with col2:
        st.metric(
            label="متوسط المحتوى المحلي",
            value="67.8%",
            delta="2.5% ↑"
        )
    
    with col3:
        st.metric(
            label="العطاءات الفائزة",
            value="12",
            delta="2 ↑"
        )
    
    with col4:
        st.metric(
            label="قيمة المشاريع (مليون ريال)",
            value="463.5",
            delta="85.2 ↑"
        )
    
    # عرض المناقصات النشطة
    st.subheader("المناقصات النشطة")
    st.dataframe(
        active_tenders[['رقم المناقصة', 'الجهة', 'اسم المشروع', 'القيمة التقديرية (مليون)', 'الموعد النهائي', 'حالة المناقصة']], 
        use_container_width=True
    )
    
    # توزيع المناقصات حسب القطاع
    st.subheader("توزيع المناقصات حسب القطاع")
    sectors_df = active_tenders.groupby('القطاع').size().reset_index(name='عدد المناقصات')
    
    fig = px.pie(
        sectors_df, 
        values='عدد المناقصات', 
        names='القطاع',
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="توزيع المناقصات حسب القطاع"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    
    # المناقصات المقبلة والتوقعات
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("المناقصات المقبلة")
        upcoming_df = active_tenders[active_tenders['الموعد النهائي'] > datetime.now().date()]
        upcoming_df = upcoming_df.sort_values('الموعد النهائي')
        
        for _, row in upcoming_df.head(5).iterrows():
            with st.container():
                st.markdown(f"""
                **{row['اسم المشروع']}**  
                **الجهة:** {row['الجهة']}  
                **القيمة التقديرية:** {row['القيمة التقديرية (مليون)']} مليون ريال  
                **الموعد النهائي:** {row['الموعد النهائي'].strftime('%Y/%m/%d')}
                """)
                st.markdown("---")
    
    with col2:
        st.subheader("توقعات النجاح")
        
        # بيانات توضيحية لتوقعات النجاح
        prediction_data = {
            'المشروع': [
                'تطوير البنية التحتية في المنطقة الشرقية',
                'إنشاء مباني سكنية في الرياض',
                'صيانة الطرق في المدينة المنورة',
                'توسعة شبكة المياه في جدة',
                'إنشاء مركز بيانات في الدمام'
            ],
            'احتمالية النجاح': [85, 72, 63, 91, 77]
        }
        
        for i, proj in enumerate(prediction_data['المشروع']):
            prob = prediction_data['احتمالية النجاح'][i]
            color = "green" if prob >= 80 else "orange" if prob >= 60 else "red"
            
            st.markdown(f"**{proj}**")
            st.progress(prob/100)
            st.markdown(f"<span style='color:{color}'><b>احتمالية النجاح: {prob}%</b></span>", unsafe_allow_html=True)
            st.markdown("---")
    
    # توزيع المناقصات حسب الشهر (كمثال على رسم بياني إضافي)
    st.subheader("توزيع المناقصات حسب الشهر")
    
    # إضافة شهر كعمود في DataFrame
    active_tenders['الشهر'] = active_tenders['الموعد النهائي'].apply(lambda x: x.strftime('%Y-%m'))
    monthly_df = active_tenders.groupby('الشهر').size().reset_index(name='عدد المناقصات')
    
    fig = px.bar(
        monthly_df, 
        x='الشهر', 
        y='عدد المناقصات',
        color='عدد المناقصات',
        color_continuous_scale='Viridis',
        title="توزيع المناقصات حسب الشهر"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # روابط سريعة للعمليات الشائعة
    st.subheader("روابط سريعة")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("تحليل مناقصة جديدة", key="new_analysis"):
            st.session_state.page = "تحليل المناقصات"
            st.experimental_rerun()
    
    with col2:
        if st.button("البحث في قاعدة الموردين", key="search_vendors"):
            st.session_state.page = "الموردون والمقاولون"
            st.experimental_rerun()
    
    with col3:
        if st.button("تقرير المحتوى المحلي", key="local_content_report"):
            st.session_state.page = "المحتوى المحلي"
            st.experimental_rerun()

# اختبار مستقل للصفحة
if __name__ == "__main__":
    st.set_page_config(
        page_title="نظام تحليل المناقصات - الصفحة الرئيسية",
        page_icon="📊",
        layout="wide",
    )
    show_home_page()