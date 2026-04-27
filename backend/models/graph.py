from pydantic import BaseModel, ConfigDict, Field, field_validator


class Edge(BaseModel):
    source: str = Field(..., min_length=1)
    target: str = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")

    @field_validator("source", "target")
    @classmethod
    def strip_endpoint(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Un sommet d'arete ne peut pas etre vide")
        return value


class GraphRequest(BaseModel):
    nodes: list[str] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)
    directed: bool = False

    model_config = ConfigDict(extra="forbid")

    @field_validator("nodes")
    @classmethod
    def strip_nodes(cls, values: list[str]) -> list[str]:
        cleaned_nodes = []
        for node in values:
            node = node.strip()
            if not node:
                raise ValueError("Un sommet ne peut pas etre vide")
            cleaned_nodes.append(node)
        return cleaned_nodes
