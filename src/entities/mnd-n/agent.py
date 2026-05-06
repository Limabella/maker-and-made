from emotion import EmotionState, update_emotion
from memory import MemoryStore
from reflection import reflect
from prompt import SYSTEM_PROMPT


class MNDEntity:

    def __init__(self):

        self.state = EmotionState()
        self.memory = MemoryStore()

    def analyze_emotion(self, text):

        text = text.lower()

        if "불안" in text or "anxious" in text:
            return {
                "stress": 0.8,
                "emotion": "anxiety"
            }

        if "외롭" in text or "lonely" in text:
            return {
                "stress": 0.6,
                "emotion": "loneliness"
            }

        if "행복" in text or "happy" in text:
            return {
                "stress": 0.1,
                "emotion": "positive"
            }

        return {
            "stress": 0.3,
            "emotion": "neutral"
        }

    def generate_response(self, user_input):

        if self.state.stress > 0.7:
            return "요즘 많이 지쳐 보이네요. 천천히 이야기해도 괜찮아요."

        if self.state.loneliness > 0.5:
            return "혼자라고 느껴지는 순간이 있었던 것 같아요."

        if self.state.trust > 0.7:
            return "계속 이야기를 들려줘서 고마워요."

        return "조금 더 이야기해줄래요?"

    def chat(self, user_input):

        analysis = self.analyze_emotion(user_input)

        self.state = update_emotion(self.state, analysis)

        self.memory.add_memory(
            user_input,
            analysis["emotion"]
        )

        reflection = reflect(
            self.memory.recent_memories()
        )

        response = self.generate_response(user_input)

        return {
            "response": response,
            "emotion_state": self.state,
            "reflection": reflection,
            "recent_memories": self.memory.recent_memories()
        }


if __name__ == "__main__":

    mnd = MNDEntity()

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break

        result = mnd.chat(user_input)

        print("\nMND-N:", result["response"])

        print("\n[Reflection]")
        print(result["reflection"])

        print("\n[Emotion State]")
        print(result["emotion_state"])