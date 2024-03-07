
CREATE TABLE IF NOT EXISTS members (
  id SERIAL PRIMARY KEY,
  full_name TEXT NOT NULL,
  username TEXT NOT NULL,
  email TEXT NOT NULL,
  api_key TEXT NOT NULL,
  active_app_id TEXT NOT NULL,
  source_id TEXT NOT NULL
);
 
ALTER TABLE members ADD CONSTRAINT source_id_unique UNIQUE (source_id);
