from functools import lru_cache
from typing import Any, Dict, Optional, Set

from requests_toolbelt.sessions import BaseUrlSession

from schema_registry.config import get_logger
from schema_registry.registries.entities import VersionedType


class HttpSchemaRegistry:
    def __init__(self, *, url: str) -> None:
        self.url = url
        self.session = BaseUrlSession(base_url=self.url)
        self.log = get_logger(self.__class__.__name__)
        self._namespaces: Set[str] = set()
        self._types: Dict[str, Set[VersionedType]] = {}

    @lru_cache(maxsize=128)
    def get(
        self, *, namespace: str, type: str, version: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        if version is None:
            self.log.debug("Fetching version")
            types_of_namespace = self.types(namespace=namespace)

            found_types = list(filter(lambda x: x.name == type, types_of_namespace))
            found_types.sort()

            self.log.debug(f"Found {found_types}")

            version = found_types[-1].version

            if len(found_types) != 1:
                self.log.info(
                    f"Found {len(found_types)} versions using latest version ({version})"
                )

        req = self.session.get(f"/registry/{namespace}/{type}/{version}/schema.json")

        self.log.debug(req)
        if req.status_code != 200:
            return None
        return req.json()  # type: ignore

    @property
    def namespaces(self) -> Set[str]:
        if not self._namespaces:
            self._initialize_namespaces()
        return self._namespaces

    def types(self, *, namespace: str) -> Set[VersionedType]:
        preliminary_result = self._types.get(namespace)

        if preliminary_result is None:
            self.log.debug(f"Fetching types for {namespace} from remote")
            self._initialize_types(namespace)

        return self._types.get(namespace, set())

    def _initialize_namespaces(self) -> None:
        index = self.session.get("/registry/index.json").json()
        schemes = index.get("schemes", [])

        self.log.debug(schemes)

        self._namespaces = {schema["ns"] for schema in schemes}

    def _initialize_types(self, namespace: str) -> None:
        index = self.session.get("/registry/index.json").json()
        schemes = index.get("schemes", [])
        filtered = filter(lambda x: x["ns"] == namespace, schemes)

        self._types[namespace] = {
            VersionedType(name=schema["type"], version=schema["version"])
            for schema in filtered
        }

    def refresh(self) -> None:
        self._initialize_namespaces()
        self._types = {}
        self.get.cache_clear()

    # TODO Transformation stuff
