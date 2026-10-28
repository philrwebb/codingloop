# Coding Loop

A local Python coding-agent experiment using MLX on Apple Silicon. The agent runs
pytest against a word-counting function and asks a local language model to rewrite
the implementation when tests fail.

## Requirements

- An Apple Silicon Mac with enough available memory for the model.
- Python 3.14 or newer and uv.
- Internet access for the initial dependency and model downloads.

## Setup and usage

Run these commands from the project directory:

```bash
uv sync --locked
uv run pytest test_solution.py -v
uv run agent_loop.py
```

The agent uses `mlx-community/gemma-2-9b-it-4bit`. Its first run downloads the
model to the Hugging Face cache (normally `~/.cache/huggingface/hub`); later runs
reuse those files. Set `HF_HUB_CACHE` to choose another cache directory.

The agent loads the model, then runs the tests. If they pass, it exits. Otherwise,
it generates replacement code, overwrites `solution.py`, and repeats, with a limit
of five iterations. Review generated changes before keeping them. After the last
rewrite, run pytest manually to verify the final result.

## Files

- `agent_loop.py`: entry point for the local test-and-rewrite loop. Configure the
  model, target file, test file, and iteration limit using its constants.
- `solution.py`: word-counting implementation that the agent can overwrite.
- `test_solution.py`: tests for empty input, case normalization, punctuation,
  and word frequencies.
- `main.py`: earlier experimental version; use `agent_loop.py` to run the agent.
- `pyproject.toml` and `uv.lock`: dependencies and locked dependency versions.

## Current limitations

The repair prompt currently includes the implementation but does not include the
captured pytest output, even though it is passed into the repair function. The
loop executes generated Python through pytest, so use it in a trusted local
development environment.
