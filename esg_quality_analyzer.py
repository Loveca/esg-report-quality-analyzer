import PyPDF2
import re
from pathlib import Path

class ESGQualityAnalyzer:
    def __init__(self):
        self.standards_keywords = [
            # 标准名称 (英文)
            "GRI", "Global Reporting Initiative",
            "SASB", "Sustainability Accounting Standards Board",
            "TCFD", "Task Force on Climate-Related Financial Disclosures",
            "ISSB", "International Sustainability Standards Board",
            "CSRD", "Corporate Sustainability Reporting Directive",
            "SDGs", "Sustainable Development Goals",
            # 标准名称 (中文)
            "全球报告倡议", "可持续发展会计准则", "气候相关财务披露",
            "国际可持续发展准则", "欧盟企业可持续发展报告指令"
        ]
        
        self.assurance_keywords = [
            "第三方鉴证", "独立验证", "外部审计", "独立保证", "独立鉴证报告",
            "第三方鉴证", "独立核验", "外部鉴证", "外部核验", "assured by",
            "verified by", "独立审计师报告", "assurance", "third-party verification",
            "independent audit"
        ]
        
        self.quantitative_units = ["吨", "%", "千瓦时", "立方米", "小时", "人次", "元"]
        self.kpi_keywords = [
            "关键绩效指标", "环境绩效数据", "社会绩效数据", "可持续发展表现",
            "ESG 数据", "绩效指标一览", "核心指标", "KPI"
        ]

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file."""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {str(e)}")
            return ""
        return text

    def check_standards_compliance(self, text):
        """Check if report follows sustainability reporting standards."""
        text = text.lower()
        for keyword in self.standards_keywords:
            if keyword.lower() in text:
                return 1
        return 0

    def check_third_party_assurance(self, text):
        """Check if report has third-party assurance."""
        text = text.lower()
        for keyword in self.assurance_keywords:
            if keyword.lower() in text:
                return 1
        return 0

    def check_quantitative_metrics(self, text):
        """Check if report contains quantitative metrics."""
        # Rule 1: Check for numbers followed by units
        for unit in self.quantitative_units:
            pattern = r'\d+(\.\d+)?\s*' + unit
            if re.search(pattern, text):
                return 1

        # Rule 2: Check for KPI keywords in section titles
        # Look for keywords followed by newlines or at the start of lines
        for keyword in self.kpi_keywords:
            pattern = r'^' + keyword + r'|[\n]' + keyword
            if re.search(pattern, text, re.MULTILINE):
                return 1

        return 0

    def analyze_report(self, pdf_path):
        """Analyze ESG report quality."""
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return None

        standards_score = self.check_standards_compliance(text)
        assurance_score = self.check_third_party_assurance(text)
        metrics_score = self.check_quantitative_metrics(text)
        
        total_score = standards_score + assurance_score + metrics_score

        return {
            'standards_compliance': standards_score,
            'third_party_assurance': assurance_score,
            'quantitative_metrics': metrics_score,
            'total_score': total_score
        }

def main():
    analyzer = ESGQualityAnalyzer()
    reports_dir = Path("报告样本")
    
    for pdf_file in reports_dir.glob("*.pdf"):
        print(f"\nAnalyzing {pdf_file.name}:")
        results = analyzer.analyze_report(pdf_file)
        
        if results:
            print(f"Standards Compliance: {results['standards_compliance']}")
            print(f"Third-party Assurance: {results['third_party_assurance']}")
            print(f"Quantitative Metrics: {results['quantitative_metrics']}")
            print(f"Total Score: {results['total_score']}")
        else:
            print("Failed to analyze the report")

if __name__ == "__main__":
    main() 