from pytest_cookies.plugin import Result


def test_bake_with_defaults(default_project: Result) -> None:
    result = default_project
    assert result.exception is None
    assert result.exit_code == 0
    assert result.project_path.is_dir()
    assert result.project_path.name == "salamander"

    root_files = [f.name for f in result.project_path.iterdir()]
    assert ".env" in root_files
    assert "docker-compose.yaml" in root_files


def test_bake_without_lint(project_salaman: Result) -> None:
    result = project_salaman

    assert result.exception is None
    assert result.exit_code == 0
