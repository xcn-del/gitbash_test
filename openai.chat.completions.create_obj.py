import weave
from typing import Iterable
from typing import Union as ChatCompletionMessageParam
from typing import Union
from typing import Literal as ChatModel
from typing import Optional
from openai.types.chat.chat_completion_audio_param import ChatCompletionAudioParam
from openai import NotGiven
import openai.types.chat.completion_create_params as completion_create_params
from typing import Dict
from typing import Dict as Metadata
from typing import List
from typing import Literal
from openai.types.chat.chat_completion_prediction_content_param import ChatCompletionPredictionContentParam
from typing import Optional as ReasoningEffort
from openai.types.chat.chat_completion_stream_options_param import ChatCompletionStreamOptionsParam
from typing import Union as ChatCompletionToolChoiceOptionParam
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from typing import Mapping as Headers
from typing import Mapping as Query
from builtins import objectas Body
import httpx
import inspect
import pydantic
from openai._utils._transform import maybe_transform
from openai._base_client import make_request_options
from openai.types.chat.chat_completion import ChatCompletion
from openai import Stream
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai._utils._utils import required_args

NOT_GIVEN = "NOT_GIVEN"

def validate_response_format(response_format: object) -> None:
    if inspect.isclass(response_format) and issubclass(response_format, pydantic.BaseModel):
        raise TypeError(
            "You tried to pass a `BaseModel` class to `chat.completions.create()`; You must use `beta.chat.completions.parse()` instead"
        )

@weave.op()
@required_args(["messages", "model"], ["messages", "model", "stream"])
def create(
    self,
    *,
    messages: Iterable[ChatCompletionMessageParam],
    model: Union[str, ChatModel],
    audio: Optional[ChatCompletionAudioParam] | NotGiven = NOT_GIVEN,
    frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
    function_call: completion_create_params.FunctionCall | NotGiven = NOT_GIVEN,
    functions: Iterable[completion_create_params.Function] | NotGiven = NOT_GIVEN,
    logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
    logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
    max_completion_tokens: Optional[int] | NotGiven = NOT_GIVEN,
    max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
    metadata: Optional[Metadata] | NotGiven = NOT_GIVEN,
    modalities: Optional[List[Literal["text", "audio"]]] | NotGiven = NOT_GIVEN,
    n: Optional[int] | NotGiven = NOT_GIVEN,
    parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
    prediction: Optional[ChatCompletionPredictionContentParam] | NotGiven = NOT_GIVEN,
    presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
    reasoning_effort: Optional[ReasoningEffort] | NotGiven = NOT_GIVEN,
    response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
    seed: Optional[int] | NotGiven = NOT_GIVEN,
    service_tier: Optional[Literal["auto", "default", "flex"]] | NotGiven = NOT_GIVEN,
    stop: Union[Optional[str], List[str], None] | NotGiven = NOT_GIVEN,
    store: Optional[bool] | NotGiven = NOT_GIVEN,
    stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
    stream_options: Optional[ChatCompletionStreamOptionsParam] | NotGiven = NOT_GIVEN,
    temperature: Optional[float] | NotGiven = NOT_GIVEN,
    tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
    tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
    top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
    top_p: Optional[float] | NotGiven = NOT_GIVEN,
    user: str | NotGiven = NOT_GIVEN,
    web_search_options: completion_create_params.WebSearchOptions | NotGiven = NOT_GIVEN,
    # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
    # The extra values given here take precedence over values defined on the client or passed to this method.
    extra_headers: Headers | None = None,
    extra_query: Query | None = None,
    extra_body: Body | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
) -> ChatCompletion | Stream[ChatCompletionChunk]:
    validate_response_format(response_format)
    return self._post(
        "/chat/completions",
        body=maybe_transform(
            {
                "messages": messages,
                "model": model,
                "audio": audio,
                "frequency_penalty": frequency_penalty,
                "function_call": function_call,
                "functions": functions,
                "logit_bias": logit_bias,
                "logprobs": logprobs,
                "max_completion_tokens": max_completion_tokens,
                "max_tokens": max_tokens,
                "metadata": metadata,
                "modalities": modalities,
                "n": n,
                "parallel_tool_calls": parallel_tool_calls,
                "prediction": prediction,
                "presence_penalty": presence_penalty,
                "reasoning_effort": reasoning_effort,
                "response_format": response_format,
                "seed": seed,
                "service_tier": service_tier,
                "stop": stop,
                "store": store,
                "stream": stream,
                "stream_options": stream_options,
                "temperature": temperature,
                "tool_choice": tool_choice,
                "tools": tools,
                "top_logprobs": top_logprobs,
                "top_p": top_p,
                "user": user,
                "web_search_options": web_search_options,
            },
            completion_create_params.CompletionCreateParamsStreaming
            if stream
            else completion_create_params.CompletionCreateParamsNonStreaming,
        ),
        options=make_request_options(
            extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
        ),
        cast_to=ChatCompletion,
        stream=stream or False,
        stream_cls=Stream[ChatCompletionChunk],
    )
