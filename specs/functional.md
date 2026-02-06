# Functional Specification – Chimera Agent Behaviors

## Perception & Sensing
As a Chimera Agent  
I want to poll configured MCP Resources every 5–30 min  
So that I detect new mentions, trends, news relevant to my niche  

Acceptance:
- Resources: twitter://mentions, news://ethiopia/fashion, market://crypto/prices
- Semantic filter (Gemini Flash) scores ≥ 0.75 → creates Planner task
- Lower scores → discarded silently

## Planning & Decomposition
As Planner  
I want to decompose high-level goals into DAG of atomic tasks  
So that Workers can execute in parallel

Acceptance:
- Input: natural language goal + current state + memories
- Output: JSON array of tasks with priority, dependencies, required tools

## Content Creation
As Worker  
I want to generate platform-optimized content package  
So that Judge can review before publishing

Acceptance:
- Input: task JSON + persona + memories + trend context
- Output: { text, image_prompts, video_tier: "portrait"|"full", predicted_engagement }
- MUST attach character_reference_id for image/video consistency

## Commerce & Budget
As CFO Judge  
I want to block transactions > daily limit OR suspicious pattern  
So that agent cannot go bankrupt or get hacked

Acceptance:
- Check Redis daily_spend
- Max daily: configurable per agent (default $50 USDC)
- Escalate > $10 single tx or >3 tx/hour