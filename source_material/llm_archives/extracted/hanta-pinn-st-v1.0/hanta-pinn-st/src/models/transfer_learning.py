"""
Transfer learning utilities for zoonotic disease pre-training.
"""
import torch
import torch.nn as nn
from peft import LoraConfig, get_peft_model


class ZoonoticTransfer:
    """
    Transfer learning from abundant zoonotic diseases (dengue, leptospirosis)
    to sparse hantavirus data.
    """
    def __init__(self, source_diseases=None):
        self.source_diseases = source_diseases or ['dengue', 'leptospirosis', 'lyme']
        self.target = 'hantavirus'

    def add_lora_adapters(self, model, r=8, lora_alpha=16, 
                         target_modules=None):
        """
        Add LoRA adapters to model for efficient fine-tuning.

        Args:
            model: Base PyTorch model
            r: LoRA rank
            lora_alpha: LoRA scaling
            target_modules: List of module names to adapt
        """
        if target_modules is None:
            target_modules = ['q_proj', 'v_proj', 'temporal_proj']

        config = LoraConfig(
            r=r,
            lora_alpha=lora_alpha,
            target_modules=target_modules,
            lora_dropout=0.1,
            bias="none",
            task_type="FEATURE_EXTRACTION"
        )

        return get_peft_model(model, config)

    def freeze_base_model(self, model, unfreeze_layers=None):
        """
        Freeze base model layers, optionally unfreezing specific ones.

        Args:
            model: PyTorch model
            unfreeze_layers: List of layer names to keep trainable
        """
        for name, param in model.named_parameters():
            param.requires_grad = False
            if unfreeze_layers:
                for layer_name in unfreeze_layers:
                    if layer_name in name:
                        param.requires_grad = True
                        break
        return model
