from langchain_community.llms import VLLM

model = VLLM(
    model="unsloth/Qwen3-8B-GGUF",
    trust_remote_code=True,
    vllm_kwargs={"quantization": "q4_k_m"},
    max_new_tokens=2048,
    max_model_len=2048,
    top_k=10,
    top_p=0.95,
    temperature=0.85,
    tensor_parallel_size=1
)