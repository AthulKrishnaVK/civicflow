from pydantic import BaseModel


class SourceMetadata(BaseModel):
    source_id: str
    organization: str
    document_title: str
    source_type: str
    official_url: str | None = None
    publication_date: str | None = None
    updated_date: str | None = None
    retrieved_date: str | None = None