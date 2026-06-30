import { AgentNode, AgentState, Role } from '../orchestrator';
import { runFlashAgent } from '../ai';
import { agentRegistry } from '../agent-registry';

export class RouterAgent implements AgentNode {
    name = 'System Router';
    role: Role = 'router';

    async execute(state: AgentState): Promise<AgentState> {
        console.log(`[router]: Analyzing intent...`);
        const lastMessage = state.messages[state.messages.length - 1];

        // If the conversation is empty or the last message isn't from the user, we fallback.
        if (!lastMessage || lastMessage.role !== 'user') {
            state.currentRole = 'po';
            state.awaitingUserApproval = false;
            return state;
        }

        const profile = agentRegistry.getProfile(this.role);
        const systemPrompt = profile ? profile.systemPrompt : `You are the SOL_CEO (Router Agent) for a multi-agent AI IDE.
Your job is to read the user's latest message and the current project state, classify the intent into one of 3 Tiers, and decide which specialized agent should handle it next.

Tiers of Complexity:
- "simple" (Tier 1): Quick tasks, single-file scripts, bug fixes. Route to "developer" or "designer".
- "standard" (Tier 2): New features, system architecture planning. Route to "architect" or "designer".
- "commercial" (Tier 3): Full applications, business ideas, startups. Route to "po".`;

        // Construct a prompt for Intent Classification
        const prompt = `
    ${systemPrompt}

    Available Agents to route to:
    - "po" (Product Owner): For Commercial/Startup ideas (Tier 3). Gathers requirements, creates PRD.md, discusses target audience.
    - "architect" (System Architect): For Standard tasks (Tier 2) or architecture decisions, selecting tech stack, generating Architecture.md.
    - "designer" (UI/UX Designer): For visual appearance, layouts, Design_System.md.
    - "developer" (Lead Intent Engineer): For Simple tasks (Tier 1), writing code, fixing bugs, or executing tasks.

    Current Project Artifacts:
    PRD exists: ${!!state.artifacts.prd}
    Architecture exists: ${!!state.artifacts.architecture}
    Design System exists: ${!!state.artifacts.designSystem}

    User's latest message: "${lastMessage.content}"

    Respond ONLY with a valid JSON object in this exact format, with no markdown formatting or extra text:
    {
      "tier": "simple" | "standard" | "commercial",
      "selected_agent": "po" | "architect" | "designer" | "developer",
      "reasoning": "brief explanation for the choice"
    }
    `;

        try {
            const response = await runFlashAgent(prompt);

            // Clean up markdown formatting if the LLM included it by mistake
            const cleanJson = response.replace(/^\`\`\`json/gm, '').replace(/^\`\`\`/gm, '').trim();
            const parsed = JSON.parse(cleanJson);

            const targetRole = parsed.selected_agent as Role;
            const tier = parsed.tier || 'unknown';
            console.log(`[router]: Intent classified. Tier: [${tier}]. Routing to -> ${targetRole} (Reason: ${parsed.reasoning})`);

            // Update state to pass the baton
            state.currentRole = targetRole;
            state.awaitingUserApproval = false; // Immediately let the next agent run

        } catch (e) {
            console.error("[router]: Failed to parse intent from LLM. Defaulting to PO.", e);
            state.currentRole = 'po';
            state.awaitingUserApproval = false;
        }

        return state;
    }
}
