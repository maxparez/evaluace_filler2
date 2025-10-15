# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an automation project for filling out LimeSurvey questionnaires for the "Šablony pro MŠ a ZŠ I" initiative. The system automatically completes evidence forms at `https://evaluace.opjak.cz/index.php/262621` based on JSON configuration files.

## Project Purpose

The agent automates completion of educational institution evaluation forms using Chrome DevTools MCP server. The forms collect data about:
- DVPP (professional development) topics for teachers
- SDP/ŽZOR (innovative education) activities across different literacy areas
- Student/child counts across school years (2022-2026)
- Data for three school types: MŠ (kindergarten), ZŠ (elementary), ŠD (after-school club)

## Key Files

- `rules.md` - Complete automation specification and business logic (in Czech)
- `test_data/Otice_ZS_MS_733_consolidated.json` - Example configuration file structure

## Configuration File Structure

Input JSON contains:
- `school_name`: School identifier
- `code`: Login code for the survey
- `MS`, `ZS`, `SD`: Base student counts for each school type
- `dvpp_topics`: Professional development topics by activity code
- `sdp_zzor`: Innovative education activities with literacy areas and yearly counts

## Critical Business Rules

### Default Calculation Logic
When specific counts aren't provided in JSON:
```
count = round(0.35 * base_count)
```
Where base_count is MS/ZS/SD depending on school type.

### School Year Format
- JSON format: `"2022-2023"` (dash)
- UI format: `"2022/2023"` (slash)
- Map years 1:1 between formats

### Navigation
- Always click "Další" (Next) button after completing each page
- Survey title: `<h1 class="survey-name text-center">Evidence podpořenosti...</h1>`
- Section headers: `<div class="group-title text-center h3 space-col">[MŠ|ZŠ|ŠD]</div>`

### Fixed Responses (Hard-coded Rules)
1. **OMJ nationality page**: Skip without filling - just click "Další"
2. **Leading educators**: Always fill 0 for all fields
3. **Ukrainian educators**: Always fill 0 for all school years

### Validation
Form completion is successful when page shows:
```
Děkujeme Vám!
Vaše odpovědi byly uloženy.
```

## Workflow Steps

1. Load JSON configuration
2. Navigate to survey URL
3. Login with `code` from JSON
4. For each school type (MŠ/ZŠ/ŠD) present in JSON:
   - Fill DVPP topics (exact label matching)
   - Fill SDP/ŽZOR activities (yearly counts per literacy area)
   - Fill general yearly counts (calculated with 0.35 multiplier if not explicit)
5. Handle special pages with fixed rules
6. Verify completion message

## Chrome DevTools MCP Usage

This project requires the Chrome DevTools MCP server:
- Takes snapshots of form pages to identify elements
- Fills form fields based on element UIDs from snapshots
- Clicks navigation buttons
- Verifies page transitions

## Language Conventions

- **Code/automation logic**: English
- **Survey content/UI**: Czech
- **Configuration values**: Czech (school names, topics)

## Development Notes

- Use case-insensitive and diacritics-insensitive matching for Czech labels
- Handle missing optional fields gracefully (skip if not in JSON)
- Verify page transitions after each "Další" click to catch validation errors
- If validation fails, check for missing required fields per rules.md
