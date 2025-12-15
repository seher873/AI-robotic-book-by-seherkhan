# Cross-Reference System

This file outlines the system for managing cross-references between different content components in the AI textbook.

## Overview

The cross-referencing system allows for linking between:
- Glossary terms and textbook modules
- Glossary terms and appendix sections
- Appendix sections and textbook modules
- Glossary terms to other related glossary terms

## Implementation Approach

Cross-references are implemented by:

1. Using Docusaurus's internal linking feature in Markdown files
2. Maintaining explicit references in the frontmatter of each document
3. Using a consistent naming convention for IDs to ensure reliable linking

## Examples of Cross-Reference Usage

In a glossary term markdown file:
```markdown
---
id: "example-term"
term: "Example Term"
relatedTerms: ["other-term", "another-concept"]
seeAlso: ["module-2", "appendix-b-chatbot-rag"]
---

# Example Term

Content here...

See also [other term](./glossary/other-term) or [appendix section](./appendices/appendix-b-chatbot-rag).
```

## Naming Conventions

- Glossary terms: `/docs/glossary/[term-name].md`
- Appendix sections: `/docs/appendices/[section-name].md`
- Module sections: `/docs/modules/[module-name].md`

## Validation

The system is validated by:
- Checking that all referenced IDs exist in their respective content types
- Verifying links work properly in the deployed documentation
- Running Docusaurus's built-in broken link detection