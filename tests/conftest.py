"""
Shared pytest configuration for Project Chimera tests.
"""

import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture
def project_root_path():
    """Return the project root path."""
    return project_root

@pytest.fixture
def sample_trend_data():
    """Sample trend data matching technical.md specifications."""
    return {
        "trend_id": "trend_yt_987654321",
        "platform": "youtube",
        "title": "AI-Powered Cooking Revolution",
        "description": "Chefs using AI to create novel recipes",
        "metrics": {
            "view_count": 1520000,
            "like_count": 85000,
            "comment_count": 4200,
            "share_count": 31000,
            "velocity_score": 0.87,
            "freshness_score": 0.92
        },
        "content_type": "short_video",
        "duration_seconds": 127,
        "hashtags": ["#AICooking", "#FoodTech", "#Innovation"],
        "detected_at": "2025-02-05T09:45:00Z",
        "confidence": 0.88,
        "opportunity_score": 0.76
    }

@pytest.fixture
def sample_api_error():
    """Sample API error matching technical.md specifications."""
    return {
        "request_id": "req_1234567890abcdef",
        "status": "error",
        "error_code": "API_RATE_LIMIT",
        "error_message": "YouTube API quota exceeded. Retry after 3600 seconds.",
        "retry_after_seconds": 3600,
        "partial_results": [
            {
                "platform": "tiktok",
                "trend_count": 18,
                "status": "complete"
            }
        ]
    }

@pytest.fixture
def valid_trend_request():
    """Valid trend research request matching technical.md."""
    return {
        "request_id": "req_1234567890abcdef",
        "platforms": ["youtube", "tiktok", "instagram"],
        "categories": ["technology", "entertainment", "lifestyle"],
        "timeframe": "24h",
        "max_results": 50,
        "filters": {
            "min_engagement": 1000,
            "max_duration_seconds": 300,
            "exclude_categories": ["politics", "controversial"]
        },
        "agent_id": "agent_research_001",
        "timestamp": "2025-02-05T10:30:00Z"
    }

# Configure pytest to show more detailed output
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

# Add custom command line option
def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run integration tests"
    )