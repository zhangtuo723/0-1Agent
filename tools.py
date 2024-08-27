
import json
import os

from tavily import TavilyClient

"""
    1、写文件
    2、读文件
    3、追加的方式写
    4、专业领域知识的获取(网络搜索)
"""

from langchain_community.tools.tavily_search import TavilySearchResults

# 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
# tavily_client = TavilyClient(api_key="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")

def read_file(filename):
    filename = os.path.join("./data/", filename)
    if not os.path.exists(filename):
        return f"{filename} not exit, please check file exist before read"
    with open(filename, 'r', encoding="utf-8") as f:
        return "\n".join(f.readlines())


def append_to_file(filename, content):
    filename = os.path.join("./data/", filename)
    if not os.path.exists(filename):
        f"{filename} not exit, please check file exist before read"
    with open(filename, 'a') as f:
        f.write(content)
    return "append_content to file success."


def write_to_file(filename, content):
    filename = os.path.join("./data/", filename)
    if not os.path.exists("./data/"):
        os.makedirs("./data/")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return "write content to file success."



def search(query):

    tavily = TavilySearchResults(max_results=5,search_depth='advanced')

    try:
        ret = tavily.invoke(input=query)
    except Exception as e:
        return e


    return ret



tools_info = [
    {
        "name": "read_file",
        "description": "读取文件行为",
        "args": [
            {
                "name": "filename",
                "type": "string",
                "description": "文件名"
            }
        ]
    },
    {
        "name": "append_to_file",
        "description": "追加内容到文件行为",
        "args": [
            {
                "name": "filename",
                "type": "string",
                "description": "文件名"
            },
            {
                "name": "content",
                "type": "string",
                "description": "追加到文件中的内容"
            }
        ]
    },
{
        "name": "write_to_file",
        "description": "写内容到文件行为",
        "args": [
            {
                "name": "filename",
                "type": "string",
                "description": "文件名"
            },
            {
                "name": "content",
                "type": "string",
                "description": "写入到文件中的内容"
            }
        ]
    },
{
        "name": "finish",
        "description": "完成用户目标行为",
        "args": [
            {
                "name": "answer",
                "type": "string",
                "description": "最后的目标结果"
            }
        ]
    },
    {
        "name": "search",
        "description": "搜索行为"
                       "when you are unsure of large model return",
        "args": [
            {
                "name": "query",
                "type": "string",
                "description": "要搜索的内容"
            }
        ]
    }
]

tools_map = {
    "read_file": read_file,
    "append_to_file": append_to_file,
    "write_to_file": write_to_file,
    "search":search
    # "search": search
}


def gen_tools_desc():
    """
    生成工具描述
    :return:
    """
    tools_desc = []
    for idx, t in enumerate(tools_info):
        args_desc = []
        for info in t["args"]:
            args_desc.append({
                "name": info["name"],
                "description": info["description"],
                "type": info["type"]
            })
        args_desc = json.dumps(args_desc, ensure_ascii=False)
        tool_desc = f"{idx+1}.{t['name']}:{t['description']}, args: {args_desc}"
        tools_desc.append(tool_desc)
    tools_prompt = "\n".join(tools_desc)
    return tools_prompt




tools_des = str(tools_info)




