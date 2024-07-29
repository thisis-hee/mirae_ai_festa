import pandas as pd
from openai import OpenAI
import json
from datetime import datetime, timedelta

client = OpenAI(api_key="OPEN-AI-API-KEY")

# md파일 불러오기
def get_instructions(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            instructions = file.read()
        return instructions
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred while reading the file:", e)


# 기사 기간 지정
start_date = "2023-07-01"
end_date = "2024-07-01"

def most_viewed_get_advice(start_date, end_date):
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= end_date:
        date_str = current_date.strftime("%Y%m%d")
        file_name = f"crawling_data/most_viewed_news_{date_str}.csv"
        
        try:
            df = pd.read_csv(file_name)
        except FileNotFoundError:
            print(f"File {file_name} not found.")
            current_date += timedelta(days=1)
            continue
        except Exception as e:
            print(f"An error occurred while reading {file_name}: {e}")
            current_date += timedelta(days=1)
            continue

        title_column = df['Title']
        result_string = '\t'.join(title_column.astype(str))
        instructions_path = "instructions_summary.md"
        instructions = get_instructions(instructions_path)
        news_titles = result_string
            
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": news_titles}
            ]
        )

        advice = response.choices[0].message['content'] if 'content' in response.choices[0].message else response.choices[0].message.content

        advice_file_name = f"gpt_issue_output/most_viewed_news_advice_{date_str}.txt"
        with open(advice_file_name, "w", encoding="utf-8") as file:
            file.write(advice)

        current_date += timedelta(days=1)

def most_comments_get_advice(start_date, end_date):
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= end_date:
        date_str = current_date.strftime("%Y%m%d")
        file_name = f"crawling_data/comments_many_news_{date_str}.csv"
        
        try:
            df = pd.read_csv(file_name)
        except FileNotFoundError:
            print(f"File {file_name} not found.")
            current_date += timedelta(days=1)
            continue
        except Exception as e:
            print(f"An error occurred while reading {file_name}: {e}")
            current_date += timedelta(days=1)
            continue

        title_column = df['Title']
        result_string = '\t'.join(title_column.astype(str))
        instructions_path = "instructions_summary.md"
        instructions = get_instructions(instructions_path)
        news_titles = result_string
            
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": news_titles}
            ]
        )

        advice = response.choices[0].message['content'] if 'content' in response.choices[0].message else response.choices[0].message.content

        advice_file_name = f"gpt_issue_output/comments_many_news_advice_{date_str}.txt"
        with open(advice_file_name, "w", encoding="utf-8") as file:
            file.write(advice)

        current_date += timedelta(days=1)

