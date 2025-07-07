from langchain_community.llms import LlamaCpp

print("Loading Magistral Small 2506...")

magistral_small_2506 = LlamaCpp(
    model_path="../models/Magistral-Small-2506-Q6_K_L.gguf",
    n_gpu_layers=-1,
    n_batch=512,
    temperature=0.8,
    max_tokens=2048,
    top_p=0.95,
    n_ctx=8192,
    verbose=False
)

models = {
    "magistral-small-2506": magistral_small_2506
}