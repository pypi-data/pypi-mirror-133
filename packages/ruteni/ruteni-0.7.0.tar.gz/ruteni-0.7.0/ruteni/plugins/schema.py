from starlette.schemas import SchemaGenerator

schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Example APINode", "version": "1.0"}}
)
