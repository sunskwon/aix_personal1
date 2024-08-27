from transformers import pipeline

classifier = pipeline("ner", model="KoichiYasuoka/roberta-base-korean-upos")

def pick_keyword(text):
    
    result = classifier(text)

    noun_list = []

    for i in range(len(result)):
        if result[i]['entity'] == 'NOUN' or result[i]['entity'] == 'B-NOUN':
            noun_list.append(result[i]['word'])
            
    return noun_list