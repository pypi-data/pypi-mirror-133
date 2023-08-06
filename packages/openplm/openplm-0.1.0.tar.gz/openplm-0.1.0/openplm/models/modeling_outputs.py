# coding: utf-8
from dataclasses import dataclass
from typing import Optional, Tuple, List

import torch

from transformers.file_utils import ModelOutput


@dataclass
class ExtractiveSummaryOutput(ModelOutput):
    """
    Base class for outputs of Extractive summary models.
    """

    loss: Optional[torch.FloatTensor] = None
    cls_mask: torch.IntTensor = None
    logits: torch.FloatTensor = None
    hidden_states: Optional[Tuple[torch.FloatTensor]] = None
    attentions: Optional[Tuple[torch.FloatTensor]] = None

