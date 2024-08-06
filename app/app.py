from settings import Settings
from openai import AsyncAzureOpenAI
import chainlit as cl


@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )


@cl.on_message
async def on_message(message: cl.Message):
    settings = Settings()

    llm = AsyncAzureOpenAI(
        api_key=settings.AZURE_OPENAI_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        azure_deployment=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
        api_version=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_VERSION,
    )

    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    stream = await llm.chat.completions.create(
        messages=message_history,
        model=settings.AZURE_OPENAI_CHAT_MODEL_NAME,
        temperature=0,
        stream=True,
    )

    final_answer = cl.Message(content="", author="Answer")

    async for part in stream:
        new_delta = part.choices[0].delta

        if new_delta.content:
            if not final_answer.content:
                await final_answer.send()
            await final_answer.stream_token(new_delta.content)

    if final_answer.content:
        await final_answer.update()
