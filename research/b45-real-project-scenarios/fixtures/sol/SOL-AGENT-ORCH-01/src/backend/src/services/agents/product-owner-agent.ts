import { AgentNode, AgentState, Role, getAgentSystemInstructions } from '../orchestrator';
import { runProAgent } from '../ai';
import { ToolDispatcher } from '../tools/dispatcher';
import { agentRegistry } from '../agent-registry';

export class ProductOwnerAgent implements AgentNode {
    name = 'Anna (PO)';
    role: Role = 'po';

    // Converts the user's conversation into either one focused discovery question or a PRD artifact for downstream specialist roles.
    async execute(state: AgentState): Promise<AgentState> {
        console.log(`[po]: Executing Product Owner logic...`);

        // Format conversation history for the prompt
        const history = state.messages.map(m => `${m.role.toUpperCase()}: ${m.content}`).join('\n');

        const profile = agentRegistry.getProfile(this.role);
        const systemPrompt = profile ? profile.systemPrompt : `You are Anna, the expert Product Owner Agent in the SOL AI-Native IDE.
You use the 'product-manager-toolkit' mindset. Your goal is to gather requirements from the user and ultimately output a Product Requirements Document (PRD).

INSTRUCTIONS:
Analyze the conversation history.
1. If the user's idea is too vague, ask EXACTLY ONE clarifying question. Keep your tone friendly, human-like, and professional.
2. If you feel you have enough information to define a basic MVP, set status to "prd_ready" and generate a comprehensive PRD in markdown format.

You must adhere to the 4-Step Universal Principle.`;

        const prompt = `
    ${systemPrompt}

    Conversation History:
    ${history}

    ${getAgentSystemInstructions(state)}

    Respond ONLY with a valid JSON object in the text output. No markdown wrapping.
    
    {
      "philosophy": "Identify the core problem or intent.",
      "logic": "Determine the optimal approach or rules to apply.",
      "strategy": "Plan the step-by-step resolution based on the logic.",
      "execution": {
          "status": "question" | "prd_ready",
          "reply": "Your message to the user",
          "prd_content": "If status is prd_ready, output the full Markdown PRD here. Otherwise, leave empty string."
      }
    }
    `;

        try {
            const responseText = await runProAgent(prompt);

            const cleanJson = responseText.replace(/^```json/gm, '').replace(/^```/gm, '').trim();
            const parsed = JSON.parse(cleanJson);

            console.log(`[po] Philosophy: ${parsed.philosophy}`);
            console.log(`[po] Logic: ${parsed.logic}`);
            console.log(`[po] Strategy: ${parsed.strategy}`);

            const execution = parsed.execution || {};

            // Save PO's reply to chat
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Anna (PO)',
                content: execution.reply || "Thinking...",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });

            if (execution.status === 'prd_ready' && execution.prd_content) {
                console.log(`[po]: PRD Generated! passing control to Business Analyst (BA)...`);
                state.artifacts.prd = execution.prd_content;

                // Passing the baton automatically to the Business Analyst when PRD is ready. 
                // We will NOT await user approval here, we will let the BA read the PRD immediately.
                state.currentRole = 'ba';
                state.awaitingUserApproval = false;
            } else {
                // Still discovering. Wait for user reply.
                console.log(`[po]: Asking question...`);
                state.awaitingUserApproval = true;
            }

        } catch (e) {
            console.error("[po]: Failed to parse PO response", e);
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Anna (PO)',
                content: "I'm having trouble structuring my thoughts right now. Could you please clarify your idea a bit more?",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
            state.awaitingUserApproval = true;
        }

        return state;
    }
}
