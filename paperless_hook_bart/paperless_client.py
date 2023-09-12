import requests
from pydantic import BaseModel


class PaperlessDocument(BaseModel):
    id: int
    content: str


class PaperlessClient:
    """
    An incomplete client around the Paperless-ngx REST API. Documented here:
    https://docs.paperless-ngx.com/api/
    """

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")  # if a trailing slash is given, chop it
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Token {token}"

    def get_document(self, document_id: int) -> PaperlessDocument:
        full_url = f"{self.base_url}/api/documents/{document_id}/?format=json"
        resp = self.session.get(full_url)
        resp.raise_for_status()
        return PaperlessDocument.parse_raw(resp.content)
