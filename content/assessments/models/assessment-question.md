# AssessmentQuestion Model Definition

## Overview

This document defines the structure and validation rules for assessment questions in the AI textbook.

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier for the question |
| moduleId | string | Yes | Reference to the module/chapter this question relates to |
| questionText | string | Yes | The actual question text (max 5000 characters) |
| questionType | string | No | Type of question, defaults to "multiple-choice" |
| options | array of strings | Yes | Array of possible answer options (2-10 items) |
| correctAnswer | integer | Yes | Index of the correct answer option |
| explanation | string | Yes | Detailed explanation of the correct answer |
| incorrectExplanations | array of strings | No | Array of explanations for incorrect options |
| difficultyLevel | string | No | Level of difficulty (beginner, intermediate, advanced) |
| tags | array of strings | No | Array of tags for categorizing the question |
| createdAt | datetime | No | Timestamp of creation |
| updatedAt | datetime | No | Timestamp of last update |

## Relationships

- Belongs to one Module/Chapter
- Related to zero or more similar questions via tags

## Validation Rules

- questionText is required and must not exceed 5000 characters
- options array must have at least 2 items and no more than 10
- correctAnswer must be a valid index in options array
- explanation is required and must provide substantive content
- tags must consist of valid, pre-approved terms

## Example

```yaml
id: "q123"
moduleId: "module-1"
questionText: "What is artificial intelligence?"
questionType: "multiple-choice"
options:
  - "Creating machines that can think and learn like humans"
  - "Programming computers to follow explicit instructions"
  - "Building faster processors"
  - "Optimizing existing algorithms"
correctAnswer: 0
explanation: "Artificial intelligence is about creating machines that can think and learn like humans, typically through algorithms that can recognize patterns, make decisions, and improve from experience."
incorrectExplanations:
  - "This is a valid approach but not the definition of AI."
  - "This describes traditional programming, not AI."
  - "This is about hardware optimization, not AI."
difficultyLevel: "beginner"
tags:
  - "ai-basics"
  - "machine-learning"
createdAt: "2025-12-15T10:00:00Z"
updatedAt: "2025-12-15T10:00:00Z"
```