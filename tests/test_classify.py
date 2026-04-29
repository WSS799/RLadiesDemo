import pytest
from unittest.mock import Mock, patch
from src.classify.engine import ClassificationEngine

@pytest.fixture
def engine():
    profile = {
        "therapeutic_areas": ["oncology"],
        "trial_phases": ["Phase II"],
        "drug_modalities": ["biologic"],
        "regulatory_domains": ["safety reporting"],
        "jurisdictions": ["FDA"]
    }
    return ClassificationEngine(api_key="fake", model="fake-model", profile=profile)

@patch('anthropic.resources.messages.Messages.create')
def test_classification_returns_valid_json(mock_create, engine):
    mock_response = Mock()
    mock_response.content = [Mock(text='{"classification": "CRITICAL", "confidence": 0.9, "rationale": "Testing", "action_required": "None", "regulatory_domain": "General"}')]
    mock_create.return_value = mock_response

    doc = {
        "title": "Test Doc",
        "document_type": "Rule",
        "publication_date": "2026-04-29",
        "abstract": "Test abstract"
    }

    result = engine.classify_document(doc)
    assert "classification" in result

@patch('anthropic.resources.messages.Messages.create')
def test_classification_values(mock_create, engine):
    mock_response = Mock()
    mock_response.content = [Mock(text='{"classification": "IMPORTANT"}')]
    mock_create.return_value = mock_response

    doc = {"title": "Doc", "document_type": "Rule", "publication_date": "2026-04-29", "abstract": ""}
    result = engine.classify_document(doc)

    valid_classifications = ["CRITICAL", "IMPORTANT", "INFORMATIONAL", "IRRELEVANT", "PARSE_ERROR"]
    assert result.get("classification") in valid_classifications
