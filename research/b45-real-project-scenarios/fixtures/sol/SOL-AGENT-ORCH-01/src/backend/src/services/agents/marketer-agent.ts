import { AgentNode, AgentState, Role, getAgentSystemInstructions } from '../orchestrator';
import { runProAgent } from '../ai';
import { ToolDispatcher } from '../tools/dispatcher';
import { agentRegistry } from '../agent-registry';

export class MarketerAgent implements AgentNode {
    name = 'Mia (Marketer)';
    role: Role = 'marketer';

    async execute(state: AgentState): Promise<AgentState> {
        console.log(`[marketer]: Executing Marketer logic...`);

        const history = state.messages.map(m => `${m.role.toUpperCase()}: ${m.content}`).join('\n');

        let artifactsContext = '';
        if (state.artifacts.prd) artifactsContext += `Product Requirements Document (PRD):\n${state.artifacts.prd}\n\n`;
        if (state.artifacts.marketResearch) artifactsContext += `Market Research:\n${state.artifacts.marketResearch}\n\n`;

        // This agent requires PRD and Market Research to proceed.
        if (!state.artifacts.marketResearch || !state.artifacts.prd) {
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Mia (Marketer)',
                content: "Hey Ben (BA), I need the Market Research and PRD before I can build the Go-To-Market strategy. Could you provide those first?",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
            state.currentRole = 'ba';
            state.awaitingUserApproval = false;
            return state;
        }

        const profile = agentRegistry.getProfile(this.role);
        const systemPrompt = profile ? profile.systemPrompt : `You are Mia, the expert Marketer Agent in the SOL AI-Native IDE.
You use the 'gtm-strategy' mindset. Your goal is to analyze the PRD and Market Research, and create a comprehensive Go-To-Market (GTM) Strategy. Our core philosophy is MVP-FIRST and reaching the FIRST PAYMENT as quickly as possible.`;

        const prompt = `
    ${systemPrompt}

    Project Context (Artifacts):
    ${artifactsContext}

    Conversation History:
    ${history}

    INSTRUCTIONS:
    Analyze the PRD and Market Research. 
    1. If you are entirely unsure about the primary launch channel or marketing budget, ask EXACTLY ONE clarifying question.
    2. Otherwise, set status to "gtm_ready" and generate a comprehensive 'GTM_Strategy.md' document.

    Your 'GTM_Strategy.md' should include:
    - Launch Strategy (Phases, Soft Launch vs Hard Launch)
    - Positioning & Key Messaging
    - Core Acquisition Channels (e.g., SEO, Content, Ads, Influencers)
    - Path to First 100 Paying Customers
    - Success Metrics (KPIs, Conversion Rates)

    ${getAgentSystemInstructions(state)}

    You must adhere to the 4-Step Universal Principle.
    Respond ONLY with a valid JSON object in the text output. No markdown wrapping.
    
    {
      "philosophy": "Identify the core problem or intent.",
      "logic": "Determine the optimal approach or rules to apply.",
      "strategy": "Plan the step-by-step resolution based on the logic.",
      "execution": {
          "status": "question" | "gtm_ready",
          "reply": "Your message to the user explaining your marketing choices or asking a question",
          "gtm_content": "If status is gtm_ready, output the full Markdown GTM_Strategy.md here. Otherwise, leave empty string."
      }
    }
    `;

        try {
            const responseText = await runProAgent(prompt);

            const cleanJson = responseText.replace(/^```json/gm, '').replace(/^```/gm, '').trim();
            const parsed = JSON.parse(cleanJson);

            console.log(`[marketer] Philosophy: ${parsed.philosophy}`);
            console.log(`[marketer] Logic: ${parsed.logic}`);
            console.log(`[marketer] Strategy: ${parsed.strategy}`);

            const execution = parsed.execution || {};

            // Save Marketer's reply to chat
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Mia (Marketer)',
                content: execution.reply || "Drafting the launch plan...",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });

            if (execution.status === 'gtm_ready' && execution.gtm_content) {
                console.log(`[marketer]: GTM Strategy Generated! Passing control to Designer/Architect...`);
                state.artifacts.gtmStrategy = execution.gtm_content;

                // Pass baton to the Designer or Architect to start building the app visually/technically.
                // We'll pass it to Designer first, as they govern the visual feel.
                state.currentRole = 'designer';
                state.awaitingUserApproval = false;
            } else {
                // Still discovering. Wait for user reply.
                console.log(`[marketer]: Asking marketing question...`);
                state.awaitingUserApproval = true;
            }

        } catch (e) {
            console.error("[marketer]: Failed to parse Marketer response", e);
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Mia (Marketer)',
                content: "I'm figuring out the best channels, but need a second. Do we have any marketing budget for the initial launch?",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
            state.awaitingUserApproval = true;
        }

        return state;
    }
}
