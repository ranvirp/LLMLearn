from transformers import AutoTokenizer, AutoConfig
from vllm import LLM, SamplingParams

max_model_len, tp_size = 8192, 8
#model_name = "deepseek-ai/DeepSeek-V2-Chat"
model_name = 'deepseek-v2-chat'
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
config = AutoConfig.from_pretrained(model_name, trust_remote_code=True)

#tokenizer.save_pretrained('deepseek-v2-chat')
#config.save_pretrained('deepseek-v2-chat')
#exit()
llm = LLM(model=model_name, tensor_parallel_size=tp_size, max_model_len=max_model_len, trust_remote_code=True, enforce_eager=True, device='cuda')
sampling_params = SamplingParams(temperature=0.3, max_tokens=256, stop_token_ids=[tokenizer.eos_token_id])

messages_list = [
    [{"role": "user", "content": "Who are you?"}],
    [{"role": "user", "content": "Translate the following content into Chinese directly: DeepSeek-V2 adopts innovative architectures to guarantee economical training and efficient inference."}],
    [{"role": "user", "content": "Write a piece of quicksort code in C++."}],
]

prompt_token_ids = [tokenizer.apply_chat_template(messages, add_generation_prompt=True) for messages in messages_list]

outputs = llm.generate(prompt_token_ids=prompt_token_ids, sampling_params=sampling_params)

generated_text = [output.outputs[0].text for output in outputs]
print(generated_text)
