import subprocess
from typing import cast

from mlx.nn import Module
from mlx_lm import load, generate
from mlx_lm.tokenizer_utils import TokenizerWrapper

# Using a community 4-bit quantized Gemma model from Hugging Face
MODEL_PATH = "mlx-community/gemma-2-9b-it-4bit" # Or your preferred 14B/9B Gemma variant
TARGET_FILE = "solution.py"
TEST_FILE = "test_solution.py"
MAX_ITERATIONS = 5

# Load model and tokenizer globally so they stay cached in unified memory
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
    """Sends current code and traceback to MLX for a local native inference pass."""
    prompt = f"""You are an expert software engineer fixing a bug. 
Here is the current implementation of {TARGET_FILE}:
```python
{code}
```
"""
# Format prompt using the model's native chat template if available
messages = [{"role": "user", "content": prompt}]
formatted_prompt = tokenizer.apply_chat_template(
messages, tokenize=False, add_generation_prompt=True
)
# Generate response locally using MLX
response = generate(model, tokenizer, prompt=formatted_prompt, verbose=False, max_tokens=2048)
# Extract code block if wrapped in markdown backticks
if "python" in response: parts = response.split("python")
code_part = parts[1].split("")[0] return code_part.strip() elif "" in response:
parts = response.split("```")
return parts[1].strip()
return response.strip()
def main():
print(f"[*] Starting MLX agent loop...")
for iteration in range(1, MAX_ITERATIONS + 1):
print(f"\n--- Iteration {iteration} of {MAX_ITERATIONS} ---")
success, output = run_tests()
if success:
print("[+] All tests passed successfully!")
print(output)
return
print("[-] Tests failed. Feeding traceback to local MLX model...")
current_code = get_file_content(TARGET_FILE)
fixed_code = ask_llm_for_fix(current_code, output)
save_file_content(TARGET_FILE, fixed_code)
print(f"[*] Updated {TARGET_FILE}. Re-running tests...")
print("\n[!] Max iterations reached without passing tests.")
if name == "main":
main()
