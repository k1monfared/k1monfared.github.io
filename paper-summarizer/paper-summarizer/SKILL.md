---
name: paper-summarizer
description: >
  Generate structured key takeaways from academic papers, patents, or technical
  documents. Use this skill whenever the user asks to summarize a paper, extract
  key contributions, create a TLDR, generate takeaways, or distill the main
  results from a PDF. Also trigger when the user provides paper PDFs and asks
  for structured output, or wants to populate a website/portfolio with paper
  summaries. Works with any academic discipline.
---

# Paper Summarizer

You are generating structured key takeaways from academic papers. Your audience
is researchers who want a quick, precise understanding of what a paper does —
not a vague rewording of the abstract. Think of this as the summary a
knowledgeable colleague would give over coffee: precise enough to be useful,
concise enough to be fast.

## Input

The user provides one or more PDF file paths (or sometimes the text of a paper
directly). Read each PDF — the first 10 pages usually contain everything you
need (abstract, introduction, main results, methodology).

## Output Format

For each paper, produce a structured summary with exactly three sections:

```
<b>Problem:</b> [1 sentence]
<b>Key result:</b> [1-2 sentences]
<b>Method:</b> [1 sentence]
```

Separate sections with `<br>` tags so it renders as a single HTML block.

### Section Guidelines

**Problem** — What question, gap, or challenge does this paper address? Frame
it as a question or "how to" statement. Be specific: "Can the structured
inverse eigenvalue problem be extended to infinite graphs?" is better than
"This paper studies inverse eigenvalue problems."

**Key result** — The main theorem, finding, or contribution. Include the
precise mathematical statement if the paper is mathematical. For empirical
papers, state the main finding with effect size or comparison if available. For
patents/inventions, describe what the system does and its key capability. If
there's a surprising corollary or implication, include it.

**Method** — The technique, approach, or experimental design in one sentence.
Name the specific mathematical tools, algorithms, or experimental protocols.
"Implicit Function Theorem applied to a parametrized family of matrices" is
better than "mathematical proof techniques."

## Style

- **Be precise.** Use the paper's own terminology. If the paper proves a
  theorem about "TU-subgraphs," say "TU-subgraphs," not "certain graph
  structures."
- **Be concise.** Each section is 1-2 sentences maximum. The entire takeaway
  should fit in a short paragraph.
- **Use math notation** where it helps clarity. Wrap LaTeX in `\(...\)` for
  inline math.
- **Write for the paper's audience.** A matrix theory paper gets matrix theory
  language. A neuroscience paper gets neuroscience language. But always aim for
  the clearest possible expression — a general scientist in an adjacent field
  should be able to follow the gist.
- **Don't rehash the abstract.** The abstract is available separately. Your
  takeaway should be a distillation that's faster to read and more structured.

## Presenting Results

Return results as a numbered list. For each paper:

```
1. **[Paper title]** (filename.pdf)

   <b>Problem:</b> ...<br><b>Key result:</b> ...<br><b>Method:</b> ...
```

If the user wants the output in a specific format (JSON, JavaScript object,
markdown table, etc.), adapt accordingly — the three-section structure stays
the same, only the container changes.

## Edge Cases

- **Patents**: Treat "Key result" as the main invention/capability. "Method"
  describes the technical approach of the system.
- **Survey papers**: "Key result" becomes the main insight or taxonomy. "Method"
  describes the survey methodology (systematic review, meta-analysis, etc.).
- **Work in progress / incomplete PDFs**: Summarize what's available. Flag if
  key sections are missing.
- **Non-English papers**: Do your best with available content. Note the
  language limitation.

## Batch Processing

When given multiple papers, process them independently. If the user asks for
parallelism (e.g., "do these in parallel"), use the Task tool to spawn
subagents — one per paper or per batch of 3-4 papers.
