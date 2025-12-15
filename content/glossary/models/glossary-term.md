# GlossaryTerm Model Definition

## Overview

This document defines the structure and validation rules for glossary terms in the AI textbook.

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier for the term |
| term | string | Yes | The actual term being defined |
| definition | string | Yes | The definition of the term |
| category | string | No | Topic category (e.g., "algorithms", "ethics", "tools") |
| relatedTerms | array of strings | No | Array of related term IDs |
| examples | array of strings | No | Array of examples that illustrate the term |
| synonyms | array of strings | No | Array of alternative terms with similar meanings |
| seeAlso | array of strings | No | Array of references to related concepts in the textbook |
| createdAt | datetime | No | Timestamp of creation |
| updatedAt | datetime | No | Timestamp of last update |

## Relationships

- Zero or more cross-references to other GlossaryTerm entities
- Zero or more references to AppendixSection entities
- Zero or more references to textbook modules

## Validation Rules

- term field is required and must be unique across all terms
- definition field is required with minimum 10 characters
- if provided, category must be from a predefined list of valid categories
- examples should provide substantive educational content

## Example

```markdown
---
id: "artificial-intelligence"
term: "Artificial Intelligence (AI)"
category: "fundamentals"
relatedTerms: ["machine-learning", "neural-networks"]
seeAlso: ["module-1", "module-2"]
---

# Artificial Intelligence (AI)

**Definition**: The simulation of human intelligence processes by machines, especially computer systems. These processes include learning, reasoning, and self-correction.

**Examples**:
- Image recognition systems
- Natural language processing
- Expert systems

**Synonyms**: 
- Machine intelligence
- Computational intelligence
```