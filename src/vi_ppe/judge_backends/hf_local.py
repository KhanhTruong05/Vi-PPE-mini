from __future__ import annotations


class HfLocalBackend:
    def __init__(self, model_cfg: dict):
        self.model_cfg = model_cfg
        self.judge_model = model_cfg["model_id"]
        self._tokenizer = None
        self._model = None

    def _load(self):
        if self._model is not None:
            return
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        quant_config = None
        if self.model_cfg.get("quantization") == "4bit_nf4":
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
        trust_remote_code = bool(self.model_cfg.get("trust_remote_code", False))
        self._tokenizer = AutoTokenizer.from_pretrained(
            self.model_cfg["model_id"],
            trust_remote_code=trust_remote_code,
        )
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_cfg["model_id"],
            device_map="auto",
            quantization_config=quant_config,
            torch_dtype=torch.bfloat16,
            trust_remote_code=trust_remote_code,
        )

    def generate(self, prompt: str, pair: dict, order: str) -> str:
        self._load()
        messages = [{"role": "user", "content": prompt}]
        rendered_prompt = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        encoded = self._tokenizer(rendered_prompt, return_tensors="pt").to(self._model.device)
        output_ids = self._model.generate(
            **encoded,
            max_new_tokens=int(self.model_cfg.get("max_new_tokens", 256)),
            do_sample=False,
        )
        prompt_length = encoded["input_ids"].shape[-1]
        return self._tokenizer.decode(output_ids[0][prompt_length:], skip_special_tokens=True)
