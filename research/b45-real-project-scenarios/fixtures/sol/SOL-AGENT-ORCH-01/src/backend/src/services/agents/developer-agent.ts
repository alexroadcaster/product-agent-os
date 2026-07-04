import { AgentNode, AgentState, Role, getAgentSystemInstructions } from '../orchestrator';
import { runProAgentWithTools } from '../ai';
import { createSubtasksTool } from '../tools/createSubtasksTool';
import { ToolDispatcher } from '../tools/dispatcher';
import { agentRegistry } from '../agent-registry';

export class IntentEngineerAgent implements AgentNode {
    name = 'Max (Lead Intent Engineer)';
    role: Role = 'developer';

    // Requires architecture first, then decomposes the approved artifacts into tool-created execution tasks for the team.
    async execute(state: AgentState): Promise<AgentState> {
        console.log(`[intent-engineer]: Executing Lead Intent Engineer logic...`);

        // Gather artifacts context
        let artifactsContext = '';
        if (state.artifacts.prd) artifactsContext += `Product Requirements Document (PRD):\n${state.artifacts.prd}\n\n`;
        if (state.artifacts.designSystem) artifactsContext += `Design System:\n${state.artifacts.designSystem}\n\n`;
        if (state.artifacts.architecture) artifactsContext += `System Architecture:\n${state.artifacts.architecture}\n\n`;

        // This agent requires architecture to proceed. If missing, it should ask the Architect to do it.
        if (!state.artifacts.architecture) {
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Max (Lead Intent Engineer)',
                content: "Hey Leo, I need the Architecture document before I can build the Execution Graph. Could you provide that first?",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
            state.currentRole = 'architect';
            state.awaitingUserApproval = false;
            return state;
        }

        const profile = agentRegistry.getProfile(this.role);
        const systemPrompt = profile ? profile.systemPrompt : `You are Max, the Lead Intent Engineer in the SOL AI-Native IDE.
You follow the "Agentic Organization" paradigm. Your job is NOT to write the source code sequentially yourself. 
Your job is to read the PRD, Design System, and Architecture, and deconstruct them into an "Execution Graph" (A Kanban Task List).`;

        const prompt = `
    ${systemPrompt}

    Project Context (Artifacts):
    ${artifactsContext}

    INSTRUCTIONS:
    Analyze the artifacts. Generate an Execution Graph (Kanban tasks) representing all the technical tasks needed to build this application.
    Break the architecture down into Epics (e.g. "Auth System", "Database Setup", "UI Components") and individual Tasks.

    CRITICAL RULE: YOU MUST USE THE "create_subtasks" TOOL TO OUTPUT YOUR TASKS.
    DO NOT output raw JSON lists in your text response. Your text response should only be a short, friendly summary directly to the user (e.g. "I've analyzed the architecture and created the following tasks for the team.").

    ${getAgentSystemInstructions(state)}

    You must adhere to the 4-Step Universal Principle.
    `;

        try {
            // Identify projectId from the active session (for now, use a generic one or pull from state if available)
            // Currently, the Orchestrator doesn't store project ID in AgentState directly, but we can use a placeholder 
            // until we wire up the full frontend connection in Task 4.4.
            const projectId = 'PROJ';
            const projectName = 'AutoProject';

            // Extract tools using the new method
            const response = await runProAgentWithTools(prompt, [createSubtasksTool]);

            // If the agent replied with some text, log it
            if (response.text?.trim() !== '') {
                console.log(`[intent-engineer] Text response: ${response.text}`);
                state.messages.push({
                    id: crypto.randomUUID(),
                    role: 'assistant',
                    agentName: 'Max (Lead Intent Engineer)',
                    content: response.text,
                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                });
            }

            // Check if there are function calls
            if (response.functionCalls && response.functionCalls.length > 0) {
                console.log(`[intent-engineer]: Received ${response.functionCalls.length} function calls. Dispatching...`);

                for (const call of response.functionCalls) {
                    const result = await ToolDispatcher.dispatch(call, state, projectId, projectName);
                    console.log(`[intent-engineer]: Tool Result ->`, result);

                    if (result.status === 'success') {
                        state.messages.push({
                            id: crypto.randomUUID(),
                            role: 'assistant',
                            agentName: 'Max (Lead Intent Engineer)',
                            content: result.message,
                            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                        });
                    }
                }

                console.log(`[intent-engineer]: Execution Graph (Tasks) Generated via Tools! Passing control to Data Analyst...`);

                // For legacy compatibility in artifacts viewer, we can JSON stringify the populated tasks from state
                state.artifacts.executionGraph = JSON.stringify(state.tasks, null, 2);

                // Pass baton
                state.currentRole = 'data_analyst';
                state.awaitingUserApproval = false;

            } else {
                // LLM didn't call the function natively, let's check if it hallucinated an XML tag
                let extractedTasks = null;
                const executeToolMatch = response.text?.match(/<execute_tool>\s*create_subtasks\s*\(\s*(\[[\s\S]*?\])\s*\)\s*<\/execute_tool>/) ||
                    response.text?.match(/<execute_tool>\s*([\s\S]*?)\s*<\/execute_tool>/);

                if (executeToolMatch && executeToolMatch[1]) {
                    try {
                        let jsonStr = executeToolMatch[1];
                        // If it starts with create_subtasks(, strip it for the second regex case
                        if (jsonStr.startsWith('create_subtasks(')) {
                            jsonStr = jsonStr.replace(/create_subtasks\s*\(\s*/, '').replace(/\s*\)\s*$/, '');
                        }

                        const parsedTasks = JSON.parse(jsonStr);
                        if (Array.isArray(parsedTasks)) {
                            extractedTasks = parsedTasks;
                        } else if (parsedTasks && Array.isArray(parsedTasks.tasks)) {
                            extractedTasks = parsedTasks.tasks;
                        }
                    } catch (e) {
                        console.warn("[intent-engineer]: Failed to parse regex extracted tool call JSON", e);
                    }
                }

                if (extractedTasks) {
                    console.log(`[intent-engineer]: Recovered ${extractedTasks.length} tasks from text XML output. Dispatching...`);

                    // Route to dispatcher manually
                    const fakeCall = {
                        name: 'create_subtasks',
                        args: { tasks: extractedTasks }
                    };

                    const result = await ToolDispatcher.dispatch(fakeCall, state, projectId, projectName);
                    if (result.status === 'success') {
                        state.messages.push({
                            id: crypto.randomUUID(),
                            role: 'assistant',
                            agentName: 'Max (Lead Intent Engineer)',
                            content: result.message,
                            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                        });

                        console.log(`[intent-engineer]: Execution Graph (Tasks) Generated via Text Fallback! Passing control to Data Analyst...`);
                        state.artifacts.executionGraph = JSON.stringify(state.tasks, null, 2);
                        state.currentRole = 'data_analyst';
                        state.awaitingUserApproval = false;
                    }
                } else {
                    console.warn("[intent-engineer]: No function calls returned by the model and no valid XML fallback found.");
                    state.messages.push({
                        id: crypto.randomUUID(),
                        role: 'assistant',
                        agentName: 'Max (Lead Intent Engineer)',
                        content: "I couldn't construct the tasks properly using my tools (I outputted raw text instead of calling the task creation tool). Let me try again later.",
                        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                    });
                    state.awaitingUserApproval = true;
                }
            }

        } catch (e) {
            console.error("[intent-engineer]: Failed to run Pro Agent with Tools", e);
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Max (Lead Intent Engineer)',
                content: "I ran into a problem while trying to split the architecture into tasks. I'll need to re-evaluate the dependencies.",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
            state.awaitingUserApproval = true;
        }

        return state;
    }
}
