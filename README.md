# UltraData-Math

<div align="center">
  <img src="assets/ultradata-math-logo.png" width="600"/>
</div>

<p align="center">
<a href="https://huggingface.co/datasets/openbmb/UltraData-Math">🤗 Dataset</a> | <a href="https://github.com/UltraData-OpenBMB/UltraData-Math">💻 Source Code</a> | <a href="README_ZH.md">🇨🇳 中文 README</a>
</p>

***UltraData-Math*** is a large-scale, high-quality mathematical pre-training dataset totaling **290B+ tokens** across three progressive tiers—**L1** (170.5B tokens web corpus), **L2** (33.7B tokens quality-selected), and **L3** (88B tokens multi-format refined)—designed to systematically enhance mathematical reasoning in LLMs. It has been applied to the mathematical pre-training of the [MiniCPM Series](https://huggingface.co/collections/openbmb/minicpm4) models.

## 🆕 What's New

- **2026.02.09**: Released UltraData-Math (290B+ tokens), a large-scale high-quality mathematical pre-training dataset with three progressive tiers (L1/L2-preview/L3).

## 📚 Introduction

High-quality pre-training data is crucial for enhancing the mathematical reasoning capabilities of large language models (LLMs). However, existing mathematical pre-training data construction schemes have the following shortcomings:

- **HTML Parsing**: General parsers (such as trafilatura, readability) are mainly designed for news/article parsing, lacking specialized processing for mathematical formulas and other content, often leading to formula structure destruction or loss; meanwhile, mathematical discussions on forum-like pages are difficult to extract completely.
- **Data Quality**: Existing datasets generally lack a systematic quality grading mechanism, with high-value mathematical content mixed with low-quality noise.
- **Data Diversity**: Mainstream datasets mostly originate from textbooks or competition question banks, lacking mathematical discussions and application scenarios in real web pages; synthetic data formats are single, difficult to cover diverse needs such as multi-turn dialogues and multi-style expressions.

To address these issues, we propose ***UltraData-Math***—a large-scale high-quality pre-training dataset for mathematical reasoning tasks. This dataset is developed based on the [UltraData](https://ultradata.openbmb.cn/blog/position-paper) L0-L4 Tiered Data Management Framework, containing four progressive levels:

- **L0 Raw Data**: Develops a mathematical parser based on *magic-html*, combined with *w3m* layout preservation rendering and multi-level fallback strategies, standardizing MathML, KaTeX, and AsciiMath into LaTeX format.
- **L1 Filtered Data**: Cleans noise through heuristic rules and performs document-level deduplication.
- **L2 Selected Data**: Uses proprietary large models to annotate seed data and distills it into a lightweight embedding classifier to achieve efficient quality grading of the full corpus.
- **L3 Refined Data**: Produces structured content with clear reasoning through rewriting, synthetic generation, and refinement in various formats such as Q&A, multi-turn dialogues, multi-style rewriting, and knowledge-grounded textbooks.

Experiments show that on the MiniCPM-1.2B architecture, ***UltraData-Math*** achieves a score of **37.02pp** on the MATH500 benchmark, an improvement of **+3.62pp** compared to Nemotron-CC 4plus; it achieves **61.79pp** on GSM8K, an improvement of **+3.34pp**, while maintaining code generation and general knowledge capabilities.

***UltraData-Math*** has been applied to the mathematical pre-training of the [MiniCPM Series](https://huggingface.co/collections/openbmb/minicpm-4-6841ab29d180257e940baa9b) models. This repository open-sources the core tools and configurations of the data processing pipeline.

- **[UltraData-Math-L1](https://huggingface.co/datasets/openbmb/UltraData-Math)**: Large-scale high-quality mathematical pre-training dataset, containing 170.5B tokens of web mathematical corpus.
- **[UltraData-Math-L2](https://huggingface.co/datasets/openbmb/UltraData-Math-L2)**: High-quality mathematical pre-training dataset selected by the quality model, containing 33.7B tokens of high-quality web mathematical corpus.
- **[UltraData-Math-L3](https://huggingface.co/datasets/openbmb/UltraData-Math-L3)**: High-quality refined mathematical dataset, containing 88B tokens of multi-format refined data (Q&A, multi-turn dialogues, knowledge textbooks, etc.).

## 🏗️ Data Processing Pipeline

To break through the limitations of existing mathematical datasets in quality and diversity, we established a refined grading standard centered on "mathematical content integrity" and "information density". ***UltraData-Math*** adopts the **L0-L4 Tiered Data Management Framework** proposed by the [UltraData](https://ultradata.openbmb.cn/blog/position-paper) paper. Through standardized level definitions, it achieves orderly management and efficient flow of mathematical data assets. Each level represents higher data purity and mathematical value, while also corresponding to a more refined degree of processing.

<div align="center">
  <img src="assets/ultradata-math-pipeline.png" width="900"/>
</div>

| Level | Name | Function | Tool |
|:---:|:---:|:---|:---|
| **L0** | Raw Data | HTML Math Parsing | `UltraData-Math-L0-Parser` |
| **L1** | Filtered Data | Format Repair + Content Filtering | `UltraData-Math-L1-Cleaner` |
| **L2** | Selected Data | Quality Classification Model Screening | `UltraData-Math-L2-Selector` |
| **L3** | Refined Data | Multi-format Data Refinement | `UltraData-Math-L3-Generator` |

---

### L0 - Raw Data

**Definition:** Initial data extracted from web sources like Common Crawl via parsers. Addressing the limitations of general HTML parsers in capturing mathematical formulas, we developed `UltraData-Math-L0-Parser` based on [magic-html](https://github.com/opendatalab/magic-html).

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
- Annotate seed data using proprietary large models.
- Distill into a lightweight embedding classifier to achieve efficient scoring of the full corpus.
- Multi-dimensional quality tags (mathematical depth, reasoning completeness, educational value).

**Characteristics:** Retains samples with high contribution to improving the model's mathematical reasoning ability, further reducing noise and significantly increasing mathematical content density. It is the core resource for the pre-training phase.

---

### L3 - Refined Data

**Definition:** High-quality mathematical data that has undergone deep rewriting, synthesis, and refinement, with structured content, clear reasoning steps, and explicit educational intent, achieving textbook-quality standards.

**Processing Methods:**
- Q&A Format Generation (Question-Answer Pair with explicit reasoning steps)
- Multi-turn Dialogue Synthesis (Math Tutoring Scenario)
- Multi-style Rewriting (Textbook Style, Competition Style, Popular Science Style)
- Knowledge Point Textbook Generation (Generates textbook-style learning materials based on knowledge points)
- Format Repair and Enhancement (Fix broken LaTeX formulas, inconsistent notation, enhance content coherence)

**Characteristics:** Strong text readability, complete reasoning steps, standardized structure, high sample quality. It is the core resource for MidTraining and SFT phases.

## 📈 Experimental Results

We evaluated data quality using the **Decay Verification** method: continuing pre-training of a **MiniCPM-1.2B** base model (pre-trained on 1.3T tokens with **MiniCPM3-4B** tokenizer) with **~100B tokens** (30% target data + 70% general data). We used [OpenCompass](https://github.com/open-compass/opencompass) as our evaluation framework. Evaluation benchmarks include:

- **General English:** MMLU, ARC-E, ARC-C, BigBench Hard (BBH), CommonSenseQA, HellaSwag, OpenbookQA, PIQA, SIQA, Winogrande
- **General Chinese:** C-Eval, CMMLU
- **Math Reasoning:** MATH500, GSM8K, Math-Bench, R-Bench-Math
- **Code Reasoning:** MBPP, HumanEval

### Effectiveness of L0 Parsing Strategy

To fairly compare different parsing strategies, we conducted experiments on a data subset sampled from the **2023-2024** distribution. We re-parsed the raw HTML from this source using different parsers. This comparison demonstrates the **effectiveness of our L0 Parser** against other parsers.

<div align="center">
  <img src="assets/ultradata-math-l0-parser-comparison.png" width="700"/>
</div>

### Pipeline Effectiveness (L1 vs L2 vs L3)

To validate the effectiveness of our L0-L3 tiered framework, we conducted ablation studies comparing models trained on different tiers of UltraData-Math. Unlike the L0 parser comparison above (which used a 2023-2024 subset), these results are based on the **full dataset**. Results demonstrate that higher-tier data (L3) significantly boosts mathematical reasoning (MATH500, GSM8K) and general capabilities.

<div align="center">
  <img src="assets/ultradata-math-l1l2l3-comparison.png" width="700"/>
</div>

### Full Evaluation Results

To compare against existing public mathematical pre-training datasets, we trained models independently on each dataset using the same model architecture and training budget (~100B tokens). The baselines include [Nemotron-CC-Math](https://huggingface.co/datasets/nvidia/Nemotron-CC-Math-v1), [MegaMath-Web-Pro](https://huggingface.co/datasets/LLM360/MegaMath), and [FineMath](https://huggingface.co/datasets/HuggingFaceTB/finemath). All models are evaluated under identical conditions for a fair comparison:

<div align="center">
  <img src="assets/ultradata-math-full-comparison.png" width="700"/>
</div>

## ❤️ Acknowledgements

- **L0 Parsing Layer**: [magic-html](https://github.com/opendatalab/magic-html), [w3m](http://w3m.sourceforge.net/), [trafilatura](https://github.com/adbar/trafilatura)
- **L3 Refined Layer**: [Qwen2.5-72B-Instruct](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct), [Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B), [GLM-4.5](https://huggingface.co/zai-org/GLM-4.5)
- **Seed Data**: [Nemotron-CC-Math](https://huggingface.co/datasets/nvidia/Nemotron-CC-Math-v1), [MegaMath](https://huggingface.co/datasets/LLM360/MegaMath), [FineMath](https://huggingface.co/datasets/HuggingFaceTB/finemath)

## 📖 Citation

If you find **UltraData-Math** useful in your research, please consider citing:

```bibtex
@misc{ultradata-math,
  title={UltraData-Math},
  author={UltraData Team},
  year={2026},
  url={https://huggingface.co/datasets/openbmb/UltraData-Math},
  publisher={Hugging Face}
}
```

## 📜 License

This project is licensed under the [Apache 2.0](./LICENSE) license.
