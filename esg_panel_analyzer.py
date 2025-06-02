import os
import re
from pathlib import Path
import pandas as pd
from tqdm import tqdm
import logging
from datetime import datetime

class ESGPanelAnalyzer:
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
            "国际可持续发展准则", "欧盟企业可持续发展报告指令", "上市公司社会责任指引"
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

    def extract_text_from_txt(self, txt_path):
        """从txt文件中提取文本"""
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logging.error(f"读取文件 {txt_path} 时出错: {str(e)}")
            return ""

    def check_standards_compliance(self, text):
        """检查是否遵循可持续发展报告准则"""
        text = text.lower()
        for keyword in self.standards_keywords:
            if keyword.lower() in text:
                return 1
        return 0

    def check_third_party_assurance(self, text):
        """检查是否有第三方鉴证"""
        text = text.lower()
        for keyword in self.assurance_keywords:
            if keyword.lower() in text:
                return 1
        return 0

    def check_quantitative_metrics(self, text):
        """检查是否有量化指标"""
        # 规则1：检查数字后跟单位
        for unit in self.quantitative_units:
            pattern = r'\d+(\.\d+)?\s*' + unit
            if re.search(pattern, text):
                return 1

        # 规则2：检查章节标题中的KPI关键词
        for keyword in self.kpi_keywords:
            pattern = r'^' + keyword + r'|[\n]' + keyword
            if re.search(pattern, text, re.MULTILINE):
                return 1

        return 0

    def analyze_report(self, txt_path):
        """分析ESG报告质量"""
        text = self.extract_text_from_txt(txt_path)
        if not text:
            return None

        standards_score = self.check_standards_compliance(text)
        assurance_score = self.check_third_party_assurance(text)
        metrics_score = self.check_quantitative_metrics(text)
        
        total_score = standards_score + assurance_score + metrics_score

        return {
            'standards_score': standards_score,
            'assurance_score': assurance_score,
            'metrics_score': metrics_score,
            'total_score': total_score
        }

    def parse_filename(self, filename):
        """解析文件名获取股票代码和年份"""
        pattern = r'(\d{6})-(\d{4})-(.*?)\.txt'
        match = re.match(pattern, filename)
        if match:
            stock_code = match.group(1)
            year = int(match.group(2))
            company_name = match.group(3)
            return stock_code, year, company_name
        return None, None, None

def setup_logging():
    """设置日志"""
    log_filename = f'esg_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def main():
    # 设置日志
    setup_logging()
    logging.info("开始ESG报告分析")
    
    analyzer = ESGPanelAnalyzer()
    reports_dir = Path("社会责任报告文本（2006-2023年）")
    results = []
    failed_files = []

    # 获取所有txt文件
    txt_files = list(reports_dir.glob("*.txt"))
    logging.info(f"找到 {len(txt_files)} 个txt文件")

    # 使用tqdm创建进度条
    for txt_file in tqdm(txt_files, desc="分析报告", unit="文件"):
        try:
            stock_code, year, company_name = analyzer.parse_filename(txt_file.name)
            
            # 只处理2015-2023年的报告
            if year and 2015 <= year <= 2023:
                scores = analyzer.analyze_report(txt_file)
                if scores is not None:
                    results.append({
                        'stock_code': stock_code,
                        'company_name': company_name,
                        'year': year,
                        'standards_score': scores['standards_score'],
                        'assurance_score': scores['assurance_score'],
                        'metrics_score': scores['metrics_score'],
                        'total_score': scores['total_score']
                    })
                else:
                    failed_files.append({
                        'file': txt_file.name,
                        'reason': '分析失败'
                    })
            else:
                failed_files.append({
                    'file': txt_file.name,
                    'reason': '年份不在2015-2023范围内'
                })
        except Exception as e:
            logging.error(f"处理文件 {txt_file.name} 时出错: {str(e)}")
            failed_files.append({
                'file': txt_file.name,
                'reason': f'处理出错: {str(e)}'
            })

    # 创建结果DataFrame并保存为CSV
    if results:
        df = pd.DataFrame(results)
        df = df.sort_values(['stock_code', 'year'])
        output_file = f'esg_panel_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        logging.info(f"成功分析 {len(results)} 份报告")
        logging.info(f"结果已保存到 {output_file}")

    # 保存失败记录
    if failed_files:
        failed_df = pd.DataFrame(failed_files)
        failed_file = f'failed_files_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        failed_df.to_csv(failed_file, index=False, encoding='utf-8-sig')
        logging.warning(f"有 {len(failed_files)} 个文件处理失败")
        logging.warning(f"失败记录已保存到 {failed_file}")

    logging.info("分析完成")

if __name__ == "__main__":
    main()