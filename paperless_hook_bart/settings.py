from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class PaperlessServerSettings(BaseSettings):
    """
    In order to talk to the Paperless-ngx API, we need a token. This isn't given to the hook by Paperless, so for now
    let's assume it's just given independently as an environment variable.
    """

    paperless_base_url: AnyHttpUrl
    paperless_token: str


class PostConsumeHookSettings(BaseSettings):
    # Documented https://docs.paperless-ngx.com/advanced_usage/#post-consume-script
    # Implemented https://github.com/paperless-ngx/paperless-ngx/blob/dev/src/documents/consumer.py#L236
    document_id: str
