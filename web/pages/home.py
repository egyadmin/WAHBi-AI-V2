import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

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
    
    # المناقصات المقبلة
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
                'إنشاء مبا