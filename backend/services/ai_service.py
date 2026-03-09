"""
AI service — thin wrapper around LiteLLM.
Swap provider by changing AI_PROVIDER in .env:
  AI_PROVIDER=claude  →  uses claude-sonnet-4-6 via Anthropic API
  AI_PROVIDER=ollama  →  uses local Ollama (model set in OLLAMA_MODEL)
"""
import litellm
from core.config import settings


def _model_id() -> str:
    if settings.AI_PROVIDER == "claude":
        return "claude-sonnet-4-6"
    # LiteLLM format for Ollama: "ollama/<model>"
    return f"ollama/{settings.OLLAMA_MODEL}"


def _base_url() -> str | None:
    if settings.AI_PROVIDER == "ollama":
        return settings.OLLAMA_BASE_URL
    return None


async def chat(
    messages: list[dict],
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> str:
    """Send a chat completion request and return the text response."""
    kwargs: dict = dict(
        model=_model_id(),
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    if settings.AI_PROVIDER == "claude":
        kwargs["api_key"] = settings.ANTHROPIC_API_KEY
    if _base_url():
        kwargs["api_base"] = _base_url()

    response = await litellm.acompletion(**kwargs)
    return response.choices[0].message.content


async def meal_suggestions(
    user_name: str,
    top_ingredients: list[str],
    daily_carb_goal: float,
    meal_type: str = "any",
    extra_context: str = "",
) -> str:
    """Ask the AI for personalized meal suggestions."""
    system = (
        "You are a knowledgeable ketogenic diet assistant. "
        "You provide practical, evidence-based meal suggestions that keep net carbs low. "
        "Be concise and friendly."
    )
    prompt = (
        f"Please suggest 3 keto-friendly {meal_type} meal ideas for {user_name}. "
        f"Their daily net carb goal is {daily_carb_goal}g. "
        f"Their highest-rated ingredients include: {', '.join(top_ingredients)}. "
        f"{'Additional context: ' + extra_context if extra_context else ''}"
        "For each meal, include: name, brief description, estimated net carbs, and key ingredients."
    )
    return await chat([{"role": "system", "content": system}, {"role": "user", "content": prompt}])


async def interpret_lab_results(raw_text: str, user_context: str = "") -> str:
    """Ask the AI to interpret lab results in the context of a keto diet."""
    system = (
        "You are a medical information assistant with expertise in ketogenic diets and metabolism. "
        "Provide clear, helpful interpretations of lab results. "
        "Always recommend consulting a healthcare provider for medical decisions. "
        "Be thorough but accessible — avoid jargon when possible."
    )
    prompt = (
        f"Please interpret the following lab results for a person following a ketogenic diet.\n\n"
        f"Lab results:\n{raw_text}\n\n"
        f"{'User context: ' + user_context if user_context else ''}\n\n"
        "Provide: (1) a plain-English summary of key values, (2) any values outside normal range, "
        "(3) keto-specific considerations, (4) questions to ask their doctor."
    )
    return await chat(
        [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        max_tokens=2048,
    )


async def research_summary(topic: str) -> str:
    """Ask the AI to summarize recent findings on a keto-related topic."""
    system = (
        "You are a research assistant specializing in ketogenic diets, metabolic health, "
        "and related medications/supplements. Summarize the current scientific consensus "
        "and any recent developments. Be evidence-based and note the strength of evidence."
    )
    prompt = (
        f"Please provide a current research summary on: {topic}\n"
        "Include: key findings, practical recommendations, and any important caveats or controversies."
    )
    return await chat(
        [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        max_tokens=2048,
    )
