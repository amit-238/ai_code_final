LANGUAGES = [
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C",
    "Go", "Rust", "Swift", "Kotlin", "Ruby", "PHP",
    "SQL", "Bash", "HTML/CSS", "R", "Dart", "Scala",
]

MODELS = {
    "Gemini 2.5 Flash (Fast)": "models/gemini-2.5-flash",
    "Gemini 2.5 Pro (Smart)":  "models/gemini-2.5-pro",
}

MODEL = "models/gemini-2.5-flash"

MAX_TOKENS = 2048

SYSTEM_PROMPT = (
    "You are an expert programmer. Generate clean, well-commented, "
    "production-ready code. Return only the code block with no extra explanation "
    "unless the user explicitly asks for it."
)

LEVELS = ["beginner", "intermediate", "production"]

EXAMPLES = [
    "A REST API endpoint that validates email addresses",
    "A recursive Fibonacci function with memoization",
    "A class that reads and parses a CSV file",
    "A CLI tool that renames files in a folder by date",
]

LANG_COLORS = {
    "python": "#3572A5",
    "javascript": "#F7DF1E",
    "typescript": "#2B7489",
    "java": "#b07219",
    "c++": "#f34b7d",
    "c": "#555555",
    "go": "#00ADD8",
    "rust": "#DEA584",
    "swift": "#F05138",
    "kotlin": "#A97BFF",
    "ruby": "#701516",
    "php": "#4F5D95",
    "sql": "#e38c00",
    "bash": "#89e051",
    "html/css": "#e34c26",
    "r": "#198CE7",
    "dart": "#00B4AB",
    "scala": "#DC322F",
}
