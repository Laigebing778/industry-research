# -*- coding: utf-8 -*-
"""
宏观经济分析智能体 v1.0

功能：
1. 宏观经济指标解读
2. 经济周期判断
3. 政策影响分析
4. 大类资产配置建议

作者：Emma
日期：2026-03-10
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# 知识库路径
KNOWLEDGE_BASE = r"D:\聪明的小C2.0\资产配置框架搭建\宏观经济智能体"

class MacroEconAgent:
    """宏观经济分析智能体"""

    def __init__(self):
        self.name = "宏观经济分析师"
        self.version = "1.0"
        self.knowledge = self._load_knowledge()

    def _load_knowledge(self) -> Dict:
        """加载知识库"""
        knowledge = {
            "indicators": self._get_indicator_definitions(),
            "cycles": self._get_cycle_definitions(),
            "policies": self._get_policy_tools(),
            "calendar": self._get_data_calendar(),
        }
        return knowledge

    def _get_indicator_definitions(self) -> Dict:
        """经济指标定义"""
        return {
            # 增长类指标
            "GDP": {
                "full_name": "国内生产总值",
                "formula": "C + I + G + (X-M)",
                "weight": {"消费": 55, "投资": 40, "净出口": 5},
                "release": "季度（首月15日左右）",
                "meaning": "衡量经济总量和增速的核心指标"
            },
            "工业增加值": {
                "full_name": "工业增加值",
                "release": "月度（次月15日左右）",
                "meaning": "反映工业生产活动景气度",
                "lead_lag": "同步指标"
            },
            "PMI": {
                "full_name": "采购经理指数",
                "release": "月度（当月1日/31日）",
                "meaning": "制造业景气度指标，50为荣枯线",
                "threshold": {"扩张": ">50", "收缩": "<50"}
            },
            # 通胀类指标
            "CPI": {
                "full_name": "消费者物价指数",
                "components": {"食品": 30, "非食品": 70},
                "release": "月度（次月10日左右）",
                "meaning": "衡量居民消费品价格变动"
            },
            "PPI": {
                "full_name": "生产者物价指数",
                "release": "月度（次月10日左右）",
                "meaning": "衡量工业品出厂价格变动",
                "lead_lag": "领先CPI 3-6个月"
            },
            # 货币类指标
            "M2": {
                "full_name": "广义货币供应量",
                "definition": "M1 + 定期存款 + 储蓄存款",
                "release": "月度（次月10-15日）",
                "meaning": "反映社会总购买力和潜在通胀压力"
            },
            "M1": {
                "full_name": "狭义货币供应量",
                "definition": "M0 + 企业活期存款",
                "meaning": "反映现实购买力"
            },
            "社融": {
                "full_name": "社会融资规模",
                "components": ["人民币贷款", "外币贷款", "委托贷款", "信托贷款",
                              "未贴现银行承兑汇票", "企业债券", "政府债券", "股票融资"],
                "meaning": "反映实体经济从金融体系获得的资金总额"
            },
            # 利率指标
            "10Y国债": {
                "full_name": "10年期国债收益率",
                "meaning": "无风险利率，资产定价锚",
                "influence": ["经济增长预期", "通胀预期", "货币政策", "海外利率"]
            },
            "DR007": {
                "full_name": "银行间存款类金融机构7天回购利率",
                "meaning": "反映银行间市场流动性松紧"
            }
        }

    def _get_cycle_definitions(self) -> Dict:
        """经济周期定义"""
        return {
            "美林时钟": {
                "复苏": {"经济": "↑", "通胀": "↓", "最佳资产": "股票"},
                "过热": {"经济": "↑", "通胀": "↑", "最佳资产": "商品"},
                "滞胀": {"经济": "↓", "通胀": "↑", "最佳资产": "现金"},
                "衰退": {"经济": "↓", "通胀": "↓", "最佳资产": "债券"}
            },
            "中国特色": {
                "传导链条": "政策周期 → 金融周期 → 经济周期 → 盈利周期",
                "政策领先": "3-6个月",
                "金融领先": "1-3个月"
            }
        }

    def _get_policy_tools(self) -> Dict:
        """政策工具"""
        return {
            "货币政策": {
                "价格型工具": ["OMO利率", "MLF利率", "LPR", "存款利率"],
                "数量型工具": ["降准", "MLF投放", "PSL", "再贷款"],
                "窗口指导": ["信贷额度", "地产信贷政策"]
            },
            "财政政策": {
                "收入端": ["减税降费", "缓税"],
                "支出端": ["专项债", "转移支付", "基建投资"],
                "赤字率": "目标赤字率反映财政发力程度"
            }
        }

    def _get_data_calendar(self) -> List[Dict]:
        """数据发布日历"""
        return [
            {"date": "每月1-10日", "data": ["PMI", "CPI", "PPI"]},
            {"date": "每月10-15日", "data": ["社融", "M2", "进出口"]},
            {"date": "每月15-20日", "data": ["工业增加值", "投资", "消费"]},
            {"date": "每季度首月", "data": ["GDP"]}
        ]

    def explain_indicator(self, indicator: str) -> Dict:
        """
        解读经济指标

        Args:
            indicator: 指标名称

        Returns:
            指标定义和解释
        """
        indicators = self.knowledge["indicators"]

        # 模糊匹配
        for key, value in indicators.items():
            if indicator in key or key in indicator:
                return {
                    "success": True,
                    "indicator": key,
                    "definition": value
                }

        return {
            "success": False,
            "message": f"未找到指标 '{indicator}' 的定义"
        }

    def judge_cycle(self, indicators: Dict) -> Dict:
        """
        判断经济周期

        Args:
            indicators: 经济指标字典
                - gdp_growth: GDP增速
                - cpi: CPI同比
                - pmi: PMI值
                - m2_growth: M2增速

        Returns:
            周期判断结果
        """
        gdp = indicators.get("gdp_growth", 0)
        cpi = indicators.get("cpi", 0)
        pmi = indicators.get("pmi", 50)

        # 简化的周期判断逻辑
        if pmi > 50:
            if cpi < 3:
                cycle = "复苏"
                asset = "股票"
            else:
                cycle = "过热"
                asset = "商品"
        else:
            if cpi < 2:
                cycle = "衰退"
                asset = "债券"
            else:
                cycle = "滞胀"
                asset = "现金"

        return {
            "cycle": cycle,
            "recommended_asset": asset,
            "reasoning": f"PMI={pmi}({'扩张' if pmi>50 else '收缩'}), CPI={cpi}%({'>3%' if cpi>3 else '<3%'})",
            "clock_position": self._get_clock_position(cycle)
        }

    def _get_clock_position(self, cycle: str) -> Dict:
        """获取时钟位置说明"""
        clock = {
            "复苏": {"quadrant": 1, "description": "经济上行、通胀下行"},
            "过热": {"quadrant": 2, "description": "经济上行、通胀上行"},
            "滞胀": {"quadrant": 3, "description": "经济下行、通胀上行"},
            "衰退": {"quadrant": 4, "description": "经济下行、通胀下行"}
        }
        return clock.get(cycle, {})

    def suggest_allocation(self, cycle: str) -> Dict:
        """
        大类资产配置建议

        Args:
            cycle: 经济周期阶段

        Returns:
            资产配置建议
        """
        allocations = {
            "复苏": {
                "股票": 60,
                "债券": 20,
                "商品": 15,
                "现金": 5,
                "reason": "经济复苏，企业盈利改善，股市表现最佳"
            },
            "过热": {
                "股票": 40,
                "债券": 10,
                "商品": 40,
                "现金": 10,
                "reason": "通胀上行，商品受益，央行可能收紧"
            },
            "滞胀": {
                "股票": 20,
                "债券": 20,
                "商品": 20,
                "现金": 40,
                "reason": "经济停滞通胀高企，现金为王"
            },
            "衰退": {
                "股票": 30,
                "债券": 50,
                "商品": 5,
                "现金": 15,
                "reason": "经济下行，央行宽松，债券表现最佳"
            }
        }

        return allocations.get(cycle, {
            "message": f"未知周期 '{cycle}'",
            "valid_cycles": list(allocations.keys())
        })

    def analyze_policy(self, policy_type: str, action: str) -> Dict:
        """
        分析政策影响

        Args:
            policy_type: 政策类型（货币/财政）
            action: 政策动作

        Returns:
            政策影响分析
        """
        impacts = {
            "降准": {
                "direct_effect": "释放长期流动性",
                "bond_impact": "利好（收益率下行）",
                "stock_impact": "利好（流动性改善）",
                "transmission": "银行资金成本↓ → 信贷投放↑ → 实体经济↑"
            },
            "降息": {
                "direct_effect": "降低融资成本",
                "bond_impact": "利好（收益率下行）",
                "stock_impact": "利好（估值提升）",
                "transmission": "政策利率↓ → LPR↓ → 贷款利率↓ → 投资/消费↑"
            },
            "专项债": {
                "direct_effect": "增加基建投资",
                "bond_impact": "中性偏空（供给增加）",
                "stock_impact": "利好基建链",
                "transmission": "专项债发行 → 资金到位 → 基建投资 ↑"
            }
        }

        for key, value in impacts.items():
            if key in action:
                return {
                    "success": True,
                    "policy": key,
                    "analysis": value
                }

        return {
            "success": False,
            "message": f"未找到政策 '{action}' 的影响分析",
            "available_policies": list(impacts.keys())
        }

    def chat(self, question: str) -> str:
        """
        智能问答

        Args:
            question: 用户问题

        Returns:
            回答
        """
        question = question.strip()

        # 指标解读
        if "是什么" in question or "含义" in question:
            for indicator in self.knowledge["indicators"]:
                if indicator in question:
                    result = self.explain_indicator(indicator)
                    if result["success"]:
                        return json.dumps(result["definition"], ensure_ascii=False, indent=2)

        # 周期判断
        if "周期" in question or "美林时钟" in question:
            return json.dumps(self.knowledge["cycles"], ensure_ascii=False, indent=2)

        # 数据日历
        if "日历" in question or "发布" in question:
            return json.dumps(self.knowledge["calendar"], ensure_ascii=False, indent=2)

        # 政策工具
        if "政策" in question:
            return json.dumps(self.knowledge["policies"], ensure_ascii=False, indent=2)

        return "我理解您的问题，但需要更具体的信息。您可以问我：\n1. 某个经济指标的含义（如：CPI是什么）\n2. 当前经济周期判断\n3. 政策影响分析\n4. 数据发布日历"


# ==================== 主程序 ====================

def main():
    """交互式主程序"""
    print("=" * 60)
    print("宏观经济分析智能体 v1.0")
    print("=" * 60)

    agent = MacroEconAgent()

    print(f"\n智能体名称: {agent.name}")
    print(f"版本: {agent.version}")

    print("\n可用功能:")
    print("1. 指标解读 - 输入指标名称")
    print("2. 周期判断 - 输入经济指标")
    print("3. 资产配置 - 输入周期阶段")
    print("4. 政策分析 - 输入政策动作")
    print("5. 退出 - 输入 'exit'")

    while True:
        print("\n" + "-" * 40)
        user_input = input("请输入问题: ").strip()

        if user_input.lower() == "exit":
            print("感谢使用，再见！")
            break

        # 尝试解析为周期判断
        if "," in user_input:
            try:
                parts = user_input.split(",")
                indicators = {}
                for part in parts:
                    k, v = part.split("=")
                    indicators[k.strip()] = float(v.strip())
                result = agent.judge_cycle(indicators)
                print("\n周期判断结果:")
                print(json.dumps(result, ensure_ascii=False, indent=2))

                # 自动给出配置建议
                allocation = agent.suggest_allocation(result["cycle"])
                print("\n资产配置建议:")
                print(json.dumps(allocation, ensure_ascii=False, indent=2))
                continue
            except:
                pass

        # 政策分析
        if "降" in user_input or "加息" in user_input:
            result = agent.analyze_policy("货币", user_input)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            continue

        # 默认问答
        result = agent.chat(user_input)
        print(result)


if __name__ == "__main__":
    main()