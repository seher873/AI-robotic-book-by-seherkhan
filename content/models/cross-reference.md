# CrossReference Model Definition

## Overview

This document defines the structure and validation rules for cross-references between content in the AI textbook.

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier for the cross-reference |
| sourceType | string | Yes | Type of source entity (glossaryTerm, appendixSection, module) |
| sourceId | string | Yes | ID of the source entity |
| targetType | string | Yes | Type of target entity (glossaryTerm, appendixSection, module) |
| targetId | string | Yes | ID of the target entity |
| relationshipType | string | Yes | Type of relationship (related, seeAlso, prerequisite, etc.) |
| createdAt | datetime | No | Timestamp of creation |

## Relationships

- Links exactly two entities (source and target) of specified types

## Validation Rules

- Both sourceId and targetId must reference existing entities
- sourceType and targetType must be from a predefined list of valid types
- relationshipType must be from a predefined list of valid relationships

## Example

```json
{
  "id": "xr-001",
  "sourceType": "glossaryTerm",
  "sourceId": "artificial-intelligence",
  "targetType": "appendixSection",
  "targetId": "appendix-b-chatbot-rag",
  "relationshipType": "related",
  "createdAt": "2025-12-16T10:00:00Z"
}
```