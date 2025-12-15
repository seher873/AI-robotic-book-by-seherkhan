# AppendixSection Model Definition

## Overview

This document defines the structure and validation rules for appendix sections in the AI textbook.

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier for the appendix section |
| title | string | Yes | Title of the appendix section |
| content | string | Yes | Main content of the appendix (Markdown format) |
| category | string | No | Topic category (e.g., "tools", "mathematical-foundations", "datasets", "chatbot-rag") |
| skillLevel | string | No | Target skill level (beginner, intermediate, advanced) |
| relatedModules | array of strings | No | Array of module IDs this appendix connects to |
| tags | array of strings | No | Array of tags for easy search |
| references | array of strings | No | Array of references cited in the appendix |
| createdAt | datetime | No | Timestamp of creation |
| updatedAt | datetime | No | Timestamp of last update |

## Relationships

- Zero or more cross-references to GlossaryTerm entities
- Zero or more references to textbook modules
- Zero or more references to other AppendixSection entities

## Validation Rules

- title is required and must be unique within the same category
- content must follow Markdown format specifications
- if provided, skillLevel must be one of "beginner", "intermediate", or "advanced"
- references should follow standard academic citation format if possible

## Example

```markdown
---
id: "appendix-b-chatbot-rag"
title: "Appendix B: Chatbot and RAG Technologies"
category: "chatbot-rag"
skillLevel: "advanced"
relatedModules: ["module-4", "module-5"]
tags: ["chatbot", "rag", "retrieval-augmented-generation", "nlp"]
references: ["Lewis et al. 2020", "Brown et al. 2020"]
---

# Appendix B: Chatbot and RAG Technologies

## Overview

This appendix provides detailed information about modern chatbot technologies and Retrieval-Augmented Generation (RAG) systems...

[Detailed content continues in Markdown format]
```