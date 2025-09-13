import os
import yaml
from langchain_community.llms import VLLM
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

CONFIG = yaml.safe_load(open(f"{os.getcwd().replace("\\", "/")}/config.yaml"))

mistral = VLLM(
    model="unsloth/Mistral-Small-3.2-24B-Instruct-2506-unsloth-bnb-4bit",
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

claude = ChatAnthropic(
    api_key=CONFIG["anthropic_api_key"],
    model="claude-3-5-haiku-20241022",
    temperature=0.85,
    max_tokens=2048,
    top_p=0.95,
    top_k=10
)

gpt = ChatOpenAI(
    api_key=CONFIG["openai_api_key"],
    model="gpt-5-mini",
    temperature=0.85,
    max_tokens=2048
)

models = {
    "mistral": mistral,
    "claude": claude,
    "gpt": gpt
}