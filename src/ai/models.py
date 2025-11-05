import os
import yaml
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

CONFIG = yaml.safe_load(open(f"{os.getcwd().replace("\\", "/")}/config.yaml"))

gpt5_nano = ChatOpenAI(
    api_key=CONFIG["openai_api_key"],
    model="gpt-5-nano",
    temperature=0.85,
    max_tokens=2048
)

gpt5_mini = ChatOpenAI(
    api_key=CONFIG["openai_api_key"],
    model="gpt-5-mini",
    temperature=0.85,
    max_tokens=2048
)

gpt5 = ChatOpenAI(
    api_key=CONFIG["openai_api_key"],
    model="gpt-5",
    temperature=0.85,
    max_tokens=2048
)

models = {
    "gpt-5-nano": gpt5_nano,
    "gpt-5-mini": gpt5_mini,
    "gpt-5": gpt5
}