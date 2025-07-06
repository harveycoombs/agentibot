from langchain_community.llms import LlamaCpp

print("Loading Qwen 3 30B A3B...")

qwen_30b_a3b_iq3_m = LlamaCpp(
    model_path="../models/Qwen_Qwen3-30B-A3B-IQ3_M.gguf",
    n_gpu_layers=-1,
    n_batch=128,
    temperature=0.7,
    max_tokens=1024,
    top_p=0.9,
    n_ctx=8192,
    verbose=False
)

print("Loading Llama 4 Scout 17B 16E Instruct...")

llama_4_scout_17b_16e_i1 = LlamaCpp(
    model_path="../models/Llama-4-Scout-17B-16E-Instruct-UD-IQ1_M.gguf",
    n_gpu_layers=-1,
    n_batch=192,
    temperature=0.7,
    max_tokens=1200,
    top_p=0.9,
    n_ctx=8192,
    verbose=False
)

models = {
    "qwen-3-30b-a3b": qwen_30b_a3b_iq3_m,
    "llama-4-scout-17b-16e": llama_4_scout_17b_16e_i1
}