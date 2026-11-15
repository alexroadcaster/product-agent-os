/** Metrics are emitted on stderr; stdout remains the engine's machine-readable result. */
process.once('exit',()=>process.stderr.write('\nPAOS_RESOURCE '+JSON.stringify({maxRssKiB:process.resourceUsage().maxRSS,cpuUserMicros:process.resourceUsage().userCPUTime,cpuSystemMicros:process.resourceUsage().systemCPUTime})+'\n'));
