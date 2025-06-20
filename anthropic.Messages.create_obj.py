import weave
from typing import Iterable
from anthropic.types.message_param import MessageParam
from typing import Union as ModelParam
from anthropic.types.metadata_param import MetadataParam
from anthropic import NotGiven
from typing import Literal
from typing import List
from typing import Union
from anthropic.types.text_block_param import TextBlockParam
from typing import Union as ThinkingConfigParam
from typing import Union as ToolChoiceParam
from typing import Union as ToolUnionParam
from typing import Mapping as Headers
from typing import Mapping as Query
from builtins import objectas Body
import httpx
from anthropic._utils._utils import is_given
import warnings
from anthropic._utils._transform import maybe_transform
import anthropic.types.message_create_params as message_create_params
from anthropic._base_client import make_request_options
from anthropic.types.message import Message
from anthropic import Stream
from typing import Annotated as RawMessageStreamEvent
from anthropic._utils._utils import required_args

NOT_GIVEN = "NOT_GIVEN"

DEFAULT_TIMEOUT = "Timeout(connect=5.0, read=600, write=600, pool=600)"

MODEL_NONSTREAMING_TOKENS = {
    "claude-opus-4-20250514": 8192,
    "claude-opus-4-0": 8192,
    "claude-4-opus-20250514": 8192,
    "anthropic.claude-opus-4-20250514-v1:0": 8192,
    "claude-opus-4@20250514": 8192
}

DEPRECATED_MODELS = {
    "claude-1.3": "November 6th, 2024",
    "claude-1.3-100k": "November 6th, 2024",
    "claude-instant-1.1": "November 6th, 2024",
    "claude-instant-1.1-100k": "November 6th, 2024",
    "claude-instant-1.2": "November 6th, 2024",
    "claude-3-sonnet-20240229": "July 21st, 2025",
    "claude-2.1": "July 21st, 2025",
    "claude-2.0": "July 21st, 2025"
}

@weave.op()
@required_args(["max_tokens", "messages", "model"], ["max_tokens", "messages", "model", "stream"])
def create(
    self,
    *,
    max_tokens: int,
    messages: Iterable[MessageParam],
    model: ModelParam,
    metadata: MetadataParam | NotGiven = NOT_GIVEN,
    service_tier: Literal["auto", "standard_only"] | NotGiven = NOT_GIVEN,
    stop_sequences: List[str] | NotGiven = NOT_GIVEN,
    stream: Literal[False] | Literal[True] | NotGiven = NOT_GIVEN,
    system: Union[str, Iterable[TextBlockParam]] | NotGiven = NOT_GIVEN,
    temperature: float | NotGiven = NOT_GIVEN,
    thinking: ThinkingConfigParam | NotGiven = NOT_GIVEN,
    tool_choice: ToolChoiceParam | NotGiven = NOT_GIVEN,
    tools: Iterable[ToolUnionParam] | NotGiven = NOT_GIVEN,
    top_k: int | NotGiven = NOT_GIVEN,
    top_p: float | NotGiven = NOT_GIVEN,
    # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
    # The extra values given here take precedence over values defined on the client or passed to this method.
    extra_headers: Headers | None = None,
    extra_query: Query | None = None,
    extra_body: Body | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
) -> Message | Stream[RawMessageStreamEvent]:
    if not stream and not is_given(timeout) and self._client.timeout == DEFAULT_TIMEOUT:
        timeout = self._client._calculate_nonstreaming_timeout(
            max_tokens, MODEL_NONSTREAMING_TOKENS.get(model, None)
        )

    if model in DEPRECATED_MODELS:
        warnings.warn(
            f"The model '{model}' is deprecated and will reach end-of-life on {DEPRECATED_MODELS[model]}.\nPlease migrate to a newer model. Visit https://docs.anthropic.com/en/docs/resources/model-deprecations for more information.",
            DeprecationWarning,
            stacklevel=3,
        )

    return self._post(
        "/v1/messages",
        body=maybe_transform(
            {
                "max_tokens": max_tokens,
                "messages": messages,
                "model": model,
                "metadata": metadata,
                "service_tier": service_tier,
                "stop_sequences": stop_sequences,
                "stream": stream,
                "system": system,
                "temperature": temperature,
                "thinking": thinking,
                "tool_choice": tool_choice,
                "tools": tools,
                "top_k": top_k,
                "top_p": top_p,
            },
            message_create_params.MessageCreateParamsStreaming
            if stream
            else message_create_params.MessageCreateParamsNonStreaming,
        ),
        options=make_request_options(
            extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
        ),
        cast_to=Message,
        stream=stream or False,
        stream_cls=Stream[RawMessageStreamEvent],
    )
