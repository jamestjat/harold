# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**harold** is an open-source control systems toolbox for Python 3.8+. It provides tools for analyzing and designing linear time-invariant (LTI) systems, a fundamental topic in control engineering. The library emphasizes user accessibility with full source code and permissive MIT licensing.

**Key capabilities:**
- Transfer function and state-space system representations
- System analysis (poles, zeros, frequency response, stability)
- Control design (state feedback, observer design, Kalman filtering)
- Discretization and time-domain/frequency-domain simulations
- MIMO (multiple-input multiple-output) system support

## Architecture & Design

Harold uses a modular architecture where each module (`_*.py` file) handles a specific domain. Two core classes represent LTI systems:

1. **Transfer** (`_classes.py`): Transfer function representation - numerator/denominator polynomials
2. **State** (`_classes.py`): State-space representation - A, B, C, D matrices

The main __init__.py imports and re-exports all functionality from private modules, creating a clean public API.

**Key design patterns:**
- **Composition of operations**: Functions operate on Transfer/State objects and return modified copies (immutable-like pattern)
- **SISO/MIMO flexibility**: Both classes support single-input-single-output and multi-input-multi-output systems with dynamic shape validation
- **Continuous/Discrete duality**: Both system types support continuous and discrete-time variants via `SamplingPeriod` property

**Module organization:**
- `_classes.py`: Core Transfer and State classes (3524 lines - largest module)
- `_polynomial_ops.py`: Polynomial arithmetic (numerator/denominator manipulation)
- `_aux_linalg.py`: Linear algebra utilities (SVD, norms, specialized decompositions)
- `_solvers.py`: Equation solvers (Lyapunov, Riccati, etc.)
- `_system_funcs.py`: System conversion and analysis functions
- `_frequency_domain.py`: Frequency-domain analysis tools
- `_time_domain.py`: Time-domain simulation and response computation
- `_kalman_ops.py`, `_static_ctrl_design.py`: Control-specific operations
- `_discrete_funcs.py`: Discretization methods and conversions
- Plotting modules: `_frequency_domain_plots.py`, `_time_domain_plots.py` (matplotlib integration)

## Development Setup

### Environment Management
- Uses **uv** for dependency management (specified in user instructions)
- Python 3.8+ required (3.12 preferred)
- Install environment: `uv sync`

### Dependencies
**Runtime:**
- `scipy>=1.8.0`: Linear algebra, signal processing, optimization
- `matplotlib`: All visualization features
- `tabulate`: Pretty-printing system information

**Development:**
- `pytest>=6.0.0`: Test framework
- `flake8>=4.0.1`: Code linting

## Building, Linting, and Testing

### Run Tests
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest harold/tests/test_classes.py -v

# Run single test function
uv run pytest harold/tests/test_classes.py::test_Transfer_Instantiations -v

# Run tests matching pattern
uv run pytest -k "Transfer" -v
```

### Linting
```bash
# Lint code
ruff check

# View lint issues with context
ruff check --show-source
```

### Type Checking
The current codebase does not have systematic type annotations. When adding new code, consider adding type hints for clarity.

## Testing Strategy

**Test organization:** One test file per main module, organized in `harold/tests/` matching module names (e.g., `test_classes.py` for `_classes.py`)

**Testing framework:** pytest with numpy testing utilities (`numpy.testing.assert_*` functions) for numerical assertions

**Test patterns observed:**
- Comprehensive instantiation tests for Transfer/State classes
- Numerical equivalence testing (using `assert_allclose` for floating point)
- Edge case testing (SISO/MIMO, continuous/discrete, gain systems)
- Integration testing for conversions and operations

**Important:** Tests are persistent (committed to repo), not ephemeral scripts. When modifying core functionality, ensure corresponding tests pass.

## Code Quality Standards

### Before Committing
1. Run full test suite: `uv run pytest`
2. Run linter: `ruff check`
3. Verify no new warnings introduced
4. For new code, consider adding type hints

### Git Workflow
- Create feature branches for significant changes
- Make frequent commits for logical subtasks
- Write clear commit messages following project style
- Only commit code with passing tests and clean linting

## Notable Implementation Details

### Transfer Function Representation
SISO: numerator and denominator are 1D arrays (polynomial coefficients)
MIMO: nested list structure - `Transfer([[num00, num01], [num10, num11]], ...)` where each element is a 1D array

### State-Space Matrices
- A, B, C, D matrices with appropriate dimensions for SISO/MIMO systems
- Properties recalculate on state changes via `_recalc()` method

### Discretization
- Multiple discretization methods supported (see `_KnownDiscretizationMethods` in `_global_constants.py`)
- Prewarp frequency available for bilinear transformation
- Continuous/discrete conversion through `SamplingPeriod` property

### System Stability
- Poles computed from A matrix eigenvalues (state-space) or denominator roots (transfer function)
- Stability flags cached and recalculated when system changes
- Both continuous (real parts < 0) and discrete (magnitude < 1) stability definitions

## File Structure

```
harold/
├── __init__.py                 # Main API exports
├── _classes.py                 # Transfer & State classes
├── _polynomial_ops.py          # Polynomial operations
├── _aux_linalg.py              # Linear algebra utilities
├── _solvers.py                 # Equation solvers (Lyapunov, Riccati)
├── _system_funcs.py            # System-level operations
├── _frequency_domain.py        # Frequency response tools
├── _time_domain.py             # Time simulation
├── _kalman_ops.py              # Kalman filtering
├── _static_ctrl_design.py      # Control design (pole placement, etc.)
├── _discrete_funcs.py          # Discretization
├── _frequency_domain_plots.py  # Bode, Nyquist plots
├── _time_domain_plots.py       # Step, impulse response plots
├── _array_validators.py        # Input validation
├── _arg_utils.py               # Argument processing utilities
├── _global_constants.py        # Global enumerations
├── _bd_algebra.py              # Block diagram algebra
├── _version.py                 # Version info
└── tests/                      # Test suite
    └── test_*.py               # One test per module
```

## Important Conventions

1. **Naming**: Private modules prefixed with underscore, public API exported in `__init__.py`
2. **Validation**: Input validation happens early with descriptive errors
3. **Immutability-like pattern**: Most functions return new Transfer/State objects rather than modifying in-place
4. **Documentation**: Extensive docstrings with examples in functions and classes
5. **Backwards compatibility**: Changes must maintain API compatibility for existing users
