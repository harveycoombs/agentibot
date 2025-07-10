from langchain_community.llms import VLLM

print("Loading Qwen3 (8B)...")

magistral_small_2506 = VLLM(
    model="Qwen/Qwen3-8B",
    trust_remote_code=True,
    max_new_tokens=2048,
    top_k=10,
    top_p=0.95,
    temperature=0.85,
    tensor_parallel_size=1
)

models = {
    "magistral-small-2506": magistral_small_2506
}