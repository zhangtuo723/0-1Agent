
import os, json
import dashscope

import random
from http import HTTPStatus
# 建议dashscope SDK 的版本 >= 1.14.0
from dashscope import Generation


def call_with_messages():
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '你是谁？'}]
    response = Generation.call(model="qwen-turbo",
                               api_key="sk-59a2db783bbf4b7f84fdddc6c150fcd5",
                               messages=messages,
                               # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                               seed=random.randint(1, 10000),
                               temperature=0.8,
                               top_p=0.8,
                               top_k=50,
                               # 将输出设置为"message"格式
                               result_format='message')
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))



class Model(object):
    def __init__(self):
        self.api_key = 'sk-'
        # self.model_name = 'qwen1.5-110b-chat'
        self._client = dashscope.Generation()
        self.max_retry_time = 3

    def chat(self, prompt, chat_history):
        cur_retry_time = 0
        while cur_retry_time < self.max_retry_time:
            cur_retry_time += 1

            message = []

            for his in chat_history:
                message.append({"role":"user","content":his[0]})
                message.append({"role":"assistant","content":his[1]}) # todo system -》assistant

            message.append({"role":"user","content":prompt})

            # print('--------------')
            # print(message)
            # print('--------')
            response = Generation.call(model="qwen-turbo",
                               api_key="sk-",
                               messages=message,
                               # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                               seed=random.randint(1, 10000),
                               temperature=0.8,
                               top_p=0.8,
                               top_k=10,
                               # 将输出设置为"message"格式
                               result_format='message')
            if response.status_code == HTTPStatus.OK:
                try:
                    content = response['output']['choices'][0]["message"]["content"]
                    return content
                except Exception as e:
                    print("调用模型异常:{}".format(e))
            else:
                print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                    response.request_id, response.status_code,
                    response.code, response.message
                ))
                print('------>!!!')
                print(message)
                exit(0)
                      
            
        return {}
    
# call_with_messages()