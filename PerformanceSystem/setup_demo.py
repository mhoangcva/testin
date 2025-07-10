#!/usr/bin/env python3
"""
Demo Setup Script for Performance Email Generator
Creates sample data and demonstrates the system functionality
"""

import os
import pandas as pd
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_sample_data():
    """Create comprehensive sample data for demonstration"""
    
    base_dir = Path("PerformanceSystem")
    
    # 1. Create sample conviction data
    logger.info("Creating sample convictions data...")
    convictions_data = {
        'Model': [
            'US Large Cap Growth',
            'Technology Sector Focus', 
            'International Developed Markets',
            'Fixed Income Core',
            'Real Estate Investment Trusts',
            'Small Cap Value',
            'Commodities & Energy',
            'Emerging Markets'
        ],
        'YTD%': [15.2, 12.5, 8.3, 4.1, 9.7, 6.8, 11.3, -2.1],
        'Commentary': [
            'Leading innovation companies showing robust earnings growth with strong balance sheets',
            'AI and cloud infrastructure investments driving exceptional performance this quarter',
            'Benefiting from currency stabilization and European economic recovery trends',
            'Stable returns providing portfolio ballast in volatile market environment',
            'Solid dividend yields with capital appreciation in commercial real estate recovery',
            'Attractive valuations in quality small-cap names with strong fundamentals',
            'Energy transition and commodity supercycle themes creating long-term value',
            'Temporary headwinds from geopolitical concerns, positioned for recovery'
        ]
    }
    
    conv_df = pd.DataFrame(convictions_data)
    conv_file = base_dir / "convictions" / "model_convictions.xlsx"
    conv_file.parent.mkdir(parents=True, exist_ok=True)
    conv_df.to_excel(conv_file, index=False)
    logger.info(f"Created convictions file: {conv_file}")
    
    # 2. Create sample PDF placeholders with realistic content
    logger.info("Creating sample PDF placeholders...")
    pdf_dir = base_dir / "reports_pdfs"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    sample_clients = [
        "John_Smith",
        "Sarah_Johnson", 
        "Michael_Brown",
        "Emily_Davis",
        "Robert_Wilson",
        "Jennifer_Taylor",
        "David_Anderson",
        "Lisa_Martinez",
        "James_Wilson",
        "Maria_Garcia"
    ]
    
    for i, client in enumerate(sample_clients):
        # Create realistic sample PDF content
        ytd_return = round(5.5 + (i * 1.2), 1)
        inception_return = round(8.2 + (i * 0.8), 1)
        sharpe_ratio = round(1.1 + (i * 0.05), 2)
        
        sample_content = f"""
        PERFORMANCE REPORT
        Client: {client.replace('_', ' ')}
        
        PERFORMANCE SUMMARY
        YTD Return: {ytd_return}%
        Rolling 12-Month: {ytd_return + 2.1}%
        Since Inception Return: {inception_return}%
        
        RISK METRICS
        Sharpe Ratio: {sharpe_ratio}
        Beta: 0.{85 + i}
        Max Drawdown: -{3.2 + (i * 0.3)}%
        
        HOLDINGS & ALLOCATIONS
        Equity: {60 + i}%
        Fixed Income: {25 - (i * 0.5)}%
        Alternatives: {15 - (i * 0.5)}%
        """
        
        pdf_path = pdf_dir / f"{client}.pdf"
        with open(pdf_path, 'w') as f:
            f.write(sample_content)
    
    logger.info(f"Created {len(sample_clients)} sample PDF files")
    
    # 3. Update email template with better formatting
    logger.info("Creating enhanced email template...")
    template_content = """Hi {Name},

I hope this message finds you well. Here's your portfolio performance update:

📊 **Portfolio Performance Summary:**
• YTD return: {YTD}
• Cumulative since inception: {SinceInception}
• Current Sharpe Ratio: {Sharpe}

🎯 **Our Highest Conviction Views Driving This Strategy:**
{Convictions}

📈 **Market Commentary:**
Your portfolio continues to benefit from our strategic positioning across our core conviction themes. The performance metrics above reflect our disciplined approach to risk management while capitalizing on market opportunities that align with our investment philosophy.

The current market environment presents both challenges and opportunities. We remain focused on quality companies with strong fundamentals and are well-positioned for the evolving economic landscape.

📋 **Next Steps:**
I've attached your full performance report with detailed breakdowns of holdings, allocations, and risk metrics. Please review at your convenience, and let me know if you'd like to schedule a call to discuss:

• Portfolio positioning and any adjustments
• Market outlook and investment strategy
• Any questions about your investment goals

As always, I'm here to help guide your investment journey and ensure your portfolio remains aligned with your objectives.

Best regards,
[Your Name]
[Your Title]
[Contact Information]

---
This email was generated using our automated performance reporting system.
"""
    
    template_file = base_dir / "templates" / "email_template.txt"
    template_file.parent.mkdir(parents=True, exist_ok=True)
    with open(template_file, 'w') as f:
        f.write(template_content)
    
    logger.info(f"Created email template: {template_file}")
    
    # 4. Create output directory
    output_dir = base_dir / "output" / "emails"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("✅ Sample data creation complete!")
    return base_dir

def run_demo():
    """Run a complete demonstration of the system"""
    logger.info("🚀 Starting Performance Email Generator Demo")
    
    # Create sample data
    base_dir = create_sample_data()
    
    # Run the basic generator
    logger.info("Running basic email generator...")
    try:
        from performance_email_generator import PerformanceEmailGenerator
        
        generator = PerformanceEmailGenerator(str(base_dir))
        generator.process_all_reports()
        
        # Check results
        output_dir = base_dir / "output" / "emails"
        email_files = list(output_dir.glob("*.txt"))
        
        logger.info(f"✅ Generated {len(email_files)} email files")
        
        # Show sample email
        if email_files:
            sample_email = email_files[0]
            logger.info(f"\n📧 Sample Email ({sample_email.name}):")
            logger.info("=" * 50)
            with open(sample_email, 'r') as f:
                content = f.read()
                # Show first 500 characters
                print(content[:500] + "..." if len(content) > 500 else content)
            logger.info("=" * 50)
        
    except ImportError as e:
        logger.error(f"Error importing generator: {e}")
    except Exception as e:
        logger.error(f"Error running demo: {e}")
    
    logger.info("✨ Demo complete!")
    
    # Instructions for next steps
    next_steps = f"""
🔄 **Next Steps to Customize for Your Environment:**

1. **Replace Sample Data:**
   • Add your actual PDF files to: {base_dir / 'reports_pdfs'}
   • Update convictions in: {base_dir / 'convictions' / 'model_convictions.xlsx'}
   • Customize email template: {base_dir / 'templates' / 'email_template.txt'}

2. **Set Up OpenAI (Optional but Recommended):**
   • Set environment variable: export OPENAI_API_KEY="your-api-key"
   • Run enhanced_generator.py for AI-powered personalization

3. **Install Dependencies:**
   • pip install -r requirements.txt

4. **Production Deployment:**
   • Schedule the script to run monthly/quarterly
   • Set up email automation to send generated emails
   • Add monitoring and error handling for production use

Generated emails are saved in: {base_dir / 'output' / 'emails'}
    """
    
    print(next_steps)

if __name__ == "__main__":
    run_demo()