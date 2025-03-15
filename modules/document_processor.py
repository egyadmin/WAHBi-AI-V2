import os
import re
import io
import tempfile
from typing import Dict, List, Any, Union, Tuple, Optional
import pandas as pd
import numpy as np
from datetime import datetime

# المكتبات الخاصة بمعالجة أنواع المستندات المختلفة
import docx
import PyPDF2
import fitz  # PyMuPDF
import textract
import mammoth
from openpyxl import load_workbook
from PIL import Image
import pytesseract

# المكتبات الخاصة بالمعالجة الطبيعية للغة
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import ngrams

# تحميل الموارد اللازمة للغة العربية
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class DocumentProcessor:
    """
    فئة لمعالجة المستندات المختلفة وتحليلها واستخراج المعلومات منها
    تدعم الملفات بصيغة PDF, DOCX, XLSX, CSV, TXT
    """
    
    def __init__(self):
        """
        تهيئة معالج المستندات
        """
        # تحميل قائمة الكلمات الدلالية للمناقصات
        self.tender_keywords = self._load_tender_keywords()
        
        # تحميل قائمة المتطلبات الشائعة
        self.common_requirements = self._load_common_requirements()
        
        # الكلمات التوقفية في اللغة العربية
        self.arabic_stopwords = set(stopwords.words('arabic'))
        
        # تعريف أنماط التعبيرات المنتظمة
        self.regex_patterns = {
            "money": r'(\d[\d,.]*)\s*(ريال|ر\.س|SAR|ر\.س\.)',
            "percentage": r'(\d[\d,.]*)\s*(%|في المائة|في المئة|بالمائة|بالمئة)',
            "date": r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})|(\d{1,2})\s+(يناير|فبراير|مارس|أبريل|مايو|يونيو|يوليو|أغسطس|سبتمبر|أكتوبر|نوفمبر|ديسمبر)\s+(\d{2,4})',
            "email": r'[\w\.-]+@[\w\.-]+\.\w+',
            "phone": r'([\+]?[\d]{1,3}[\s-]?)?(\d{3,4})[\s-]?(\d{3,4})[\s-]?(\d{3,4})',
            "url": r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        }
        
        # قائمة بكلمات المناقصات الهامة
        self.important_tender_terms = [
            "مناقصة", "عطاء", "ترسية", "عقد", "مشروع", "تسليم", "اجتماع", "تمهيدي",
            "ضمان", "كفالة", "ابتدائي", "نهائي", "غرامة", "غرامات", "جزائية", "صيانة",
            "ضمان", "تمديد", "تأجيل", "إلغاء", "تعديل", "ملحق", "مصنع محلي", "مستورد",
            "المحتوى المحلي", "التقييم الفني", "التقييم المالي", "العرض الفني", "العرض المالي"
        ]
        
    def _load_tender_keywords(self) -> Dict[str, List[str]]:
        """
        تحميل الكلمات الدلالية المتعلقة بالمناقصات وتصنيفها
        """
        # في التطبيق الفعلي، قد تُحمل هذه الكلمات من ملف أو قاعدة بيانات
        return {
            "requirements": [
                "متطلبات", "شروط", "مواصفات", "معايير", 
                "يجب", "يتعين", "ضرورة", "إلزامي", "إلزامية",
                "المتطلبات الفنية", "المتطلبات الإدارية", "الاشتراطات"
            ],
            "costs": [
                "تكلفة", "تكاليف", "سعر", "أسعار", "ميزانية", 
                "قيمة", "مالي", "مالية", "تمويل", "تقدير مالي",
                "ريال", "ريال سعودي", "سعودي"
            ],
            "dates": [
                "تاريخ", "مدة", "جدول زمني", "موعد", "مهلة",
                "التسليم", "الاستحقاق", "بداية", "نهاية", "أيام",
                "أسابيع", "شهور", "سنوات"
            ],
            "local_content": [
                "محتوى محلي", "توطين", "نطاقات", "سعودة", 
                "وطني", "محلية", "إنتاج محلي", "صناعة محلية",
                "منتجات وطنية", "خدمات وطنية", "منشأ سعودي",
                "رؤية 2030", "رؤية المملكة"
            ],
            "supply_chain": [
                "سلسلة الإمداد", "توريد", "موردين", "مناولة", 
                "لوجستيات", "مخزون", "مخازن", "شراء", "بضائع",
                "سلسلة التوريد", "جدولة الإمداد", "الواردات"
            ]
        }
    
    def _load_common_requirements(self) -> List[Dict[str, Any]]:
        """
        تحميل قائمة المتطلبات الشائعة للمناقصات
        """
        # في التطبيق الفعلي، قد تُحمل هذه المتطلبات من ملف أو قاعدة بيانات
        return [
            {
                "title": "شهادة الزكاة والدخل",
                "category": "إدارية",
                "keywords": ["زكاة", "ضريبة", "شهادة زكاة", "مصلحة الزكاة", "هيئة الزكاة", "إقرار ضريبي"]
            },
            {
                "title": "السجل التجاري",
                "category": "إدارية",
                "keywords": ["سجل تجاري", "الغرفة التجارية", "رخصة تجارية", "وزارة التجارة"]
            },
            {
                "title": "شهادة الاشتراك في التأمينات الاجتماعية",
                "category": "إدارية",
                "keywords": ["تأمينات", "تأمينات اجتماعية", "مؤسسة التأمينات", "تأمين اجتماعي"]
            },
            {
                "title": "تصنيف المقاولين",
                "category": "فنية",
                "keywords": ["تصنيف", "شهادة تصنيف", "المقاولين", "وزارة الإسكان", "وزارة الشؤون البلدية"]
            },
            {
                "title": "نسبة المحتوى المحلي",
                "category": "محتوى محلي",
                "keywords": ["محتوى محلي", "نسبة سعودة", "توطين", "نطاقات", "رؤية 2030"]
            },
            {
                "title": "الخبرات السابقة",
                "category": "فنية",
                "keywords": ["خبرة", "خبرات سابقة", "مشاريع مماثلة", "أعمال سابقة", "سابقة أعمال"]
            }
        ]
        
    def process_document(self, file_content: bytes, file_extension: str, file_name: str) -> Dict[str, Any]:
        """
        معالجة المستند وتحليله حسب نوعه
        
        المعاملات:
        ----------
        file_content : bytes
            محتوى الملف بصيغة بايت
        file_extension : str
            امتداد الملف (pdf, docx, xlsx, csv, txt)
        file_name : str
            اسم الملف
            
        المخرجات:
        --------
        Dict[str, Any]
            قاموس يحتوي على البيانات المستخرجة من المستند
        """
        # تخزين المحتوى في ملف مؤقت
        with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=False) as temp_file:
            temp_file.write(file_content)
            temp_path = temp_file.name
        
        try:
            # معالجة الملف حسب نوعه
            if file_extension.lower() == 'pdf':
                extracted_data = self._process_pdf(temp_path)
            elif file_extension.lower() in ['docx', 'doc']:
                extracted_data = self._process_docx(temp_path)
            elif file_extension.lower() in ['xlsx', 'xls']:
                extracted_data = self._process_excel(temp_path)
            elif file_extension.lower() == 'csv':
                extracted_data = self._process_csv(temp_path)
            elif file_extension.lower() == 'txt':
                extracted_data = self._process_txt(temp_path)
            else:
                extracted_data = {"error": f"نوع الملف {file_extension} غير مدعوم"}
            
            # إضافة معلومات أساسية عن الملف
            extracted_data["file_name"] = file_name
            extracted_data["file_type"] = file_extension
            extracted_data["processed_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # تحليل إضافي للمحتوى المستخرج
            if "text" in extracted_data:
                self._analyze_text_content(extracted_data)
            
            return extracted_data
            
        finally:
            # حذف الملف المؤقت بعد الانتهاء
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    def _process_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        معالجة ملف PDF واستخراج النص والبيانات منه
        """
        extracted_data = {
            "text": "",
            "metadata": {},
            "images": [],
            "tables": [],
            "pages": []
        }
        
        try:
            # استخراج النص باستخدام PyMuPDF (fitz)
            doc = fitz.open(file_path)
            
            # استخراج البيانات الوصفية
            extracted_data["metadata"] = doc.metadata
            
            # معالجة كل صفحة
            for page_num, page in enumerate(doc):
                page_text = page.get_text()
                extracted_data["text"] += page_text
                
                # إضافة معلومات الصفحة
                page_data = {
                    "page_num": page_num + 1,
                    "text": page_text,
                    "dimensions": {"width": page.rect.width, "height": page.rect.height}
                }
                
                # استخراج الصور
                image_list = page.get_images(full=True)
                page_images = []
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_info = {
                        "index": img_index,
                        "width": base_image["width"],
                        "height": base_image["height"],
                        "format": base_image["ext"]
                    }
                    page_images.append(image_info)
                
                page_data["images"] = page_images
                
                # استخراج الجداول (تقريبي - قد يحتاج لتحسين)
                tables = []
                # بالنسبة للجداول، نستخدم تعبير منتظم للبحث عن نمط من المسافات وعلامات الجدولة
                # هذه طريقة بسيطة وقد تحتاج لتحسين باستخدام مكتبات متخصصة
                table_pattern = re.compile(r'(.+?[\t|]{2,}.+?[\n\r]){3,}', re.DOTALL)
                for match in table_pattern.finditer(page_text):
                    tables.append(match.group(0))
                
                page_data["tables"] = tables
                extracted_data["pages"].append(page_data)
                
                # جمع كل الجداول المستخرجة
                extracted_data["tables"].extend(tables)
            
            # إذا لم نستطع استخراج نص باستخدام PyMuPDF، نجرب PyPDF2
            if not extracted_data["text"].strip():
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        extracted_data["text"] += page.extract_text()
            
            # إذا لم نستطع استخراج نص بعد، نجرب textract
            if not extracted_data["text"].strip():
                extracted_data["text"] = textract.process(file_path).decode('utf-8', errors='ignore')
                
            # تحليل OCR إذا كان النص قليلاً أو غير موجود
            if len(extracted_data["text"].strip()) < 100:
                self._apply_ocr_to_pdf(file_path, extracted_data)
                
        except Exception as e:
            extracted_data["error"] = f"خطأ في معالجة ملف PDF: {str(e)}"
            
        return extracted_data
    
    def _apply_ocr_to_pdf(self, file_path: str, extracted_data: Dict[str, Any]) -> None:
        """
        تطبيق OCR على ملف PDF لاستخراج النص من الصور
        """
        try:
            doc = fitz.open(file_path)
            ocr_text = ""
            
            for page_num, page in enumerate(doc):
                # استخراج الصفحة كصورة
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                
                # فتح الصورة باستخدام PIL
                with io.BytesIO(img_data) as img_stream:
                    img = Image.open(img_stream)
                    
                    # تطبيق OCR
                    page_text = pytesseract.image_to_string(img, lang='ara+eng')
                    ocr_text += page_text
                    
                    # إضافة النص المستخرج إلى بيانات الصفحة
                    if page_num < len(extracted_data["pages"]):
                        extracted_data["pages"][page_num]["ocr_text"] = page_text
            
            # إضافة النص المستخرج بواسطة OCR
            extracted_data["ocr_text"] = ocr_text
            
            # إذا كان النص الأصلي فارغاً، استخدم نص OCR كبديل
            if not extracted_data["text"].strip():
                extracted_data["text"] = ocr_text
                
        except Exception as e:
            extracted_data["ocr_error"] = f"خطأ في معالجة OCR: {str(e)}"
    
    def _process_docx(self, file_path: str) -> Dict[str, Any]:
        """
        معالجة ملف Word (DOCX) واستخراج النص والبيانات منه
        """
        extracted_data = {
            "text": "",
            "metadata": {},
            "images": [],
            "tables": [],
            "paragraphs": []
        }
        
        try:
            # استخراج النص من ملف DOCX
            doc = docx.Document(file_path)
            
            # استخراج النص الكامل
            for para in doc.paragraphs:
                if para.text.strip():
                    extracted_data["text"] += para.text + "\n"
                    extracted_data["paragraphs"].append({
                        "text": para.text,
                        "style": para.style.name if para.style else "Normal"
                    })
            
            # استخراج الجداول
            tables_data = []
            for table_idx, table in enumerate(doc.tables):
                table_data = []
                for row_idx, row in enumerate(table.rows):
                    row_data = []
                    for cell_idx, cell in enumerate(row.cells):
                        row_data.append(cell.text)
                    table_data.append(row_data)
                tables_data.append({
                    "table_idx": table_idx,
                    "data": table_data
                })
            extracted_data["tables"] = tables_data
            
            # استخراج البيانات الوصفية
            doc_properties = doc.core_properties
            extracted_data["metadata"] = {
                "author": doc_properties.author,
                "created": str(doc_properties.created) if doc_properties.created else None,
                "modified": str(doc_properties.modified) if doc_properties.modified else None,
                "title": doc_properties.title,
                "subject": doc_properties.subject,
                "keywords": doc_properties.keywords
            }
            
            # تجربة استخدام mammoth للحصول على نص إضافي إذا لزم الأمر
            if not extracted_data["text"].strip():
                with open(file_path, "rb") as docx_file:
                    result = mammoth.extract_raw_text(docx_file)
                    extracted_data["text"] = result.value
            
        except Exception as e:
            extracted_data["error"] = f"خطأ في معالجة ملف DOCX: {str(e)}"
            
            # محاولة استخراج النص باستخدام textract كخطة بديلة
            try:
                extracted_data["text"] = textract.process(file_path).decode('utf-8', errors='ignore')
            except:
                pass
                
        return extracted_data
    
    def _process_excel(self, file_path: str) -> Dict[str, Any]:
        """
        معالجة ملف Excel واستخراج البيانات منه
        """
        extracted_data = {
            "sheets": [],
            "tables": [],
            "text": ""
        }
        
        try:
            # قراءة الملف باستخدام pandas
            xl = pd.ExcelFile(file_path)
            sheet_names = xl.sheet_names
            
            # استخراج البيانات من كل ورقة
            all_sheets_data = {}
            for sheet_name in sheet_names:
                df = pd.read_excel(xl, sheet_name)
                sheet_data = df.fillna('').to_dict(orient='records')
                all_sheets_data[sheet_name] = sheet_data
                
                # جمع النص لتحليل المحتوى
                for row in sheet_data:
                    for column, value in row.items():
                        if isinstance(value, str) and value.strip():
                            extracted_data["text"] += value + " "
                
                # إضافة معلومات الورقة
                sheet_info = {
                    "name": sheet_name,
                    "rows": len(df),
                    "columns": len(df.columns),
                    "column_names": df.columns.tolist(),
                    "data": sheet_data
                }
                extracted_data["sheets"].append(sheet_info)
                
                # إضافة كجدول
                extracted_data["tables"].append({
                    "sheet_name": sheet_name,
                    "data": sheet_data
                })
            
            # استخراج البيانات الوصفية باستخدام openpyxl
            workbook = load_workbook(file_path, read_only=True)
            extracted_data["metadata"] = {
                "title": workbook.properties.title,
                "author": workbook.properties.creator,
                "created": str(workbook.properties.created) if workbook.properties.created else None,
                "modified": str(workbook.properties.modified) if workbook.properties.modified else None,
                "sheet_names": workbook.sheetnames
            }
            
        except Exception as e:
            extracted_data["error"] = f"خطأ في معالجة ملف Excel: {str(e)}"
            
        return extracted_data
    
    def _process_csv(self, file_path: str) -> Dict[str, Any]:
        """
        معالجة ملف CSV واستخراج البيانات منه
        """
        extracted_data = {
            "headers": [],
            "data": [],
            "text": ""
        }
        
        try:
            # قراءة الملف بعدة ترميزات للتعامل مع الملفات العربية
            encodings = ['utf-8', 'cp1256', 'iso-8859-6', 'utf-16']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except:
                    continue
            
            if df is None:
                # محاولة أخيرة باستخدام ترميز لاتيني وتجاهل الأخطاء
                df = pd.read_csv(file_path, encoding='latin1', errors='ignore')
            
            # استخراج البيانات
            extracted_data["headers"] = df.columns.tolist()
            extracted_data["data"] = df.fillna('').to_dict(orient='records')
            
            # جمع النص لتحليل المحتوى
            for row in extracted_data["data"]:
                for column, value in row.items():
                    if isinstance(value, str) and value.strip():
                        extracted_data["text"] += value + " "
            
            # إضافة معلومات إحصائية
            extracted_data["stats"] = {
                "rows": len(df),
                "columns": len(df.columns)
            }
            
        except Exception as e:
            extracted_data["error"] = f"خطأ في معالجة ملف CSV: {str(e)}"
            
        return extracted_data
    
    def _process_txt(self, file_path: str) -> Dict[str, Any]:
        """
        معالجة ملف نص عادي واستخراج البيانات منه
        """
        extracted_data = {
            "text": "",
            "lines": []
        }
        
        try:
            # قراءة الملف بعدة ترميزات للتعامل مع الملفات العربية
            encodings = ['utf-8', 'cp1256', 'iso-8859-6', 'utf-16']
            text_content = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        text_content = f.read()
                    break
                except:
                    continue
            
            if text_content is None:
                # محاولة أخيرة باستخدام ترميز لاتيني وتجاهل الأخطاء
                with open(file_path, 'r', encoding='latin1', errors='ignore') as f:
                    text_content = f.read()
            
            # إضافة النص والأسطر
            extracted_data["text"] = text_content
            extracted_data["lines"] = text_content.splitlines()
            
            # إضافة معلومات إحصائية
            extracted_data["stats"] = {
                "lines": len(extracted_data["lines"]),
                "words": len(text_content.split()),
                "chars": len(text_content)
            }
            
        except Exception as e:
            extracted_data["error"] = f"خطأ في معالجة ملف النص: {str(e)}"
            
        return extracted_data
    
    def _analyze_text_content(self, extracted_data: Dict[str, Any]) -> None:
        """
        تحليل محتوى النص المستخرج لاستخراج معلومات إضافية
        مثل المتطلبات، وتفاصيل المناقصة، والمحتوى المحلي.
        """
        text = extracted_data["text"]
        
        # استخراج الكلمات الدلالية
        keywords = {}
        for category, terms in self.tender_keywords.items():
            category_keywords = []
            for term in terms:
                pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE | re.MULTILINE)
                matches = pattern.findall(text)
                if matches:
                    category_keywords.extend(matches)
            keywords[category] = category_keywords
        
        extracted_data["keywords"] = keywords
        
        # استخراج المتطلبات المحتملة
        requirements = self._extract_requirements(text)
        extracted_data["requirements"] = requirements
        
        # استخراج البيانات المالية (أرقام، مبالغ، نسب مئوية)
        financial_data = self._extract_financial_data(text)
        extracted_data["financial_data"] = financial_data
        
        # استخراج التواريخ الهامة
        dates = self._extract_dates(text)
        extracted_data["dates"] = dates
        
        # استخراج معلومات المحتوى المحلي
        local_content = self._extract_local_content_info(text)
        extracted_data["local_content"] = local_content
        
        # استخراج معلومات سلسلة الإمداد
        supply_chain = self._extract_supply_chain_info(text)
        extracted_data["supply_chain"] = supply_chain
        
        # استخراج الجهات والأطراف المعنية
        entities = self._extract_entities(text)
        extracted_data["entities"] = entities
    
    def _extract_requirements(self, text: str) -> List[Dict[str, Any]]:
        """
        استخراج المتطلبات المحتملة من النص
        """
        requirements = []
        
        # البحث عن المتطلبات بناءً على كلمات دلالية
        for req_keyword in self.tender_keywords["requirements"]:
            # كلمات البداية للمتطلبات ونهايتها
            pattern = re.compile(
                r'(' + re.escape(req_keyword) + r'[^\n.]{0,100})([\n.].{0,500}?)(?:\n\n|\.\s|$)',
                re.DOTALL | re.MULTILINE
            )
            matches = pattern.finditer(text)
            
            for match in matches:
                title = match.group(1).strip()
                description = match.group(2).strip()
                
                # تحديد الأهمية بناءً على وجود كلمات إلزامية
                importance = "عادية"
                for imp_word in ["يجب", "إلزامي", "ضروري", "لا بد", "إجباري"]:
                    if imp_word in title.lower() or imp_word in description.lower():
                        importance = "عالية"
                        break
                
                # تحديد الفئة
                category = "عامة"
                for cat, words in [
                    ("فنية", ["فني", "تقني", "مواصفات", "معايير", "أداء", "جودة"]),
                    ("إدارية", ["إداري", "قانوني", "تنظيمي", "إجرائي", "شروط"]),
                    ("مالية", ["مالي", "سعر", "تكلفة", "دفع", "تسعير", "ميزانية"]),
                    ("محتوى محلي", ["محلي", "محتوى محلي", "توطين", "سعودة"]),
                    ("زمنية", ["زمني", "موعد", "تاريخ", "مدة", "جدول"])
                ]:
                    for word in words:
                        if word in title.lower() or word in description.lower():
                            category = cat
                            break
                
                # إضافة المتطلب
                requirement = {
                    "title": title,
                    "description": description,
                    "importance": importance,
                    "category": category
                }
                requirements.append(requirement)
        
        # البحث عن المتطلبات من قائمة المتطلبات الشائعة
        for common_req in self.common_requirements:
            for keyword in common_req["keywords"]:
                if keyword in text:
                    # التحقق من أن المتطلب لم تتم إضافته بالفعل
                    if not any(req["title"] == common_req["title"] for req in requirements):
                        # العثور على الفقرة المتعلقة بهذا المتطلب
                        pattern = re.compile(
                            r'(.{0,100}' + re.escape(keyword) + r'.{0,200})',
                            re.DOTALL | re.MULTILINE
                        )
                        match = pattern.search(text)
                        
                        description = match.group(1).strip() if match else "تم التعرف على المتطلب ولكن التفاصيل غير متاحة"
                        
                        requirement = {
                            "title": common_req["title"],
                            "description": description,
                            "importance": "عالية",
                            "category": common_req["category"],
                            "is_common": True
                        }
                        requirements.append(requirement)
                        break
        
        return requirements
    
    def _extract_financial_data(self, text: str) -> Dict[str, Any]:
        """
        استخراج البيانات المالية من النص
        """
        financial_data = {
            "amounts": [],
            "percentages": [],
            "total_cost": None
        }
        
        # استخراج المبالغ المالية
        money_pattern = self.regex_patterns["money"]
        money_matches = re.finditer(money_pattern, text)
        
        for match in money_matches:
            amount = match.group(1)
            currency = match.group(2)
            
            # تنظيف الرقم
            amount = amount.replace(',', '')
            try:
                amount_value = float(amount)
                financial_data["amounts"].append({
                    "value": amount_value,
                    "currency": currency,
                    "original": match.group(0),
                    "context": text[max(0, match.start() - 50):min(len(text), match.end() + 50)]
                })
            except:
                pass
        
        # استخراج النسب المئوية
        percentage_pattern = self.regex_patterns["percentage"]
        percentage_matches = re.finditer(percentage_pattern, text)
        
        for match in percentage_matches:
            percentage = match.group(1)
            
            # تنظيف الرقم
            percentage = percentage.replace(',', '')
            try:
                percentage_value = float(percentage)
                financial_data["percentages"].append({
                    "value": percentage_value,
                    "original": match.group(0),
                    "context": text[max(0, match.start() - 50):min(len(text), match.end() + 50)]
                })
            except:
                pass
        
        # محاولة تحديد التكلفة الإجمالية
        total_cost_patterns = [
            r'القيمة الإجمالية[^\d]*([\d.,]+)[^\d]*(ريال|ر\.س)',
            r'إجمالي القيمة[^\d]*([\d.,]+)[^\d]*(ريال|ر\.س)',
            r'المبلغ الإجمالي[^\d]*([\d.,]+)[^\d]*(ريال|ر\.س)',
            r'قيمة العقد[^\d]*([\d.,]+)[^\d]*(ريال|ر\.س)',
            r'قيمة المشروع[^\d]*([\d.,]+)[^\d]*(ريال|ر\.س)'
        ]
        
        for pattern in total_cost_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount = match.group(1).replace(',', '')
                try:
                    amount_value = float(amount)
                    financial_data["total_cost"] = {
                        "value": amount_value,
                        "currency": match.group(2),
                        "original": match.group(0)
                    }
                    break
                except:
                    pass
        
        return financial_data
    
    def _extract_dates(self, text: str) -> List[Dict[str, Any]]:
        """
        استخراج التواريخ الهامة من النص
        """
        dates = []
        
        # استخراج التواريخ باستخدام التعبير المنتظم
        date_pattern = self.regex_patterns["date"]
        date_matches = re.finditer(date_pattern, text)
        
        # قاموس لتحويل أسماء الشهور العربية إلى أرقام
        month_to_num = {
            "يناير": 1, "فبراير": 2, "مارس": 3, "أبريل": 4, "مايو": 5, "يونيو": 6,
            "يوليو": 7, "أغسطس": 8, "سبتمبر": 9, "أكتوبر": 10, "نوفمبر": 11, "ديسمبر": 12
        }
        
        for match in date_matches:
            try:
                # التحقق من نوع التاريخ المستخرج (رقمي أو مع اسم الشهر)
                if match.group(1):  # تاريخ رقمي بالكامل
                    day = int(match.group(1))
                    month = int(match.group(2))
                    year = int(match.group(3))
                    if year < 100:  # تحويل سنة مختصرة
                        year += 2000 if year < 50 else 1900
                else:  # تاريخ مع اسم الشهر
                    day = int(match.group(4))
                    month = month_to_num[match.group(5)]
                    year = int(match.group(6))
                    if year < 100:  # تحويل سنة مختصرة
                        year += 2000 if year < 50 else 1900
                
                # التحقق من صحة التاريخ
                if 1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2100:
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    
                    # محاولة تحديد نوع التاريخ بناءً على السياق
                    context = text[max(0, match.start() - 50):min(len(text), match.end() + 50)]
                    
                    date_type = "غير محدد"
                    for date_keyword, date_type_value in [
                        (["بداية", "بدء", "بدأ", "انطلاق"], "بداية"),
                        (["نهاية", "انتهاء", "الانتهاء", "إغلاق"], "نهاية"),
                        (["تسليم", "استلام", "توصيل"], "تسليم"),
                        (["إصدار", "صدور", "إصدار", "نشر"], "إصدار"),
                        (["اجتماع", "لقاء", "تمهيدي"], "اجتماع"),
                        (["زيارة", "معاينة", "موقع"], "زيارة ميدانية")
                    ]:
                        for keyword in date_keyword:
                            if keyword in context:
                                date_type = date_type_value
                                break
                        if date_type != "غير محدد":
                            break
                    
                    dates.append({
                        "date": date_str,
                        "original": match.group(0),
                        "context": context,
                        "type": date_type
                    })
            except:
                pass
        
        return dates
    
    def _extract_local_content_info(self, text: str) -> Dict[str, Any]:
        """
        استخراج معلومات المحتوى المحلي من النص
        """
        local_content = {
            "mentions": [],
            "percentages": [],
            "requirements": []
        }
        
        # كلمات دلالية متعلقة بالمحتوى المحلي
        keywords = [
            "المحتوى المحلي", "محتوى محلي", "توطين", "سعودة", "نطاقات", 
            "رؤية 2030", "رؤية المملكة", "النسبة المحلية", "الصناعة المحلية",
            "سلسلة الإمداد المحلية", "المنتجات المحلية", "الخدمات المحلية"
        ]
        
        # البحث عن ذكر المحتوى المحلي
        for keyword in keywords:
            pattern = re.compile(
                r'(.{0,100}' + re.escape(keyword) + r'.{0,200})',
                re.DOTALL | re.MULTILINE
            )
            matches = pattern.finditer(text)
            
            for match in matches:
                local_content["mentions"].append({
                    "keyword": keyword,
                    "context": match.group(1).strip()
                })
        
        # استخراج النسب المئوية المتعلقة بالمحتوى المحلي
        for mention in local_content["mentions"]:
            context = mention["context"]
            
            # البحث عن نسب مئوية في سياق المحتوى المحلي
            percentage_pattern = self.regex_patterns["percentage"]
            percentage_matches = re.finditer(percentage_pattern, context)
            
            for match in percentage_matches:
                percentage = match.group(1)
                
                # تنظيف الرقم
                percentage = percentage.replace(',', '')
                try:
                    percentage_value = float(percentage)
                    local_content["percentages"].append({
                        "value": percentage_value,
                        "keyword": mention["keyword"],
                        "original": match.group(0),
                        "context": context
                    })
                except:
                    pass
        
        # استخراج متطلبات المحتوى المحلي
        requirement_patterns = [
            r'يجب أن (يكون|تكون) نسبة المحتوى المحلي.{0,100}',
            r'يتعين على (المورد|المقاول|المتعهد|الشركة).{0,100}محتوى محلي.{0,100}',
            r'الحد الأدنى للمحتوى المحلي.{0,100}',
            r'يلتزم (المورد|المقاول|المتعهد|الشركة).{0,100}محتوى محلي.{0,100}'
        ]
        
        for pattern in requirement_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                requirement = match.group(0).strip()
                local_content["requirements"].append(requirement)
        
        return local_content
    
    def _extract_supply_chain_info(self, text: str) -> Dict[str, Any]:
        """
        استخراج معلومات سلسلة الإمداد من النص
        """
        supply_chain = {
            "mentions": [],
            "suppliers": [],
            "materials": []
        }
        
        # كلمات دلالية متعلقة بسلسلة الإمداد
        keywords = [
            "سلسلة الإمداد", "سلسلة التوريد", "موردين", "مناولة", "لوجستيات", 
            "مخزون", "توريد", "استيراد", "تخزين", "خدمات لوجستية", "مواد",
            "منتجات", "بضائع", "شحن", "نقل", "خدمات", "مصنع", "منتج محلي"
        ]
        
        # البحث عن ذكر سلسلة الإمداد
        for keyword in keywords:
            pattern = re.compile(
                r'(.{0,100}' + re.escape(keyword) + r'.{0,200})',
                re.DOTALL | re.MULTILINE
            )
            matches = pattern.finditer(text)
            
            for match in matches:
                supply_chain["mentions"].append({
                    "keyword": keyword,
                    "context": match.group(1).strip()
                })
        
        # استخراج أسماء الموردين المحتملين
        supplier_patterns = [
            r'(شركة|مؤسسة|مصنع)\s+([^\n.,]{3,50})',
            r'المورد\s+([^\n.,]{3,50})',
            r'التوريد من\s+([^\n.,]{3,50})',
            r'تصنيع بواسطة\s+([^\n.,]{3,50})'
        ]
        
        for pattern in supplier_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                supplier = match.group(1) + " " + match.group(2) if "شركة|مؤسسة|مصنع" in pattern else match.group(1)
                supplier = supplier.strip()
                
                # تجنب الإضافات المزدوجة
                if supplier not in [s["name"] for s in supply_chain["suppliers"]]:
                    supply_chain["suppliers"].append({
                        "name": supplier,
                        "context": text[max(0, match.start() - 30):min(len(text), match.end() + 30)]
                    })
        
        # استخراج المواد الخام أو المنتجات
        materials_patterns = [
            r'مواد\s+([^\n.,]{3,50})',
            r'منتجات\s+([^\n.,]{3,50})',
            r'توريد\s+([^\n.,]{3,50})',
            r'استيراد\s+([^\n.,]{3,50})'
        ]
        
        for pattern in materials_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                material = match.group(1).strip()
                
                # تجنب الإضافات المزدوجة
                if material not in [m["name"] for m in supply_chain["materials"]]:
                    supply_chain["materials"].append({
                        "name": material,
                        "context": text[max(0, match.start() - 30):min(len(text), match.end() + 30)]
                    })
        
        return supply_chain
    
    def _extract_entities(self, text: str) -> Dict[str, List[Dict[str, str]]]:
        """
        استخراج الجهات والأطراف المعنية من النص
        """
        entities = {
            "organizations": [],
            "persons": [],
            "locations": []
        }
        
        # استخراج المنظمات
        org_patterns = [
            r'(وزارة|هيئة|شركة|مؤسسة|جامعة|معهد|مركز|بلدية|أمانة)\s+([^\n.,]{3,50})',
            r'(جهة|جهات)\s+(حكومية|منفذة|مشرفة|متعاقدة|مالكة)'
        ]
        
        for pattern in org_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                org_name = match.group(0).strip()
                
                # تجنب الإضافات المزدوجة
                if org_name not in [org["name"] for org in entities["organizations"]]:
                    entities["organizations"].append({
                        "name": org_name,
                        "context": text[max(0, match.start() - 30):min(len(text), match.end() + 30)]
                    })
        
        # استخراج الأشخاص (بسيط - يمكن تحسينه)
        person_patterns = [
            r'(المهندس|الدكتور|الأستاذ|السيد|الشيخ|المدير|الرئيس)\s+([^\n.,]{3,50})',
            r'(مدير|رئيس|مسؤول|منسق|مشرف)\s+(المشروع|العقد|الموقع|العملية)'
        ]
        
        for pattern in person_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                person_name = match.group(0).strip()
                
                # تجنب الإضافات المزدوجة
                if person_name not in [p["name"] for p in entities["persons"]]:
                    entities["persons"].append({
                        "name": person_name,
                        "context": text[max(0, match.start() - 30):min(len(text), match.end() + 30)]
                    })
        
        # استخراج المواقع
        location_patterns = [
            r'مدينة\s+([^\n.,]{3,50})',
            r'محافظة\s+([^\n.,]{3,50})',
            r'منطقة\s+([^\n.,]{3,50})',
            r'حي\s+([^\n.,]{3,50})',
            r'موقع (المشروع|العمل|التنفيذ)'
        ]
        
        for pattern in location_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                location_name = match.group(0).strip()
                
                # تجنب الإضافات المزدوجة
                if location_name not in [loc["name"] for loc in entities["locations"]]:
                    entities["locations"].append({
                        "name": location_name,
                        "context": text[max(0, match.start() - 30):min(len(text), match.end() + 30)]
                    })
        
        return entities