"""
نظام تحليل المناقصات وسلاسل الإمداد والتوقعات المستقبلية
تطبيق خاص بشركة شبه الجزيرة للمقاولات

مهندس التطوير: م. تامر الجوهري
"""

import os
import sys
import yaml
import json
import logging
from datetime import datetime
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# إضافة المجلد الرئيسي للمسار
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# استيراد المكونات الضرورية
from web.pages.home import show_home_page
from web.pages.tender_analysis import show_tender_analysis
from web.pages.requirements import show_requirements_analysis
from web.pages.cost_estimation import show_cost_estimation
from web.pages.risk_analysis import show_risk_analysis
from web.pages.timeline import show_timeline
from web.pages.local_content import show_local_content
from web.pages.supply_chain import show_supply_chain
from web.pages.procurement import show_procurement
from web.pages.vendors import show_vendors
from web.pages.future_projects import show_future_projects
from web.pages.success_prediction import show_success_prediction
from web.pages.reports import show_reports

from web.components.sidebar import create_sidebar
from web.components.header import create_header

from utils.file_handler import setup_logging

# إعداد التسجيل
setup_logging()
logger = logging.getLogger("TenderAnalysisSystem")

# تحميل الإعدادات
def load_config():
    config_path = os.path.join(current_dir, "config", "config.yaml")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}

# تهيئة حالة الجلسة
def initialize_session():
    if 'config' not in st.session_state:
        st.session_state.config = load_config()
    
    if 'page' not in st.session_state:
        st.session_state.page = "الرئيسية"
    
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}
    
    if 'current_tender' not in st.session_state:
        st.session_state.current_tender = None
    
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {
            "company": "شركة شبه الجزيرة للمقاولات",
            "user_name": "المستخدم الحالي",
            "role": "محلل مناقصات"
        }
    
    if 'latest_predictions' not in st.session_state:
        st.session_state.latest_predictions = None

# إعداد صفحة Streamlit
def setup_page():
    st.set_page_config(
        page_title="نظام تحليل المناقصات - شركة شبه الجزيرة للمقاولات",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # إضافة CSS المخصص
    with open(os.path.join(current_dir, "web", "styles", "main.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # إضافة CSS للغة العربية
    with open(os.path.join(current_dir, "web", "styles", "rtl.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# التطبيق الرئيسي
def main():
    # تهيئة الجلسة وإعداد الصفحة
    initialize_session()
    setup_page()
    
    # إنشاء الشريط الجانبي
    selected_page = create_sidebar()
    
    # إنشاء رأس الصفحة
    create_header()
    
    # عرض الصفحة المحددة
    if selected_page == "الرئيسية":
        show_home_page()
    
    elif selected_page == "تحليل المناقصات":
        show_tender_analysis()
    
    elif selected_page == "تحليل المتطلبات":
        show_requirements_analysis()
    
    elif selected_page == "تقدير التكاليف":
        show_cost_estimation()
    
    elif selected_page == "تحليل المخاطر":
        show_risk_analysis()
    
    elif selected_page == "الجدول الزمني":
        show_timeline()
    
    elif selected_page == "المحتوى المحلي":
        show_local_content()
    
    elif selected_page == "سلاسل الإمداد":
        show_supply_chain()
    
    elif selected_page == "المشتريات":
        show_procurement()
    
    elif selected_page == "الموردون والمقاولون":
        show_vendors()
    
    elif selected_page == "المشاريع المستقبلية":
        show_future_projects()
    
    elif selected_page == "توقع احتمالية النجاح":
        show_success_prediction()
    
    elif selected_page == "التقارير":
        show_reports()
    
    # تسجيل زيارة الصفحة
    logger.info(f"تمت زيارة صفحة {selected_page}")

if __name__ == "__main__":
    main()