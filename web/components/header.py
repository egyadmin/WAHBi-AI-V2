import streamlit as st

def create_header():
    """
    إنشاء رأس الصفحة للتطبيق
    """
    # الزمن والتاريخ الحالي
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # العنوان الرئيسي حسب الصفحة المختارة
        current_page = st.session_state.page
        
        if current_page == "الرئيسية":
            st.title("لوحة المعلومات الرئيسية")
        elif current_page == "تحليل المناقصات":
            st.title("تحليل المناقصات")
        elif current_page == "تحليل المتطلبات":
            st.title("تحليل متطلبات المناقصات")
        elif current_page == "تقدير التكاليف":
            st.title("تقدير التكاليف والميزانية")
        elif current_page == "تحليل المخاطر":
            st.title("تحليل المخاطر وخطط التخفيف")
        elif current_page == "الجدول الزمني":
            st.title("إدارة الجدول الزمني والموارد")
        elif current_page == "المحتوى المحلي":
            st.title("تحليل وتحسين المحتوى المحلي")
        elif current_page == "سلاسل الإمداد":
            st.title("إدارة سلاسل الإمداد")
        elif current_page == "المشتريات":
            st.title("إدارة المشتريات والعقود")
        elif current_page == "الموردون والمقاولون":
            st.title("قاعدة بيانات الموردين والمقاولين")
        elif current_page == "المشاريع المستقبلية":
            st.title("تحليل المشاريع المستقبلية")
        elif current_page == "توقع احتمالية النجاح":
            st.title("توقع احتمالية نجاح العطاءات")
        elif current_page == "التقارير":
            st.title("التقارير والإحصائيات")
        else:
            st.title("نظام تحليل المناقصات")
    
    with col2:
        # زر تحديث البيانات
        if st.button("تحديث البيانات", key="refresh_data"):
            st.experimental_rerun()
    
    # خط فاصل تحت العنوان
    st.markdown("---")
    
    # وصف مختصر للصفحة الحالية
    if current_page == "الرئيسية":
        st.markdown("عرض ملخص للمناقصات النشطة والمؤشرات الرئيسية ولوحة المعلومات")
    elif current_page == "تحليل المناقصات":
        st.markdown("تحليل تفاصيل المناقصات واستخراج المعلومات الرئيسية")
    elif current_page == "تحليل المتطلبات":
        st.markdown("تحليل متطلبات المناقصة وتصنيفها حسب الأولوية والتخصص")
    elif current_page == "تقدير التكاليف":
        st.markdown("حساب التكاليف المتوقعة للمشروع وتوزيعها على بنود الميزانية")
    elif current_page == "تحليل المخاطر":
        st.markdown("تحديد وتقييم المخاطر المحتملة ووضع خطط للتخفيف منها")
    elif current_page == "الجدول الزمني":
        st.markdown("إنشاء وإدارة الجدول الزمني للمشروع وتخصيص الموارد")
    elif current_page == "المحتوى المحلي":
        st.markdown("تحليل نسب المحتوى المحلي والامتثال لمتطلبات النسب المطلوبة")
    elif current_page == "سلاسل الإمداد":
        st.markdown("تحليل وتحسين سلاسل الإمداد وتحديد مصادر المواد والخدمات")
    elif current_page == "المشتريات":
        st.markdown("إدارة عمليات الشراء والعقود مع الموردين والمقاولين")
    elif current_page == "الموردون والمقاولون":
        st.markdown("قاعدة بيانات شاملة للموردين والمقاولين وتقييم أدائهم")
    elif current_page == "المشاريع المستقبلية":
        st.markdown("تحليل واستشراف المشاريع المستقبلية المحتملة")
    elif current_page == "توقع احتمالية النجاح":
        st.markdown("استخدام نماذج التعلم الآلي لتوقع احتمالية نجاح العطاء")
    elif current_page == "التقارير":
        st.markdown("إنشاء وتصدير تقارير مفصلة وإحصائيات عن المناقصات والمشاريع")
    
    # مساحة فارغة بعد الوصف
    st.markdown("")