#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import uuid
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
APP_DIR = Path(__file__).resolve().parent
WEB_FILE = APP_DIR / 'index.html'
DATA_DIR = APP_DIR / 'data'
RUNTIME_DIR = DATA_DIR / 'runtime'
RUNS_JSONL = RUNTIME_DIR / 'runs.jsonl'
FEEDBACK_DIR = ROOT / 'feedback' / 'reviews' / 'ai-application-engineer'
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '-', value)
    value = re.sub(r'-{2,}', '-', value).strip('-')
    return value or 'pilot'


def read_json(request_handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    length = int(request_handler.headers.get('Content-Length', '0'))
    raw = request_handler.rfile.read(length) if length else b'{}'
    try:
        return json.loads(raw.decode('utf-8')) if raw else {}
    except json.JSONDecodeError as exc:
        raise ValueError(f'Invalid JSON payload: {exc}') from exc


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + '\n')


def load_history() -> list[dict[str, Any]]:
    if not RUNS_JSONL.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in RUNS_JSONL.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows[-20:][::-1]


def default_payload() -> dict[str, Any]:
    return {
        'pilot_id': 'pilot-ifw-20260405-001',
        'pilot_name': '采购审批预审与分流试点',
        'direction_id': 'dir-aie-internal-process-automation',
        'direction_path': 'AI 应用工程师 / 内部流程自动化',
        'process_name': '采购申请预审',
        'business_department': '采购 / 运营',
        'business_owner': '业务 owner',
        'technical_owner': 'AI 应用工程师',
        'requester': '张三',
        'system_of_record': 'OA 审批系统',
        'secondary_systems': 'ERP 供应商主数据 / 工单系统',
        'intake_channel': '表单',
        'request_summary': '采购申请进入审批前，先做字段完整性检查、政策规则预审和责任人分流。',
        'policy_anchor': '金额、供应商、合同条款、预算科目必须复核。',
        'target_users': '采购专员 / 运营同学 / 业务 owner',
        'success_standard': '把人工整理与来回确认从一轮压缩到一次，并保持可审计回写。',
        'current_baseline_minutes': '8',
        'target_minutes': '3',
        'expected_volume_per_week': '30',
        'data_sensitivity': 'medium',
        'risk_level': 'medium',
        'human_gate': '高风险字段确认 + 最终提交前复核',
        'fallback_owner': '采购主管或业务 owner',
        'fallback_plan': '低置信度时只出草稿，不自动提交；缺字段则退回补充。',
        'writeback_target': 'OA 审批备注 + 试点证据回流包',
        'audit_path': 'repo/feedback/reviews/ai-application-engineer/',
        'trial_mode': 'shadow_mode',
        'baseline_error_rate': '0.12',
        'baseline_rework_rate': '0.20',
        'baseline_human_touches': '2',
        'evidence_baseline': '历史审批单、旧版 SOP、工单截图',
        'evidence_artifacts': '输入表单、AI 初稿、人工修改痕迹、最终回写结果、审计日志',
        'run_notes': '先跑 shadow mode，确认字段完整度与人审点稳定后再考虑小范围上线。',
        'case_id': 'aie-ifw-pilot-001',
        'human_confirmation_status': 'pending',
        'human_confirmation_notes': '',
        'final_decision': 'needs_more_info',
        'final_decision_reason': '',
        'accepted': False,
        'score': '7.8',
        'failure_reason': '',
        'human_edits': '',
        'reuse_score': '0.78',
        'roi_signal': '节省采购申请整理与补字段时间',
        'should_deepen': True,
        'collector': 'pilot-ui',
    }


def parse_int(value: Any, fallback: int = 0) -> int:
    try:
        return int(str(value).strip())
    except Exception:
        return fallback


def parse_float(value: Any, fallback: float = 0.0) -> float:
    try:
        return float(str(value).strip())
    except Exception:
        return fallback


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    required_fields = [
        'pilot_id',
        'pilot_name',
        'process_name',
        'system_of_record',
        'business_owner',
        'request_summary',
        'policy_anchor',
        'human_gate',
        'fallback_owner',
        'writeback_target',
        'audit_path',
        'current_baseline_minutes',
        'target_minutes',
        'expected_volume_per_week',
        'trial_mode',
    ]
    completeness_hits = sum(1 for key in required_fields if str(payload.get(key, '')).strip())
    completeness = round(completeness_hits / len(required_fields), 2)

    baseline_minutes = parse_int(payload.get('current_baseline_minutes'), 0)
    target_minutes = parse_int(payload.get('target_minutes'), 0)
    weekly_volume = parse_int(payload.get('expected_volume_per_week'), 0)
    time_saved_per_case = max(0, baseline_minutes - target_minutes)
    weekly_time_saved = time_saved_per_case * weekly_volume

    risk_level = str(payload.get('risk_level', 'medium')).strip().lower()
    data_sensitivity = str(payload.get('data_sensitivity', 'medium')).strip().lower()
    trial_mode = str(payload.get('trial_mode', 'shadow_mode')).strip().lower()
    system_of_record = str(payload.get('system_of_record', '')).strip()
    fallback_owner = str(payload.get('fallback_owner', '')).strip()
    human_gate = str(payload.get('human_gate', '')).strip()
    policy_anchor = str(payload.get('policy_anchor', '')).strip()

    missing = [key for key in required_fields if not str(payload.get(key, '')).strip()]
    blockers: list[str] = []
    if not system_of_record:
        blockers.append('system_of_record 未明确')
    if not human_gate:
        blockers.append('人工确认点未明确')
    if not fallback_owner:
        blockers.append('fallback 责任人未明确')
    if not policy_anchor:
        blockers.append('政策规则锚点未明确')

    if blockers or completeness < 0.7:
        verdict = 'needs_more_info'
        confidence = 0.58
    elif completeness < 0.9 or risk_level == 'high' or data_sensitivity == 'high':
        verdict = 'shadow_mode_only'
        confidence = 0.72
    else:
        verdict = 'ready_for_pilot'
        confidence = 0.86

    if trial_mode == 'shadow_mode':
        pilot_recommendation = '先 shadow mode 跑 1 个业务周期，再决定是否扩大范围。'
    elif verdict == 'ready_for_pilot':
        pilot_recommendation = '可以进入小范围试点，但高风险字段仍要人工确认。'
    else:
        pilot_recommendation = '先补齐关键信息，不要直接进入试点。'

    human_review_points = [
        '确认 system of record 是 OA / ERP，而不是本地草稿。',
        '确认高风险字段（金额 / 供应商 / 合同条款）必须人工复核。',
        '确认 fallback_owner 在异常时能接住请求。',
        '确认写回路径只在人工确认后提交。',
    ]
    if data_sensitivity == 'high':
        human_review_points.append('高敏感数据不进入自动通过路径。')

    writeback_path = [
        'UI 提交试点输入',
        '服务端生成运行记录与评估结果',
        '保存到 apps/internal-process-automation-pilot/data/runtime/',
        '导出反馈回写包到 feedback/reviews/ai-application-engineer/',
        '可再整理进 data/direction-priority-db/ 作为方向优先级输入',
    ]

    return {
        'verdict': verdict,
        'confidence': confidence,
        'completeness': completeness,
        'missing_fields': missing,
        'blockers': blockers,
        'pilot_recommendation': pilot_recommendation,
        'human_review_points': human_review_points,
        'writeback_path': writeback_path,
        'metrics': {
            'baseline_minutes': baseline_minutes,
            'target_minutes': target_minutes,
            'time_saved_per_case': time_saved_per_case,
            'weekly_volume': weekly_volume,
            'estimated_weekly_time_saved': weekly_time_saved,
            'baseline_error_rate': parse_float(payload.get('baseline_error_rate'), 0.0),
            'baseline_rework_rate': parse_float(payload.get('baseline_rework_rate'), 0.0),
            'baseline_human_touches': parse_float(payload.get('baseline_human_touches'), 0.0),
        },
        'system_of_record': system_of_record,
        'risk_summary': {
            'risk_level': risk_level,
            'data_sensitivity': data_sensitivity,
            'trial_mode': trial_mode,
            'fallback_owner': fallback_owner,
        },
    }


def make_markdown_bundle(run: dict[str, Any]) -> str:
    p = run['payload']
    e = run['evaluation']
    h = run['human_confirmation']
    f = run['feedback']
    ev = run['evidence']
    lines = [
        f"# {p.get('pilot_name', '内部流程自动化试点')} 回写包",
        '',
        f"- 试点编号：{p.get('pilot_id', '')}",
        f"- 方向：{p.get('direction_path', '')}",
        f"- 流程名称：{p.get('process_name', '')}",
        f"- system of record：{p.get('system_of_record', '')}",
        f"- 试点结论：{e['verdict']}",
        f"- 置信度：{e['confidence']}",
        f"- 完整度：{e['completeness']}",
        '',
        '## 试点输入',
        f"- 业务部门：{p.get('business_department', '')}",
        f"- 业务 owner：{p.get('business_owner', '')}",
        f"- 请求摘要：{p.get('request_summary', '')}",
        f"- 政策锚点：{p.get('policy_anchor', '')}",
        f"- 人工确认点：{p.get('human_gate', '')}",
        f"- fallback owner：{p.get('fallback_owner', '')}",
        f"- 写回目标：{p.get('writeback_target', '')}",
        '',
        '## 运行结果',
        f"- 推荐：{e['pilot_recommendation']}",
        f"- 缺失字段：{', '.join(e['missing_fields']) or '无'}",
        f"- 阻塞项：{', '.join(e['blockers']) or '无'}",
        f"- 审核点：{'；'.join(e['human_review_points'])}",
        '',
        '## 人工确认',
        f"- 状态：{h.get('status', '')}",
        f"- 备注：{h.get('notes', '')}",
        '',
        '## 反馈回写',
        f"- case_id：{f.get('case_id', '')}",
        f"- direction_id：{f.get('direction_id', '')}",
        f"- success_failure：{f.get('success_failure', '')}",
        f"- reuse_score：{f.get('reuse_score', '')}",
        f"- roi_signal：{f.get('roi_signal', '')}",
        f"- should_deepen：{f.get('should_deepen', '')}",
        '',
        '## 试点证据记录',
        f"- 基线：{ev.get('baseline', '')}",
        f"- 结果摘要：{ev.get('notes', '')}",
        f"- 附件：{ev.get('artifacts', '')}",
        f"- 审计路径：{p.get('audit_path', '')}",
        '',
        '## 回写路径',
        *[f"- {item}" for item in e['writeback_path']],
    ]
    return '\n'.join(lines).strip() + '\n'


def save_run(payload: dict[str, Any], evaluation: dict[str, Any]) -> dict[str, Any]:
    run_id = f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
    human_confirmation = {
        'status': str(payload.get('human_confirmation_status', 'pending')).strip() or 'pending',
        'notes': str(payload.get('human_confirmation_notes', '')).strip(),
    }
    feedback = {
        'case_id': str(payload.get('case_id', '')).strip() or 'aie-ifw-pilot-001',
        'direction_id': str(payload.get('direction_id', '')).strip() or 'dir-aie-internal-process-automation',
        'direction_path': str(payload.get('direction_path', '')).strip() or 'AI 应用工程师 / 内部流程自动化',
        'success_failure': str(payload.get('success_failure', 'mixed')).strip() or 'mixed',
        'failure_reason': str(payload.get('failure_reason', '')).strip(),
        'human_edits': str(payload.get('human_edits', '')).strip(),
        'reuse_score': parse_float(payload.get('reuse_score'), 0.0),
        'roi_signal': str(payload.get('roi_signal', '')).strip(),
        'should_deepen': 1 if str(payload.get('should_deepen', 'true')).lower() in {'1', 'true', 'yes', 'on'} else 0,
        'accepted': bool(payload.get('accepted', False)),
        'score': parse_float(payload.get('score'), 0.0),
        'final_decision': str(payload.get('final_decision', 'needs_more_info')).strip(),
        'final_decision_reason': str(payload.get('final_decision_reason', '')).strip(),
        'collector': str(payload.get('collector', 'pilot-ui')).strip() or 'pilot-ui',
    }
    evidence = {
        'baseline': str(payload.get('evidence_baseline', '')).strip(),
        'artifacts': str(payload.get('evidence_artifacts', '')).strip(),
        'notes': str(payload.get('run_notes', '')).strip(),
    }
    run = {
        'id': run_id,
        'created_at': now_iso(),
        'payload': payload,
        'evaluation': evaluation,
        'human_confirmation': human_confirmation,
        'feedback': feedback,
        'evidence': evidence,
    }

    runtime_json = RUNTIME_DIR / f'{run_id}.json'
    runtime_md = RUNTIME_DIR / f'{run_id}.md'
    feedback_json = FEEDBACK_DIR / f'internal-process-pilot-{run_id}.json'
    feedback_md = FEEDBACK_DIR / f'internal-process-pilot-{run_id}.md'

    write_json(runtime_json, run)
    runtime_md.write_text(make_markdown_bundle(run), encoding='utf-8')
    append_jsonl(RUNS_JSONL, run)
    write_json(feedback_json, run)
    feedback_md.write_text(make_markdown_bundle(run), encoding='utf-8')

    return {
        'run': run,
        'files': {
            'runtime_json': str(runtime_json.relative_to(ROOT)),
            'runtime_md': str(runtime_md.relative_to(ROOT)),
            'feedback_json': str(feedback_json.relative_to(ROOT)),
            'feedback_md': str(feedback_md.relative_to(ROOT)),
            'jsonl': str(RUNS_JSONL.relative_to(ROOT)),
        },
    }


class Handler(BaseHTTPRequestHandler):
    server_version = 'InternalProcessPilot/0.1'

    def _send(self, status: int, body: bytes, content_type: str = 'application/json; charset=utf-8') -> None:
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        self._send(status, json.dumps(payload, ensure_ascii=False, indent=2).encode('utf-8'))

    def log_message(self, fmt: str, *args: Any) -> None:
        return

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == '/':
            html = WEB_FILE.read_text(encoding='utf-8')
            self._send(HTTPStatus.OK, html.encode('utf-8'), 'text/html; charset=utf-8')
            return
        if parsed.path == '/api/defaults':
            self._json(HTTPStatus.OK, default_payload())
            return
        if parsed.path == '/api/history':
            self._json(HTTPStatus.OK, {'items': load_history()})
            return
        if parsed.path.startswith('/api/artifact/'):
            rel = parsed.path.removeprefix('/api/artifact/').lstrip('/')
            target = (ROOT / rel).resolve()
            if ROOT not in target.parents and target != ROOT:
                self._json(HTTPStatus.FORBIDDEN, {'error': 'invalid path'})
                return
            if not target.exists():
                self._json(HTTPStatus.NOT_FOUND, {'error': 'not found'})
                return
            data = target.read_text(encoding='utf-8')
            ctype = 'application/json; charset=utf-8' if target.suffix == '.json' else 'text/markdown; charset=utf-8'
            self._send(HTTPStatus.OK, data.encode('utf-8'), ctype)
            return
        self._json(HTTPStatus.NOT_FOUND, {'error': 'not found'})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        try:
            payload = read_json(self)
        except ValueError as exc:
            self._json(HTTPStatus.BAD_REQUEST, {'error': str(exc)})
            return

        if parsed.path == '/api/evaluate':
            self._json(HTTPStatus.OK, evaluate(payload))
            return
        if parsed.path == '/api/save':
            evaluation = payload.get('evaluation') if isinstance(payload.get('evaluation'), dict) else evaluate(payload)
            saved = save_run(payload, evaluation)
            self._json(HTTPStatus.OK, {'ok': True, **saved})
            return
        self._json(HTTPStatus.NOT_FOUND, {'error': 'not found'})


def main() -> None:
    parser = argparse.ArgumentParser(description='Local pilot UI for internal process automation.')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f'Internal process automation pilot UI running at http://{args.host}:{args.port}')
    print(f'Runtime files: {RUNTIME_DIR.relative_to(ROOT)}')
    print(f'Feedback writeback: {FEEDBACK_DIR.relative_to(ROOT)}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
