import pandas as pd
import os

import pandas as pd
import os

def combine_and_sort_csv(sort_column):
    # 현재 파일의 경로
    folder_path = os.path.dirname(os.path.abspath(__file__))

    # 모든 CSV 파일을 읽어서 리스트에 저장
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    # 데이터프레임 리스트 초기화
    dfs = []

    # 각 CSV 파일을 읽어서 데이터프레임 리스트에 추가
    for filename in all_files:
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path, encoding='cp949')
        dfs.append(df)

    # 모든 데이터프레임을 하나로 합치기
    combined_df = pd.concat(dfs, ignore_index=True)

    # 특정 속성으로 정렬
    combined_df.sort_values(by=sort_column, inplace=True)

    # 통합된 데이터프레임을 CSV 파일로 저장
    output_file = os.path.join(folder_path, 'combined_sorted.csv')
    combined_df.to_csv(output_file, index=False, encoding='cp949')

    print(f'CSV 파일이 통합되고 {sort_column}으로 정렬되었습니다. 저장된 파일: {output_file}')

# 사용 예
sort_column = ['모델','월(month)']  # 정렬할 속성명
combine_and_sort_csv(sort_column)