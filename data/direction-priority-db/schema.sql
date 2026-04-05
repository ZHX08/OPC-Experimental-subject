PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS direction_catalog (
  direction_id TEXT PRIMARY KEY,
  direction_family TEXT NOT NULL,
  direction_name TEXT NOT NULL,
  direction_path TEXT NOT NULL UNIQUE,
  description TEXT,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sample_case (
  case_id TEXT PRIMARY KEY,
  direction_id TEXT NOT NULL,
  case_code TEXT NOT NULL UNIQUE,
  case_title TEXT NOT NULL,
  case_status TEXT NOT NULL CHECK (case_status IN ('success', 'failure', 'mixed')),
  sample_quality_score REAL NOT NULL,
  feedback_result TEXT NOT NULL,
  hit_frequency INTEGER NOT NULL DEFAULT 0,
  should_deepen INTEGER NOT NULL DEFAULT 0 CHECK (should_deepen IN (0, 1)),
  source_path TEXT NOT NULL,
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (direction_id) REFERENCES direction_catalog(direction_id)
);

CREATE TABLE IF NOT EXISTS case_asset (
  asset_id TEXT PRIMARY KEY,
  case_id TEXT NOT NULL,
  asset_type TEXT NOT NULL,
  asset_path TEXT NOT NULL,
  asset_quality_score REAL,
  accepted INTEGER,
  created_at TEXT NOT NULL,
  FOREIGN KEY (case_id) REFERENCES sample_case(case_id)
);

CREATE TABLE IF NOT EXISTS direction_hit_log (
  hit_id TEXT PRIMARY KEY,
  direction_id TEXT NOT NULL,
  case_id TEXT,
  hit_source TEXT NOT NULL,
  hit_count INTEGER NOT NULL,
  query_text TEXT,
  recorded_at TEXT NOT NULL,
  notes TEXT,
  FOREIGN KEY (direction_id) REFERENCES direction_catalog(direction_id),
  FOREIGN KEY (case_id) REFERENCES sample_case(case_id)
);

CREATE TABLE IF NOT EXISTS direction_review (
  review_id TEXT PRIMARY KEY,
  direction_id TEXT NOT NULL,
  review_date TEXT NOT NULL,
  sample_quality_avg REAL NOT NULL,
  feedback_result TEXT NOT NULL,
  hit_frequency INTEGER NOT NULL,
  should_deepen INTEGER NOT NULL CHECK (should_deepen IN (0, 1)),
  priority_score REAL NOT NULL,
  reason TEXT NOT NULL,
  next_action TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY (direction_id) REFERENCES direction_catalog(direction_id)
);

CREATE VIEW IF NOT EXISTS direction_deepening_radar AS
SELECT
  d.direction_id,
  d.direction_family,
  d.direction_name,
  d.direction_path,
  r.review_date,
  r.sample_quality_avg,
  r.feedback_result,
  r.hit_frequency,
  r.should_deepen,
  r.priority_score,
  r.reason,
  r.next_action,
  (
    SELECT COUNT(*)
    FROM sample_case c
    WHERE c.direction_id = d.direction_id
  ) AS case_count,
  (
    SELECT SUM(CASE WHEN c.case_status = 'success' THEN 1 ELSE 0 END)
    FROM sample_case c
    WHERE c.direction_id = d.direction_id
  ) AS success_case_count,
  (
    SELECT SUM(CASE WHEN c.case_status = 'failure' THEN 1 ELSE 0 END)
    FROM sample_case c
    WHERE c.direction_id = d.direction_id
  ) AS failure_case_count
FROM direction_catalog d
JOIN direction_review r ON r.direction_id = d.direction_id
WHERE r.review_date = (
  SELECT MAX(review_date)
  FROM direction_review r2
  WHERE r2.direction_id = d.direction_id
);
