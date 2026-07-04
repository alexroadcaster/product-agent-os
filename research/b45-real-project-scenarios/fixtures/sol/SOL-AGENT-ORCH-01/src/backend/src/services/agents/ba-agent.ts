import { AgentNode, AgentState, Role, getAgentSystemInstructions } from '../orchestrator';
import { runProAgent } from '../ai';
import { ToolDispatcher } from '../tools/dispatcher';
import { agentRegistry } from '../agent-registry';

export class BusinessAnalystAgent implements AgentNode {
    name = 'Ben (Business Analyst)';
    role: Role = 'ba';

    // Turns the PRD and conversation history into market-research output, or routes back to the PO when the prerequisite PRD is absent.
    async execute(state: AgentState): Promise<AgentState> {
        console.log(`[ba]: Executing Business Analyst logic...`);

        const history = state.messages.map(m => `${m.role.toUpperCase()}: ${m.content}`).join('\n');

        // This agent requires PRD to proceed. If missing, it should ask the PO to do it.
        if (!state.artifacts.prd) {
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Ben (Business Analyst)',
                content: "Hey Anna (PO), I need the PRD before I can conduct the Market Research. Could you provide that first?",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
            state.currentRole = 'po';
            state.awaitingUserApproval = false;
            return state;
        }

        const profile = agentRegistry.getProfile(this.role);
        const systemPrompt = profile ? profile.systemPrompt : `You are Ben, the expert Business Analyst Agent in the SOL AI-Native IDE.
You use the 'market-research' mindset. Your goal is to analyze the Product Requirements Document (PRD), identify the Target Addressable Market (TAM), define the business model, and analyze the competitive landscape.`;

        const prompt = `
    ${systemPrompt}

    Project Context (PRD):
    ${state.artifacts.prd}

    Conversation History:
    ${history}

    INSTRUCTIONS:
    Analyze the PRD and user history. 
    1. If the business model (e.g., B2B vs B2C, subscription vs one-time) or target market is entirely unclear from the PRD, ask EXACTLY ONE clarifying question to the user.
    2. If you have enough information to define the market, set status to "research_ready" and generate a comprehensive 'Market_Research.md' document.

    Your 'Market_Research.md' should include:
    - Target Audience & User Personas
    - Value Proposition
    - Core Business Model & Revenue Streams
    - Competitive Landscape (Direct & Indirect Competitors)
    - SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)

    ${getAgentSystemInstructions(state)}

    You must adhere to the 4-Step Universal Principle.
    Respond ONLY with a valid JSON object in the text output. No markdown wrapping.
    
    {
      "philosophy": "Identify the core problem or intent.",
      "logic": "Determine the optimal approach or rules to apply.",
      "strategy": "Plan the step-by-step resolution based on the logic.",
      "execution": {
          "status": "question" | "research_ready",
          "reply": "Your message to the user explaining your analysis or asking a question",
          "research_content": "If status is research_ready, output the full Markdown Market_Research.md here. Otherwise, leave empty string."
      }
    }
    `;

        try {
            const responseText = await runProAgent(prompt);

            const cleanJson = responseText.replace(/^```json/gm, '').replace(/^```/gm, '').trim();
            const parsed = JSON.parse(cleanJson);

            console.log(`[ba] Philosophy: ${parsed.philosophy}`);
            console.log(`[ba] Logic: ${parsed.logic}`);
            console.log(`[ba] Strategy: ${parsed.strategy}`);

            const execution = parsed.execution || {};

            // Save BA's reply to chat
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Ben (Business Analyst)',
                content: execution.reply || "Thinking about the market...",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });

            if (execution.status === 'research_ready' && execution.research_content) {
                console.log(`[ba]: Market Research Generated! Passing control to Marketer...`);
                state.artifacts.marketResearch = execution.research_content;

                // Pass baton to the Marketer to create the GTM strategy
                state.currentRole = 'marketer';
                state.awaitingUserApproval = false;
            } else {
                // Still discovering business requirements. Wait for user reply.
                console.log(`[ba]: Asking business question...`);
                state.awaitingUserApproval = true;
            }

        } catch (e) {
            console.error("[ba]: Failed to parse Business Analyst response", e);
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Ben (Business Analyst)',
                content: "I'm crunching the market numbers, but I need a moment. Do you have a specific monetization model in mind?",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
            state.awaitingUserApproval = true;
        }

        return state;
    }
}
