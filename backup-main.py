
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class SQLAnalysis(BaseModel):
    query_type: str
    tables: list[str]
    columns: list[str]
    joins: list[str]
    complexity: str
    filters: list[str]
    aggregations: list[str]
    group_by: list[str]
    order_by: list[str]
    subqueries: list[str]
    business_purpose: str
    explanation: str
    optimization_tips: list[str]
print("=== SQL Query Explainer ===")
print("Paste your SQL query below.")
print("Enter END on a new line when finished.\n")

lines = []

while True:
    line = input()

    if line.strip().upper() == "END":
        break

    lines.append(line)

sql_query = "\n".join(lines)

if not sql_query.strip():
    print("No SQL query entered.")
    raise SystemExit

print("\nYour SQL query:")
print(sql_query)

response = client.responses.parse(
    model="gpt-4.1-mini",
    instructions=(
        "You are an experienced SQL analyst. "
        "Analyze the SQL query provided by the user. "
        "Identify the query type, tables, columns, "
        "filters, joins, aggregations, GROUP BY, "
        "ORDER BY, and subqueries. "
        "Classify complexity as Beginner, Intermediate, "
        "or Advanced. "
        "Explain the SQL query in simple English. "
        "Describe the likely business purpose of the query. "
        "Provide practical optimization suggestions "
        "when appropriate. "
        "Use empty lists when a feature is not present. "
        "Do not execute the SQL query. "
        "Do not invent tables or columns. "
        "Do not assume business context not supported "
        "by the SQL query. "
        "If business purpose is unclear, say so."
    ),
    input=sql_query,
    text_format=SQLAnalysis
)

result = response.output_parsed

if result is None:
    print("No structured analysis was returned.")
else:
    print("\n===== SQL ANALYSIS =====")

    print("\nQuery Type:", result.query_type)
    print("Tables:", ", ".join(result.tables))
    print("Columns:", ", ".join(result.columns))
    print("Joins:", ", ".join(result.joins) or "None")
    print("Complexity:", result.complexity)
    print("Filters:", ", ".join(result.filters) or "None")
    print("Aggregations:", ", ".join(result.aggregations) or "None")
    print("Group By:", ", ".join(result.group_by) or "None")
    print("Order By:", ", ".join(result.order_by) or "None")
    print("Subqueries:", ", ".join(result.subqueries) or "None")
    print("\nExplanation:")
    print(result.explanation)
    print("\nBusiness Purpose:")
    print(result.business_purpose)
    print("\nOptimization Suggestions:")
    if result.optimization_tips:
     for tip in result.optimization_tips:
        print("-", tip)
    else:
        print("None")

    print("\n========================================")
