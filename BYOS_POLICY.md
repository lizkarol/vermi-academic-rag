# BYOS Policy: Legal Framework for vermi-academic-rag

## Principle

This repository adheres to **Bring Your Own Sources** (BYOS) model:
- We publish code and synthesized knowledge (chunks, embeddings)
- We do NOT distribute copyrighted source materials (PDFs, direct conversions)
- We ALWAYS cite originals via DOI or persistent URL

## Why?

1. **Copyright Compliance:** Fair use allows summarization and commentary, not redistribution
2. **Transparency:** Source code + methodology visible → reproducible
3. **Flexibility:** Users can apply the same process to their own sources
4. **Sustainability:** Repository remains lean and DMCA-proof

## Guidelines

### Source Management

**Private (Your machine / Cloud storage):**
- Keep original PDFs and direct conversions private
- Use for local processing only
- Back up to secure cloud (Google Drive, etc.)

**Public (This GitHub repo):**
- Chunk JSON with paraphrased content
- Computing scripts and examples
- DOI/URL references (not PDFs)
- Quality reports and metadata

### Paraphrasing Standard

When converting a source to chunks:

```
❌ BAD:
"Lorem ipsum dolor sit amet..." (direct copy)
source_field: "The vermicomposting process involves the action of earthworms..."

✅ GOOD:
source_field: "Vermicomposting relies on earthworm activity to..."
(your own words, capturing the same idea)
```

### Attribution

Every chunk MUST include:
- `source_document`: DOI or canonical URL (NOT local file path)
- `citations`: Array of references
- `reliability_level`: Indication of source quality

Example:
```json
{
  "source_document": "https://doi.org/10.1016/j.wasman.2024.01.001",
  "citations": ["doi:10.1016/j.wasman.2024.01.001"],
  "reliability_level": "high"
}
```

### Open Licenses (CC-BY, CC0, Public Domain)

If a source has **CC-BY** or more permissive license, we MAY redistribute with proper attribution:

```json
{
  "source_document": "https://openknowledge.fao.org/handle/20.500.14283/cb7836en",
  "license_note": "CC-BY 4.0 (FAO, 2024)",
  "citations": ["https://openknowledge.fao.org/..."]
}
```

In this case, direct quotes and adaptations are legal if attributed.

## Contributor Checklist

Before submitting a PR with new chunks:

- [ ] Chunks are paraphrased (not verbatim copies)
- [ ] `source_document` is a DOI or URL (not a file path)
- [ ] `citations` include full references
- [ ] `reliability_level` reflects source credibility
- [ ] If source is CC-BY, `license_note` is included
- [ ] No PDF or direct Markdown conversion attached to PR
- [ ] Validate with `python scripts/validate_chunks.py --strict`

## Enforcement

This repository uses automated and manual checks:

- **Pre-commit hooks** (local): Prevent accidental PDFs commits
- **GitHub Actions** (CI): Validate chunk schema and citation completeness
- **Manual review**: Maintainers check for verbatim excerpts or licensing issues

Violations will result in PR rejection with guidance to comply.

---
