"""Tests for data models."""

import pytest
from pydantic import ValidationError

from app.models import Vacancy


class TestVacancy:
    """Test cases for Vacancy model."""

    def test_valid_vacancy(self):
        """Test creating a valid vacancy."""
        vacancy_data = {
            "title": "Python Developer",
            "salary": "100000-150000 USD",
            "url": "https://example.com/job/123",
        }

        vacancy = Vacancy(**vacancy_data)
        assert vacancy.title == "Python Developer"
        assert vacancy.salary == "100000-150000 USD"
        assert str(vacancy.url) == "https://example.com/job/123"

    def test_vacancy_with_optional_fields(self):
        """Test creating vacancy with optional fields."""
        vacancy_data = {
            "title": "Developer",
            "salary": "50000-70000 USD",
            "url": "https://example.com/job/456",
        }

        vacancy = Vacancy(**vacancy_data)
        assert vacancy.title == "Developer"
        assert vacancy.salary == "50000-70000 USD"

    def test_invalid_vacancy_missing_required(self):
        """Test creating vacancy with missing required fields."""
        vacancy_data = {
            "title": "Developer",
            # Missing required fields
        }

        with pytest.raises(ValidationError):
            Vacancy(**vacancy_data)

    def test_vacancy_str_representation(self):
        """Test string representation of vacancy."""
        vacancy_data = {
            "title": "Python Developer",
            "salary": "100000-150000 USD",
            "url": "https://example.com/job/123",
        }

        vacancy = Vacancy(**vacancy_data)
        str_repr = str(vacancy)
        assert "Python Developer" in str_repr
        assert "100000-150000 USD" in str_repr
