import subprocess
import shutil
import re

# Preload model list at module load
available_models = ["llama3.3"]  # fallback default
if shutil.which("ollama") is not None:
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().splitlines()[1:]
        parsed = [line.split()[0].strip() for line in lines if line.strip()]
        if parsed:
            available_models = sorted(set(parsed))
        print(f"[PromptEmbellisherOllama] Available Ollama models: {available_models}")
    except Exception as e:
        print(f"[PromptEmbellisherOllama] Error getting Ollama models: {e}")

class PromptEmbellisherOllama:
    @classmethod
    def INPUT_TYPES(cls):
        # Two text inputs: base_prompt (not sent) and embellish_prompt (sent)
        required = {
            "base_prompt": ("STRING", {"multiline": True}),
            "embellish_prompt": ("STRING", {"multiline": True}),
            # Tone selection via arrow control
            "tone": ([
                "surreal", "western", "fantasy", "sci-fi",
                "mystery", "horror", "romance", "dramatic",
                "comic", "epic"
            ],),
            "intensity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0}),
            "max_lines": ("INT", {"default": 4, "min": 1, "max": 10}),
        }
        # Model toggles as INT sliders under optional
        optional = {}
        for model in available_models:
            key = re.sub(r"[^0-9a-zA-Z_]+", "_", model)
            optional[key] = ("INT", {"default": 0, "min": 0, "max": 1, "step": 1})
        return {"required": required, "optional": optional}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("result_prompt",)
    FUNCTION = "embellish"
    CATEGORY = "Prompt"

    def embellish(self, base_prompt, embellish_prompt, tone, intensity, max_lines, **kwargs):
        import ollama
        # Determine selected models
        selected = [m for m in available_models
                    if kwargs.get(re.sub(r"[^0-9a-zA-Z_]+", "_", m), 0) == 1]
        if not selected:
            selected = [available_models[0]]
        model_to_use = selected[0]
        print(f"[PromptEmbellisherOllama] Using model: {model_to_use}")

        instructions = (
            f"Rewrite this prompt in a more {tone} and imaginative style. "
            f"Use vivid, creative language. Amplify descriptive richness proportional to an intensity of {intensity}. "
            f"Limit the response to at most {max_lines} lines."
        )
        try:
            response = ollama.chat(
                model=model_to_use,
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": embellish_prompt},
                ]
            )
            embellished = response['message']['content']
        except Exception as e:
            embellished = f"[Error embellishing prompt: {e}]"

        # Trim to max_lines and combine
        lines = embellished.splitlines()
        trimmed_lines = lines[:max_lines]
        embellishment_text = " ".join(trimmed_lines)

        # Apply default weight of 1.5
        weighted_embellishment = f"({embellishment_text}:1.5)"

        # Append weighted embellishment to base_prompt
        result = f"{base_prompt} {weighted_embellishment}".strip()
        return (result,)

# Node registration
NODE_CLASS_MAPPINGS = {"PromptEmbellisherOllama": PromptEmbellisherOllama}
NODE_DISPLAY_NAME_MAPPINGS = {"PromptEmbellisherOllama": "Prompt Embellisher (Ollama)"}

