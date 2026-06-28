#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EMR-CRIF v2.0: 电子病历数据使用行为合规性评估模型

评估对象：人使用数据的行为（主体、权限、场景、行为）
而非：电子病历数据集本身的质量

法律依据：
1. 《中华人民共和国个人信息保护法》（2021）
2. 《中华人民共和国数据安全法》（2021）
3. 《中华人民共和国网络安全法》（2017）
4. 《涉及人的生命科学和医学研究伦理审查办法》（2023）
5. 《医疗卫生机构网络安全管理办法》（2022）
6. GB/T 35273-2020《信息安全技术 个人信息安全规范》
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple


class BehaviorComplianceModel:
    """数据使用行为合规性评估模型"""
    
    def __init__(self):
        self.version = "2.0.0"
        self.legal_basis = [
            "《中华人民共和国个人信息保护法》（2021）",
            "《中华人民共和国数据安全法》（2021）",
            "《中华人民共和国网络安全法》（2017）",
            "《涉及人的生命科学和医学研究伦理审查办法》（2023）",
            "《医疗卫生机构网络安全管理办法》（2022）",
            "GB/T 35273-2020《信息安全技术 个人信息安全规范》"
        ]
        
        # 权重配置（总和=1.0）
        self.weights = {
            "subject_compliance": 0.25,    # 主体合规性
            "authorization_compliance": 0.30,  # 权限合规性（最重要）
            "scenario_compliance": 0.20,  # 场景合规性
            "operation_compliance": 0.25  # 操作合规性
        }
        
        # 风险等级划分
        self.risk_levels = {
            (90, 100): "合规（行为合法，无风险）",
            (70, 89): "基本合规（存在轻微瑕疵，需改进）",
            (50, 69): "不合规（存在违法风险，需整改）",
            (0, 49): "严重违法（行为违法，需立即停止）"
        }
    
    def assess_subject_compliance(self, behavior: Dict) -> Tuple[float, Dict]:
        """
        评估主体合规性（谁在使用数据？）
        
        审查要素：
        1. 使用主体是否授权人员
        2. 主体权限是否匹配角色
        3. 主体行为是否可追溯
        """
        score = 0.0
        details = {}
        
        # 1. 使用主体身份合法性（40分）
        actor = behavior.get("actor", {})
        if actor.get("authorization_status") == "已授权":
            score += 40
            details["actor_identity"] = {
                "score": 40,
                "status": f"授权人员（{actor.get('role', '')}）",
                "evidence": actor.get("authorization_id", "")
            }
        elif actor.get("authorization_status") == "临时授权":
            score += 20
            details["actor_identity"] = {
                "score": 20,
                "status": "临时授权人员（需审批）",
                "evidence": actor.get("authorization_id", "")
            }
        else:
            details["actor_identity"] = {
                "score": 0,
                "status": "❌ 未授权人员（严重违法）",
                "evidence": ""
            }
        
        # 2. 主体权限匹配性（35分）
        if actor.get("permission_match_role", False):
            score += 35
            details["permission_match"] = {
                "score": 35,
                "status": "权限与角色匹配"
            }
        else:
            details["permission_match"] = {
                "score": 0,
                "status": "❌ 越权访问（严重违法）"
            }
        
        # 3. 主体行为可追溯性（25分）
        if behavior.get("audit_log_exists", False):
            score += 25
            details["audit_log"] = {
                "score": 25,
                "status": "行为有完整审计日志"
            }
        else:
            details["audit_log"] = {
                "score": 0,
                "status": "⚠️ 无审计日志（违法）"
            }
        
        return score, details
    
    def assess_authorization_compliance(self, behavior: Dict) -> Tuple[float, Dict]:
        """
        评估权限合规性（是否有合法权限使用数据？）
        
        审查要素：
        1. 是否取得知情同意
        2. 是否通过伦理审查
        3. 是否签署数据处理协议
        """
        score = 0.0
        details = {}
        
        # 1. 知情同意有效性（40分）
        consent = behavior.get("consent_status", {})
        if consent.get("obtained", False):
            score += 20
            details["consent_obtained"] = {
                "score": 20,
                "status": "已取得知情同意"
            }
            
            # 同意是否包含具体用途
            if consent.get("specific_to_purpose", False):
                score += 20
                details["consent_specific"] = {
                    "score": 20,
                    "status": "同意书包含具体用途授权"
                }
            else:
                details["consent_specific"] = {
                    "score": 0,
                    "status": "⚠️ 同意书未包含具体用途（瑕疵）"
                }
        else:
            details["consent_obtained"] = {
                "score": 0,
                "status": "❌ 未取得知情同意（严重违法）"
            }
        
        # 2. 伦理审查覆盖性（35分）
        ethics = behavior.get("ethics_approval", {})
        if ethics.get("approved", False):
            score += 35
            details["ethics_approval"] = {
                "score": 35,
                "status": f"已通过伦理审查（编号：{ethics.get('approval_id', '')}）"
            }
        else:
            details["ethics_approval"] = {
                "score": 0,
                "status": "❌ 未通过伦理审查（严重违法）"
            }
        
        # 3. 数据处理协议完备性（25分）
        dpa = behavior.get("data_processing_agreement", {})
        if dpa.get("signed", False):
            score += 25
            details["dpa_status"] = {
                "score": 25,
                "status": "已签署数据处理协议"
            }
        elif dpa.get("not_required", False):
            score += 25
            details["dpa_status"] = {
                "score": 25,
                "status": "无需签署（直接使用，非委托处理）"
            }
        else:
            details["dpa_status"] = {
                "score": 0,
                "status": "⚠️ 未签署数据处理协议（违法）"
            }
        
        return score, details
    
    def assess_scenario_compliance(self, behavior: Dict) -> Tuple[float, Dict]:
        """
        评估场景合规性（用途是否符合授权？）
        
        审查要素：
        1. 使用目的是否符合告知目的
        2. 使用场景是否授权
        3. 是否遵循数据最小化原则
        """
        score = 0.0
        details = {}
        
        # 1. 使用目的匹配性（40分）
        purpose = behavior.get("purpose", {})
        if purpose.get("within_informed_consent", False):
            score += 40
            details["purpose_match"] = {
                "score": 40,
                "status": f"使用目的符合知情同意（{purpose.get('description', '')}）"
            }
        else:
            details["purpose_match"] = {
                "score": 0,
                "status": "❌ 使用目的超出知情同意范围（违法）"
            }
        
        # 2. 使用场景授权性（35分）
        scenario = behavior.get("scenario", {})
        if scenario.get("authorized", False):
            score += 35
            details["scenario_auth"] = {
                "score": 35,
                "status": f"使用场景已授权（{scenario.get('type', '')}）"
            }
        else:
            details["scenario_auth"] = {
                "score": 0,
                "status": "⚠️ 使用场景未授权（需补充授权）"
            }
        
        # 3. 数据最小化原则遵循性（25分）
        data_minimization = behavior.get("data_minimization", {})
        if data_minimization.get("followed", False):
            score += 25
            details["data_minimization"] = {
                "score": 25,
                "status": "遵循数据最小化原则"
            }
        else:
            details["data_minimization"] = {
                "score": 0,
                "status": "⚠️ 未遵循数据最小化原则（索取无关数据）"
            }
        
        return score, details
    
    def assess_operation_compliance(self, behavior: Dict) -> Tuple[float, Dict]:
        """
        评估操作合规性（操作是否合规？）
        
        审查要素：
        1. 访问行为是否合规
        2. 复制/下载行为是否合规
        3. 共享/传输行为是否合规
        4. 删除/销毁行为是否合规
        """
        score = 0.0
        details = {}
        
        # 1. 访问行为合规性（30分）
        access = behavior.get("access_behavior", {})
        access_score = 0
        
        if access.get("logged", False):
            access_score += 15
            details["access_log"] = {"score": 15, "status": "访问行为有日志"}
        else:
            details["access_log"] = {"score": 0, "status": "⚠️ 访问行为无日志"}
            
        if access.get("justified", False):
            access_score += 15
            details["access_justification"] = {"score": 15, "status": "访问行为有合理理由"}
        else:
            details["access_justification"] = {"score": 0, "status": "⚠️ 访问行为无合理理由"}
            
        score += access_score
        details["access"] = {"score": access_score, "max": 30}
        
        # 2. 复制/下载行为合规性（25分）
        copy_behavior = behavior.get("copy_behavior", {})
        if copy_behavior.get("occurred", False):
            # 有复制/下载行为
            if copy_behavior.get("approved", False):
                score += 25
                details["copy_approval"] = {"score": 25, "status": "复制/下载行为已审批"}
            else:
                details["copy_approval"] = {"score": 0, "status": "⚠️ 复制/下载行为未审批（违法）"}
        else:
            # 无复制/下载行为
            score += 25
            details["copy_approval"] = {"score": 25, "status": "无复制/下载行为（合规）"}
        
        # 3. 共享/传输行为合规性（25分）
        share_behavior = behavior.get("share_behavior", {})
        if share_behavior.get("occurred", False):
            # 有共享/传输行为
            if share_behavior.get("encrypted", False):
                score += 15
                details["share_encryption"] = {"score": 15, "status": "共享/传输行为已加密"}
            else:
                details["share_encryption"] = {"score": 0, "status": "❌ 共享/传输行为未加密（严重违法）"}
                
            if share_behavior.get("recipient_compliant", False):
                score += 10
                details["share_recipient"] = {"score": 10, "status": "接收方合规"}
            else:
                details["share_recipient"] = {"score": 0, "status": "⚠️ 接收方不合规"}
        else:
            # 无共享/传输行为
            score += 25
            details["share_encryption"] = {"score": 25, "status": "无共享/传输行为（合规）"}
        
        # 4. 删除/销毁行为合规性（20分）
        delete_behavior = behavior.get("delete_behavior", {})
        if delete_behavior.get("occurred", False):
            # 有删除/销毁行为
            if delete_behavior.get("logged", False):
                score += 20
                details["delete_log"] = {"score": 20, "status": "删除/销毁行为有留痕"}
            else:
                details["delete_log"] = {"score": 0, "status": "⚠️ 删除/销毁行为无留痕（违法）"}
        else:
            # 无删除/销毁行为
            score += 20
            details["delete_log"] = {"score": 20, "status": "无删除/销毁行为（合规）"}
        
        return score, details
    
    def calculate_overall_score(self, behavior: Dict) -> Dict:
        """计算综合评分"""
        
        # 各维度评分
        subject_score, subject_details = self.assess_subject_compliance(behavior)
        auth_score, auth_details = self.assess_authorization_compliance(behavior)
        scenario_score, scenario_details = self.assess_scenario_compliance(behavior)
        operation_score, operation_details = self.assess_operation_compliance(behavior)
        
        # 加权综合评分
        overall_score = (
            subject_score * self.weights["subject_compliance"] +
            auth_score * self.weights["authorization_compliance"] +
            scenario_score * self.weights["scenario_compliance"] +
            operation_score * self.weights["operation_compliance"]
        )
        
        # 确定风险等级
        risk_level = "未知"
        for (low, high), level in self.risk_levels.items():
            if low <= overall_score <= high:
                risk_level = level
                break
        
        # 生成评估报告
        report = {
            "report_id": f"EMR-CRIF-v2-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "model_version": self.version,
            "assessment_date": datetime.now().isoformat(),
            "legal_basis": self.legal_basis,
            "behavior_summary": {
                "event_id": behavior.get("event_id", "未知"),
                "timestamp": behavior.get("timestamp", "未知"),
                "actor": behavior.get("actor", {}).get("name", "未知"),
                "actor_role": behavior.get("actor", {}).get("role", "未知"),
                "action_type": behavior.get("action", {}).get("type", "未知"),
                "purpose": behavior.get("purpose", {}).get("description", "未知"),
                "data_source": behavior.get("data_source", "未知"),
                "data_category": behavior.get("data_category", "未知"),
                "processing_method": behavior.get("processing_method", "未知")
            },
            "dimension_scores": {
                "subject_compliance": {
                    "score": subject_score,
                    "max_score": 100,
                    "weight": self.weights["subject_compliance"],
                    "weighted_score": subject_score * self.weights["subject_compliance"],
                    "details": subject_details
                },
                "authorization_compliance": {
                    "score": auth_score,
                    "max_score": 100,
                    "weight": self.weights["authorization_compliance"],
                    "weighted_score": auth_score * self.weights["authorization_compliance"],
                    "details": auth_details
                },
                "scenario_compliance": {
                    "score": scenario_score,
                    "max_score": 100,
                    "weight": self.weights["scenario_compliance"],
                    "weighted_score": scenario_score * self.weights["scenario_compliance"],
                    "details": scenario_details
                },
                "operation_compliance": {
                    "score": operation_score,
                    "max_score": 100,
                    "weight": self.weights["operation_compliance"],
                    "weighted_score": operation_score * self.weights["operation_compliance"],
                    "details": operation_details
                }
            },
            "overall_score": round(overall_score, 2),
            "risk_level": risk_level,
            "is_compliant": overall_score >= 70,
            "legal_risk": self._assess_legal_risk(overall_score, subject_details, auth_details),
            "recommendations": self._generate_recommendations(overall_score, subject_details, auth_details, scenario_details, operation_details)
        }
        
        return report
    
    def _assess_legal_risk(self, score: float, subject: Dict, auth: Dict) -> str:
        """评估法律风险"""
        if score < 50:
            return "❌ 严重法律风险：行为可能构成违法，需立即停止并整改"
        elif score < 70:
            return "⚠️ 中等法律风险：行为存在违法风险，需限期整改"
        elif score < 90:
            return "⚠️ 轻微法律风险：行为基本合规，存在轻微瑕疵"
        else:
            return "✅ 无法律风险：行为合法合规"
    
    def _generate_recommendations(self, score: float, subject: Dict, auth: Dict, scenario: Dict, operation: Dict) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 主体合规性建议
        if subject.get("actor_identity", {}).get("score", 0) < 40:
            recommendations.append("❌ 必须确保使用数据的主体是授权人员")
        if subject.get("permission_match", {}).get("score", 0) < 35:
            recommendations.append("❌ 必须确保主体权限与角色匹配，禁止越权访问")
        if subject.get("audit_log", {}).get("score", 0) < 25:
            recommendations.append("⚠️ 必须建立完整的审计日志系统")
        
        # 权限合规性建议
        if auth.get("consent_obtained", {}).get("score", 0) < 20:
            recommendations.append("❌ 必须取得患者知情同意，否则行为违法")
        if auth.get("consent_specific", {}).get("score", 0) < 20:
            recommendations.append("⚠️ 必须补充知情同意书，明确包含科研用途授权")
        if auth.get("ethics_approval", {}).get("score", 0) < 35:
            recommendations.append("❌ 必须通过伦理委员会审查，否则研究违法")
        if auth.get("dpa_status", {}).get("score", 0) < 25:
            recommendations.append("⚠️ 必须签署数据处理协议（DPA）")
        
        # 场景合规性建议
        if scenario.get("purpose_match", {}).get("score", 0) < 40:
            recommendations.append("❌ 必须确保使用目的符合知情同意范围")
        if scenario.get("scenario_auth", {}).get("score", 0) < 35:
            recommendations.append("⚠️ 必须补充使用场景授权")
        if scenario.get("data_minimization", {}).get("score", 0) < 25:
            recommendations.append("⚠️ 必须遵循数据最小化原则")
        
        # 操作合规性建议
        if operation.get("access", {}).get("score", 0) < 30:
            recommendations.append("⚠️ 必须确保访问行为有日志、有合理理由")
        if "copy_approval" in operation and operation["copy_approval"].get("score", 0) < 25:
            recommendations.append("⚠️ 复制/下载行为必须审批")
        if "share_encryption" in operation and operation["share_encryption"].get("score", 0) < 15:
            recommendations.append("❌ 共享/传输行为必须加密")
        
        if not recommendations:
            recommendations.append("✅ 行为合法合规，无改进建议")
            
        return recommendations
    
    def generate_compliance_report(self, report: Dict) -> str:
        """生成合规性评估报告（司法鉴定报告格式）"""
        
        lines = []
        lines.append("=" * 80)
        lines.append("电子病历数据使用行为合规性评估报告")
        lines.append("报告编号：" + report["report_id"])
        lines.append("评估日期：" + report["assessment_date"])
        lines.append("=" * 80)
        lines.append("")
        
        lines.append("【法律依据】")
        for basis in report["legal_basis"]:
            lines.append(f"  • {basis}")
        lines.append("")
        
        lines.append("【行为概要】")
        for key, value in report["behavior_summary"].items():
            lines.append(f"  {key}：{value}")
        lines.append("")
        
        lines.append("【评估结果与评分】")
        lines.append(f"  综合评分：{report['overall_score']} / 100")
        lines.append(f"  风险等级：{report['risk_level']}")
        lines.append(f"  合规性：{'✅ 合规' if report['is_compliant'] else '❌ 不合规'}")
        lines.append(f"  法律风险：{report['legal_risk']}")
        lines.append("")
        
        lines.append("【各维度评分详情】")
        for dim_name, dim_data in report["dimension_scores"].items():
            lines.append(f"")
            lines.append(f"  ■ {dim_name}（权重{dim_data['weight']}）")
            lines.append(f"    原始得分：{dim_data['score']:.1f} / {dim_data['max_score']}")
            lines.append(f"    加权得分：{dim_data['weighted_score']:.2f}")
            lines.append(f"    评估详情：")
            for detail_name, detail_data in dim_data["details"].items():
                if isinstance(detail_data, dict):
                    lines.append(f"      - {detail_name}：{detail_data.get('status', '')}（得分：{detail_data.get('score', 0)}）")
        lines.append("")
        
        lines.append("【改进建议】")
        for i, rec in enumerate(report["recommendations"], 1):
            lines.append(f"  {i}. {rec}")
        lines.append("")
        lines.append("=" * 80)
        lines.append("评估模型：EMR-CRIF v" + report["model_version"])
        lines.append("免责声明：本报告基于提供的行为日志评估，实际合规状态以监管机构审查为准")
        lines.append("=" * 80)
        
        return "\n".join(lines)


# 测试用例：模拟3种不同合规状态的行为
def create_test_cases():
    """创建测试用例"""
    
    # 测试用例1：合规行为（科研人员正常使用数据）
    compliant_behavior = {
        "event_id": "EVT-2026-LECHENG-001",
        "timestamp": "2026-06-25T10:30:00+08:00",
        "actor": {
            "id": "RESEARCHER-001",
            "name": "李某某",
            "role": "科研人员",
            "department": "乐城真实世界研究院",
            "authorization_status": "已授权",
            "authorization_id": "AUTH-2026-001"
        },
        "action": {
            "type": "查询",
            "target_patient_id": "P-2026-001（已去标识化）",
            "data_fields_accessed": ["诊断记录", "用药记录", "随访记录"],
            "purpose": "真实世界研究（科研项目编号：PROJ-2026-001）",
            "system": "医院科研数据平台"
        },
        "consent_status": {
            "obtained": True,
            "specific_to_purpose": True,
            "consent_form_id": "CONSENT-2026-001"
        },
        "ethics_approval": {
            "approved": True,
            "approval_id": "IRB-2026-001"
        },
        "data_processing_agreement": {
            "signed": True,
            "agreement_id": "DPA-2026-001"
        },
        "purpose": {
            "description": "真实世界研究",
            "within_informed_consent": True
        },
        "scenario": {
            "type": "科研用途",
            "authorized": True
        },
        "data_minimization": {
            "followed": True
        },
        "audit_log_exists": True,
        "access_behavior": {
            "logged": True,
            "justified": True
        },
        "copy_behavior": {
            "occurred": False
        },
        "share_behavior": {
            "occurred": False
        },
        "delete_behavior": {
            "occurred": False
        },
        "data_source": "乐城某医院科研数据平台",
        "data_category": "去标识化电子病历数据",
        "processing_method": "统计分析（Python/R）"
    }
    
    # 测试用例2：不合规行为（未取得知情同意）
    non_compliant_behavior = {
        "event_id": "EVT-2026-LECHENG-002",
        "timestamp": "2026-06-25T14:00:00+08:00",
        "actor": {
            "id": "DOCTOR-002",
            "name": "王某某",
            "role": "医生",
            "department": "甲状腺外科",
            "authorization_status": "已授权",
            "authorization_id": "AUTH-2026-002"
        },
        "action": {
            "type": "查询+复制",
            "target_patient_id": "P-2026-002（未去标识化）",
            "data_fields_accessed": ["姓名", "身份证号", "诊断记录", "用药记录"],
            "purpose": "学术研究（未明确告知患者）",
            "system": "医院HIS系统"
        },
        "consent_status": {
            "obtained": False,  # 未取得知情同意
            "specific_to_purpose": False,
            "consent_form_id": ""
        },
        "ethics_approval": {
            "approved": False,  # 未通过伦理审查
            "approval_id": ""
        },
        "data_processing_agreement": {
            "signed": False,
            "agreement_id": ""
        },
        "purpose": {
            "description": "学术研究",
            "within_informed_consent": False  # 超出知情同意范围
        },
        "scenario": {
            "type": "学术研究",
            "authorized": False
        },
        "data_minimization": {
            "followed": False  # 未遵循最小化原则
        },
        "audit_log_exists": True,
        "access_behavior": {
            "logged": True,
            "justified": False  # 访问行为无合理理由
        },
        "copy_behavior": {
            "occurred": True,
            "approved": False  # 复制行为未审批
        },
        "share_behavior": {
            "occurred": True,
            "encrypted": False,  # 共享行为未加密
            "recipient_compliant": False
        },
        "delete_behavior": {
            "occurred": False
        },
        "data_source": "医院HIS系统",
        "data_category": "未去标识化电子病历数据",
        "processing_method": "Excel手工处理"
    }
    
    # 测试用例3：基本合规行为（存在轻微瑕疵）
    partially_compliant_behavior = {
        "event_id": "EVT-2026-LECHENG-003",
        "timestamp": "2026-06-25T16:30:00+08:00",
        "actor": {
            "id": "RESEARCHER-002",
            "name": "张某某",
            "role": "科研人员",
            "department": "乐城真实世界研究院",
            "authorization_status": "已授权",
            "authorization_id": "AUTH-2026-003"
        },
        "action": {
            "type": "查询",
            "target_patient_id": "P-2026-003（已去标识化）",
            "data_fields_accessed": ["诊断记录", "用药记录"],
            "purpose": "真实世界研究",
            "system": "医院科研数据平台"
        },
        "consent_status": {
            "obtained": True,
            "specific_to_purpose": False,  # 瑕疵：同意书未包含科研用途专门授权
            "consent_form_id": "CONSENT-2026-003"
        },
        "ethics_approval": {
            "approved": True,
            "approval_id": "IRB-2026-003"
        },
        "data_processing_agreement": {
            "signed": True,
            "agreement_id": "DPA-2026-003"
        },
        "purpose": {
            "description": "真实世界研究",
            "within_informed_consent": True
        },
        "scenario": {
            "type": "科研用途",
            "authorized": True
        },
        "data_minimization": {
            "followed": True
        },
        "audit_log_exists": True,
        "access_behavior": {
            "logged": True,
            "justified": True
        },
        "copy_behavior": {
            "occurred": False
        },
        "share_behavior": {
            "occurred": False
        },
        "delete_behavior": {
            "occurred": False
        },
        "data_source": "乐城某医院科研数据平台",
        "data_category": "去标识化电子病历数据",
        "processing_method": "统计分析（Python）"
    }
    
    return [compliant_behavior, non_compliant_behavior, partially_compliant_behavior]


# 示例用法
if __name__ == "__main__":
    # 创建模型实例
    model = BehaviorComplianceModel()
    
    # 获取测试用例
    test_cases = create_test_cases()
    
    # 评估每个测试用例
    for i, behavior in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"测试用例 {i}：{behavior['actor']['name']} 的 {behavior['action']['type']} 行为")
        print(f"{'=' * 80}")
        
        # 计算评分
        report = model.calculate_overall_score(behavior)
        
        # 生成合规性评估报告
        compliance_report = model.generate_compliance_report(report)
        
        # 输出结果
        print(compliance_report)
        
        # 输出JSON格式报告
        print("\n\n")
        print(f"【测试用例 {i} 的JSON格式报告】")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        print("\n\n")
