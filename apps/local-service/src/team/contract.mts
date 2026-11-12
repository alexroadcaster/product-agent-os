import {createHash,randomUUID} from 'node:crypto';
import type {AssetProfile,AssetSummary,AssetProposal,AssetPreview,TeamRegistry,AssetVersion} from '../../../../packages/contracts/team/assets.ts';
import {safePersistedText} from '../redaction/persisted.mts';
export const teamId='m2b-team-assets';
export function teamFail(code:string):never{throw Object.assign(new Error(code),{code});}
export function digest(value:unknown):string{return createHash('sha256').update(JSON.stringify(value)).digest('hex');}
export function safeAssetPath(path:string){return typeof path==='string'&&path.length<512&&!path.split(/[\\/]/).some(p=>!p||p==='.'||p==='..'||/[\x00-\x1f:<>"|?*]/.test(p)||/[. ]$/.test(p)||/^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)/i.test(p));}
export function sensitivePath(path:string){return /(?:^|[\\/])(?:\.env(?:\..*)?|credentials(?:\..*)?|auth(?:cache|\.json)|id_(?:rsa|ed25519)|.*\.(?:pem|key|p12|pfx))$/i.test(path);}
export function validateProposal(raw:unknown):AssetProposal{
 if(!raw||typeof raw!=='object'||Array.isArray(raw))teamFail('TEAM_PROPOSAL_INVALID');const p=raw as AssetProposal;
 if(!['agent','skill'].includes(p.kind)||!['create','update','archive','delete','restore'].includes(p.action))teamFail('TEAM_PROPOSAL_INVALID');
 for(const key of ['name','description','content','reason'] as const)if(typeof p[key]!=='string'||p[key].length>(key==='content'?256*1024:20000)||p[key].includes('\0'))teamFail('TEAM_PROPOSAL_INVALID');
 if(!p.name.trim()||!p.reason.trim()||!Array.isArray(p.dependencies)||p.dependencies.length>100||p.dependencies.some(x=>typeof x!=='string'||!x||x.length>512)||new Set(p.dependencies).size!==p.dependencies.length)teamFail('TEAM_PROPOSAL_INVALID');
 if(p.action!=='create'&&typeof p.assetId!=='string')teamFail('TEAM_PROPOSAL_INVALID');
 if(safePersistedText(p.content)!==p.content||safePersistedText(p.description)!==p.description)teamFail('SENSITIVE_ASSET_CONTENT');
 const resources=p.resources??[];if(!Array.isArray(resources)||resources.length>100)teamFail('ASSET_RESOURCE_LIMIT');let total=0;const paths=new Set<string>();
 for(const r of resources){if(!safeAssetPath(r.path)||sensitivePath(r.path)||paths.has(r.path.toLowerCase()))teamFail('ASSET_RESOURCE_PATH_INVALID');paths.add(r.path.toLowerCase());
  if(typeof r.base64!=='string'&&!r.blobId)teamFail('ASSET_RESOURCE_INVALID');if(r.base64!==undefined){const bytes=Buffer.from(r.base64,'base64');if(bytes.toString('base64')!==r.base64||bytes.length!==r.byteSize||createHash('sha256').update(bytes).digest('hex')!==r.hash)teamFail('ASSET_RESOURCE_INVALID');
   if(safePersistedText(bytes.toString('utf8'))!==bytes.toString('utf8'))teamFail('SENSITIVE_ASSET_CONTENT');}
  if(!Number.isSafeInteger(r.byteSize)||r.byteSize<0)teamFail('ASSET_RESOURCE_INVALID');total+=r.byteSize;
 }if(total>5*1024*1024)teamFail('ASSET_RESOURCE_LIMIT');
 return {...p,dependencies:[...p.dependencies],resources};
}
/** Pure plan is recomputed under SQLite transaction; preview never grants authority. */
export function previewAsset(registry:TeamRegistry,raw:unknown,expectedRevision:number,activeRuns:{id:string;assetIds:string[]}[],available:(AssetProfile|AssetSummary)[]=registry.assets):AssetPreview{
 let proposal=validateProposal(raw);const old=registry.assets.find(a=>a.id===proposal.assetId);
 if(proposal.action==='create'?Boolean(old):!old)teamFail('TEAM_ASSET_NOT_FOUND');if((old?.revision??0)!==expectedRevision)teamFail('REVISION_CONFLICT');
 if(old?.management==='source_read_only')teamFail('SOURCE_READONLY');
 // Restore is a new version of the historical effective payload, not of editable decoy fields.
 if(proposal.action==='restore'){const restored=old?.versions.find(v=>v.version===proposal.restoreVersion);if(!restored)teamFail('ASSET_VERSION_NOT_FOUND');proposal=validateProposal({...proposal,name:restored.name,description:restored.description,content:restored.content,dependencies:restored.dependencies,resources:restored.resources,source:restored.source});}
 else proposal={...proposal,source:proposal.source??old?.source??null};
 if(old&&old.kind!==proposal.kind)teamFail('ASSET_KIND_IMMUTABLE');
 if(old&&proposal.source&&JSON.stringify(proposal.source)!==JSON.stringify(old.source))teamFail('ASSET_PROVENANCE_IMMUTABLE');
 const dependencyPins=proposal.dependencies.map(id=>{const a=available.find(a=>a.id===id&&!a.archived&&!a.deleted);if(!a||id===proposal.assetId)teamFail('ASSET_DEPENDENCY_UNAVAILABLE');return {id,version:a.effectiveVersion,hash:('versions' in a?a.versions.at(-1)?.hash:a.versionHash)??a.source?.hash};});
 const dependencies=registry.assets.filter(a=>!a.deleted&&a.dependencies.includes(proposal.assetId??'')).map(a=>a.id).sort();
 const activeRunIds=activeRuns.filter(r=>r.assetIds.includes(proposal.assetId??'')).map(r=>r.id).sort();
 if(proposal.action==='delete'&&(dependencies.length||activeRunIds.length))teamFail('ASSET_DEPENDENCY_CONFLICT');
 if(proposal.action==='restore'&&!old?.versions.some(v=>v.version===proposal.restoreVersion))teamFail('ASSET_VERSION_NOT_FOUND');
 const graph=new Map(available.map(a=>[a.id,a.dependencies]));if(proposal.assetId)graph.set(proposal.assetId,proposal.dependencies);const visiting=new Set<string>(),visited=new Set<string>();function visit(id:string){if(visiting.has(id))teamFail('ASSET_DEPENDENCY_CYCLE');if(visited.has(id))return;visiting.add(id);for(const next of graph.get(id)??[])visit(next);visiting.delete(id);visited.add(id);}for(const id of graph.keys())visit(id);
 const review=(value:{name:string;description:string;content:string;dependencies:string[];resources?:AssetProfile['resources'];source?:AssetProfile['source'];archived:boolean;deleted:boolean})=>JSON.stringify({...value,resources:(value.resources??[]).map(({path,hash,byteSize})=>({path,hash,byteSize})).sort((a,b)=>a.path.localeCompare(b.path))},null,2);
 const before=old?review({name:old.name,description:old.description,content:old.content,dependencies:old.dependencies,resources:old.resources,source:old.source,archived:old.archived,deleted:old.deleted}):'';
 const after=review({name:proposal.name,description:proposal.description,content:proposal.content,dependencies:proposal.dependencies,resources:proposal.resources,source:proposal.source,archived:proposal.action==='archive',deleted:proposal.action==='delete'});
 const dependencyImpact={assets:dependencies,activeRunIds};const baseRevision=old?.revision??0;
 const canonical={...proposal,resources:proposal.resources?.map(({path,hash,byteSize})=>({path,hash,byteSize}))};
 return {proposal,baseRevision,diff:{before,after},dependencyImpact,warnings:['PAOS managed version; native profile loading is not observed'],previewDigest:digest({proposal:canonical,baseRevision,dependencyImpact,dependencyPins,head:old??null})};
}
export function applyAsset(registry:TeamRegistry,preview:AssetPreview,actorId:string):{registry:TeamRegistry;asset:AssetProfile}{
 const p=preview.proposal,old=registry.assets.find(a=>a.id===p.assetId),id=p.action==='create'?(p.assetId??randomUUID()):p.assetId!;
 const restored=p.action==='restore'?old!.versions.find(v=>v.version===p.restoreVersion):undefined;
 const content=restored?.content??p.content,resources=restored?.resources??p.resources??[],dependencies=restored?.dependencies??p.dependencies,name=restored?.name??p.name,description=restored?.description??p.description,source=restored?.source??p.source??old?.source??null;
 const version=(old?.versions.length??0)+1;
 const next:AssetVersion={version,hash:digest({content,resources,dependencies,name,description}),createdAt:new Date().toISOString(),actorId,action:p.action,name,description,content,dependencies,resources,source};
 const asset:AssetProfile={id,kind:p.kind,name,description,scope:'project',source,content,resources,dependencies,revision:(old?.revision??0)+1,effectiveVersion:version,loadedVersion:null,loadedCoverage:'unavailable',archived:p.action==='archive',deleted:p.action==='delete',versions:[...old?.versions??[],next],redacted:false,management:'paos_managed'};
 return {asset,registry:{category:'team_registry',assets:[...registry.assets.filter(a=>a.id!==id),asset]}};
}
