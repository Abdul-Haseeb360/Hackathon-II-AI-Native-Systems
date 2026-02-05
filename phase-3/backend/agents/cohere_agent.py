"""
Cohere agent implementation for AI-powered task management
Handles natural language processing and tool calling for task operations
"""
import os
import logging
from typing import Dict, Any, List, Optional
import cohere
from tools.mcp_tools import add_task, list_tasks, complete_task, delete_task, update_task  # type: ignore
from sqlmodel import Session
from src.database.database import engine  # type: ignore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class CohereAgent:
    def __init__(self):
        """
        Initialize the Cohere agent with API key and tool definitions
        """
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            logger.error("COHERE_API_KEY environment variable is not set")
            raise ValueError("COHERE_API_KEY environment variable is not set")

        try:
            self.client = cohere.Client(api_key=api_key)
            logger.info("Cohere client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Cohere client: {str(e)}")
            raise

        # Track token usage for cost control
        self.token_usage = {
            'input_tokens': 0,
            'output_tokens': 0,
            'total_tokens': 0
        }

        # Define tools that the agent can use
        self.tools = [
            {
                "name": "add_task",
                "description": "Add a new task to the user's task list",
                "parameter_definitions": {
                    "title": {
                        "type": "str",
                        "description": "Title of the task to add",
                        "required": True
                    },
                    "description": {
                        "type": "str",
                        "description": "Optional description of the task",
                        "required": False
                    }
                }
            },
            {
                "name": "list_tasks",
                "description": "List tasks for the current user, optionally filtered by status",
                "parameter_definitions": {
                    "status": {
                        "type": "str",
                        "description": "Filter tasks by status: 'all', 'pending', 'completed'",
                        "required": False
                    }
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameter_definitions": {
                    "task_id": {
                        "type": "int",
                        "description": "ID of the task to mark as completed",
                        "required": True
                    }
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task from the user's task list",
                "parameter_definitions": {
                    "task_id": {
                        "type": "int",
                        "description": "ID of the task to delete",
                        "required": True
                    }
                }
            },
            {
                "name": "update_task",
                "description": "Update an existing task",
                "parameter_definitions": {
                    "task_id": {
                        "type": "int",
                        "description": "ID of the task to update",
                        "required": True
                    },
                    "title": {
                        "type": "str",
                        "description": "New title for the task (optional)",
                        "required": False
                    },
                    "description": {
                        "type": "str",
                        "description": "New description for the task (optional)",
                        "required": False
                    },
                    "completed": {
                        "type": "bool",
                        "description": "New completion status for the task (optional)",
                        "required": False
                    }
                }
            }
        ]

    def call_tool(self, tool_name: str, parameters: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Execute a tool with the given parameters

        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool
            user_id: ID of the user making the request

        Returns:
            Result of the tool execution
        """
        # Add user_id to parameters for all tools
        params_with_user = {**parameters, "user_id": user_id}

        # Create a database session for the tool call
        with Session(engine) as session:
            params_with_user["session"] = session

            try:
                if tool_name == "add_task":
                    return add_task(**params_with_user)
                elif tool_name == "list_tasks":
                    return list_tasks(**params_with_user)
                elif tool_name == "complete_task":
                    return complete_task(**params_with_user)
                elif tool_name == "delete_task":
                    return delete_task(**params_with_user)
                elif tool_name == "update_task":
                    return update_task(**params_with_user)
                else:
                    return {"status": "error", "message": f"Unknown tool: {tool_name}"}
            except Exception as e:
                return {"status": "error", "message": f"Tool execution failed: {str(e)}"}

    def process_message(self, message: str, user_id: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Process a natural language message using Cohere and execute any required tools

        Args:
            message: Natural language message from the user
            user_id: ID of the user making the request
            conversation_history: Previous messages in the conversation (for context)

        Returns:
            Response from the AI agent
        """
        try:
            # Validate input
            if not message or not message.strip():
                return {
                    "response": "Please provide a valid message.",
                    "status": "error"
                }

            # Prepare the chat history
            chat_history = []
            if conversation_history:
                for msg in conversation_history:
                    chat_history.append({
                        "role": "USER" if msg.get("role") == "user" else "CHATBOT",
                        "message": msg.get("content", "")
                    })

            # Add the current message to history
            chat_history.append({"role": "USER", "message": message})

            # Call Cohere's chat endpoint with tools with error handling and retry logic
            max_retries = 3
            retry_count = 0

            while retry_count < max_retries:
                try:
                    response = self.client.chat(
                        message=message,
                        chat_history=chat_history[:-1],  # Exclude the current message from history
                        tools=self.tools,
                        force_single_step=True,
                        preamble=self._get_system_preamble(),
                        # Add timeout and other safety parameters
                        temperature=0.7,
                        max_tokens=1000
                    )

                    # Update token usage statistics
                    if hasattr(response, 'meta') and hasattr(response.meta, 'tokens'):
                        tokens = response.meta.tokens
                        self.token_usage['input_tokens'] += getattr(tokens, 'input_tokens', 0)
                        self.token_usage['output_tokens'] += getattr(tokens, 'output_tokens', 0)
                        self.token_usage['total_tokens'] += getattr(tokens, 'total_tokens', 0)

                    break  # Success, exit retry loop
                except Exception as api_error:
                    retry_count += 1
                    logger.warning(f"Cohere API error (attempt {retry_count}): {str(api_error)}")

                    if retry_count >= max_retries:
                        # Log the error for monitoring
                        logger.error(f"Cohere API failed after {max_retries} retries: {str(api_error)}")

                        return {
                            "response": "Sorry, I'm currently experiencing high demand. Please try again in a moment.",
                            "status": "error",
                            "message": "API temporarily unavailable"
                        }

                    # Wait before retry (implementing exponential backoff)
                    import time
                    time.sleep(2 ** retry_count)  # 2s, 4s, 8s backoff

            # Check if the model decided to use any tools
            if response.tool_calls:
                # Execute each tool call and collect results
                tool_results = []

                # Limit the number of tool calls to prevent abuse
                tool_calls_to_process = response.tool_calls[:5]  # Maximum 5 tool calls per request

                for tool_call in tool_calls_to_process:
                    tool_name = tool_call.name
                    parameters = tool_call.parameters

                    # Execute the tool with error handling
                    try:
                        result = self.call_tool(tool_name, parameters, user_id)
                        tool_results.append({
                            "call": {"name": tool_name, "parameters": parameters},
                            "outputs": [result]
                        })
                    except Exception as tool_error:
                        logger.error(f"Tool execution error for {tool_name}: {str(tool_error)}")
                        tool_results.append({
                            "call": {"name": tool_name, "parameters": parameters},
                            "outputs": [{"status": "error", "message": f"Tool execution failed: {str(tool_error)}"}]
                        })

                # If there were tool calls, get the final response after tool execution
                if tool_results:
                    try:
                        # Get final response from Cohere after processing tool results
                        final_response = self.client.chat(
                            message=message,
                            chat_history=chat_history + [{"role": "CHATBOT", "message": str(tool_results)}],
                            tools=self.tools
                        )

                        # Update token usage for final response
                        if hasattr(final_response, 'meta') and hasattr(final_response.meta, 'tokens'):
                            tokens = final_response.meta.tokens
                            self.token_usage['input_tokens'] += getattr(tokens, 'input_tokens', 0)
                            self.token_usage['output_tokens'] += getattr(tokens, 'output_tokens', 0)
                            self.token_usage['total_tokens'] += getattr(tokens, 'total_tokens', 0)

                        # Process the response to format task lists with bullet points
                        processed_response = self._format_task_list_response(final_response.text, tool_results)

                        return {
                            "response": processed_response,
                            "tool_calls": [tc.dict() for tc in response.tool_calls],
                            "tool_results": tool_results,
                            "status": "success"
                        }
                    except Exception as final_error:
                        logger.error(f"Final response generation error: {str(final_error)}")
                        # Return response with tool results even if final response fails
                        # Process the response to format task lists with bullet points
                        default_response = f"I processed your request with {len(tool_results)} operations, but encountered an issue generating the final response. The operations were completed successfully."
                        processed_response = self._format_task_list_response(default_response, tool_results)

                        return {
                            "response": processed_response,
                            "tool_calls": [tc.dict() for tc in response.tool_calls],
                            "tool_results": tool_results,
                            "status": "partial_success"
                        }

            # If no tools were called, return the direct response
            return {
                "response": response.text,
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Unexpected error in process_message: {str(e)}")
            return {
                "response": "Sorry, I encountered an unexpected error processing your request. Please try again.",
                "status": "error",
                "message": str(e)
            }

    def _get_system_preamble(self) -> str:
        """
        Get the system preamble that guides the AI behavior
        """
        return """
        You are an AI assistant that helps users manage their todo tasks.
        Your job is to understand natural language requests and perform appropriate task operations.
        Always be helpful, concise, and confirm actions taken.

        Available operations:
        - Add tasks: when user wants to create a new task
        - List tasks: when user wants to see their tasks (filter by pending/completed if specified)
        - Complete tasks: when user wants to mark a task as done
        - Delete tasks: when user wants to remove a task
        - Update tasks: when user wants to modify an existing task

        Always respond in a friendly, helpful tone and confirm any actions taken.
        If you're unsure about a request, ask for clarification.

       
        When listing tasks, always use this specific format for each item:
        - Task [id]: [title] ([status])
        Use "(incomplete)" for pending tasks and "(completed)" for finished ones.
        """

    def _format_task_list_response(self, response_text: str, tool_results: List[Dict]) -> str:
        """
        Format task list responses to use clean bullet points

        Args:
            response_text: Original response from the AI
            tool_results: Results from tool executions

        Returns:
            Formatted response with bullet points for task lists
        """
        import re

        # Check if this is a list_tasks operation
        has_list_operation = any(
            result.get('call', {}).get('name') == 'list_tasks'
            for result in tool_results
        )

        if has_list_operation:
            # Extract task data from tool results
            for result in tool_results:
                if result.get('call', {}).get('name') == 'list_tasks':
                    task_output = result.get('outputs', [{}])[0]

                    # If the output contains tasks, format them nicely
                    if 'tasks' in task_output and isinstance(task_output['tasks'], list):
                        tasks = task_output['tasks']

                        # Build formatted task list
                        formatted_tasks = "\n\n**Your tasks:**"
                        for task in tasks:
                            status = "✓" if task.get('completed', False) else "○"
                            title = task.get('title', 'Untitled Task')
                            task_id = task.get('id', 'N/A')

                            # Format based on completion status
                            if task.get('completed', False):
                                formatted_tasks += f"\n- Task {task_id}: {title} (completed)"
                            else:
                                formatted_tasks += f"\n- Task {task_id}: {title} (incomplete)"

                        # Replace any generic task list in the response with our formatted version
                        # Look for patterns that indicate a task list is being returned
                        if 'following tasks' in response_text.lower() or 'here are' in response_text.lower():
                            # Remove any existing task list from the response
                            lines = response_text.split('\n')
                            filtered_lines = []
                            skip_next_lines = False

                            for line in lines:
                                # Skip lines that look like raw task listings
                                if re.match(r'^\s*[0-9]+\.|^-\s+Task|^•', line):
                                    if not skip_next_lines:
                                        skip_next_lines = True
                                    continue
                                elif skip_next_lines and (line.strip() == "" or re.match(r'^\s*[0-9]+\.|^-\s+Task|^•', line)):
                                    continue
                                else:
                                    skip_next_lines = False
                                    filtered_lines.append(line)

                            # Reconstruct the response without the original task list
                            base_response = '\n'.join(filtered_lines).strip()

                            # Combine the base response with our formatted task list
                            return f"{base_response}{formatted_tasks}"
                        else:
                            # Append the formatted task list to the response
                            return f"{response_text}{formatted_tasks}"

        return response_text


# Global agent instance
cohere_agent_instance = None


def get_cohere_agent():
    """
    Get or create a singleton instance of the Cohere agent
    """
    global cohere_agent_instance
    if cohere_agent_instance is None:
        cohere_agent_instance = CohereAgent()
    return cohere_agent_instance