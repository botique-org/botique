from .custom_knowledge_bot import CustomKnowledgeBot
from bot_registry import register_bot

register_bot("custom_knowledge_bot", CustomKnowledgeBot)
