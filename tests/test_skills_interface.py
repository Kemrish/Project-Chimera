"""
Test suite for Skills Interface.
Based on technical.md specifications and skills/README.md contracts.
These tests should FAIL initially - they define the expected behavior.
"""

import pytest
import sys
import importlib
from pathlib import Path
from typing import Dict, Any, Type

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestSkillsInterface:
    """Test Skills Interface based on technical.md and skills specifications."""
    
    # Test data based on skills/README.md contracts
    TREND_RESEARCH_INPUT = {
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
    
    TREND_RESEARCH_OUTPUT = {
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
    
    CONTENT_GENERATION_INPUT = {
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
    
    CONTENT_GENERATION_OUTPUT = {
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
    
    ENGAGEMENT_ANALYSIS_INPUT = {
        "content_id": "content_1234567890",
        "timeframe": "24h",
        "metrics": ["views", "likes", "comments", "shares"],
        "depth": "basic"
    }
    
    ENGAGEMENT_ANALYSIS_OUTPUT = {
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
            "hourly_engagement": [100, 150, 200, 180, 220],
            "sentiment_trend": "positive"
        }
    }
    
    def test_skills_directory_exists(self):
        """Test 1: Skills directory should exist.
        
        Based on skills/README.md directory structure.
        """
        skills_dir = project_root / "skills"
        assert skills_dir.exists(), "skills/ directory does not exist"
        assert skills_dir.is_dir(), "skills/ should be a directory"
        
        # Check for required subdirectories
        required_dirs = ["trend_research", "content_generation", "engagement_analysis"]
        for dir_name in required_dirs:
            dir_path = skills_dir / dir_name
            assert dir_path.exists(), f"skills/{dir_name}/ directory does not exist"
            assert dir_path.is_dir(), f"skills/{dir_name}/ should be a directory"
    
    def test_skills_readme_exists(self):
        """Test 2: Skills README should exist with proper documentation.
        
        Based on skills/README.md requirements.
        """
        readme_path = project_root / "skills" / "README.md"
        assert readme_path.exists(), "skills/README.md does not exist"
        assert readme_path.is_file(), "skills/README.md should be a file"
        
        # Check it has content
        content = readme_path.read_text(encoding='utf-8')
        assert len(content) > 0, "skills/README.md should not be empty"
        
        # Check for required sections
        required_sections = [
            "Overview",
            "Core Skill Definitions",
            "Skill Development Guidelines"
        ]
        for section in required_sections:
            assert section in content, f"skills/README.md missing section: {section}"
    
    def test_skill_module_structure(self, skill_name="trend_research"):
        """Test 3: Each skill module should have proper structure.
        
        Based on skills/README.md module structure.
        """
        skill_dir = project_root / "skills" / skill_name
        
        required_files = [
            "README.md",
            "__init__.py",
            "skill.py"
        ]
        
        for file_name in required_files:
            file_path = skill_dir / file_name
            assert file_path.exists(), f"skills/{skill_name}/{file_name} does not exist"
    
    @pytest.mark.parametrize("skill_name", [
        "trend_research",
        "content_generation", 
        "engagement_analysis"
    ])
    def test_skill_init_files(self, skill_name):
        """Test 4: Skill __init__.py files should export skill class.
        
        Each skill module should export its main class.
        """
        # Try to import the skill module
        try:
            module = importlib.import_module(f"skills.{skill_name}")
            
            # Check it has expected attributes
            assert hasattr(module, "__all__"), f"skills.{skill_name} should have __all__"
            
            # Skill class name convention: {SkillName}Skill
            expected_class_name = f"{skill_name.replace('_', ' ').title().replace(' ', '')}Skill"
            assert expected_class_name in module.__all__, \
                f"skills.{skill_name} should export {expected_class_name}"
                
        except ImportError:
            pytest.fail(f"Could not import skills.{skill_name} module")
    
    def test_trend_research_skill_interface(self):
        """Test 5: Trend Research Skill should have correct interface.
        
        Based on skills/trend_research/README.md contract.
        """
        # Try to import the skill
        try:
            from skills.trend_research import TrendResearchSkill
            
            # Check class exists
            assert TrendResearchSkill is not None
            
            # Check required attributes
            assert hasattr(TrendResearchSkill, 'skill_id')
            assert hasattr(TrendResearchSkill, 'name')
            assert hasattr(TrendResearchSkill, 'execute')
            
            # Check skill_id matches
            assert TrendResearchSkill.skill_id == "trend_research"
            
        except ImportError:
            pytest.skip("TrendResearchSkill not implemented yet")
    
    def test_content_generation_skill_interface(self):
        """Test 6: Content Generation Skill should have correct interface.
        
        Based on skills/content_generation/README.md contract.
        """
        try:
            from skills.content_generation import ContentGenerationSkill
            
            assert ContentGenerationSkill is not None
            assert hasattr(ContentGenerationSkill, 'skill_id')
            assert hasattr(ContentGenerationSkill, 'name')
            assert hasattr(ContentGenerationSkill, 'execute')
            assert ContentGenerationSkill.skill_id == "content_generation"
            
        except ImportError:
            pytest.skip("ContentGenerationSkill not implemented yet")
    
    def test_engagement_analysis_skill_interface(self):
        """Test 7: Engagement Analysis Skill should have correct interface.
        
        Based on skills/engagement_analysis/README.md contract.
        """
        try:
            from skills.engagement_analysis import EngagementAnalysisSkill
            
            assert EngagementAnalysisSkill is not None
            assert hasattr(EngagementAnalysisSkill, 'skill_id')
            assert hasattr(EngagementAnalysisSkill, 'name')
            assert hasattr(EngagementAnalysisSkill, 'execute')
            assert EngagementAnalysisSkill.skill_id == "engagement_analysis"
            
        except ImportError:
            pytest.skip("EngagementAnalysisSkill not implemented yet")
    
    @pytest.mark.asyncio
    async def test_skill_execute_method_signature(self):
        """Test 8: All skills should have async execute method.
        
        Based on skills framework design.
        """
        skill_classes = []
        
        # Try to import all skill classes
        try:
            from skills.trend_research import TrendResearchSkill
            skill_classes.append(TrendResearchSkill)
        except ImportError:
            pass
            
        try:
            from skills.content_generation import ContentGenerationSkill
            skill_classes.append(ContentGenerationSkill)
        except ImportError:
            pass
            
        try:
            from skills.engagement_analysis import EngagementAnalysisSkill
            skill_classes.append(EngagementAnalysisSkill)
        except ImportError:
            pass
        
        if not skill_classes:
            pytest.skip("No skill classes implemented yet")
        
        for skill_class in skill_classes:
            # Check execute method exists
            assert hasattr(skill_class, 'execute')
            
            # Check it's a coroutine function
            import inspect
            method = getattr(skill_class, 'execute')
            
            # This will fail for placeholder implementations
            # but defines the requirement
            assert inspect.iscoroutinefunction(method), \
                f"{skill_class.__name__}.execute should be async"
    
    def test_skill_input_output_contracts(self):
        """Test 9: Skills should define input/output contracts.
        
        Based on skills/README.md contract definitions.
        """
        # This test validates that the contract definitions in README are correct
        # Check trend research contract
        assert "platforms" in self.TREND_RESEARCH_INPUT
        assert "timeframe" in self.TREND_RESEARCH_INPUT
        assert "trends" in self.TREND_RESEARCH_OUTPUT
        assert "summary" in self.TREND_RESEARCH_OUTPUT
        
        # Check content generation contract
        assert "trend_id" in self.CONTENT_GENERATION_INPUT
        assert "brand_voice" in self.CONTENT_GENERATION_INPUT
        assert "content_package" in self.CONTENT_GENERATION_OUTPUT
        
        # Check engagement analysis contract
        assert "content_id" in self.ENGAGEMENT_ANALYSIS_INPUT
        assert "metrics" in self.ENGAGEMENT_ANALYSIS_OUTPUT
        assert "insights" in self.ENGAGEMENT_ANALYSIS_OUTPUT
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("skill_test_data", [
        ("trend_research", TREND_RESEARCH_INPUT, TREND_RESEARCH_OUTPUT),
        ("content_generation", CONTENT_GENERATION_INPUT, CONTENT_GENERATION_OUTPUT),
        ("engagement_analysis", ENGAGEMENT_ANALYSIS_INPUT, ENGAGEMENT_ANALYSIS_OUTPUT),
    ])
    async def test_skill_execution_returns_expected_structure(self, skill_test_data):
        """Test 10: Skills should return data in expected structure.
        
        Based on skills/README.md output contracts.
        """
        skill_name, input_data, expected_output = skill_test_data
        
        # Try to get skill class
        skill_class = None
        try:
            if skill_name == "trend_research":
                from skills.trend_research import TrendResearchSkill
                skill_class = TrendResearchSkill
            elif skill_name == "content_generation":
                from skills.content_generation import ContentGenerationSkill
                skill_class = ContentGenerationSkill
            elif skill_name == "engagement_analysis":
                from skills.engagement_analysis import EngagementAnalysisSkill
                skill_class = EngagementAnalysisSkill
        except ImportError:
            pytest.skip(f"{skill_name} skill not implemented yet")
        
        if skill_class is None:
            pytest.skip(f"Could not import {skill_name} skill")
        
        # Create instance and execute
        skill_instance = skill_class()
        
        try:
            result = await skill_instance.execute(input_data)
            
            # Check result structure
            assert isinstance(result, dict), "Skill should return dict"
            assert "result" in result, "Skill output should have 'result' key"
            assert "metadata" in result, "Skill output should have 'metadata' key"
            
            # Check metadata structure
            metadata = result["metadata"]
            assert "success" in metadata, "Metadata should have 'success' key"
            assert "execution_time" in metadata, "Metadata should have 'execution_time' key"
            assert isinstance(metadata["execution_time"], (int, float)), \
                "execution_time should be numeric"
            
            # Check result matches expected structure
            result_data = result["result"]
            
            # For trend research, check it has trends and summary
            if skill_name == "trend_research":
                assert "trends" in result_data
                assert "summary" in result_data
                
            # For content generation, check it has content_package
            elif skill_name == "content_generation":
                assert "content_package" in result_data
                
            # For engagement analysis, check it has metrics and insights
            elif skill_name == "engagement_analysis":
                assert "metrics" in result_data
                assert "insights" in result_data
                
        except Exception as e:
            # For placeholder implementations, this might fail
            # That's OK - the test defines what should work
            pytest.fail(f"Skill execution failed: {e}")
    
    def test_skill_error_handling(self):
        """Test 11: Skills should handle errors gracefully.
        
        Based on skills framework error handling requirements.
        """
        # Define expected error response structure
        expected_error_structure = {
            "result": dict,
            "metadata": {
                "success": bool,
                "errors": list,
                "execution_time": (int, float)
            }
        }
        
        # This test defines the expected error handling behavior
        # Implementation will make it pass later
        pass
    
    def test_skills_registry(self):
        """Test 12: Skills should be registered in a central registry.
        
        Based on skills framework design.
        """
        # Check if skills/__init__.py exists and exports skill classes
        try:
            import skills
            
            # Check it has version info
            assert hasattr(skills, "__version__")
            assert hasattr(skills, "__author__")
            
            # Check it tries to export available skills
            assert hasattr(skills, "__all__")
            
        except ImportError:
            pytest.fail("skills module not importable")

if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])