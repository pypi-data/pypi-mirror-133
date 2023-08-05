from schema_registry.config import get_configuration
from schema_registry.registries import HttpSchemaRegistry


def get_registry(profile: str = "default") -> HttpSchemaRegistry:
    config = get_configuration(profile)
    return HttpSchemaRegistry(url=config.schema_registry_url)
