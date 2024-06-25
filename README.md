<p align="center">
  <a href="https://github.com/yuting1214/FastAPIChat">
    <img src="frontend/login/static/favicon.ico" height="50">
  </a>
  <h1 align="center">
    <a href="https://github.com/yuting1214/FastAPIChat">FastAPIChat</a>
  </h1>
</p>

<p align="center">
<a href="https://railway.app/template/_-qAbG?referralCode=jk_FgY">
  <img src="https://railway.app/button.svg" alt="Deploy on Railway" height="30">
</a> 
</p>


FastAPIChat is a powerful application for testing and evaluating large language model based chatbots.
- FastAPIChat powers [LLM Arena](https://gradioapp-production.up.railway.app/arena/), serving over 10+ LLMs, for diverse and dynamic chatbot interactions
- FastAPIChat enables seamlessly rate [LLM](https://gradioapp-production.up.railway.app/chatbot/) generated responses, ensuring continuous improvement based on user feedback.

![Demo of FastAPIChat](https://github.com/yuting1214/FastAPIChat/blob/main/materials/demo.gif)

## News
- [2024/06] 🔥 We released FastAPIChat v1.0.0

<details>
<summary>More</summary>

- [2024/06] We released FastAPIChat v1.0.0 with ChatBot and ChatBot Arena

</details>

<a href="https://chat.lmsys.org"><img src="assets/demo_narrow.gif" width="70%"></a>

## 🎉 Key Features and Integrations
Key features:

* 💬 LLM Chats(10+ LLMs)
* ⚔️ LLM Arena
* 🗳️ Chat Feedback collection
* ⚡ FastAPI API Documentation and Authentication

FastAPIChat integrates seamlessly with Python programs and libraries and includes out-of-the-box integrations for:

- [LangChain](https://docs.chainlit.io/integrations/langchain)
- [OpenRouter](https://openrouter.ai/)
- [Gradio](https://www.gradio.app/)

## Quick-Start 🚀

Note: To begin, you'll need an API key from [OpenRouter](https://openrouter.ai/keys).

### Development Mode

* Note: In Dev mode, the default config with backend is **SQLite**.

1. Clone Repo:

```
git clone https://github.com/yuting1214/FastAPIChat.git
```

2. Configure Virtual Environment (Recommended):
<details>
  
   * Create Virtual Environment
   
     ```
     # macOS/Linux
     # You may need to run `sudo apt-get install python3-venv` first on Debian-based OSs
     python3 -m venv .venv
     
     # Windows
     # You can also use `py -3 -m venv .venv`
     python -m venv .venv
     ```

   * Activate the virtual environment:
     ```
     # macOS/Linux
     source .venv/bin/activate
     
     # Windows
     .venv\Scripts\activate
     ```
</details>
     
3. Install Dependencies:
```
pip install -r requirements.txt
```

4. Update the .env file with

```
USER_NAME=<API_Doc_Username>
PASSWORD=min=<API_Doc_PASSWORD>
OPENROUTER_API_KEY=<Your_API_KEY>
```

5. Run the application:

```
python -m backend.app.main --mode dev 
```

### Production Mode

1. Add extra envs in with your environment configurations:

```
DB_ENGINE=<Your_DB_config>
DB_USERNAME=<Your_DB_config>
DB_PASS=<Your_DB_config>
DB_HOST=<Your_DB_config>
DB_PORT=<Your_DB_config>
DB_NAME=<Your_DB_config>
API_BASE_URL=<Your_Host_URL>
```

2. Run the application:

```
python -m backend.app.main --mode prod
```

* Alternatively, use Dockerfile for deployment.

## App Settings 📋

### Managing Quota

* Control quotas by adjusting limits in `backend/app/core/constants.py`:

```
TEXT_API_QUOTA_LIMIT = <int>
```

### Adding New LLM Models (OpenRouter)

* To add a new LLM model, specify its details in backend/data/llm_models:

```
    {
        'llm_model_name': 'Mixtral 8x22B',
        'llm_vendor': 'Mistral AI',
        'llm_type': 'text',
        'api_provider': 'OpenRouter',
        'api_endpoint': 'mistralai/mixtral-8x22b-instruct',
    }
```

## Features 🌟

1. **Utilize Gradio and FastAPI Integration**: Seamlessly combine Gradio for the frontend display and FastAPI for robust backend functionality, offering a smooth user experience.

2. **Well-Crafted API Management**: Our meticulously designed API ensures efficient data transportation and effective management of API quota usage, providing users with a reliable and hassle-free experience.

3. **Integration of Leading Language Models**: Integrate more than 10+ popular language models from various vendors, including OpenAI, Mistral, Meta and Anthropic, enabling users to leverage cutting-edge AI capabilities for text generation.

4. **Comprehensive Testing and Documentation**: Benefit from comprehensive testing suites and detailed documentation, empowering developers to understand and contribute to the project with ease, ensuring robustness and maintainability.
Third-Party Services: Integrate with third-party APIs for enhanced functionality.

5. **Third-Party Services Integration**: Seamlessly integrates with third-party APIs for enhanced functionality.

## Project Structure 📁

* Project Details: [Heptabase](https://app.heptabase.com/w/80fcc9a0476f3a3ac30ac895c36eef51ede0bc4aa090cb7be1c6c0ed507cfda9)

<details>
<summary>More Project Details</summary>

```
FastAPIChat/
├── backend/                      # Backend directory for the FastAPI application
│   ├── app/                      # Main application directory
│   │   ├── __init__.py           # Initialization file for the app package
│   │   ├── api/                  # Directory for API related code
│   │   │   ├── __init__.py       # Initialization file for the API package
│   │   │   ├── v1/               # Version 1 of the API
│   │   │   │   ├── __init__.py   # Initialization file for the v1 API package
│   │   │   │   ├── endpoints/    # Directory for API endpoint definitions
│   │   │   │   │   ├── __init__.py          # Initialization file for endpoints package
│   │   │   │   │   ├── text_generation.py   # Endpoints for text generation
│   │   │   │   │   ├── llm_management.py    # Endpoints for LLM model management
│   │   │   │   │   ├── api_usage.py         # Endpoints for API usage management
│   │   │   │   │   ├── api_calldetail.py    # Endpoints for API Detail management
│   │   │   │   │   ├── message.py           # Endpoints for messasge management
│   │   │   │   │   ├── chat.py              # Endpoints for chat management
│   │   │   │   │   ├── rating.py            # Endpoints for rating management
│   │   │   │   │   ├── user.py              # Endpoints for user management
│   │   │   │   │   ├── quota.py             # Endpoints for quota management
│   │   │   │   │   ├── doc.py               # Endpoints for OpenAPI doc management
│   │   ├── dependencies/         # Directory for dependency management
│   │   │   ├── __init__.py       # Initialization file for dependencies package
│   │   │   ├── database.py       # Database connection and session management
│   │   │   ├── rate_limiter.py   # Rate limiting logic
│   │   ├── core/                 # Core application logic
│   │   │   ├── __init__.py       # Initialization file for core package
│   │   │   ├── constant.py       # Constant settings
│   │   │   ├── config.py         # Configuration settings
│   │   │   ├── init_setting.py   # Init settings with user's input
│   │   ├── models/               # Directory for SQLAlchemy models
│   │   │   ├── __init__.py       # Initialization file for models package
│   │   │   ├── user.py           # User model
│   │   │   ├── quota.py          # Quota model
│   │   │   ├── message.py        # Message model
│   │   │   ├── api_usage.py      # API usage model
│   │   │   ├── llm.py            # LLM model
│   │   │   ├── chat.py           # Chat model
│   │   │   ├── rating.py         # rating model
│   │   ├── schemas/              # Directory for Pydantic schemas
│   │   │   ├── __init__.py       # Initialization file for schemas package
│   │   │   ├── user.py           # Schemas for user data
│   │   │   ├── quota.py          # Schemas for quota data
│   │   │   ├── message.py        # Schemas for message data
│   │   │   ├── api_usage.py      # Schemas for API usage data
│   │   │   ├── llm.py            # Schemas for LLM model data
│   │   │   ├── llm_message.py    # Schemas for LLM generated output data
│   │   │   ├── chat.py           # Schemas for chat data
│   │   │   ├── rating.py         # Schemas for rating data
│   │   ├── crud/                 # Directory for CRUD operations
│   │   │   ├── __init__.py       # Initialization file for crud package
│   │   │   ├── user.py           # CRUD for user management
│   │   │   ├── quota.py          # CRUD for quota management
│   │   │   ├── message.py        # CRUD for message management
│   │   │   ├── api_usage.py      # CRUD for API usage management
│   │   │   ├── llm.py            # CRUD for LLM model management
│   │   │   ├── llm_message.py    # CRUD for LLM generated output management
│   │   │   ├── chat.py           # CRUD for chat management
│   │   │   ├── rating.py         # CRUD for rating management
│   │   ├── main.py               # Main FastAPI application file
│   ├── data/                     # Directory for data when initiating db
│   │   ├── __init__.py           # Initialization file for data package
│   │   ├── llm_models.py         # LLM models infomation
│   ├── security/                  # New directory for authentication and authorization
│   │   ├── __init__.py            # Initialization file for security package
│   │   ├── authentication.py      # Authentication logic
│   │   ├── authorization.py       # Authorization logic
│   ├── tests/                    # Directory for test files
│   │   ├── __init__.py           # Initialization file for tests package
│   │   ├── test_text_generation.py  # Tests for text generation endpoints
├── frontend/                     # Frontend directory for the Gradio app
│   ├── __init__.py               # Initialization file for frontend package
│   ├── gradio/                   # Main gradio UI directory
│   │   ├── __init__.py           # Initialization file for the gradio package
│   │   ├── text/                 # Directory for ChatBot UI related code
│   │   │   ├── __init__.py       # Initialization file for the text package
│   │   │   ├── event_listeners.py #      
│   │   │   ├── text_generation.py # 
│   │   │   ├── text_generation_arena.py               
│   ├── login/                     # Main login UI directory
│   │   ├── __init__.py           # Initialization file for the gradio package
│   │   ├── static/               # Directory for static files
│   │   │   ├── style.css         # CSS for login UI               
│   │   ├── templates/            # Directory for HTML templates
│   │   │   ├── base.html         # HTML base template
│   │   │   ├── login.html        # HTML login template   
├── llm/
│   ├── __init__.py               # Makes llm a Python package
│   ├── llm_text_chain.py         # Module for LLM text generation integration
│   └── prompt/                   # Folder for prompt handling
│       ├── __init__.py           # Initializes the prompt package
│       ├── base_text_templates.py# Stores base prompt templates for text generation
│       └── examples/             # Directory for few-shot examples used by the chain
│       └── deprecated/           # Directory for deprecated prompts
│   └── vendors/                  # Directory for vendor-specific LLM configurations
│       ├── __init__.py           # Makes vendors a Python package
│       └── openrouter.py         # Configurations and usage for OpenRouter as LLM provider
├── .env                          # Environment variables file
├── .gitignore                    # Git ignore file
├── requirements.txt              # Python dependencies file
├── Dockerfile                    # Docker configuration
├── README.md                     # Project README file
```
</details>

## Future Direction 📝

1. Integraion of local LLM: Integrate with [Ollama](https://github.com/ollama/ollama) to enable users to run LLMs locally and battle with LLMs from API.

2. Integraion of RAG LLM: Enable users to compare different configuration of RAG LLM in LLM Arena.

3. Integration of Redis or other NoSQL Databases: Incorporate Redis or other NoSQL databases to efficiently track and store user history data, enabling personalized experiences and insights for users.

4. History Message Management: Allow user to fetch back the previous messages from database and continue the chat.

5. Rate Limiter: Integrate rate limiter for API protection.

## Contributing 🤝
We welcome contributions from the community! Whether it's bug fixes, feature enhancements, or documentation improvements, feel free to open a pull request.

---

Designed with :heart: by [Mark Chen](https://github.com/yuting1214)
