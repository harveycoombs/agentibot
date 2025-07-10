from langchain_community.llms import VLLM

print("Loading Magistral Small 2506...")

magistral_small_2506 = VLLM(
    model="mistralai/Magistral-Small-2506",
    tokenizer="mistralai/Magistral-Small-2506",
    trust_remote_code=True,
    max_new_tokens=2048,
    top_k=10,
    top_p=0.95,
    temperature=0.85,
    tensor_parallel_size=1,
    tokenizer_mode="mistral"
)

models = {
    "magistral-small-2506": magistral_small_2506
}