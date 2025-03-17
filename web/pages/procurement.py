import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

# ✅ تأكد أن `set_page_config` هو أول أمر بعد الاستيراد
st.set_page_config(
    page_title="تحليل المناقصات والعقود",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# إضافة المسار الرئيسي للمشروع إلى PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# استيراد الوحدات الخاصة بالمشروع
from modules.document_processor import DocumentProcessor
from modules.requirement_analyzer import RequirementAnalyzer
from modules.cost_risk_analyzer import CostRiskAnalyzer
from modules.schedule_analyzer import ScheduleAnalyzer
from modules.local_content import LocalContentCalculator
from modules.supply_chain import SupplyChainAnalyzer
from modules.ai_models import LLMProcessor, ArabicBERTModel
from utils.database import VectorDBConnector, TemplateLoader
from utils.api_integrations import MunafasatAPI, EtimadAPI, BaladyAPI


# تكوين الصفحة
st.set_page_config(
    page_title="تحليل المناقصات والعقود",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تحديد النمط والتصميم
st.markdown("""
<style>
    .main {
        direction: rtl;
        text-align: right;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F0F2F6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .css-12oz5g7 {
        flex-direction: row-reverse;
    }
    .css-1v3fvcr {
        direction: rtl;
    }
    .stMarkdown {
        direction: rtl;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------
# الدوال المساعدة
# ------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_tender_templates():
    """تحميل قوالب المناقصات من قاعدة البيانات"""
    template_loader = TemplateLoader()
    return template_loader.load_tender_templates()

@st.cache_data(ttl=3600)
def load_supplier_database():
    """تحميل قاعدة بيانات الموردين"""
    try:
        supply_chain = SupplyChainAnalyzer()
        return supply_chain.get_suppliers_database()
    except Exception as e:
        st.error(f"خطأ في تحميل قاعدة بيانات الموردين: {e}")
        return pd.DataFrame()

def process_uploaded_documents(uploaded_files):
    """معالجة المستندات المرفوعة"""
    if not uploaded_files:
        return None, None
    
    document_processor = DocumentProcessor()
    
    extracted_data = {}
    file_contents = {}
    
    for file in uploaded_files:
        try:
            file_content = file.read()
            file_extension = file.name.split(".")[-1].lower()
            
            file_contents[file.name] = file_content
            processed_data = document_processor.process_document(
                file_content, 
                file_extension, 
                file.name
            )
            
            extracted_data[file.name] = processed_data
            
        except Exception as e:
            st.error(f"خطأ في معالجة الملف {file.name}: {e}")
    
    return extracted_data, file_contents

def analyze_requirements(extracted_data):
    """تحليل متطلبات المناقصة"""
    if not extracted_data:
        return None
    
    requirement_analyzer = RequirementAnalyzer()
    
    analyzed_results = {}
    for file_name, data in extracted_data.items():
        analyzed_results[file_name] = requirement_analyzer.analyze(data)
    
    return analyzed_results

def analyze_local_content(extracted_data, project_data):
    """تحليل المحتوى المحلي للمناقصة"""
    if not extracted_data or not project_data:
        return None
    
    local_content_calculator = LocalContentCalculator()
    
    # استخراج بيانات المشروع ذات الصلة
    project_type = project_data.get("project_type", "")
    budget = project_data.get("budget", 0)
    location = project_data.get("location", "")
    duration = project_data.get("duration", 0)
    
    # تحليل المحتوى المحلي
    local_content_results = local_content_calculator.calculate(
        extracted_data, 
        project_type=project_type,
        budget=budget,
        location=location,
        duration=duration
    )
    
    return local_content_results

# ------------------------------------------------------------------------
# واجهة المستخدم الرئيسية
# ------------------------------------------------------------------------
def main():
    st.title("نظام تحليل المناقصات والعقود")
    
    # الشريط الجانبي
    with st.sidebar:
        st.header("الإعدادات والخيارات")
        
        st.subheader("رفع المستندات")
        uploaded_files = st.file_uploader(
            "رفع وثائق المناقصة، العقد، أو الملفات ذات الصلة",
            accept_multiple_files=True,
            type=["pdf", "docx", "xlsx", "csv", "txt"]
        )
        
        st.subheader("ضبط التحليل")
        analysis_mode = st.radio(
            "اختر نمط التحليل:",
            ["سريع", "متوسط", "متقدم"]
        )
        
        use_ai = st.checkbox("استخدام الذكاء الاصطناعي للتحليل المتقدم", value=True)
        
        # إعدادات متقدمة
        with st.expander("إعدادات متقدمة"):
            ai_model = st.selectbox(
                "نموذج الذكاء الاصطناعي",
                ["Claude (Anthropic)", "AraGPT", "BERT عربي مخصص"]
            )
            
            similarity_threshold = st.slider(
                "عتبة التشابه للتوصيات",
                min_value=0.5,
                max_value=0.95,
                value=0.75,
                step=0.05
            )
            
            supply_chain_depth = st.slider(
                "عمق تحليل سلسلة الإمداد",
                min_value=1,
                max_value=5,
                value=2,
                step=1
            )
        
        # زر تحليل
        analysis_btn = st.button("بدء التحليل", type="primary")
    
    # الأقسام الرئيسية للتطبيق
    tabs = st.tabs([
        "نظرة عامة",
        "تحليل المتطلبات",
        "تحليل التكاليف والمخاطر",
        "المحتوى المحلي",
        "سلسلة الإمداد",
        "الجدول الزمني",
        "التوصيات والملخص"
    ])
    
    # حالة التطبيق
    if "project_data" not in st.session_state:
        st.session_state.project_data = {
            "project_title": "",
            "project_type": "",
            "project_number": "",
            "budget": 0,
            "location": "",
            "duration": 0,
            "start_date": None,
            "end_date": None
        }
    
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    
    if "extracted_data" not in st.session_state:
        st.session_state.extracted_data = None
    
    # نظرة عامة - القسم الأول
    with tabs[0]:
        st.header("معلومات المشروع / المناقصة")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.project_data["project_title"] = st.text_input(
                "عنوان المشروع / المناقصة",
                value=st.session_state.project_data.get("project_title", "")
            )
            
            st.session_state.project_data["project_type"] = st.selectbox(
                "نوع المشروع",
                [
                    "", "إنشاءات", "تقنية معلومات", "استشارات", 
                    "توريد معدات", "خدمات", "أخرى"
                ],
                index=0
            )
            
            st.session_state.project_data["project_number"] = st.text_input(
                "رقم المشروع / المناقصة",
                value=st.session_state.project_data.get("project_number", "")
            )
            
            st.session_state.project_data["budget"] = st.number_input(
                "الميزانية التقديرية (ريال سعودي)",
                min_value=0,
                value=int(st.session_state.project_data.get("budget", 0))
            )
        
        with col2:
            st.session_state.project_data["location"] = st.text_input(
                "الموقع",
                value=st.session_state.project_data.get("location", "")
            )
            
            st.session_state.project_data["duration"] = st.number_input(
                "المدة (بالأشهر)",
                min_value=0,
                value=int(st.session_state.project_data.get("duration", 0))
            )
            
            start_date = st.date_input(
                "تاريخ البدء المتوقع",
                value=st.session_state.project_data.get("start_date", datetime.now().date())
            )
            st.session_state.project_data["start_date"] = start_date
            
            end_date = st.date_input(
                "تاريخ الانتهاء المتوقع",
                value=st.session_state.project_data.get("end_date", None)
            )
            st.session_state.project_data["end_date"] = end_date
        
        # عرض المستندات المرفوعة
        if uploaded_files:
            st.subheader("المستندات المرفوعة")
            file_list = ", ".join([file.name for file in uploaded_files])
            st.info(f"تم رفع {len(uploaded_files)} ملفات: {file_list}")
    
    # تحليل المتطلبات - القسم الثاني
    with tabs[1]:
        st.header("تحليل المتطلبات")
        
        if st.session_state.extracted_data is not None:
            # عرض المتطلبات المستخرجة
            st.subheader("المتطلبات الرئيسية")
            
            # هنا سنفترض أن البيانات المستخرجة تحتوي على مفتاح 'requirements'
            requirements_found = False
            
            for file_name, data in st.session_state.extracted_data.items():
                if 'requirements' in data:
                    requirements_found = True
                    st.write(f"المتطلبات من الملف: {file_name}")
                    
                    for i, req in enumerate(data['requirements']):
                        with st.expander(f"المتطلب {i+1}: {req.get('title', 'متطلب')}"):
                            st.write(f"**الوصف:** {req.get('description', 'لا يوجد وصف')}")
                            st.write(f"**الأهمية:** {req.get('importance', 'عادية')}")
                            st.write(f"**الفئة:** {req.get('category', 'عامة')}")
                            
                            if 'compliance' in req:
                                st.write(f"**الامتثال:** {req['compliance']}")
            
            if not requirements_found:
                st.info("لم يتم استخراج متطلبات محددة من المستندات. يرجى رفع وثائق المناقصة أو العقد.")
        else:
            st.info("يرجى رفع المستندات وبدء التحليل لعرض المتطلبات.")
    
    # تحليل التكاليف والمخاطر - القسم الثالث
    with tabs[2]:
        st.header("تحليل التكاليف والمخاطر")
        
        if st.session_state.analysis_results is not None:
            cost_tab, risk_tab = st.tabs(["تحليل التكاليف", "تحليل المخاطر"])
            
            with cost_tab:
                st.subheader("هيكل التكاليف")
                # هنا يمكن إضافة رسوم بيانية وتحليلات للتكاليف
                
                # مثال لرسم بياني افتراضي
                if 'cost_breakdown' in st.session_state.analysis_results:
                    cost_data = st.session_state.analysis_results['cost_breakdown']
                    fig = px.pie(
                        values=list(cost_data.values()),
                        names=list(cost_data.keys()),
                        title="توزيع التكاليف"
                    )
                    st.plotly_chart(fig)
                else:
                    st.write("لم يتم العثور على بيانات التكاليف")
            
            with risk_tab:
                st.subheader("تقييم المخاطر")
                # هنا يمكن إضافة تحليل المخاطر
                
                # مثال لعرض جدول المخاطر
                if 'risks' in st.session_state.analysis_results:
                    risks_df = pd.DataFrame(st.session_state.analysis_results['risks'])
                    st.dataframe(risks_df)
                else:
                    st.write("لم يتم العثور على بيانات المخاطر")
        else:
            st.info("يرجى رفع المستندات وبدء التحليل لعرض تحليل التكاليف والمخاطر.")
    
    # المحتوى المحلي - القسم الرابع
    with tabs[3]:
        st.header("تحليل المحتوى المحلي")
        
        if st.session_state.analysis_results is not None and 'local_content' in st.session_state.analysis_results:
            local_content = st.session_state.analysis_results['local_content']
            
            # عرض النسبة الإجمالية للمحتوى المحلي
            if 'overall_percentage' in local_content:
                st.metric(
                    label="نسبة المحتوى المحلي الإجمالية",
                    value=f"{local_content['overall_percentage']:.2f}%"
                )
            
            # عرض تفاصيل المحتوى المحلي
            if 'breakdown' in local_content:
                st.subheader("تفاصيل المحتوى المحلي")
                
                breakdown = local_content['breakdown']
                fig = px.bar(
                    x=list(breakdown.keys()),
                    y=list(breakdown.values()),
                    title="تحليل المحتوى المحلي حسب الفئة"
                )
                fig.update_layout(
                    xaxis_title="الفئة",
                    yaxis_title="النسبة المئوية"
                )
                st.plotly_chart(fig)
            
            # توصيات لتحسين نسبة المحتوى المحلي
            if 'recommendations' in local_content:
                st.subheader("توصيات لتحسين المحتوى المحلي")
                
                for i, rec in enumerate(local_content['recommendations']):
                    st.write(f"{i+1}. {rec}")
        else:
            st.info("يرجى رفع المستندات وبدء التحليل لعرض تحليل المحتوى المحلي.")
    
    # سلسلة الإمداد - القسم الخامس
    with tabs[4]:
        st.header("تحليل سلسلة الإمداد")
        
        if st.session_state.analysis_results is not None and 'supply_chain' in st.session_state.analysis_results:
            supply_chain = st.session_state.analysis_results['supply_chain']
            
            # عرض الموردين المحتملين
            if 'potential_suppliers' in supply_chain:
                st.subheader("الموردين المحتملين")
                suppliers_df = pd.DataFrame(supply_chain['potential_suppliers'])
                st.dataframe(suppliers_df)
            
            # عرض المخاطر المتعلقة بسلسلة الإمداد
            if 'risks' in supply_chain:
                st.subheader("مخاطر سلسلة الإمداد")
                
                for i, risk in enumerate(supply_chain['risks']):
                    with st.expander(f"المخاطرة {i+1}: {risk['title']}"):
                        st.write(f"**الوصف:** {risk['description']}")
                        st.write(f"**الاحتمالية:** {risk['probability']}")
                        st.write(f"**التأثير:** {risk['impact']}")
                        st.write(f"**استراتيجيات التخفيف:** {risk['mitigation']}")
            
            # عرض توصيات تحسين سلسلة الإمداد
            if 'optimization' in supply_chain:
                st.subheader("توصيات تحسين سلسلة الإمداد")
                
                for i, opt in enumerate(supply_chain['optimization']):
                    st.write(f"{i+1}. {opt}")
        else:
            st.info("يرجى رفع المستندات وبدء التحليل لعرض تحليل سلسلة الإمداد.")
    
    # الجدول الزمني - القسم السادس
    with tabs[5]:
        st.header("تحليل الجدول الزمني")
        
        if st.session_state.analysis_results is not None and 'schedule' in st.session_state.analysis_results:
            schedule = st.session_state.analysis_results['schedule']
            
            # عرض المراحل الرئيسية للمشروع
            if 'phases' in schedule:
                st.subheader("المراحل الرئيسية للمشروع")
                
                for i, phase in enumerate(schedule['phases']):
                    with st.expander(f"المرحلة {i+1}: {phase['name']}"):
                        st.write(f"**البداية:** {phase['start_date']}")
                        st.write(f"**النهاية:** {phase['end_date']}")
                        st.write(f"**المدة:** {phase['duration']} أيام")
                        st.write(f"**الأنشطة:** {', '.join(phase['activities'])}")
            
            # عرض المسار الحرج
            if 'critical_path' in schedule:
                st.subheader("المسار الحرج")
                
                for i, activity in enumerate(schedule['critical_path']):
                    st.write(f"{i+1}. {activity}")
            
            # عرض توصيات لتحسين الجدول الزمني
            if 'optimization' in schedule:
                st.subheader("توصيات تحسين الجدول الزمني")
                
                for i, opt in enumerate(schedule['optimization']):
                    st.write(f"{i+1}. {opt}")
        else:
            st.info("يرجى رفع المستندات وبدء التحليل لعرض تحليل الجدول الزمني.")
    
    # التوصيات والملخص - القسم السابع
    with tabs[6]:
        st.header("التوصيات والملخص")
        
        if st.session_state.analysis_results is not None and 'recommendations' in st.session_state.analysis_results:
            recommendations = st.session_state.analysis_results['recommendations']
            
            # عرض التوصيات الرئيسية
            st.subheader("التوصيات الرئيسية")
            
            for i, rec in enumerate(recommendations):
                with st.expander(f"التوصية {i+1}: {rec['title']}"):
                    st.write(f"**الوصف:** {rec['description']}")
                    st.write(f"**الأولوية:** {rec['priority']}")
                    st.write(f"**الفوائد:** {rec['benefits']}")
                    
                    if 'implementation' in rec:
                        st.write(f"**خطوات التنفيذ:**")
                        for j, step in enumerate(rec['implementation']):
                            st.write(f"  {j+1}. {step}")
            
            # عرض الملخص التنفيذي
            if 'executive_summary' in st.session_state.analysis_results:
                st.subheader("الملخص التنفيذي")
                st.write(st.session_state.analysis_results['executive_summary'])
        else:
            st.info("يرجى رفع المستندات وبدء التحليل لعرض التوصيات والملخص.")
    
    # معالجة زر التحليل
    if analysis_btn and uploaded_files:
        with st.spinner("جارٍ تحليل المستندات..."):
            # معالجة المستندات المرفوعة
            extracted_data, file_contents = process_uploaded_documents(uploaded_files)
            st.session_state.extracted_data = extracted_data
            
            # تحليل المتطلبات
            requirement_results = analyze_requirements(extracted_data)
            
            # تحليل المحتوى المحلي
            local_content_results = analyze_local_content(
                extracted_data, 
                st.session_state.project_data
            )
            
            # إنشاء نتائج التحليل الشاملة
            st.session_state.analysis_results = {
                "requirements": requirement_results,
                "local_content": local_content_results,
                # هنا ستضاف نتائج التحليلات الأخرى
            }
            
            st.success("تم الانتهاء من التحليل!")
    elif analysis_btn and not uploaded_files:
        st.error("يرجى رفع المستندات المطلوبة أولاً.")

if __name__ == "__main__":
    main()