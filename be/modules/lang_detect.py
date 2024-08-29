import re

def detect_language(text):
    
    # 한글과 영어의 유니코드 범위
    KOREAN_PATTERN = re.compile('[가-힣]')
    
    if KOREAN_PATTERN.search(text):
        return text
    else:
        return ''