# Contributing Guidelines

Thank you for your interest in contributing to the Django Portfolio project!

## Code Style

### Python Code
- Use **tabs for indentation** (not spaces)
- Follow PEP 8 guidelines for naming conventions
- Use descriptive variable names that indicate their purpose
- Keep functions focused and single-purpose

### Documentation
- All classes must have docstrings explaining their purpose
- All functions must have docstrings with:
  - Brief description of what the function does
  - Args section listing parameters
  - Returns section describing return values
  - Any important notes or warnings

### Example:
```python
def calculate_distance(point_a, point_b):
	"""
	Calculate the distance between two geographic points.
	
	Args:
		point_a: PostGIS Point geometry for first location
		point_b: PostGIS Point geometry for second location
		
	Returns:
		float: Distance in meters between the two points
		
	Note:
		Uses geography=True for accurate Earth-surface calculations
	"""
	return point_a.distance(point_b)
```

## Git Workflow

### Commit Messages
Write clear, meaningful commit messages that explain the intent of your changes:

**Good examples:**
- `Add user profile model with PostGIS location field`
- `Implement role-based filtering in GeoJSON API`
- `Fix coordinate order in Point geometry construction`

**Bad examples:**
- `Update files`
- `Fix bug`
- `Changes`

### Commit Structure
- Each commit should represent a logical unit of work
- Don't combine unrelated changes in a single commit
- Test your changes before committing

### Branch Naming
- `feature/description` - For new features
- `fix/description` - For bug fixes
- `docs/description` - For documentation updates

## Testing

### Writing Tests
- Write tests for all new features
- Ensure tests cover both success and failure cases
- Test edge cases and boundary conditions
- Use descriptive test method names

### Running Tests
Before submitting a pull request, ensure all tests pass:

```bash
# With Docker
docker compose run --rm web bash -lc "python manage.py test -v 2"

# Locally
python manage.py test -v 2
```

### Test Coverage
Aim for high test coverage:
- Models: Test field validation, relationships, methods
- Views: Test authentication, permissions, data filtering
- Forms: Test validation, data cleaning, error handling
- Signals: Test automatic behaviors

## Pull Request Process

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the code style guidelines
3. **Add tests** for any new functionality
4. **Update documentation** (README, docstrings, comments)
5. **Run tests** to ensure everything passes
6. **Commit your changes** with clear, descriptive messages
7. **Push to your fork** and submit a pull request

### Pull Request Template
When creating a PR, include:
- **Description**: What does this PR do?
- **Motivation**: Why is this change needed?
- **Testing**: How was this tested?
- **Screenshots**: If applicable, add screenshots
- **Checklist**:
  - [ ] Tests pass
  - [ ] Documentation updated
  - [ ] Code follows style guidelines
  - [ ] Commit messages are clear

## Development Setup

See the [README.md](README.md) for detailed setup instructions.

### Quick Start
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/django-portfolio.git
cd django-portfolio

# Start with Docker
docker compose up --build

# Create migrations and superuser
docker compose exec web python manage.py makemigrations profiles
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser

# Run tests
docker compose exec web python manage.py test -v 2
```

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

### What We Look For
- **Functionality**: Does it work as intended?
- **Code Quality**: Is it clean, readable, and maintainable?
- **Documentation**: Are changes well-documented?
- **Tests**: Are there adequate tests?
- **Style**: Does it follow our guidelines?

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Ask in your pull request
- Review existing code for examples

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
