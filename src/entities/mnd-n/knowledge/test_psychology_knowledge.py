import unittest
from unittest.mock import patch

from glossary_extractor import parse_locations
from lightrag_adapter import build_custom_kg, format_entry_for_index
from mnd_n_education_policy import (
    educational_answer_instruction,
    should_retrieve_psychology_knowledge,
)
from mnd_n_knowledge_service import maybe_answer_psychology_question


ENTRY = {
    "id": "cognitive-dissonance",
    "term_en": "Cognitive Dissonance",
    "term_ko": "인지 부조화",
    "definition_en": "Discomfort from incompatible thoughts.",
    "definition_ko": "양립하기 어려운 생각에서 생기는 불편함.",
    "aliases_ko": [],
    "relations": [],
    "translation_status": "machine_draft",
    "relation_status": "not_started",
    "source": {"title": "Social Psychology Glossary", "page": 2},
}


class PsychologyKnowledgeTests(unittest.TestCase):
    def test_parses_multiple_source_locations(self) -> None:
        self.assertEqual(
            parse_locations("Course Overview Lecture 1.1 Reading 1.1"),
            ["Course Overview", "Lecture 1.1", "Reading 1.1"],
        )

    def test_index_text_preserves_bilingual_source_provenance(self) -> None:
        text = format_entry_for_index(ENTRY)
        self.assertIn("Cognitive Dissonance", text)
        self.assertIn("인지 부조화", text)
        self.assertIn("page 2", text)
        self.assertIn("machine_draft", text)

    def test_custom_kg_uses_source_concept_without_unreviewed_relations(self) -> None:
        kg = build_custom_kg([ENTRY])
        self.assertEqual(kg["entities"][0]["entity_name"], "Cognitive Dissonance")
        self.assertIn("#page=2", kg["chunks"][0]["file_path"])
        self.assertEqual(kg["relationships"], [])

    def test_retrieval_requires_an_explicit_educational_cue(self) -> None:
        self.assertTrue(should_retrieve_psychology_knowledge("인지 부조화가 무슨 뜻이야?"))
        self.assertFalse(should_retrieve_psychology_knowledge("오늘 마음이 복잡해"))

    def test_instruction_forbids_diagnosis_and_requires_source(self) -> None:
        instruction = educational_answer_instruction("source page 2")
        self.assertIn("Do not diagnose", instruction)
        self.assertIn("source document and page", instruction)

    @patch.dict("os.environ", {"PSYCH_RAG_ENABLED": "false"})
    def test_optional_service_stays_off_by_default(self) -> None:
        self.assertIsNone(maybe_answer_psychology_question("심리학 용어를 설명해 줘"))


if __name__ == "__main__":
    unittest.main()
