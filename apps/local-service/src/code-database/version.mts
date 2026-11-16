import {createRequire} from 'node:module';
const require=createRequire(new URL('../../../web/package.json',import.meta.url));
/** Package metadata only; importing the production service does not load the native parser. */
export const parserVersion='rolldown-'+require('rolldown/package.json').version+':code-database-static-v1';
