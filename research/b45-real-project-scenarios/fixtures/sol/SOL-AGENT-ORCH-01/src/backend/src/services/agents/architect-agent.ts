import { AgentNode, AgentState, Role, getAgentSystemInstructions } from '../orchestrator';
import { runProAgent } from '../ai';
import { ToolDispatcher } from '../tools/dispatcher';
import { agentRegistry } from '../agent-registry';

export class ArchitectAgent implements AgentNode {
    name = 'Leo (Architect)';
    role: Role = 'architect';

    // Builds the architecture-stage prompt from prior artifacts and either asks for missing constraints or hands a completed architecture to the developer role.
    async execute(state: AgentState): Promise<AgentState> {
        console.log(`[architect]: Executing System Architect logic...`);

        // Format conversation history for the prompt
        const history = state.messages.map(m => `${m.role.toUpperCase()}: ${m.content}`).join('\n');

        // Gather artifacts context
        let artifactsContext = '';
        if (state.artifacts.prd) {
            artifactsContext += `Product Requirements Document (PRD):\n${state.artifacts.prd}\n\n`;
        } else {
            artifactsContext += `No PRD is available. (This is unusual, as I usually come after the PO).\n\n`;
        }

        if (state.artifacts.designSystem) {
            artifactsContext += `Design System:\n${state.artifacts.designSystem}\n\n`;
        }

        const profile = agentRegistry.getProfile(this.role);
        const systemPrompt = profile ? profile.systemPrompt : `You are Leo, the expert System Architect Agent in the SOL AI-Native IDE.
You use 'architecture' and 'architecture-patterns' skills. Your goal is to design the technical architecture for the user's project based on the PRD.
Our core philosophy is MVP-FIRST and pragmatic development. You must design the architecture to be as simple as possible to reach the market quickly and secure the first payment.`;

        const prompt = `
    ${systemPrompt}
    
    Project Context (Artifacts):
    ${artifactsContext}

    Conversation History:
    ${history}

    INSTRUCTIONS:
    Analyze the PRD and User History. 
    1. If the technical constraints are unclear, ask EXACTLY ONE clarifying technical question.
    2. If you have enough information, set status to "architecture_ready" and generate a comprehensive 'Architecture.md' document.
    3. CRITICAL: Propose a simple, fast-to-market stack (e.g., Next.js, BaaS like Supabase/Firebase, easy payment integrations like Stripe). Explicitly avoid premature optimization or complex microservices for the v1/MVP unless strictly demanded by the PRD.

    Your 'Architecture.md' should include:
    - Chosen Tech Stack (Frontend, Backend, Database)
    - Monetization/BaaS Infrastructure (e.g., Stripe)
    - High-level Diagram description or Structure
    - Primary Data Models (Schema concepts)
    - Key architectural decisions focusing on time-to-market

    ${getAgentSystemInstructions(state)}

    You must adhere to the 4-Step Universal Principle.
    Respond ONLY with a valid JSON object in the text output. No markdown wrapping.
    
    {
      "philosophy": "Identify the core problem or intent.",
      "logic": "Determine the optimal approach or rules to apply.",
      "strategy": "Plan the step-by-step resolution based on the logic.",
      "execution": {
          "status": "question" | "architecture_ready",
          "reply": "Your message to the user explaining your technical choices or asking a question",
          "architecture_content": "If status is architecture_ready, output the full Markdown Architecture doc here. Otherwise, leave empty string."
      }
    }
    `;

        try {
            const responseText = await runProAgent(prompt);

            const cleanJson = responseText.replace(/^```json/gm, '').replace(/^```/gm, '').trim();
            const parsed = JSON.parse(cleanJson);

            console.log(`[architect] Philosophy: ${parsed.philosophy}`);
            console.log(`[architect] Logic: ${parsed.logic}`);
            console.log(`[architect] Strategy: ${parsed.strategy}`);

            const execution = parsed.execution || {};

            // Save Architect's reply to chat
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Leo (Architect)',
                content: execution.reply || "Thinking...",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });

            if (execution.status === 'architecture_ready' && execution.architecture_content) {
                console.log(`[architect]: Architecture Generated! Passing control to Developer...`);
                state.artifacts.architecture = execution.architecture_content;

                // Pass baton to the developer to start splitting tasks
                state.currentRole = 'developer';
                state.awaitingUserApproval = false;
            } else {
                // Still discovering technical requirements. Wait for user reply.
                console.log(`[architect]: Asking technical question...`);
                state.awaitingUserApproval = true;
            }

        } catch (e) {
            console.error("[architect]: Failed to parse Architect response", e);
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Leo (Architect)',
                content: "I'm crunching the numbers on the best tech stack for this, but I need a moment. Do you have any preference between SQL and NoSQL?",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
            state.awaitingUserApproval = true;
        }

        return state;
    }
}
