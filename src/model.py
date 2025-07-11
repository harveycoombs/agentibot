from langchain_community.llms import VLLM

qwen3_8b = VLLM(
    model="",
    trust_remote_code=True,
    max_new_tokens=2048,
    top_k=10,
    top_p=0.95,
    temperature=0.85,
    tensor_parallel_size=1
)

models = {
    "qwen3-8b": qwen3_8b
}