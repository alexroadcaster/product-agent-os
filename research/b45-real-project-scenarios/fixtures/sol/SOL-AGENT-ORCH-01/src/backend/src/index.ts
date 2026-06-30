import express, { Request, Response } from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';
import { runFlashAgent, runProAgent } from './services/ai';
import { initializeCollections, getSession, saveSession, getAllAgentProfiles, getAgentProfile, saveAgentProfile } from './services/db';
import { agentRegistry, AgentProfile } from './services/agent-registry';
import { orchestrator, AgentState, Role } from './services/orchestrator';
import { TaskMaster } from './services/taskMaster';
import { RouterAgent } from './services/agents/router-agent';
import { ProductOwnerAgent } from './services/agents/product-owner-agent';
import { ArchitectAgent } from './services/agents/architect-agent';
import { DesignerAgent } from './services/agents/designer-agent';
import { IntentEngineerAgent } from './services/agents/developer-agent';
import { BusinessAnalystAgent } from './services/agents/ba-agent';
import { MarketerAgent } from './services/agents/marketer-agent';
import { DataAnalystAgent } from './services/agents/data-analyst-agent';
import { OptimizerAgent } from './services/agents/optimizer-agent';
import { QaAgent } from './services/agents/qa-agent';
import { SecurityAgent } from './services/agents/security-agent';

dotenv.config();

// Register MAS Agents
orchestrator.registerAgent(new RouterAgent());
orchestrator.registerAgent(new ProductOwnerAgent());
orchestrator.registerAgent(new BusinessAnalystAgent());
orchestrator.registerAgent(new MarketerAgent());
orchestrator.registerAgent(new ArchitectAgent());
orchestrator.registerAgent(new DesignerAgent());
orchestrator.registerAgent(new IntentEngineerAgent());
orchestrator.registerAgent(new DataAnalystAgent());
orchestrator.registerAgent(new OptimizerAgent());
orchestrator.registerAgent(new QaAgent());
orchestrator.registerAgent(new SecurityAgent());

const sessions = new Map<string, AgentState>();

const app = express();
const httpServer = createServer(app);
const PORT = process.env.PORT || 3001;

// Socket.io Setup
export const io = new Server(httpServer, {
    cors: {
        origin: "http://localhost:3000", // Allow Next.js frontend
        methods: ["GET", "POST"]
    }
});

// Middleware
app.use(cors());
app.use(express.json());

// Basic health check route
app.get('/api/health', (req: Request, res: Response) => {
    res.status(200).json({ status: 'ok', message: 'SOL Orchestrator Backend is running' });
});

// Test LLM endpoint
app.get('/api/llm/test', async (req: Request, res: Response): Promise<void> => {
    try {
        const prompt = "Please say exactly: 'Hello, SOL Orchestrator! Gemini is connected.'";
        console.log(`Sending test prompt to Gemini 3.1 Flash: "${prompt}"`);
        const result = await runFlashAgent(prompt);
        res.status(200).json({ status: 'ok', llm_response: result });
    } catch (error: any) {
        console.error("LLM Test Error:", error);
        res.status(500).json({ status: 'error', message: error.message });
    }
});

// Socket.io Connection Handler
io.on('connection', (socket) => {
    console.log(`[socket]: User connected: ${socket.id}`);

    socket.on('disconnect', () => {
        console.log(`[socket]: User disconnected: ${socket.id}`);
    });

    // Listen for session load
    socket.on('load_session', async ({ sessionId }) => {
        console.log(`[socket]: Loading session: ${sessionId}`);
        if (!sessionId) return;

        const state = await getSession(sessionId);
        if (state) {
            socket.emit('session_loaded', {
                messages: state.messages || [],
                artifacts: state.artifacts || {},
                tasks: state.tasks || []
            });
            sessions.set(sessionId, state); // Cache in memory
        }
    });

    // Listen for pause session
    socket.on('pause_session', async ({ sessionId }) => {
        console.log(`[socket]: Pausing session: ${sessionId}`);
        if (!sessionId) return;

        const state = sessions.get(sessionId);
        if (state) {
            state.isPaused = true;
            // Await user approval so the UI knows we are done thinking
            state.awaitingUserApproval = true;
            sessions.set(sessionId, state);
            await saveSession(sessionId, state);
            socket.emit('session_paused');
        }
    });

    // Listen for manual task creation
    socket.on('create_manual_task', async (data) => {
        console.log(`[socket]: Manually creating task in project: ${data.projectId}`);
        const sessionId = data.projectId; // Assuming 1:1 mapping mapping project ID to session ID for now

        if (!sessionId) return;

        let state = sessions.get(sessionId);
        if (!state) {
            const dbState = await getSession(sessionId);
            if (dbState) {
                state = dbState;
            } else {
                return; // Nothing to attach the task to
            }
        }

        // Find existing project name or fallback to a default
        const projectName = "Manual Task";
        const master = new TaskMaster(state as AgentState, sessionId, projectName);

        master.addTask(
            data.title,
            data.description || '',
            data.type || 'Task',
            'User', // Author is user for manual tasks
            data.assignees || []
        );

        sessions.set(sessionId, state as AgentState);
        await saveSession(sessionId, state as AgentState);
    });

    // Listen for task updates from UI
    socket.on('update_task', async (data: { projectId: string; taskId: string; updates: Partial<import('./services/orchestrator').Task> }) => {
        console.log(`[socket]: Updating task ${data.taskId} in project: ${data.projectId}`);
        const sessionId = data.projectId;

        if (!sessionId || !data.taskId) return;

        let state = sessions.get(sessionId);
        if (!state) {
            const dbState = await getSession(sessionId);
            if (dbState) {
                state = dbState;
            } else {
                return;
            }
        }

        const master = new TaskMaster(state as AgentState, sessionId, 'Update');
        const updatedTask = master.updateTask(data.taskId, data.updates);

        if (updatedTask) {
            sessions.set(sessionId, state as AgentState);
            await saveSession(sessionId, state as AgentState);
        }
    });

    // Listen for task deletion from UI
    socket.on('delete_task', async (data: { projectId: string; taskId: string }) => {
        console.log(`[socket]: Deleting task ${data.taskId} in project: ${data.projectId}`);
        const sessionId = data.projectId;

        if (!sessionId || !data.taskId) return;

        let state = sessions.get(sessionId);
        if (!state) {
            const dbState = await getSession(sessionId);
            if (dbState) {
                state = dbState;
            } else {
                return;
            }
        }

        const master = new TaskMaster(state as AgentState, sessionId, 'Delete');
        const deleted = master.deleteTask(data.taskId);

        if (deleted) {
            sessions.set(sessionId, state as AgentState);
            await saveSession(sessionId, state as AgentState);
        }
    });

    // Listen for artifact updates from UI (user editing documents)
    socket.on('update_artifact', async (data: { projectId: string; artifactKey: string; content: string }) => {
        console.log(`[socket]: Updating artifact "${data.artifactKey}" in project: ${data.projectId}`);
        const sessionId = data.projectId;

        if (!sessionId || !data.artifactKey) return;

        let state = sessions.get(sessionId);
        if (!state) {
            const dbState = await getSession(sessionId);
            if (dbState) {
                state = dbState;
            } else {
                return;
            }
        }

        // Update the artifact in state
        if (!state) return;
        (state.artifacts as any)[data.artifactKey] = data.content;
        sessions.set(sessionId, state);
        await saveSession(sessionId, state);

        // Notify all clients about the update
        io.emit('artifact_updated', { artifactKey: data.artifactKey, content: data.content });
        console.log(`[socket]: Artifact "${data.artifactKey}" saved successfully.`);
    });

    // Listen for agent message deletion from UI
    socket.on('delete_message', async (data: { sessionId: string; messageId: string }) => {
        console.log(`[socket]: Deleting message ${data.messageId} in session: ${data.sessionId}`);
        const { sessionId, messageId } = data;

        if (!sessionId || !messageId) return;

        let state = sessions.get(sessionId);
        if (!state) {
            const dbState = await getSession(sessionId);
            if (dbState) {
                state = dbState;
            } else {
                return;
            }
        }

        // Filter out the deleted message
        const originalLength = (state as AgentState).messages.length;
        (state as AgentState).messages = (state as AgentState).messages.filter(msg => msg.id !== messageId);

        // If a message was actually removed, save the new state
        if ((state as AgentState).messages.length < originalLength) {
            sessions.set(sessionId, state as AgentState);
            await saveSession(sessionId, state as AgentState);
            socket.emit('message_deleted', { messageId }); // Optional acknowledgment
            console.log(`[socket]: Message ${messageId} deleted successfully.`);
        }
    });

    // Listen for a direct message from UI
    // Map roles to display names for typing indicator
    const roleToAgent: Record<string, string> = {
        router: 'Router', po: 'Anna (PO)', ba: 'Ben (Business Analyst)',
        marketer: 'Mia (Marketer)', designer: 'Sophie (Designer)', architect: 'Leo (Architect)',
        developer: 'Max (Developer)', data_analyst: 'Ben (Data Analyst)',
        optimizer: 'Diana (Optimizer)', qa: 'Eve (QA)', security: 'Trent (Security)'
    };

    socket.on('send_message', async (data) => {
        console.log(`[socket]: Received message from ${socket.id}`, data.content);

        // Send an immediate acknowledgment
        socket.emit('message_received', { status: 'thinking', agentName: 'Anna (PO)' });

        try {
            const sessionId = data.sessionId || socket.id;

            // Get state from memory cache first
            let state = sessions.get(sessionId);

            // If not in memory, try DB
            if (!state) {
                const dbState = await getSession(sessionId);
                if (dbState) {
                    state = dbState;
                }
            }

            // If still no state, initialize fresh
            if (!state) {
                state = {
                    currentRole: 'router',
                    messages: [],
                    artifacts: {},
                    tasks: [],
                    awaitingUserApproval: false
                };
            }

            const userMessage = {
                id: crypto.randomUUID(),
                role: 'user' as const,
                content: data.content,
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            };

            // Run the state machine with a callback to stream updates
            const newState = await orchestrator.processMessage(
                state,
                userMessage,
                (incrementalState) => {
                    // Get the last message generated by this specific agent
                    const latestMsg = incrementalState.messages[incrementalState.messages.length - 1];
                    if (latestMsg && latestMsg.role === 'assistant') {
                        socket.emit('agent_response', {
                            ...latestMsg,
                            artifacts: incrementalState.artifacts,
                            tasks: incrementalState.tasks || []
                        });
                        // Tell UI we are "thinking" again if the chain continues
                        if (!incrementalState.awaitingUserApproval) {
                            const nextAgentName = roleToAgent[incrementalState.currentRole] || 'AI Team';
                            socket.emit('message_received', { status: 'thinking', agentName: nextAgentName });
                        }
                    }
                }
            );

            sessions.set(sessionId, newState);
            await saveSession(sessionId, newState); // Persist to DB

            // If the loop finished but no assistant messages were ever generated (fallback)
            const finalMsg = newState.messages[newState.messages.length - 1];
            if (!finalMsg || finalMsg.role !== 'assistant') {
                socket.emit('agent_response', {
                    id: crypto.randomUUID(),
                    role: 'assistant',
                    agentName: 'System',
                    content: 'Processed successfully.',
                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                    artifacts: newState.artifacts
                });
            }
        } catch (error) {
            console.error("[socket] Error calling MAS Orchestrator:", error);
            socket.emit('error', { message: 'Failed to process AI request' });
        }
    });

    // ── Init project directory on disk ──
    socket.on('init_project_dir', async (data: { projectId: string; projectName: string; description?: string; localPath: string }) => {
        const { projectId, projectName, description, localPath } = data;
        try {
            const projectDir = path.join(localPath, projectName.replace(/[<>:"/\\|?*]/g, '_'));

            // Create folder structure
            fs.mkdirSync(path.join(projectDir, 'docs'), { recursive: true });
            fs.mkdirSync(path.join(projectDir, 'src'), { recursive: true });

            // README.md
            const readme = `# ${projectName}\n\n${description || 'Project created by SOL IDE.'}\n\n---\n*Generated by SOL AI-Native IDE*\n`;
            fs.writeFileSync(path.join(projectDir, 'README.md'), readme, 'utf-8');

            // docs placeholders
            fs.writeFileSync(path.join(projectDir, 'docs', 'prd.md'), `# PRD — ${projectName}\n\n> Auto-generated placeholder. Will be filled by AI Team.\n`, 'utf-8');
            fs.writeFileSync(path.join(projectDir, 'docs', 'architecture.md'), `# Architecture — ${projectName}\n\n> Auto-generated placeholder. Will be filled by AI Team.\n`, 'utf-8');

            console.log(`[init_project_dir] Created project structure at: ${projectDir}`);
            socket.emit('project_dir_ready', { projectId, path: projectDir });
        } catch (err: any) {
            console.error('[init_project_dir] Error:', err);
            socket.emit('project_dir_error', { projectId, message: err.message || 'Failed to create project directory' });
        }
    });

    // ── Agent Profiles & Registry ──
    socket.on('get_agents', async () => {
        try {
            console.log(`[socket]: Fetching all agents for ${socket.id}`);
            // Force memory to sync with DB if needed
            const dbProfiles = await getAllAgentProfiles();
            dbProfiles.forEach(p => agentRegistry.updateProfile(p.id, p));
            socket.emit('agents_list', agentRegistry.getAllProfiles());
        } catch (e: any) {
            console.error('[socket] get_agents error:', e);
            socket.emit('error', { message: 'Failed to fetch agent profiles' });
        }
    });

    socket.on('get_agent_profile', async ({ agentId }) => {
        try {
            console.log(`[socket]: Fetching agent profile ${agentId} for ${socket.id}`);
            let profile = agentRegistry.getProfile(agentId);
            const dbProfile = await getAgentProfile(agentId);

            if (dbProfile) {
                profile = agentRegistry.updateProfile(agentId, dbProfile);
            }

            if (profile) {
                socket.emit('agent_profile', profile);
            } else {
                socket.emit('error', { message: `Agent profile ${agentId} not found` });
            }
        } catch (e: any) {
            console.error(`[socket] get_agent_profile error for ${agentId}:`, e);
            socket.emit('error', { message: 'Failed to fetch agent profile details' });
        }
    });

    socket.on('update_agent_profile', async ({ agentId, updates }) => {
        try {
            console.log(`[socket]: Updating agent profile ${agentId}`);
            let profile = agentRegistry.getProfile(agentId);

            if (profile) {
                // Update in memory (handles versioning of prompts)
                const updated = agentRegistry.updateProfile(agentId, updates);
                if (updated) {
                    // Persist to LanceDB
                    await saveAgentProfile(agentId, updated);
                    socket.emit('agent_profile_updated', updated);

                    // Broadcast updated list to others just in case name/role changed
                    io.emit('agents_list', agentRegistry.getAllProfiles());
                }
            } else {
                socket.emit('error', { message: `Agent profile ${agentId} not found for update` });
            }
        } catch (e: any) {
            console.error(`[socket] update_agent_profile error for ${agentId}:`, e);
            socket.emit('error', { message: 'Failed to update agent profile' });
        }
    });

    // ── Direct Agent Chat (Bypassing Router but hooked to LLM) ──
    socket.on('send_direct_message', async (data: { agentId: string, content: string }) => {
        try {
            console.log(`[socket]: Direct message to ${data.agentId} from ${socket.id}`);
            const profile = agentRegistry.getProfile(data.agentId);

            if (!profile) {
                socket.emit('error', { message: `Agent ${data.agentId} not found` });
                return;
            }

            // Acknowledge receipt
            socket.emit('direct_agent_response', {
                id: 'typing_' + crypto.randomUUID(),
                role: 'assistant',
                agentName: profile.name,
                content: '',
                status: 'thinking'
            });

            // For now, construct a direct prompt combined with the agent's profile system prompt
            const fullPrompt = `${profile.systemPrompt}\n\nUser Message: ${data.content}`;

            // Run the LLM directly through runProAgent or runFlashAgent based on tier or availability. Using Flash for speed/chat.
            const result = await runFlashAgent(fullPrompt);

            // Send back the direct response
            socket.emit('direct_agent_response', {
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: profile.name,
                content: result,
                status: 'done',
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });

        } catch (e: any) {
            console.error(`[socket] send_direct_message error for ${data.agentId}:`, e);
            socket.emit('error', { message: 'Failed to process direct agent message' });
            socket.emit('direct_agent_response', { status: 'error' }); // Clear typing status
        }
    });
});

// Start server
httpServer.listen(PORT, async () => {
    console.log(`[server]: SOL Orchestrator is running at http://localhost:${PORT}`);

    // Initialize LanceDB embedded database
    try {
        await initializeCollections();
    } catch (e) {
        console.error('[db]: Error initializing LanceDB:', e);
    }
});
