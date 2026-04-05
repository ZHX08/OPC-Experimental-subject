#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / 'data' / 'direction-priority-db' / 'direction-priority.sqlite3'
SCHEMA = ROOT / 'data' / 'direction-priority-db' / 'schema.sql'
SEED = ROOT / 'data' / 'direction-priority-db' / 'seed.sql'


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path) -> None:
    if db_path.exists():
        db_path.unlink()
    with connect(db_path) as conn:
        conn.executescript(SCHEMA.read_text(encoding='utf-8'))
        conn.executescript(SEED.read_text(encoding='utf-8'))
        conn.commit()


def report(db_path: Path) -> None:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT
              direction_path,
              direction_name,
              case_count,
              success_case_count,
              failure_case_count,
              feedback_count,
              feedback_success_count,
              feedback_failure_count,
              sample_quality_avg,
              avg_reuse_score,
              feedback_result,
              hit_frequency,
              should_deepen,
              priority_score,
              reason,
              next_action,
              roi_signals,
              human_edits_summary,
              deepen_vote_rate
            FROM direction_deepening_radar
            ORDER BY should_deepen DESC, priority_score DESC, hit_frequency DESC, direction_name ASC
            """
        ).fetchall()

    print('direction_path | cases | success | failure | feedback | reuse | hits | deepen | score | result')
    print('-' * 112)
    for row in rows:
        result = 'yes' if row['should_deepen'] else 'no'
        reuse = f"{row['avg_reuse_score']:.2f}" if row['avg_reuse_score'] is not None else '-'
        print(
            f"{row['direction_path']} | {row['case_count']} | {row['success_case_count']} | {row['failure_case_count']} | "
            f"{row['feedback_count']} | {reuse} | {row['hit_frequency']} | {result} | {row['priority_score']:.1f} | {row['feedback_result']}"
        )
        print(f"  reason: {row['reason']}")
        print(f"  next:   {row['next_action']}")
        if row['roi_signals']:
            print(f"  roi:    {row['roi_signals']}")
        if row['human_edits_summary']:
            print(f"  edits:  {row['human_edits_summary']}")
        if row['deepen_vote_rate'] is not None:
            print(f"  vote:   {row['deepen_vote_rate']}")


def feedback_report(db_path: Path) -> None:
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT
              feedback_id,
              case_id,
              direction_path,
              success_failure,
              failure_reason,
              human_edits,
              reuse_score,
              roi_signal,
              should_deepen,
              linked_jd_id,
              linked_candidate_id,
              linked_report_id,
              recorded_at
            FROM case_feedback_bridge
            ORDER BY direction_path ASC, recorded_at ASC, feedback_id ASC
            """
        ).fetchall()

    print('feedback_id | case_id | direction_path | result | reuse | deepen | roi')
    print('-' * 112)
    for row in rows:
        result = row['success_failure']
        deepen = 'yes' if row['should_deepen'] else 'no'
        print(
            f"{row['feedback_id']} | {row['case_id']} | {row['direction_path']} | {result} | "
            f"{row['reuse_score']:.2f} | {deepen} | {row['roi_signal']}"
        )
        if row['failure_reason']:
            print(f"  failure: {row['failure_reason']}")
        print(f"  edits:   {row['human_edits']}")
        print(f"  refs:    jd={row['linked_jd_id']} cand={row['linked_candidate_id']} report={row['linked_report_id']}")


def main() -> None:
    parser = argparse.ArgumentParser(description='Build and inspect the direction priority SQLite database.')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB, help='SQLite database path')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init', help='Create and seed the database')
    sub.add_parser('report', help='Print the direction priority report')
    sub.add_parser('feedback', help='Print the feedback-to-case bridge report')
    args = parser.parse_args()

    if args.command == 'init':
        init_db(args.db)
    elif args.command == 'report':
        report(args.db)
    elif args.command == 'feedback':
        feedback_report(args.db)


if __name__ == '__main__':
    main()
