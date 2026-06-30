import { AgentState, Task, TaskType, TaskStatus } from './orchestrator';
import { io } from '../index';

export class TaskMaster {
    private state: AgentState;
    private projectId: string;
    private projectName: string;

    constructor(state: AgentState, projectId: string, projectName: string) {
        this.state = state;
        this.projectId = projectId;
        this.projectName = projectName;

        if (!this.state.tasks) {
            this.state.tasks = [];
        }
    }

    /**
     * Generates a predictable ID for the task based on the project name.
     * e.g. "SOL-1", "FAR-2"
     */
    private generateTaskId(): string {
        const prefix = this.projectName.substring(0, 3).toUpperCase();
        const currentCount = this.state.tasks.filter(t => t.id.startsWith(prefix)).length;
        return `${prefix}-${currentCount + 1}`;
    }

    /**
     * Adds a new task to the state.
     */
    public addTask(
        title: string,
        description: string,
        type: TaskType = 'Task',
        author: string = 'System',
        assignees: string[] = [],
        dependencies: string[] = [],
        artifacts: string[] = [],
        affectedFiles: string[] = [],
        plannedTime?: string
    ): Task {
        const newTask: Task = {
            projectId: this.projectId,
            projectName: this.projectName,
            id: this.generateTaskId(),
            title,
            description,
            type,
            status: 'To Do',
            author,
            assignees,
            dependencies,
            artifacts,
            affectedFiles,
            agentThoughts: [],
            plannedTime,
        };

        this.state.tasks.push(newTask);

        // Notify clients in real-time
        io.emit('task_created', newTask);

        return newTask;
    }

    /**
     * Updates an existing task by its ID.
     */
    public updateTask(taskId: string, updates: Partial<Task>): Task | null {
        const taskIndex = this.state.tasks.findIndex(t => t.id === taskId);
        if (taskIndex === -1) return null;

        this.state.tasks[taskIndex] = {
            ...this.state.tasks[taskIndex],
            ...updates
        };

        const updatedTask = this.state.tasks[taskIndex];

        // Notify clients in real-time
        io.emit('task_updated', updatedTask);

        return updatedTask;
    }

    /**
     * Updates task status
     */
    public updateTaskStatus(taskId: string, status: TaskStatus): Task | null {
        return this.updateTask(taskId, { status });
    }

    /**
     * Adds a new thought to the agentThoughts array of a task
     */
    public addAgentThought(taskId: string, thought: string): Task | null {
        const task = this.getTaskById(taskId);
        if (!task) return null;

        const newThoughts = [...(task.agentThoughts || []), thought];
        return this.updateTask(taskId, { agentThoughts: newThoughts });
    }

    /**
     * Deletes a task by its ID.
     */
    public deleteTask(taskId: string): boolean {
        const taskIndex = this.state.tasks.findIndex(t => t.id === taskId);
        if (taskIndex === -1) return false;

        this.state.tasks.splice(taskIndex, 1);

        // Notify clients in real-time
        io.emit('task_deleted', { taskId });

        return true;
    }

    /**
     * Retrieves all tasks for the current project.
     */
    public getAllTasks(): Task[] {
        return this.state.tasks;
    }

    /**
     * Retrieves a specific task by its ID.
     */
    public getTaskById(taskId: string): Task | undefined {
        return this.state.tasks.find(t => t.id === taskId);
    }

    /**
     * Retrieves all pending tasks (To Do or In Progress).
     */
    public getPendingTasks(): Task[] {
        return this.state.tasks.filter(t => t.status === 'To Do' || t.status === 'In Progress');
    }
}
