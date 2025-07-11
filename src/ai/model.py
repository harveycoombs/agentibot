from langchain_community.llms import VLLM
from transformers import BitsAndBytesConfig

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="q4_k_m",
    bnb_4bit_compute_dtype="float16"
)

model = VLLM(
    model="unsloth/Qwen3-8B-GGUF",
    engine_kwargs={ "quantization": quant_config },
    trust_remote_code=True,
    max_new_tokens=2048,
    top_k=10,
    top_p=0.95,
    temperature=0.85,
    tensor_parallel_size=1
)