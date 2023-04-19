def test_bake_project_default(cookies):
    result = cookies.bake()

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()


def test_bake_project_1_field(cookies):
    result = cookies.bake(
        extra_context={
            "further_fields": {
                "title": {"type": "str", "test_value": "Chess for Zebras"}
            }
        }
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()


def test_bake_project_1_field_no_test_value(cookies):
    result = cookies.bake(extra_context={"further_fields": {"title": {"type": "str"}}})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()


def test_bake_project_2_further_fields(cookies):
    result = cookies.bake(
        extra_context={
            "further_fields": {
                "language": {"type": "str", "test_value": "Python"},
                "number": {"type": "int", "test_value": 42},
            }
        }
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()


def test_bake_project_custom_unique_field(cookies):
    result = cookies.bake(
        {"unique_field": "short_title", "unique_field_test_value": "A Brief History"}
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()
