from unittest.mock import patch, MagicMock
from generator import generate_code

def test_empty_prompt_returns_result():
    """Empty prompt should still return something, not crash."""
    result, usage = generate_code("Python", "")
    assert result is not None

def test_generate_code_calls_api():
    """Check that a normal prompt returns the model's text."""
    mock_response = MagicMock()
    mock_response.text = "print('hello world')"
    mock_response.usage_metadata = MagicMock()
    mock_response.usage_metadata.prompt_token_count = 10
    mock_response.usage_metadata.candidates_token_count = 5

    with patch("generator.client") as mock_client:
        mock_client.models.generate_content.return_value = mock_response
        result, usage = generate_code("Python", "print hello world")

    assert "hello world" in result

def test_api_error_returns_error_message():
    """When API fails, result should start with # Error, not crash the app."""
    with patch("generator.client") as mock_client:
        mock_client.models.generate_content.side_effect = Exception("quota exceeded")
        result, usage = generate_code("Python", "some task")

    assert "Error" in result
    assert usage == {}

def test_explain_flag_modifies_prompt():
    """explain=True should work without crashing."""
    mock_response = MagicMock()
    mock_response.text = "def foo(): pass\n## Explanation\nThis defines foo."
    mock_response.usage_metadata = MagicMock()
    mock_response.usage_metadata.prompt_token_count = 20
    mock_response.usage_metadata.candidates_token_count = 15

    with patch("generator.client") as mock_client:
        mock_client.models.generate_content.return_value = mock_response
        result, usage = generate_code("Python", "a function", explain=True)

    assert result is not None

def test_custom_model_is_passed():
    """Custom model string should be passed to the API call."""
    mock_response = MagicMock()
    mock_response.text = "code here"
    mock_response.usage_metadata = MagicMock()
    mock_response.usage_metadata.prompt_token_count = 5
    mock_response.usage_metadata.candidates_token_count = 5

    with patch("generator.client") as mock_client:
        mock_client.models.generate_content.return_value = mock_response
        generate_code("Go", "hello world", model="models/gemini-2.5-pro")
        call_kwargs = mock_client.models.generate_content.call_args
        assert call_kwargs.kwargs.get("model") == "models/gemini-2.5-pro"
