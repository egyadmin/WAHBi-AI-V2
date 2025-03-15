import streamlit as st
import datetime

def create_sidebar():
    """
    إنشاء الشريط الجانبي للتطبيق
    """
    with st.sidebar:
        # شعار الشركة والعنوان
        st.image("https://via.placeholder.com/150x100?text=شعار+الشركة", width=150)
        st.title("نظام تحليل المناقصات")
        st.markdown("---")
        
        # معلومات المستخدم
        user_info = st.session_state.user_info
        st.markdown(f"**مرحباً، {user_info['user_name']}**")
        st.markdown(f"**الشركة:** {user_info['company']}")
        st.markdown(f"**الدور:** {user_info['role']}")
        st.markdown("---")
        
        # القائمة الرئيسية
        st.subheader("القائمة الرئيسية")
        page = st.radio(
            "اختر الصفحة:",
            [
                "الرئيسية",
                "تحليل المناقصات",
                "تحليل المتطلبات",
                "تقدير التكاليف",
                "تحليل المخاطر",
                "الجدول الزمني",
                "المحتوى المحلي",
                "سلاسل الإمداد",
                "المشتريات",
                "الموردون والمقاولون",
                "المشاريع المستقبلية",
                "توقع احتمالية النجاح",
                "التقارير"
            ]
        )
        
        st.markdown("---")
        
        # أدوات إضافية
        st.subheader("أدوات")
        
        # أداة تحديد الفترة الزمنية
        st.markdown("**فلترة حسب التاريخ**")
        
        today = datetime.date.today()
        start_date = st.date_input(
            "من تاريخ:",
            today.replace(month=1, day=1)
        )
        
        end_date = st.date_input(
            "إلى تاريخ:",
            today
        )
        
        # قسم البحث
        st.markdown("**بحث عن مناقصة**")
        search_query = st.text_input("أدخل رقم المناقصة أو الكلمات المفتاحية")
        
        if st.button("بحث"):
            st.session_state.search_query = search_query
        
        st.markdown("---")
        
        # معلومات النظام
        st.markdown("**معلومات النظام**")
        st.text(f"الإصدار: {st.session_state.config.get('app', {}).get('version', '1.0.0')}")
        st.text(f"تاريخ اليوم: {today.strftime('%Y-%m-%d')}")
        
        # حقوق النشر
        st.markdown("---")
        st.markdown("© 2025 شركة شبه الجزيرة للمقاولات")
    
    # تحديث حالة الصفحة
    st.session_state.page = page
    
    return page