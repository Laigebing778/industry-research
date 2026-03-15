# -*- coding: utf-8 -*-
"""
财务分析智能体 v1.0

功能：
1. 财务指标计算与分析
2. 杜邦分析
3. 财务舞弊识别
4. 企业估值建模

作者：Emma
日期：2026-03-11
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class FinancialData:
    """财务数据结构"""
    # 资产负债表
    cash: float = 0                    # 现金
    accounts_receivable: float = 0     # 应收账款
    inventory: float = 0               # 存货
    prepaid: float = 0                 # 预付账款
    fixed_assets: float = 0            # 固定资产
    total_assets: float = 0            # 总资产

    accounts_payable: float = 0        # 应付账款
    advance_from_customers: float = 0  # 预收账款
    short_term_debt: float = 0         # 短期借款
    long_term_debt: float = 0          # 长期借款
    total_liabilities: float = 0       # 总负债

    equity: float = 0                  # 所有者权益

    # 利润表
    revenue: float = 0                 # 营业收入
    cost: float = 0                    # 营业成本
    operating_expense: float = 0       # 费用
    operating_profit: float = 0        # 营业利润
    interest: float = 0                # 利息支出
    income_tax: float = 0              # 所得税
    net_profit: float = 0              # 净利润

    # 现金流量表
    operating_cash_flow: float = 0     # 经营现金流
    investing_cash_flow: float = 0     # 投资现金流
    financing_cash_flow: float = 0     # 融资现金流


class FinancialAnalysisAgent:
    """财务分析智能体"""

    def __init__(self):
        self.name = "财务分析师"
        self.version = "1.0"

    # ==================== 财务指标计算 ====================

    def calculate_profitability(self, data: FinancialData) -> Dict:
        """计算盈利能力指标"""
        return {
            "ROE": self._safe_divide(data.net_profit, data.equity),
            "ROA": self._safe_divide(data.net_profit, data.total_assets),
            "销售净利率": self._safe_divide(data.net_profit, data.revenue),
            "销售毛利率": self._safe_divide(data.revenue - data.cost, data.revenue),
            "营业利润率": self._safe_divide(data.operating_profit, data.revenue),
        }

    def calculate_operation(self, data: FinancialData) -> Dict:
        """计算营运能力指标"""
        return {
            "应收账款周转率": self._safe_divide(data.revenue, data.accounts_receivable),
            "存货周转率": self._safe_divide(data.cost, data.inventory),
            "总资产周转率": self._safe_divide(data.revenue, data.total_assets),
        }

    def calculate_solvency(self, data: FinancialData) -> Dict:
        """计算偿债能力指标"""
        current_assets = data.cash + data.accounts_receivable + data.inventory + data.prepaid
        quick_assets = data.cash + data.accounts_receivable
        current_liabilities = data.accounts_payable + data.short_term_debt

        return {
            "资产负债率": self._safe_divide(data.total_liabilities, data.total_assets),
            "流动比率": self._safe_divide(current_assets, current_liabilities),
            "速动比率": self._safe_divide(quick_assets, current_liabilities),
        }

    def calculate_growth(self, current: FinancialData, previous: FinancialData) -> Dict:
        """计算成长性指标"""
        return {
            "营收增长率": self._safe_divide(current.revenue - previous.revenue, previous.revenue),
            "净利润增长率": self._safe_divide(current.net_profit - previous.net_profit, previous.net_profit),
            "总资产增长率": self._safe_divide(current.total_assets - previous.total_assets, previous.total_assets),
        }

    # ==================== 杜邦分析 ====================

    def dupont_analysis(self, data: FinancialData) -> Dict:
        """杜邦分析"""
        # ROE = 净利润/净资产 = 净利润率 × 资产周转率 × 权益乘数
        net_profit_margin = self._safe_divide(data.net_profit, data.revenue)
        asset_turnover = self._safe_divide(data.revenue, data.total_assets)
        equity_multiplier = self._safe_divide(data.total_assets, data.equity)
        roe = net_profit_margin * asset_turnover * equity_multiplier

        return {
            "ROE": roe,
            "分解": {
                "销售净利率": net_profit_margin,
                "资产周转率": asset_turnover,
                "权益乘数": equity_multiplier,
            },
            "分析": self._interpret_dupont(net_profit_margin, asset_turnover, equity_multiplier)
        }

    def _interpret_dupont(self, npm: float, at: float, em: float) -> str:
        """解读杜邦分析结果"""
        if npm > 0.15 and at < 1:
            return "高利润率-低周转率模式：可能具有技术垄断或品牌溢价，如高端制造业"
        elif npm < 0.1 and at > 1.5:
            return "低利润率-高周转率模式：通过高效运营和成本控制获利，如零售业"
        elif em > 3:
            return "高杠杆模式：财务风险较高，需关注偿债能力"
        else:
            return "均衡模式：各项指标较为平衡"

    # ==================== 财务舞弊识别 ====================

    def fraud_detection(self, data: FinancialData) -> Dict:
        """财务舞弊识别"""
        warnings = []
        risk_score = 0

        # 1. 利润与现金流背离
        if data.net_profit > 0 and data.operating_cash_flow < 0:
            warnings.append("[警告] 净利润为正但经营现金流为负，利润质量存疑")
            risk_score += 20

        # 2. 应收账款异常
        if data.accounts_receivable > 0:
            ar_turnover = self._safe_divide(data.revenue, data.accounts_receivable)
            if ar_turnover < 3:  # 周转率低于3次
                warnings.append(f"[警告] 应收账款周转率仅{ar_turnover:.1f}次，回款速度慢")
                risk_score += 15

        # 3. 存货异常
        if data.inventory > 0:
            inv_turnover = self._safe_divide(data.cost, data.inventory)
            if inv_turnover < 2:  # 周转率低于2次
                warnings.append(f"[警告] 存货周转率仅{inv_turnover:.1f}次，存货积压风险")
                risk_score += 15

        # 4. 毛利率异常高
        gross_margin = self._safe_divide(data.revenue - data.cost, data.revenue)
        if gross_margin > 0.5:
            warnings.append(f"[警告] 毛利率{gross_margin:.1%}较高，需验证持续性")
            risk_score += 10

        # 5. 其他应收款占比
        other_receivables = data.total_assets - data.cash - data.accounts_receivable - data.inventory - data.fixed_assets
        other_ratio = self._safe_divide(other_receivables, data.total_assets)
        if other_ratio > 0.1:
            warnings.append(f"[警告] 其他应收款占资产{other_ratio:.1%}，可能存在关联方占用")
            risk_score += 15

        return {
            "风险评分": min(risk_score, 100),
            "风险等级": self._get_risk_level(risk_score),
            "预警信号": warnings if warnings else ["[正常] 未发现明显舞弊信号"]
        }

    def _get_risk_level(self, score: float) -> str:
        """风险等级判定"""
        if score >= 60:
            return "高风险"
        elif score >= 30:
            return "中风险"
        else:
            return "低风险"

    # ==================== 企业估值 ====================

    def pe_valuation(self, net_profit: float, pe_ratio: float) -> Dict:
        """PE估值法"""
        market_cap = net_profit * pe_ratio
        return {
            "估值方法": "PE估值",
            "净利润": net_profit,
            "PE倍数": pe_ratio,
            "估值结果": market_cap,
            "说明": f"假设PE={pe_ratio}倍，企业价值={market_cap:.2f}亿元"
        }

    def pb_valuation(self, equity: float, pb_ratio: float) -> Dict:
        """PB估值法"""
        market_cap = equity * pb_ratio
        return {
            "估值方法": "PB估值",
            "净资产": equity,
            "PB倍数": pb_ratio,
            "估值结果": market_cap,
            "说明": f"假设PB={pb_ratio}倍，企业价值={market_cap:.2f}亿元"
        }

    def dcf_valuation(self, fcf_list: List[float], wacc: float,
                      terminal_growth: float = 0.03) -> Dict:
        """DCF估值法"""
        # 计算预测期现金流现值
        pv_fcf = sum(fcf / (1 + wacc) ** (i + 1) for i, fcf in enumerate(fcf_list))

        # 计算终值
        terminal_fcf = fcf_list[-1] * (1 + terminal_growth)
        terminal_value = terminal_fcf / (wacc - terminal_growth)
        pv_terminal = terminal_value / (1 + wacc) ** len(fcf_list)

        enterprise_value = pv_fcf + pv_terminal

        return {
            "估值方法": "DCF估值",
            "预测期现金流现值": pv_fcf,
            "终值现值": pv_terminal,
            "企业价值": enterprise_value,
            "参数": {
                "WACC": wacc,
                "永续增长率": terminal_growth
            }
        }

    # ==================== 综合分析 ====================

    def comprehensive_analysis(self, data: FinancialData) -> Dict:
        """综合财务分析"""
        return {
            "盈利能力": self.calculate_profitability(data),
            "营运能力": self.calculate_operation(data),
            "偿债能力": self.calculate_solvency(data),
            "杜邦分析": self.dupont_analysis(data),
            "舞弊风险": self.fraud_detection(data),
        }

    # ==================== 工具函数 ====================

    def _safe_divide(self, numerator: float, denominator: float) -> float:
        """安全除法"""
        if denominator == 0:
            return 0
        return numerator / denominator

    def format_report(self, analysis: Dict) -> str:
        """格式化分析报告"""
        report = []
        report.append("=" * 60)
        report.append("财务分析报告")
        report.append("=" * 60)

        for section, data in analysis.items():
            report.append(f"\n【{section}】")
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, float):
                        report.append(f"  {key}: {value:.2%}" if value < 1 else f"  {key}: {value:.2f}")
                    else:
                        report.append(f"  {key}: {value}")
            else:
                report.append(f"  {data}")

        return "\n".join(report)


# ==================== 主程序 ====================

def main():
    """演示程序"""
    print("=" * 60)
    print("财务分析智能体 v1.0")
    print("=" * 60)

    agent = FinancialAnalysisAgent()

    # 示例数据
    data = FinancialData(
        # 资产负债表（单位：亿元）
        cash=50,
        accounts_receivable=30,
        inventory=20,
        prepaid=5,
        fixed_assets=100,
        total_assets=250,
        accounts_payable=25,
        short_term_debt=30,
        long_term_debt=50,
        total_liabilities=125,
        equity=125,
        # 利润表
        revenue=200,
        cost=120,
        operating_expense=30,
        operating_profit=50,
        interest=5,
        income_tax=10,
        net_profit=35,
        # 现金流量表
        operating_cash_flow=40,
    )

    # 综合分析
    analysis = agent.comprehensive_analysis(data)
    print(agent.format_report(analysis))

    # 估值示例
    print("\n" + "=" * 60)
    print("估值分析")
    print("=" * 60)

    pe_result = agent.pe_valuation(35, 15)
    print(f"\nPE估值: {pe_result}")

    pb_result = agent.pb_valuation(125, 2)
    print(f"\nPB估值: {pb_result}")


if __name__ == "__main__":
    main()