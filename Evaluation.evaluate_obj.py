import weave
from typing import Union
from weave.trace.op import Op
from weave.flow.model import Model
import json
from weave.trace.weave_client import Call
from datetime import datetime
from weave.flow.util import make_memorable_name

logger = "<Logger weave.flow.eval (INFO)>"

def default_evaluation_display_name(call: Call) -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    unique_name = make_memorable_name()
    return f"eval-{date}-{unique_name}"

@weave.op(call_display_name=default_evaluation_display_name)
async def evaluate(self, model: Union[Op, Model]) -> dict:
    eval_results = await self.get_eval_results(model)
    summary = await self.summarize(eval_results)

    logger.info(f"Evaluation summary {json.dumps(summary, indent=2)}")

    return summary
