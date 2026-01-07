# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python package for accurate epidemiological weeks calculation using the US CDC (MMWR) and ISO week numbering systems.

### Core Structure
- **`src/epiweeks/`** - Main package code
  - `__init__.py` - Contains `Week` and `Year` classes with week calculation logic

### Key Classes
- **`Week`** - Represents a week in CDC (MMWR) or ISO week numbering system
- **`Year`** - Represents a year for epidemiological week calculations
- Both classes provide methods for week iteration, date ranges, and arithmetic operations

### Limitations
- **Week Systems**: Only supports CDC (MMWR) and ISO week systems
- **Date Range**: Limited by Python's `datetime.date` range

## Development

The project uses `uv` as the package manager. Run `uv sync` to set up the environment.

### Commands
```bash
uv run ruff format       # Format code
uv run ruff check --fix  # Lint code
uv run mypy              # Type check
uv run pytest --cov      # Test with coverage
```

### Testing Structure
- `tests/unit/` - Unit tests for individual modules
- `tests/integration/` - Integration tests against reference data
- Fixtures in `tests/integration/fixtures/` contain verified CDC reference calendars

## Code Quality Standards

- **100% test coverage** is required - coverage will fail if below 100%
- **Type hints** are mandatory for all functions and methods
- **Ruff** is used for both formatting and linting
- **MyPy** runs in strict mode
- **Google docstring style** for all public APIs

## Critical Constraints

- **Zero runtime dependencies** - do not add any
- **Calculation accuracy is critical** - validate against CDC reference data in integration tests
- **Performance matters** - this is an optimized library
