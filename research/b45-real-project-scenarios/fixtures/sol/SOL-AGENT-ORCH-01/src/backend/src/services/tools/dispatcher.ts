import { AgentState } from '../orchestrator';
import { TaskMaster } from '../taskMaster';

/**
 * Handles function calls returned by the AI agent and executes the corresponding
 * local side-effects (e.g., adding tasks to TaskMaster).
 */
export class ToolDispatcher {

    /**
     * Dispatches a single function call to the appropriate internal tool logic.
     * Modifies the AgentState in place via TaskMaster.
     */
    public static async dispatch(
        functionCall: any,
        state: AgentState,
        projectId: string,
        projectName: string
    ): Promise<any> {

        console.log(`[ToolDispatcher] Executing function: ${functionCall.name}`);

        // Switch on the function name defined in our tools schema
        switch (functionCall.name) {
            case 'create_subtasks':
                return await this.handleCreateSubtasks(functionCall.args, state, projectId, projectName);

            // We can add more tools here in the future (e.g. read_github_repo, search_web)
            default:
                console.warn(`[ToolDispatcher] Unknown function call: ${functionCall.name}`);
                return { error: `Unknown function: ${functionCall.name}` };
        }
    }

    /**
     * Internal handler for the 'create_subtasks' tool.
     * Parses the args and instantiates tasks in the TaskMaster.
     */
    private static async handleCreateSubtasks(
        args: any,
        state: AgentState,
        projectId: string,
        projectName: string
    ): Promise<any> {

        const taskMaster = new TaskMaster(state, projectId, projectName);
        const addedTasks = [];

        // The arguments should contain a "tasks" array as defined in our schema
        if (args && Array.isArray(args.tasks)) {
            for (const t of args.tasks) {

                // Let TaskMaster handle incrementing IDs and saving to state
                const newTask = taskMaster.addTask(
                    t.title,
                    t.description || '',
                    t.type || 'Task',
                    'Agent', // We can improve this by passing the specific agent's role
                    t.assignees || [],
                    t.dependencies || [],
                    t.artifacts || [],
                    t.affectedFiles || [],
                    t.plannedTime
                );

                // If the agent provided a specific thought process for this task
                if (t.agentThoughts) {
                    taskMaster.addAgentThought(newTask.id, t.agentThoughts);
                }

                addedTasks.push(newTask.id);
            }

            return {
                status: "success",
                message: `Successfully created ${addedTasks.length} tasks.`,
                createdTaskIds: addedTasks
            };

        } else {
            return {
                status: "error",
                message: "Invalid arguments: 'tasks' array missing or malformed."
            };
        }
    }
}
