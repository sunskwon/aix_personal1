import torch
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel
from rank_bm25 import BM25Okapi
import numpy as np

# Tokenizer 및 모델 로드
tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
  bos_token='</s>', eos_token='</s>', unk_token='<unk>',
  pad_token='<pad>', mask_token='<mask>')
tokenizer.tokenize("안녕하세요. 한국어 GPT-2 입니다.😤:)l^o")
model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')

# BM25용 샘플 문서 및 쿼리
documents = [
    "근육이 커지기 위해서는 운동과 단백질 섭취가 중요합니다.",
    "유산소 운동과 근력 운동을 병행하면 체중 감소에 도움이 됩니다.",
    "탄수화물은 에너지 공급원으로, 운동 전후에 섭취하는 것이 좋습니다."
]
queries = ["키가 크려면?"]
# prompt = (
#     "다음 질문에 대해 context의 내용을 바탕으로 대답해주세요. \n\n"
#     "context에 적합한 내용이 없으면 '응답종료'로 대답하세요. \n\n"
# )

# BM25 인덱스 구축
tokenized_docs = [doc.split() for doc in documents]
bm25 = BM25Okapi(tokenized_docs)

# 검색 쿼리 토크나이즈
query = queries[0]
tokenized_query = query.split()

# 쿼리로부터 검색된 문서의 인덱스 가져오기
scores = bm25.get_scores(tokenized_query)
best_doc_idx = np.argmax(scores)
retrieved_document = documents[best_doc_idx]

# KoGPT 모델로 텍스트 생성
# text = f"prompt: {prompt} \n\n context: {retrieved_document} \n\n query: {query}"
text = f"{retrieved_document} \n\n {query}"
input_ids = tokenizer.encode(text, return_tensors='pt')

# 텍스트 생성
gen_ids = model.generate(
    input_ids,
    max_length=128,
    repetition_penalty=2.0,
    do_sample=True,
    temperature=0.3, # 샘플링의 창의성 조정
    top_p=0.9,       # nucleus sampling
    pad_token_id=tokenizer.pad_token_id,
    eos_token_id=tokenizer.eos_token_id,
    bos_token_id=tokenizer.bos_token_id,
    use_cache=True
)

# 응답 디코딩 및 출력
generated = tokenizer.decode(gen_ids[0], skip_special_tokens=True)
print("Generated Response:", generated.split("."))
print("Generated Response:", generated.split(".")[0])
print("Generated Response:", generated.split(".")[1])
