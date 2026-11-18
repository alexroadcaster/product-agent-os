import type {Connection} from '../api/client.ts';
import type {GraphStatus} from '../../../../packages/contracts/graph/code-graph.ts';
import type {DatabaseMapStatus} from '../../../../packages/contracts/database-map.ts';

export type CapabilityState='not_configured'|'unsupported'|'unavailable'|'indexing'|'partial'|'stale'|'failed'|'available'|'staged'|'connected'|'qualified'|'accepted';
const labels:Record<CapabilityState,readonly [string,string]>={
 not_configured:['Не настроено / не построено','Not configured / not built'],
 unsupported:['Не поддерживается','Unsupported'],unavailable:['Недоступно','Unavailable'],
 indexing:['Построение выполняется','Indexing in progress'],partial:['Частичное покрытие','Partial coverage'],
 stale:['Снимок устарел','Snapshot stale'],failed:['Операция завершилась ошибкой','Operation failed'],
 available:['Доступно в указанном scope','Available in the stated scope'],staged:['Подготовлено к проверке','Staged for review'],
 connected:['Подключено','Connected'],qualified:['Квалифицировано в указанном scope','Qualified in the stated scope'],
 accepted:['Принято владельцем','Accepted by owner'],
};
/** Display vocabulary only: it never grants authority or infers acceptance from another state. */
export function capabilityLabel(state:string,locale:'ru'|'en'):string{
 const pair=Object.hasOwn(labels,state)?labels[state as CapabilityState]:labels.unavailable;
 return pair[locale==='ru'?0:1];
}
/** Global connection attests attachment only; broker qualification belongs to a selected binding. */
export function runtimeConnectionState(connection:Connection|null):CapabilityState{
 if(connection?.route!=='codex_app_agent')return 'not_configured';
 if(!connection.verified||connection.state!=='connected')return 'unavailable';
 return 'connected';
}
export function graphCapabilityState(status:GraphStatus|undefined):CapabilityState{
 if(!status)return 'not_configured';
 if(status.state!=='fresh')return status.state;
 if(!status.counts?.files&&status.coverage?.some(row=>row.status==='unsupported'))return 'unsupported';
 // Even a fresh lexical index has bounded language/semantic coverage.
 return 'partial';
}
export function databaseCapabilityState(status:DatabaseMapStatus|undefined):CapabilityState{
 if(!status||status.state==='unselected'||status.state==='selected')return 'not_configured';
 return status.state==='ready'?'available':status.state;
}
