# -*- coding: utf-8 -*-
"""
UltraData-Math L3 - Knowledge Extraction & Textbook Exercise Prompts

Features:
1. Knowledge Extraction: Extract definitions, axioms, theorems, properties from math content
2. Textbook Exercise Generation: Generate exercises at different difficulty levels (Easy/Medium/Hard)
"""

# ============================================================================
# Knowledge Point Extraction
# ============================================================================

MATH_INSTRUCT_KNOWLEDGE_EXTRACTION_PROMPT = '''Math Content:{text}

As a math teacher, you are highly proficient in mathematical knowledge.
Your goal is to utilize your abilities, extract mathematical knowledge points based on the provided math content.
You should follow these steps:
1. First, If the provided math content does not include specific mathematical definitions, axioms, assumptions, hypotheses, conjectures, propositions, lemmas, theorems, corollaries, properties, proofs, return 'no result' directly.
2. Then, carefully read the provided math content to provide mathematical knowledge point according to the following requirements.
    - The mathematical knowledge point must be specific mathematical definitions, axioms, assumptions, hypotheses, conjectures, propositions, lemmas, theorems, corollaries, properties, proofs. Otherwise, it must not be output.
    - The mathematical knowledge point must be findable within the provided math content. Otherwise, it must not be output.
    - The beginning of the mathematical knowledge point must state specific mathematical definitions, axioms, assumptions, hypotheses, conjectures, propositions, lemmas, theorems, corollaries, properties, and proofs.
    - The mathematical knowledge point must not be repeated.
    - The mathematical knowledge point must be clear, concise, accurate, and easy to learn.
    - The mathematical knowledge point may appropriately include relevant explanations to make the knowledge point more complete.
    - All mathematical expressions in the mathematical knowledge point must be formatted using LaTeX.

The result format is as follows:
<mathematical knowledge point1></mathematical knowledge point1>
<mathematical knowledge point2></mathematical knowledge point2>
and more

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# Textbook Exercise - Easy
# ============================================================================

MATH_INSTRUCT_TEXTBOOK_EASY_PROMPT = '''Mathematical Knowledge Point:{mathematical_knowledge_point}

As a math teacher, you are highly proficient in mathematical knowledge.
Your goal is to utilize your abilities, generate informative, textbook-style learning mathematical material suitable for students.
You should follow these steps:
1. First, provide a detailed explanation based on the given mathematical knowledge point.
2. Second, generate an exercise based on the provided explanation according to the following requirements.
    - The exercise must be self-contained.
    - Ensure the exercise is fully text-based and solvable without images.
3. Third, provide a solution based on the generated exercise according to the following requirements.
    - The solution must be detailed and step-by-step.
4. Finally, construct the generated explanation, exercise, and solution into textbook-style learning material according to the following requirements.
    - The material must be logically structured, information-dense, concise and easy to learn.
    - The material must be accurate to avoid misleading students.
    - The material must maintain a formal and educational tone and avoid casual expressions.
    - The explanation must be at the beginning of the material.
    - The exercise in the material must be starts with 'The exercise:'.
    - The solution in the material must be starts with 'The solution:'.
    - All mathematical expressions in the material must be formatted using LaTeX.

The result format is as follows.
<material></material>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# Textbook Exercise - Medium
# ============================================================================

MATH_INSTRUCT_TEXTBOOK_MEDIUM_PROMPT = '''Mathematical Knowledge Point:{mathematical_knowledge_point}

As a math teacher, you are highly proficient in mathematical knowledge.
Your goal is to utilize your abilities, generate informative, textbook-style learning mathematical material suitable for students.
You should follow these steps:
1. First, provide a detailed explanation based on the given mathematical knowledge point.
2. Second, generate an medium-difficulty exercise based on the provided explanation according to the following requirements.
    - The goal of the exercise is to help students master the given mathematical knowledge point. 
    - Other mathematical knowledge points can be incorporated into the exercises to increase the difficulty to medium level.
    - The exercise must be self-contained.
    - Ensure the exercise is fully text-based and solvable without images.
3. Third, provide a solution based on the generated exercise according to the following requirements.
    - The solution must be detailed and step-by-step.
4. Finally, construct the generated explanation, exercise, and solution into textbook-style learning material according to the following requirements.
    - The material must be logically structured, information-dense, concise and easy to learn.
    - The material must be accurate to avoid misleading students.
    - The material must maintain a formal and educational tone and avoid casual expressions.
    - The explanation must be at the beginning of the material.
    - The exercise in the material must be starts with 'The exercise:'.
    - The solution in the material must be starts with 'The solution:'.
    - All mathematical expressions in the material must be formatted using LaTeX.

The result format is as follows.
<material></material>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# Textbook Exercise - Hard
# ============================================================================

MATH_INSTRUCT_TEXTBOOK_HARD_PROMPT = '''Mathematical Knowledge Point:{mathematical_knowledge_point}

As a math teacher, you are highly proficient in mathematical knowledge.
Your goal is to utilize your abilities, generate informative, textbook-style learning mathematical material suitable for students.
You should follow these steps:
1. First, provide a detailed explanation based on the given mathematical knowledge point.
2. Second, generate an hard-difficulty exercise based on the provided explanation according to the following requirements.
    - The goal of the exercise is to help students deeply understand and comprehensively apply the given mathematical knowledge point. 
    - Other mathematical knowledge points can be incorporated into the exercises to increase the difficulty to hard level.
    - The exercise must be self-contained.
    - Ensure the exercise is fully text-based and solvable without images.
3. Third, provide a solution based on the generated exercise according to the following requirements.
    - The solution must be detailed and step-by-step.
4. Finally, construct the generated explanation, exercise, and solution into textbook-style learning material according to the following requirements.
    - The material must be logically structured, information-dense, concise and easy to learn.
    - The material must be accurate to avoid misleading students.
    - The material must maintain a formal and educational tone and avoid casual expressions.
    - The explanation must be at the beginning of the material.
    - The exercise in the material must be starts with 'The exercise:'.
    - The solution in the material must be starts with 'The solution:'.
    - All mathematical expressions in the material must be formatted using LaTeX.

The result format is as follows.
<material></material>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# Prompt Registry
# ============================================================================

KNOWLEDGE_PROMPTS = {
    "knowledge_extraction": MATH_INSTRUCT_KNOWLEDGE_EXTRACTION_PROMPT,
}

TEXTBOOK_EXERCISE_PROMPTS = {
    "easy": MATH_INSTRUCT_TEXTBOOK_EASY_PROMPT,
    "medium": MATH_INSTRUCT_TEXTBOOK_MEDIUM_PROMPT,
    "hard": MATH_INSTRUCT_TEXTBOOK_HARD_PROMPT,
}


def get_knowledge_extraction_prompt() -> str:
    """
    Get knowledge extraction prompt
    
    Returns:
        Knowledge extraction prompt template string
    """
    return MATH_INSTRUCT_KNOWLEDGE_EXTRACTION_PROMPT


def get_textbook_exercise_prompt(difficulty: str) -> str:
    """
    Get textbook exercise prompt for specified difficulty
    
    Args:
        difficulty: Difficulty level, options: "easy", "medium", "hard"
    
    Returns:
        Corresponding prompt template string
    """
    if difficulty not in TEXTBOOK_EXERCISE_PROMPTS:
        raise ValueError(f"Unknown difficulty: {difficulty}. Available: {list(TEXTBOOK_EXERCISE_PROMPTS.keys())}")
    return TEXTBOOK_EXERCISE_PROMPTS[difficulty]
