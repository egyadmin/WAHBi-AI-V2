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
            {"المتطلب": "توفير الصي