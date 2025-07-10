"""
Configuration settings for Performance Email Generator
"""

import os
from pathlib import Path

class Config:
    """Configuration class for email generator settings"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent
    PDF_DIR = BASE_DIR / "reports_pdfs"
    CONVICTIONS_FILE = BASE_DIR / "convictions" / "model_convictions.xlsx"
    TEMPLATE_FILE = BASE_DIR / "templates" / "email_template.txt"
    OUTPUT_DIR = BASE_DIR / "output" / "emails"
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"
    OPENAI_TEMPERATURE = 0.3
    
    # Email generation settings
    MAX_CONVICTIONS = 3
    LOG_LEVEL = "INFO"
    
    # PDF parsing settings
    PDF_PAGES_TO_PARSE = [1, 2, 3]  # Pages 2, 3, 4 (0-indexed)
    
    @classmethod
    def validate(cls):
        """Validate configuration settings"""
        issues = []
        
        if not cls.TEMPLATE_FILE.exists():
            issues.append(f"Email template not found: {cls.TEMPLATE_FILE}")
        
        if cls.OPENAI_API_KEY is None:
            issues.append("OPENAI_API_KEY environment variable not set")
        
        return issues