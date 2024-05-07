import requests
from bs4 import BeautifulSoup

# 크롤링할 웹 페이지의 URL
url = 'https://gani-dev.tistory.com/category'

postArr = []
# HTTP GET 요청을 보내고 응답을 받음
response = requests.get(url)

# 응답의 상태코드 확인
if response.status_code == 200:
    # HTML을 BeautifulSoup을 사용하여 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 클래스가 'post'인 모든 div 요소 찾기
    post_divs = soup.find_all('div', class_='post')

    # 각 div 태그에서 <a> 태그 찾아서 href와 text 출력
    for div in post_divs:
        titleDiv = div.find('div', class_='title')
        link = titleDiv.find('a')
        postTitle ='['+link.text+']'+'(https://gani-dev.tistory.com'+link['href']+')'
        postArr.append(postTitle)
    
    # README 파일 경로
    file_path = "README.md"

    with open(file_path, "r") as file:
        # README 파일 내용 읽기
        readme_content = file.read()

    # "Latest Blog Posts" 아랫부분 위치 찾기
    index = readme_content.find("### Latest Blog Posts")
    if index != -1:
        # "### Latest Blog Posts" 이후의 문자열을 새로운 내용으로 대체
        default_readme_content = readme_content[:index + len("### Latest Blog Posts")] + "\n"
    else:
        # "### Latest Blog Posts"가 README 파일에 없을 경우 새로운 내용을 README 파일에 추가
        default_readme_content = readme_content + "\n\n### Latest Blog Posts\n"

    # README 파일 열기 (쓰기 모드)
    with open(file_path, "w") as file:
        # 새로운 README 내용으로 파일에 쓰기
        file.write(default_readme_content)
        for post in postArr :
            file.write("- "+post+"\n")
else:
    print("HTTP 요청 실패:", response.status_code)
