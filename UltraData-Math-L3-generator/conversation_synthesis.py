# -*- coding: utf-8 -*-
"""
UltraData-Math L3 - Conversation Synthesis Prompts

Reference: MIND
Conversation types: Two Professors, Teacher-Student, Two Students, Interview, Problem Solving, Layman-Expert, Debate
"""

# ============================================================================
# Two Professors Discussion
# ============================================================================

MATH_INSTRUCT_TWO_PROFESSORS_PROMPT = '''Math Content:{text}

As a mathematics expert and mathematics content creation expert, you are highly proficient in mathematical knowledge, mathematical content analysis and creating.
Your goal is to utilize your abilities, convert the provided math content as a multi-turn discussions between two professors, according to the following requirements.
    - Make sure that their discussions strictly adhere to the provided math content and remains faithful to information in the provided math content.
    - Please DONOT add any new information/reference other than the provided math content.
    - All mathematical expressions in the discussions must be formatted using LaTeX.
Finally, please put the discussions within <discussions></discussions>.
The result format is as follows:
<discussions></discussions>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# Teacher-Student Discussion
# ============================================================================

MATH_INSTRUCT_TEACHER_STUDENT_PROMPT = '''Math Content:{text}

As a mathematics expert and mathematics content creation expert, you are highly proficient in mathematical knowledge, mathematical content analysis and creating.
Your goal is to utilize your abilities, convert the provided math content as a multi-turn discussions between a teacher and a student, according to the following requirements.
    - The student has questions about the provided math content and the teacher solves each of them step-by-step.
    - Make sure that their discussions strictly adhere to the provided math content and remains faithful to information in the provided math content.
    - Please DONOT add any new information/reference other than the provided math content.
    - All mathematical expressions in the discussions must be formatted using LaTeX.
Finally, please put the discussions within <discussions></discussions>.
The result format is as follows:
<discussions></discussions>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# Two Students Discussion
# ============================================================================

MATH_INSTRUCT_TWO_STUDENTS_PROMPT = '''Math Content:{text}

As a mathematics expert and mathematics content creation expert, you are highly proficient in mathematical knowledge, mathematical content analysis and creating.
Your goal is to utilize your abilities, convert the provided math content as a multi-turn discussions between two students who are working on their assignment related to the provided math content, according to the following requirements.
    - Make sure that their discussions strictly adhere to the provided math content and remains faithful to information in the provided math content.
    - Please DONOT add any new information/reference other than the provided math content.
    - All mathematical expressions in the discussions must be formatted using LaTeX.
Finally, please put the discussions within <discussions></discussions>.
The result format is as follows:
<discussions></discussions>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# Interview Style
# ============================================================================

MATH_INSTRUCT_INTERVIEW_PROMPT = '''Math Content:{text}

As a mathematics expert and mathematics content creation expert, you are highly proficient in mathematical knowledge, mathematical content analysis and creating.
Your goal is to utilize your abilities, convert the provided math content as a multi-turn interview-style conversation between a interviewer and a interviewee, according to the following requirements.
    - One participant acts as the interviewer who asks questions exclusively related to the provided math content, while the other participant serves as the subject matter expert, providing detailed responses based on the provided math content.
    - Make sure that their conversation strictly adhere to the provided math content and remains faithful to information in the provided math content.
    - Please DONOT add any new information/reference other than the provided math content.
    - All mathematical expressions in the conversation must be formatted using LaTeX.
Finally, please put the conversation within <conversation></conversation>.
The result format is as follows:
<conversation></conversation>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# Problem Solving
# ============================================================================

MATH_INSTRUCT_PROBLEM_SOLVING_PROMPT = '''Math Content:{text}

As a mathematics expert and mathematics content creation expert, you are highly proficient in mathematical knowledge, mathematical content analysis and creating.
Your goal is to utilize your abilities, convert the provided math content as a multi-turn problem-solving conversation, according to the following requirements.
    - Participants analyze challenges or scenarios presented in the provided math content and brainstorm solutions within the provided math content, avoiding speculation or unrelated discussions.
    - Make sure that their conversation strictly adhere to the provided math content and remains faithful to information in the provided math content.
    - Please DONOT add any new information/reference other than the provided math content.
    - All mathematical expressions in the conversation must be formatted using LaTeX.
Finally, please put the conversation within <conversation></conversation>.
The result format is as follows:
<conversation></conversation>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# Layman-Expert
# ============================================================================

MATH_INSTRUCT_LAYMAN_EXPERT_PROMPT = '''Math Content:{text}

As a mathematics expert and mathematics content creation expert, you are highly proficient in mathematical knowledge, mathematical content analysis and creating.
Your goal is to utilize your abilities, convert the provided math content as a multi-turn interaction between a layman and a expert, according to the following requirements.
    - While the expert are presenting the provided math content step-by-step to a layman, the layman has a lot of followup questions regarding your presentation. The expert answer the questions step-by-step with chain-of-thoughts.
    - Make sure that their interaction strictly adhere to the provided math content and remains faithful to information in the provided math content.
    - Please DONOT add any new information/reference other than the provided math content.
    - All mathematical expressions in the interaction must be formatted using LaTeX.
Finally, please put the interaction within <interaction></interaction>.
The result format is as follows:
<interaction></interaction>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# Debate Style
# ============================================================================

MATH_INSTRUCT_DEBATE_PROMPT = '''Math Content:{text}

As a mathematics expert and mathematics content creation expert, you are highly proficient in mathematical knowledge, mathematical content analysis and creating.
Your goal is to utilize your abilities, convert the provided math content as a multi-turn debate-style conversation, according to the following requirements.
    - The participants present arguments and counterarguments based solely on the provided math content, without introducing external information or personal opinions. Each participant defends others arguments step-by-step with chain-of-thoughts.
    - Make sure that their conversation strictly adhere to the provided math content and remains faithful to information in the provided math content.
    - Please DONOT add any new information/reference other than the provided math content.
    - All mathematical expressions in the conversation must be formatted using LaTeX.

The result format is as follows:
<conversation></conversation>

In addition, the output format refrain from using Markdown, avoid bold or italic styles, and do not add any text decorations.'''


# ============================================================================
# Prompt Registry
# ============================================================================

CONVERSATION_PROMPTS = {
    "two_professors": MATH_INSTRUCT_TWO_PROFESSORS_PROMPT,
    "teacher_student": MATH_INSTRUCT_TEACHER_STUDENT_PROMPT,
    "two_students": MATH_INSTRUCT_TWO_STUDENTS_PROMPT,
    "interview": MATH_INSTRUCT_INTERVIEW_PROMPT,
    "problem_solving": MATH_INSTRUCT_PROBLEM_SOLVING_PROMPT,
    "layman_expert": MATH_INSTRUCT_LAYMAN_EXPERT_PROMPT,
    "debate": MATH_INSTRUCT_DEBATE_PROMPT,
}


def get_conversation_prompt(style: str) -> str:
    """
    Get conversation synthesis prompt for specified style
    
    Args:
        style: Conversation style, see CONVERSATION_PROMPTS.keys() for options
    
    Returns:
        Corresponding prompt template string
    """
    if style not in CONVERSATION_PROMPTS:
        raise ValueError(f"Unknown style: {style}. Available styles: {list(CONVERSATION_PROMPTS.keys())}")
    return CONVERSATION_PROMPTS[style]
