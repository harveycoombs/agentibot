from langchain_community.llms import VLLM

model = VLLM(
    model="unsloth/Qwen3-8B-bnb-4bit",
    trust_remote_code=True,
    max_new_tokens=2048,
    top_k=10,
    top_p=0.95,
    temperature=0.85,
    tensor_parallel_size=1,
    vllm_kwargs={
        "max_model_len": 2048
    }
)