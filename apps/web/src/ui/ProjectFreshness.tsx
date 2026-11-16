import {useEffect,useState} from 'react';
import type {M1Api} from '../api/client.ts';
import type {ProjectFreshness} from '../../../../packages/contracts/project-freshness.ts';
import {sameProjectFreshness} from '../../../../packages/contracts/project-freshness.ts';
import {startProjectFreshnessPolling} from '../api/project-freshness.ts';

/** Snapshot invalidation never replaces a controlled editor or advances its optimistic revision. */
export function ProjectFreshnessNotice({api,projectId,baseline,enabled=true,locale,onRefresh}:{api:M1Api;projectId:string;baseline?:ProjectFreshness;enabled?:boolean;locale:'ru'|'en';onRefresh?:()=>void}){
 const [state,setState]=useState<'fresh'|'stale'|'unavailable'|'unobserved'>('unobserved'),key=JSON.stringify(baseline);
 useEffect(()=>{setState('unobserved');if(!enabled)return;return startProjectFreshnessPolling({projectId,read:signal=>api.projectFreshness(projectId,signal),publish:value=>setState(baseline?sameProjectFreshness(baseline,value)?'fresh':'stale':'unobserved'),error:()=>setState('unavailable')});},[api,projectId,key,enabled]);
 if(!enabled||state==='fresh')return null;
 return <p role="status" className="ui-notice" data-testid="project-freshness" data-state={state}>{state==='stale'?(locale==='ru'?'Снимок устарел: задачи, очередь, scan или policy изменились. Обновите экран; несохранённый черновик сохранит свою revision.':'Snapshot is stale: tasks, queue, scan or policy changed. Refresh this view; an unsaved draft retains its revision.'):state==='unavailable'?(locale==='ru'?'Свежесть снимка проверить не удалось. Используйте явное обновление.':'Snapshot freshness is unavailable. Use explicit refresh.'):(locale==='ru'?'Снимок наблюдался при загрузке; свежесть проверяется отдельно.':'Snapshot was observed on load; freshness is checked separately.')}{onRefresh&&state!=='unobserved'&&<button type="button" onClick={onRefresh}>{locale==='ru'?'Обновить снимок':'Refresh snapshot'}</button>}</p>;
}
