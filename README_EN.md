# UltraData-Math

<div align="center">
  <img src="assets/ultradata-math-logo.png" width="600"/>
</div>

<div align="center">

[🤗 Dataset](https://huggingface.co/datasets/openbmb/UltraData-Math-L1) | [💻 Code Repository](https://github.com/UltraData-OpenBMB/UltraData-Math)

</div>

## 📚 Introduction

High-quality pre-training data is crucial for enhancing the mathematical reasoning capabilities of Large Language Models (LLMs). However, existing mathematical pre-training data construction schemes have the following shortcomings:

- **HTML Parsing Level**: General extractors (such as trafilatura, readability) are mainly designed for news/article scenarios, lacking specialized processing for mathematical formulas and other content, often leading to formula structure destruction or loss; meanwhile, mathematical discussions on forum-like pages are difficult to extract completely.
- **Data Quality Level**: Existing datasets generally lack a systematic quality grading mechanism, with high-value mathematical content mixed with low-quality noise.
- **Data Diversity Level**: Mainstream datasets mostly originate from textbooks or competition question banks, lacking mathematical discussions and application scenarios in real web pages; synthetic data formats are single, difficult to cover diverse needs such as multi-turn dialogues and multi-style expressions.

To address these issues, we propose ***UltraData-Math***—a large-scale high-quality pre-training dataset for mathematical reasoning tasks. This dataset is developed based on the [Ultra-Data](xxx) L0-L4 hierarchical data processing framework, containing four progressive levels:

- **L0 Raw Data Layer**: Developed a mathematical parser based on *magic-html*, combined with *w3m* layout preservation rendering and multi-level fallback strategies, standardizing MathML, KaTeX, and AsciiMath into LaTeX format.
- **L1 Filtered Data Layer**: Cleans noise through heuristic rules and performs document-level deduplication.
- **L2 Selected Data Layer**: Uses closed-source large models to annotate seed data and distills it into a lightweight Embedding classifier to achieve efficient quality grading of the full corpus.
- **L3 Synthetic Data Layer**: Generates synthetic data in various formats such as Q&A, multi-turn dialogues, multi-style rewriting, and knowledge-grounded textbooks based on multi-model ensemble.

Experiments show that on the MiniCPM-1B architecture, ***UltraData-Math*** achieves a score of **37.02** on the MATH benchmark, an improvement of **+3.62** compared to Nemotron-CC 4plus; it achieves **61.79** on GSM8K, an improvement of **+3.34**, while maintaining code generation and general knowledge capabilities.

***UltraData-Math*** has been applied to the mathematical pre-training of the [MiniCPM Series](https://huggingface.co/collections/openbmb/minicpm-4-6841ab29d180257e940baa9b) models. This repository open-sources the core tools and configurations of the data processing pipeline.


## 🏗️ Data Processing Pipeline

To break through the limitations of existing mathematical datasets in quality and diversity, we established a refined grading standard centered on "mathematical content integrity" and "information density". ***UltraData-Math*** adopts the **L0-L4 Data Grading System** proposed by the UltraData position paper. Through standardized level definitions, it achieves orderly management and efficient flow of mathematical data assets. Each level represents higher data purity and mathematical value, while also corresponding to a more refined degree of processing.

<div align="center">
  <img src="assets/ultradata-math-pipeline.png" width="900"/>
</div>

| Level | Name | Function | Tool |
|:---:|:---:|:---|:---|
| **L0** | Raw Data | HTML Math Parsing | `UltraData-Math-L0-Parser` |
| **L1** | Filtered Data | Format Repair + Content Filtering | `UltraData-Math-L1-Cleaner` |
| **L2** | Selected Data | Quality Classification Model Screening | `UltraData-Math-L2-Selector` |
| **L3** | Synthetic Data | Multi-format Data Synthesis | `UltraData-Math-L3-Generator` |

---

### L0 - Raw Data

**Definition:** Initial data extracted from web sources like Common Crawl via parsers. Addressing the limitations of general HTML extractors in capturing mathematical formulas, we developed `UltraData-Math-L0-Parser` based on [magic-html](https://github.com/opendatalab/magic-html).

#### 🔧 UltraData-Math-L0-Parser

An enhanced HTML parser based on magic-html, optimized specifically for mathematical content extraction.

**📊 Comparison with Original magic-html**

| Feature | magic-html | UltraData-Math-L0-Parser |
|:---|:---:|:---:|
| Unified Extraction Mode (UnifiedParser) | ❌ | ✅ Automatically identifies and merges scattered posts |
| Multi-level Fallback Strategy | ❌ | ✅ `primary` → `wild_text` → `readability` |
| Image LaTeX Intelligent Extraction | ❌ | ✅ Recovers formulas from `alt` attributes |
| Math Container Protection | ❌ | ✅ Protects `<math>` tags from accidental deletion |
| Configurable Table/Image | ❌ | ✅ `include_tables` / `include_images` |

**✨ Core Features**

**1. UnifiedParser - Unified Extraction Mode**

Merges extraction logic for Article and Forum, automatically adapting to different page types:

```python
from ultradata_math_parser import GeneralParser

parser = GeneralParser()
result = parser.extract(html, base_url=url, html_type="unified")
# Returns: {html, title, text_length, fallback_strategy, forum_assembled}
```

**2. Multi-level Fallback Strategy**

Automatically triggers a multi-level fallback chain when the main extracted content is insufficient, ensuring content integrity.

**3. Mathematical Formula Format Standardization**

Supports converting various mathematical formats into unified LaTeX, and intelligently recovers formulas from image `alt` attributes:

| Input Format | Conversion Method |
|:---|:---|
| MathML (`<math>`) | XSLT Conversion |
| KaTeX (`.katex`) | Extract annotation |
| AsciiMath | py-asciimath Conversion |
| LaTeX Image | Intelligent recovery from URL/alt |
| `\begin{equation}` | Direct Extraction |


**Characteristics:** Mathematical formulas are completely preserved, LaTeX format is unified, serving as the foundational layer resource for subsequent cleaning and screening.

---

### L1 - Filtered Data

**Definition:** Data cleaned through heuristic rules, with standardized text format and basic readability.

**Processing Methods:**
- **Mapper (Format Repair)**: Cleans invisible characters, continuous line breaks, navigation bars/buttons, and other noisy text.
- **Filter (Content Filtering)**: Filters short texts and texts with abnormal lengths.

**Characteristics:** Data noise is significantly reduced, format consistency is improved; see [`UltraData-Math-L1-Cleaner/README.md`](./UltraData-Math-L1-Cleaner/README.md) for details.

---

### L2 - Selected Data

**Definition:** Data screened by quality assessment models, possessing high information density and mathematical educational value, with clear themes and coherent reasoning logic.

**Processing Methods:**
- Annotate seed data using closed-source large models.
- Distill into a lightweight Embedding classifier to achieve efficient scoring of the full corpus.
- Multi-dimensional quality tags (mathematical depth, reasoning completeness, educational value).

**Characteristics:** Retains samples with high contribution to improving the model's mathematical reasoning ability, further reducing noise and significantly increasing mathematical content density. It is the core resource for the pre-training phase.

---

### L3 - Synthetic Data

**Definition:** High-quality mathematical data that has undergone deep rewriting or synthesis, with an extremely high degree of structure, clear reasoning steps, and educational value.

**Processing Methods:**
- Q&A Format Synthesis (Question-Answer Pair Generation)
- Multi-turn Dialogue Synthesis (Math Tutoring Scenario)
- Multi-style Rewriting (Textbook Style, Competition Style, Popular Science Style)
- Knowledge Point Textbook Generation (Generates textbook-style learning materials based on knowledge points)

**Characteristics:** Strong text readability, complete reasoning steps, standardized structure, high sample quality. It is the core resource for MidTraining and SFT phases.

## 📈 Experimental Results

We used the **MiniCPM-1.2B** model architecture and **MiniCPM3-4B** tokenizer for experimental verification. Each experiment was conducted with a training volume of **100 billion Tokens**, allowing for comprehensive verification of data performance within a parameter range with controllable computational efficiency. We used the Lighteval library for model evaluation, and all evaluation metrics are based on **Zero-Shot** settings. Evaluation benchmarks include:

- **Mathematical Reasoning:** GSM8K, MATH, R-Bench, Math-Bench
- **Code Generation:** HumanEval, MBPP
- **Comprehensive Knowledge:** MMLU, MMLU-STEM

### L0 Parser Ablation Study

Based on data from the same source, we used different parsers for extraction and trained independently to directly compare the effects of parsing strategies:

| Parser | Average | MMLU | GSM8K | HumanEval | math | mbpp_full | mmlu-stem |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **UltraData-Math-L0-Parser (Ours)** | **43.44** | 51.41 | 54.97 | **31.71** | **28.72** | 47.10 | 46.76 |
| trafilatura + w3m | 42.33 | 50.95 | 54.51 | 27.44 | 27.64 | 47.93 | 45.52 |
| trafilatura | 42.44 | 51.42 | 56.03 | 26.83 | 28.08 | 45.64 | 46.62 |
| Megamath | 42.32 | 51.46 | 54.06 | 29.88 | 26.04 | 45.64 | 46.81 |
| magic-html + w3m | 41.29 | 51.23 | 51.63 | 26.83 | 26.58 | 45.02 | 46.45 |

### Full Evaluation Results

We used a single dataset for independent training to directly compare the effects of different data sources:

| Model | Average | MMLU | GSM8K | HumanEval | math | mbpp_full | mmlu-stem | R-bench | Math-bench |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **UltraData-Math (Ours)** | **43.79** | 51.67 | **61.79** | 32.93 | **37.02** | **49.27** | 45.93 | 23.38 | **48.33** |
| Nemotron-cc 4plus mind | 43.45 | 52.09 | 59.97 | 34.76 | 35.96 | 48.03 | 45.99 | 23.51 | 47.25 |
| Nemotron-cc 4plus | 42.62 | 51.96 | 58.45 | 35.37 | 33.40 | 46.47 | 45.67 | 22.74 | 46.92 |
| MegaMath-Web-Pro | 41.38 | 53.16 | 56.71 | 31.71 | 32.12 | 47.10 | 47.15 | 21.23 | 41.83 |
| FineMath-4+ | 40.51 | 50.90 | 56.25 | 29.88 | 29.84 | 48.96 | 44.98 | 18.93 | 44.33 |


## ❤️ Acknowledgements

- **L0 Parsing Layer**: [magic-html](https://github.com/opendatalab/magic-html), [w3m](http://w3m.sourceforge.net/), [trafilatura](https://github.com/adbar/trafilatura)
- **L3 Synthesis Layer**: [Qwen2.5-72B-Instruct](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct), [Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B), [GLM-4.5](https://huggingface.co/zai-org/GLM-4.5)
- **Seed Data**: [Nemotron-CC-Math](https://huggingface.co/datasets/nvidia/Nemotron-CC-Math-v1), [MegaMath](https://huggingface.co/datasets/LLM360/MegaMath), [FineMath](https://huggingface.co/datasets/HuggingFaceTB/finemath)

## 📜 License

This project is licensed under the [Apache 2.0](./LICENSE) license.
