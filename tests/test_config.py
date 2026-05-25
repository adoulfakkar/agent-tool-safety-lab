from agent_tool_safety_lab.config import load_settings


def test_defaults_to_local_mock_friendly_settings(monkeypatch):
    monkeypatch.delenv("ATSL_RUNTIME_MODE", raising=False)
    monkeypatch.delenv("ATSL_LLM_PROVIDER", raising=False)

    settings = load_settings()

    assert settings.runtime_mode == "local"
    assert settings.llm_provider == "ollama"
    assert settings.llm_base_url == "https://ollama.com"


def test_reads_huggingface_settings(monkeypatch):
    monkeypatch.setenv("ATSL_LLM_PROVIDER", "huggingface")
    monkeypatch.setenv("ATSL_HUGGINGFACE_API_KEY", "secret-test-key")
    monkeypatch.setenv("ATSL_HUGGINGFACE_MODEL", "test/model")

    settings = load_settings()

    assert settings.llm_provider == "huggingface"
    assert settings.llm_model == "test/model"
    assert settings.llm_api_key == "secret-test-key"


def test_loads_local_env_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("ATSL_OLLAMA_API_KEY", raising=False)
    (tmp_path / ".env").write_text("ATSL_OLLAMA_API_KEY=local-secret\n")

    settings = load_settings()

    assert settings.llm_api_key == "local-secret"
