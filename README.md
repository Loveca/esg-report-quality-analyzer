# ESG报告质量分析工具

这是一个用于分析企业ESG（环境、社会和治理）报告质量的Python工具。该工具可以自动分析ESG报告中的关键要素，包括标准遵循情况、第三方鉴证和量化指标等，帮助评估ESG报告的质量和完整性。

## 功能特点

- 支持PDF和TXT格式的ESG报告分析
- 自动检测报告是否遵循主要ESG报告标准（如GRI、SASB、TCFD等）
- 识别第三方鉴证和独立验证的存在
- 分析报告中量化指标的使用情况
- 生成综合评分和详细分析报告
- 支持批量处理多个报告文件
- 提供详细的日志记录和错误追踪

## 安装说明

1. 克隆仓库：
```bash
git clone [repository-url]
cd [repository-name]
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 分析单个报告

```python
from esg_quality_analyzer import ESGQualityAnalyzer

analyzer = ESGQualityAnalyzer()
results = analyzer.analyze_report("path/to/your/report.pdf")

# 查看分析结果
print(f"标准遵循得分: {results['standards_compliance']}")
print(f"第三方鉴证得分: {results['third_party_assurance']}")
print(f"量化指标得分: {results['quantitative_metrics']}")
print(f"总分: {results['total_score']}")
```

### 批量分析报告

使用`esg_panel_analyzer.py`进行批量分析：

```bash
python esg_panel_analyzer.py
```

分析结果将保存在以下文件中：
- `esg_panel_data_[timestamp].csv`：包含所有成功分析的报告数据
- `failed_files_[timestamp].csv`：记录处理失败的文件
- `esg_analysis_[timestamp].log`：详细的处理日志

## 评分标准

工具从以下三个维度评估ESG报告质量：

1. **标准遵循（Standards Compliance）**
   - 检查报告是否遵循主要ESG报告标准
   - 包括GRI、SASB、TCFD、ISSB、CSRD等

2. **第三方鉴证（Third-party Assurance）**
   - 检查是否存在独立的第三方验证
   - 包括审计报告、鉴证声明等

3. **量化指标（Quantitative Metrics）**
   - 检查报告中是否包含具体的量化数据
   - 包括环境指标、社会指标等

每个维度得分范围为0-1，总分范围为0-3。

## 注意事项

- 确保报告文件格式正确（PDF或TXT）
- 建议使用UTF-8编码的文本文件
- 对于PDF文件，确保文本可以被正确提取
- 批量处理时注意文件命名格式：`股票代码-年份-公司名称.txt`

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目。在提交代码之前，请确保：

1. 代码符合PEP 8规范
2. 添加适当的注释和文档
3. 更新测试用例（如果有）
4. 更新requirements.txt（如果添加了新的依赖）

## 许可证

本项目采用MIT许可证。详见[LICENSE](LICENSE)文件。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue
- 发送邮件至：[your-email]

## 致谢

感谢所有为本项目做出贡献的开发者。 