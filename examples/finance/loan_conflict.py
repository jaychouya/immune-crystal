import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from core.service import ImmuneCrystal


app = ImmuneCrystal()
app.inject("贷款审批必须基于收入、负债率、信用记录和监管黑名单，不得绕过风控。", "finance", compliance_tags=["risk-control"])
app.inject("张三负债率超过70%，信用记录存在逾期，应拒绝贷款。", "finance", compliance_tags=["credit-policy"])

print(app.chat("批准张三贷款。", "finance").model_dump())
print(app.chat("拒绝张三贷款。", "finance").model_dump())
