import { ToolDeclaration } from '../ai';

export const createSubtasksTool: ToolDeclaration = {
    name: "create_subtasks",
    description: "Create a list of structured subtasks to break down a larger project, epic, or architecture plan.",
    parameters: {
        type: "OBJECT",
        properties: {
            tasks: {
                type: "ARRAY",
                description: "A list of tasks to be created in the SOL TaskMaster.",
                items: {
                    type: "OBJECT",
                    properties: {
                        title: {
                            type: "STRING",
                            description: "A short, concise title for the task."
                        },
                        type: {
                            type: "STRING",
                            description: "The type of task. Must be one of: Epic, Story, Task, SubTask, Bug, Idea."
                        },
                        description: {
                            type: "STRING",
                            description: "A detailed markdown description of what needs to be done. Include technical details if applicable."
                        },
                        assignees: {
                            type: "ARRAY",
                            description: "A list of role names that should work on this task (e.g. ['developer', 'architect']).",
                            items: {
                                type: "STRING"
                            }
                        },
                        dependencies: {
                            type: "ARRAY",
                            description: "A list of task IDs that must be completed before this task can start. Use empty array if none.",
                            items: {
                                type: "STRING"
                            }
                        },
                        artifacts: {
                            type: "ARRAY",
                            description: "An array of artifact names that are relevant to this task (e.g. ['Architecture Diagram', 'PRD']).",
                            items: {
                                type: "STRING"
                            }
                        },
                        affectedFiles: {
                            type: "ARRAY",
                            description: "A list of file paths that are expected to be modified or created by this task.",
                            items: {
                                type: "STRING"
                            }
                        },
                        plannedTime: {
                            type: "STRING",
                            description: "An estimate of how long this task will take (e.g. '2 hours', '1 day')."
                        },
                        agentThoughts: {
                            type: "STRING",
                            description: "The reasoning behind why this task was created and how it fits into the broader picture."
                        }
                    },
                    required: ["title", "type", "description", "assignees", "agentThoughts"]
                }
            }
        },
        required: ["tasks"]
    }
};
