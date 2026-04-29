import os
import pytest
from src.pipeline import Pipeline
from config.settings import Settings

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake")
    monkeypatch.setenv("SENDGRID_API_KEY", "fake")
    monkeypatch.setenv("SENDER_EMAIL", "fake@fake.com")
    monkeypatch.setenv("RECIPIENT_EMAIL", "fake@fake.com")

def test_pipeline_initializes(mock_env):
    pipeline = Pipeline()
    assert isinstance(pipeline.settings, Settings)

def test_pipeline_loads_profiles(mock_env):
    pipeline = Pipeline()
    # It should find at least the asco_oncology.yaml file created during setup
    assert len(pipeline.profiles) >= 1
