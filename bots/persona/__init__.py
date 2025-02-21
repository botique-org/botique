from .persona import Persona
from bot_registry import register_bot

# Register the Persona bot under the name "persona"
register_bot("persona", Persona)
