from emotion import EmotionState, update_emotion, load_state, save_state
from memory import (
    ShortTermMemory,
    LongTermMemory
)
from reflection import reflect
from prompt import SYSTEM_PROMPT
from cognition.stress_prediction import StressPredictor



class MNDEntity:

    def __init__(self):

        self.predictor = StressPredictor()

        self.state = load_state()
        
        self.short_term_memory = ShortTermMemory()
        
        self.long_term_memory = LongTermMemory()
        

    def generate_response(self, user_input):

        if self.state.stress > 0.7:
            return "요즘 많이 지쳐 보이네요. 천천히 이야기해도 괜찮아요."

        if self.state.loneliness > 0.5:
            return "혼자라고 느껴지는 순간이 있었던 것 같아요."

        if self.state.trust > 0.7:
            return "계속 이야기를 들려줘서 고마워요."

        return "조금 더 이야기해줄래요?"

    def chat(self, user_input):

        analysis = self.predictor.predict(user_input)

        self.state = update_emotion(self.state, analysis)
        save_state(self.state)

        self.short_term_memory.add_memory(
            user_input,
            analysis["emotion"]
        )

        self.long_term_memory.update_emotion(
            analysis["emotion"]
        )

        self.long_term_memory.update_relationship(
            trust_delta=0.01
        )

        reflection = reflect(
            self.short_term_memory.get_recent()
        )

        response = self.generate_response(user_input)

        return {
            "response": response,
            "analysis": analysis,
            "emotion_state": self.state,
            "reflection": reflection,
            "recent_memories": self.short_term_memory.get_recent(),
            "long_term_patterns": self.long_term_memory.get_emotion_patterns()
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

        print("\n[Long-Term Memory]")
        print(result["long_term_patterns"])