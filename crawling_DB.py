import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import json


def financial_crawling(keyword):
    # URL 설정
    url = f'https://comp.fnguide.com/SVO2/asp/SVD_Finance.asp?pGB=1&gicode={keyword}&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701'

    # 웹 페이지 요청
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 재무제표 테이블 찾기
    tables = soup.find_all('table', {'class': 'us_table_ty1 h_fix zigbg_no'})

    # 필요한 테이블을 데이터프레임으로 변환하여 리스트에 저장
    dfs = [pd.read_html(str(tables[i]))[0] for i in [0, 2, 4]]

    # 데이터프레임을 행으로 합치기
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df=combined_df.iloc[:,0:5]
    ifrs=['매출액',
    '매출원가',
    '매출총이익',
    '판매비와관리비계산',
    '영업이익',
    '영업이익(발표기준)',
    '금융수익계산',
    '금융원가계산',
    '기타수익계산',
    '기타비용계산',
    '종속기업,공동지배기업및관계기업관련손익계산',
    '세전계속사업이익',
    '법인세비용',
    '계속영업이익',  
    '중단영업이익',
    '당기순이익',
    '지배주주순이익',
    '비지배주주순이익',
    '자산',
    '유동자산계산',
    '비유동자산계산',
        '기타금융업부채',
    '부채',
    '유동부채계산',
    '비유동부채계산',
        '기타금융업부채',
    '자본',
    '지배기업주주지분계산',
    '비지배주주지분',
    '영업활동으로인한현금흐름',
    '당기순손익',
        '법인세비용차감전계속사업이익',
    '현금유출이없는비용등가산계산',
    '(현금유입이없는수익등차감)계산',
    '영업활동으로인한자산부채변동(운전자본변동)계산',
    '*영업에서창출된현금흐름',
    '기타영업활동으로인한현금흐름계산',
    '투자활동으로인한현금흐름',
    '투자활동으로인한현금유입액계산',
    '(투자활동으로인한현금유출액)계산',
        '기타투자활동으로인한현금흐름',
    '재무활동으로인한현금흐름',
    '재무활동으로인한현금유입액계산',
    '(재무활동으로인한현금유출액)계산',
    '기타재무활동으로인한현금흐름계산',
        '영업투자재무활동기타현금흐름',
        '연결범위변동으로인한현금의증가',
    '환율변동효과',
    '현금및현금성자산의증가',
    '기초현금및현금성자산',
    '기말현금및현금성자산']
    combined_df['IFRS(연결)']=ifrs
    cleaned_df = combined_df.dropna()
    df=cleaned_df.reset_index().drop('index',axis=1)
    df.insert(0, 'code', keyword)
    df.columns = ['code', 'IFRS(연결)', '202112', '202212', '202312', '202403']
    print(df)
    return df



def initialize_db():
    db_path='financial_data.sqlite'
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financial_data (
                code TEXT,
                ITEM TEXT,
                "202112" REAL,
                "202212" REAL,
                "202312" REAL,
                "202403" REAL
            )
    ''')
        conn.commit()



def insert_data_into_db(df):
    db_name='financial_data.sqlite'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for i, row in df.iterrows():
        cursor.execute('''
        INSERT INTO financial_data (code, Item, "202112", "202212", "202312", "202403")
        VALUES (?, ?, ?, ?, ?, ?)
        ''', tuple(row))

    conn.commit()
    conn.close()


def bring(keyword):
    conn = sqlite3.connect("financial_data.sqlite")
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM financial_data WHERE code=?", (keyword,))
    
    columns = [description[0] for description in cur.description]
    
    rows = cur.fetchall()
    
    data = [dict(zip(columns, row)) for row in rows]
    
    json_file=f'{keyword}_financial.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    cur.close()
    conn.close()

# db 초기화 코드. 한번만 생성해주면 됨.
#initialize_db()

# 재무제표 정보 크롤링
#dataset1 = financial_crawling('A003490')

# db에 크롤링한 데이터 삽입
#insert_data_into_db(dataset1)

# db에서 json 파일로 데이터 가져오기
bring('A003490')


