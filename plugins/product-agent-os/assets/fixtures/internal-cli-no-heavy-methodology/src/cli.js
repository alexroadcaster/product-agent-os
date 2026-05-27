export function runCheck() {
  return "synthetic-internal-check";
}

if (process.argv.includes("--check")) {
  console.log(runCheck());
}
