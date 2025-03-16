import os
import sys
import streamlit as st
import logging
from datetime import datetime

# إضافة المسار الرئيسي للمشروع إلى PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد الوحدات الخاصة بالمشروع
from config import get_config
from web.pages.procurement import main as procurement_page

# إعداد التسجيل
config = get_config()
log_dir = config["paths"]["logs_dir"]
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log"),
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def main():
    """
    الدالة الرئيسية لتشغيل التطبيق
    """
    # تكوين الصفحة
    st.set_page_config(
        page_title=config["app"]["name"],
        page_icon="📋",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # تسجيل بدء تشغيل التطبيق
    logger.info(f"Starting {config['app']['name']} v{config['app']['version']}")
    
    # اختيار الصفحة
    pages = {
        "المناقصات والعقود": procurement_page,
        # يمكن إضافة صفحات أخرى هنا
    }
    
    # شريط التنقل الجانبي
    with st.sidebar:
        st.title(config["app"]["name"])
        st.markdown(f"**الإصدار:** {config['app']['version']}")
        
        # اختيار الصفحة
        page = st.radio("اختر الصفحة:", list(pages.keys()))
        
        # معلومات إضافية
        st.markdown("---")
        st.markdown("### المطور بواسطة")
        st.markdown("فريق تطوير البرمجيات")
        st.markdown("© 2023-2024 جميع الحقوق محفوظة")
    
    # عرض الصفحة المختارة
    pages[page]()
    
    # تذييل الصفحة
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: gray; font-size: 0.8em;">
            {config["app"]["name"]} - الإصدار {config["app"]["version"]} | تم التحديث: {datetime.now().strftime("%Y-%m-%d")}
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()