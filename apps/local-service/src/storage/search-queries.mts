/** Shared with the SQLite query-plan regression fixture. Bind every value. */
export const RANKED_SEARCH_SQL = `SELECT e.* FROM search_fts f JOIN indexed_documents d ON d.rowid=f.rowid
  JOIN entities e ON e.project_id=d.project_id AND e.id=d.entity_id
  WHERE search_fts MATCH ? AND e.project_id=? AND e.deleted=0 AND e.revision=d.revision
  ORDER BY rank LIMIT ? OFFSET ?`;
