# -*- coding: utf-8 -*-
"""
有色金属行业研究智能体 v1.0

功能：
1. 行业分类与产业链分析
2. 供需平衡分析
3. 库存周期判断
4. 价格影响因素分析
5. 公司基本面分析
6. 连接Choice API获取数据

作者：Emma
日期：2026-03-11
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class MetalType(Enum):
    """有色金属类型"""
    # 工业金属
    COPPER = "铜"
    ALUMINUM = "电解铝"
    ZINC = "锌"
    LEAD = "铅"
    NICKEL = "镍"
    TIN = "锡"

    # 贵金属
    GOLD = "黄金"
    SILVER = "白银"
    PLATINUM = "铂金"
    PALLADIUM = "钯金"

    # 能源金属
    LITHIUM = "锂"
    COBALT = "钴"
    NICKEL_ENERGY = "能源镍"

    # 稀土
    RARE_EARTH = "稀土"

@dataclass
class SupplyDemandData:
    """供需数据结构"""
    period: str                    # 时期
    supply: float = 0              # 供给量
    demand: float = 0              # 需求量
    balance: float = 0             # 供需缺口
    inventory: float = 0           # 库存
    price: float = 0               # 价格

@dataclass
class CompanyInfo:
    """公司信息"""
    code: str                      # 股票代码
    name: str                      # 公司名称
    industry: str = ""             # 所属申万行业
    main_business: str = ""        # 主营业务
    revenue: float = 0             # 营业收入
    net_profit: float = 0          # 净利润
    roe: float = 0                 # ROE
    pe: float = 0                  # PE
    pb: float = 0                  # PB
    market_cap: float = 0          # 市值

class NonFerrousMetalAgent:
    """有色金属行业研究智能体"""

    def __init__(self):
        self.name = "有色金属研究员"
        self.version = "1.0"
        self.knowledge = self._load_knowledge()

    def _load_knowledge(self) -> Dict:
        """加载知识库"""
        return {
            "metals": self._get_metal_definitions(),
            "chains": self._get_industry_chains(),
            "cycles": self._get_inventory_cycles(),
            "companies": self._get_company_list(),
            "choice_indicators": self._get_choice_indicators(),
        }

    def _get_metal_definitions(self) -> Dict:
        """有色金属定义"""
        return {
            "铜": {
                "分类": "工业金属",
                "特性": "导电性、导热性优异，耐腐蚀",
                "主要用途": ["电线电缆", "建筑", "汽车", "电子"],
                "定价权": "全球定价，LME为基准",
                "主要产区": ["智利", "秘鲁", "中国", "刚果"],
                "储量分布": {"智利": "23%", "秘鲁": "10%", "澳大利亚": "10%"},
                "关键指标": ["TC/RC加工费", "库存(LME+SHFE)", "现货升贴水", "废铜价差"],
            },
            "电解铝": {
                "分类": "工业金属",
                "特性": "轻量化、耐腐蚀、导电性好",
                "主要用途": ["建筑", "交通运输", "电力", "包装"],
                "定价权": "中国定价主导，产能天花板4500万吨",
                "主要产区": ["中国", "俄罗斯", "印度", "加拿大"],
                "成本构成": {"氧化铝": "40%", "电力": "40%", "阳极": "10%"},
                "关键指标": ["产能利用率", "库存", "氧化铝价格", "电力成本"],
                "政策约束": "产能天花板4500万吨，碳中和约束",
            },
            "黄金": {
                "分类": "贵金属",
                "特性": "货币属性、商品属性、金融属性",
                "主要用途": ["珠宝首饰", "投资", "央行储备", "工业"],
                "定价逻辑": "实际利率=名义利率-通胀预期",
                "关键指标": ["美国实际利率", "美元指数", "ETF持仓", "央行购金"],
                "周期特征": "避险资产，与风险资产负相关",
            },
            "锂": {
                "分类": "能源金属",
                "特性": "电池级碳酸锂为新能源车核心材料",
                "主要用途": ["动力电池", "储能", "陶瓷玻璃"],
                "定价权": "从长协定价向现货定价转变",
                "资源类型": ["盐湖提锂", "锂辉石", "锂云母"],
                "关键指标": ["电池级碳酸锂价格", "氢氧化锂价格", "锂精矿价格"],
            },
        }

    def _get_industry_chains(self) -> Dict:
        """产业链结构"""
        return {
            "铜产业链": {
                "上游": {
                    "矿产资源": "铜矿开采 → 铜精矿",
                    "主要企业": ["紫金矿业", "洛阳钼业", "江西铜业"],
                },
                "中游": {
                    "冶炼加工": "铜精矿 → 粗铜 → 精炼铜 → 铜材",
                    "主要企业": ["江西铜业", "铜陵有色", "云南铜业"],
                },
                "下游": {
                    "应用领域": "电力电缆、建筑、汽车、电子",
                    "主要企业": ["精达股份", "海亮股份", "金田铜业"],
                },
            },
            "电解铝产业链": {
                "上游": {
                    "矿产资源": "铝土矿 → 氧化铝",
                    "主要企业": ["中国铝业", "南山铝业"],
                },
                "中游": {
                    "冶炼": "氧化铝 + 电解 → 电解铝",
                    "主要企业": ["中国宏桥", "云铝股份", "神火股份"],
                },
                "下游": {
                    "加工": "铝材、铝箔、铝型材",
                    "主要企业": ["中国忠旺", "南山铝业", "明泰铝业"],
                },
            },
            "锂产业链": {
                "上游": {
                    "资源": "锂辉石/盐湖/锂云母 → 锂盐",
                    "主要企业": ["赣锋锂业", "天齐锂业", "盐湖股份"],
                },
                "中游": {
                    "材料": "碳酸锂/氢氧化锂 → 正极材料",
                    "主要企业": ["容百科技", "当升科技", "德方纳米"],
                },
                "下游": {
                    "电池": "动力电池、储能电池",
                    "主要企业": ["宁德时代", "比亚迪", "亿纬锂能"],
                },
            },
        }

    def _get_inventory_cycles(self) -> Dict:
        """库存周期"""
        return {
            "四个阶段": {
                "被动补库": "需求下降，库存上升 → 价格下跌",
                "主动去库": "需求下降，库存下降 → 价格筑底",
                "被动去库": "需求上升，库存下降 → 价格上涨",
                "主动补库": "需求上升，库存上升 → 价格见顶",
            },
            "判断指标": [
                "社会库存",
                "交易所库存(LME/SHFE)",
                "企业库存",
                "库存周转天数",
            ],
            "铜库存周期": {
                "观察指标": "LME库存 + SHFE库存 + 保税区库存",
                "正常区间": "全球显性库存30-50万吨",
                "紧张信号": "库存低于20万吨，现货升水",
                "过剩信号": "库存高于60万吨，现货贴水",
            },
            "铝库存周期": {
                "观察指标": "社会库存 + 交易所库存",
                "正常区间": "社会库存80-120万吨",
                "特点": "季节性明显，春节后累库，旺季去库",
            },
        }

    def _get_company_list(self) -> Dict:
        """有色金属公司列表（按申万行业分类）"""
        return {
            "申万一级: 有色金属": {
                "铜": [
                    {"代码": "601899.SH", "名称": "紫金矿业", "主营": "金铜锌采矿选矿冶炼"},
                    {"代码": "600362.SH", "名称": "江西铜业", "主营": "铜采选冶炼加工"},
                    {"代码": "000630.SZ", "名称": "铜陵有色", "主营": "铜冶炼加工"},
                    {"代码": "601168.SH", "名称": "西部矿业", "主营": "铜铅锌采选冶炼"},
                ],
                "铝": [
                    {"代码": "601600.SH", "名称": "中国铝业", "主营": "氧化铝电解铝"},
                    {"代码": "000807.SZ", "名称": "云铝股份", "主营": "绿色电解铝"},
                    {"代码": "000933.SZ", "名称": "神火股份", "主营": "电解铝煤炭"},
                    {"代码": "602192.SH", "名称": "中国宏桥", "主营": "电解铝"},
                ],
                "贵金属": [
                    {"代码": "600547.SH", "名称": "山东黄金", "主营": "黄金采选"},
                    {"代码": "600489.SH", "名称": "中金黄金", "主营": "黄金采选冶炼"},
                    {"代码": "002155.SZ", "名称": "湖南黄金", "主营": "黄金锑钨"},
                ],
                "能源金属": [
                    {"代码": "002460.SZ", "名称": "赣锋锂业", "主营": "锂产品"},
                    {"代码": "002466.SZ", "名称": "天齐锂业", "主营": "锂资源"},
                    {"代码": "000792.SZ", "名称": "盐湖股份", "主营": "钾肥锂盐"},
                    {"代码": "603993.SH", "名称": "洛阳钼业", "主营": "钼钨钴铜"},
                ],
                "稀土": [
                    {"代码": "600111.SH", "名称": "北方稀土", "主营": "稀土采选冶炼"},
                    {"代码": "000831.SZ", "名称": "五矿稀土", "主营": "稀土冶炼"},
                ],
            },
        }

    def _get_choice_indicators(self) -> Dict:
        """Choice API指标映射"""
        return {
            "期货行情": {
                "日行情": "Close,Open,High,Low,Volume,OI,Amount",
                "主力合约": "MAINCONTRACT",
            },
            "股票行情": {
                "日行情": "CLOSE,OPEN,HIGH,LOW,VOLUME,AMOUNT",
                "估值": "PE,PB,PS,MV",
                "财务": "ROE,NETPROFIT,OPERATEREVE",
            },
            "宏观指标": {
                "PMI": "制造业景气度",
                "CPI": "通胀预期",
                "M2": "流动性",
            },
            "行业指标": {
                "库存": "社会库存,交易所库存",
                "加工费": "TC/RC",
                "升贴水": "现货升贴水",
            },
        }

    # ==================== 行业分析功能 ====================

    def analyze_metal(self, metal_name: str) -> Dict:
        """
        分析特定金属

        Args:
            metal_name: 金属名称（铜/电解铝/黄金/锂等）

        Returns:
            金属分析报告
        """
        metals = self.knowledge["metals"]

        for key, value in metals.items():
            if metal_name in key or key in metal_name:
                return {
                    "success": True,
                    "metal": key,
                    "definition": value,
                    "chain": self.knowledge["chains"].get(f"{key}产业链", {}),
                }

        return {
            "success": False,
            "message": f"未找到金属 '{metal_name}' 的信息",
            "available_metals": list(metals.keys()),
        }

    def get_supply_demand_analysis(self, metal: str) -> Dict:
        """
        供需平衡分析

        Args:
            metal: 金属名称

        Returns:
            供需分析框架
        """
        return {
            "metal": metal,
            "供给端": {
                "矿产供给": "全球矿山产量、新产能投放",
                "再生供给": "废料回收",
                "进口供给": "进口量",
            },
            "需求端": {
                "下游需求": "各行业消费占比",
                "季节性": "旺季/淡季",
                "新兴需求": "新能源等增量需求",
            },
            "平衡表": {
                "项目": ["供给", "需求", "缺口", "库存变化"],
                "数据来源": "ILZSG, WBMS, SMM",
            },
            "关键跟踪": [
                "月度供需平衡",
                "显性库存变化",
                "现货升贴水",
            ],
        }

    def judge_inventory_cycle(self, inventory_trend: str, demand_trend: str) -> Dict:
        """
        判断库存周期阶段

        Args:
            inventory_trend: 库存趋势（上升/下降/稳定）
            demand_trend: 需求趋势（上升/下降/稳定）

        Returns:
            周期判断结果
        """
        cycles = self.knowledge["cycles"]["四个阶段"]

        if demand_trend == "下降" and inventory_trend == "上升":
            phase = "被动补库"
            price_view = "价格下跌"
        elif demand_trend == "下降" and inventory_trend == "下降":
            phase = "主动去库"
            price_view = "价格筑底"
        elif demand_trend == "上升" and inventory_trend == "下降":
            phase = "被动去库"
            price_view = "价格上涨"
        elif demand_trend == "上升" and inventory_trend == "上升":
            phase = "主动补库"
            price_view = "价格见顶"
        else:
            phase = "过渡阶段"
            price_view = "方向不明"

        return {
            "phase": phase,
            "price_outlook": price_view,
            "description": cycles.get(phase, ""),
            "investment_advice": self._get_cycle_investment_advice(phase),
        }

    def _get_cycle_investment_advice(self, phase: str) -> str:
        """根据周期阶段给出投资建议"""
        advice = {
            "被动补库": "规避风险，等待价格企稳",
            "主动去库": "关注左侧布局机会",
            "被动去库": "积极配置，价格上行期",
            "主动补库": "持有为主，关注见顶信号",
        }
        return advice.get(phase, "观望为主")

    def get_company_ranking(self, metal_type: str) -> Dict:
        """
        获取公司排名

        Args:
            metal_type: 金属类型

        Returns:
            公司排名列表
        """
        companies = self.knowledge["companies"]
        metal_companies = []

        for industry, data in companies.items():
            if metal_type in data:
                metal_companies = data[metal_type]
                break

        return {
            "metal_type": metal_type,
            "companies": metal_companies,
            "ranking_criteria": [
                "资源储量",
                "产能规模",
                "成本优势",
                "盈利能力",
            ],
        }

    def analyze_price_factors(self, metal: str) -> Dict:
        """
        分析价格影响因素

        Args:
            metal: 金属名称

        Returns:
            价格影响因素分析
        """
        factors = {
            "铜": {
                "长期因素": [
                    "全球经济增长",
                    "铜矿资本开支",
                    "绿色转型需求",
                ],
                "中期因素": [
                    "TC/RC加工费",
                    "库存水平",
                    "中国需求",
                ],
                "短期因素": [
                    "美元指数",
                    "市场情绪",
                    "投机持仓",
                ],
            },
            "电解铝": {
                "长期因素": [
                    "产能天花板",
                    "碳中和政策",
                    "需求结构变化",
                ],
                "中期因素": [
                    "氧化铝价格",
                    "电力成本",
                    "产能利用率",
                ],
                "短期因素": [
                    "社会库存",
                    "下游开工率",
                    "季节性因素",
                ],
            },
            "黄金": {
                "长期因素": [
                    "实际利率趋势",
                    "央行购金",
                    "美元信用",
                ],
                "中期因素": [
                    "美联储货币政策",
                    "通胀预期",
                    "ETF持仓",
                ],
                "短期因素": [
                    "避险情绪",
                    "美元波动",
                    "投机持仓",
                ],
            },
        }

        for key, value in factors.items():
            if metal in key or key in metal:
                return {
                    "metal": key,
                    "factors": value,
                    "分析框架": "长期看供给，中期看库存，短期看情绪",
                }

        return {
            "message": f"未找到 {metal} 的价格分析框架",
            "available": list(factors.keys()),
        }

    def get_choice_api_query(self, data_type: str, codes: List[str]) -> Dict:
        """
        生成Choice API查询参数

        Args:
            data_type: 数据类型（futures_daily/stock_daily/financial）
            codes: 证券代码列表

        Returns:
            API查询参数
        """
        indicators = self.knowledge["choice_indicators"]

        queries = {
            "futures_daily": {
                "function": "pedb.get_data_by_date",
                "fields": indicators["期货行情"]["日行情"],
                "codes": codes,
                "example": "pedb.get_data(['CU2504.SHF'], 'Close,Volume', '2026-01-01', '2026-03-11')",
            },
            "stock_daily": {
                "function": "pedb.get_data_by_date",
                "fields": indicators["股票行情"]["日行情"],
                "codes": codes,
                "example": "pedb.get_data(['601899.SH'], 'CLOSE,VOLUME', '2026-01-01', '2026-03-11')",
            },
            "valuation": {
                "function": "pedb.get_data_by_date",
                "fields": indicators["股票行情"]["估值"],
                "codes": codes,
            },
        }

        return queries.get(data_type, {
            "message": f"未知数据类型: {data_type}",
            "available": list(queries.keys()),
        })

    def format_report(self, analysis: Dict, title: str = "有色金属行业分析报告") -> str:
        """格式化分析报告"""
        report = []
        report.append("=" * 60)
        report.append(title)
        report.append("=" * 60)

        for section, data in analysis.items():
            report.append(f"\n【{section}】")
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        report.append(f"  {key}: {', '.join(map(str, value))}")
                    else:
                        report.append(f"  {key}: {value}")
            else:
                report.append(f"  {data}")

        return "\n".join(report)


# ==================== 主程序 ====================

def main():
    """演示程序"""
    print("=" * 60)
    print("有色金属行业研究智能体 v1.0")
    print("=" * 60)

    agent = NonFerrousMetalAgent()

    print(f"\n智能体名称: {agent.name}")
    print(f"版本: {agent.version}")

    # 示例：铜的分析
    print("\n" + "-" * 40)
    print("铜行业分析")
    print("-" * 40)
    copper_analysis = agent.analyze_metal("铜")
    print(json.dumps(copper_analysis, ensure_ascii=False, indent=2))

    # 示例：库存周期判断
    print("\n" + "-" * 40)
    print("库存周期判断")
    print("-" * 40)
    cycle = agent.judge_inventory_cycle("下降", "上升")
    print(f"库存趋势: 下降, 需求趋势: 上升")
    print(f"周期阶段: {cycle['phase']}")
    print(f"价格展望: {cycle['price_outlook']}")
    print(f"投资建议: {cycle['investment_advice']}")

    # 示例：公司排名
    print("\n" + "-" * 40)
    print("铜行业公司")
    print("-" * 40)
    companies = agent.get_company_ranking("铜")
    for company in companies.get("companies", []):
        print(f"  {company['代码']} {company['名称']}: {company['主营']}")


if __name__ == "__main__":
    main()