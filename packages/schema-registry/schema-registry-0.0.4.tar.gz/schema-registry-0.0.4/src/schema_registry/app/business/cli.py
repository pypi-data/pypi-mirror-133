from schema_registry.config import get_configuration
from schema_registry.registries.HttpRegistry import EnrichingHttpSchemaRegistry


def get_registry(profile: str = "default") -> EnrichingHttpSchemaRegistry:
    config = get_configuration(profile)
    return EnrichingHttpSchemaRegistry(url=config.schema_registry_url)
