import { useState } from "react";

export function SearchBox() {
  const [query, setQuery] = useState("");

  return (
    <form aria-label="Synthetic search">
      <label htmlFor="fixture-search">Search</label>
      <input
        id="fixture-search"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder="Synthetic query"
      />
      <button type="submit">Search</button>
    </form>
  );
}
