# NavigationLink Model Definition

## Overview

This document defines the structure and validation rules for navigation links in the AI textbook.

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier for the navigation link |
| label | string | Yes | Text to display for the link |
| url | string | Yes | URL path to the target location |
| sourceSection | string | Yes | Section where the link is placed (mainContent, glossary, appendices) |
| targetSection | string | Yes | Section the link navigates to (mainContent, glossary, appendices) |
| displayPriority | number | No | Priority for display order (lower numbers first) |
| createdAt | datetime | No | Timestamp of creation |

## Validation Rules

- url must be a valid relative path within the documentation site
- sourceSection and targetSection must be from a predefined list of valid sections
- displayPriority must be a positive integer if provided

## Example

```json
{
  "id": "nav-001",
  "label": "View Glossary",
  "url": "/docs/glossary",
  "sourceSection": "mainContent",
  "targetSection": "glossary",
  "displayPriority": 1,
  "createdAt": "2025-12-16T10:00:00Z"
}
```