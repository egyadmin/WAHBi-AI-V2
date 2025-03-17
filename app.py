import os
import sys
import streamlit as st
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import base64
from io import BytesIO

# إضافة المسار الرئيسي للمشروع إلى PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# تكوين الصفحة
st.set_page_config(
    page_title="نظام WAHBi-AI-V2",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# إضافة CSS للدعم العربي وتحسين المظهر
def add_custom_css():
    custom_css = """
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    
    * {
        font-family: 'Tajawal', sans-serif;
    }
    
    html {
        direction: rtl;
    }
    
    .stApp {
        direction: rtl;
    }
    
    .css-1d391kg, .css-1cpxqw2 {
        direction: rtl;
        text-align: right;
    }
    
    div[data-testid="stVerticalBlock"] {
        direction: rtl;
    }
    
    button[data-testid="baseButton-secondary"] {
        background-color: #1e88e5;
        border-color: #1e88e5;
        color: white;
    }
    
    button[data-testid="baseButton-primary"] {
        background-color: #28a745;
        border-color: #28a745;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1e88e5;
    }
    
    div[data-testid="stMetricDelta"] {
        font-size: 0.9rem;
    }
    
    div[data-testid="stMetricLabel"] {
        font-weight: 500;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Tajawal', sans-serif;
        font-weight: 700;
    }
    
    .dashboard-title {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .insights-box {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 1rem;
        background-color: #f9f9f9;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        direction: rtl;
    }
    
    .stTabs [data-baseweb="tab"] {
        direction: rtl;
        text-align: right;
    }
    
    /* تصحيح مشكلة الجداول */
    .stDataFrame {
        direction: rtl;
    }
    
    /* تصحيح الاتجاه في فلاتر متعدد الاختيار */
    div[data-testid="stMultiSelect"] {
        direction: rtl;
        text-align: right;
    }
    """
    st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

# إضافة CSS
add_custom_css()

# إعداد نظام التسجيل
def setup_app_logging():
    """إعداد نظام التسجيل"""
    try:
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log"),
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        return logging.getLogger(__name__)
    except Exception as e:
        st.error(f"خطأ في إعداد التسجيل: {str(e)}")
        return logging.getLogger(__name__)

logger = setup_app_logging()

# دوال ونماذج محاكاة للوحدات الفعلية
def get_config():
    """محاكاة لوحدة config.config.get_config"""
    return {
        "app": {
            "name": "نظام WAHBi-AI-V2 لإدارة المناقصات والعقود",
            "version": "1.2.0",
            "description": "نظام متكامل لإدارة المناقصات والعقود مدعوم بالذكاء الاصطناعي"
        },
        "paths": {
            "logs_dir": "logs",
            "data_dir": "data",
            "models_dir": "models",
            "reports_dir": "reports"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "wahbi_ai_db",
            "user": "db_user"
        },
        "api": {
            "base_url": "https://api.wahbi-ai.org",
            "version": "v1",
            "timeout": 30
        },
        "ai": {
            "models": {
                "text_analysis": "ar_nlp_v2",
                "risk_assessment": "risk_model_v1",
                "prediction": "tender_prediction_v3"
            },
            "parameters": {
                "confidence_threshold": 0.75,
                "batch_size": 16
            }
        }
    }

def load_local_content():
    """محاكاة لوحدة modules.local_content.load_local_content"""
    logger.info("تحميل بيانات المحتوى المحلي")
    return True

def load_ai_models():
    """محاكاة لوحدة modules.ai_models.load_ai_models"""
    logger.info("تحميل نماذج الذكاء الاصطناعي")
    return True

def process_document(document_path):
    """محاكاة لوحدة modules.document_processor.process_document"""
    logger.info(f"معالجة المستند: {document_path}")
    return {
        "success": True,
        "pages": 12,
        "entities": 45,
        "requirements": 32
    }

def analyze_requirements(req_text):
    """محاكاة لوحدة modules.requirement_analyzer.analyze_requirements"""
    logger.info("تحليل المتطلبات")
    return {
        "functional": [],
        "non_functional": [],
        "constraints": [],
        "risks": []
    }

def analyze_cost_risk(project_data):
    """محاكاة لوحدة modules.cost_risk_analyzer.analyze_cost_risk"""
    logger.info("تحليل مخاطر التكلفة")
    return {
        "total_risk_score": 0.65,
        "cost_overrun_probability": 0.35,
        "schedule_delay_probability": 0.42
    }

def init_database():
    """محاكاة لوحدة utils.database.init_database"""
    logger.info("تهيئة قاعدة البيانات")
    return True

def setup_logging():
    """محاكاة لوحدة utils.helpers.setup_logging"""
    logger.info("إعداد نظام التسجيل")
    return True

def handle_uploaded_files(files):
    """محاكاة لوحدة utils.file_handler.handle_uploaded_files"""
    logger.info(f"معالجة الملفات المرفوعة: {len(files)} ملفات")
    return {
        "success": True,
        "processed": len(files)
    }

def setup_api_connections():
    """محاكاة لوحدة utils.api_integrations.setup_api_connections"""
    logger.info("إعداد اتصالات API")
    return True

def get_procurement_plan(tender_id):
    """محاكاة لوحدة supply_chain.procurement_planner.get_procurement_plan"""
    logger.info(f"الحصول على خطة المشتريات للمناقصة: {tender_id}")
    return {
        "phases": [
            {"name": "التخطيط", "start": "2024-04-01", "end": "2024-04-15"},
            {"name": "طرح المناقصة", "start": "2024-04-16", "end": "2024-05-15"},
            {"name": "التقييم", "start": "2024-05-16", "end": "2024-06-01"},
            {"name": "الترسية", "start": "2024-06-02", "end": "2024-06-10"},
            {"name": "التعاقد", "start": "2024-06-11", "end": "2024-06-25"}
        ],
        "estimated_cost": 3500000,
        "local_content_target": 60
    }

def analyze_project_requirements(req_file):
    """محاكاة لوحدة analysis.requirement_analyzer.analyze_project_requirements"""
    logger.info(f"تحليل متطلبات المشروع: {req_file}")
    return {
        "total_requirements": 32,
        "functional_requirements": 24,
        "non_functional_requirements": 8,
        "complexity": "متوسطة",
        "effort_estimate": "85 يوم عمل"
    }

def analyze_risks(project_data):
    """محاكاة لوحدة analysis.risk_analyzer.analyze_risks"""
    logger.info("تحليل المخاطر")
    return {
        "risk_count": 12,
        "high_risks": 3,
        "medium_risks": 5,
        "low_risks": 4
    }

def estimate_costs(project_scope):
    """محاكاة لوحدة analysis.cost_estimator.estimate_costs"""
    logger.info("تقدير التكاليف")
    return {
        "total_cost": 4250000,
        "labor_cost": 2800000,
        "material_cost": 850000,
        "overhead_cost": 600000
    }

def analyze_local_content(supply_chain_data):
    """محاكاة لوحدة analysis.local_content_analyzer.analyze_local_content"""
    logger.info("تحليل المحتوى المحلي")
    return {
        "average_local_content": 62.5,
        "potential_increase": 15.8,
        "suppliers_count": {
            "local": 12,
            "foreign": 5,
            "joint": 3
        }
    }

# تحميل بيانات العرض التوضيحي
def load_demo_data():
    """تحميل بيانات توضيحية للعرض"""
    # بيانات المناقصات
    tenders_data = {
        "رقم المناقصة": [f"RFP-2024-{i:03d}" for i in range(1, 21)],
        "العنوان": [
            "توريد معدات تقنية", "خدمات صيانة", "تطوير نظام إلكتروني", 
            "توريد أجهزة طبية", "خدمات استشارية", "تنفيذ مشروع بنية تحتية",
            "خدمات أمن المعلومات", "توريد أثاث مكتبي", "تطوير تطبيقات موبايل",
            "خدمات تدريب", "توريد وتركيب أنظمة مراقبة", "صيانة مباني",
            "تطوير محتوى تعليمي", "خدمات نظافة", "توريد سيارات",
            "تنفيذ حملة إعلامية", "تطوير موقع إلكتروني", "خدمات لوجستية",
            "توريد مستلزمات مكتبية", "تركيب أنظمة تكييف"
        ],
        "تاريخ الإعلان": [
            (datetime.now() - timedelta(days=np.random.randint(1, 60))).strftime('%Y-%m-%d')
            for _ in range(20)
        ],
        "تاريخ الإغلاق": [
            (datetime.now() + timedelta(days=np.random.randint(5, 45))).strftime('%Y-%m-%d')
            for _ in range(20)
        ],
        "القيمة التقديرية": [
            round(np.random.uniform(100000, 5000000), -3)
            for _ in range(20)
        ],
        "الحالة": np.random.choice(
            ["جديدة", "مفتوحة", "قيد التقييم", "معلقة", "مغلقة", "ملغاة"],
            size=20,
            p=[0.15, 0.25, 0.25, 0.1, 0.2, 0.05]
        ),
        "نسبة النجاح المتوقعة": [
            round(np.random.uniform(30, 95), 1)
            for _ in range(20)
        ]
    }
    
    # بيانات العقود
    contracts_data = {
        "رقم العقد": [f"CONT-2024-{i:03d}" for i in range(1, 16)],
        "رقم المناقصة": [f"RFP-2024-{i:03d}" for i in range(1, 16)],
        "المورد": [
            "شركة التقنية المتطورة", "مؤسسة الحلول الذكية", "شركة الخدمات المتكاملة",
            "مجموعة الإبداع التقني", "شركة التطوير الرقمي", "مؤسسة الجودة الشاملة",
            "شركة الاتصالات المتقدمة", "مؤسسة البناء الحديث", "شركة التقنيات الذكية",
            "مجموعة الخدمات الاستشارية", "شركة الحلول الهندسية", "مؤسسة التطوير والابتكار",
            "شركة الأنظمة المتكاملة", "مجموعة الخدمات اللوجستية", "شركة المشاريع التقنية"
        ],
        "تاريخ البدء": [
            (datetime.now() - timedelta(days=np.random.randint(1, 120))).strftime('%Y-%m-%d')
            for _ in range(15)
        ],
        "تاريخ الانتهاء": [
            (datetime.now() + timedelta(days=np.random.randint(30, 365))).strftime('%Y-%m-%d')
            for _ in range(15)
        ],
        "القيمة": [
            round(np.random.uniform(80000, 4500000), -3)
            for _ in range(15)
        ],
        "نسبة الإنجاز": [
            round(np.random.uniform(0, 100), 1)
            for _ in range(15)
        ],
        "المحتوى المحلي": [
            round(np.random.uniform(20, 95), 1)
            for _ in range(15)
        ],
        "مستوى المخاطر": np.random.choice(
            ["منخفض", "متوسط", "عالي"],
            size=15,
            p=[0.4, 0.4, 0.2]
        )
    }
    
    # بيانات المخاطر
    risks_data = {
        "الرمز": [f"RISK-{i:02d}" for i in range(1, 13)],
        "الوصف": [
            "تأخر في تسليم المواد", "تجاوز الميزانية المخططة", "مشاكل في جودة المنتجات",
            "تغيير في المتطلبات", "مشاكل في توفر الموارد", "تضارب في الجدول الزمني",
            "مشاكل فنية غير متوقعة", "تغييرات في الأنظمة واللوائح", "تأخر في الموافقات",
            "مشاكل مع الموردين الفرعيين", "صعوبات في الحصول على التصاريح", "نقص في المهارات المطلوبة"
        ],
        "التأثير": np.random.choice(
            ["منخفض", "متوسط", "عالي", "حرج"],
            size=12,
            p=[0.2, 0.4, 0.3, 0.1]
        ),
        "الاحتمالية": np.random.choice(
            ["منخفضة", "متوسطة", "عالية"],
            size=12,
            p=[0.3, 0.5, 0.2]
        ),
        "المعالجة": np.random.choice(
            ["تجنب", "تخفيف", "نقل", "قبول"],
            size=12
        ),
        "المسؤول": [
            "مدير المشروع", "مدير المشتريات", "مدير الجودة", "مدير المالية",
            "مدير تقنية المعلومات", "مدير الموارد البشرية", "مدير العمليات",
            "المستشار القانوني", "مدير المشروع", "مدير المشتريات", 
            "مدير الجودة", "مدير المالية"
        ],
        "الحالة": np.random.choice(
            ["جديدة", "قيد المعالجة", "معالجة", "مغلقة"],
            size=12,
            p=[0.25, 0.4, 0.25, 0.1]
        )
    }
    
    # بيانات المحتوى المحلي
    local_content_data = {
        "الفئة": ["توظيف", "توطين التقنية", "سلاسل التوريد", "البحث والتطوير", "التدريب"],
        "النسبة المستهدفة": [60, 40, 55, 25, 45],
        "النسبة الحالية": [53.2, 35.8, 48.7, 18.4, 42.1],
        "التغير السنوي": ["+8.2%", "+5.5%", "+3.2%", "+7.1%", "+9.3%"]
    }
    
    # بيانات التحليل المالي
    financial_data = {
        "الشهر": [f"شهر {i}" for i in range(1, 13)],
        "المخطط": [
            round(np.random.uniform(1000000, 1500000), -3)
            for _ in range(12)
        ],
        "الفعلي": [
            round(np.random.uniform(800000, 1600000), -3)
            for _ in range(12)
        ]
    }
    
    financial_df = pd.DataFrame(financial_data)
    financial_df["الفرق"] = financial_df["الفعلي"] - financial_df["المخطط"]
    financial_df["نسبة الانحراف"] = (financial_df["الفرق"] / financial_df["المخطط"] * 100).round(1)
    
    return pd.DataFrame(tenders_data), pd.DataFrame(contracts_data), pd.DataFrame(risks_data), pd.DataFrame(local_content_data), financial_df

def initialize_app():
    """تهيئة التطبيق وتحميل المتطلبات الأساسية"""
    try:
        # إعداد متغيرات الجلسة
        if 'is_initialized' not in st.session_state:
            st.session_state.is_initialized = False
            
            config = get_config()
            st.session_state.app_name = config["app"]["name"]
            st.session_state.app_version = config["app"]["version"]
            st.session_state.user_role = "مدير النظام"
            
            # محاكاة تهيئة النظام
            init_database()
            load_local_content()
            load_ai_models()
            setup_api_connections()
            
            # تحميل البيانات التوضيحية وتخزينها في الجلسة
            tenders_df, contracts_df, risks_df, local_content_df, financial_df = load_demo_data()
            st.session_state.tenders_df = tenders_df
            st.session_state.contracts_df = contracts_df
            st.session_state.risks_df = risks_df
            st.session_state.local_content_df = local_content_df
            st.session_state.financial_df = financial_df
            
            st.session_state.is_initialized = True
            
            # تسجيل بدء تشغيل التطبيق
            logger.info(f"تم بدء تشغيل {st.session_state.app_name} v{st.session_state.app_version}")
            
        return True
    except Exception as e:
        logger.error(f"خطأ في تهيئة التطبيق: {str(e)}")
        st.error(f"خطأ في تهيئة التطبيق: {str(e)}")
        return False

def render_sidebar():
    """عرض القائمة الجانبية"""
    with st.sidebar:
        # عنوان التطبيق
        st.title(f"📋 {st.session_state.app_name}")
        st.caption(f"الإصدار: {st.session_state.app_version}")
        
        st.markdown("---")
        
        # القائمة الرئيسية
        selected_page = st.radio(
            "القائمة الرئيسية:",
            ["الرئيسية", "المناقصات والعقود", "تحليل المتطلبات", "تخطيط سلسلة التوريد", "تحليل المخاطر", "توقع النجاح", "المحتوى المحلي", "التقارير", "لوحة المؤشرات"]
        )
        
        st.markdown("---")
        
        # إحصائيات سريعة
        st.subheader("إحصائيات سريعة")
        
        # عرض بعض الإحصائيات
        col1, col2 = st.columns(2)
        with col1:
            active_tenders = len(st.session_state.tenders_df[st.session_state.tenders_df['الحالة'].isin(['جديدة', 'مفتوحة', 'قيد التقييم'])])
            st.metric(label="المناقصات النشطة", value=active_tenders)
        
        with col2:
            active_contracts = len(st.session_state.contracts_df[pd.to_datetime(st.session_state.contracts_df['تاريخ الانتهاء']) > datetime.now()])
            st.metric(label="العقود الجارية", value=active_contracts)
        
        st.markdown("---")
        
        # معلومات المستخدم
        st.subheader("معلومات المستخدم")
        st.write(f"**المستخدم:** {st.session_state.user_role}")
        st.write(f"**تاريخ الدخول:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        st.markdown("---")
        
        # معلومات النظام
        st.caption("© 2024 جميع الحقوق محفوظة")
        st.caption("فريق تطوير البرمجيات")
    
    return selected_page

def render_header():
    """عرض رأس الصفحة"""
    col1, col2, col3 = st.columns([2, 5, 2])
    
    with col1:
        st.write("## 📋")
    
    with col2:
        st.title("نظام WAHBi-AI-V2")
        st.caption("منصة متكاملة لإدارة المناقصات والعقود مدعومة بالذكاء الاصطناعي")
    
    with col3:
        st.write(f"**التاريخ:** {datetime.now().strftime('%Y-%m-%d')}")
        st.write(f"**المستخدم:** {st.session_state.user_role}")
    
    st.markdown("---")

def home_page():
    """صفحة الرئيسية"""
    # العنوان الرئيسي
    st.markdown("<h1 style='text-align: center;'>نظام WAHBi-AI-V2 لإدارة المناقصات والعقود</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em;'>مدعوم بتقنيات الذكاء الاصطناعي والتحليل المتقدم</p>", unsafe_allow_html=True)
    
    # مؤشرات الأداء الرئيسية
    st.markdown("## 📊 مؤشرات الأداء الرئيسية")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_tenders = len(st.session_state.tenders_df[st.session_state.tenders_df['الحالة'].isin(['جديدة', 'مفتوحة', 'قيد التقييم'])])
        st.metric(
            "المناقصات النشطة", 
            active_tenders,
            "+3"
        )
    
    with col2:
        active_contracts = len(st.session_state.contracts_df[pd.to_datetime(st.session_state.contracts_df['تاريخ الانتهاء']) > datetime.now()])
        st.metric(
            "العقود الجارية", 
            active_contracts,
            "+1"
        )
    
    with col3:
        avg_success = round(st.session_state.tenders_df['نسبة النجاح المتوقعة'].mean(), 1)
        st.metric(
            "متوسط نسبة النجاح المتوقعة", 
            f"{avg_success}%",
            "+2.5%"
        )
    
    with col4:
        avg_local_content = round(st.session_state.contracts_df['المحتوى المحلي'].mean(), 1)
        st.metric(
            "متوسط المحتوى المحلي", 
            f"{avg_local_content}%",
            "+5.3%"
        )
    
    # رسوم بيانية
    st.markdown("## 📈 تحليل البيانات")
    
    tab1, tab2, tab3 = st.tabs(["📑 المناقصات", "📝 العقود", "⚠️ المخاطر"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # توزيع المناقصات حسب الحالة
            status_counts = st.session_state.tenders_df['الحالة'].value_counts().reset_index()
            status_counts.columns = ['الحالة', 'العدد']
            
            fig = px.pie(
                status_counts, 
                values='العدد', 
                names='الحالة',
                title='توزيع المناقصات حسب الحالة',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig.update_layout(
                title_font_size=20,
                title_font_family="Tajawal",
                title_x=0.5,
                legend_title_font_size=16
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # نسب النجاح المتوقعة للمناقصات النشطة
            active_tenders = st.session_state.tenders_df[st.session_state.tenders_df['الحالة'].isin(['جديدة', 'مفتوحة', 'قيد التقييم'])]
            active_tenders = active_tenders.sort_values('نسبة النجاح المتوقعة', ascending=False).head(8)
            
            fig = px.bar(
                active_tenders,
                x='نسبة النجاح المتوقعة',
                y='رقم المناقصة',
title='نسب النجاح المتوقعة للمناقصات النشطة',
                color='نسبة النجاح المتوقعة',
                color_continuous_scale='Viridis',
                orientation='h'
            )
            fig.update_layout(
                title_font_size=20,
                title_font_family="Tajawal",
                title_x=0.5,
                yaxis={'categoryorder':'total ascending'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # توزيع قيم العقود
            fig = px.histogram(
                st.session_state.contracts_df,
                x='القيمة',
                nbins=10,
                title='توزيع قيم العقود',
                color_discrete_sequence=['#3498db']
            )
            fig.update_layout(
                title_font_size=20,
                title_font_family="Tajawal",
                title_x=0.5,
                xaxis_title="القيمة (ريال)",
                yaxis_title="عدد العقود"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # نسب المحتوى المحلي
            fig = px.scatter(
                st.session_state.contracts_df,
                x='القيمة',
                y='المحتوى المحلي',
                size='نسبة الإنجاز',
                color='مستوى المخاطر',
                hover_name='رقم العقد',
                title='نسب المحتوى المحلي للعقود',
                color_discrete_map={
                    'منخفض': '#2ecc71',
                    'متوسط': '#f39c12',
                    'عالي': '#e74c3c'
                }
            )
            fig.update_layout(
                title_font_size=20,
                title_font_family="Tajawal",
                title_x=0.5,
                xaxis_title="القيمة (ريال)",
                yaxis_title="نسبة المحتوى المحلي (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # مصفوفة المخاطر
            risk_matrix = pd.crosstab(
                st.session_state.risks_df['التأثير'], 
                st.session_state.risks_df['الاحتمالية'],
                margins=False
            )
            
            # تحويل القيم إلى حرارية
            risk_severity = {
                ('منخفض', 'منخفضة'): 1,
                ('منخفض', 'متوسطة'): 2,
                ('منخفض', 'عالية'): 3,
                ('متوسط', 'منخفضة'): 2,
                ('متوسط', 'متوسطة'): 4,
                ('متوسط', 'عالية'): 6,
                ('عالي', 'منخفضة'): 3,
                ('عالي', 'متوسطة'): 6,
                ('عالي', 'عالية'): 9,
                ('حرج', 'منخفضة'): 4,
                ('حرج', 'متوسطة'): 8,
                ('حرج', 'عالية'): 12
            }
            
            # تحضير بيانات المصفوفة
            impact_order = ['منخفض', 'متوسط', 'عالي', 'حرج']
            probability_order = ['منخفضة', 'متوسطة', 'عالية']
            
            # إنشاء مصفوفة حرارية
            heat_values = []
            annotations = []
            
            for impact in impact_order:
                heat_row = []
                for prob in probability_order:
                    try:
                        value = risk_matrix.loc[impact, prob]
                    except:
                        value = 0
                    heat_row.append(risk_severity.get((impact, prob), 0))
                    annotations.append(dict(
                        text=str(value),
                        x=prob,
                        y=impact,
                        showarrow=False
                    ))
                heat_values.append(heat_row)
            
            # إنشاء الرسم البياني
            fig = go.Figure(data=go.Heatmap(
                z=heat_values,
                x=probability_order,
                y=impact_order,
                colorscale=[
                    [0.0, "#2ecc71"],  # أخضر للمخاطر المنخفضة
                    [0.33, "#f1c40f"],  # أصفر للمخاطر المتوسطة
                    [0.66, "#e67e22"],  # برتقالي للمخاطر العالية
                    [1.0, "#e74c3c"]    # أحمر للمخاطر الحرجة
                ],
                showscale=False
            ))
            
            # إضافة النصوص
            for annotation in annotations:
                fig.add_annotation(annotation)
            
            fig.update_layout(
                title='مصفوفة المخاطر',
                title_font_size=20,
                title_font_family="Tajawal",
                title_x=0.5,
                xaxis_title="الاحتمالية",
                yaxis_title="التأثير"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # توزيع المخاطر حسب استراتيجية المعالجة
            treatment_counts = st.session_state.risks_df['المعالجة'].value_counts().reset_index()
            treatment_counts.columns = ['المعالجة', 'العدد']
            
            fig = px.bar(
                treatment_counts,
                x='المعالجة',
                y='العدد',
                title='استراتيجيات معالجة المخاطر',
                color='المعالجة',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                title_font_size=20,
                title_font_family="Tajawal",
                title_x=0.5,
                xaxis_title="استراتيجية المعالجة",
                yaxis_title="عدد المخاطر"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # قسم المناقصات القادمة
    st.markdown("## 📅 المناقصات القادمة للإغلاق")
    upcoming_tenders = st.session_state.tenders_df[
        (pd.to_datetime(st.session_state.tenders_df['تاريخ الإغلاق']) > datetime.now()) &
        (pd.to_datetime(st.session_state.tenders_df['تاريخ الإغلاق']) <= datetime.now() + timedelta(days=14))
    ]
    upcoming_tenders = upcoming_tenders.sort_values('تاريخ الإغلاق')
    
    if not upcoming_tenders.empty:
        # عرض المناقصات في جدول
        upcoming_display = upcoming_tenders[['رقم المناقصة', 'العنوان', 'تاريخ الإغلاق', 'القيمة التقديرية', 'نسبة النجاح المتوقعة']]
        upcoming_display['أيام متبقية'] = (pd.to_datetime(upcoming_display['تاريخ الإغلاق']) - datetime.now()).dt.days
        upcoming_display['القيمة التقديرية'] = upcoming_display['القيمة التقديرية'].apply(lambda x: f"{x:,.0f} ريال")
        upcoming_display['نسبة النجاح المتوقعة'] = upcoming_display['نسبة النجاح المتوقعة'].apply(lambda x: f"{x}%")
        
        st.dataframe(
            upcoming_display,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("لا توجد مناقصات ستغلق خلال الأسبوعين القادمين")
    
    # قسم تحليل الذكاء الاصطناعي
    st.markdown("## 🤖 تحليلات الذكاء الاصطناعي")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### التنبؤ بنجاح المناقصات")
        st.markdown("""
        تستخدم خوارزميات الذكاء الاصطناعي لتحليل البيانات التاريخية وتحديد العوامل المؤثرة في نجاح المناقصات. 
        يمكن للنظام التنبؤ بنسب النجاح المتوقعة للمناقصات الجديدة بناءً على خصائصها ومتطلباتها.
        """)
        
        if st.button("تحليل مناقصة جديدة", key="analyze_new_tender"):
            with st.spinner("جاري تحليل المناقصة..."):
                time.sleep(2)  # محاكاة وقت المعالجة
                st.success("تم التحليل بنجاح!")
                st.info("نسبة النجاح المتوقعة للمناقصة: 78.5%")
                st.markdown("""
                **العوامل المؤثرة في النتيجة:**
                - قدرة عالية على تلبية المتطلبات الفنية (+15%)
                - توافق المنتج مع المعايير المطلوبة (+12%)
                - خبرة سابقة مع نفس الجهة (+10%)
                - المنافسة المتوقعة قوية (-7%)
                """)
    
    with col2:
        st.markdown("### تحليل المتطلبات")
        st.markdown("""
        يقوم النظام بتحليل وثائق المتطلبات باستخدام تقنيات معالجة اللغة الطبيعية لاستخراج البنود المهمة والمخاطر المحتملة.
        يساعد هذا التحليل في تقييم مدى تعقيد المتطلبات وتحديد النقاط التي تحتاج إلى اهتمام خاص.
        """)
        
        uploaded_file = st.file_uploader("رفع ملف متطلبات للتحليل", type=['pdf', 'docx', 'txt'])
        if uploaded_file is not None:
            with st.spinner("جاري تحليل المتطلبات..."):
                time.sleep(3)  # محاكاة وقت المعالجة
                st.success("تم تحليل المتطلبات بنجاح!")
                
                # عرض نتائج التحليل
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("عدد المتطلبات", "27")
                    st.metric("المتطلبات الوظيفية", "19")
                    st.metric("المتطلبات غير الوظيفية", "8")
                
                with col2:
                    st.metric("درجة التعقيد", "متوسطة")
                    st.metric("المخاطر المحتملة", "4")
                    st.metric("البنود الغامضة", "3")

def dashboard_page():
    """صفحة لوحة المؤشرات"""
    st.markdown("# 📊 لوحة المؤشرات")
    
    st.markdown("""
    ## لوحة مؤشرات الأداء الرئيسية
    
    استخدم هذه اللوحة لمراقبة أداء المؤشرات الرئيسية للنظام واستعراض الإحصائيات والاتجاهات.
    """)
    
    # المؤشرات الرئيسية
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_success = round(st.session_state.tenders_df['نسبة النجاح المتوقعة'].mean(), 1)
        st.metric(
            "متوسط نسبة النجاح",
            f"{avg_success}%",
            "+2.5%"
        )
    
    with col2:
        avg_local_content = round(st.session_state.contracts_df['المحتوى المحلي'].mean(), 1)
        st.metric(
            "متوسط المحتوى المحلي",
            f"{avg_local_content}%",
            "+5.3%"
        )
    
    with col3:
        active_contracts = len(st.session_state.contracts_df[pd.to_datetime(st.session_state.contracts_df['تاريخ الانتهاء']) > datetime.now()])
        avg_contract_value = round(st.session_state.contracts_df['القيمة'].mean() / 1000000, 2)
        st.metric(
            "متوسط قيمة العقود",
            f"{avg_contract_value} مليون",
            "+0.8 مليون"
        )
    
    with col4:
        high_risks = len(st.session_state.risks_df[st.session_state.risks_df['التأثير'].isin(['عالي', 'حرج']) & st.session_state.risks_df['الاحتمالية'].isin(['متوسطة', 'عالية'])])
        st.metric(
            "المخاطر العالية",
            high_risks,
            "-2"
        )
    
    # الرسوم البيانية الرئيسية
    st.markdown("## تحليلات رئيسية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # توزيع المناقصات حسب الحالة
        status_counts = st.session_state.tenders_df['الحالة'].value_counts().reset_index()
        status_counts.columns = ['الحالة', 'العدد']
        
        fig = px.pie(
            status_counts, 
            values='العدد', 
            names='الحالة',
            title='توزيع المناقصات حسب الحالة',
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_layout(
            title_font_size=20,
            title_font_family="Tajawal",
            title_x=0.5,
            legend_title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # تحليل المحتوى المحلي
        local_df = st.session_state.local_content_df
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=local_df['الفئة'],
            y=local_df['النسبة الحالية'],
            name='النسبة الحالية',
            marker_color='#3498db'
        ))
        
        fig.add_trace(go.Bar(
            x=local_df['الفئة'],
            y=local_df['النسبة المستهدفة'],
            name='النسبة المستهدفة',
            marker_color='#2ecc71'
        ))
        
        fig.update_layout(
            barmode='group',
            title_text='تحليل المحتوى المحلي',
            title_font_size=20,
            title_font_family="Tajawal",
            title_x=0.5,
            xaxis_title="الفئة",
            yaxis_title="النسبة المئوية (%)",
            legend_title="النسبة",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # تحليل المالي
    st.markdown("## التحليل المالي والموازنة")
    
    financial_df = st.session_state.financial_df
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=financial_df['الشهر'],
        y=financial_df['المخطط'],
        name='المخطط',
        line=dict(color='#3498db', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=financial_df['الشهر'],
        y=financial_df['الفعلي'],
        name='الفعلي',
        line=dict(color='#e74c3c', width=2)
    ))
    
    fig.update_layout(
        title_text='مقارنة التكاليف المخططة والفعلية',
        title_font_size=20,
        title_font_family="Tajawal",
        title_x=0.5,
        xaxis_title="الشهر",
        yaxis_title="التكلفة (ريال)",
        legend_title="النوع",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # المشاريع القادمة
    st.markdown("## المشاريع والمناقصات القادمة")
    
    upcoming_tenders = st.session_state.tenders_df[
        (pd.to_datetime(st.session_state.tenders_df['تاريخ الإغلاق']) > datetime.now()) &
        (pd.to_datetime(st.session_state.tenders_df['تاريخ الإغلاق']) <= datetime.now() + timedelta(days=30))
    ]
    
    if not upcoming_tenders.empty:
        upcoming_display = upcoming_tenders[['رقم المناقصة', 'العنوان', 'تاريخ الإغلاق', 'القيمة التقديرية', 'نسبة النجاح المتوقعة']]
        upcoming_display['أيام متبقية'] = (pd.to_datetime(upcoming_display['تاريخ الإغلاق']) - datetime.now()).dt.days
        upcoming_display['القيمة التقديرية'] = upcoming_display['القيمة التقديرية'].apply(lambda x: f"{x:,.0f} ريال")
        upcoming_display['نسبة النجاح المتوقعة'] = upcoming_display['نسبة النجاح المتوقعة'].apply(lambda x: f"{x}%")
        
        st.dataframe(upcoming_display, hide_index=True, use_container_width=True)
    else:
        st.info("لا توجد مناقصات قادمة خلال الثلاثين يوماً القادمة.")

def procurement_page():
    """صفحة المناقصات والعقود"""
    st.markdown("# 📑 المناقصات والعقود")
    
    tab1, tab2 = st.tabs(["المناقصات", "العقود"])
    
    with tab1:
        st.markdown("## إدارة المناقصات")
        
        # أزرار الإجراءات
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🆕 إضافة مناقصة جديدة"):
                st.session_state.show_add_tender = True
        
        with col2:
            st.button("🔍 بحث متقدم")
        
        with col3:
            st.button("📊 تصدير التقرير")
        
        with col4:
            st.button("🔄 تحديث البيانات")
        
        # عرض جدول المناقصات
        st.markdown("### قائمة المناقصات")
        
        # فلاتر
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect(
                "الحالة:",
                ["الكل"] + list(st.session_state.tenders_df['الحالة'].unique()),
                default=["الكل"]
            )
        
        with col2:
            date_range = st.date_input(
                "تاريخ الإعلان:",
                value=(
                    (datetime.now() - timedelta(days=60)).date(),
                    datetime.now().date()
                )
            )
        
        with col3:
            min_value, max_value = st.slider(
                "القيمة التقديرية (ريال):",
                0, 
                int(st.session_state.tenders_df['القيمة التقديرية'].max()),
                (0, int(st.session_state.tenders_df['القيمة التقديرية'].max())),
                step=100000
            )
        
        # تطبيق الفلاتر
        filtered_df = st.session_state.tenders_df.copy()
        
        # فلتر الحالة
        if "الكل" not in status_filter:
            filtered_df = filtered_df[filtered_df['الحالة'].isin(status_filter)]
        
        # فلتر التاريخ
        filtered_df = filtered_df[
            (pd.to_datetime(filtered_df['تاريخ الإعلان']) >= pd.Timestamp(date_range[0])) &
            (pd.to_datetime(filtered_df['تاريخ الإعلان']) <= pd.Timestamp(date_range[1]))
        ]
        
        # فلتر القيمة
        filtered_df = filtered_df[
            (filtered_df['القيمة التقديرية'] >= min_value) &
            (filtered_df['القيمة التقديرية'] <= max_value)
        ]
        
        # عرض الجدول
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )
        
        # نموذج إضافة مناقصة جديدة
        if 'show_add_tender' in st.session_state and st.session_state.show_add_tender:
            st.markdown("### إضافة مناقصة جديدة")
            with st.form("add_tender_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    tender_id = st.text_input("رقم المناقصة", f"RFP-2024-{len(st.session_state.tenders_df) + 1:03d}")
                    title = st.text_input("عنوان المناقصة", "")
                    start_date = st.date_input("تاريخ الإعلان", datetime.now())
                
                with col2:
                    end_date = st.date_input("تاريخ الإغلاق", datetime.now() + timedelta(days=30))
                    estimated_value = st.number_input("القيمة التقديرية", min_value=0, value=1000000, step=100000)
                    status = st.selectbox("الحالة", ["جديدة", "مفتوحة", "قيد التقييم", "معلقة", "مغلقة", "ملغاة"])
                
                submitted = st.form_submit_button("حفظ المناقصة")
                cancel = st.form_submit_button("إلغاء")
                
                if submitted:
                    st.success("تم إضافة المناقصة بنجاح")
                    st.session_state.show_add_tender = False
                
                if cancel:
                    st.session_state.show_add_tender = False
    
    with tab2:
        st.markdown("## إدارة العقود")
        
        # أزرار الإجراءات
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("🆕 إضافة عقد جديد")
        
        with col2:
            st.button("🔍 بحث متقدم", key="search_contracts")
        
        with col3:
            st.button("📊 تصدير التقرير", key="export_contracts")
        
        with col4:
            st.button("🔄 تحديث البيانات", key="refresh_contracts")
        
        # عرض جدول العقود
        st.markdown("### قائمة العقود")
        
        # فلاتر
        col1, col2 = st.columns(2)
        with col1:
            risk_filter = st.multiselect(
                "مستوى المخاطر:",
                ["الكل"] + list(st.session_state.contracts_df['مستوى المخاطر'].unique()),
                default=["الكل"]
            )
        
        with col2:
            local_content_range = st.slider(
                "نسبة المحتوى المحلي (%):",
                0, 100,
                (0, 100),
                step=10
            )
        
        # تطبيق الفلاتر
        filtered_df = st.session_state.contracts_df.copy()
        
        # فلتر مستوى المخاطر
        if "الكل" not in risk_filter:
            filtered_df = filtered_df[filtered_df['مستوى المخاطر'].isin(risk_filter)]
        
        # فلتر المحتوى المحلي
        filtered_df = filtered_df[
            (filtered_df['المحتوى المحلي'] >= local_content_range[0]) &
            (filtered_df['المحتوى المحلي'] <= local_content_range[1])
        ]
        
        # عرض الجدول
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

def requirements_analysis_page():
    """صفحة تحليل المتطلبات"""
    st.markdown("# 🔍 تحليل المتطلبات")
    
    st.markdown("""
    ## نظام تحليل المتطلبات بالذكاء الاصطناعي
    
    يقوم هذا النظام بتحليل وثائق المتطلبات باستخدام تقنيات معالجة اللغة الطبيعية والذكاء الاصطناعي لاستخراج:
    - المتطلبات الوظيفية وغير الوظيفية
    - التبعيات بين المتطلبات
    - المخاطر المحتملة
    - الشروط والقيود
    - تقدير الجهد والتكلفة
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### تحميل وثائق المتطلبات")
        uploaded_file = st.file_uploader("اختر ملف", type=['pdf', 'docx', 'txt'])
        
        if uploaded_file is not None:
            st.success(f"تم تحميل الملف: {uploaded_file.name}")
            
            if st.button("بدء التحليل"):
                with st.spinner("جاري تحليل المتطلبات..."):
                    time.sleep(3)  # محاكاة وقت المعالجة
                    st.success("تم تحليل المستند بنجاح!")
                    
                    # عرض نتائج التحليل في الجانب الآخر
                    st.session_state.show_analysis_results = True
    
    with col2:
        if 'show_analysis_results' in st.session_state and st.session_state.show_analysis_results:
            st.markdown("### نتائج التحليل")
            
            tab1, tab2, tab3 = st.tabs(["ملخص", "المتطلبات المستخرجة", "المخاطر"])
            
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("إجمالي المتطلبات", "34")
                    st.metric("المتطلبات الوظيفية", "26")
                    st.metric("المتطلبات غير الوظيفية", "8")
                
                with col2:
                    st.metric("تقدير الجهد", "87 يوم عمل")
                    st.metric("التكلفة التقديرية", "435,000 ريال")
st.metric("درجة التعقيد", "متوسطة")
            
            with tab2:
                requirements_demo = pd.DataFrame({
                    "المعرف": [f"REQ-{i:03d}" for i in range(1, 11)],
                    "النوع": ["وظيفي", "وظيفي", "غير وظيفي", "وظيفي", "وظيفي", "غير وظيفي", "وظيفي", "وظيفي", "غير وظيفي", "وظيفي"],
                    "الوصف": [
                        "يجب أن يوفر النظام واجهة لإدارة المستخدمين",
                        "يجب أن يتيح النظام إمكانية إضافة مناقصات جديدة",
                        "يجب أن يدعم النظام اللغة العربية",
                        "يجب أن يوفر النظام تقارير عن حالة المناقصات",
                        "يجب أن يقوم النظام بحساب نسبة المحتوى المحلي",
                        "يجب أن يستجيب النظام في أقل من 3 ثواني",
                        "يجب أن يدعم النظام تحميل المستندات",
                        "يجب أن يوفر النظام واجهة لإدارة العقود",
                        "يجب أن يعمل النظام على متصفحات الويب الحديثة",
                        "يجب أن يوفر النظام نظام تنبيهات للمواعيد النهائية"
                    ],
                    "الأولوية": ["عالية", "عالية", "متوسطة", "عالية", "عالية", "منخفضة", "متوسطة", "عالية", "متوسطة", "متوسطة"],
                    "التعقيد": ["متوسط", "بسيط", "بسيط", "متوسط", "معقد", "بسيط", "متوسط", "معقد", "بسيط", "متوسط"]
                })
                
                st.dataframe(requirements_demo, use_container_width=True, hide_index=True)
            
            with tab3:
                risks_demo = pd.DataFrame({
                    "المعرف": [f"RISK-{i:03d}" for i in range(1, 6)],
                    "الوصف": [
                        "غموض في متطلبات حساب المحتوى المحلي",
                        "تعارض بين متطلبات الأداء والوظائف المطلوبة",
                        "عدم وضوح آلية تكامل النظام مع الأنظمة الخارجية",
                        "تعقيد في متطلبات التقارير",
                        "متطلبات أمنية غير محددة بوضوح"
                    ],
                    "المتطلبات المتأثرة": [
                        "REQ-005", 
                        "REQ-006, REQ-003", 
                        "REQ-010", 
                        "REQ-004", 
                        "REQ-001, REQ-007"
                    ],
                    "الخطورة": ["عالية", "متوسطة", "عالية", "متوسطة", "عالية"],
                    "التوصية": [
                        "طلب توضيح تفصيلي من العميل",
                        "إعادة تحديد أولويات المتطلبات",
                        "عقد ورشة عمل للتكامل",
                        "طلب نماذج للتقارير المطلوبة",
                        "إضافة متطلبات أمنية تفصيلية"
                    ]
                })
                
                st.dataframe(risks_demo, use_container_width=True, hide_index=True)
        else:
            st.markdown("### ملخص المتطلبات")
            st.info("قم بتحميل ملف المتطلبات وبدء التحليل لعرض النتائج هنا")

def supply_chain_page():
    """صفحة تخطيط سلسلة التوريد"""
    st.markdown("# 🔄 تخطيط سلسلة التوريد")
    
    tab1, tab2, tab3 = st.tabs(["تحليل المحتوى المحلي", "إدارة الموردين", "التخطيط للمشتريات"])
    
    with tab1:
        st.markdown("## تحليل وتحسين المحتوى المحلي")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### نسب المحتوى المحلي حسب الفئة")
            
            # الرسم البياني
            fig = go.Figure()
            
            local_df = st.session_state.local_content_df
            
            # إضافة الأعمدة
            fig.add_trace(go.Bar(
                x=local_df['الفئة'],
                y=local_df['النسبة الحالية'],
                name='النسبة الحالية',
                marker_color='#3498db'
            ))
            
            fig.add_trace(go.Bar(
                x=local_df['الفئة'],
                y=local_df['النسبة المستهدفة'],
                name='النسبة المستهدفة',
                marker_color='#2ecc71'
            ))
            
            # تخصيص الرسم البياني
            fig.update_layout(
                barmode='group',
                title_text='مقارنة المحتوى المحلي الحالي والمستهدف',
                title_font_size=16,
                xaxis_title="الفئة",
                yaxis_title="النسبة المئوية (%)",
                legend_title="النسبة",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### فرص تحسين المحتوى المحلي")
            
            for i, row in local_df.iterrows():
                gap = row['النسبة المستهدفة'] - row['النسبة الحالية']
                
                if gap > 5:
                    st.markdown(f"""
                    **تحسين {row['الفئة']}**
                    - الفجوة الحالية: {gap:.1f}%
                    - التغير السنوي: {row['التغير السنوي']}
                    - توصية: زيادة الاعتماد على الموردين المحليين في هذه الفئة
                    """)
            
            st.markdown("### تقدير التأثير الاقتصادي")
            st.metric(
                "القيمة المضافة المحلية المتوقعة", 
                "3.2 مليون ريال",
                "+12.5%"
            )
    
    with tab2:
        st.markdown("## إدارة الموردين")
        
        # أزرار الإجراءات
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("إضافة مورد جديد")
        
        with col2:
            st.button("تصدير قائمة الموردين")
        
        with col3:
            st.button("تقييم الموردين")
        
        # بيانات الموردين التوضيحية
        suppliers_data = {
            "اسم المورد": [
                "شركة التقنية المتطورة", "مؤسسة الحلول الذكية", "شركة الخدمات المتكاملة",
                "مجموعة الإبداع التقني", "شركة التطوير الرقمي", "مؤسسة الجودة الشاملة",
                "شركة الاتصالات المتقدمة", "مؤسسة البناء الحديث"
            ],
            "التصنيف": [
                "محلي", "محلي", "أجنبي",
                "محلي", "محلي مشترك", "محلي",
                "أجنبي", "محلي"
            ],
            "المنتجات/الخدمات": [
                "أنظمة تقنية", "خدمات استشارية", "معدات وأجهزة",
                "برمجيات", "حلول تقنية", "خدمات صيانة",
                "أنظمة اتصالات", "إنشاءات"
            ],
            "درجة التقييم": [
                "A", "A", "B",
                "B", "A", "C",
                "B", "A"
            ],
            "المحتوى المحلي": [
                "87%", "92%", "34%",
                "79%", "63%", "95%",
                "28%", "91%"
            ],
            "تاريخ آخر تعامل": [
                "2024-01-15", "2024-02-20", "2023-11-05",
                "2024-03-10", "2024-02-25", "2023-09-18",
                "2024-01-30", "2024-03-05"
            ]
        }
        
        suppliers_df = pd.DataFrame(suppliers_data)
        
        # تصفية البيانات
        local_filter = st.multiselect(
            "التصنيف:",
            ["الكل"] + list(suppliers_df['التصنيف'].unique()),
            default=["الكل"]
        )
        
        filtered_suppliers = suppliers_df.copy()
        if "الكل" not in local_filter:
            filtered_suppliers = filtered_suppliers[filtered_suppliers['التصنيف'].isin(local_filter)]
        
        # عرض الجدول
        st.dataframe(filtered_suppliers, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("## التخطيط للمشتريات")
        
        st.markdown("""
        ### التخطيط الاستراتيجي للمشتريات
        
        استخدم هذا القسم لتخطيط المشتريات المستقبلية وتحليل الاحتياجات وفرص توفير التكاليف.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### توزيع المشتريات حسب الفئة")
            
            categories = ["أجهزة ومعدات", "خدمات استشارية", "برمجيات", "خدمات صيانة", "مستلزمات مكتبية"]
            values = [45, 25, 15, 10, 5]
            
            fig = px.pie(
                names=categories,
                values=values,
                title="توزيع المشتريات حسب الفئة",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            fig.update_layout(
                title_font_size=16,
                legend_title=""
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### التكاليف الشهرية المتوقعة")
            
            # بيانات مالية توضيحية
            financial_df = st.session_state.financial_df
            
            # تحويل البيانات المالية إلى صيغة مناسبة للرسم البياني
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=financial_df['الشهر'],
                y=financial_df['المخطط'],
                name='المخطط',
                line=dict(color='#3498db', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=financial_df['الشهر'],
                y=financial_df['الفعلي'],
                name='الفعلي',
                line=dict(color='#e74c3c', width=2)
            ))
            
            fig.update_layout(
                title_text='مقارنة التكاليف المخططة والفعلية',
                title_font_size=16,
                xaxis_title="الشهر",
                yaxis_title="التكلفة (ريال)",
                legend_title="النوع",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

def risk_analysis_page():
    """صفحة تحليل المخاطر"""
    st.markdown("# ⚠️ تحليل المخاطر")
    
    st.markdown("""
    ## نظام تحليل وإدارة المخاطر
    
    يقوم هذا النظام بتحديد وتقييم وإدارة المخاطر المرتبطة بالمناقصات والعقود. 
    يمكنك من خلاله تحليل المخاطر المختلفة وتحديد استراتيجيات الاستجابة المناسبة.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### تصنيف المخاطر")
        
        risk_options = [
            "مخاطر قانونية",
            "مخاطر مالية",
            "مخاطر تشغيلية",
            "مخاطر فنية",
            "مخاطر تعاقدية",
            "مخاطر خارجية"
        ]
        
        selected_risk = st.radio("اختر نوع المخاطر:", risk_options)
        
        st.markdown("### تحليل ذكي")
        if st.button("تحليل المخاطر بالذكاء الاصطناعي"):
            with st.spinner("جاري التحليل..."):
                time.sleep(2)
                st.success("تم التحليل بنجاح!")
                
                ai_results = {
                    "مخاطر قانونية": """
                    - احتمالية عالية لتغير اللوائح التنظيمية خلال فترة المشروع
                    - مخاطر متوسطة لوجود ثغرات في صياغة العقد
                    - مخاطر منخفضة لنزاعات قضائية
                    """,
                    "مخاطر مالية": """
                    - مخاطر عالية لتقلبات أسعار المواد الخام
                    - مخاطر متوسطة لتغير أسعار الصرف
                    - مخاطر عالية للتأخر في السداد
                    """,
                    "مخاطر تشغيلية": """
                    - مخاطر متوسطة لتأخر جدول المشروع
                    - مخاطر عالية لنقص الكوادر المؤهلة
                    - مخاطر منخفضة للأعطال التقنية
                    """,
                    "مخاطر فنية": """
                    - مخاطر عالية لعدم وضوح المتطلبات الفنية
                    - مخاطر متوسطة لتعارض تقني مع أنظمة قائمة
                    - مخاطر منخفضة لأداء النظام
                    """,
                    "مخاطر تعاقدية": """
                    - مخاطر عالية لغموض نطاق العمل
                    - مخاطر متوسطة لتغيير متطلبات العميل
                    - مخاطر متوسطة لمعايير القبول
                    """,
                    "مخاطر خارجية": """
                    - مخاطر منخفضة للعوامل البيئية
                    - مخاطر متوسطة للعوامل السياسية
                    - مخاطر منخفضة للكوارث الطبيعية
                    """
                }
                
                st.info(ai_results[selected_risk])
    
    with col2:
        st.markdown("### سجل المخاطر")
        
        # عرض جدول المخاطر
        st.dataframe(
            st.session_state.risks_df,
            use_container_width=True,
            hide_index=True
        )
        
        # مصفوفة المخاطر
        st.markdown("### مصفوفة المخاطر")
        
        risk_matrix = pd.crosstab(
            st.session_state.risks_df['التأثير'], 
            st.session_state.risks_df['الاحتمالية'],
            margins=False
        )
        
        # تحويل القيم إلى حرارية
        risk_severity = {
            ('منخفض', 'منخفضة'): 1,
            ('منخفض', 'متوسطة'): 2,
            ('منخفض', 'عالية'): 3,
            ('متوسط', 'منخفضة'): 2,
            ('متوسط', 'متوسطة'): 4,
            ('متوسط', 'عالية'): 6,
            ('عالي', 'منخفضة'): 3,
            ('عالي', 'متوسطة'): 6,
            ('عالي', 'عالية'): 9,
            ('حرج', 'منخفضة'): 4,
            ('حرج', 'متوسطة'): 8,
            ('حرج', 'عالية'): 12
        }
        
        # تحضير بيانات المصفوفة
        impact_order = ['منخفض', 'متوسط', 'عالي', 'حرج']
        probability_order = ['منخفضة', 'متوسطة', 'عالية']
        
        # إنشاء مصفوفة حرارية
        heat_values = []
        annotations = []
        
        for impact in impact_order:
            heat_row = []
            for prob in probability_order:
                try:
                    value = risk_matrix.loc[impact, prob]
                except:
                    value = 0
                heat_row.append(risk_severity.get((impact, prob), 0))
                annotations.append(dict(
                    text=str(value),
                    x=prob,
                    y=impact,
                    showarrow=False
                ))
            heat_values.append(heat_row)
        
        # إنشاء الرسم البياني
        fig = go.Figure(data=go.Heatmap(
            z=heat_values,
            x=probability_order,
            y=impact_order,
            colorscale=[
                [0.0, "#2ecc71"],  # أخضر للمخاطر المنخفضة
                [0.33, "#f1c40f"],  # أصفر للمخاطر المتوسطة
                [0.66, "#e67e22"],  # برتقالي للمخاطر العالية
                [1.0, "#e74c3c"]    # أحمر للمخاطر الحرجة
            ],
            showscale=False
        ))
        
        # إضافة النصوص
        for annotation in annotations:
            fig.add_annotation(annotation)
        
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="الاحتمالية",
            yaxis_title="التأثير"
        )
        
        st.plotly_chart(fig, use_container_width=True)

def local_content_page():
    """صفحة المحتوى المحلي"""
    st.markdown("# 🏠 المحتوى المحلي")
    
    st.markdown("""
    ## قياس وتحسين المحتوى المحلي
    
    يتيح النظام إمكانية قياس نسبة المحتوى المحلي في المشاريع والمناقصات وتحديد فرص التحسين.
    """)
    
    tab1, tab2 = st.tabs(["تحليل المحتوى المحلي", "فرص التحسين"])
    
    with tab1:
        # تحليل المحتوى المحلي حسب الفئة
        local_df = st.session_state.local_content_df
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=local_df['الفئة'],
                y=local_df['النسبة الحالية'],
                name='النسبة الحالية',
                marker_color='#3498db'
            ))
            
            fig.add_trace(go.Bar(
                x=local_df['الفئة'],
                y=local_df['النسبة المستهدفة'],
                name='النسبة المستهدفة',
                marker_color='#2ecc71'
            ))
            
            fig.update_layout(
                barmode='group',
                title_text='تحليل المحتوى المحلي حسب الفئة',
                title_font_size=20,
                title_x=0.5,
                xaxis_title="الفئة",
                yaxis_title="النسبة المئوية (%)",
                legend_title="النسبة"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            total_current = local_df['النسبة الحالية'].mean()
            total_target = local_df['النسبة المستهدفة'].mean()
            gap = total_target - total_current
            
            st.markdown("### المحتوى المحلي الإجمالي")
            st.metric(
                "النسبة الحالية",
                f"{total_current:.1f}%",
                delta=None
            )
            
            st.metric(
                "النسبة المستهدفة",
                f"{total_target:.1f}%",
                delta=None
            )
            
            st.metric(
                "الفجوة",
                f"{gap:.1f}%",
                delta=None
            )
        
        # تحليل المحتوى المحلي حسب العقود
        st.markdown("### تحليل المحتوى المحلي في العقود")
        
        sorted_contracts = st.session_state.contracts_df.sort_values('المحتوى المحلي', ascending=False)
        
        fig = px.bar(
            sorted_contracts.head(10),
            x='رقم العقد',
            y='المحتوى المحلي',
            color='المحتوى المحلي',
            color_continuous_scale=px.colors.sequential.Viridis,
            title="أعلى 10 عقود من حيث المحتوى المحلي"
        )
        
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="رقم العقد",
            yaxis_title="نسبة المحتوى المحلي (%)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### فرص تحسين المحتوى المحلي")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### مجالات التحسين
            
            1. **توظيف الكوادر المحلية**
               - توظيف مهندسين محليين
               - التعاقد مع خبراء محليين للاستشارات
               - برامج تدريب للكوادر المحلية
            
            2. **شراء المواد والمعدات المحلية**
               - تفضيل الموردين المحليين
               - دعم المصنعين المحليين
               - تطوير سلاسل التوريد المحلية
            
            3. **نقل التقنية**
               - توطين التقنيات الحديثة
               - تطوير الخبرات المحلية
               - الشراكة مع الجامعات المحلية
            """)
        
        with col2:
            st.markdown("### أكبر الفجوات في المحتوى المحلي")
            
            # البيانات
            categories = []
            gaps = []
            
            for i, row in local_df.iterrows():
                gap = row['النسبة المستهدفة'] - row['النسبة الحالية']
                categories.append(row['الفئة'])
                gaps.append(gap)
            
            # ترتيب البيانات
            gap_df = pd.DataFrame({
                'الفئة': categories,
                'الفجوة': gaps
            })
            
            sorted_gap_df = gap_df.sort_values('الفجوة', ascending=False)
            
            fig = px.bar(
                sorted_gap_df,
                x='الفئة',
                y='الفجوة',
                color='الفجوة',
                color_continuous_scale=px.colors.sequential.Reds,
                title="الفجوات في المحتوى المحلي حسب الفئة"
            )
            
            fig.update_layout(
                title_font_size=16,
                title_x=0.5,
                xaxis_title="الفئة",
                yaxis_title="الفجوة (%)"
            )
            
            st.plotly_chart(fig, use_container_width=True)

def success_prediction_page():
    """صفحة توقع احتمالية النجاح"""
    st.markdown("# 🎯 توقع احتمالية النجاح")
    
    st.markdown("""
    ## نظام التنبؤ بنجاح المناقصات
    
    يستخدم هذا النظام خوارزميات الذكاء الاصطناعي لتحليل عوامل نجاح المناقصات وتوقع احتمالية الفوز بها.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### تحليل مناقصة جديدة")
        
        with st.form("prediction_form"):
            tender_type = st.selectbox(
                "نوع المناقصة:",
                ["مناقصة عامة", "مناقصة محدودة", "منافسة محدودة", "شراء مباشر"]
            )
            
            tender_sector = st.selectbox(
                "القطاع:",
                ["حكومي", "شبه حكومي", "خاص"]
            )
            
            tender_value = st.number_input(
                "القيمة التقديرية (ريال):",
                min_value=100000,
                max_value=100000000,
                value=1000000,
                step=100000
            )
            
            competitors_count = st.slider(
                "عدد المنافسين المتوقع:",
                min_value=1,
                max_value=20,
                value=5
            )
            
            technical_weight = st.slider(
                "وزن التقييم الفني (%):",
                min_value=0,
                max_value=100,
                value=60
            )
            
            previous_experience = st.checkbox("خبرة سابقة مع نفس الجهة")
            
            local_content_value = st.slider(
                "نسبة المحتوى المحلي المقدمة (%):",
                min_value=0,
                max_value=100,
                value=65
            )
            
            submit_button = st.form_submit_button("توقع احتمالية النجاح")
        
        if submit_button:
            with st.spinner("جاري تحليل المناقصة..."):
                time.sleep(2)  # محاكاة وقت المعالجة
                
                # حساب احتمالية النجاح (محاكاة)
                base_probability = 70  # احتمالية أساسية
                
                # العوامل المؤثرة
                factors = {}
                
# نوع المناقصة
                if tender_type == "مناقصة عامة":
                    factors["نوع المناقصة"] = -5  # منافسة أكبر
                elif tender_type == "مناقصة محدودة":
                    factors["نوع المناقصة"] = 5
                elif tender_type == "منافسة محدودة":
                    factors["نوع المناقصة"] = 10
                else:  # شراء مباشر
                    factors["نوع المناقصة"] = 15
                
                # القطاع
                if tender_sector == "حكومي":
                    factors["القطاع"] = 0
                elif tender_sector == "شبه حكومي":
                    factors["القطاع"] = 5
                else:  # خاص
                    factors["القطاع"] = -5
                
                # القيمة التقديرية
                if tender_value < 500000:
                    factors["القيمة"] = 5
                elif tender_value < 2000000:
                    factors["القيمة"] = 0
                elif tender_value < 10000000:
                    factors["القيمة"] = -5
                else:
                    factors["القيمة"] = -10
                
                # عدد المنافسين
                if competitors_count <= 3:
                    factors["المنافسين"] = 10
                elif competitors_count <= 7:
                    factors["المنافسين"] = 0
                else:
                    factors["المنافسين"] = -10
                
                # وزن التقييم الفني
                if technical_weight >= 70:
                    factors["التقييم الفني"] = 10
                elif technical_weight >= 50:
                    factors["التقييم الفني"] = 5
                else:
                    factors["التقييم الفني"] = 0
                
                # خبرة سابقة
                if previous_experience:
                    factors["خبرة سابقة"] = 15
                else:
                    factors["خبرة سابقة"] = 0
                
                # المحتوى المحلي
                if local_content_value >= 80:
                    factors["المحتوى المحلي"] = 10
                elif local_content_value >= 60:
                    factors["المحتوى المحلي"] = 5
                elif local_content_value >= 40:
                    factors["المحتوى المحلي"] = 0
                else:
                    factors["المحتوى المحلي"] = -5
                
                # حساب الاحتمالية النهائية
                final_probability = base_probability + sum(factors.values())
                
                # تعديل النتيجة ضمن النطاق المقبول
                final_probability = max(min(final_probability, 99), 1)
                
                # عرض النتيجة
                st.success(f"احتمالية النجاح في المناقصة: {final_probability}%")
                
                # عرض تفاصيل التحليل
                st.markdown("### تفاصيل التحليل")
                
                for factor, value in factors.items():
                    icon = "🔼" if value > 0 else "🔽" if value < 0 else "◀▶"
                    st.text(f"{icon} {factor}: {value:+d}%")
    
    with col2:
        st.markdown("### العوامل المؤثرة في نجاح المناقصات")
        
        # بيانات توضيحية للعوامل المؤثرة
        factors_df = pd.DataFrame({
            "العامل": [
                "المحتوى المحلي",
                "السعر التنافسي",
                "الخبرة السابقة",
                "الحلول التقنية",
                "القدرات الفنية",
                "سرعة التنفيذ",
                "جودة المقترح الفني",
                "الامتثال للمتطلبات"
            ],
            "تأثير إيجابي": [
                0.85, 0.78, 0.72, 0.65, 0.62, 0.58, 0.52, 0.48
            ]
        })
        
        fig = px.bar(
            factors_df,
            x="تأثير إيجابي",
            y="العامل",
            orientation='h',
            color="تأثير إيجابي",
            color_continuous_scale=px.colors.sequential.Viridis,
            title="تأثير العوامل المختلفة على احتمالية النجاح"
        )
        
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            xaxis_title="مستوى التأثير الإيجابي",
            yaxis_title=""
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### إحصائيات المناقصات السابقة")
        
        # بيانات توضيحية للمناقصات السابقة
        historical_df = pd.DataFrame({
            "الشهر": [
                "يناير", "فبراير", "مارس", "أبريل", "مايو", 
                "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر"
            ],
            "عدد المناقصات": [5, 7, 4, 6, 9, 8, 6, 7, 10, 8],
            "معدل النجاح": [0.6, 0.57, 0.75, 0.67, 0.44, 0.5, 0.67, 0.71, 0.6, 0.75]
        })
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(
                x=historical_df["الشهر"],
                y=historical_df["عدد المناقصات"],
                name="عدد المناقصات",
                marker_color="#3498db"
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=historical_df["الشهر"],
                y=historical_df["معدل النجاح"],
                name="معدل النجاح",
                mode="lines+markers",
                marker_color="#e74c3c",
                line=dict(width=3)
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            title_text="إحصائيات المناقصات السابقة",
            title_font_size=16,
            title_x=0.5,
            legend_title="",
            xaxis_title="الشهر"
        )
        
        fig.update_yaxes(title_text="عدد المناقصات", secondary_y=False)
        fig.update_yaxes(title_text="معدل النجاح", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)

def settings_page():
    """صفحة الإعدادات"""
    st.markdown("# ⚙️ الإعدادات")
    
    st.markdown("""
    ## إعدادات النظام
    
    يمكنك من خلال هذه الصفحة تخصيص إعدادات النظام بما يتناسب مع احتياجاتك.
    """)
    
    tab1, tab2, tab3 = st.tabs(["إعدادات عامة", "إعدادات الحساب", "الدعم والمساعدة"])
    
    with tab1:
        st.markdown("### الإعدادات العامة")
        
        st.markdown("#### إعدادات اللغة")
        lang = st.radio(
            "اللغة الافتراضية للنظام:",
            ["العربية", "English"],
            index=0
        )
        
        st.markdown("#### إعدادات العرض")
        theme = st.selectbox(
            "السمة:",
            ["السمة الافتراضية", "الوضع الداكن", "الوضع الفاتح"],
            index=0
        )
        
        st.markdown("#### إعدادات الإشعارات")
        st.checkbox("تفعيل الإشعارات داخل النظام", value=True)
        st.checkbox("تفعيل الإشعارات عبر البريد الإلكتروني", value=True)
        
        if st.button("حفظ الإعدادات العامة"):
            st.success("تم حفظ الإعدادات بنجاح")
    
    with tab2:
        st.markdown("### إعدادات الحساب")
        
        st.markdown("#### البيانات الشخصية")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("الاسم:", value="محمد أحمد")
            st.text_input("البريد الإلكتروني:", value="mohammed@example.com")
        
        with col2:
            st.text_input("المسمى الوظيفي:", value="مدير مشاريع")
            st.text_input("رقم الهاتف:", value="0555555555")
        
        st.markdown("#### تغيير كلمة المرور")
        st.password_input("كلمة المرور الحالية:")
        st.password_input("كلمة المرور الجديدة:")
        st.password_input("تأكيد كلمة المرور الجديدة:")
        
        if st.button("تحديث البيانات"):
            st.success("تم تحديث البيانات بنجاح")
        
        st.markdown("#### إعدادات الأمان")
        st.checkbox("تفعيل المصادقة الثنائية", value=False)
    
    with tab3:
        st.markdown("### الدعم والمساعدة")
        
        st.markdown("""
        #### كيفية استخدام النظام
        
        يوفر النظام مجموعة من الأدوات والتحليلات التي تساعدك في إدارة المناقصات والعقود وتحليل المخاطر.
        يمكنك الاطلاع على دليل الاستخدام للحصول على شرح تفصيلي لكافة الوظائف.
        """)
        
        st.download_button(
            "تحميل دليل الاستخدام",
            data="محتوى دليل الاستخدام",
            file_name="user_guide.pdf",
            mime="application/pdf"
        )
        
        st.markdown("#### التواصل مع الدعم الفني")
        
        with st.form("support_form"):
            st.text_input("العنوان:")
            st.text_area("الرسالة:")
            st.selectbox(
                "نوع المشكلة:",
                ["استفسار عام", "مشكلة فنية", "اقتراح تحسين", "أخرى"]
            )
            st.file_uploader("إرفاق ملف (اختياري):")
            
            submit_support = st.form_submit_button("إرسال")
        
        if submit_support:
            st.success("تم إرسال رسالتك بنجاح، سيتم التواصل معك قريباً")

def about_page():
    """صفحة حول النظام"""
    st.markdown("# ℹ️ حول النظام")
    
    st.markdown("""
    ## نظام إدارة المناقصات والعقود
    
    ### نبذة عن النظام
    
    نظام متكامل لإدارة المناقصات والعقود يعتمد على أحدث التقنيات والذكاء الاصطناعي لتحسين كفاءة العمليات وزيادة فرص النجاح.
    يوفر النظام مجموعة من الأدوات والتحليلات التي تساعد في اتخاذ القرارات وإدارة المخاطر وتحسين المحتوى المحلي.
    
    ### المميزات الرئيسية
    
    * إدارة المناقصات والفرص التجارية
    * تحليل وإدارة المخاطر
    * قياس وتحسين المحتوى المحلي
    * توقع احتمالية النجاح في المناقصات
    * إدارة وتحليل العقود
    * تخطيط سلسلة التوريد
    * تحليل المتطلبات
    
    ### فريق التطوير
    
    تم تطوير هذا النظام بواسطة فريق من الخبراء المتخصصين في مجالات البرمجة والذكاء الاصطناعي وإدارة المشاريع والعقود.
    
    ### التواصل
    
    للمزيد من المعلومات أو الاستفسارات، يرجى التواصل عبر:
    
    * البريد الإلكتروني: info@tenderssystem.com
    * رقم الهاتف: 0123456789
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("إصدار النظام: 1.0.0")
    
    with col2:
        st.info("تاريخ الإطلاق: 2024/03/15")
    
    with col3:
        st.info("آخر تحديث: 2024/03/18")

# تكوين القائمة الجانبية
def setup_sidebar():
    """إعداد القائمة الجانبية"""
    with st.sidebar:
        st.image("logo.png", width=150)
        st.title("نظام إدارة المناقصات")
        
        # معلومات المستخدم
        st.markdown("### أهلاً م تامر الجوهري ")
        st.markdown("مدير المناقصات والعقود")
        
        st.markdown("---")
        
        # القائمة الرئيسية
        page = st.radio(
            "القائمة الرئيسية",
            [
                "📊 الرئيسية", 
                "📋 المناقصات",
                "📑 العقود",
                "🔍 تحليل المتطلبات",
                "🔄 تخطيط سلسلة التوريد",
                "⚠️ تحليل المخاطر",
                "🏠 المحتوى المحلي",
                "🎯 توقع احتمالية النجاح",
                "⚙️ الإعدادات",
                "ℹ️ حول النظام"
            ]
        )
        
        st.markdown("---")
        
        # الإحصائيات
        st.markdown("### إحصائيات سريعة")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("المناقصات", "28")
        with col2:
            st.metric("العقود", "14")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("قيد الدراسة", "7")
        with col2:
            st.metric("معدل النجاح", "64%")
    
    return page

# الدالة الرئيسية للتطبيق
def main():
    """الدالة الرئيسية للتطبيق"""
    # إعداد الصفحة
    st.set_page_config(
        page_title="نظام إدارة المناقصات والعقود",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # التأكد من وجود بيانات الجلسة
    initialize_session_state()
    
    # إعداد القائمة الجانبية
    page = setup_sidebar()
    
    # عرض الصفحة المناسبة
    if page == "📊 الرئيسية":
        home_page()
    elif page == "📋 المناقصات":
        tenders_page()
    elif page == "📑 العقود":
        contracts_page()
    elif page == "🔍 تحليل المتطلبات":
        requirements_page()
    elif page == "🔄 تخطيط سلسلة التوريد":
        supply_chain_page()
    elif page == "⚠️ تحليل المخاطر":
        risk_analysis_page()
    elif page == "🏠 المحتوى المحلي":
        local_content_page()
    elif page == "🎯 توقع احتمالية النجاح":
        success_prediction_page()
    elif page == "⚙️ الإعدادات":
        settings_page()
    elif page == "ℹ️ حول النظام":
        about_page()

if __name__ == "__main__":
    main()