"""Tests for configuration module."""

import pytest


class TestConfig:
    """Test cases for Config class."""

    def test_validate_missing_token(self):
        """Test validation with missing bot token."""
        from app.config import Config

        # Create a config class with empty token
        Config.BOT_TOKEN = ""

        with pytest.raises(
            ValueError, match="BOT_TOKEN environment variable is required"
        ):
            Config.validate()

    def test_validate_placeholder_token(self):
        """Test validation with placeholder token."""
        from app.config import Config

        # Create a config class with placeholder token
        Config.BOT_TOKEN = "your_bot_token_here"

        with pytest.raises(ValueError, match="Please set a real BOT_TOKEN"):
            Config.validate()

    def test_validate_valid_token(self):
        """Test validation with valid token."""
        from app.config import Config

        # Create a config class with valid token
        Config.BOT_TOKEN = "real_token_123"

        # Should not raise any exception
        Config.validate()

    def test_config_attributes_exist(self):
        """Test that config has all required attributes."""
        from app.config import config

        # Check that all required attributes exist
        assert hasattr(config, "BOT_TOKEN")
        assert hasattr(config, "API_HOST")
        assert hasattr(config, "API_PORT")
        assert hasattr(config, "MAX_VACANCIES")
        assert hasattr(config, "NOTIFICATION_USER_ID")

        # Check that validate method exists
        assert hasattr(config, "validate")
        assert callable(config.validate)
