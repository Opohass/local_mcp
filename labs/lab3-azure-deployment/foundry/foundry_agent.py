"""
Create an Azure AI Foundry agent connected to the deployed MCP server.

Prerequisites:
    pip install azure-identity azure-ai-projects

Environment variables:
    AZURE_AI_PROJECT_ENDPOINT  - Your Foundry project endpoint
    MCP_SERVER_URL             - Your deployed MCP server URL (e.g., https://<fqdn>/mcp)

Usage:
    python foundry_agent.py
"""

import asyncio
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


async def main():
    endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
    mcp_url = os.environ.get("MCP_SERVER_URL")
    model = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")

    if not endpoint or not mcp_url:
        print("ERROR: Set AZURE_AI_PROJECT_ENDPOINT and MCP_SERVER_URL environment variables.")
        print("")
        print("Example:")
        print('  export AZURE_AI_PROJECT_ENDPOINT="https://<hub>.services.ai.azure.com/api/projects/<id>"')
        print('  export MCP_SERVER_URL="https://<fqdn>/mcp"')
        return

    print("Creating Foundry agent with MCP tools...")

    async with DefaultAzureCredential() as credential:
        async with AIProjectClient(
            endpoint=endpoint,
            credential=credential,
        ) as client:
            # Create MCP tool connection
            mcp_tool = client.agents.get_mcp_tool(
                server_label="DevTools",
                server_url=mcp_url,
                require_approval="never",
            )

            # Create agent
            agent = await client.agents.create_agent(
                model=model,
                name="MCP-DevAssistant",
                instructions="You are a developer assistant. Use the MCP DevTools to help with development tasks.",
                tools=mcp_tool.definitions,
                headers=mcp_tool.headers,
            )
            print(f"Agent created: {agent.id}")

            # Create a thread and run a test query
            thread = await client.agents.create_thread()
            test_query = "Check the health of https://httpbin.org/get and search for 'degraded' in the sample dataset"
            print(f"Running test query: \"{test_query}\"")

            await client.agents.create_message(
                thread_id=thread.id,
                role="user",
                content=test_query,
            )

            run = await client.agents.create_and_process_run(
                thread_id=thread.id,
                agent_id=agent.id,
            )

            if run.status == "failed":
                print(f"Run failed: {run.last_error}")
            else:
                messages = await client.agents.list_messages(thread_id=thread.id)
                for msg in messages.data:
                    if msg.role == "assistant":
                        for block in msg.content:
                            if hasattr(block, "text"):
                                print(f"\nAgent response:\n{block.text.value}")

            # Cleanup
            print("\nCleaning up agent...")
            await client.agents.delete_agent(agent.id)
            print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
