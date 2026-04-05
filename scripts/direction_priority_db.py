#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / 'data' / 'direction-priority-db' / 'direction-priority.sqlite3'
SCHEMA = ROOT / 'data' / 'direction-priority-db' / 'schema.sql'
SEED = ROOT / 'data' / 'direction-priority-db' / 'seed.sql'

DEFAULT_DIRECTION_INFO = {
    'dir-aie-internal-process-automation': {
        'direction_family': 'AI 应用工程师',
        'direction_name': '内部流程自动化',
        'direction_path': 'AI 应用工程师 / 内部流程自动化',
        'description': '面向采购、法务、审批和内部流转自动化的方向。',
        'status': 'active',
    },
}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
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


def parse_json(text: str, source: Path) -> dict[str, Any]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f'Invalid JSON in {source}: {exc}') from exc
    if not isinstance(data, dict):
        raise ValueError(f'Expected a JSON object in {source}')
    return data


def load_bridge_payload(source: Path) -> dict[str, Any]:
    if source.suffix.lower() == '.json':
        data = parse_json(source.read_text(encoding='utf-8'), source)
        if 'sqlite_bridge' in data and isinstance(data['sqlite_bridge'], dict):
            return data['sqlite_bridge']
        if 'feedback_case_map_record' in data:
            return data
        if {'feedback_id', 'case_id', 'direction_id'} <= data.keys():
            return {'feedback_case_map_record': data}
        raise ValueError(f'{source} does not contain a sqlite bridge payload')

    if source.suffix.lower() == '.md':
        text = source.read_text(encoding='utf-8')
        match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.S)
        if not match:
            raise ValueError(f'Could not find a JSON export block in {source}')
        data = parse_json(match.group(1), source)
        if 'feedback_case_map_record' in data:
            return data
        if {'feedback_id', 'case_id', 'direction_id'} <= data.keys():
            return {'feedback_case_map_record': data}
        raise ValueError(f'{source} does not contain an importable feedback record')

    raise ValueError(f'Unsupported export type: {source}')


def iter_sources(paths: list[Path]) -> list[Path]:
    items: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        if path.is_dir():
            preferred: dict[Path, Path] = {}
            for child in sorted(path.rglob('*')):
                if child.suffix.lower() not in {'.json', '.md'}:
                    continue
                key = child.with_suffix('').resolve()
                current = preferred.get(key)
                if current is None or (current.suffix.lower() == '.md' and child.suffix.lower() == '.json'):
                    preferred[key] = child
            for child in preferred.values():
                resolved = child.resolve()
                if resolved in seen:
                    continue
                seen.add(resolved)
                items.append(child)
        else:
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                items.append(path)
    return items


def direction_record_from_feedback(record: dict[str, Any]) -> dict[str, Any]:
    direction_id = str(record.get('direction_id', '')).strip()
    default = DEFAULT_DIRECTION_INFO.get(direction_id, {})
    direction_path = str(record.get('direction_path', '')).strip() or default.get('direction_path', direction_id)
    if '/' in direction_path:
        direction_family, direction_name = [part.strip() for part in direction_path.split('/', 1)]
    else:
        direction_family = default.get('direction_family', 'AI 应用工程师')
        direction_name = default.get('direction_name', direction_path or direction_id)
    return {
        'direction_id': direction_id,
        'direction_family': default.get('direction_family', direction_family),
        'direction_name': default.get('direction_name', direction_name),
        'direction_path': default.get('direction_path', direction_path),
        'description': default.get('description', ''),
        'status': default.get('status', 'active'),
    }


def sample_case_record_from_feedback(record: dict[str, Any], source: Path, now: str) -> dict[str, Any]:
    direction_id = str(record.get('direction_id', '')).strip()
    case_id = str(record.get('case_id', '')).strip() or f"case-{source.stem}"
    case_code = str(record.get('case_code', '')).strip() or source.stem.replace('_', '-').replace(' ', '-')
    case_title = str(record.get('case_title', '')).strip() or case_code
    success_failure = str(record.get('success_failure', 'mixed')).strip() or 'mixed'
    feedback_result = str(record.get('feedback_result', '')).strip()
    if not feedback_result:
        feedback_result = 'passed' if success_failure == 'success' else 'rejected' if success_failure == 'failure' else 'mixed'
    reuse_score = float(record.get('reuse_score', 0.0) or 0.0)
    should_deepen = 1 if record.get('should_deepen') else 0
    hit_frequency = record.get('hit_frequency')
    if hit_frequency is None:
        hit_frequency = max(1, int(round(reuse_score * 10)) if reuse_score > 0 else 1)
    notes = '；'.join(filter(None, [
        str(record.get('notes', '')).strip(),
        f"roi={record.get('roi_signal', '')}".strip(),
    ]))
    source_path = str(record.get('source_path', '')).strip() or str(source)
    return {
        'case_id': case_id,
        'direction_id': direction_id,
        'case_code': case_code,
        'case_title': case_title,
        'case_status': success_failure,
        'sample_quality_score': round(reuse_score * 10, 1),
        'feedback_result': feedback_result,
        'hit_frequency': int(hit_frequency),
        'should_deepen': should_deepen,
        'source_path': source_path,
        'notes': notes,
        'created_at': record.get('recorded_at', now),
        'updated_at': now,
    }


def feedback_case_map_record_from_bridge(record: dict[str, Any], source: Path, now: str) -> dict[str, Any]:
    feedback_id = str(record.get('feedback_id', '')).strip() or f"fb-{source.stem}"
    case_id = str(record.get('case_id', '')).strip() or f"case-{source.stem}"
    direction_id = str(record.get('direction_id', '')).strip()
    source_path = str(record.get('source_path', '')).strip() or str(source)
    notes = str(record.get('notes', '')).strip()
    return {
        'feedback_id': feedback_id,
        'case_id': case_id,
        'direction_id': direction_id,
        'task_type': str(record.get('task_type', 'internal_process_automation_pilot')).strip() or 'internal_process_automation_pilot',
        'workflow_stage': str(record.get('workflow_stage', 'pilot_run')).strip() or 'pilot_run',
        'success_failure': str(record.get('success_failure', 'mixed')).strip() or 'mixed',
        'failure_reason': str(record.get('failure_reason', '')).strip(),
        'human_edits': str(record.get('human_edits', '')).strip(),
        'reuse_score': float(record.get('reuse_score', 0.0) or 0.0),
        'roi_signal': str(record.get('roi_signal', '')).strip(),
        'should_deepen': 1 if record.get('should_deepen') else 0,
        'linked_jd_id': str(record.get('linked_jd_id', '')).strip(),
        'linked_candidate_id': str(record.get('linked_candidate_id', '')).strip(),
        'linked_report_id': str(record.get('linked_report_id', '')).strip(),
        'source_path': source_path,
        'recorded_at': str(record.get('recorded_at', now)).strip() or now,
        'notes': notes,
    }


def upsert_direction_catalog(conn: sqlite3.Connection, record: dict[str, Any], now: str) -> None:
    conn.execute(
        """
        INSERT INTO direction_catalog (
          direction_id, direction_family, direction_name, direction_path, description, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(direction_id) DO UPDATE SET
          direction_family = excluded.direction_family,
          direction_name = excluded.direction_name,
          direction_path = excluded.direction_path,
          description = excluded.description,
          status = excluded.status,
          updated_at = excluded.updated_at
        """,
        (
            record['direction_id'],
            record['direction_family'],
            record['direction_name'],
            record['direction_path'],
            record.get('description', ''),
            record.get('status', 'active'),
            record.get('created_at', now),
            now,
        ),
    )


def upsert_sample_case(conn: sqlite3.Connection, record: dict[str, Any], now: str) -> None:
    conn.execute(
        """
        INSERT INTO sample_case (
          case_id, direction_id, case_code, case_title, case_status, sample_quality_score,
          feedback_result, hit_frequency, should_deepen, source_path, notes, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(case_id) DO UPDATE SET
          direction_id = excluded.direction_id,
          case_code = excluded.case_code,
          case_title = excluded.case_title,
          case_status = excluded.case_status,
          sample_quality_score = excluded.sample_quality_score,
          feedback_result = excluded.feedback_result,
          hit_frequency = excluded.hit_frequency,
          should_deepen = excluded.should_deepen,
          source_path = excluded.source_path,
          notes = excluded.notes,
          updated_at = excluded.updated_at
        """,
        (
            record['case_id'],
            record['direction_id'],
            record['case_code'],
            record['case_title'],
            record['case_status'],
            record['sample_quality_score'],
            record['feedback_result'],
            record['hit_frequency'],
            record['should_deepen'],
            record['source_path'],
            record['notes'],
            record.get('created_at', now),
            record.get('updated_at', now),
        ),
    )


def upsert_feedback_case_map(conn: sqlite3.Connection, record: dict[str, Any], now: str) -> None:
    conn.execute(
        """
        INSERT INTO feedback_case_map (
          feedback_id, case_id, direction_id, task_type, workflow_stage, success_failure, failure_reason,
          human_edits, reuse_score, roi_signal, should_deepen, linked_jd_id, linked_candidate_id,
          linked_report_id, source_path, recorded_at, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(feedback_id) DO UPDATE SET
          case_id = excluded.case_id,
          direction_id = excluded.direction_id,
          task_type = excluded.task_type,
          workflow_stage = excluded.workflow_stage,
          success_failure = excluded.success_failure,
          failure_reason = excluded.failure_reason,
          human_edits = excluded.human_edits,
          reuse_score = excluded.reuse_score,
          roi_signal = excluded.roi_signal,
          should_deepen = excluded.should_deepen,
          linked_jd_id = excluded.linked_jd_id,
          linked_candidate_id = excluded.linked_candidate_id,
          linked_report_id = excluded.linked_report_id,
          source_path = excluded.source_path,
          recorded_at = excluded.recorded_at,
          notes = excluded.notes
        """,
        (
            record['feedback_id'],
            record['case_id'],
            record['direction_id'],
            record['task_type'],
            record['workflow_stage'],
            record['success_failure'],
            record['failure_reason'],
            record['human_edits'],
            record['reuse_score'],
            record['roi_signal'],
            record['should_deepen'],
            record['linked_jd_id'],
            record['linked_candidate_id'],
            record['linked_report_id'],
            record['source_path'],
            record['recorded_at'],
            record['notes'],
        ),
    )


def import_feedback(db_path: Path, sources: list[Path]) -> int:
    now = now_iso()
    count = 0
    with connect(db_path) as conn:
        for source in iter_sources(sources):
            bridge = load_bridge_payload(source)
            feedback_record = bridge.get('feedback_case_map_record')
            if not isinstance(feedback_record, dict):
                raise ValueError(f'{source} does not contain a feedback_case_map_record object')

            direction_record = bridge.get('direction_record')
            if not isinstance(direction_record, dict):
                direction_record = direction_record_from_feedback(feedback_record)
            sample_record = bridge.get('sample_case_record')
            if not isinstance(sample_record, dict):
                sample_record = sample_case_record_from_feedback(feedback_record, source, now)
            feedback_row = feedback_case_map_record_from_bridge(feedback_record, source, now)

            upsert_direction_catalog(conn, direction_record, now)
            upsert_sample_case(conn, sample_record, now)
            upsert_feedback_case_map(conn, feedback_row, now)
            count += 1

        conn.commit()
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description='Build and inspect the direction priority SQLite database.')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB, help='SQLite database path')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init', help='Create and seed the database')
    sub.add_parser('report', help='Print the direction priority report')
    sub.add_parser('feedback', help='Print the feedback-to-case bridge report')
    import_parser = sub.add_parser('import-feedback', help='Import feedback writeback packages from JSON or Markdown')
    import_parser.add_argument('sources', nargs='+', type=Path, help='Feedback package file(s) or directories')
    args = parser.parse_args()

    if args.command == 'init':
        init_db(args.db)
    elif args.command == 'report':
        report(args.db)
    elif args.command == 'feedback':
        feedback_report(args.db)
    elif args.command == 'import-feedback':
        imported = import_feedback(args.db, args.sources)
        print(f'Imported {imported} feedback package(s) into {args.db}')


if __name__ == '__main__':
    main()
