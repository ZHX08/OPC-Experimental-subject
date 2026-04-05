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
              sample_quality_avg,
              feedback_result,
              hit_frequency,
              should_deepen,
              priority_score,
              reason,
              next_action
            FROM direction_deepening_radar
            ORDER BY should_deepen DESC, priority_score DESC, hit_frequency DESC, direction_name ASC
            """
        ).fetchall()

    print('direction_path | case_count | success | failure | quality | hits | deepen | score | result')
    print('-' * 96)
    for row in rows:
        result = 'yes' if row['should_deepen'] else 'no'
        print(
            f"{row['direction_path']} | {row['case_count']} | {row['success_case_count']} | {row['failure_case_count']} | "
            f"{row['sample_quality_avg']:.1f} | {row['hit_frequency']} | {result} | {row['priority_score']:.1f} | {row['feedback_result']}"
        )
        print(f"  reason: {row['reason']}")
        print(f"  next:   {row['next_action']}")


def main() -> None:
    parser = argparse.ArgumentParser(description='Build and inspect the direction priority SQLite database.')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB, help='SQLite database path')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init', help='Create and seed the database')
    sub.add_parser('report', help='Print the direction priority report')
    args = parser.parse_args()

    if args.command == 'init':
        init_db(args.db)
    elif args.command == 'report':
        report(args.db)


if __name__ == '__main__':
    main()
