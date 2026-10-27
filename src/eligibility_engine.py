from dataclasses import dataclass, field
from typing import Literal

from src.scheme_schema import GovernmentScheme
from src.eligibility_rules import (
    SchemeRuleSet,
    evaluate_rule,
)


EligibilityStatus = Literal[
    "potentially_eligible",
    "not_eligible",
    "insufficient_information",
    "rules_unverified",
]


@dataclass
class EligibilityResult:
    scheme_id: str
    status: EligibilityStatus
    explanation: str
    missing_information: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)


class EligibilityEngine:

    def check(
        self,
        scheme: GovernmentScheme,
        applicant: dict,
        rule_set: SchemeRuleSet | None = None
    ) -> EligibilityResult:

        source = str(scheme.official_source_url)

        if scheme.verification_status != "verified":
            return EligibilityResult(
                scheme_id=scheme.scheme_id,
                status="rules_unverified",
                explanation=(
                    "Current eligibility rules are not verified. "
                    "No eligibility decision can be made."
                ),
                evidence=[source]
            )

        if (
            rule_set is None
            or rule_set.scheme_id != scheme.scheme_id
            or not rule_set.source_verified
            or not rule_set.rules_reviewed
        ):
            return EligibilityResult(
                scheme_id=scheme.scheme_id,
                status="rules_unverified",
                explanation=(
                    "A verified and reviewed eligibility rule set "
                    "is not available for this scheme."
                ),
                evidence=[source]
            )

        missing = []
        failed = []
        passed = []
        evidence = []

        for rule in rule_set.rules:
            outcome = evaluate_rule(rule, applicant)
            evidence.append(rule.source_reference)

            if outcome is None:
                missing.append(rule.field)
            elif outcome is False:
                failed.append(rule.description)
            else:
                passed.append(rule.description)

        if failed:
            return EligibilityResult(
                scheme_id=scheme.scheme_id,
                status="not_eligible",
                explanation=(
                    "The applicant does not satisfy these "
                    "configured conditions: "
                    + "; ".join(failed)
                    + ". This is not an official eligibility decision."
                ),
                evidence=list(dict.fromkeys(evidence))
            )

        if missing:
            return EligibilityResult(
                scheme_id=scheme.scheme_id,
                status="insufficient_information",
                explanation=(
                    "More or correctly typed applicant information "
                    "is required to evaluate all conditions."
                ),
                missing_information=sorted(set(missing)),
                evidence=list(dict.fromkeys(evidence))
            )

        return EligibilityResult(
            scheme_id=scheme.scheme_id,
            status="potentially_eligible",
            explanation=(
                "All configured eligibility conditions passed. "
                "This is not an official approval."
            ),
            evidence=list(dict.fromkeys(evidence))
        )
