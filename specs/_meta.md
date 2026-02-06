# Project Chimera – _meta.md

## 1. Vision & North Star
Build a fleet of autonomous AI influencers that:
- Perceive trends (via MCP Resources)
- Reason & plan (FastRender-style Planner → Worker → Judge swarm)
- Create multimodal content
- Publish & engage on social platforms
- Earn & spend crypto via Agentic Commerce (Coinbase AgentKit)

… while remaining safe, auditable, and spec-compliant.

## 2. Core Constraints (Non-negotiable)
- MUST use MCP for ALL external interactions (no direct API calls from agent logic)
- MUST follow FastRender swarm pattern (Planner / Worker / Judge)
- Human-in-the-Loop (HITL) mandatory for < 0.90 confidence OR sensitive topics
- Agents MUST have non-custodial wallets — never store private keys in code
- All published content MUST include AI disclosure (platform native flags)
- Spec-Driven Development: NO implementation before ratified spec

## 3. Out of Scope (for v1)
- On-device / fully local inference (cloud APIs ok)
- Real-time voice interaction
- Physical world actions (only digital social & commerce)

## 4. Glossary
- Chimera Agent = persistent persona + memory + wallet + swarm runtime
- MCP Host = the agent runtime environment
- MCP Server = bridge to external capability (twitter, weaviate, coinbase…)
- FastRender Swarm = Planner → TaskQueue → Workers → Judge → GlobalState