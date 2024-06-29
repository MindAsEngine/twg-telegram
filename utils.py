import logging
from jinja2 import Environment, FileSystemLoader


_jinja_env = Environment(
    loader=FileSystemLoader('templates')
)


async def render_template(template: str, **context) -> str:
    template = _jinja_env.get_template(template)
    return template.render(**context)

