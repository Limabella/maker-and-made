# Trainer Bot (TRN-N)
Trainer Bot is an intelligent, vision-based coaching agent designed to analyze user exercise posture through multimodal reasoning. It goes beyond simple geometric calculations to provide context-aware, natural language coaching.

## 1. Key Features
Real-time Posture Estimation: Extracts 33 body landmarks using MediaPipe to calculate precise joint angles.

Exercise Repetition Counting: Tracks exercise phases to ensure accurate rep counting and session management.

Multimodal Error Detection: Combines geometric data (joint angles) with visual semantic context (image analysis) to detect complex posture errors.

Personalized Natural Language Coaching: Generates human-like feedback using the M-CoT (Multimodal Chain-of-Thought) strategy.

## 2. System Architecture
Motion Analyzer (Geometric Engine): Handles the mathematical analysis of body coordinates and physical state transitions.

Semantic Visual Reasoner (Vision Intelligence): A local MLLM engine (Ollama/Llama-3 Vision) that interprets "why" a posture is incorrect based on visual context (e.g., "heels lifting," "unstable gaze").

LLM Coach: Integrates outputs from both the Geometric and Semantic engines to synthesize final coaching messages.

State & Memory Tracker: Manages user history via memory.py for long-term progress tracking and session reflection.

## 3. Tech Stack
Language: Python

Computer Vision: OpenCV, MediaPipe

Intelligence Engine: Ollama (Llava / Llama-3 Vision), OpenAI API

Data Management: JSON-based persistent logging

## 4. Multimodal Expansion Roadmap (3-Phase Plan)
This roadmap integrates core concepts from the research paper "A Survey on Multimodal Large Language Models" into the TRN-N ecosystem.

### [Phase 1] Semantic Visual Reasoning Integration
Objective: Supplement numerical data (e.g., "Knee angle: 85°") with semantic interpretation (e.g., "Knees are collapsing inward").

Implementation: Create the VisualReasoner class to interface with local Small Multimodal Models (SMMs).

Technology: Ollama-based Llama-3 Vision or Llava.

### [Phase 2] Event-Driven LAVR (LLM-Aided Visual Reasoning)
Objective: Optimize local PC resources by analyzing only 'critical moments' rather than every single frame.

Implementation: Trigger the MLLM only when the MotionAnalyzer detects a specific event (e.g., "Postural deviation detected" or "Repetition completed").

Technology: Applying LAVR techniques to minimize computational overhead.

### [Phase 3] Multimodal CoT & Semantic Logging
Objective: Enhance the logic of feedback and maintain high-quality diagnostic records.

Implementation: - M-CoT: Design system prompts that follow a reasoning chain: "Observe landmarks -> Cross-reference with visual context -> Generate diagnostic conclusion."

Semantic Logging: Update memory.py to store MLLM's contextual analysis alongside raw geometric data for advanced session reflection.

## 5. Testing Guide (Video File Input)
To test the current and upcoming features with your own workout video:

Modify Input Source: In trn_bot.py, change cv2.VideoCapture(0) to your video file path (e.g., cv2.VideoCapture('my_video.mp4')).

Launch Local MLLM: Ensure the Ollama server is running with ollama run llava or llama3-vision.

Verify Logs: After the session, check the memory.json file. Ensure the semantic_context field contains the AI's intelligent posture descriptions.
