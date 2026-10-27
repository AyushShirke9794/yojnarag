from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

SchemeCategory = Literal[
    "Education",
    "Agriculture",
    "Employment",
    "Women & Children",
    "Housing",
    "Healthcare",
]

class GovernmentScheme(BaseModel):
    scheme_id: str = Field(min_length=1)
    scheme_name: str = Field(min_length=1)
    category: SchemeCategory
    description: str = Field(min_length=1)
    eligibility_text: str = Field(min_length=1)
    benefits: str = Field(min_length=1)
    required_documents: list[str] = Field(default_factory=list)
    official_source_url: HttpUrl

    verification_status: Literal[
        "pending",
        "verified",
        "historical"
    ] = "pending"

    source_document_date: date | None = None
    source_verified_date: date | None = None

    source_document_title: str | None = None
    verification_notes: str | None = None