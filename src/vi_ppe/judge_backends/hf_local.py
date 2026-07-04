from __future__ import annotations


class HfLocalBackend:
    def __init__(self, model_cfg: dict):
        self.model_cfg = model_cfg
        self.judge_model = model_cfg["model_id"]
        self._tokenizer = None
        self._processor = None
        self._model = None

    def _load(self):
        if self._model is not None:
            return
        import torch
        from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        quant_config = None
        if self.model_cfg.get("quantization") == "4bit_nf4":
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
        trust_remote_code = bool(self.model_cfg.get("trust_remote_code", False))
        model_config = AutoConfig.from_pretrained(
            self.model_cfg["model_id"],
            trust_remote_code=trust_remote_code,
        )
        attn_impl = self.model_cfg.get("attn_impl")
        if attn_impl:
            attn_config = getattr(model_config, "attn_config", None)
            if not isinstance(attn_config, dict):
                attn_config = {}
                model_config.attn_config = attn_config
            attn_config["attn_impl"] = attn_impl
        if self.model_cfg.get("loader") == "gemma3_conditional_generation":
            from transformers import AutoProcessor, Gemma3ForConditionalGeneration

            self._processor = AutoProcessor.from_pretrained(
                self.model_cfg["model_id"],
                trust_remote_code=trust_remote_code,
            )
            self._tokenizer = getattr(self._processor, "tokenizer", None)
            if self._tokenizer is not None:
                if self._tokenizer.pad_token is None:
                    self._tokenizer.pad_token = self._tokenizer.eos_token
                self._tokenizer.padding_side = "left"
            self._model = Gemma3ForConditionalGeneration.from_pretrained(
                self.model_cfg["model_id"],
                device_map="auto",
                config=model_config,
                quantization_config=quant_config,
                torch_dtype=torch.bfloat16,
                trust_remote_code=trust_remote_code,
            ).eval()
            return
        self._tokenizer = AutoTokenizer.from_pretrained(
            self.model_cfg["model_id"],
            trust_remote_code=trust_remote_code,
        )
        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token
        self._tokenizer.padding_side = "left"
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_cfg["model_id"],
            device_map="auto",
            config=model_config,
            quantization_config=quant_config,
            torch_dtype=torch.bfloat16,
            trust_remote_code=trust_remote_code,
        )

    def generate(self, prompt: str, pair: dict, order: str) -> str:
        return self.generate_batch([prompt], pairs=[pair], orders=[order])[0]

    def generate_batch(self, prompts: list[str], pairs: list[dict] | None = None, orders: list[str] | None = None) -> list[str]:
        self._load()
        if self._processor is not None:
            import torch

            messages = [
                [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
                for prompt in prompts
            ]
            encoded = self._processor.apply_chat_template(
                messages,
                tokenize=True,
                add_generation_prompt=True,
                return_dict=True,
                return_tensors="pt",
                padding=True,
            ).to(self._model.device)
            with torch.inference_mode():
                output_ids = self._model.generate(
                    **encoded,
                    max_new_tokens=int(self.model_cfg.get("max_new_tokens", 256)),
                    do_sample=False,
                )
            prompt_length = encoded["input_ids"].shape[-1]
            return [
                self._processor.decode(output[prompt_length:], skip_special_tokens=True)
                for output in output_ids
            ]
        rendered_prompts = [
            self._tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}],
                tokenize=False,
                add_generation_prompt=True,
            )
            for prompt in prompts
        ]
        encoded = self._tokenizer(rendered_prompts, return_tensors="pt", padding=True).to(self._model.device)
        output_ids = self._model.generate(
            **encoded,
            max_new_tokens=int(self.model_cfg.get("max_new_tokens", 256)),
            do_sample=False,
        )
        prompt_length = encoded["input_ids"].shape[-1]
        return [
            self._tokenizer.decode(output[prompt_length:], skip_special_tokens=True)
            for output in output_ids
        ]
