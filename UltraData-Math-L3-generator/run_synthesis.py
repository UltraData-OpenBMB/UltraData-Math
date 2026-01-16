# -*- coding: utf-8 -*-
"""
UltraData-Math L3 - Data Synthesis Script

OpenAI API-based data synthesis tool, supporting:
- Q&A synthesis
- Multi-turn conversation synthesis
- Multi-style rewriting
- Knowledge extraction and textbook exercise generation

Usage:
    python run_synthesis.py \
        --input data.jsonl \
        --output output.jsonl \
        --task qa \
        --level high_school \
        --model gpt-4o \
        --workers 10
"""

import argparse
import asyncio
import json
import os
import re
import time
from pathlib import Path
from typing import Optional

from openai import AsyncOpenAI

# Import prompt templates
from qa_synthesis import QA_PROMPTS, get_qa_prompt
from conversation_synthesis import CONVERSATION_PROMPTS, get_conversation_prompt
from multistyle_rewrite import MULTISTYLE_PROMPTS, get_multistyle_prompt
from knowledge_textbook import (
    get_knowledge_extraction_prompt,
    get_textbook_exercise_prompt,
    TEXTBOOK_EXERCISE_PROMPTS,
)


# ============================================================================
# Configuration
# ============================================================================

DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096
DEFAULT_WORKERS = 10
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0


# ============================================================================
# Output Parsers
# ============================================================================

def parse_qa_output(response: str) -> dict:
    """Parse Q&A synthesis output"""
    result = {"raw": response}
    
    # Extract <problem> and <solution>
    problem_match = re.search(r"<problem>(.*?)</problem>", response, re.DOTALL)
    solution_match = re.search(r"<solution>(.*?)</solution>", response, re.DOTALL)
    
    if problem_match:
        result["problem"] = problem_match.group(1).strip()
    if solution_match:
        result["solution"] = solution_match.group(1).strip()
    
    return result


def parse_conversation_output(response: str) -> dict:
    """Parse conversation synthesis output"""
    result = {"raw": response}
    
    # Try multiple tags
    for tag in ["discussions", "conversation", "interaction"]:
        match = re.search(rf"<{tag}>(.*?)</{tag}>", response, re.DOTALL)
        if match:
            result["content"] = match.group(1).strip()
            result["type"] = tag
            break
    
    return result


def parse_rewrite_output(response: str) -> dict:
    """Parse multi-style rewrite output"""
    result = {"raw": response}
    
    match = re.search(r"<rewritten content>(.*?)</rewritten content>", response, re.DOTALL)
    if match:
        result["rewritten"] = match.group(1).strip()
    
    return result


def parse_knowledge_output(response: str) -> dict:
    """Parse knowledge extraction output"""
    result = {"raw": response}
    
    if "no result" in response.lower():
        result["knowledge_points"] = []
        return result
    
    # Extract all knowledge points
    pattern = r"<mathematical knowledge point\d*>(.*?)</mathematical knowledge point\d*>"
    matches = re.findall(pattern, response, re.DOTALL)
    result["knowledge_points"] = [m.strip() for m in matches]
    
    return result


def parse_textbook_output(response: str) -> dict:
    """Parse textbook exercise output"""
    result = {"raw": response}
    
    match = re.search(r"<material>(.*?)</material>", response, re.DOTALL)
    if match:
        result["material"] = match.group(1).strip()
    
    return result


OUTPUT_PARSERS = {
    "qa": parse_qa_output,
    "conversation": parse_conversation_output,
    "rewrite": parse_rewrite_output,
    "knowledge": parse_knowledge_output,
    "textbook": parse_textbook_output,
}


# ============================================================================
# API Client
# ============================================================================

class SynthesisClient:
    """Data synthesis client"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
    ):
        self.client = AsyncOpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url or os.getenv("OPENAI_BASE_URL"),
        )
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    async def generate(self, prompt: str) -> str:
        """Call API to generate content"""
        for attempt in range(self.max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
                return response.choices[0].message.content
            except Exception as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                else:
                    raise e
        return ""


# ============================================================================
# Synthesis Tasks
# ============================================================================

class SynthesisTask:
    """Base class for synthesis tasks"""
    
    def __init__(self, client: SynthesisClient, text_field: str = "text"):
        self.client = client
        self.text_field = text_field
    
    def get_prompt(self, sample: dict) -> str:
        raise NotImplementedError
    
    def parse_output(self, response: str) -> dict:
        raise NotImplementedError
    
    async def process(self, sample: dict) -> dict:
        """Process a single sample"""
        prompt = self.get_prompt(sample)
        response = await self.client.generate(prompt)
        parsed = self.parse_output(response)
        return {**sample, "synthesis_result": parsed}


class QASynthesisTask(SynthesisTask):
    """Q&A synthesis task"""
    
    def __init__(self, client: SynthesisClient, level: str, text_field: str = "text"):
        super().__init__(client, text_field)
        self.level = level
        self.prompt_template = get_qa_prompt(level)
    
    def get_prompt(self, sample: dict) -> str:
        text = sample.get(self.text_field, "")
        return self.prompt_template.format(text=text)
    
    def parse_output(self, response: str) -> dict:
        return parse_qa_output(response)


class ConversationSynthesisTask(SynthesisTask):
    """Conversation synthesis task"""
    
    def __init__(self, client: SynthesisClient, style: str, text_field: str = "text"):
        super().__init__(client, text_field)
        self.style = style
        self.prompt_template = get_conversation_prompt(style)
    
    def get_prompt(self, sample: dict) -> str:
        text = sample.get(self.text_field, "")
        return self.prompt_template.format(text=text)
    
    def parse_output(self, response: str) -> dict:
        return parse_conversation_output(response)


class RewriteSynthesisTask(SynthesisTask):
    """Multi-style rewrite task"""
    
    def __init__(self, client: SynthesisClient, style: str, text_field: str = "text"):
        super().__init__(client, text_field)
        self.style = style
        self.prompt_template = get_multistyle_prompt(style)
    
    def get_prompt(self, sample: dict) -> str:
        text = sample.get(self.text_field, "")
        return self.prompt_template.format(text=text)
    
    def parse_output(self, response: str) -> dict:
        return parse_rewrite_output(response)


class KnowledgeExtractionTask(SynthesisTask):
    """Knowledge extraction task"""
    
    def __init__(self, client: SynthesisClient, text_field: str = "text"):
        super().__init__(client, text_field)
        self.prompt_template = get_knowledge_extraction_prompt()
    
    def get_prompt(self, sample: dict) -> str:
        text = sample.get(self.text_field, "")
        return self.prompt_template.format(text=text)
    
    def parse_output(self, response: str) -> dict:
        return parse_knowledge_output(response)


class TextbookExerciseTask(SynthesisTask):
    """Textbook exercise generation task"""
    
    def __init__(self, client: SynthesisClient, difficulty: str, knowledge_field: str = "knowledge_point"):
        super().__init__(client)
        self.difficulty = difficulty
        self.knowledge_field = knowledge_field
        self.prompt_template = get_textbook_exercise_prompt(difficulty)
    
    def get_prompt(self, sample: dict) -> str:
        knowledge = sample.get(self.knowledge_field, "")
        return self.prompt_template.format(mathematical_knowledge_point=knowledge)
    
    def parse_output(self, response: str) -> dict:
        return parse_textbook_output(response)


# ============================================================================
# Batch Processing
# ============================================================================

async def process_batch(
    task: SynthesisTask,
    samples: list[dict],
    workers: int,
    progress_callback=None,
) -> list[dict]:
    """Process batch data concurrently"""
    semaphore = asyncio.Semaphore(workers)
    results = []
    completed = 0
    
    async def process_with_semaphore(sample: dict, idx: int):
        nonlocal completed
        async with semaphore:
            try:
                result = await task.process(sample)
                result["_status"] = "success"
            except Exception as e:
                result = {**sample, "_status": "error", "_error": str(e)}
            
            completed += 1
            if progress_callback:
                progress_callback(completed, len(samples))
            
            return idx, result
    
    tasks = [process_with_semaphore(sample, i) for i, sample in enumerate(samples)]
    task_results = await asyncio.gather(*tasks)
    
    # Sort by original order
    task_results.sort(key=lambda x: x[0])
    results = [r[1] for r in task_results]
    
    return results


def load_jsonl(filepath: str) -> list[dict]:
    """Load JSONL file"""
    data = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def save_jsonl(data: list[dict], filepath: str):
    """Save JSONL file"""
    with open(filepath, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


# ============================================================================
# Command Line Interface
# ============================================================================

def create_task(args, client: SynthesisClient) -> SynthesisTask:
    """Create synthesis task based on arguments"""
    task_type = args.task
    
    if task_type == "qa":
        level = args.level or "high_school"
        if level not in QA_PROMPTS:
            raise ValueError(f"Invalid QA level: {level}. Available: {list(QA_PROMPTS.keys())}")
        return QASynthesisTask(client, level, args.text_field)
    
    elif task_type == "conversation":
        style = args.style or "teacher_student"
        if style not in CONVERSATION_PROMPTS:
            raise ValueError(f"Invalid conversation style: {style}. Available: {list(CONVERSATION_PROMPTS.keys())}")
        return ConversationSynthesisTask(client, style, args.text_field)
    
    elif task_type == "rewrite":
        style = args.style or "textbook"
        if style not in MULTISTYLE_PROMPTS:
            raise ValueError(f"Invalid rewrite style: {style}. Available: {list(MULTISTYLE_PROMPTS.keys())}")
        return RewriteSynthesisTask(client, style, args.text_field)
    
    elif task_type == "knowledge":
        return KnowledgeExtractionTask(client, args.text_field)
    
    elif task_type == "textbook":
        difficulty = args.difficulty or "easy"
        if difficulty not in TEXTBOOK_EXERCISE_PROMPTS:
            raise ValueError(f"Invalid difficulty: {difficulty}. Available: {list(TEXTBOOK_EXERCISE_PROMPTS.keys())}")
        return TextbookExerciseTask(client, difficulty, args.knowledge_field)
    
    else:
        raise ValueError(f"Unknown task type: {task_type}")


def print_progress(completed: int, total: int):
    """Print progress"""
    percent = completed / total * 100
    print(f"\rProgress: {completed}/{total} ({percent:.1f}%)", end="", flush=True)


async def main_async(args):
    """Async main function"""
    # Create client
    client = SynthesisClient(
        api_key=args.api_key,
        base_url=args.base_url,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        max_retries=args.max_retries,
    )
    
    # Create task
    task = create_task(args, client)
    
    # Load data
    print(f"Loading data from {args.input}...")
    samples = load_jsonl(args.input)
    
    # Limit processing count
    if args.limit:
        samples = samples[:args.limit]
    
    print(f"Processing {len(samples)} samples with {args.workers} workers...")
    start_time = time.time()
    
    # Process data
    results = await process_batch(
        task,
        samples,
        args.workers,
        progress_callback=print_progress if not args.quiet else None,
    )
    
    elapsed = time.time() - start_time
    print(f"\nCompleted in {elapsed:.2f}s ({len(samples)/elapsed:.1f} samples/s)")
    
    # Statistics
    success_count = sum(1 for r in results if r.get("_status") == "success")
    error_count = len(results) - success_count
    print(f"Success: {success_count}, Error: {error_count}")
    
    # Save results
    save_jsonl(results, args.output)
    print(f"Results saved to {args.output}")


def main():
    parser = argparse.ArgumentParser(
        description="UltraData-Math L3 Data Synthesis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Q&A synthesis (high school level)
  python run_synthesis.py -i data.jsonl -o qa_output.jsonl -t qa --level high_school

  # Multi-turn conversation synthesis (teacher-student)
  python run_synthesis.py -i data.jsonl -o conv_output.jsonl -t conversation --style teacher_student

  # Multi-style rewrite (textbook style)
  python run_synthesis.py -i data.jsonl -o rewrite_output.jsonl -t rewrite --style textbook

  # Knowledge extraction
  python run_synthesis.py -i data.jsonl -o knowledge_output.jsonl -t knowledge

  # Textbook exercise generation (medium difficulty)
  python run_synthesis.py -i knowledge.jsonl -o textbook_output.jsonl -t textbook --difficulty medium

Task Types:
  qa           Q&A synthesis
               --level: grade_school, middle_school, high_school, college

  conversation Multi-turn conversation synthesis
               --style: two_professors, teacher_student, two_students,
                        interview, problem_solving, layman_expert, debate

  rewrite      Multi-style rewrite
               --style: wikipedia, textbook, blog, popular_science,
                        academic_paper, learning_note, lecture_note

  knowledge    Knowledge extraction

  textbook     Textbook exercise generation
               --difficulty: easy, medium, hard
        """
    )
    
    # Input/Output
    parser.add_argument("-i", "--input", required=True, help="Input JSONL file path")
    parser.add_argument("-o", "--output", required=True, help="Output JSONL file path")
    
    # Task configuration
    parser.add_argument("-t", "--task", required=True,
                        choices=["qa", "conversation", "rewrite", "knowledge", "textbook"],
                        help="Synthesis task type")
    parser.add_argument("--level", help="Q&A difficulty level")
    parser.add_argument("--style", help="Conversation/rewrite style")
    parser.add_argument("--difficulty", help="Textbook exercise difficulty")
    
    # Field configuration
    parser.add_argument("--text-field", default="text", help="Input text field name (default: text)")
    parser.add_argument("--knowledge-field", default="knowledge_point", help="Knowledge point field name (default: knowledge_point)")
    
    # API configuration
    parser.add_argument("--api-key", help="OpenAI API Key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--base-url", help="API Base URL (or set OPENAI_BASE_URL env var)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE, help=f"Sampling temperature (default: {DEFAULT_TEMPERATURE})")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS, help=f"Max tokens to generate (default: {DEFAULT_MAX_TOKENS})")
    
    # Execution configuration
    parser.add_argument("-w", "--workers", type=int, default=DEFAULT_WORKERS, help=f"Concurrency (default: {DEFAULT_WORKERS})")
    parser.add_argument("--max-retries", type=int, default=DEFAULT_MAX_RETRIES, help=f"Max retries (default: {DEFAULT_MAX_RETRIES})")
    parser.add_argument("--limit", type=int, help="Limit number of samples to process")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode")
    
    args = parser.parse_args()
    
    # Run
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
