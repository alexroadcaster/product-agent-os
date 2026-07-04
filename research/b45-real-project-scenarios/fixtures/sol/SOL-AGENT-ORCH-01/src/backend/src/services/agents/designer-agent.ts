import { AgentNode, AgentState, Role, getAgentSystemInstructions } from '../orchestrator';
import { runProAgent } from '../ai';
import { ToolDispatcher } from '../tools/dispatcher';
import { agentRegistry } from '../agent-registry';

export class DesignerAgent implements AgentNode {
    name = 'Sophie (Designer)';
    role: Role = 'designer';

    // Converts current product context into design guidance while preserving the one-question fallback for missing style direction.
    async execute(state: AgentState): Promise<AgentState> {
        console.log(`[designer]: Executing Designer logic...`);

        const history = state.messages.map(m => `${m.role.toUpperCase()}: ${m.content}`).join('\n');
        const prdContext = state.artifacts.prd ? `Existing PRD:\n${state.artifacts.prd}` : 'No PRD available yet.';

        const profile = agentRegistry.getProfile(this.role);
        const systemPrompt = profile ? profile.systemPrompt : `You are Sophie, the expert UI/UX Designer Agent (Trust Designer) in the SOL AI-Native IDE.
You use the 'ui-ux-pro-max' skill. You focus on accessibility (CRITICAL), touch & interaction, performance, layout, typography, color, and most importantly, CONVERSION and TRUST.
Our core philosophy is MVP-FIRST and reaching the first user payment quickly.`;

        const prompt = `
    ${systemPrompt}

    Current Project State:
    ${prdContext}

    Conversation History:
    ${history}

    INSTRUCTIONS:
    1. If the user is asking a specific design question, answer it professionally.
    2. If the user wants you to create the design system, generate a comprehensive Design_System.md covering colors, typography, component styles, and accessibility.
    3. CRITICAL: Optimize the design for the fastest path to the core value and the payment/checkout flow. Do not over-design non-essential screens for the first version. Focus on building user trust to facilitate the first payment.
    4. If you need more info to choose a style (e.g. "Do you prefer dark mode or light mode? minimal or playful?"), ask ONE clarifying question.

    ${getAgentSystemInstructions(state)}

    You must adhere to the 4-Step Universal Principle.
    Respond ONLY with a valid JSON object in the text output. No markdown wrapping.
    
    {
      "philosophy": "Identify the core problem or intent.",
      "logic": "Determine the optimal approach or rules to apply.",
      "strategy": "Plan the step-by-step resolution based on the logic.",
      "execution": {
          "status": "question" | "design_system_ready",
          "reply": "Your message to the user explaining your design choices or asking a question",
          "design_system_content": "If status is design_system_ready, output the full Markdown Design_System.md here. Otherwise, leave empty string."
      }
    }
    `;

        try {
            const responseText = await runProAgent(prompt);

            const cleanJson = responseText.replace(/^```json/gm, '').replace(/^```/gm, '').trim();
            const parsed = JSON.parse(cleanJson);

            console.log(`[designer] Philosophy: ${parsed.philosophy}`);
            console.log(`[designer] Logic: ${parsed.logic}`);
            console.log(`[designer] Strategy: ${parsed.strategy}`);

            const execution = parsed.execution || {};

            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Sophie (Designer)',
                content: execution.reply || "Thinking...",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });

            if (execution.status === 'design_system_ready' && execution.design_system_content) {
                console.log(`[designer]: Design System Generated!`);
                state.artifacts.designSystem = execution.design_system_content;

                // Pass baton to the Architect to design the technical architecture
                state.currentRole = 'architect';
                state.awaitingUserApproval = false;
            } else {
                console.log(`[designer]: Asking design question...`);
                state.awaitingUserApproval = true;
            }

        } catch (e) {
            console.error("[designer]: Failed to parse Designer response", e);
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Sophie (Designer)',
                content: "I'm currently visualizing some UI concepts. Could you tell me if you have any color preferences?",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
            state.awaitingUserApproval = true;
        }

        return state;
    }
}
