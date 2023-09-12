from pydantic_settings import BaseSettings


class PostConsumeHookSettings(BaseSettings):
    # Documented https://docs.paperless-ngx.com/advanced_usage/#post-consume-script
    # Implemented https://github.com/paperless-ngx/paperless-ngx/blob/dev/src/documents/consumer.py#L236
    document_id: str
