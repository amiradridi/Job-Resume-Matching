import pytest
from ..loggers import wandb_logger_v1


def test_logger():
    wandb_logger_v1("test", [])
