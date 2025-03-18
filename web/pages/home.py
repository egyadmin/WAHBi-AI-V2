import streamlit as st
import pandas as pd
import plotly.express as px

def show_home_page():
    """
    عرض الصفحة الرئيسية لتطبيق تحليل المناقصات مع سلاسل الإمداد والمحتوى المحلي
    """
    # إعداد صفحة البداية
    st.set_page_config(
        page_title="نظام تحليل المناقصات",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # العنوان الرئيسي
    st.title("نظام تحليل المناقصات مع سلاسل الإمداد والمحتوى المحلي")
    st.markdown("---")
    
    # عرض لوحة المعلومات الرئيسية
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="المناقصات النشطة", value="24", delta="4")
    
    with col2:
        st.metric(label="نسبة المحتوى المحلي", value="68%", delta="2.5%")
    
    with col3:
        st.metric(label="الموردين المحليين", value="156", delta="12")
    
    # عرض رسم بياني توضيحي (مثال)
    st.subheader("توزيع المناقصات حسب القطاع")
    
    # بيانات توضيحية
    data = {
        'القطاع': ['البنية التحتية', 'الطاقة', 'التقنية', 'الصحة', 'التعليم', 'النقل'],
        'عدد المناقصات': [15, 12, 8, 10, 5, 7],
        'متوسط المحتوى المحلي': [72, 65, 45, 60, 80, 58]
    }
    
    df = pd.DataFrame(data)
    
    # رسم بياني
    fig = px.bar(
        df, 
        x='القطاع', 
        y='عدد المناقصات',
        color='متوسط المحتوى المحلي',
        color_continuous_scale='Viridis',
        title='توزيع المناقصات حسب القطاع والمحتوى المحلي'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # الشريط الجانبي
    with st.sidebar:
        st.title("لوحة التحكم")
        st.markdown("---")
        
        # خيارات التحليل
        st.subheader("خيارات التحليل")
        analysis_type = st.selectbox(
            "نوع التحليل",
            ["تحليل المناقصات", "تحليل المحتوى المحلي", "تحليل سلاسل الإمداد"]
        )
        
        # فلترة حسب التاريخ
        st.subheader("الفترة الزمنية")
        date_range = st.date_input(
            "اختر الفترة الزمنية",
            value=[pd.to_datetime("2024-01-01"), pd.to_datetime("2024-03-01")]
        )
        
        # زر لتطبيق التحليل
        if st.button("تحليل البيانات"):
            st.success("تم تطبيق التحليل بنجاح!")

if __name__ == "__main__":
    show_home_page()