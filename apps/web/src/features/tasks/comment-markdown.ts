import {safeExternalUrl} from './model.ts';

export type Inline = {kind:'text'|'strong'|'em'|'code';text:string}|{kind:'link';text:string;href:string};
export type Block = {kind:'paragraph'|'heading'|'code';text:string}|{kind:'list';items:string[]};

/** Bounded Markdown subset; unsupported HTML, images and unsafe links remain literal text. */
export function inlineMarkdown(source:string):Inline[]{
 const result:Inline[]=[];
 const tokens=/(!?\[[^\]\n]{1,512}\]\([^\s)]{1,2048}\)|`[^`\n]{1,4096}`|\*\*[^*\n]{1,4096}\*\*|\*[^*\n]{1,4096}\*)/g;
 let previous=0;
 for(const match of source.matchAll(tokens)){
  if(match.index!>previous)result.push({kind:'text',text:source.slice(previous,match.index)});
  const token=match[0];
  if(token.startsWith('!'))result.push({kind:'text',text:token});
  else if(token.startsWith('[')){
   const parts=/^\[([^\]]+)\]\((.+)\)$/.exec(token)!;const href=safeExternalUrl(parts[2]);
   result.push(href?{kind:'link',text:parts[1],href}:{kind:'text',text:token});
  }else if(token.startsWith('`'))result.push({kind:'code',text:token.slice(1,-1)});
  else if(token.startsWith('**'))result.push({kind:'strong',text:token.slice(2,-2)});
  else result.push({kind:'em',text:token.slice(1,-1)});
  previous=match.index!+token.length;
 }
 if(previous<source.length)result.push({kind:'text',text:source.slice(previous)});
 return result;
}

export function commentMarkdown(source:string):Block[]{
 const lines=source.replace(/\r\n?/g,'\n').split('\n'),blocks:Block[]=[];
 let paragraph:string[]=[];const flush=()=>{if(paragraph.length){blocks.push({kind:'paragraph',text:paragraph.join('\n')});paragraph=[];}};
 for(let i=0;i<lines.length;i++){
  const line=lines[i];
  if(line.startsWith('```')){
   const start=i,code:string[]=[];while(++i<lines.length&&!lines[i].startsWith('```'))code.push(lines[i]);
   if(i===lines.length){paragraph.push(...lines.slice(start));break;}
   flush();blocks.push({kind:'code',text:code.join('\n')});
  }else if(!line.trim())flush();
  else if(/^#{1,6} /.test(line)){flush();blocks.push({kind:'heading',text:line.replace(/^#{1,6} /,'')});}
  else if(/^[-*] /.test(line)){flush();const items=[line.slice(2)];while(i+1<lines.length&&/^[-*] /.test(lines[i+1]))items.push(lines[++i].slice(2));blocks.push({kind:'list',items});}
  else paragraph.push(line);
 }
 flush();return blocks;
}
