from dataclasses import dataclass


@dataclass(frozen=True)
class SourceMetadata:
    source_id: str
    organization: str
    document_title: str
    source_type: str
    official_url: str | None = None
    publication_date: str | None = None
    updated_date: str | None = None


SOURCE_REGISTRY = {

    "fssai_foscos": SourceMetadata(
        source_id="fssai_foscos",
        organization=(
            "Food Safety and Standards Authority of India"
        ),
        document_title=(
            "Food Business Services / FoSCoS"
        ),
        source_type="government_digital_service",
        official_url="https://foscos.fssai.gov.in/",
    ),

    "fssai": SourceMetadata(
        source_id="fssai",
        organization=(
            "Food Safety and Standards Authority of India"
        ),
        document_title=(
            "Food Safety and Standards "
            "(Licensing and Registration of Food Businesses) Regulations"
        ),
        source_type="government_regulation",
        official_url=None,
    ),

    "kerala_lsgd_trade_license": SourceMetadata(
        source_id="kerala_lsgd_trade_license",
        organization=(
            "Local Self Government Department, "
            "Government of Kerala"
        ),
        document_title="Trade License",
        source_type="government_service_information",
        official_url=(
            "https://lsgd.kerala.gov.in/en/trade-license/"
        ),
    ),

    "kerala_kswift_kya": SourceMetadata(
        source_id="kerala_kswift_kya",
        organization=(
            "Kerala State Industrial Development Corporation / "
            "Government of Kerala"
        ),
        document_title="Know Your Approval",
        source_type="government_approval_discovery_service",
        official_url=(
            "https://kswift.kerala.gov.in/index/kya_qusetionaire.php"
        ),
    ),
}


def get_source_metadata(source_id: str):

    metadata = SOURCE_REGISTRY.get(
        source_id
    )

    if metadata is None:
        raise ValueError(
            f"Unknown source_id: {source_id}"
        )

    return metadata