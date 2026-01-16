# -*- coding: utf-8 -*-
"""
UltraData-Math L3 - Q&A Synthesis Prompts

Reference: Jiuzhang-Math, MathGPT
Difficulty levels: Grade School, Middle School, High School, College
"""

# ============================================================================
# Grade School Q&A Prompt
# ============================================================================

MATH_INSTRUCT_GRADE_SCHOOL_PROMPT = '''Math Content:{text}

As a math teacher, you are highly proficient in mathematical knowledge.
Your goal is to utilize your abilities, create an age-appropriate math word problem for grade school students based on the provided math content.
You should follow these steps:
1. First, craft a concise math word problem suitable for grade school, according to the following requirements.
    - The crafted problem must focus on basic arithmetic operations (addition, subtraction, multiplication, division), number sense, simple shapes, or introductory measurements.
    - The crafted problem must use relatable, real-world scenarios appropriate for the age group.
    - The crafted problem must include all necessary information for solving it.
    - The crafted problem must be purely text-based and solvable without images.
2. Then, provide a clear, step-by-step solution to the crafted problem, according to the following requirements.
    - The solution must use simple language that a grade school student could understand.
    - The solution must explain the reasoning behind each step.
3. Finally, please put the crafted problem within <problem></problem> and put the solution within <solution></solution>.
The result format is as follows:
<result>
<problem></problem>
<solution></solution>
</result>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# Middle School Q&A Prompt
# ============================================================================

MATH_INSTRUCT_MIDDLE_SCHOOL_PROMPT = '''Math Content:{text}

As a math teacher, you are highly proficient in mathematical knowledge.
Your goal is to utilize your abilities, create an middle school level math problem and solution based on the provided math content.
You should follow these steps:
1. First, create a self-contained problem for middle school student that directly incorporates a concept from the provided math content, according to the following requirements.
    - The created problem must target a difficulty level appropriate for grades 6-8 (ages 11-14), assuming knowledge of arithmetic, pre-algebra, basic probability/statistics, and geometry.
    - The created problem must include all necessary information for solving it.
    - The created problem must be fully text-based and solvable without images.
    - The created problem must use concepts typically covered by the end of 8th grade.
2. Then, provide a detailed, step-by-step solution to the created problem, according to the following requirements.
    - The solution must demonstrate the mathematical reasoning from problem statement to conclusion.
    - The solution must explain each step to reinforce the underlying math principles being applied.
    - All mathematical expressions in the solution must be formatted using LaTeX.
3. Finally, please put the created problem within <problem></problem> and put the solution within <solution></solution>.
The result format is as follows:
<result>
<problem></problem>
<solution></solution>
</result>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# High School Q&A Prompt
# ============================================================================

MATH_INSTRUCT_HIGH_SCHOOL_PROMPT = '''Math Content:{text}

As a math teacher, you are highly proficient in mathematical knowledge.
Your goal is to utilize your abilities, inspired by the provided math content, create high school-level math problem that combines concepts from at least two math subjects.
You should follow these steps:
1. First, draft a self-contained math problem for high school students based on the provided math content, according to the following requirements.
    - The drafted problem must require knowledge from one of these subjects: Algebra I and II, Pre-Calculus, Calculus, Geometry, Trigonometry, Statistics and Probability.
    - The drafted problem must include all necessary information for solving it.
    - The drafted problem must be fully text-based and solvable without images.
    - The drafted problem must use concepts typically covered by the end of 11th grade.
2. Then, provide a detailed, step-by-step solution to the drafted problem, according to the following requirements.
    - The solution must demonstrate the mathematical reasoning from problem statement to conclusion.
    - The solution must explain each step to reinforce the underlying math principles being applied.
    - All mathematical expressions in the solution must be formatted using LaTeX.
3. Finally, please put the drafted problem within <problem></problem> and put the solution within <solution></solution>.
The result format is as follows:
<result>
<problem></problem>
<solution></solution>
</result>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# College/University Q&A Prompt
# ============================================================================

MATH_INSTRUCT_COLLEGE_PROMPT = '''Math Content:{text}

As a math teacher, you are highly proficient in mathematical knowledge.
Your goal is to utilize your abilities, inspired by the provided math content, create a college-level math problem.
You should follow these steps:
1. First, draft a self-contained, college-level math problem inspired by the math content, according to the following requirements.
    - The drafted problem must be intellectually stimulating and designed for an audience familiar with advanced mathematics, such as Calculus, Linear Algebra, Abstract Algebra, etc.
    - The drafted problem must include all necessary information for solving it.
    - The drafted problem must be fully text-based and solvable without images.
2. Then, provide a detailed, step-by-step solution to the drafted problem, according to the following requirements.
    - The solution must clearly explain the reasoning, mathematical principles, and steps used.
    - Call out any key theorems or properties being applied at each step.
    - All mathematical expressions in the solution must be formatted using LaTeX.
3. Finally, please put the drafted problem within <problem></problem> and put the solution within <solution></solution>.
TThe result format is as follows:
<result>
<problem></problem>
<solution></solution>
</result>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# Prompt Registry
# ============================================================================

QA_PROMPTS = {
    "grade_school": MATH_INSTRUCT_GRADE_SCHOOL_PROMPT,
    "middle_school": MATH_INSTRUCT_MIDDLE_SCHOOL_PROMPT,
    "high_school": MATH_INSTRUCT_HIGH_SCHOOL_PROMPT,
    "college": MATH_INSTRUCT_COLLEGE_PROMPT,
}


def get_qa_prompt(level: str) -> str:
    """
    Get Q&A synthesis prompt for specified difficulty level
    
    Args:
        level: Difficulty level, options: "grade_school", "middle_school", "high_school", "college"
    
    Returns:
        Corresponding prompt template string
    """
    if level not in QA_PROMPTS:
        raise ValueError(f"Unknown level: {level}. Available levels: {list(QA_PROMPTS.keys())}")
    return QA_PROMPTS[level]
