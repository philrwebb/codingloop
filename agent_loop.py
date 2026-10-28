# agent_loop.py
import subprocess
from typing import cast
from mlx.nn import Module
from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler
from mlx_lm.tokenizer_utils import TokenizerWrapper

# Using a reliable 4-bit quantized model from the mlx-community
# (Adjust to your preferred local model tag if needed, e.g., gemma-2-9b-it-4bit)
MODEL_PATH = "mlx-community/gemma-2-9b-it-4bit"
TARGET_FILE = "solution.py"
TEST_FILE = "test_solution.py"
MAX_ITERATIONS = 5

print(f"[*] Loading model {MODEL_PATH} into Apple Silicon unified memory...")
model, tokenizer = cast(
    tuple[Module, TokenizerWrapper], load(MODEL_PATH, return_config=False)
)

def run_tests():
    """Runs pytest via subprocess and returns (success: bool, output: str)."""
    result = subprocess.run(
        ["pytest", TEST_FILE, "-v"],
        capture_output=True,
        text=True
    )
    success = (result.returncode == 0)
    output = result.stdout + "\n" + result.stderr
    return success, output

def get_file_content(filepath):
    with open(filepath, "r") as f:
        return f.read()

def save_file_content(filepath, content):
    with open(filepath, "w") as f:
        f.write(content)

def ask_llm_for_fix(code, error_output):
    """Sends current code and pytest traceback to MLX for local native inference."""
    prompt = f"""You are an expert Python software engineer fixing a failing test suite. 
    Here is the current implementation of {TARGET_FILE}:
    ```python
    {code}
    ```
    """
    messages = [{"role": "user", "content": prompt}]
    formatted_prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    response = generate(
    model,
    tokenizer,
    prompt=formatted_prompt,
    verbose=False,
    max_tokens=2048,
    sampler=make_sampler(temp=0.1),
    )
    # Extract code block if wrapped in markdown backticks
    if "```python" in response:
        return response.split("```python", 1)[1].split("```", 1)[0].strip()
    elif "```" in response:
        return response.split("```", 1)[1].split("```", 1)[0].strip()
    return response.strip()


def main():
    print(f"[*] Starting MLX agent coding loop...")
    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- Iteration {iteration} of {MAX_ITERATIONS} ---")
        # 1. Run tests
        success, output = run_tests()
        if success:
            print("[+] All tests passed successfully!")
            print(output)
            return
        print("[-] Tests failed. Sending failure details to local MLX model...")
        current_code = get_file_content(TARGET_FILE)
        fixed_code = ask_llm_for_fix(current_code, output)
        # 4. Overwrite file and loop back to test
        save_file_content(TARGET_FILE, fixed_code)
        print(f"[*] Updated {TARGET_FILE}. Re-running tests...")
    print(
        "\n[!] Max iterations reached without passing tests. Manual intervention required."
    )

if __name__ == '__main__':
    main()
