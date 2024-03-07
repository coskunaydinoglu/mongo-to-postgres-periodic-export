
CREATE TABLE IF NOT EXISTS members (
  id SERIAL PRIMARY KEY,
  full_name TEXT NOT NULL,
  username TEXT NOT NULL,
  email TEXT NOT NULL,
  api_key TEXT NOT NULL
);
 