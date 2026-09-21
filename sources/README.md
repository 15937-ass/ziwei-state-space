# Source Storage and Provenance

## Why source PDFs are not committed

The source books used by this project are copyrighted works. The repository therefore stores **metadata, provenance references, structured rule extractions, and research-derived representations**, but does not redistribute full copyrighted PDFs by default.

The current GitHub connector also writes UTF-8 text files; it is not being used as a binary-PDF upload channel.

## Where the source files live during extraction

Approved source files are supplied to the ChatGPT project/file context. During a work package, the research assistant reads the source on demand and extracts bounded, source-grounded rules.

The books are **not trained into model weights** and are not treated as an invisible persistent knowledge base. Each extraction task should be reproducible from:
1. source identity in `source_index.csv`,
2. source location/page/section in each rule,
3. the rule extraction schema,
4. the committed structured output.

## What GitHub stores

GitHub is the project source of truth for **research state**, including:

- source manifest and scope,
- atomic rules,
- source locations and provenance,
- candidate qi ontology,
- star/star-system models,
- mathematical formalization,
- audits and conflicts,
- code and tests,
- paper materials,
- decision history.

Example pipeline:

```text
Source PDF in approved project files
        |
        | read on demand
        v
GPT source-grounded extraction
        |
        | producer -> critic -> revision
        v
Structured rule artifact
        |
        v
GitHub (versioned source of truth)
```

## Reproducibility requirement

A committed rule is not considered approved merely because GPT generated it.

For approval it must retain sufficient provenance to locate the supporting passage in the approved source. Future releases should additionally maintain local file hashes or archival identifiers where legally and technically appropriate.

## Paper-1 policy

Paper 1 will cite the source works but will not bundle the full source books in the public research artifact unless distribution rights explicitly permit it.
