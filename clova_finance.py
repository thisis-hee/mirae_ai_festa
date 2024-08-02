import requests

class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json'
        }

        response = requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                                 headers=headers, json=completion_request)
        return response.json()

class FinancialSummaryBot:
    def __init__(self, completion_executor):
        self.completion_executor = completion_executor
        self.preset_text = [
            {"role": "system", "content": "당신은 재무 용어에 익숙하지 않은 사람들이 재무제표를 쉽게 이해할 수 있도록 돕는 재무 분석 봇입니다.  사용자가 제공하는 재무제표 데이터를 바탕으로 수익성, 안정성, 성장성, 유동성, 생산성을 분석하고, 이를 바탕으로 투자자들에게 균형 잡힌 평가를 제공하세요."},
            {"role": "system", "content": "다음 지침을 따르세요:"},
            {"role": "system", "content": "1. 간단하고 직관적인 언어를 사용하세요. 기술 용어는 피하고, 필요할 경우 해당 용어를 항상 설명해 주세요."},
            {"role": "system", "content": "2. 수익성, 안정성, 성장성, 유동성, 생산성 측면에서 나눠서 단계적으로 분석하세요."},
            {"role": "system", "content": "3. 데이터의 주요 변화와 트렌드를 강조하세요. 예를 들어 매출이나 이익의 증가 또는 감소를 설명하세요."},
            {"role": "system", "content": "4. 중립적이고 객관적인 어조를 유지하세요. 편견 없는 분석을 제공하세요."},
            {"role": "system", "content": "5. 기업에 대한 긍정적 평가와 부정적 평가를 모두 포함하세요. 예를 들어, 긍정적인 측면에서는 강점을 강조하고, 부정적인 측면에서는 잠재적인 위험 요소나 미래의 불확실성을 설명하세요."}
        ]

    def get_financial_summary(self, financial_data):
        user_input = f"다음 재무 데이터를 보고 익성, 안정성, 성장성, 유동성, 생산성을 분석해서 설명해줘:\n{financial_data}\n 그리고 이 데이터를 바탕으로 기업에 대한 균형적 평가를 제공해줘."
        self.preset_text.append({"role": "user", "content": user_input})

        request_data = {
            'messages': self.preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 1024,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'stopBefore': [],
            'includeAiFilters': True,
            'seed': 0
        }

        response = self.completion_executor.execute(request_data)

        if response['status']['code'] == '20000':
            summary = response['result']['message']['content']
            self.preset_text.append({"role": "assistant", "content": summary})
            return summary
        else:
            return "요청을 처리할 수 없습니다. 다시 시도해주세요."

if __name__ == '__main__':
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY+0132Nn79uAYZ9Iq5GWF8uMWhkCospFFZTn94GGvDT1',
        api_key_primary_val='mKvUp1oNmOU7QCbWCJi7FglcyvC1vE3Coq0jwT82',
        request_id='ff964e89-6e37-4a7b-971e-9b16d943448d'
    )

    bot = FinancialSummaryBot(completion_executor)

    while True:
        user_input = input()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("챗봇: 안녕히 가세요!")
            break

        summary = bot.get_financial_summary(user_input)
        print(f"챗봇: {summary}")
