import {commentMarkdown,inlineMarkdown} from './comment-markdown.ts';

/** React escapes all text; external links are protocol-checked and never fetched for previews. */
export function CommentMarkdown({body}:{body:string}){
 const inline=(text:string)=>inlineMarkdown(text).map((part,i)=>part.kind==='link'?<a key={i} href={part.href} target="_blank" rel="noopener noreferrer">{part.text}</a>:part.kind==='strong'?<strong key={i}>{part.text}</strong>:part.kind==='em'?<em key={i}>{part.text}</em>:part.kind==='code'?<code key={i}>{part.text}</code>:part.text);
 return <div className="m2-comment-body">{commentMarkdown(body).map((block,i)=>block.kind==='list'?<ul key={i}>{block.items.map((text,j)=><li key={j}>{inline(text)}</li>)}</ul>:block.kind==='code'?<pre key={i}><code>{block.text}</code></pre>:block.kind==='heading'?<h4 key={i}>{inline(block.text)}</h4>:<p key={i}>{inline(block.text)}</p>)}</div>;
}
