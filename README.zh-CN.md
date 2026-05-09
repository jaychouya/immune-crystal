# immune-crystal

[![CI](https://github.com/jaychouya/immune-crystal/actions/workflows/ci.yml/badge.svg)](https://github.com/jaychouya/immune-crystal/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-22c55e)](#roadmap)
[![Enterprise](https://img.shields.io/badge/Focus-Enterprise%20AI-7c3aed)](#企业场景)

[English](./README.md) | 简体中文

通用企业级 AI 免疫记忆共生体：将动态领域隔离与时间晶体式记忆自修复合并为一个可落地系统。

> 让企业 AI 既安全、又有状态、还能审计追溯。

## 一分钟演示

![immune-crystal demo](./assets/demo/immune-crystal-demo.gif)

流程示意（约 60 秒）。本地复现：`python examples/generic/bootstrap_and_chat.py`。重新生成 GIF：`pip install -e ".[dev]"` 后执行 `python scripts/generate_demo_gif.py`。完整录制说明见 [`assets/demo/README.md`](./assets/demo/README.md)。

## 你会得到什么

- 任意领域隔离（`customer_support`、`engineering`、`hr`、`finance` 等）
- 跨域泄露与提示词注入拦截
- 周期强化可信记忆、衰减噪声记忆
- 每次响应返回审计信号：`purity`、`lineage`、`audit_id`

## 可信度信号

| 信号 | 位置 |
| --- | --- |
| 法律可用性 | [`LICENSE`](./LICENSE) |
| 安全披露流程 | [`SECURITY.md`](./SECURITY.md) |
| 贡献规范 | [`CONTRIBUTING.md`](./CONTRIBUTING.md) |
| 版本变更 | [`CHANGELOG.md`](./CHANGELOG.md) |
| 企业 PoC 检查清单 | [`docs/enterprise-evaluation.md`](./docs/enterprise-evaluation.md) |

## 为什么做这个

企业大模型常见两类失败：

- 知识污染（跨域信息泄露）
- 长会话记忆混乱（漂移、冲突、噪声积累）

immune-crystal 同时提供防御与修复双引擎：

- Domain Registry
- T-Cell detector
- B-Cell memory pool
- Time Crystal oscillator
- Audit lineage

## 对比（vs RAG / Guardrails）

| 能力 | 传统 RAG | 仅 Guardrails | immune-crystal |
| --- | --- | --- | --- |
| 跨域隔离 | 部分 | 部分 | 强 |
| 注入防护 | 弱 | 强 | 强 |
| 长会话记忆修复 | 弱 | 无 | 强 |
| 冲突状态处理 | 弱 | 规则式 | 动态隔离相 |
| 输出可追溯性 | 中 | 中 | 强（`purity`+`lineage`） |

## 快速启动

```bash
pip install -e .
uvicorn api.app:app --host 0.0.0.0 --port 8000
```

```bash
cd web
npm install
npm run dev
```

## 5 分钟接入

### 1）注入企业知识

```bash
curl -X POST "http://localhost:8000/inject" \
  -H "Content-Type: application/json" \
  -d "{\"content\":\"客服仅可使用公开资料和授权工单。\",\"domain\":\"customer_support\",\"compliance_tags\":[\"support-policy\",\"least-privilege\"]}"
```

### 2）业务请求先走免疫层

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"客服是否可访问研发密钥？\",\"domain\":\"customer_support\"}"
```

### 3）治理与观测

```bash
curl "http://localhost:8000/domains"
curl "http://localhost:8000/crystal/state"
curl "http://localhost:8000/audit"
```

### 可选：批量初始化

```bash
curl -X POST "http://localhost:8000/bootstrap" \
  -H "Content-Type: application/json" \
  -d "{\"items\":[{\"domain\":\"customer_support\",\"content\":\"客服仅可使用公开资料。\"},{\"domain\":\"engineering\",\"content\":\"研发令牌属于高敏信息。\"}]}"
```

## API

- `POST /inject`
- `POST /bootstrap`
- `POST /chat`
- `POST /poison/test`
- `GET /domains`
- `GET /crystal/state`
- `GET /audit`
- `GET /audit/{id}`
- `POST /crystal/reset/{cell_id}`

## 示例

```bash
python examples/generic/bootstrap_and_chat.py
python examples/finance/loan_conflict.py
python examples/medical/cross_domain_poison.py
```

## 基准测试

```bash
python benchmarks/pollution_intercept.py
python benchmarks/memory_repair.py
python benchmarks/audit_latency.py
```

## 企业场景

- 内部 Copilot 安全网关
- 跨团队 RAG 访问保护层
- 长任务 Agent 记忆治理层
- 合规审计证据层

## 信任与治理

- 安全报告：[`SECURITY.md`](./SECURITY.md)
- 企业评估：[`docs/enterprise-evaluation.md`](./docs/enterprise-evaluation.md)
- 演示录制指南：[`assets/demo/README.md`](./assets/demo/README.md)
- 截图占位指南：[`assets/screenshots/README.md`](./assets/screenshots/README.md)

## Roadmap

- [ ] 领域画像导入导出
- [ ] 企业策略 DSL
- [ ] 流式 API 与异步任务
- [ ] 多租户看板
- [ ] 更大规模基准集

## 贡献方式

- 提交 Issue 时附：场景、预期行为、最小复现请求
- 关键逻辑改动请附 benchmark 或测试
- 尽量保持 API 向后兼容
