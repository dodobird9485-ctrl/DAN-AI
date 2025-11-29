# Agent Tools Reference

## Available Tools (23 Total)

### Data & Logic
- **calculate**: Perform mathematical operations (triggers on: +, -, *, /)
- **memory**: Store and retrieve information (triggers on: remember, recall, store, save)
- **logic**: Evaluate conditional statements (triggers on: if, then, condition, logic)

### Classification & Analysis
- **classify**: Categorize input (triggers on: classify, category, type, what kind)
- **summarize**: Condense information (triggers on: summarize, summary, brief, short)
- **sentiment**: Analyze emotional tone (triggers on: sentiment, feeling, emotion, mood)

### External Integration
- **fetch_url**: Request data from websites (triggers on: fetch, url, website, download)
- **database**: Query/store data (triggers on: database, query, store, record)
- **api_call**: Call external APIs (triggers on: api, request, call)
- **file_io**: Read/write files (triggers on: file, read, write, save)

### Text Processing
- **translate**: Convert between languages (triggers on: translate, language, spanish, french)
- **extract**: Pull structured data (triggers on: extract, pull, find, get data)
- **generate**: Create new content (triggers on: generate, create, write, compose)
- **parse_json**: Handle JSON data (triggers on: { in text)

### Advanced Analysis
- **statistics**: Calculate metrics (triggers on: statistics, average, mean, count, total)
- **validate**: Check data integrity (triggers on: validate, check, verify)
- **compare**: Analyze differences (triggers on: compare, difference, vs, versus)

### Execution & Control
- **execute_code**: Run scripts (triggers on: execute, run, code, script)
- **schedule**: Plan future actions (triggers on: schedule, plan, later, remind)
- **audit**: Log agent decisions (always enabled)
- **rate_limit**: Control request frequency (always enabled)

### Search & Reasoning
- **search**: Find information (triggers on: what, who, where, when, search)
- **reason**: Logical reasoning (fallback tool)

## How to Use

### Enable/Disable Tools in Policy

Edit `policy.json`:
```json
"tools_enabled": [
  "calculate",
  "memory",
  "classify"
]
```

### Example Queries

```
Calculate: "What is 5 + 3?"
Memory: "Remember this: my favorite color is blue"
Logic: "If the condition is true then execute"
Classify: "Classify this request"
Summarize: "Summarize this long document"
Translate: "Translate to Spanish"
Extract: "Extract data from this text"
Generate: "Generate a creative story"
Parse JSON: {"name": "John", "age": 30}
Statistics: "Calculate statistics for the dataset"
Validate: "Validate this input"
Compare: "Compare A vs B"
Execute: "Execute this code"
Schedule: "Schedule a meeting tomorrow"
```

## Tool Status

View audit log:
```python
agent.audit_log
```

View stored memory:
```python
agent.memory
```

View request count:
```python
agent.request_count
```
