import {createHash} from 'node:crypto';
import {bindProject} from '../adapters/project-sources.ts';
import type {CredentialStore} from './broker.ts';

export type ProfileIdentity=Readonly<{profileId:string;registeredPath:string;canonicalRoot:string;directoryIdentity:string}>;
const normalized=(path:string)=>process.platform==='win32'?path.replaceAll('\\','/').toLowerCase():path;
const unavailable=()=>Object.assign(new Error('The registered profile directory is unavailable or changed.'),{code:'PROFILE_ROOT_UNAVAILABLE'});

/** Server-only credential namespace. Canonical aliases share identity; replacing the physical directory revokes it. */
export async function bindProfile(directory:string):Promise<ProfileIdentity> {
 try {
  const binding=await bindProject('profile',directory);
  const digest=createHash('sha256').update(JSON.stringify(['paos_profile_v1',normalized(binding.workspaceRoot),binding.directoryIdentity])).digest('hex');
  return Object.freeze({profileId:`profile_${digest}`,registeredPath:directory,canonicalRoot:binding.workspaceRoot,directoryIdentity:binding.directoryIdentity});
 } catch {throw unavailable();}
}

/** Check both the original selector and canonical location. This is an admission check, not an atomic filesystem lock. */
export async function assertProfileIdentity(identity:ProfileIdentity):Promise<void> {
 const current=await bindProfile(identity.registeredPath);
 if(current.profileId!==identity.profileId||normalized(current.canonicalRoot)!==normalized(identity.canonicalRoot))throw unavailable();
}

/** No lookup, migration, or deletion of legacy/default or foreign-profile targets is allowed. */
export function createProfileScopedStore(identity:ProfileIdentity,store:CredentialStore):CredentialStore {
 async function guard(target:string) {
  const prefix=`PAOS/${identity.profileId}/`;
  if(!target.startsWith(prefix)||!/^[A-Za-z0-9_-]{1,100}$/.test(target.slice(prefix.length))) {
   throw Object.assign(new Error('The credential target is outside this profile.'),{code:'PROFILE_TARGET_REJECTED'});
  }
  await assertProfileIdentity(identity);
 }
 return {
  async read(target){await guard(target);return store.read(target);},
  async write(target,value){await guard(target);await store.write(target,value);},
  async delete(target){await guard(target);await store.delete(target);},
 };
}
