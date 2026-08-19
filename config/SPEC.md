# Configuration Modules Specification

**Version**: v1.0.0 | **Status**: Active | **Last Updated**: July 2026

**Layer**: Config | **Role**: Parameter definitions

## Purpose
The `config/` directory holds declarative **YAML** files that govern runtime behavior of the `fep_lean` orchestrator: OpenGauss session defaults, Hermes-related settings, and the 50-topic catalogue.

## Components
1. `settings.yaml`: Controls operational variables (GAUSS_HOME, model IDs, force reload flags).
2. `topics.yaml`: The definitive catalogue of 50 canonical FEP/AI/BM theorem topics to be formalized.

## Operating Contracts
- All YAML files must successfully validate at load-time (schema checks).
- No executable code (`.py`) is permitted in this directory.
- Modifications to `topics.yaml` must preserve the 50-topic sequence for regression tracking.
