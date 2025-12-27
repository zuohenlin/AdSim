"""
系统配置接口（仅本地调试使用）
"""

import os

from flask import request

from . import system_bp
from ..config import Config, project_root_env


def _update_env_file(env_path, updates):
    lines = []
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

    found = {key: False for key in updates.keys()}
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or '=' not in stripped:
            new_lines.append(line)
            continue
        key, _ = stripped.split('=', 1)
        if key in updates:
            new_lines.append(f"{key}={updates[key]}\n")
            found[key] = True
        else:
            new_lines.append(line)

    for key, value in updates.items():
        if not found.get(key):
            new_lines.append(f"{key}={value}\n")

    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)


@system_bp.route('/llm-config', methods=['POST'])
def update_llm_config():
    if not Config.DEBUG:
        return {"success": False, "error": "Only available in debug mode"}, 403

    payload = request.get_json(silent=True) or {}
    api_key = (payload.get('api_key') or '').strip()
    base_url = (payload.get('base_url') or '').strip()
    model_name = (payload.get('model_name') or '').strip()
    zep_api_key = (payload.get('zep_api_key') or '').strip()
    boost_api_key = (payload.get('boost_api_key') or '').strip()
    boost_base_url = (payload.get('boost_base_url') or '').strip()
    boost_model_name = (payload.get('boost_model_name') or '').strip()

    if not api_key:
        return {"success": False, "error": "api_key is required"}, 400

    updates = {"LLM_API_KEY": api_key}
    if base_url:
        updates["LLM_BASE_URL"] = base_url
    if model_name:
        updates["LLM_MODEL_NAME"] = model_name
    if zep_api_key:
        updates["ZEP_API_KEY"] = zep_api_key
    if boost_api_key:
        updates["LLM_BOOST_API_KEY"] = boost_api_key
    if boost_base_url:
        updates["LLM_BOOST_BASE_URL"] = boost_base_url
    if boost_model_name:
        updates["LLM_BOOST_MODEL_NAME"] = boost_model_name

    _update_env_file(project_root_env, updates)

    os.environ["LLM_API_KEY"] = api_key
    Config.LLM_API_KEY = api_key
    if base_url:
        os.environ["LLM_BASE_URL"] = base_url
        Config.LLM_BASE_URL = base_url
    if model_name:
        os.environ["LLM_MODEL_NAME"] = model_name
        Config.LLM_MODEL_NAME = model_name
    if zep_api_key:
        os.environ["ZEP_API_KEY"] = zep_api_key
        Config.ZEP_API_KEY = zep_api_key

    masked = api_key[:4] + "****" if len(api_key) >= 4 else "****"
    return {
        "success": True,
        "data": {
            "updated": list(updates.keys()),
            "api_key": masked,
            "base_url": base_url or Config.LLM_BASE_URL,
            "model_name": model_name or Config.LLM_MODEL_NAME
        }
    }
