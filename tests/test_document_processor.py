import os
import sys
import unittest
from datetime import datetime
import tempfile

# إضافة المسار الرئيسي للمشروع إلى PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# استيراد الوحدات المراد اختبارها
from modules.document_processor import DocumentProcessor

class TestDocumentProcessor(unittest.TestCase):
    """
    اختبارات وحدة لمعالج المستندات
    """
    
    def setUp(self):
        """
        إعداد بيئة الاختبار
        """
        self.document_processor = DocumentProcessor()
        
        # إنشاء ملفات اختبار مؤقتة
        self.temp_files = {}
        
        # إنشاء ملف نصي للاختبار
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write("""
            مناقصة لإنشاء مبنى إداري
            
            المتطلبات:
            1. يجب أن تكون الشركة مصنفة في مجال المباني الدرجة الثانية على الأقل
            2. خبرة لا تقل عن 10 سنوات في مجال إنشاء المباني الإدارية
            3. تنفيذ 3 مشاريع مماثلة خلال الخمس سنوات الماضية
            
            المحتوى المحلي:
            يجب ألا تقل نسبة المحتوى المحلي عن 40% من إجمالي قيمة المشروع
            
            التكلفة التقديرية: 15,000,000 ريال سعودي
            
            المدة: 24 شهر
            
            تاريخ البدء: 01/01/2024
            """.encode('utf-8'))
            self.temp_files["txt"] = tmp.name
    
    def tearDown(self):
        """
        تنظيف بيئة الاختبار
        """
        # حذف الملفات المؤقتة
        for file_path in self.temp_files.values():
            if os.path.exists(file_path):
                os.remove(file_path)
    
    def test_process_txt_document(self):
        """
        اختبار معالجة ملف نصي
        """
        # قراءة محتوى الملف
        with open(self.temp_files["txt"], 'rb') as f:
            file_content = f.read()
        
        # معالجة الملف
        result = self.document_processor.process_document(
            file_content, 
            "txt", 
            "test_document.txt"
        )
        
        # التحقق من النتائج
        self.assertIn("text", result)
        self.assertIn("file_name", result)
        self.assertEqual(result["file_name"], "test_document.txt")
        self.assertEqual(result["file_type"], "txt")
        
        # التحقق من استخراج النص
        self.assertIn("مناقصة لإنشاء مبنى إداري", result["text"])
        
        # التحقق من استخراج المتطلبات
        self.assertIn("requirements", result)
        requirements = result.get("requirements", [])
        self.assertGreaterEqual(len(requirements), 1)
        
        # التحقق من استخراج المحتوى المحلي
        self.assertIn("local_content", result)
        local_content = result.get("local_content", {})
        self.assertIn("percentages", local_content)
        
        # التحقق من استخراج البيانات المالية
        self.assertIn("financial_data", result)
        financial_data = result.get("financial_data", {})
        self.assertIn("total_cost", financial_data)
        
        # التحقق من استخراج التواريخ
        self.assertIn("dates", result)
        dates = result.get("dates", [])
        self.assertGreaterEqual(len(dates), 1)
    
    def test_extract_requirements(self):
        """
        اختبار استخراج المتطلبات
        """
        test_text = """
        المتطلبات الفنية:
        1. يجب أن يكون المقاول مصنفاً في مجال المباني الدرجة الأولى
        2. خبرة لا تقل عن 15 سنة
        
        المتطلبات المالية:
        1. ملاءة مالية لا تقل عن 10 مليون ريال
        """
        
        requirements = self.document_processor._extract_requirements(test_text)
        
        # التحقق من النتائج
        self.assertGreaterEqual(len(requirements), 2)
        
        # التحقق من تصنيف المتطلبات
        categories = set(req["category"] for req in requirements)
        self.assertIn("فنية", categories)
    
    def test_extract_local_content_info(self):
        """
        اختبار استخراج معلومات المحتوى المحلي
        """
