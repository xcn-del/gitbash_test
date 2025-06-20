import weave
from pydantic.main import BaseModel

anthropic_client = "<anthropic.Anthropic object at 0x0000028BE3AA9110>"

class FruitExtract(BaseModel):
    fruit: str
    color: str
    flavor: str
@weave.op()
def predict(self, sentence: str) -> dict:
    # Anthropic 메시지 API 사용
    try:
        response = anthropic_client.messages.create(
            model=self.model_name,
            max_tokens=1024,  # 최대 토큰 수 설정
            messages=[
                {
                    "role": "user",
                    "content": self.prompt_template.format(sentence=sentence),
                },
                # Claude가 JSON을 잘 생성하도록 돕기 위해
                # "assistant" 역할로 시작하는 메시지를 추가할 수 있습니다.
                # {"role": "assistant", "content": "```json\n"},
            ],
        )
        # Claude의 응답은 response.content[0].text에 있습니다.
        # 우리는 모델이 JSON 문자열을 반환한다고 가정합니다.
        json_string = response.content[0].text.strip()

        # 때로는 Claude가 JSON을 마크다운 블록 안에 넣을 수 있습니다.
        if json_string.startswith("```json") and json_string.endswith("```"):
            json_string = json_string[len("```json"): -len("```")].strip()
        elif json_string.startswith("```") and json_string.endswith("```"):
            json_string = json_string[len("```"): -len("```")].strip()

        result = FruitExtract.model_validate_json(json_string)

    except Exception as e:
        print(f"Anthropic 응답 처리 오류: {e}")
        # 응답 파싱 실패 시 기본값 반환
        result = FruitExtract(fruit="unknown", color="unknown", flavor="unknown")
    return result
