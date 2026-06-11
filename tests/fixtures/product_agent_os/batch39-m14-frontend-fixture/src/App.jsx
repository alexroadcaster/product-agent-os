export function App({ state = "success" }) {
  if (state === "loading") {
    return <main aria-busy="true">Loading dashboard</main>;
  }

  if (state === "empty") {
    return <main>No workflows yet</main>;
  }

  if (state === "error") {
    return (
      <main role="alert">
        Could not load workflows
      </main>
    );
  }

  return (
    <main>
      <h1>Workflow Console</h1>
      <button type="button">Create workflow</button>
    </main>
  );
}

