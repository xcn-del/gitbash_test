import weave


<error>
@weave.op()
def predict(self, sentence: str) -> dict:
    try:
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": self.prompt_template.format(sentence=sentence),
                },
            ],
            temperature=0.3,
            max_tokens=512,
        )
        content = response.choices[0].message.content.strip()

        # 마크다운 JSON 블록 제거
        if content.startswith("```json") and content.endswith("```"):
            content = content[7:-3].strip()
        elif content.startswith("```") and content.endswith("```"):
            content = content[3:-3].strip()

        result = FruitExtract.model_validate_json(content)

        if isinstance(result.flavor, list):
            result.flavor = ", ".join(result.flavor)

    except Exception as e:
        print(f"OpenRouter 응답 처리 오류: {e}")
        result = FruitExtract(fruit="unknown", color="unknown", flavor="unknown")

    return result
