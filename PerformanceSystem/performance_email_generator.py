#!/usr/bin/env python3
"""
Performance Report Email Generator
Automatically generates personalized client emails from PDF performance reports
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PerformanceEmailGenerator:
    """Main class for generating personalized performance emails"""
    
    def __init__(self, base_dir: str = "PerformanceSystem"):
        self.base_dir = Path(base_dir)
        self.pdf_dir = self.base_dir / "reports_pdfs"
        self.conv_file = self.base_dir / "convictions" / "model_convictions.xlsx"
        self.template_file = self.base_dir / "templates" / "email_template.txt"
        self.output_dir = self.base_dir / "output" / "emails"
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load components
        self.convictions_df = None
        self.email_template = None
        self._load_components()
    
    def _load_components(self):
        """Load convictions data and email template"""
        try:
            # Load convictions (create sample if doesn't exist)
            if not self.conv_file.exists():
                self._create_sample_convictions()
            
            self.convictions_df = pd.read_excel(self.conv_file)
            logger.info(f"Loaded {len(self.convictions_df)} conviction entries")
            
            # Load email template
            if self.template_file.exists():
                with open(self.template_file, 'r') as f:
                    self.email_template = f.read()
                logger.info("Email template loaded successfully")
            else:
                logger.error(f"Email template not found at {self.template_file}")
                
        except Exception as e:
            logger.error(f"Error loading components: {e}")
    
    def _create_sample_convictions(self):
        """Create sample convictions file if it doesn't exist"""
        logger.info("Creating sample convictions file...")
        
        conviction_data = {
            'Model': [
                'US Large Cap Growth',
                'International Developed Markets', 
                'Technology Sector Focus',
                'Fixed Income Core',
                'Emerging Markets',
                'Real Estate Investment Trusts',
                'Small Cap Value',
                'Commodities & Energy'
            ],
            'YTD%': [12.5, 8.3, 15.2, 4.1, -2.1, 9.7, 6.8, 11.3],
            'Commentary': [
                'Strong performance driven by AI and cloud infrastructure investments',
                'Benefiting from currency stabilization and economic recovery',
                'Leading innovation companies showing robust earnings growth', 
                'Stable returns in volatile market environment',
                'Temporary headwinds from geopolitical concerns',
                'Solid dividend yields with capital appreciation potential',
                'Attractive valuations in quality small-cap names',
                'Energy transition and commodity supercycle themes'
            ]
        }
        
        df = pd.DataFrame(conviction_data)
        self.conv_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(self.conv_file, index=False)
        logger.info(f"Sample convictions file created at {self.conv_file}")
    
    def parse_report(self, pdf_path: Path) -> Dict[str, str]:
        """
        Extract key metrics from PDF performance report
        This is a simplified version - you'll need to adapt based on your actual PDF structure
        """
        try:
            # For demo purposes, we'll simulate extracted data
            # In reality, you'd use pdfplumber or similar to extract from actual PDFs
            
            # Simulated extraction based on typical performance report structure
            sample_data = {
                "YTD": "8.5%",
                "SinceInception": "12.3%", 
                "Sharpe": "1.42",
                "Beta": "0.95",
                "MaxDrawdown": "-5.2%"
            }
            
            logger.info(f"Parsed report for {pdf_path.name}")
            return sample_data
            
        except Exception as e:
            logger.error(f"Error parsing {pdf_path}: {e}")
            return {}
    
    def get_top_convictions(self, n: int = 3) -> str:
        """Get top N convictions formatted for email"""
        if self.convictions_df is None:
            return "Conviction data not available"
        
        try:
            top_convs = self.convictions_df.nlargest(n, 'YTD%')
            conv_text = "\n".join([
                f"✅ {row['Model']}: {row['YTD%']}% — {row['Commentary']}"
                for _, row in top_convs.iterrows()
            ])
            return conv_text
        except Exception as e:
            logger.error(f"Error getting convictions: {e}")
            return "Error retrieving conviction data"
    
    def generate_email(self, client_name: str, metrics: Dict[str, str], convictions: str) -> str:
        """Generate personalized email using template and data"""
        if not self.email_template:
            return "Email template not available"
        
        try:
            # Fill in template placeholders
            email_content = self.email_template.format(
                Name=client_name,
                YTD=metrics.get("YTD", "N/A"),
                SinceInception=metrics.get("SinceInception", "N/A"),
                Sharpe=metrics.get("Sharpe", "N/A"),
                Convictions=convictions
            )
            
            return email_content
            
        except Exception as e:
            logger.error(f"Error generating email for {client_name}: {e}")
            return f"Error generating email: {e}"
    
    def process_all_reports(self):
        """Main orchestration method to process all PDF reports"""
        if not self.pdf_dir.exists():
            logger.error(f"PDF directory not found: {self.pdf_dir}")
            self._create_sample_pdfs()
            return
        
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.warning("No PDF files found. Creating sample structure...")
            self._create_sample_pdfs()
            return
        
        logger.info(f"Processing {len(pdf_files)} PDF reports...")
        
        # Get convictions once for all emails
        convictions_text = self.get_top_convictions(3)
        
        processed_count = 0
        for pdf_path in pdf_files:
            try:
                # Extract client name from filename
                client_name = pdf_path.stem.replace("_", " ").title()
                
                # Parse the PDF report
                metrics = self.parse_report(pdf_path)
                
                if not metrics:
                    logger.warning(f"No metrics extracted for {client_name}")
                    continue
                
                # Generate email
                email_content = self.generate_email(client_name, metrics, convictions_text)
                
                # Save email
                output_path = self.output_dir / f"{client_name}.txt"
                with open(output_path, 'w') as f:
                    f.write(email_content)
                
                logger.info(f"✅ Generated email for {client_name}")
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing {pdf_path.name}: {e}")
                continue
        
        logger.info(f"🎉 Successfully processed {processed_count} reports")
        self._generate_summary_report(processed_count)
    
    def _create_sample_pdfs(self):
        """Create sample PDF structure for demonstration"""
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        
        sample_clients = [
            "John_Smith.pdf",
            "Sarah_Johnson.pdf", 
            "Michael_Brown.pdf",
            "Emily_Davis.pdf",
            "Robert_Wilson.pdf"
        ]
        
        for client_file in sample_clients:
            sample_path = self.pdf_dir / client_file
            with open(sample_path, 'w') as f:
                f.write(f"Sample PDF placeholder for {client_file}")
        
        logger.info(f"Created {len(sample_clients)} sample PDF files for demonstration")
    
    def _generate_summary_report(self, processed_count: int):
        """Generate a summary report of the email generation process"""
        summary = f"""
Email Generation Summary Report
Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 Processing Statistics:
• Total emails generated: {processed_count}
• Conviction models used: {len(self.convictions_df) if self.convictions_df is not None else 0}
• Output directory: {self.output_dir}

📁 Files created in: {self.output_dir.absolute()}

🔄 Next Steps:
1. Review generated emails in the output folder
2. Add your actual PDF files to: {self.pdf_dir.absolute()}
3. Update convictions data in: {self.conv_file.absolute()}
4. Customize email template in: {self.template_file.absolute()}
5. Set up OpenAI API key for advanced personalization
        """
        
        summary_path = self.output_dir / "generation_summary.txt"
        with open(summary_path, 'w') as f:
            f.write(summary)
        
        logger.info(f"Summary report saved to {summary_path}")

def main():
    """Main execution function"""
    logger.info("🚀 Starting Performance Email Generator")
    
    generator = PerformanceEmailGenerator()
    generator.process_all_reports()
    
    logger.info("✨ Email generation complete!")

if __name__ == "__main__":
    main()