from typing import Literal
from langgraph.types import Command, interrupt
from langchain_core.messages import AIMessage, HumanMessage
from src.utils.graph_utils import StateHrAgent, giga, RouteLLMOut
from src.utils.logger import logger

from pydantic import BaseModel, Field, ValidationError
import json


ROUTER_SYSTEM = (
    "Ты — маршрутизатор запросов HR-копайлота. Задачи:\n"
    "1) Матчинг резюме↔вакансия.\n"
    "2) Анализ интервью и портрет кандидата.\n"
    "Верни ТОЛЬКО JSON:\n"
    '{ "intent": "<compatibility|interview|clarify|out_of_scope>", '
    '"relevance": {"compatibility": 0-100, "interview": 0-100}, '
    '"reason": "<кратко>" }'
)

ROUTER_USER_TMPL = (
    "Запрос пользователя:\n-----\n{text}\n-----\n"
    "Оцени релевантность двум функциям (0..100) и выбери intent.\n"
    "Если обе < 40 — intent='out_of_scope' (если оффтоп) или 'clarify' (если по теме HR, но надо уточнение)."
)

# Приветствие
# greet
def greet(state: StateHrAgent) -> Command[Literal["human"]]:
    msg = (
        "Привет! Я HR-копайлот. Могу:\n"
        "1) Оценить совместимость резюме и вакансии.\n"
        "2) Проанализировать интервью и дать портрет кандидата.\n"
        "Сформулируй запрос в одной фразе."
    )
    logger.log("CHAT", "▶️ greet(): запуск приветствия")
    logger.log("CHAT", f"🤖 Приветствие: {msg}")  # <- добавили явный вывод текста
    return Command(update={"messages":[AIMessage(content=msg)]}, goto="human")

# human
def human(state: StateHrAgent) -> Command[Literal["router"]]:
    text = interrupt("human")
    logger.log("CHAT", f"💬 Пользователь: {text}")
    return Command(update={"user_input": text, "messages":[HumanMessage(content=text)]}, goto="router")

# router (LLM вариант)
def router(state: StateHrAgent) -> Command[Literal["compatibility_stub","interview_stub","human"]]:
    text = state.get("user_input", "").strip()
    logger.log("CONTEXT", f"🔍 router(): анализируем запрос: {text}")

    sys_msg = ROUTER_SYSTEM
    user_msg = ROUTER_USER_TMPL.format(text=text)
    llm_resp = giga.invoke([{"role":"system","content":sys_msg},
                            {"role":"user","content":user_msg}]).content
    logger.log("DATA", f"📩 LLM ответ для роутинга: {llm_resp}")

    # Парсим максимально бережно
    intent = "clarify"
    relevance = {"compatibility": 0, "interview": 0}
    reason = ""

    try:
        data = json.loads(llm_resp)
        intent = data.get("intent", intent)
        rel = data.get("relevance", {}) or {}
        relevance["compatibility"] = int(rel.get("compatibility", 0) or 0)
        relevance["interview"]     = int(rel.get("interview", 0) or 0)
        reason = str(data.get("reason", "") or "")
    except Exception as e:
        logger.error(f"❌ Ошибка парсинга JSON от LLM: {e}")
        # мягкий fallback — попросим корректный запрос
        msg = ("Не смог понять запрос. Примеры:\n"
               "• «Оцени совместимость резюме и вакансии»\n"
               "• «Проанализируй транскрипт интервью и опиши портрет кандидата»")
        return Command(update={"messages":[AIMessage(content=msg)],
                               "intent": None, "meta":{"router_error": str(e)}},
                       goto="human")

    logger.log("REASONING", f"intent={intent}, relevance={relevance}, reason='{reason}'")

    feedback = (f"Роутинг: intent = {intent}\n"
                f"Релевантность → matching: {relevance['compatibility']}%, "
                f"interview: {relevance['interview']}%.")

    if intent == "compatibility":
        return Command(update={"messages":[AIMessage(content=feedback)],
                               "intent":"compatibility",
                               "meta":{"relevance": relevance, "reason": reason}},
                       goto="compatibility_stub")

    if intent == "interview":
        return Command(update={"messages":[AIMessage(content=feedback)],
                               "intent":"interview",
                               "meta":{"relevance": relevance, "reason": reason}},
                       goto="interview_stub")

    # clarify / out_of_scope
    help_msg = (
        f"{feedback}\n"
        "Пожалуйста, задай корректный запрос. Примеры:\n"
        "• «Оцени совместимость этого резюме с этой вакансией»\n"
        "• «Проанализируй транскрипт интервью и опиши портрет кандидата»"
    )
    return Command(update={"messages":[AIMessage(content=help_msg)],
                           "intent": intent,
                           "meta":{"relevance": relevance, "reason": reason}},
                   goto="human")

# Заглушки задач (пока не разработаны)
def compatibility_stub(state: StateHrAgent):
    msg = "🔧 Нода «Совместимость резюме и вакансии» пока не разработана."
    logger.log("CHAT", f"{msg}")
    return Command(update={"messages":[AIMessage(content=msg)]}, goto="human")

def interview_stub(state: StateHrAgent):
    msg = "🔧 Нода «Анализ интервью / портрет кандидата» пока не разработана."
    logger.log("CHAT", f"{msg}")
    return Command(update={"messages":[AIMessage(content=msg)]}, goto="human")
