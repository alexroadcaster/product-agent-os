export type MessageStreamRedactor = Readonly<{
  push: (text:string)=>string;
  finish: ()=>string;
  bufferedCharacters: ()=>number;
}>;
export class MessageStreamError extends Error {
  readonly code:string;
  constructor(code:string){super('The visible message stream is unavailable.');this.code=code;}
}
const tokenCharacter=(value:string)=>/^[A-Za-z0-9_-]$/.test(value);
const keyPrefix='sk-';
const replacement='[redacted]';

/** Retain only possible credential prefixes; unknown sk-* bodies are discarded as they arrive, never buffered. */
export function createMessageStreamRedactor(options:Readonly<{secrets:()=>readonly string[];maxChunkBytes?:number}>):MessageStreamRedactor {
  let pending='';let previousRaw='';let token=false;let closed=false;
  function consume(length:number) {previousRaw=pending[length-1]??previousRaw;pending=pending.slice(length);}
  function drain(secrets:readonly string[],final:boolean):string {
    let visible='';
    while(pending.length) {
      if(token) {
        if(tokenCharacter(pending[0])){consume(1);continue;}
        token=false;
      }
      const prefixes=secrets.filter((secret)=>secret.startsWith(pending));
      if(!final&&prefixes.some((secret)=>secret.length>pending.length))break;
      const marker=secrets.some((secret)=>replacement.includes(secret))?'':replacement;
      const boundary=!previousRaw||!/^[A-Za-z0-9_]$/.test(previousRaw);
      const full=secrets.filter((secret)=>pending.startsWith(secret)).sort((left,right)=>right.length-left.length)[0];
      if(full){const keyToken=boundary&&/^sk-[A-Za-z0-9_-]*$/.test(full);consume(full.length);visible+=marker;if(keyToken)token=true;continue;}
      if(prefixes.length){if(final){consume(pending.length);visible+=marker;}break;}
      if(boundary&&pending.startsWith(keyPrefix)){consume(keyPrefix.length);visible+=marker;token=true;continue;}
      if(boundary&&keyPrefix.startsWith(pending)) {
        if(final){consume(pending.length);visible+=marker;}
        break;
      }
      visible+=pending[0];consume(1);
    }
    return visible;
  }
  function keys() {
    const secrets=options.secrets();
    if(secrets.length>16||secrets.some((secret)=>typeof secret!=='string'||!secret||Buffer.byteLength(secret)>2560))throw new MessageStreamError('MESSAGE_STREAM_KEYS_INVALID');
    return secrets;
  }
  return {
    push(text) {
      if(closed)throw new MessageStreamError('MESSAGE_STREAM_CLOSED');
      if(typeof text!=='string'||Buffer.byteLength(text)>(options.maxChunkBytes??1024*1024))throw new MessageStreamError('MESSAGE_STREAM_CHUNK_LIMIT');
      const secrets=keys();let visible='';
      for(const character of text) {
        pending+=character;visible+=drain(secrets,false);
        if(pending.length>2561)throw new MessageStreamError('MESSAGE_STREAM_BUFFER_LIMIT');
      }
      return visible;
    },
    finish() {
      if(closed)return '';closed=true;
      const result=drain(keys(),true);pending='';token=false;return result;
    },
    bufferedCharacters:()=>pending.length,
  };
}
