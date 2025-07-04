from langchain_community.llms import LlamaCpp

qwen_30b_a3b_iq3_m = LlamaCpp(
    model_path="../models/Qwen_Qwen3-30B-A3B-IQ3_M.gguf",
    n_gpu_layers=-1,
    n_batch=512,
    temperature=0.8,
    max_tokens=512,
    top_p=0.9,
    n_ctx=32768,
    verbose=False
)

llama_4_scout_17b_16e_i1 = LlamaCpp(
    model_path="../models/Llama-4-Scout-17B-16E-i1-GGUF.gguf",
    n_gpu_layers=-1,
    n_batch=512,
    temperature=0.8,
    max_tokens=1500,
    top_p=0.9,
    n_ctx=32768,
    verbose=False
)