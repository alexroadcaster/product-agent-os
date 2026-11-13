import * as d3 from 'd3';
import { gsap } from 'gsap';
import icons from '@iconify-json/duo-icons/icons.json';

// Browser-only, fully local dependencies for synthetic design review.
// Mermaid Tiny is prepended by build.mjs; it owns globalThis.mermaid.
window.DesignRuntime = { d3, gsap, mermaid: globalThis.mermaid, icons,
  versions: {d3: '7.9.2', gsap: '3.15.1', mermaid: '12.3.0', icons: '1.2.2'} };
