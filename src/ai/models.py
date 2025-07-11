from langchain_community.llms import VLLM

print("Loading Qwen3 14B...")

qwen3_14b = VLLM(
    model="Qwen/Qwen3-14B",
    trust_remote_code=True,
    max_new_tokens=2048,
    top_k=10,
    top_p=0.95,
    temperature=0.85,
    tensor_parallel_size=1
)

models = {
    "qwen3-14b": qwen3_14b
}