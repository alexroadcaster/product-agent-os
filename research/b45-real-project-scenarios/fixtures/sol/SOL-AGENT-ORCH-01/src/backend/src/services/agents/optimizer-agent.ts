import { AgentNode, AgentState, getAgentSystemInstructions } from '../orchestrator';
import { runProAgent } from '../ai';
import { ToolDispatcher } from '../tools/dispatcher';
import { agentRegistry } from '../agent-registry';

export class OptimizerAgent implements AgentNode {
    name = 'Diana (Lead Optimizer)';
    role = 'optimizer' as const;

    async execute(state: AgentState): Promise<AgentState> {
        const userMessage = state.messages.find(m => m.role === 'user')?.content || '';
        const architecture = state.artifacts.architecture || '';

        const profile = agentRegistry.getProfile(this.role);
        const systemPrompt = profile ? profile.systemPrompt : `You are Diana, the Lead Optimizer for the SOL ecosystem.
You operate on a strict 4-Step Universal Principle: Philosophy, Logic, Strategy, Execution.

[Philosophy]: "Ruthless efficiency. We eliminate waste in resource utilization, token consumption, and deployment bottlenecks. We do not tolerate slow CI/CD or uncompressed context windows."
[Logic]: We analyze the Architecture and Data Pipeline. We identify where caching is required (e.g., Redis, CDN), where CI/CD can be sped up, and how we can compress the AI memory/tokens in our MAS (Multi-Agent System).
[Strategy]: Formulate a strategy for Token Compression (summarizing older messages instead of passing arrays) and CI/CD optimization.`;

        const prompt = `
    ${systemPrompt}
    
    ${getAgentSystemInstructions(state)}

    [Execution]:
    Output ONLY a valid JSON object in the text output. No markdown wrapping.
    
    {
      "philosophy": "Statement of your core belief regarding system efficiency",
      "logic": "Step-by-step reasoning on bottlenecks and token usage",
      "strategy": "Actionable plan for CI/CD, Caching, and Token Compression",
      "execution": {
        "reply": "A concise message explaining your optimization plan and passing control to QA",
        "optimizationPlan": "Detailed markdown string containing your caching, infrastructure, and token management strategies"
      }
    }

    Context:
    Architecture & Database Plan:
    ${architecture}
    `;

        try {
            const responseText = await runProAgent(prompt);

            const cleanJson = responseText.replace(/^```json/gm, '').replace(/^```/gm, '').trim();
            const parsed = JSON.parse(cleanJson);

            console.log(`[optimizer] Philosophy: ${parsed.philosophy}`);
            console.log(`[optimizer] Logic: ${parsed.logic}`);
            console.log(`[optimizer] Strategy: ${parsed.strategy}`);

            const execution = parsed.execution || {};

            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Diana (Lead Optimizer)',
                content: execution.reply || "Thinking...",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });

            if (execution.optimizationPlan) {
                state.artifacts = state.artifacts || {};
                state.artifacts.optimizationPlan = execution.optimizationPlan;
            }

            console.log(`[optimizer]: Handing off to QA Agent...`);
            // In the future this might go to QA/TESTER, but for now we route to QA
            state.currentRole = 'qa';
            state.awaitingUserApproval = false;

        } catch (e) {
            console.error("[optimizer] Failed to process:", e);
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Diana (Lead Optimizer)',
                content: "I encountered an error analyzing optimization opportunities. Please check my logs.",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
            state.awaitingUserApproval = true;
        }

        return state;
    }
}
