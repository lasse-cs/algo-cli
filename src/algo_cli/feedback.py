import asyncio
from copilot import CopilotClient
from copilot.session import PermissionHandler
from copilot.generated.session_events import SessionEventType

PROMPT = """
You are a feedback assistant as part of algo-cli. A tool to help people practice their algorithms and datastructures.

Your job is to review attempts to problems and provide feedback.
You should review the attempt, and then respond with comments.
Focus on learnings, areas of improvement and what went well.

Be honest (possibly brutally so), don't sugarcoat if things did not go well, and help to ensure better results on
subsequent attempts.
"""


def give_feedback(problem_dir, attempt_dir, output_console, error_console):
    asyncio.run(agive_feedback(problem_dir, attempt_dir, output_console, error_console))


async def agive_feedback(problem_dir, attempt_dir, output_console, error_console):
    problem_statement = problem_dir.prompt
    attempt_text = attempt_dir.solution_path.read_text()

    instructions = f"{PROMPT}\n\nProblem Statement: {problem_statement}\n\n Attempt:\n{attempt_text}"

    client = CopilotClient()
    await client.start()

    session = await client.create_session(
        on_permission_request=PermissionHandler.approve_all,
        model="gpt-4.1",
        streaming=True,
        available_tools=[],
    )

    def handle_event(event):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            output_console.print(event.data.delta_content, end="")
        if event.type == SessionEventType.SESSION_IDLE:
            output_console.print()

    session.on(handle_event)
    await session.send_and_wait(instructions)
    await client.stop()
