
import time
from prompt import gen_prompt
import json
from model import Model
from tools import tools_map
import re

def extract_ast_to_bts(string):
    match = re.search(r'```json(.*?)```', string, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

"""
todo: 
    1.环境变量设置
    2. 工具引入
    3. prompt 模版
    4. 模型初始化
"""

model = Model()

chat_history= []
agent_scratch = ''

def parse_thouths(response):
    """
        response:
        {
            "action":{
                "name" : "action_name",
                "args":{
                    "args name" : "args value"
                }
            },
            "thoughts":
            {
                "text" : "thought",
                "plan" : "plan",
                "criticism" : "criticism",
                "speak" : "当前步返回给用户的总结",
                "reasoning":""
            }    
        }
    """
    try:
        thoughts = response.get("thoughts")
        observation = thoughts.get('speak')
        plan = thoughts.get("plan")
        reasoning = thoughts.get("reasoning")
        criticism = thoughts.get("criticism")
        prompt = f"plan:{plan}\nreasoning:{reasoning}\ncriticism:{criticism}\nobservation:{observation}"
        return prompt
    except Exception as err:
        print('parse thoughts err: {}'.format(err))
        return "".format(err)

def agent_excute(query,max_request_time=10):
    cur_request_time = 0
    global agent_scratch

    while cur_request_time < max_request_time:
        cur_request_time +=1
        prompt = gen_prompt(query,agent_scratch)

        start_time = time.time()

        print('*****************{},开始调用llm........'.format(cur_request_time),flush=True)

        # 调大模型

        """

        sys_prompt:
        user_msg,assistant,history,
        """
        content = model.chat(prompt,chat_history=chat_history)

        end_time = time.time()
        
        print('*****************{},调用大模型结束，耗时：{}'.format(cur_request_time,end_time-start_time),flush=True)

        print("模型输出:",content)

        if content.startswith("```json"):
            content = extract_ast_to_bts(content)
            print('格式处理',content)
        try:

            response = json.loads(content)
        except Exception as e:
            print('调用大模型错误，即将重试。。。。',e)
            # chat_history.append([prompt,content])
            # prompt = '请直接输出json内容，不要带有```json 标识'
            continue
        """
        response:
        {
            "action":{
                "name" : "action_name",
                "args":{
                    "args name" : "args value"
                }
            },
            "thoughts":
            {
                "text" : "thought",
                "plan" : "plan",
                "criticism" : "criticism",
                "speak" : "当前步返回给用户的总结",
                "reasoning":""
            }    
        }
        """
        action_info = response.get('action')
        action_name = action_info.get('name')
        action_args = action_info.get('args')
        print('当前action name ：',action_name,action_args)

        if action_name == "finish":
            final_answer = action_args.get("answer")
            print("final_answer:", final_answer)
            break

        observation = response.get('thoughts').get("speak")
        try:
            func = tools_map.get(action_name)
            call_function_result = func(**action_args)
        except Exception as err:
            print("调用工具异常",err)

        agent_scratch= agent_scratch + '\n' + observation
        agent_scratch = agent_scratch + "\n: observation:{}\n execute action result: {}".format(observation,
                                                                                                call_function_result)
        
        chat_history.append([prompt,content])
        
def main():
    max_request_time = 10
    while True:
        query = input('请输入目标:')

        if query == 'exit':
            return

        agent_excute(query,max_request_time=max_request_time)

if __name__ == '__main__':
    main()