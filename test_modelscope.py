#!/usr/bin/env python3
"""
ModelScope API接口测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_api import ModelConfig, stream_chat, modelscope_model_config

def test_modelscope_api():
    """测试ModelScope API接口"""
    print("ModelScope API接口测试")
    print("=" * 50)
    
    # 打印可用的ModelScope模型
    print("可用的ModelScope模型:")
    for model in modelscope_model_config:
        print(f"  - {model}")
    print()
    
    # 测试配置
    test_api_key = "ms-15989b4c-db65-4849-9f2c-1e45bcd367b1"  # 测试用的API Key
    test_model = "MiniMax/MiniMax-M2"
    
    try:
        # 创建模型配置
        model_config = ModelConfig(
            model=test_model,
            api_key=test_api_key,
            max_tokens=1000
        )
        
        print(f"测试模型: {test_model}")
        print(f"API Key: {test_api_key[:10]}...")
        print("-" * 50)
        
        # 测试消息
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你好，请用一句话介绍自己。"}
        ]
        
        print("用户消息: 你好，请用一句话介绍自己。")
        print("助手回复: ", end="", flush=True)
        
        # 流式调用
        for response in stream_chat(model_config, messages):
            if response and len(response) > 0:
                content = response[-1].get('content', '')
                if content:
                    print(content, end='', flush=True)
        
        print("\n" + "=" * 50)
        print("测试完成！")
        
    except Exception as e:
        print(f"测试失败: {e}")
        return False
    
    return True

def test_all_modelscope_models():
    """测试所有ModelScope模型"""
    print("\n测试所有ModelScope模型")
    print("=" * 50)
    
    test_api_key = "ms-15989b4c-db65-4849-9f2c-1e45bcd367b1"
    
    for model_name in modelscope_model_config:
        print(f"\n测试模型: {model_name}")
        print("-" * 30)
        
        try:
            model_config = ModelConfig(
                model=model_name,
                api_key=test_api_key,
                max_tokens=100
            )
            
            messages = [
                {"role": "user", "content": "你好"}
            ]
            
            response_text = ""
            for response in stream_chat(model_config, messages):
                if response and len(response) > 0:
                    content = response[-1].get('content', '')
                    if content:
                        response_text = content
            
            print(f"响应: {response_text[:50]}...")
            print("✓ 测试通过")
            
        except Exception as e:
            print(f"✗ 测试失败: {e}")

if __name__ == "__main__":
    # 运行基础测试
    if test_modelscope_api():
        # 如果基础测试通过，测试所有模型
        test_all_modelscope_models()
    
    print("\n测试完成！")