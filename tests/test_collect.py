import pytest
from src.collect.federal_register import FederalRegisterCollector

@pytest.fixture
def collector():
    return FederalRegisterCollector('https://www.federalregister.gov/api/v1')

def test_collect_returns_list(collector):
    docs = collector.collect(days=7)
    assert isinstance(docs, list)

def test_documents_have_required_fields(collector):
    docs = collector.collect(days=1)
    if docs:
        doc = docs[0]
        assert "title" in doc
        assert "abstract" in doc
        assert "document_type" in doc
        assert "publication_date" in doc
        assert "html_url" in doc

def test_filter_removes_irrelevant(collector):
    mock_docs = [
        {"title": "Regulation of Tobacco Products", "document_type": "Notice"},
        {"title": "IND Safety Reporting Guidelines", "document_type": "Rule"},
        {"title": "Meeting of the Food Additive Board", "document_type": "Proposed Rule"}
    ]
    filtered = collector.filter_relevant_types(mock_docs)
    assert len(filtered) == 1
    assert "IND Safety" in filtered[0]["title"]
