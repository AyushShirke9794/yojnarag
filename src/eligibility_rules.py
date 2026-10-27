from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


RuleOperator = Literal[
    "eq",
    "ne",
    "gt",
    "gte",
    "lt",
    "lte",
    "in",
    "not_in",
]


class EligibilityRule(BaseModel):
    rule_id: str = Field(min_length=1)
    field: str = Field(min_length=1)
    operator: RuleOperator
    value: Any
    description: str = Field(min_length=1)
    source_reference: str = Field(min_length=1)


class SchemeRuleSet(BaseModel):
    scheme_id: str = Field(min_length=1)
    rules: list[EligibilityRule] = Field(min_length=1)

    source_verified: bool = False
    rules_reviewed: bool = False

    @model_validator(mode="after")
    def validate_unique_rule_ids(self):
        ids = [rule.rule_id for rule in self.rules]

        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate eligibility rule IDs.")

        return self


def evaluate_rule(rule: EligibilityRule, applicant: dict):
    if rule.field not in applicant:
        return None

    actual = applicant[rule.field]
    expected = rule.value

    if actual is None:
        return None

    try:
        if rule.operator == "eq":
            return actual == expected

        if rule.operator == "ne":
            return actual != expected

        if rule.operator == "gt":
            return actual > expected

        if rule.operator == "gte":
            return actual >= expected

        if rule.operator == "lt":
            return actual < expected

        if rule.operator == "lte":
            return actual <= expected

        if rule.operator == "in":
            return actual in expected

        if rule.operator == "not_in":
            return actual not in expected

    except (TypeError, ValueError):
        return None

    return None
