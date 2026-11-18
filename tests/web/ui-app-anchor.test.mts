import assert from 'node:assert/strict';
import {test} from 'node:test';
import {parseAppAnchor} from '../../apps/web/src/ui/app-anchor.ts';

const projects = [{id:'primary'}, {id:'secondary'}];

test('App anchors preserve encoded paths, route priority and the bounded line number',()=>{
  assert.deepEqual(parseAppAnchor('#project=primary&file=docs%2FGuide+%D0%A5.md&line=12&database=orders',projects),
    {section:'files',projectId:'primary',path:'docs/Guide Х.md',line:12});
  assert.deepEqual(parseAppAnchor('#project=primary&file=guide.md&line=1000001',projects),
    {section:'files',projectId:'primary',path:'guide.md',line:1});
  assert.deepEqual(parseAppAnchor('#project=primary&file=C%3A%5Cguide.md&database=orders&dbtab=changes&session=s&message=m',projects),
    {section:'database',projectId:'primary',table:'orders',tab:'changes'});
});

test('App anchors recognize an empty database selection and a complete session message',()=>{
  assert.deepEqual(parseAppAnchor('#project=secondary&database=&dbtab=unknown',projects),
    {section:'database',projectId:'secondary',table:'',tab:'schema'});
  assert.deepEqual(parseAppAnchor('#project=secondary&session=session-2&message=message-4',projects),
    {section:'sessions',projectId:'secondary',sessionId:'session-2',messageId:'message-4'});
});

test('App anchors leave the active screen alone for unknown projects and invalid targets',()=>{
  for(const hash of [
    '',
    '#unsupported-route',
    '#project=missing&file=guide.md',
    '#project=primary&session=s',
    '#project=primary&session=s%5Cq&message=m',
    '#project=primary&database=orders%0Dnext',
  ])assert.equal(parseAppAnchor(hash,projects),null,hash);
});
