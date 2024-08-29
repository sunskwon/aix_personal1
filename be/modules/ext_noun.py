import torch
from transformers import pipeline

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# pipeline 생성
classifier = pipeline("ner", model="KoichiYasuoka/roberta-base-korean-upos", device=device)

def pick_noun(text):
    
    # 입력된 문장에서 명사 추출
    result = classifier(text)

    noun_list = []
    for word in result:
        if word['entity'] == 'NOUN' or word['entity'] == 'B-NOUN':
            noun_list.append(word['word'])
            
    return noun_list