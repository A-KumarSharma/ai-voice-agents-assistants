import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe,JobContext,WorkerOptions,cli,llm
from livekit.agents.voice_assistant import voice_assistant
from livekit.plugins import openai,silero
from api import AssistantFnc

load_dotenv()

async def entrypoint(ctx:JobContext):
    initial_ctx=llm.ChatContext().append(
        role="system",
        text=(
            "Welcome to the voice assistant service. I can provide general information on a wide range of topics.Please let me know how I can assist you today."
        ),
    )
    await ctx.connect(Auto_Subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx=AssistantFnc()


    assitant=VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,
    )

    assitant.start(ctx.room)

    await asyncio.sleep(1)
    await assitant.say("hey,how can i help you today!!",allow_interruptions=True)
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))