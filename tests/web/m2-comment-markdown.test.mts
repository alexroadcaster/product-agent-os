import test from 'node:test';
import assert from 'node:assert/strict';
import {inlineMarkdown,commentMarkdown} from '../../apps/web/src/features/tasks/comment-markdown.ts';

test('comment subset preserves unsafe links, HTML and images as inert text',()=>{
 const raw='<img src=x onerror=alert(1)> ![remote](https://example.test/a.png) [bad](javascript:alert) [secret](https://user:pass@example.test)';
 assert.equal(inlineMarkdown(raw).every(p=>p.kind==='text'),true);
 assert.equal(inlineMarkdown(raw).map(p=>p.text).join(''),raw);
});
test('comment subset renders emphasis, code, safe link, blocks and keeps incomplete fences',()=>{
 assert.deepEqual(inlineMarkdown('**bold** *em* `code` [ok](https://example.test)'),[
  {kind:'strong',text:'bold'},{kind:'text',text:' '},{kind:'em',text:'em'},{kind:'text',text:' '},{kind:'code',text:'code'},{kind:'text',text:' '},{kind:'link',text:'ok',href:'https://example.test/'}]);
 assert.deepEqual(commentMarkdown('# Heading\n\n- one\n- two\n\n```js\n<script>\n```\n\n```unclosed\nraw'),[
  {kind:'heading',text:'Heading'},{kind:'list',items:['one','two']},{kind:'code',text:'<script>'},{kind:'paragraph',text:'```unclosed\nraw'}]);
});
