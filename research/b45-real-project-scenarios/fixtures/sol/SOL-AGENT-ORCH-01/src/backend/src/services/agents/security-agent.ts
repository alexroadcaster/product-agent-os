import { AgentNode, AgentState, getAgentSystemInstructions } from '../orchestrator';
import { runProAgent } from '../ai';
import { ToolDispatcher } from '../tools/dispatcher';
import { agentRegistry } from '../agent-registry';

export class SecurityAgent implements AgentNode {
    name = 'Trent (Lead Security Auditor)';
    role = 'security' as const;

    async execute(state: AgentState): Promise<AgentState> {
        const userMessage = state.messages.find(m => m.role === 'user')?.content || '';
        const architecture = state.artifacts.architecture || '';
        const tasks = state.tasks || [];

        const profile = agentRegistry.getProfile(this.role);
        const systemPrompt = profile ? profile.systemPrompt : `You are Trent, the Lead Security Auditor (Red Teamer) for the SOL ecosystem.
You operate on a strict 4-Step Universal Principle: Philosophy, Logic, Strategy, Execution.

[Philosophy]: "Paranoia is a virtue." Assume the system is under constant attack. You must protect user data at all costs.
[Logic]: We act as a Red Teamer. We analyze the Architecture, Database Plan, and Tasks for OWASP Top 10 vulnerabilities (Injection, Broken Auth, XSS, SSRF, etc.).
[Strategy]: Formulate a "Security Audit & Hardening Plan". Assume we need to sanitize all inputs, use prepared SQL statements, protect against IDOR, and implement rate limiting.`;

        const prompt = `
    ${systemPrompt}
    
    ${getAgentSystemInstructions(state)}

    [Execution]:
    Output ONLY a valid JSON object in the text output. No markdown wrapping.

    {
      "philosophy": "Statement of your core belief regarding threat modeling and system defense",
      "logic": "Step-by-step reasoning on potential attack vectors and vulnerabilities",
      "strategy": "Actionable security hardening plan and audit checks",
      "execution": {
        "reply": "A concise message explaining your audit results. Conclude that the Phase 3 planning is now complete and await user approval to proceed to Phase 4.",
        "securityPlan": "Detailed markdown string containing your Threat Model, OWASP Top 10 checklist, and specific hardening rules for the worker agents."
      }
    }

    Context:
    Architecture & Plans so far:
    ${architecture}

    Tasks planned:
    ${JSON.stringify(tasks, null, 2)}
    `;

        try {
            const responseText = await runProAgent(prompt);

            const cleanJson = responseText.replace(/^```json/gm, '').replace(/^```/gm, '').trim();
            const parsed = JSON.parse(cleanJson);

            console.log(`[security] Philosophy: ${parsed.philosophy}`);
            console.log(`[security] Logic: ${parsed.logic}`);
            console.log(`[security] Strategy: ${parsed.strategy}`);

            const execution = parsed.execution || {};

            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Trent (Lead Security Auditor)',
                content: execution.reply || "Thinking about threat models...",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });

            if (execution.securityPlan) {
                state.artifacts = state.artifacts || {};
                state.artifacts.securityPlan = execution.securityPlan;
            }

            console.log(`[security]: Planning Phase Complete. Handing control back to User.`);

            // End of the chain, wait for user
            state.awaitingUserApproval = true;

        } catch (e) {
            console.error("[security] Failed to process:", e);
            state.messages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                agentName: 'Trent (Lead Security Auditor)',
                content: "I encountered an error during the security audit. Please check my logs.",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            });
            state.awaitingUserApproval = true;
        }

        return state;
    }
}
