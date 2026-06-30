import { GoogleGenAI } from '@google/genai';
import dotenv from 'dotenv';
dotenv.config();

// Initialize GoogleGenAI
const genAIConfig: any = {};
if (process.env.GEMINI_API_KEY) {
    genAIConfig.apiKey = process.env.GEMINI_API_KEY;
} else if (process.env.GOOGLE_CLOUD_PROJECT && process.env.GOOGLE_CLOUD_LOCATION) {
    genAIConfig.vertexai = {
        project: process.env.GOOGLE_CLOUD_PROJECT,
        location: process.env.GOOGLE_CLOUD_LOCATION,
    };
}

const ai = new GoogleGenAI(genAIConfig);

// Retry config
const MAX_RETRIES = 2;
const RETRY_DELAY_MS = 2000;

export interface ToolDeclaration {
    name: string;
    description: string;
    parameters?: any;
}

export interface AgentResponse {
    text: string;
    functionCalls?: any[];
}

/**
 * Helper: delay for exponential backoff
 */
function delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Core generate function with automatic retry + fallback to Flash on 429.
 * On rate limit (429): retries up to MAX_RETRIES times with exponential backoff,
 * then falls back to gemini-2.5-flash as a last resort.
 */
async function generateWithFallback(
    config: any,
    primaryModel: string,
    fallbackModel: string = 'gemini-2.5-flash'
): Promise<any> {
    let lastError: any = null;

    // Try primary model with retries
    for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
        try {
            if (attempt > 0) {
                const waitMs = RETRY_DELAY_MS * Math.pow(2, attempt - 1);
                console.log(`[ai]: Retry ${attempt}/${MAX_RETRIES} for ${primaryModel} after ${waitMs}ms...`);
                await delay(waitMs);
            }
            return await ai.models.generateContent({ ...config, model: primaryModel });
        } catch (error: any) {
            lastError = error;
            if (error?.status !== 429) {
                // Non-rate-limit error — don't retry
                throw error;
            }
            console.warn(`[ai]: Rate limited (429) on ${primaryModel}, attempt ${attempt + 1}/${MAX_RETRIES + 1}`);
        }
    }

    // All retries exhausted on primary model — fallback to Flash
    if (primaryModel !== fallbackModel) {
        console.warn(`[ai]: ⚡ Falling back from ${primaryModel} → ${fallbackModel}`);
        try {
            return await ai.models.generateContent({ ...config, model: fallbackModel });
        } catch (fallbackError: any) {
            console.error(`[ai]: Fallback to ${fallbackModel} also failed:`, fallbackError);
            // If fallback also fails, throw the original error
            throw lastError;
        }
    }

    throw lastError;
}

/**
 * Run a complex task using Gemini 2.5 Pro (with auto-fallback to Flash on 429)
 */
export async function runProAgent(prompt: string, tools?: ToolDeclaration[]): Promise<string> {
    try {
        const req: any = {
            contents: prompt,
        };

        if (tools && tools.length > 0) {
            req.config = { tools: [{ functionDeclarations: tools }] };
        }

        const response = await generateWithFallback(req, 'gemini-2.5-pro');
        return response.text || '';
    } catch (error) {
        console.error("Error in runProAgent:", error);
        throw error;
    }
}

/**
 * Run a fast task using Gemini 2.5 Flash (with retry on 429)
 */
export async function runFlashAgent(prompt: string, tools?: ToolDeclaration[]): Promise<string> {
    try {
        const req: any = {
            contents: prompt,
        };

        if (tools && tools.length > 0) {
            req.config = { tools: [{ functionDeclarations: tools }] };
        }

        // Flash is already the cheapest model, so no fallback — just retry
        const response = await generateWithFallback(req, 'gemini-2.5-flash', 'gemini-2.5-flash');
        return response.text || '';
    } catch (error) {
        console.error("Error in runFlashAgent:", error);
        throw error;
    }
}

/**
 * Run a complex task using Gemini 2.5 Pro and return structured tool calls
 * (with auto-fallback to Flash on 429)
 */
export async function runProAgentWithTools(prompt: string, tools: ToolDeclaration[]): Promise<AgentResponse> {
    try {
        const req: any = {
            contents: prompt,
            config: {
                tools: [{ functionDeclarations: tools }]
            }
        };

        const response = await generateWithFallback(req, 'gemini-2.5-pro');

        return {
            text: response.text || '',
            functionCalls: response.functionCalls || []
        };
    } catch (error) {
        console.error("Error in runProAgentWithTools:", error);
        throw error;
    }
}
