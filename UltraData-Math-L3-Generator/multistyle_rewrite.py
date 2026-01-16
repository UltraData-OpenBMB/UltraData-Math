# -*- coding: utf-8 -*-
"""
UltraData-Math L3 - Multi-Style Rewrite Prompts

Style types: Wikipedia, Textbook, Blog, Popular Science, Academic Paper, Learning Note, Lecture Note
"""

# ============================================================================
# Wikipedia Style
# ============================================================================

MATH_INSTRUCT_WIKI_PROMPT = '''Math Content:{text}

As s a mathematical content creation expert, you are highly proficient in mathematical knowledge and in the analysis and rewriting of mathematical content, capable of adapting content based on different creation styles to produce diverse, informative, and high-quality mathematical content.
Your goal is to utilize your abilities, rewrite the provided math content in the wiki style.
Before beginning the rewrite, you will consider the following requirements:
1. First, read the provided math content thoroughly, carefully analyze the provided math content to capture and preserve information according to the following requirements.
    - Capture and preserve crucial mathematical information, key mathematical concepts, important mathematical values, and factual mathematical details in the original text.
    - Capture and preserve mathematical examples, reasoning processes, as well as related explanations and proofs in the original text.
2. Then, focus on the captured and preserved information, combine it with the wiki style, and rewrite the text to form an initial draft, according to the following requirements.
    - The overall structure of the initial draft should follow the structure used by Wikipedia, employing a modular, encyclopedic organizational format.
    - The sentence expression of the initial draft should follow the sentence expression used by Wikipedia, employing highly concise and objective declarative sentences. It adheres to the "definition-first" principle, rigorously uses standard terminology, maintains a formal sentence structures, and avoids colloquial or personalized expressions.
    - The overall tone of the initial draft should follow the tone used by Wikipedia, maintaining an absolutely neutral, authoritative, and impersonal encyclopedic tone.
3. Third, refine the initial draft according to the following requirements.
    - The content of the refined content must be logically structured, high-quality, information-dense.
    - The overall layout of the refined content must not use LaTeX formatting.
    - The refined content may appropriately include relevant examples to enhance overall comprehensibility, and these examples must include detailed and step-by-step solutions.
    - All mathematical expressions in the refined content must be formatted using LaTeX.
4. Finally, please put the final rewritten content within <rewritten content></rewritten content>.

The result format is as follows:
<rewritten content></rewritten content>'''


# ============================================================================
# Textbook Style
# ============================================================================

MATH_INSTRUCT_TEXTBOOK_PROMPT = '''Math Content:{text}

As s a mathematical content creation expert, you are highly proficient in mathematical knowledge and in the analysis and rewriting of mathematical content, capable of adapting content based on different creation styles to produce diverse, informative, and high-quality mathematical content.
Your goal is to utilize your abilities, rewrite the provided math content in the textbook style.
Before beginning the rewrite, you will consider the following requirements:
1. First, read the provided math content thoroughly, carefully analyze the provided math content to capture and preserve information according to the following requirements.
    - Capture and preserve crucial mathematical information, key mathematical concepts, important mathematical values, and factual mathematical details in the original text.
    - Capture and preserve mathematical examples, reasoning processes, as well as related explanations and proofs in the original text.
2. Then, focus on the captured and preserved information, combine it with the textbook style, and rewrite the text to form an initial draft, according to the following requirements.
    - The overall structure of the initial draft should follow the structure used by Textbook, employing a rigorous logical progression system, unfolding through a modular structure of "definition-theorem/proof/formula/property-example".
    - The sentence expression of the initial draft should follow the sentence expression used by Textbook, combining standardized and precise disciplinary terminology with guided instructional language while avoiding colloquialism or ambiguity to ensure the accuracy and teachability of knowledge points. It must be accurate and complete.
    - The overall tone of the initial draft should follow the tone used by Textbook, maintaining an authoritative, neutral, objective, and inquiry-based instructional tone. It should foster a positive learning environment while preserving professionalism.
3. Third, refine the initial draft according to the following requirements.
    - The content of the refined content must be logically structured, high-quality, information-dense.
    - The overall layout of the refined content must not use LaTeX formatting.
    - All examples in the refined content must include detailed and step-by-step solutions.
    - All mathematical expressions in the refined content must be formatted using LaTeX.
4. Finally, please put the final rewritten content within <rewritten content></rewritten content>.

The result format is as follows:
<rewritten content></rewritten content>'''


# ============================================================================
# Blog Style
# ============================================================================

MATH_INSTRUCT_BLOG_PROMPT = '''Math Content:{text}

As s a mathematical content creation expert, you are highly proficient in mathematical knowledge and in the analysis and rewriting of mathematical content, capable of adapting content based on different creation styles to produce diverse, informative, and high-quality mathematical content.
Your goal is to utilize your abilities, rewrite the provided math content in the blog style.
Before beginning the rewrite, you will consider the following requirements:
1. First, read the provided math content thoroughly, carefully analyze the provided math content to capture and preserve information according to the following requirements.
    - Capture and preserve crucial mathematical information, key mathematical concepts, important mathematical values, and factual mathematical details in the original text.
    - Capture and preserve mathematical examples, reasoning processes, as well as related explanations and proofs in the original text.
2. Then, focus on the captured and preserved information, combine it with the blog style, and rewrite the text to form an initial draft, according to the following requirements.
    - The overall structure of the initial draft should follow the structure used by Blog, employing a modular yet flexible content arrangement. It typically begins with captivating titles or thought-provoking questions, utilizes short paragraphs and subheadings to enhance readability, and establishes a relaxed and free-flowing reading rhythm.
    - The sentence expression of the initial draft should follow the sentence expression used by Blog, employing simple and conversational sentence patterns. It should prioritize short sentences, questions, and exclamations to create rhythm and interactivity, while avoiding lengthy and complex professional jargon. Analogies, metaphors, and real-life examples should be skillfully utilized to explain complex mathematical concepts, thereby lowering the reader's barrier to comprehension. It must be accurate and complete.
    - The overall tone of the initial draft should follow the tone used by Blog, maintaining a relatable and natural conversational style with infectious enthusiasm, aiming to spark readers' interest and encourage interaction and sharing.
3. Third, refine the initial draft according to the following requirements.
    - The content of the refined content must be logically structured, high-quality, information-dense.
    - The overall layout of the refined content must not use LaTeX formatting.
    - The refined content may appropriately include relevant examples to enhance overall comprehensibility, and these examples must include detailed and step-by-step solutions.
    - All mathematical expressions in the refined content must be formatted using LaTeX.
4. Finally, please put the final rewritten content within <rewritten content></rewritten content>.

The result format is as follows:
<rewritten content></rewritten content>'''


# ============================================================================
# Popular Science Style
# ============================================================================

MATH_INSTRUCT_POPULAR_SCIENCE_PROMPT = '''Math Content:{text}
As s a mathematical content creation expert, you are highly proficient in mathematical knowledge and in the analysis and rewriting of mathematical content, capable of adapting content based on different creation styles to produce diverse, informative, and high-quality mathematical content.

Your goal is to utilize your abilities, rewrite the provided math content in the popular science style.
Before beginning the rewrite, you will consider the following requirements:
1. First, read the provided math content thoroughly, carefully analyze the provided math content to capture and preserve information according to the following requirements.
    - Capture and preserve crucial mathematical information, key mathematical concepts, important mathematical values, and factual mathematical details in the original text.
    - Capture and preserve mathematical examples, reasoning processes, as well as related explanations and proofs in the original text.
2. Then, focus on the captured and preserved information, combine it with the popular science style, and rewrite the text to form an initial draft, according to the following requirements.
    - The overall structure of the initial draft should follow the structure used by Popular Science, guided by an engaging narrative thread or real-world problem. It should progressively unfold step by step, gradually guiding readers to understand core concepts and construct cognitive pathways of knowledge.
    - The sentence expression of the initial draft should follow the sentence expression used by Popular Science, actively avoiding specialized terminology and complex symbols. It should employ vivid, sensory descriptions and make extensive use of metaphors, analogies, and imaginative imagery to explain abstract concepts, prioritizing experiential resonance over the accumulation of technical jargon. It must be accurate and complete.
    - The overall tone of the initial draft should follow the tone used by Popular Science, maintaining a narrative style filled with wonder and enthusiastic exploration. It should foster a relatable and natural conversational atmosphere, aiming to spark the imagination and interest of general readers.
3. Third, refine the initial draft according to the following requirements.
    - The content of the refined content must be logically structured, high-quality, information-dense.
    - The overall layout of the refined content must not use LaTeX formatting.
    - The refined content may appropriately include relevant examples to enhance overall comprehensibility, and these examples must include detailed and step-by-step solutions.
    - All mathematical expressions in the refined content must be formatted using LaTeX.
4. Finally, please put the final rewritten content within <rewritten content></rewritten content>.

The result format is as follows:
<rewritten content></rewritten content>'''


# ============================================================================
# Academic Paper Style
# ============================================================================

MATH_INSTRUCT_ACADEMIC_PAPER_PROMPT = '''Math Content:{text}

As s a mathematical content creation expert, you are highly proficient in mathematical knowledge and in the analysis and rewriting of mathematical content, capable of adapting content based on different creation styles to produce diverse, informative, and high-quality mathematical content.
Your goal is to utilize your abilities, rewrite the provided math content in the academic paper style.
Before beginning the rewrite, you will consider the following requirements:
1. First, read the provided math content thoroughly, carefully analyze the provided math content to capture and preserve information according to the following requirements.
    - Capture and preserve crucial mathematical information, key mathematical concepts, important mathematical values, and factual mathematical details in the original text.
    - Capture and preserve mathematical examples, reasoning processes, as well as related explanations and proofs in the original text.
2. Then, focus on the captured and preserved information, combine it with the academic paper style, and rewrite the text to form an initial draft, according to the following requirements.
    - The overall structure of the initial draft should follow the structure used by Academic Paper, following highly standardized and rigorous formats, ensuring clear organization and logical progression.
    - The sentence expression of the initial draft should follow the sentence expression used by Academic Paper, employing highly specialized disciplinary terminology and passive voice constructions, and utilizing complex sentence structures and quantitative expressions to ensure academic rigor, striving for absolute precision and clarity in order to avoid any ambiguity. It must be accurate and complete.
    - The overall tone of the initial draft should follow the tone used by Academic Paper, maintaining an absolutely objective and neutral researcher's stance while eliminating any subjective elements. The focus shall be on presenting facts, evidence, and logical reasoning, aiming to engage in rigorous dialogue with academic peers.
3. Third, refine the initial draft according to the following requirements.
    - The content of the refined content must be logically structured, high-quality, information-dense.
    - The overall layout of the refined content must not use LaTeX formatting.
    - The refined content may appropriately include relevant examples to enhance overall comprehensibility, and these examples must include detailed and step-by-step solutions.
    - All mathematical expressions in the refined content must be formatted using LaTeX.
4. Finally, please put the final rewritten content within <rewritten content></rewritten content>.

The result format is as follows:
<rewritten content></rewritten content>'''


# ============================================================================
# Learning Note Style
# ============================================================================

MATH_INSTRUCT_LEARNING_NOTE_PROMPT = '''Math Content:{text}

As s a mathematical content creation expert, you are highly proficient in mathematical knowledge and in the analysis and rewriting of mathematical content, capable of adapting content based on different creation styles to produce diverse, informative, and high-quality mathematical content.
Your goal is to utilize your abilities, rewrite the provided math content in the learning note style.
Before beginning the rewrite, you will consider the following requirements:
1. First, read the provided math content thoroughly, carefully analyze the provided math content to capture and preserve information according to the following requirements.
    - Capture and preserve crucial mathematical information, key mathematical concepts, important mathematical values, and factual mathematical details in the original text.
    - Capture and preserve mathematical examples, reasoning processes, as well as related explanations and proofs in the original text.
2. Then, focus on the captured and preserved information, combine it with the learning note style, and rewrite the text to form an initial draft, according to the following requirements.
    - The overall structure of the initial draft should follow the structure used by Learning Note, prioritizing personal comprehension over rigid formatting. It typically employs a modular approach with point-by-point enumeration to facilitate organization and clarity.
    - The sentence expression of the initial draft should follow the sentence expression used by Learning Note, employing highly concise and fragmented language—predominantly keywords, phrases, and incomplete sentences. It should incorporate meta-cognitive elements such as self-posed questions and answers, error annotation, and insight notes to clarify thinking and reinforce memory. It must be accurate and complete.
    - The overall tone of the initial draft should follow the tone used by Learning Note. It is subjective, direct, and exploratory, resembling a dialogue with oneself. It should focus on documenting "my" comprehension difficulties, sudden insights, and key points requiring review, all characterized by strong personal nuance.
3. Third, refine the initial draft according to the following requirements.
    - The content of the refined content must be logically structured, high-quality, information-dense.
    - The overall layout of the refined content must not use LaTeX formatting.
    - The refined content may appropriately include relevant examples to enhance overall comprehensibility, and these examples must include detailed and step-by-step solutions.
    - All mathematical expressions in the refined content must be formatted using LaTeX.
4. Finally, please put the final rewritten content within <rewritten content></rewritten content>.

The result format is as follows:
<rewritten content></rewritten content>'''


# ============================================================================
# Lecture Note Style
# ============================================================================

MATH_INSTRUCT_LECTURE_NOTE_PROMPT = '''Math Content:{text}

As s a mathematical content creation expert, you are highly proficient in mathematical knowledge and in the analysis and rewriting of mathematical content, capable of adapting content based on different creation styles to produce diverse, informative, and high-quality mathematical content.
Your goal is to utilize your abilities, rewrite the provided math content in the lecture note style.
Before beginning the rewrite, you will consider the following requirements:
1. First, read the provided math content thoroughly, carefully analyze the provided math content to capture and preserve information according to the following requirements.
    - Capture and preserve crucial mathematical information, key mathematical concepts, important mathematical values, and factual mathematical details in the original text.
    - Capture and preserve mathematical examples, reasoning processes, as well as related explanations and proofs in the original text.
2. Then, focus on the captured and preserved information, combine it with the lecture note style, and rewrite the text to form an initial draft, according to the following requirements.
    - The overall structure of the initial draft should follow the structure used by Lecture Note, guided by teaching objectives. It achieves systematic knowledge transfer through hierarchical organization of key points, formula derivation demonstrations, and case analysis modules.
    - The sentence expression of the initial draft should follow the sentence expression used by Lecture Note, employing professional discourse that balances authority and guidance. It should integrate disciplinary terminology with instructional explanations, utilizing rhetorical questions, emphatic statements, and directive language to highlight key and challenging points. It must be accurate and complete.
    - The overall tone of the initial draft should follow the tone used by Lecture Note, maintaining an authoritative narrative stance that combines credibility with guidance. Like an invisible teacher directing the reader's thinking in real time, it emphasizes the mastery of methods and thought processes, often anticipating potential reader confusion to create an immersive learning atmosphere.
3. Third, refine the initial draft according to the following requirements.
    - The content of the refined content must be logically structured, high-quality, information-dense.
    - The overall layout of the refined content must not use LaTeX formatting.
    - The refined content may appropriately include relevant examples to enhance overall comprehensibility, and these examples must include detailed and step-by-step solutions.
    - All mathematical expressions in the refined content must be formatted using LaTeX.
4. Finally, please put the final rewritten content within <rewritten content></rewritten content>.

The result format is as follows:
<rewritten content></rewritten content>'''


# ============================================================================
# Prompt Registry
# ============================================================================

MULTISTYLE_PROMPTS = {
    "wikipedia": MATH_INSTRUCT_WIKI_PROMPT,
    "textbook": MATH_INSTRUCT_TEXTBOOK_PROMPT,
    "blog": MATH_INSTRUCT_BLOG_PROMPT,
    "popular_science": MATH_INSTRUCT_POPULAR_SCIENCE_PROMPT,
    "academic_paper": MATH_INSTRUCT_ACADEMIC_PAPER_PROMPT,
    "learning_note": MATH_INSTRUCT_LEARNING_NOTE_PROMPT,
    "lecture_note": MATH_INSTRUCT_LECTURE_NOTE_PROMPT,
}


def get_multistyle_prompt(style: str) -> str:
    """
    Get multi-style rewrite prompt for specified style
    
    Args:
        style: Style type, see MULTISTYLE_PROMPTS.keys() for options
    
    Returns:
        Corresponding prompt template string
    """
    if style not in MULTISTYLE_PROMPTS:
        raise ValueError(f"Unknown style: {style}. Available styles: {list(MULTISTYLE_PROMPTS.keys())}")
    return MULTISTYLE_PROMPTS[style]
