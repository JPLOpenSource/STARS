# StarsProj - STARS F´ Test Project

This F´ project is used by STARS developers to test state machine autocoder output and demonstrate integration with F´ components.

## Purpose

- **For STARS Developers**: Test the fprime backend autocoder by running generated state machines in actual F´ components
- **For STARS Users**: Example of how to integrate STARS-generated state machines into F´ components

## Setup

The fprime library is not tracked in the STARS repository. To set up this project:

1. **Clone fprime as a submodule** (first time only):
   ```bash
   cd StarsProj
   git submodule update --init --recursive
   ```

2. **Create Python virtual environment**:
   ```bash
   python3 -m venv fprime-venv
   source fprime-venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Build the component**:
   ```bash
   cd Simple_Component
   fprime-util build
   ```

4. **Run unit tests**:
   ```bash
   fprime-util check
   ```

## Components

- **Simple_Component**: Example F´ component with a STARS-generated state machine

## More Information

F´ (F Prime) is a component-driven framework that enables rapid development and deployment of spaceflight and other embedded software applications.
**Visit the F´ Website:** https://fprime.jpl.nasa.gov
