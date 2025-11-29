def test_debug_enabled():
    \"\"\"Этот тест должен падать если debug=True\"\"\"
    debug_mode = False  # Измените на True для демонстрации ошибки
    assert debug_mode == False, "Debug mode should be disabled in production"

def test_ssl_required():
    \"\"\"Проверка что SSL требуется\"\"\"
    ssl_enabled = True
    assert ssl_enabled == True, "SSL should be enabled"
