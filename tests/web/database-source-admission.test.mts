import {test} from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {join} from 'node:path';
import {writeFile,mkdir,open,link} from 'node:fs/promises';
import {m2Fixture} from './m2-fixture.mts';
import {createProjectInventory} from '../../apps/local-service/src/project-inventory/service.mts';

test('explicit offline SQLite admission accepts a pinned database while generic text access stays forbidden',async t=>{
 const f=await m2Fixture(t),p=(await f.store.project('p'))!,path=join(f.root,'schema.db'),db=new DatabaseSync(path);db.exec('CREATE TABLE sample(id INTEGER)');db.close();
 const inventory=createProjectInventory(),entry=await inventory.inspect(p,'schema.db'),admitted=await inventory.admitDatabaseSource(p,{path:'schema.db',revision:entry.revision});
 assert.equal(admitted.fileRevision,entry.revision);assert.equal(admitted.rootIdentity,p.rootIdentity);assert.equal(admitted.byteSize,8192);await assert.rejects(inventory.read(p,{path:'schema.db'}),{code:'INVENTORY_SOURCE_FORBIDDEN'});
});

import {unlink,readFile} from 'node:fs/promises';
test('database admission reapplies excludes, nested ignores, hard deny, pins and policy completeness',async t=>{
 const f=await m2Fixture(t),p=(await f.store.project('p'))!;await mkdir(join(f.root,'nested'));await mkdir(join(f.root,'.aws'));
 for(const name of ['schema.db','nested/ignored.db','.aws/secret.db']){const db=new DatabaseSync(join(f.root,name));db.exec('CREATE TABLE sample(id INTEGER)');db.close();}
 await writeFile(join(f.root,'.gitignore'),'nested/*.db\n');
 await assert.rejects(createProjectInventory({policy:{exclude:['schema.db'],include:['**']}}).admitDatabaseSource(p,{path:'schema.db'}),{code:'INVENTORY_SOURCE_FORBIDDEN'});
 await assert.rejects(createProjectInventory().admitDatabaseSource(p,{path:'nested/ignored.db'}),{code:'INVENTORY_SOURCE_FORBIDDEN'});
 assert.equal((await createProjectInventory({policy:{include:['nested/*.db']}}).admitDatabaseSource(p,{path:'nested/ignored.db'})).relativePath,'nested/ignored.db');
 await assert.rejects(createProjectInventory({policy:{include:['**']}}).admitDatabaseSource(p,{path:'.aws/secret.db'}),{code:'INVENTORY_SOURCE_FORBIDDEN'});
 const inventory=createProjectInventory(),entry=await inventory.inspect(p,'schema.db');await writeFile(join(f.root,'schema.db'),await readFile(join(f.root,'schema.db')));await assert.rejects(inventory.admitDatabaseSource(p,{path:'schema.db',revision:entry.revision}),{code:'INVENTORY_REVISION_STALE'});
 await assert.rejects(inventory.admitDatabaseSource(p,{path:'../schema.db'}),{code:'INVENTORY_PATH_FORBIDDEN'});
 await writeFile(join(f.root,'.gitignore'),'[[:digit:]].db\n');await assert.rejects(inventory.admitDatabaseSource(p,{path:'schema.db'}),{code:'INVENTORY_SOURCE_FORBIDDEN'});
});
test('offline database admission refuses sidecars, WAL header without sidecars, corrupt/missing/hardlinked and oversized sources',async t=>{
 const f=await m2Fixture(t),p=(await f.store.project('p'))!,path=join(f.root,'schema.db'),db=new DatabaseSync(path);db.exec('CREATE TABLE sample(id INTEGER)');db.close();const inventory=createProjectInventory(),header=(await readFile(path)).subarray(0,100);
 for(const suffix of ['-wal','-shm','-journal']){await writeFile(path+suffix,'synthetic');await assert.rejects(inventory.admitDatabaseSource(p,{path:'schema.db'}),{code:'INVENTORY_DATABASE_SIDECAR'});await unlink(path+suffix);}
 const h=await open(path,'r+');await h.write(Buffer.from([2,2]),0,2,18);await h.close();await assert.rejects(inventory.admitDatabaseSource(p,{path:'schema.db'}),{code:'INVENTORY_DATABASE_WAL_UNSUPPORTED'});
 await writeFile(path,'corrupt');await assert.rejects(inventory.admitDatabaseSource(p,{path:'schema.db'}),{code:'INVENTORY_DATABASE_FORMAT_UNSUPPORTED'});
 await assert.rejects(inventory.admitDatabaseSource(p,{path:'missing.db'}),{code:'ENOENT'});
 await link(path,path+'.hard');await assert.rejects(inventory.admitDatabaseSource(p,{path:'schema.db'}),{code:'INVENTORY_SOURCE_FORBIDDEN'});await unlink(path+'.hard');
 const sparse=await open(path,'w');await sparse.truncate(128*1024*1024);await sparse.write(header,0,100,0);await sparse.close();assert.equal((await inventory.admitDatabaseSource(p,{path:'schema.db'})).byteSize,128*1024*1024);const larger=await open(path,'r+');await larger.truncate(128*1024*1024+1);await larger.close();await assert.rejects(inventory.admitDatabaseSource(p,{path:'schema.db'}),{code:'INVENTORY_FILE_TOO_LARGE'});
});
