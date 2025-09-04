from langchain_core.messages import AnyMessage
from langchain_gigachat.chat_models.gigachat import GigaChat

from langgraph.graph.message import add_messages

from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from typing import Any, Optional, List, Dict, Annotated
from dotenv import find_dotenv, dotenv_values
from typing import Any, List, Optional,  Literal
import json
import difflib


# инициализация модели
config = dotenv_values(find_dotenv(".env"))
giga = GigaChat(model=config["giga_version"],
                verify_ssl_certs=False,
                profanity_check=False,
                credentials=config['giga_token'],
                scope='GIGACHAT_API_PERS',
                streaming=False,
                temperature=config["giga_temp"],
                timeout=600)

# промпты
# with open("src/data/prompts.json") as f:
#     prompts = json.load(f)


# Состояние графа
class StateHrAgent(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    user_input: str
    intent: Optional[str]
    meta: Dict[str, Any]   

class RouteLLMOut(BaseModel):
    intent: Literal["compatibility", "interview", "clarify", "out_of_scope"]
    relevance: dict = Field(default_factory=dict)  