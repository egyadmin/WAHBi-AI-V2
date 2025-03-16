"""
محمّل النماذج
يقوم بتحميل وإدارة نماذج الذكاء الاصطناعي المستخدمة في النظام
"""

import os
import logging
import torch
import gc
from typing import Dict, Any, Optional, Union, List
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelLoader:
    """
    محمّل النماذج
    """
    
    def __init__(self, config=None, use_gpu=True):
        """
        تهيئة محمّل النماذج
        
        المعاملات:
        ----------
        config : Dict, optional
            إ