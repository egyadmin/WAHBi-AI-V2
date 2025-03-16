import os
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Union, Tuple, Optional
from datetime import datetime

class VectorDBConnector:
    """
    فئة للاتصال بقاعدة بيانات المتجهات واسترجاع البيانات المتشابهة
    """
    
    def __init__(self, db_path: str = "data/vector_db"):
        """
        تهيئة الاتصال بقاعدة بيانات المتجهات
        
        المعاملات:
        ----------
        db_path : str, optional
            مسار قاعدة بيانات المتجهات (افتراضي: "data/vector_db")
        """
        self.db_path = db_path
        
        # التحقق من وجود قاعدة البيانات وإنشائها إذا لم تكن موجودة
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # تحميل البيانات المخزنة مسبقاً
        self.vectors = self._load_vectors()
    
    def _load_vectors(self) -> Dict[str, Any]:
        """
        تحميل المتجهات المخزنة مسبقاً
        """
        # في التطبيق الفعلي، ستُحمل المتجهات من قاعدة البيانات
        # هنا نستخدم بيانات افتراضية للتوضيح
        return {
            "tender1": {
                "text": "مناقصة لتطوير نظام إدارة موارد المؤسسة (ERP) لشركة متوسطة الحجم في قطاع التجارة والتوزيع",
                "vector": np.random.rand(384).tolist(),
                "metadata": {
                    "sector": "تقنية المعلومات",
                    "location": "جدة",
                    "date": "2023-08-22"
                }
            },
            "tender3": {
                "text": "مناقصة لتوريد وتركيب أنظمة تكييف مركزية لمجمع سكني يتكون من 5 مباني في المنطقة الشرقية",
                "vector": np.random.rand(384).tolist(),
                "metadata": {
                    "sector": "الإنشاءات",
                    "location": "الدمام",
                    "date": "2023-06-10"
                }
            },
            "tender4": {
                "text": "مناقصة لتقديم خدمات استشارية لتطوير استراتيجية التحول الرقمي لجهة حكومية",
                "vector": np.random.rand(384).tolist(),
                "metadata": {
                    "sector": "تقنية المعلومات",
                    "location": "الرياض",
                    "date": "2023-09-05"
                }
            },
            "tender5": {
                "text": "مناقصة لإنشاء مستودعات لوجستية بمساحة 10000 متر مربع في المدينة الصناعية الثانية بالرياض",
                "vector": np.random.rand(384).tolist(),
                "metadata": {
                    "sector": "الإنشاءات",
                    "location": "الرياض",
                    "date": "2023-07-18"
                }
            }
        }
    
    def store_vector(self, doc_id: str, text: str, vector: np.ndarray, metadata: Dict[str, Any] = None) -> bool:
        """
        تخزين متجه جديد في قاعدة البيانات
        
        المعاملات:
        ----------
        doc_id : str
            معرف المستند
        text : str
            النص الأصلي
        vector : np.ndarray
            متجه التمثيل
        metadata : Dict[str, Any], optional
            بيانات وصفية إضافية
            
        المخرجات:
        --------
        bool
            نجاح أو فشل العملية
        """
        try:
            self.vectors[doc_id] = {
                "text": text,
                "vector": vector.tolist(),
                "metadata": metadata or {}
            }
            return True
        except Exception as e:
            print(f"Error storing vector: {str(e)}")
            return False
    
    def retrieve_similar(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        استرجاع المستندات المتشابهة
        
        المعاملات:
        ----------
        query_vector : np.ndarray
            متجه الاستعلام
        top_k : int, optional
            عدد المستندات المراد استرجاعها (افتراضي: 5)
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة بالمستندات المتشابهة مع درجات التشابه
        """
        results = []
        
        for doc_id, doc_data in self.vectors.items():
            vector = np.array(doc_data["vector"])
            
            # حساب التشابه باستخدام جيب التمام (cosine similarity)
            similarity = np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))
            
            results.append({
                "doc_id": doc_id,
                "text": doc_data["text"],
                "similarity": float(similarity),
                "metadata": doc_data["metadata"]
            })
        
        # ترتيب النتائج حسب درجة التشابه (تنازلياً)
        results = sorted(results, key=lambda x: x["similarity"], reverse=True)
        
        return results[:top_k]
    
    def filter_by_metadata(self, filters: Dict[str, Any], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        تصفية المستندات حسب البيانات الوصفية
        
        المعاملات:
        ----------
        filters : Dict[str, Any]
            معايير التصفية
        top_k : int, optional
            عدد المستندات المراد استرجاعها (افتراضي: 5)
            
        المخرجات:
        --------
        List[Dict[str, Any]]
            قائمة بالمستندات المطابقة للمعايير
        """
        results = []
        
        for doc_id, doc_data in self.vectors.items():
            metadata = doc_data["metadata"]
            match = True
            
            for key, value in filters.items():
                if key not in metadata or metadata[key] != value:
                    match = False
                    break
            
            if match:
                results.append({
                    "doc_id": doc_id,
                    "text": doc_data["text"],
                    "metadata": metadata
                })
                
                if len(results) >= top_k:
                    break
        
        return results


class TemplateLoader:
    """
    فئة لتحميل القوالب المختلفة للمناقصات
    """
    
    def __init__(self, templates_path: str = "data/templates"):
        """
        تهيئة محمل القوالب
        
        المعاملات:
        ----------
        templates_path : str, optional
            مسار ملفات القوالب (افتراضي: "data/templates")
        """
        self.templates_path = templates_path
        
        # التحقق من وجود مجلد القوالب وإنشائه إذا لم يكن موجوداً
        os.makedirs(templates_path, exist_ok=True)
    
    def load_tender_templates(self) -> Dict[str, Any]:
        """
        تحميل قوالب المناقصات
        
        المخرجات:
        --------
        Dict[str, Any]
            قوالب المناقصات المختلفة
        """
        # في التطبيق الفعلي، ستُحمل القوالب من ملفات
        # هنا نستخدم قوالب افتراضية للتوضيح
        return {
            "construction": {
                "title": "نموذج مناقصة إنشائية",
                "sections": [
                    {
                        "name": "معلومات عامة",
                        "fields": [
                            {"name": "عنوان المناقصة", "type": "text", "required": True},
                            {"name": "وصف المشروع", "type": "text", "required": True},
                            {"name": "الموقع", "type": "text", "required": True},
                            {"name": "المدة", "type": "number", "unit": "شهر", "required": True},
                            {"name": "الميزانية التقديرية", "type": "number", "unit": "ريال", "required": False}
                        ]
                    },
                    {
                        "name": "متطلبات فنية",
                        "fields": [
                            {"name": "مساحة البناء", "type": "number", "unit": "متر مربع", "required": True},
                            {"name": "عدد الطوابق", "type": "number", "required": True},
                            {"name": "نوع الهيكل", "type": "select", "options": ["خرساني", "معدني", "مختلط"], "required": True},
                            {"name": "مواد البناء", "type": "text", "required": True},
                            {"name": "المواصفات الإضافية", "type": "text", "required": False}
                        ]
                    },
                    {
                        "name": "متطلبات المحتوى المحلي",
                        "fields": [
                            {"name": "نسبة المحتوى المحلي", "type": "number", "unit": "%", "required": True},
                            {"name": "نسبة توطين الوظائف", "type": "number", "unit": "%", "required": True},
                            {"name": "نسبة المورِّدين المحليين", "type": "number", "unit": "%", "required": True}
                        ]
                    },
                    {
                        "name": "الجدول الزمني",
                        "fields": [
                            {"name": "تاريخ بدء المشروع", "type": "date", "required": True},
                            {"name": "تاريخ انتهاء المشروع", "type": "date", "required": True},
                            {"name": "المراحل الرئيسية", "type": "text", "required": True}
                        ]
                    }
                ]
            },
            "it": {
                "title": "نموذج مناقصة تقنية معلومات",
                "sections": [
                    {
                        "name": "معلومات عامة",
                        "fields": [
                            {"name": "عنوان المناقصة", "type": "text", "required": True},
                            {"name": "وصف المشروع", "type": "text", "required": True},
                            {"name": "المدة", "type": "number", "unit": "شهر", "required": True},
                            {"name": "الميزانية التقديرية", "type": "number", "unit": "ريال", "required": False}
                        ]
                    },
                    {
                        "name": "متطلبات فنية",
                        "fields": [
                            {"name": "نوع النظام", "type": "select", "options": ["تطبيق ويب", "تطبيق جوال", "نظام ERP", "أخرى"], "required": True},
                            {"name": "التقنيات المطلوبة", "type": "text", "required": True},
                            {"name": "عدد المستخدمين", "type": "number", "required": True},
                            {"name": "متطلبات الأمان", "type": "text", "required": True},
                            {"name": "متطلبات الأداء", "type": "text", "required": True}
                        ]
                    },
                    {
                        "name": "متطلبات المحتوى المحلي",
                        "fields": [
                            {"name": "نسبة المحتوى المحلي", "type": "number", "unit": "%", "required": True},
                            {"name": "نسبة توطين الوظائف", "type": "number", "unit": "%", "required": True}
                        ]
                    },
                    {
                        "name": "الجدول الزمني",
                        "fields": [
                            {"name": "تاريخ بدء المشروع", "type": "date", "required": True},
                            {"name": "تاريخ انتهاء المشروع", "type": "date", "required": True},
                            {"name": "مراحل التطوير", "type": "text", "required": True}
                        ]
                    }
                ]
            },
            "general": {
                "title": "نموذج مناقصة عامة",
                "sections": [
                    {
                        "name": "معلومات عامة",
                        "fields": [
                            {"name": "عنوان المناقصة", "type": "text", "required": True},
                            {"name": "وصف المشروع", "type": "text", "required": True},
                            {"name": "المدة", "type": "number", "unit": "شهر", "required": True},
                            {"name": "الميزانية التقديرية", "type": "number", "unit": "ريال", "required": False}
                        ]
                    },
                    {
                        "name": "متطلبات المشروع",
                        "fields": [
                            {"name": "المتطلبات الفنية", "type": "text", "required": True},
                            {"name": "المتطلبات الإدارية", "type": "text", "required": True},
                            {"name": "المتطلبات المالية", "type": "text", "required": True}
                        ]
                    },
                    {
                        "name": "متطلبات المحتوى المحلي",
                        "fields": [
                            {"name": "نسبة المحتوى المحلي", "type": "number", "unit": "%", "required": True}
                        ]
                    },
                    {
                        "name": "الجدول الزمني",
                        "fields": [
                            {"name": "تاريخ بدء المشروع", "type": "date", "required": True},
                            {"name": "تاريخ انتهاء المشروع", "type": "date", "required": True}
                        ]
                    }
                ]
            }
        }
    
    def load_risk_templates(self) -> Dict[str, Any]:
        """
        تحميل قوالب المخاطر
        
        المخرجات:
        --------
        Dict[str, Any]
            قوالب المخاطر المختلفة
        """
        # في التطبيق الفعلي، ستُحمل القوالب من ملفات
        # هنا نستخدم قوالب افتراضية للتوضيح
        return {
            "construction": [
                {
                    "id": "C001",
                    "title": "تأخير في الحصول على التصاريح",
                    "description": "تأخير في الحصول على التصاريح والموافقات اللازمة من الجهات المختصة",
                    "probability": "متوسطة",
                    "impact": "عالي",
                    "mitigation": [
                        "البدء في إجراءات الحصول على التصاريح مبكراً",
                        "التنسيق المستمر مع الجهات المختصة",
                        "الاستعانة بمستشارين متخصصين"
                    ]
                },
                {
                    "id": "C002",
                    "title": "ارتفاع أسعار مواد البناء",
                    "description": "ارتفاع غير متوقع في أسعار مواد البناء الرئيسية",
                    "probability": "عالية",
                    "impact": "عالي",
                    "mitigation": [
                        "تضمين بند تعديل الأسعار في العقود",
                        "شراء المواد الرئيسية مسبقاً",
                        "البحث عن موردين بديلين"
                    ]
                },
                {
                    "id": "C003",
                    "title": "نقص العمالة الماهرة",
                    "description": "عدم توفر العمالة الماهرة بالعدد المطلوب",
                    "probability": "متوسطة",
                    "impact": "متوسط",
                    "mitigation": [
                        "التعاقد المسبق مع مقاولي الباطن",
                        "توفير برامج تدريب للعمالة",
                        "زيادة الحوافز للعمالة الماهرة"
                    ]
                }
            ],
            "it": [
                {
                    "id": "IT001",
                    "title": "تغيير متطلبات المشروع",
                    "description": "تغييرات متكررة في متطلبات المشروع خلال مرحلة التطوير",
                    "probability": "عالية",
                    "impact": "عالي",
                    "mitigation": [
                        "توثيق المتطلبات بشكل دقيق والحصول على موافقة العميل",
                        "استخدام منهجية مرنة للتطوير",
                        "تحديد إجراءات واضحة لإدارة التغييرات"
                    ]
                },
                {
                    "id": "IT002",
                    "title": "مشاكل في تكامل الأنظمة",
                    "description": "صعوبات في تكامل النظام الجديد مع الأنظمة القائمة",
                    "probability": "متوسطة",
                    "impact": "عالي",
                    "mitigation": [
                        "إجراء دراسة تفصيلية للأنظمة القائمة",
                        "تطوير واجهات برمجة تطبيقات (APIs) قياسية",
                        "إجراء اختبارات تكامل شاملة"
                    ]
                },
                {
                    "id": "IT003",
                    "title": "مشاكل في أمن المعلومات",
                    "description": "ثغرات أمنية في النظام تؤدي إلى مخاطر أمنية",
                    "probability": "متوسطة",
                    "impact": "عالي",
                    "mitigation": [
                        "تطبيق معايير أمن المعلومات العالمية",
                        "إجراء اختبارات اختراق دورية",
                        "تطوير خطة استجابة للحوادث الأمنية"
                    ]
                }
            ],
            "general": [
                {
                    "id": "G001",
                    "title": "تجاوز الميزانية",
                    "description": "تجاوز الميزانية المخصصة للمشروع",
                    "probability": "متوسطة",
                    "impact": "عالي",
                    "mitigation": [
                        "وضع ميزانية واقعية مع احتياطي كافٍ",
                        "مراقبة التكاليف بشكل مستمر",
                        "تحديد بنود التكاليف الرئيسية ومراقبتها"
                    ]
                },
                {
                    "id": "G002",
                    "title": "تأخير في الجدول الزمني",
                    "description": "تأخير في تنفيذ المشروع وفق الجدول الزمني المحدد",
                    "probability": "عالية",
                    "impact": "متوسط",
                    "mitigation": [
                        "وضع جدول زمني واقعي مع احتياطي كافٍ",
                        "مراقبة التقدم بشكل مستمر",
                        "تحديد المسار الحرج وإعطاؤه الأولوية"
                    ]
                },
                {
                    "id": "G003",
                    "title": "مشاكل في جودة المنتج/الخدمة",
                    "description": "عدم مطابقة المنتج أو الخدمة للمواصفات المطلوبة",
                    "probability": "متوسطة",
                    "impact": "عالي",
                    "mitigation": [
                        "تحديد معايير الجودة بوضوح",
                        "إجراء اختبارات جودة دورية",
                        "تطبيق نظام إدارة الجودة"
                    ]
                }
            ]
        }
    
    def load_local_content_templates(self) -> Dict[str, Any]:
        """
        تحميل قوالب المحتوى المحلي
        
        المخرجات:
        --------
        Dict[str, Any]
            قوالب المحتوى المحلي المختلفة
        """
        # في التطبيق الفعلي، ستُحمل القوالب من ملفات
        # هنا نستخدم قوالب افتراضية للتوضيح
        return {
            "construction": {
                "min_percentage": 30,
                "sections": [
                    {
                        "name": "المواد والمنتجات",
                        "weight": 0.5,
                        "items": [
                            {"name": "الحديد", "local_alternatives": ["حديد السعودية", "حديد الراجحي", "حديد صلب"]},
                            {"name": "الأسمنت", "local_alternatives": ["أسمنت اليمامة", "أسمنت السعودية", "أسمنت الراجحي"]},
                            {"name": "الخرسانة", "local_alternatives": ["الخرسانة السعودية", "خرسانة البناء", "الخرسانة المسلحة"]},
                            {"name": "البلاط", "local_alternatives": ["بلاط وطني", "بلاط السلطان", "بلاط الفخار"]}
                        ]
                    },
                    {
                        "name": "القوى العاملة",
                        "weight": 0.3,
                        "target_percentage": 50,
                        "categories": [
                            {"name": "المهندسون", "target_percentage": 70},
                            {"name": "الفنيون", "target_percentage": 50},
                            {"name": "العمال", "target_percentage": 30}
                        ]
                    },
                    {
                        "name": "المقاولون والموردون",
                        "weight": 0.2,
                        "target_percentage": 60
                    }
                ]
            },
            "it": {
                "min_percentage": 25,
                "sections": [
                    {
                        "name": "البرمجيات والتراخيص",
                        "weight": 0.4,
                        "items": [
                            {"name": "أنظمة التشغيل", "local_alternatives": []},
                            {"name": "قواعد البيانات", "local_alternatives": []},
                            {"name": "برمجيات التطوير", "local_alternatives": []}
                        ]
                    },
                    {
                        "name": "الأجهزة والعتاد",
                        "weight": 0.2,
                        "items": [
                            {"name": "الخوادم", "local_alternatives": ["تجميع محلي"]},
                            {"name": "أجهزة الحاسب", "local_alternatives": ["تجميع محلي"]},
                            {"name": "أجهزة الشبكات", "local_alternatives": []}
                        ]
                    },
                    {
                        "name": "القوى العاملة",
                        "weight": 0.4,
                        "target_percentage": 70,
                        "categories": [
                            {"name": "المهندسون والمطورون", "target_percentage": 80},
                            {"name": "المحللون", "target_percentage": 90},
                            {"name": "الدعم الفني", "target_percentage": 100}
                        ]
                    }
                ]
            },
            "general": {
                "min_percentage": 20,
                "sections": [
                    {
                        "name": "المواد والمنتجات",
                        "weight": 0.4
                    },
                    {
                        "name": "القوى العاملة",
                        "weight": 0.4,
                        "target_percentage": 60
                    },
                    {
                        "name": "المقاولون والموردون",
                        "weight": 0.2,
                        "target_percentage": 50
                    }
                ]
            }
        }
    
    def save_template(self, template_type: str, template_name: str, template_data: Dict[str, Any]) -> bool:
        """
        حفظ قالب جديد أو تحديث قالب موجود
        
        المعاملات:
        ----------
        template_type : str
            نوع القالب (tender, risk, local_content)
        template_name : str
            اسم القالب
        template_data : Dict[str, Any]
            بيانات القالب
            
        المخرجات:
        --------
        bool
            نجاح أو فشل العملية
        """
        try:
            # التحقق من وجود المجلد الخاص بنوع القالب وإنشائه إذا لم يكن موجوداً
            type_path = os.path.join(self.templates_path, template_type)
            os.makedirs(type_path, exist_ok=True)
            
            # حفظ القالب في ملف JSON
            file_path = os.path.join(type_path, f"{template_name}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=4)
            
            return True
        except Exception as e:
            print(f"Error saving template: {str(e)}")
            return Falseإنشاء مبنى إداري من 4 طوابق بمساحة 2000 متر مربع في مدينة الرياض",
                "vector": np.random.rand(384).tolist(),  # تمثيل المتجه كقائمة
                "metadata": {
                    "sector": "الإنشاءات",
                    "location": "الرياض",
                    "date": "2023-05-15"
                }
            },
            "tender2": {
                "text": "مناقصة ل