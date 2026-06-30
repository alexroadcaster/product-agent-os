import * as lancedb from '@lancedb/lancedb';
import path from 'path';
import fs from 'fs';

// Store the database inside the backend directory for now
const DB_PATH = path.join(__dirname, '../../.sol_data');

let db: lancedb.Connection | null = null;

/**
 * Initializes and returns the connection to the local LanceDB database.
 */
export async function getDb(): Promise<lancedb.Connection> {
    if (db) return db;

    // Ensure the directory exists
    if (!fs.existsSync(DB_PATH)) {
        fs.mkdirSync(DB_PATH, { recursive: true });
    }

    console.log(`[db]: Connecting to LanceDB at ${DB_PATH}`);
    db = await lancedb.connect(DB_PATH);

    return db;
}

/**
 * Initializes the base collections needed for SOL (Projects, Conversations).
 * We will expand the schema here as we build out the features.
 */
export async function initializeCollections() {
    const database = await getDb();
    const collectionNames = await database.tableNames();

    // Basic sanity check/creation of a test "projects" table if it doesn't exist
    if (!collectionNames.includes('projects')) {
        console.log('[db]: Creating "projects" table...');
        // LanceDB requires an array of objects to implicitly define the schema
        await database.createTable('projects', [
            { id: '1', name: 'Farmer Marketplace', category: 'B2C', createdAt: new Date().toISOString() }
        ]);
    }

    // Check for "sessions" table
    if (!collectionNames.includes('sessions')) {
        console.log('[db]: Creating "sessions" table...');
        await database.createTable('sessions', [
            { id: 'default', state_json: '{}', updated_at: new Date().toISOString() }
        ]);
    }

    // Check for "agent_profiles" table
    if (!collectionNames.includes('agent_profiles')) {
        console.log('[db]: Creating "agent_profiles" table...');
        await database.createTable('agent_profiles', [
            { id: 'default', profile_json: '{}', updated_at: new Date().toISOString() }
        ]);
    }

    console.log('[db]: LanceDB collections initialized.');
}

/**
 * Saves a session state to the database.
 */
export async function saveSession(sessionId: string, state: any) {
    try {
        const database = await getDb();
        const table = await database.openTable('sessions');

        // Check if exists
        const records = await table.query().where(`id = '${sessionId}'`).toArray();
        const stateJson = JSON.stringify(state);
        const timestamp = new Date().toISOString();

        if (records.length > 0) {
            // Update (LanceDB JS currently doesn't have a simple UPDATE by ID, 
            // so we delete and insert)
            await table.delete(`id = '${sessionId}'`);
        }

        await table.add([{ id: sessionId, state_json: stateJson, updated_at: timestamp }]);
    } catch (e) {
        console.error('[db] Error saving session:', e);
    }
}

/**
 * Retrieves a session state from the database.
 */
export async function getSession(sessionId: string): Promise<any | null> {
    try {
        const database = await getDb();
        const table = await database.openTable('sessions');
        const records = await table.query().where(`id = '${sessionId}'`).toArray();

        if (records.length > 0 && records[0].state_json) {
            return JSON.parse(records[0].state_json as string);
        }
        return null;
    } catch (e) {
        console.error('[db] Error loading session:', e);
        return null;
    }
}

/**
 * Saves an agent profile to the database.
 */
export async function saveAgentProfile(profileId: string, profile: any) {
    try {
        const database = await getDb();
        const table = await database.openTable('agent_profiles');

        const records = await table.query().where(`id = '${profileId}'`).toArray();
        const profileJson = JSON.stringify(profile);
        const timestamp = new Date().toISOString();

        if (records.length > 0) {
            await table.delete(`id = '${profileId}'`);
        }

        await table.add([{ id: profileId, profile_json: profileJson, updated_at: timestamp }]);
    } catch (e) {
        console.error(`[db] Error saving agent profile ${profileId}:`, e);
    }
}

/**
 * Retrieves an agent profile from the database.
 */
export async function getAgentProfile(profileId: string): Promise<any | null> {
    try {
        const database = await getDb();
        const table = await database.openTable('agent_profiles');
        const records = await table.query().where(`id = '${profileId}'`).toArray();

        if (records.length > 0 && records[0].profile_json) {
            return JSON.parse(records[0].profile_json as string);
        }
        return null;
    } catch (e) {
        console.error(`[db] Error loading agent profile ${profileId}:`, e);
        return null;
    }
}

/**
 * Retrieves all agent profiles from the database.
 */
export async function getAllAgentProfiles(): Promise<any[]> {
    try {
        const database = await getDb();
        const table = await database.openTable('agent_profiles');
        // A simple query without where clause returns all. Limit to a reasonable number.
        const records = await table.query().limit(100).toArray();

        return records
            .filter(r => r.id !== 'default') // Exclude the dummy initialization record
            .map(r => JSON.parse(r.profile_json as string));
    } catch (e) {
        console.error('[db] Error loading all agent profiles:', e);
        return [];
    }
}
