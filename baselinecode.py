import urllib.request
import tarfile
import os
import pandas as pd

# 1. 다운로드할 URL
url = "https://aistages-api-public-prod.s3.amazonaws.com/app/Competitions/000362/data/20250511152423/code.tar.gz"
filename = "baselinecode.tar.gz"
extract_dir = "baselinecode"  # 원하는 폴더 이름만 남김

# 2. 파일 다운로드
urllib.request.urlretrieve(url, filename)
print(f"{filename} 다운로드 완료")

# 3. 압축 해제 (내부 폴더 제거)
if not os.path.exists(extract_dir):
    os.makedirs(extract_dir)

with tarfile.open(filename, "r:gz") as tar:
    for member in tar.getmembers():
        if member.name.startswith("code/"):  # 내부 폴더 이름이 'code/'일 경우
            member.name = member.name.replace("code/", "")  # 폴더 제거
            tar.extract(member, path=extract_dir)

print(f"{filename} 압축 해제 완료 → {extract_dir}/ 에 파일 정리됨")