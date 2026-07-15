from dataclasses import dataclass

from main import build_interaction_record, run_pipeline
from layers.memory_layer import MemoryLayer
from support_layers.llm_expression_layer import (
    build_fallback_expression,
    generate_nvidia_expression,
)
from knowledge.mnd_n_knowledge_service import maybe_answer_psychology_question


@dataclass
class ConversationTurn:
    result: dict
    expression: dict


class ConversationService:
    """Complete one turn and persist it only after dialogue is available."""

    def __init__(self, memory: MemoryLayer, use_nvidia: bool = False):
        self.memory = memory
        self.use_nvidia = use_nvidia

    def respond(self, user_sentence: str) -> ConversationTurn:
        recent_interactions = self.memory.load_interactions()
        result = run_pipeline(user_sentence, self.memory, persist=False)

        if self.use_nvidia:
            expression = generate_nvidia_expression(
                user_sentence,
                result,
                recent_interactions=recent_interactions,
            )
        else:
            expression = build_fallback_expression(result)

        knowledge_answer = None
        if not result["safety"]["triggered"]:
            knowledge_answer = maybe_answer_psychology_question(user_sentence)
        if knowledge_answer:
            expression["mnd_n_line"] = knowledge_answer
            expression["knowledge_provider"] = "lightrag"

        interaction = build_interaction_record(result)
        interaction.update(
            {
                "onn_c_line": expression["onn_c_line"],
                "mnd_n_line": expression["mnd_n_line"],
                "expression_provider": expression["provider"],
                "knowledge_provider": expression.get("knowledge_provider"),
            }
        )
        self.memory.add_interaction(interaction)
        return ConversationTurn(result=result, expression=expression)
