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

CREATE TABLE IF NOT EXISTS feedback_case_map (
  feedback_id TEXT PRIMARY KEY,
  case_id TEXT NOT NULL,
  direction_id TEXT NOT NULL,
  task_type TEXT NOT NULL,
  workflow_stage TEXT NOT NULL,
  success_failure TEXT NOT NULL CHECK (success_failure IN ('success', 'failure', 'mixed')),
  failure_reason TEXT,
  human_edits TEXT NOT NULL,
  reuse_score REAL NOT NULL CHECK (reuse_score >= 0 AND reuse_score <= 1),
  roi_signal TEXT NOT NULL,
  should_deepen INTEGER NOT NULL CHECK (should_deepen IN (0, 1)),
  linked_jd_id TEXT,
  linked_candidate_id TEXT,
  linked_report_id TEXT,
  source_path TEXT NOT NULL,
  recorded_at TEXT NOT NULL,
  notes TEXT,
  FOREIGN KEY (case_id) REFERENCES sample_case(case_id),
  FOREIGN KEY (direction_id) REFERENCES direction_catalog(direction_id)
);

CREATE VIEW IF NOT EXISTS case_feedback_bridge AS
SELECT
  f.feedback_id,
  f.case_id,
  c.case_code,
  c.case_title,
  f.direction_id,
  d.direction_family,
  d.direction_name,
  d.direction_path,
  f.task_type,
  f.workflow_stage,
  f.success_failure,
  f.failure_reason,
  f.human_edits,
  f.reuse_score,
  f.roi_signal,
  f.should_deepen,
  f.linked_jd_id,
  f.linked_candidate_id,
  f.linked_report_id,
  f.source_path,
  f.recorded_at,
  f.notes
FROM feedback_case_map f
JOIN sample_case c ON c.case_id = f.case_id
JOIN direction_catalog d ON d.direction_id = f.direction_id;

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
  ) AS failure_case_count,
  (
    SELECT COUNT(*)
    FROM feedback_case_map f
    WHERE f.direction_id = d.direction_id
  ) AS feedback_count,
  (
    SELECT SUM(CASE WHEN f.success_failure = 'success' THEN 1 ELSE 0 END)
    FROM feedback_case_map f
    WHERE f.direction_id = d.direction_id
  ) AS feedback_success_count,
  (
    SELECT SUM(CASE WHEN f.success_failure = 'failure' THEN 1 ELSE 0 END)
    FROM feedback_case_map f
    WHERE f.direction_id = d.direction_id
  ) AS feedback_failure_count,
  (
    SELECT ROUND(AVG(f.reuse_score), 2)
    FROM feedback_case_map f
    WHERE f.direction_id = d.direction_id
  ) AS avg_reuse_score,
  (
    SELECT group_concat(f.roi_signal, ' | ')
    FROM feedback_case_map f
    WHERE f.direction_id = d.direction_id
  ) AS roi_signals,
  (
    SELECT group_concat(f.human_edits, ' || ')
    FROM feedback_case_map f
    WHERE f.direction_id = d.direction_id
  ) AS human_edits_summary,
  (
    SELECT ROUND(AVG(CASE WHEN f.should_deepen = 1 THEN 1.0 ELSE 0.0 END), 2)
    FROM feedback_case_map f
    WHERE f.direction_id = d.direction_id
  ) AS deepen_vote_rate
FROM direction_catalog d
JOIN direction_review r ON r.direction_id = d.direction_id
WHERE r.review_date = (
  SELECT MAX(review_date)
  FROM direction_review r2
  WHERE r2.direction_id = d.direction_id
);
