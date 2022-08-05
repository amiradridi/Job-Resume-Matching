from typing import Dict, Any, Tuple, Callable, List, Optional, IO
import sys

from spacy import util
from spacy.errors import Errors
from spacy.util import registry


def wandb_logger_v1(project_name: str, remove_config_values: List[str] = []):
    try:
        import wandb
        from wandb import init, log, join  # test that these are available
    except ImportError:
        raise ImportError(Errors.E880)

    console_logger = registry.get("loggers", "spacy.ConsoleLogger.v1")
    console = console_logger(progress_bar=False)

    def setup_logger(
        nlp: "Language", stdout: IO = sys.stdout, stderr: IO = sys.stderr
    ) -> Tuple[Callable[[Dict[str, Any]], None], Callable[[], None]]:
        config = nlp.config.interpolate()
        config_dot = util.dict_to_dot(config)
        for field in remove_config_values:
            del config_dot[field]
        config = util.dot_to_dict(config_dot)
        wandb.init(project=project_name, config=config, reinit=True)
        console_log_step, console_finalize = console(nlp, stdout, stderr)

        def log_step(info: Optional[Dict[str, Any]]):
            console_log_step(info)
            if info is not None:
                score = info["score"]
                other_scores = info["other_scores"]
                losses = info["losses"]
                wandb.log({"score": score})
                if losses:
                    wandb.log({f"loss_{k}": v for k, v in losses.items()})
                if isinstance(other_scores, dict):
                    wandb.log(other_scores)

        def finalize() -> None:
            console_finalize()
            wandb.join()

        return log_step, finalize

    return setup_logger
