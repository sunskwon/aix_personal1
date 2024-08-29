from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch

src_text = [
    """ 위대한상상이 운영하는 배달플랫폼 요기요가 창사 이후 처음으로 희망퇴직을 실시한다. 배달의민족, 쿠팡이츠와 함께 ‘빅3’인 요기요는 배달앱 시장 출혈경쟁 등으로 적자가 누적되고 실적 악화가 지속하자 인력 감축을 통한 비용 절감에 나선 것으로 풀이된다. 

29일 업계에 따르면 전날 전준희 위대한상상 대표이사는 임직원에게 보낸 ‘CEO 레터’ 메일을 통해 “현재의 위기를 극복하고 시장에서 생존 가능성을 최대한 높이기 위해 정규직 직원을 대상으로 희망퇴직 제도를 시행한다”고 밝혔다."""
]

model_name = "google/pegasus-xsum"
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
batch = tokenizer(src_text, truncation=True, padding="longest", return_tensors="pt").to(device)
translated = model.generate(**batch)
tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
print(tgt_text)
# assert (
#     tgt_text[0]
#     == "California's largest electricity provider has turned off power to hundreds of thousands of customers."
# )