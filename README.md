# FoodieSpot Reservation Chatbot

A conversational AI agent for managing restaurant reservations across multiple locations.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/foodiespot.git
cd foodiespot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```
LLM_API_KEY=your_api_key_here
LLM_API_URL=your_api_url_here
ENVIRONMENT=development
```

5. Run the application:
```bash
streamlit run app/main.py
```

## Project Structure

- `app/`: Main application code and configuration
- `core/`: Core functionality (LLM integration, tool management)
- `models/`: Data models and schemas
- `tools/`: Tool implementations
- `utils/`: Helper functions and utilities
- `data/`: Data storage
- `tests/`: Test suites
- `docs/`: Documentation

## Development

1. Create new tools in the `tools/` directory
2. Add models in the `models/` directory
3. Update prompts in `core/llm_manager.py`
4. Add utility functions in `utils/`

## Testing

Run tests using pytest:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License