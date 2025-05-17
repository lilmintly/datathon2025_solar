import urllib.request
import tarfile
import os
import pandas as pd

# 1. 다운로드할 URL
url = "https://aistages-api-public-prod.s3.amazonaws.com/app/Competitions/000362/data/20250510042253/data.tar.gz"
filename = "data.tar.gz"
extract_dir = "."  

# 다운로드
urllib.request.urlretrieve(url, filename)
print(f"{filename} 다운로드 완료")

# 압축 해제
with tarfile.open(filename, "r:gz") as tar:
    # 압축 안의 모든 파일 반복
    for member in tar.getmembers():
        # "data/"로 시작하는 파일만 추출
        if member.name.startswith("data/"):
            # 경로에서 "data/" 제거 → data/train.csv → train.csv
            member.name = member.name.replace("data/", "")
            tar.extract(member, path="data")  # 실제 추출 위치는 ./data/
print("압축 해제 완료 → data/ 폴더에 파일만 정리됨")

