import requests
import pandas as pd
import pandas as pd
import csv
import json


# 네이버 클라우드 플랫폼에서 발급받은 클라이언트 아이디와 시크릿
client_id = "ezp6anpue8"
client_secret = "b3ax7kQmIP3l165zVSmFluVwvDOA9gsn3MWdxg2L"

# API 엔드포인트 URL
url = "https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize"

# 요청 헤더 설정
headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/json"
}

# Content만 빼서 json형태로 바꾸는 함수 지정
def to_json_and_summary_comments(csv_path):
    data_contents=pd.read_csv(csv_path)
    data_contents=data_contents['본문']
    data_contents.to_json('comments.json', orient = 'index', indent = 4)

    json_path='comments.json'
    with open(json_path, 'r') as f:
        json_data = json.load(f)

    summarized_data = []

    for i in range(len(json_data)):
        index=i
        specific_row = json_data[str(index)]

        data = {
            "document": {
                "content": specific_row
            },
            "option": {
                "language": "ko",
                "model": "general",
                "tone": 0,
                "summaryCount": 3
            }
        }
        # POST 요청 보내기
        response = requests.post(url, headers=headers, json=data)

        # 응답 처리
        if response.status_code == 200:
            summary_result = response.json()
            summarized_text = summary_result.get("summary", "")  # 요약 결과에서 실제 요약 텍스트 추출 (필요에 따라 수정)
            summarized_data.append({"Text": summarized_text})
        else:
            print("요청 실패: 상태 코드", response.status_code)
            print("응답 내용:", response.text)

    df_summarized = pd.DataFrame(summarized_data)
    with open('comments_summary.json', 'w', encoding='utf-8') as f:
        json.dump(df_summarized.to_dict(orient='records'), f, ensure_ascii=False, indent=4)


to_json_and_summary_comments('news_summary/comments_many_news_content.csv')