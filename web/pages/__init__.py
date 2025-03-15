# هذا الملف يجعل مجلد pages وحدة Python
# يمكن استخدامه لاستيراد الدوال المهمة لجعلها متاحة بشكل مباشر

from .home import show_home_page

__all__ = ['show_home_page']