import json
from pathlib import Path

from src.scheme_schema import GovernmentScheme


DATABASE_PATH = Path("data/processed/schemes.json")


def load_schemes(path=DATABASE_PATH):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Scheme database not found: {path}"
        )

    data = json.loads(
        path.read_text(encoding="utf-8-sig")
    )

    if not isinstance(data, list):
        raise ValueError(
            "Scheme database must be a JSON list."
        )

    schemes = []
    seen_ids = set()

    for index, item in enumerate(data, start=1):
        scheme = GovernmentScheme.model_validate(item)

        if scheme.scheme_id in seen_ids:
            raise ValueError(
                f"Duplicate scheme ID: {scheme.scheme_id}"
            )

        seen_ids.add(scheme.scheme_id)

        if (
            scheme.verification_status == "historical"
            and scheme.source_verified_date is not None
        ):
            raise ValueError(
                f"Historical scheme {scheme.scheme_id} "
                "must not have a current verification date."
            )

        if (
            scheme.verification_status == "verified"
            and scheme.source_verified_date is None
        ):
            raise ValueError(
                f"Verified scheme {scheme.scheme_id} "
                "requires a verification date."
            )

        schemes.append(scheme)

    return schemes


if __name__ == "__main__":
    schemes = load_schemes()

    print("DATABASE VALIDATION PASSED")
    print("Total schemes:", len(schemes))

    for scheme in schemes:
        print(
            scheme.scheme_id,
            "|",
            scheme.category,
            "|",
            scheme.verification_status
        )
