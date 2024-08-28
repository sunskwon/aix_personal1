from transformers import pipeline

# pipeline 생성
classifier = pipeline("ner", model="KoichiYasuoka/roberta-base-korean-upos")

def pick_keyword(text):
    
    # 입력된 문장에서 명사 추출
    result = classifier(text)

    noun_list = []
    for word in result:
        if word['entity'] == 'NOUN' or word['entity'] == 'B-NOUN':
            noun_list.append(word['word'])
            
    return noun_list