from langchain_community.llms import VLLM

print("Loading Gemma 3 (12B)...")

gemma3_12b = VLLM(
    model="google/gemma-3-12b-it",
    trust_remote_code=True,
    max_new_tokens=2048,
    top_k=10,
    top_p=0.95,
    temperature=0.85,
    tensor_parallel_size=1
)

models = {
    "gemma3-12b": gemma3_12b
}