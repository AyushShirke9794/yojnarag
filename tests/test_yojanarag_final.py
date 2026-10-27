from pathlib import Path

from src.scheme_database import load_schemes
from src.eligibility_engine import EligibilityEngine
from src.eligibility_rules import EligibilityRule, evaluate_rule


def test_scheme_database():
    schemes = load_schemes()
    assert len(schemes) >= 1
    assert any(s.scheme_id == "pm_kisan" for s in schemes)


def test_historical_scheme_safety():
    scheme = next(
        s for s in load_schemes()
        if s.scheme_id == "pm_kisan"
    )
    assert scheme.verification_status == "historical"

    result = EligibilityEngine().check(
        scheme,
        {"age": 25}
    )
    assert result.status == "rules_unverified"


def test_eligibility_rule_pass():
    rule = EligibilityRule(
        rule_id="synthetic_age",
        field="age",
        operator="gte",
        value=18,
        description="Synthetic age condition",
        source_reference="TEST_ONLY"
    )
    assert evaluate_rule(rule, {"age": 25}) is True


def test_eligibility_rule_fail():
    rule = EligibilityRule(
        rule_id="synthetic_age",
        field="age",
        operator="gte",
        value=18,
        description="Synthetic age condition",
        source_reference="TEST_ONLY"
    )
    assert evaluate_rule(rule, {"age": 16}) is False


def test_missing_applicant_information():
    rule = EligibilityRule(
        rule_id="synthetic_age",
        field="age",
        operator="gte",
        value=18,
        description="Synthetic age condition",
        source_reference="TEST_ONLY"
    )
    assert evaluate_rule(rule, {}) is None


def test_vectorstore_files_exist():
    assert Path("data/vectorstore/faiss.index").is_file()
    assert Path("data/vectorstore/metadata.json").is_file()


def test_processed_chunks_exist():
    assert Path(
        "data/processed/pm_kisan_chunks.json"
    ).is_file()


def test_streamlit_app_exists():
    assert Path("app.py").is_file()
