import os
import yaml
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

CONFIG = yaml.safe_load(open(f"{os.getcwd().replace("\\", "/")}/config.yaml"))

gpt = ChatOpenAI(
    api_key=CONFIG["openai_api_key"],
    model="gpt-5-mini",
    temperature=0.85,
    max_tokens=2048
)

claude = ChatAnthropic(
    api_key=CONFIG["anthropic_api_key"],
    model="claude-3-5-haiku-20241022",
    temperature=0.85,
    max_tokens=2048,
    top_p=0.95,
    top_k=10
)

models = {
    "gpt": gpt,
    "claude": claude
}