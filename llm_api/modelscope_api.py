from openai import OpenAI
from .chat_messages import ChatMessages

# ModelScope模型配置 - 免费调用，价格为0
modelscope_model_config = {
    "MiniMax/MiniMax-M2": {
        "Pricing": (0, 0),
        "currency_symbol": '￥',
    },
    "Qwen/Qwen3-Coder-480B-A35B-Instruct": {
        "Pricing": (0, 0),
        "currency_symbol": '￥',
    },
    "Qwen/Qwen3-30B-A3B-Instruct-2507": {
        "Pricing": (0, 0),
        "currency_symbol": '￥',
    },
    "Qwen/Qwen3-235B-A22B-Thinking-2507": {
        "Pricing": (0, 0),
        "currency_symbol": '￥',
    },
}

def stream_chat_with_modelscope(messages, model='MiniMax/MiniMax-M2', response_json=False, api_key=None, base_url='https://api-inference.modelscope.cn/v1', max_tokens=4_096):
    """
    ModelScope平台流式聊天接口
    
    Args:
        messages: 消息列表
        model: 模型ID，如 'MiniMax/MiniMax-M2'
        response_json: 是否返回JSON格式
        api_key: ModelScope API Token
        base_url: ModelScope API基础URL
        max_tokens: 最大token数
    
    Returns:
        生成器，yield消息对象
    """
    if api_key is None:
        raise Exception('未提供有效的 api_key！')
    
    # 创建OpenAI客户端，使用ModelScope的base_url
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    try:
        # 创建流式聊天完成
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            max_tokens=max_tokens,
            response_format={"type": "json_object"} if response_json else None
        )
        
        # 初始化消息内容
        messages.append({'role': 'assistant', 'content': ''})
        
        # 流式处理响应
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                messages[-1]['content'] += chunk.choices[0].delta.content
                yield messages
        
        return messages
        
    except Exception as e:
        raise Exception(f"ModelScope API调用失败: {str(e)}")

if __name__ == '__main__':
    # 测试函数
    test_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你好，请介绍一下自己。"}
    ]
    
    try:
        for response in stream_chat_with_modelscope(
            messages=test_messages,
            model='MiniMax/MiniMax-M2',
            api_key='ms-15989b4c-db65-4849-9f2c-1e45bcd367b1'  # 测试用的API Key
        ):
            print(response[-1]['content'], end='', flush=True)
    except Exception as e:
        print(f"测试失败: {e}")