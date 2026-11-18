import {scaleLinear} from 'd3';
import {Icon,type IconName} from './Icon.tsx';

export function Metric({label,value,note,icon}:{label:string;value:string|number;note:string;icon:IconName}){return <div className="ui-metric"><span><Icon name={icon}/>{label}</span><strong>{value}</strong><small>{note}</small></div>;}
/** React owns marks; D3 owns the shared zero-based scale. Values are always visible without hover. */
export function Bars({rows,label}:{rows:{id:string;name:string;value:number}[];label:string}){const max=Math.max(1,...rows.map(r=>r.value)),scale=scaleLinear().domain([0,max]).range([0,100]);return <div aria-label={label} data-renderer="d3-scale">{rows.map(r=><div className="ui-chart-row" key={r.id}><span>{r.name}</span><svg viewBox="0 0 100 16" preserveAspectRatio="none" aria-hidden="true"><rect className="ui-chart-track" width="100" height="16" rx="3"/><rect className="ui-chart-bar" width={scale(r.value)} height="16" rx="3"/></svg><strong>{r.value.toLocaleString()}</strong></div>)}</div>;}
