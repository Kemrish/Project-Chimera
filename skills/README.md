# Project Chimera: Skills Framework

## Overview

Skills are reusable capability packages that enable autonomous agents to perform specific tasks. This framework provides a standardized way to define, implement, and use skills within the Project Chimera ecosystem.

## Directory Structure

skills/
├── README.md                    # This file
├── __init__.py                  # Skill registry and utilities
│
├── trend_research/              # Trend research skills
│   ├── README.md                # Skill documentation
│   ├── __init__.py              # Skill registration
│   ├── skill.py                 # Main skill implementation
│   ├── models.py                # Data models
│   └── tests/                   # Skill tests
│       └── test_skill.py        # Unit tests
│
├── content_generation/          # Content creation skills
│   ├── README.md
│   ├── __init__.py
│   ├── skill.py
│   ├── models.py
│   └── tests/
│       └── test_skill.py
│
└── engagement_analysis/         # Engagement analysis skills
    ├── README.md
    ├── __init__.py
    ├── skill.py
    ├── models.py
    └── tests/
        └── test_skill.py
```

## Core Skill Definitions

### 1. Trend Research Skill

**Directory:** `skills/trend_research/`

**Purpose:** Research trends across social media platforms

**Input Contract:**
```json
{
  "platforms": ["youtube", "tiktok", "instagram"],
  "categories": ["technology", "entertainment", "lifestyle"],
  "timeframe": "24h",
  "max_results": 50,
  "filters": {
    "min_engagement": 1000,
    "max_duration_seconds": 300,
    "exclude_categories": ["politics", "controversial"]
  }
}
```

**Output Contract:**
```json
{
  "trends": [
    {
      "trend_id": "trend_yt_123456789",
      "platform": "youtube",
      "title": "AI-Powered Cooking Revolution",
      "metrics": {
        "view_count": 1520000,
        "velocity_score": 0.87,
        "freshness_score": 0.92
      },
      "confidence": 0.88,
      "opportunity_score": 0.76
    }
  ],
  "summary": {
    "total_trends": 42,
    "average_velocity": 0.65,
    "top_category": "technology"
  }
}
```

### 2. Content Generation Skill

**Directory:** `skills/content_generation/`

**Purpose:** Generate platform-optimized content from trends

**Input Contract:**
```json
{
  "trend_id": "trend_yt_987654321",
  "brand_voice": {
    "tone": "professional_enthusiastic",
    "target_audience": "tech_early_adopters",
    "key_messages": ["innovation", "practical_application"]
  },
  "content_requirements": {
    "platforms": ["youtube", "tiktok"],
    "formats": ["short_video"],
    "duration_seconds": {
      "min": 60,
      "max": 180
    }
  },
  "variations": 3
}
```

**Output Contract:**
```json
{
  "content_package": {
    "package_id": "pkg_7890123456",
    "core_concept": "AI in everyday cooking",
    "variations": [
      {
        "variation_id": "var_001",
        "title": "How AI is Revolutionizing Home Cooking",
        "script": "Hey everyone! Today we're exploring how AI is transforming home cooking...",
        "platform_optimizations": {
          "youtube": {
            "tags": ["AI", "cooking", "technology"],
            "description": "Discover how artificial intelligence is changing home cooking..."
          },
          "tiktok": {
            "hashtags": ["#AICooking", "#FoodHack"],
            "caption": "Your fridge is about to get SMART! 🧠🍳 #AI #Cooking"
          }
        }
      }
    ]
  }
}
```

### 3. Engagement Analysis Skill

**Directory:** `skills/engagement_analysis/`

**Purpose:** Analyze audience engagement and provide insights

**Input Contract:**
```json
{
  "content_id": "content_1234567890",
  "timeframe": "24h",
  "metrics": ["views", "likes", "comments", "shares"],
  "depth": "basic"
}
```

**Output Contract:**
```json
{
  "metrics": {
    "view_count": 1520000,
    "like_count": 85000,
    "comment_count": 4200,
    "share_count": 31000,
    "engagement_rate": 0.045
  },
  "insights": [
    {
      "type": "performance",
      "description": "Content performed 25% above average for this category",
      "confidence": 0.85
    },
    {
      "type": "recommendation",
      "description": "Consider creating follow-up content on AI kitchen gadgets",
      "priority": "medium"
    }
  ],
  "trends": {
    "hourly_engagement": [...],
    "sentiment_trend": "positive"
  }
}
```

## Skill Development Guidelines

### Creating a New Skill

1. **Create Skill Directory:**
   ```bash
   mkdir -p skills/new_skill/tests
   ```

2. **Define Input/Output Models:**
   ```python
   # skills/new_skill/models.py
   from pydantic import BaseModel
   from typing import List, Optional
   
   class NewSkillInput(BaseModel):
       required_param: str
       optional_param: Optional[str] = None
   
   class NewSkillOutput(BaseModel):
       result: dict
       metadata: dict
   ```

3. **Implement Skill Logic:**
   ```python
   # skills/new_skill/skill.py
   from .models import NewSkillInput, NewSkillOutput
   
   class NewSkill:
       skill_id = "new_skill"
       name = "New Skill"
       
       async def execute(self, input_data: NewSkillInput) -> NewSkillOutput:
           # Skill implementation
           pass
   ```

4. **Register Skill:**
   ```python
   # skills/new_skill/__init__.py
   from .skill import NewSkill
   ```

### Testing Skills

Each skill must include comprehensive tests:
```python
# skills/trend_research/tests/test_skill.py
import pytest
from skills.trend_research import TrendResearchSkill

@pytest.mark.asyncio
async def test_trend_research_basic():
    skill = TrendResearchSkill()
    input_data = {
        "platforms": ["youtube"],
        "timeframe": "24h"
    }
    result = await skill.execute(input_data)
    assert result.metadata["success"] == True
    assert "trends" in result.result
```

## Skill Execution Protocol

### Execution Flow
1. **Input Validation:** Validate input against schema
2. **Skill Execution:** Run skill logic
3. **Result Processing:** Format output
4. **Error Handling:** Catch and handle errors
5. **Logging:** Record execution details

### Error Handling
Skills should return structured error information:
```json
{
  "result": {},
  "metadata": {
    "success": false,
    "errors": ["API connection failed"],
    "execution_time": 2.5,
    "retry_after": 60
  }
}
```

## Dependencies

### Required Packages
```toml
# pyproject.toml dependencies for skills
pydantic = "^2.0.0"
httpx = "^0.25.0"
tenacity = "^8.2.0"
```

### Environment Variables
```bash
# Required for skills
YOUTUBE_API_KEY=your_key_here
TIKTOK_ACCESS_TOKEN=your_token_here
INSTAGRAM_ACCESS_TOKEN=your_token_here
OPENAI_API_KEY=your_key_here
```

## Next Steps

1. **Week 1:** Implement skill registry and base classes
2. **Week 2:** Complete trend research skill implementation
3. **Week 3:** Complete content generation skill implementation
4. **Week 4:** Complete engagement analysis skill implementation
5. **Week 5:** Integration testing and performance optimization

## Support

For questions about skill development:
- Review existing skill examples
- Check skill design guidelines
- Contact skills maintainer
```
