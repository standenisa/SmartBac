"""
Inferență Qwen2.5-VL-3B + LoRA — acceptă o imagine, returnează soluția.

Usage:
    # CLI test
    python ai/finetune/inference_vlm.py --image path/to/photo.jpg

    # Ca modul importat
    from ai.finetune.inference_vlm import load_vlm, solve_from_image
    load_vlm()
    result = solve_from_image("photo.jpg")
    print(result["answer"])
"""

import os
import re
import argparse
from typing import Optional

import torch
from PIL import Image

_model = None
_processor = None
_loaded = False

MODEL_ID = "Qwen/Qwen2.5-VL-3B-Instruct"
ADAPTER_PATH = os.environ.get(
    "VLM_ADAPTER_PATH",
    os.path.join(os.path.dirname(__file__), "adapters", "vlm-lora"),
)

# Must stay in sync with the system prompt in ai/finetune/train_vlm.py
# (duplicated there so the training script can run standalone on Kaggle).
SYSTEM_PROMPT = (
    "Ești SmartBAC, un tutore expert de matematică pentru Bacalaureatul din România. "
    "Citești exercițiul din imagine și îl rezolvi pas cu pas. "
    "Răspunde DOAR în limba română. "
    "Format: Pasul 1: ... Pasul 2: ... Răspuns: ..."
)


def load_vlm(
    model_id: str = MODEL_ID,
    adapter_path: Optional[str] = None,
    device: str = "auto",
) -> bool:
    """Load VLM model + LoRA adapter. Returns True on success."""
    global _model, _processor, _loaded

    if _loaded:
        return True

    adapter = adapter_path or ADAPTER_PATH
    use_adapter = os.path.isdir(adapter)

    print(f"[VLM] Loading {model_id}...")

    try:
        from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, BitsAndBytesConfig

        has_cuda = torch.cuda.is_available()

        if has_cuda:
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
            _model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                model_id,
                quantization_config=quant_config,
                device_map=device,
                torch_dtype=torch.bfloat16,
            )
        else:
            _model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                model_id,
                device_map=device,
                torch_dtype=torch.float32,
            )

        _processor = AutoProcessor.from_pretrained(model_id)

        if use_adapter:
            from peft import PeftModel
            print(f"[VLM] Loading LoRA adapter from {adapter}")
            _model = PeftModel.from_pretrained(_model, adapter)

        _model.eval()
        _loaded = True
        print(f"[VLM] Ready (adapter={'yes' if use_adapter else 'no'})")
        return True

    except Exception as e:
        print(f"[VLM] Load failed: {e}")
        return False


def solve_from_image(
    image_path: str,
    prompt: str = "Rezolvă exercițiul din imagine.",
    max_new_tokens: int = 512,
    temperature: float = 0.3,
) -> dict:
    """
    Send image to VLM, get structured solution back.

    Returns: {
        "answer": str,
        "steps": [str],
        "full_response": str,
        "model_used": str,
    }
    """
    if not _loaded:
        if not load_vlm():
            return {
                "answer": "",
                "steps": [],
                "full_response": "Model not available",
                "model_used": "vlm_error",
            }

    # Load and preprocess image
    img = Image.open(image_path).convert("RGB")

    # Build messages in Qwen2.5-VL format
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": [
                {"type": "image", "image": img},
                {"type": "text", "text": prompt},
            ],
        },
    ]

    # Apply chat template
    text_prompt = _processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    inputs = _processor(
        text=[text_prompt],
        images=[img],
        return_tensors="pt",
        padding=True,
    )

    # Move to model device
    device = next(_model.parameters()).device
    inputs = {k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}

    # Generate
    with torch.no_grad():
        output_ids = _model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=temperature > 0,
            top_p=0.9,
        )

    # Decode only new tokens
    input_len = inputs["input_ids"].shape[1]
    generated_ids = output_ids[0][input_len:]
    response = _processor.tokenizer.decode(generated_ids, skip_special_tokens=True).strip()

    # Parse response into steps + answer
    steps = []
    answer = response
    for line in response.split("\n"):
        line = line.strip()
        if re.match(r"^Pasul\s+\d+", line, re.IGNORECASE):
            steps.append(line)
        elif re.match(r"^Răspuns|^Raspuns", line, re.IGNORECASE):
            answer = re.sub(r"^(Răspuns|Raspuns)\s*:\s*", "", line).strip()

    if not answer or answer == response:
        # Try to extract last meaningful line as answer
        lines = [l.strip() for l in response.strip().split("\n") if l.strip()]
        if lines:
            answer = lines[-1]

    return {
        "answer": answer,
        "steps": steps,
        "full_response": response,
        "model_used": "qwen_vlm_lora",
    }


def solve_from_bytes(
    image_bytes: bytes,
    prompt: str = "Rezolvă exercițiul din imagine.",
    **kwargs,
) -> dict:
    """Solve from raw image bytes (for API integration)."""
    import io
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    # Save to temp file
    tmp_path = "/tmp/vlm_input.jpg"
    img.save(tmp_path, "JPEG")
    return solve_from_image(tmp_path, prompt, **kwargs)


# ─── CLI ───

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test VLM inference on an image")
    parser.add_argument("--image", required=True, help="Path to image file")
    parser.add_argument("--prompt", default="Rezolvă exercițiul din imagine.")
    parser.add_argument("--adapter", default=None)
    parser.add_argument("--model", default=MODEL_ID)
    args = parser.parse_args()

    load_vlm(model_id=args.model, adapter_path=args.adapter)
    result = solve_from_image(args.image, args.prompt)

    print(f"\n{'='*50}")
    print(f"Model: {result['model_used']}")
    print(f"Answer: {result['answer']}")
    print(f"Steps: {len(result['steps'])}")
    print(f"{'='*50}")
    print(result["full_response"])
