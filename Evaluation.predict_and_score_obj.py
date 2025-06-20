import weave
from typing import Union
from weave.trace.op import Op
from weave.flow.model import Model
from weave.flow.model import apply_model_async
from weave.flow.model import ApplyModelError
from weave.flow.scorer import get_scorer_attributes

@weave.op()
async def predict_and_score(self, model: Union[Op, Model], example: dict) -> dict:
    apply_model_result = await apply_model_async(
        model, example, self.preprocess_model_input
    )

    if isinstance(apply_model_result, ApplyModelError):
        return {
            self._output_key: None,
            "scores": {},
            "model_latency": apply_model_result.model_latency,
        }

    model_output = apply_model_result.model_output
    model_call = apply_model_result.model_call
    model_latency = apply_model_result.model_latency

    scores = {}
    if scorers := self.scorers:
        for scorer in scorers:
            apply_scorer_result = await model_call.apply_scorer(scorer, example)
            result = apply_scorer_result.result
            scorer_attributes = get_scorer_attributes(scorer)
            scorer_name = scorer_attributes.scorer_name
            scores[scorer_name] = result

    return {
        self._output_key: model_output,
        "scores": scores,
        "model_latency": model_latency,
    }
