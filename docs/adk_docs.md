Okay, I will organize the provided text content from the various ADK documentation pages into a single Markdown file with clear headers per chapter. I'll ensure to deduplicate content where it's repeated and format it neatly.

```markdown
# Agent Development Kit (ADK) Documentation

## 1. Overview

### Google I/O'25 - ADK updates
Big news!
Introducing Java ADK v0.1.0 , extending agent capabilities to the Java ecosystem.
Python ADK is officially v1.0.0 offering stability for production-ready agents.

### What is Agent Development Kit?
Agent Development Kit (ADK) is a flexible and modular framework for developing and deploying AI agents. While optimized for Gemini and the Google ecosystem, ADK is model-agnostic, deployment-agnostic, and is built for compatibility with other frameworks. ADK was designed to make agent development feel more like software development, to make it easier for developers to create, deploy, and orchestrate agentic architectures that range from simple tasks to complex workflows.

### Core Concepts
ADK is built around a few key primitives and concepts that make it powerful and flexible. Here are the essentials:

*   **Agent**: The fundamental worker unit designed for specific tasks. Agents can use language models (`LlmAgent`) for complex reasoning, or act as deterministic controllers of the execution, which are called "workflow agents" (`SequentialAgent`, `ParallelAgent`, `LoopAgent`).
*   **Tool**: Gives agents abilities beyond conversation, letting them interact with external APIs, search information, run code, or call other services.
*   **Callbacks**: Custom code snippets you provide to run at specific points in the agent's process, allowing for checks, logging, or behavior modifications.
*   **Session Management (`Session` & `State`)**: Handles the context of a single conversation (`Session`), including its history (`Events`) and the agent's working memory for that conversation (`State`).
*   **Memory**: Enables agents to recall information about a user across multiple sessions, providing long-term context (distinct from short-term session `State`).
*   **Artifact Management (`Artifact`)**: Allows agents to save, load, and manage files or binary data (like images, PDFs) associated with a session or user.
*   **Code Execution**: The ability for agents (usually via Tools) to generate and execute code to perform complex calculations or actions.
*   **Planning**: An advanced capability where agents can break down complex goals into smaller steps and plan how to achieve them like a ReAct planner.
*   **Models**: The underlying LLM that powers `LlmAgent`s, enabling their reasoning and language understanding abilities.
*   **Event**: The basic unit of communication representing things that happen during a session (user message, agent reply, tool use), forming the conversation history.
*   **Runner**: The engine that manages the execution flow, orchestrates agent interactions based on `Events`, and coordinates with backend services.

**Note:** Features like Multimodal Streaming, Evaluation, Deployment, Debugging, and Trace are also part of the broader ADK ecosystem, supporting real-time interaction and the development lifecycle.

### Key Capabilities
ADK offers several key advantages for developers building agentic applications:

*   **Flexible Orchestration**: Define workflows using workflow agents (`Sequential`, `Parallel`, `Loop`) for predictable pipelines, or leverage LLM-driven dynamic routing (`LlmAgent` transfer) for adaptive behavior.
*   **Multi-Agent System Design/Architecture**: Easily build applications composed of multiple, specialized agents arranged hierarchically. Agents can coordinate complex tasks, delegate sub-tasks using LLM-driven transfer or explicit `AgentTool` invocation, enabling modular and scalable solutions. Explore multi-agent systems.
*   **Rich Tool Ecosystem**: Equip agents with diverse capabilities: use pre-built tools (Search, Code Exec), create custom functions (`FunctionTool`), integrate 3rd-party libraries (LangChain, CrewAI), or even use other agents as tools (`AgentTool`). Support for long-running tools allows handling asynchronous operations effectively. Browse tools.
*   **Deployment Ready**: Containerize and deploy your agents anywhere – run locally, scale with Vertex AI Agent Engine, or integrate into custom infrastructure using Cloud Run or Docker. Deploy agents.
*   **Built-in Evaluation System**: Systematically assess agent performance by evaluating both the final response quality and the step-by-step execution trajectory against predefined test cases. Evaluate agents.
*   **Building Safe and Secure Agents**: Learn how to building powerful and trustworthy agents by implementing security and safety patterns and best practices into your agent's design. Safety and Security.
*   **Integrated Developer Tooling**: Develop and iterate locally with ease. ADK includes tools like a command-line interface (CLI) and a Developer UI for running agents, inspecting execution steps (events, state changes), debugging interactions, and visualizing agent definitions.
*   **Native Streaming Support**: Build real-time, interactive experiences with native support for bidirectional streaming (text and audio). This integrates seamlessly with underlying capabilities like the Multimodal Live API for the Gemini Developer API (or for Vertex AI), often enabled with simple configuration changes.
*   **Broad LLM Support**: While optimized for Google's Gemini models, the framework is designed for flexibility, allowing integration with various LLMs (potentially including open-source or fine-tuned models) through its `BaseLlm` interface.
*   **Artifact Management**: Enable agents to handle files and binary data. The framework provides mechanisms (`ArtifactService`, context methods) for agents to save, load, and manage versioned artifacts like images, documents, or generated reports during their execution.
*   **Extensibility and Interoperability**: ADK promotes an open ecosystem. While providing core tools, it allows developers to easily integrate and reuse tools from other popular agent frameworks including LangChain and CrewAI.
*   **State and Memory Management**: Automatically handles short-term conversational memory (`State` within a `Session`) managed by the `SessionService`. Provides integration points for longer-term `Memory` services, allowing agents to recall user information across multiple sessions.

### Watch "Introducing Agent Development Kit"!
Learn more by watching the introductory video.

## 2. Get Started

### Installation
Install `google-adk` for Python or Java and get up and running in minutes.

#### Python
Create & activate virtual environment:
We recommend creating a virtual Python environment using `venv`:
```bash
python -m venv .venv
```
Now, you can activate the virtual environment using the appropriate command for your operating system and environment:
```bash
# Mac / Linux
source .venv/bin/activate
# Windows CMD:
.venv\Scripts\activate.bat
# Windows PowerShell:
.venv\Scripts\Activate.ps1
```
Install ADK:
```bash
pip install google-adk
```
(Optional) Verify your installation:
```bash
pip show google-adk
```

#### Java
You can either use maven or gradle to add the `google-adk` and `google-adk-dev` package.
`google-adk` is the core Java ADK library. Java ADK also comes with a pluggable example SpringBoot server to run your agents seamlessly. This optional package is present as part of `google-adk-dev`.

If you are using maven, add the following to your `pom.xml`:
```xml
<dependencies>
    <!-- The ADK Core dependency -->
    <dependency>
        <groupId>com.google.adk</groupId>
        <artifactId>google-adk</artifactId>
        <version>0.1.0</version>
    </dependency>
    <!-- The ADK Dev Web UI to debug your agent (Optional) -->
    <dependency>
        <groupId>com.google.adk</groupId>
        <artifactId>google-adk-dev</artifactId>
        <version>0.1.0</version>
    </dependency>
<dependencies>
```
Here's a complete `pom.xml` file for reference.

If you are using gradle, add the dependency to your `build.gradle`:
```gradle
dependencies {
    implementation 'com.google.adk:google-adk:0.1.0'
    implementation 'com.google.adk:google-adk-dev:0.1.0'
}
```
Quickstart maven dependency:
```xml
<dependency>
    <groupId>com.google.adk</groupId>
    <artifactId>google-adk</artifactId>
    <version>0.1.0</version>
</dependency>
```
Quickstart gradle dependency:
```gradle
dependencies {
    implementation 'com.google.adk:google-adk:0.1.0'
}
```

### Quickstart
This quickstart guides you through installing the Agent Development Kit (ADK), setting up a basic agent with multiple tools, and running it locally either in the terminal or in the interactive, browser-based dev UI.
This quickstart assumes a local IDE (VS Code, PyCharm, IntelliJ IDEA, etc.) with Python 3.9+ or Java 17+ and terminal access. This method runs the application entirely on your machine and is recommended for internal development.

#### Python
##### 1. Set up Environment & Install ADK
Create & Activate Virtual Environment (Recommended):
```bash
# Create
python -m venv .venv
# Activate (each new terminal)
# macOS/Linux:
source .venv/bin/activate
# Windows CMD:
.venv\Scripts\activate.bat
# Windows PowerShell:
.venv\Scripts\Activate.ps1
```
Install ADK:
```bash
pip install google-adk
```

##### 2. Create Agent Project
**Project structure**

You will need to create the following project structure:
```
parent_folder/
└── multi_tool_agent/
    ├── __init__.py
    ├── agent.py
    └── .env
```
Create the folder `multi_tool_agent`:
```bash
mkdir multi_tool_agent/
```
**Note for Windows users**
When using ADK on Windows for the next few steps, we recommend creating Python files using File Explorer or an IDE because the following commands (`mkdir`, `echo`) typically generate files with null bytes and/or incorrect encoding.

**`__init__.py`**

Now create an `__init__.py` file in the folder:
```bash
echo "from . import agent" > multi_tool_agent/__init__.py
```
Your `__init__.py` should now look like this:
```python
from . import agent
```

**`agent.py`**

Create an `agent.py` file in the same folder:
```bash
touch multi_tool_agent/agent.py
```
Copy and paste the following code into `agent.py`:
```python
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.
    Args:
        city (str): The name of the city for which to retrieve the weather report.
    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.
    Args:
        city (str): The name of the city for which to retrieve the current time.
    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }
    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")} '
    )
    return {"status": "success", "report": report}

root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and"
        " weather in a city."
    ),
    tools=[get_weather, get_current_time],
)
```

**`.env`**

Create a `.env` file in the same folder:
```bash
touch multi_tool_agent/.env
```
More instructions about this file are described in the next section on Set up the model.

##### 3. Set up the model
Your agent's ability to understand user requests and generate responses is powered by a Large Language Model (LLM). Your agent needs to make secure calls to this external LLM service, which requires authentication credentials. Without valid authentication, the LLM service will deny the agent's requests, and the agent will be unable to function.

**Option 1: Google AI Studio**
Get an API key from Google AI Studio.
Open the `.env` file located inside (`multi_tool_agent/`) and copy-paste the following code.
`multi_tool_agent/.env`:
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=PASTE_YOUR_ACTUAL_API_KEY_HERE
```
Replace `PASTE_YOUR_ACTUAL_API_KEY_HERE` with your actual API KEY.

**Option 2: Vertex AI**
You need an existing Google Cloud account and a project.
1. Set up a Google Cloud project
2. Set up the gcloud CLI
3. Authenticate to Google Cloud, from the terminal by running `gcloud auth login`.
4. Enable the Vertex AI API.

Open the `.env` file located inside (`multi_tool_agent/`). Copy-paste the following code and update the project ID and location.
`multi_tool_agent/.env`:
```
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=LOCATION
```

##### 4. Run Your Agent
Using the terminal, navigate to the parent directory of your agent project (e.g. using `cd ..`):
```
parent_folder/      <-- navigate to this directory
└── multi_tool_agent/
    ├── __init__.py
    ├── agent.py
    └── .env
```
There are multiple ways to interact with your agent:

**a) Use ADK Web UI**
Run the following command to launch the dev UI.
```bash
adk web
```
Step 1: Open the URL provided (usually `http://localhost:8000` or `http://127.0.0.1:8000`) directly in your browser.
Step 2. In the top-left corner of the UI, you can select your agent in the dropdown. Select "multi_tool_agent".
    *Troubleshooting*: If you do not see "multi_tool_agent" in the dropdown menu, make sure you are running `adk web` in the parent folder of your agent folder (i.e. the parent folder of `multi_tool_agent`).
Step 3. Now you can chat with your agent using the textbox.
Step 4. By using the Events tab at the left, you can inspect individual function calls, responses and model responses by clicking on the actions.
On the Events tab, you can also click the Trace button to see the trace logs for each event that shows the latency of each function calls.
Step 5. You can also enable your microphone and talk to your agent.
    *Model support for voice/video streaming*: In order to use voice/video streaming in ADK, you will need to use Gemini models that support the Live API. You can find the model ID(s) that supports the Gemini Live API in the documentation:
    *   Google AI Studio: Gemini Live API
    *   Vertex AI: Gemini Live API
    You can then replace the `model` string in `root_agent` in the `agent.py` file you created earlier. Your code should look something like:
    ```python
    root_agent = Agent(
        name="weather_time_agent",
        model="replace-me-with-model-id", #e.g. gemini-2.0-flash-live-001
        # ...
    )
    ```

**b) Use CLI**
Run the following command, to chat with your Weather agent.
```bash
adk run multi_tool_agent
```
To exit, use Cmd/Ctrl+C.

**c) Use API Server**
`adk api_server` enables you to create a local FastAPI server in a single command, enabling you to test local cURL requests before you deploy your agent.
To learn how to use `adk api_server` for testing, refer to the documentation on testing.

#### Java
To install ADK and setup the environment, proceed to the following steps.

##### 1. Set up Environment & Install ADK
(Handled by `pom.xml` or `build.gradle` as shown in the Installation section above)

##### 2. Create Agent Project
Java projects generally feature the following project structure:
```
project_folder/
├── pom.xml (or build.gradle)
└── src/
    ├── main/
    │   └── java/
    │       └── agents/
    │           └── multitool/
    │               └── MultiToolAgent.java
    └── test/
```
**Create `MultiToolAgent.java`**
Create a `MultiToolAgent.java` source file in the `agents.multitool` package in the `src/main/java/agents/multitool/` directory.
Copy and paste the following code into `MultiToolAgent.java`:
```java
package agents.multitool;

import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.LlmAgent;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.adk.tools.Annotations.Schema;
import com.google.adk.tools.FunctionTool;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import java.nio.charset.StandardCharsets;
import java.text.Normalizer;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Map;
import java.util.Scanner;

public class MultiToolAgent {
    private static String USER_ID = "student";
    private static String NAME = "multi_tool_agent";

    // The run your agent with Dev UI, the ROOT_AGENT should be a global public static variable.
    public static BaseAgent ROOT_AGENT = initAgent();

    public static BaseAgent initAgent() {
        return LlmAgent.builder()
            .name(NAME)
            .model("gemini-2.0-flash")
            .description("Agent to answer questions about the time and weather in a city.")
            .instruction(
                "You are a helpful agent who can answer user questions about the time and weather"
                    + " in a city.")
            .tools(
                FunctionTool.create(MultiToolAgent.class, "getCurrentTime"),
                FunctionTool.create(MultiToolAgent.class, "getWeather"))
            .build();
    }

    public static Map<String, String> getCurrentTime(
        @Schema(description = "The name of the city for which to retrieve the current time")
            String city) {
        String normalizedCity =
            Normalizer.normalize(city, Normalizer.Form.NFD)
                .trim()
                .toLowerCase()
                .replaceAll("(\\p{IsM}+|\\p{IsP}+)", "")
                .replaceAll("\\s+", "_");
        return ZoneId.getAvailableZoneIds().stream()
            .filter(zid -> zid.toLowerCase().endsWith("/" + normalizedCity))
            .findFirst()
            .map(
                zid ->
                    Map.of(
                        "status",
                        "success",
                        "report",
                        "The current time in "
                            + city
                            + " is "
                            + ZonedDateTime.now(ZoneId.of(zid))
                                .format(DateTimeFormatter.ofPattern("HH:mm"))
                            + "."))
            .orElse(
                Map.of(
                    "status", "error", "report", "Sorry, I don't have timezone information for " + city + "."));
    }

    public static Map<String, String> getWeather(
        @Schema(description = "The name of the city for which to retrieve the weather report")
            String city) {
        if (city.toLowerCase().equals("new york")) {
            return Map.of(
                "status",
                "success",
                "report",
                "The weather in New York is sunny with a temperature of 25 degrees Celsius (77 degrees"
                    + " Fahrenheit).");
        } else {
            return Map.of("status", "error", "report", "Weather information for " + city + " is not available.");
        }
    }

    public static void main(String[] args) throws Exception {
        InMemoryRunner runner = new InMemoryRunner(ROOT_AGENT);
        Session session = runner.sessionService().createSession(NAME, USER_ID).blockingGet();
        try (Scanner scanner = new Scanner(System.in, StandardCharsets.UTF_8)) {
            while (true) {
                System.out.print("\nYou > ");
                String userInput = scanner.nextLine();
                if ("quit".equalsIgnoreCase(userInput)) {
                    break;
                }
                Content userMsg = Content.fromParts(Part.fromText(userInput));
                Flowable<Event> events = runner.runAsync(USER_ID, session.id(), userMsg);
                System.out.print("\nAgent > ");
                events.blockingForEach(event -> System.out.println(event.stringifyContent()));
            }
        }
    }
}
```

##### 3. Set up the model
(Similar to Python, choose Google AI Studio or Vertex AI and set environment variables accordingly)

**Option 1: Google AI Studio**
Get an API key from Google AI Studio.
Define environment variables:
```bash
export GOOGLE_GENAI_USE_VERTEXAI=FALSE
export GOOGLE_API_KEY=PASTE_YOUR_ACTUAL_API_KEY_HERE
```
Replace `PASTE_YOUR_ACTUAL_API_KEY_HERE` with your actual API KEY.

**Option 2: Vertex AI**
You need an existing Google Cloud account and a project.
1. Set up a Google Cloud project
2. Set up the gcloud CLI
3. Authenticate to Google Cloud, from the terminal by running `gcloud auth login`.
4. Enable the Vertex AI API.
Define environment variables:
```bash
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
export GOOGLE_CLOUD_LOCATION=LOCATION
```

##### 4. Run Your Agent
Using the terminal, navigate to the parent directory of your agent project (e.g. using `cd ..`):
```
project_folder/                <-- navigate to this directory
├── pom.xml (or build.gradle)
└── src/
    ├── main/
    │   └── java/
    │       └── agents/
    │           └── multitool/
    │               └── MultiToolAgent.java
    └── test/
```
There are multiple ways to interact with your agent:

**a) Use ADK Dev UI**
Run the following command from the terminal to launch the Dev UI.
DO NOT change the main class name of the Dev UI server.
```bash
mvn exec:java \
-Dexec.mainClass="com.google.adk.web.AdkWebServer" \
-Dexec.args="--adk.agents.source-dir=src/main/java" \
-Dexec.classpathScope="compile"
```
Step 1: Open the URL provided (usually `http://localhost:8080` or `http://127.0.0.1:8080`) directly in your browser.
Step 2. In the top-left corner of the UI, you can select your agent in the dropdown. Select "multi_tool_agent".
    *Troubleshooting*: If you do not see "multi_tool_agent" in the dropdown menu, make sure you are running the `mvn` command at the location where your Java source code is located (usually `src/main/java`).
Step 3. Now you can chat with your agent using the textbox.
Step 4. You can also inspect individual function calls, responses and model responses by clicking on the actions.

**b) Use CLI**
With Maven, run the `main()` method of your Java class with the following command:
```bash
mvn compile exec:java -Dexec.mainClass="agents.multitool.MultiToolAgent"
```
With Gradle, the `build.gradle` or `build.gradle.kts` build file should have the following Java plugin in its `plugins` section:
```gradle
plugins {
    id("java")
    // other plugins
}
```
Then, elsewhere in the build file, at the top-level, create a new task to run the `main()` method of your agent:
```gradle
task runAgent(type: JavaExec) {
    classpath = sourceSets.main.runtimeClasspath
    mainClass = "agents.multitool.MultiToolAgent"
}
```
Finally, on the command-line, run the following command:
```bash
gradle runAgent
```

##### Example prompts to try
*   What is the weather in New York?
*   What is the time in New York?
*   What is the weather in Paris?
*   What is the time in Paris?

---

**Congratulations!**
You've successfully created and interacted with your first agent using ADK!

---
**Next steps**
*   Go to the tutorial: Learn how to add memory, session, state to your agent: tutorial.
*   Delve into advanced configuration: Explore the setup section for deeper dives into project structure, configuration, and other interfaces.
*   Understand Core Concepts: Learn about agents concepts.

### Streaming Quickstarts
The Agent Development Kit (ADK) enables real-time, interactive experiences with your AI agents through streaming. This allows for features like live voice conversations, real-time tool use, and continuous updates from your agent.

#### Python ADK: Streaming Quickstart
With this quickstart, you'll learn to create a simple agent and use ADK Streaming to enable voice and video communication with it that is low-latency and bidirectional. We will install ADK, set up a basic "Google Search" agent, try running the agent with Streaming with `adk web` tool, and then explain how to build a simple asynchronous web app by yourself using ADK Streaming and FastAPI.

**Note:** This guide assumes you have experience using a terminal in Windows, Mac, and Linux environments.

**Supported models for voice/video streaming**
In order to use voice/video streaming in ADK, you will need to use Gemini models that support the Live API. You can find the model ID(s) that supports the Gemini Live API in the documentation:
*   Google AI Studio: Gemini Live API
*   Vertex AI: Gemini Live API

##### 1. Setup Environment & Install ADK
Create & Activate Virtual Environment (Recommended):
```bash
# Create
python -m venv .venv
# Activate (each new terminal)
# macOS/Linux:
source .venv/bin/activate
# Windows CMD:
.venv\Scripts\activate.bat
# Windows PowerShell:
.venv\Scripts\Activate.ps1
```
Install ADK:
```bash
pip install google-adk
```

##### 2. Project Structure
Create the following folder structure with empty files:
```
adk-streaming/  # Project folder
└── app/        # the web app folder
    ├── .env    # Gemini API key
    └── google_search_agent/  # Agent folder
        ├── __init__.py       # Python package
        └── agent.py          # Agent definition
```

**`agent.py`**
Copy-paste the following code block to the `agent.py`.
For `model`, please double check the model ID as described earlier in the Models section.
```python
from google.adk.agents import Agent
from google.adk.tools import google_search  # Import the tool

root_agent = Agent(
    # A unique name for the agent.
    name="basic_search_agent",
    # The Large Language Model (LLM) that agent will use.
    model="gemini-2.0-flash-exp",
    # model="gemini-2.0-flash-live-001",  # New streaming model version as of Feb 2025
    # A short description of the agent's purpose.
    description="Agent to answer questions using Google Search.",
    # Instructions to set the agent's behavior.
    instruction="You are an expert researcher. You always stick to the facts.",
    # Add google_search tool to perform grounding with Google search.
    tools=[google_search]
)
```
**Note:** To enable both text and audio/video input, the model must support the `generateContent` (for text) and `bidiGenerateContent` methods. Verify these capabilities by referring to the List Models Documentation. This quickstart utilizes the `gemini-2.0-flash-exp` model for demonstration purposes.
`agent.py` is where all your agent(s)' logic will be stored, and you must have a `root_agent` defined.
Notice how easily you integrated grounding with Google Search capabilities. The `Agent` class and the `google_search` tool handle the complex interactions with the LLM and grounding with the search API, allowing you to focus on the agent's purpose and behavior.

Copy-paste the following code block to `__init__.py`.
```python
from . import agent
```

##### 3. Set up the platform
To run the agent, choose a platform from either Google AI Studio or Google Cloud Vertex AI:

**Option 1: Google AI Studio**
Get an API key from Google AI Studio.
Open the `.env` file located inside (`app/`) and copy-paste the following code.
`.env`:
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=PASTE_YOUR_ACTUAL_API_KEY_HERE
```
Replace `PASTE_YOUR_ACTUAL_API_KEY_HERE` with your actual API KEY.

**Option 2: Vertex AI**
You need an existing Google Cloud account and a project.
1. Set up a Google Cloud project
2. Set up the gcloud CLI
3. Authenticate to Google Cloud, from the terminal by running `gcloud auth login`.
4. Enable the Vertex AI API.
Open the `.env` file located inside (`app/`). Copy-paste the following code and update the project ID and location.
`.env`:
```
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=PASTE_YOUR_ACTUAL_PROJECT_ID
GOOGLE_CLOUD_LOCATION=us-central1
```

##### 4. Try the agent with `adk web`
Now it's ready to try the agent. Run the following command to launch the dev UI. First, make sure to set the current directory to `app`:
```bash
cd app
```
Also, set `SSL_CERT_FILE` variable with the following command. This is required for the voice and video tests later.
```bash
export SSL_CERT_FILE=$(python -m certifi)
```
Then, run the dev UI:
```bash
adk web
```
Open the URL provided (usually `http://localhost:8000` or `http://127.0.0.1:8000`) directly in your browser. This connection stays entirely on your local machine. Select `google_search_agent`.

**Try with text**
Try the following prompts by typing them in the UI.
*   What is the weather in New York?
*   What is the time in New York?
*   What is the weather in Paris?
*   What is the time in Paris?
The agent will use the `google_search` tool to get the latest information to answer those questions.

**Try with voice and video**
To try with voice, reload the web browser, click the microphone button to enable the voice input, and ask the same question in voice. You will hear the answer in voice in real-time.
To try with video, reload the web browser, click the camera button to enable the video input, and ask questions like "What do you see?". The agent will answer what they see in the video input.

**Stop the tool**
Stop `adk web` by pressing Ctrl-C on the console.

**Note on ADK Streaming**
The following features will be supported in the future versions of the ADK Streaming: Callback, LongRunningTool, ExampleTool, and Shell agent (e.g. SequentialAgent).

Congratulations! You've successfully created and interacted with your first Streaming agent using ADK!
Next steps: build custom streaming app. In Custom Audio Streaming app tutorial, it overviews the server and client code for a custom asynchronous web app built with ADK Streaming and FastAPI, enabling real-time, bidirectional audio and text communication.

#### Java ADK: Streaming Quickstart
This quickstart guide will walk you through the process of creating a basic agent and leveraging ADK Streaming with Java to facilitate low-latency, bidirectional voice interactions.
You'll begin by setting up your Java and Maven environment, structuring your project, and defining the necessary dependencies. Following this, you'll create a simple `ScienceTeacherAgent`, test its text-based streaming capabilities using the Dev UI, and then progress to enabling live audio communication, transforming your agent into an interactive voice-driven application.

##### Create your first agent
**Prerequisites**
In this getting started guide, you will be programming in Java. Check if Java is installed on your machine. Ideally, you should be using Java 17 or more (you can check that by typing `java -version`)
You’ll also be using the Maven build tool for Java. So be sure to have Maven installed on your machine before going further (this is the case for Cloud Top or Cloud Shell, but not necessarily for your laptop).

**Prepare the project structure**
To get started with ADK Java, let’s create a Maven project with the following directory structure:
```
adk-agents/
├── pom.xml
└── src/
    └── main/
        └── java/
            └── agents/
                └── ScienceTeacherAgent.java
```
Follow the instructions in Installation page to add `pom.xml` for using the ADK package.
**Note**: Feel free to use whichever name you like for the root directory of your project (instead of adk-agents)

**Running a compilation**
Let’s see if Maven is happy with this build, by running a compilation (`mvn compile` command):
```
$ mvn compile
[INFO] Scanning for projects...
[INFO]
[INFO] --------------------< adk-agents:adk-agents >--------------------
[INFO] Building adk-agents 1.0-SNAPSHOT
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO]
[INFO] --- resources:3.3.1:resources (default-resources) @ adk-demo ---
[INFO] skip non existing resourceDirectory /home/user/adk-demo/src/main/resources
[INFO]
[INFO] --- compiler:3.13.0:compile (default-compile) @ adk-demo ---
[INFO] Nothing to compile - all classes are up to date.
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  1.347 s
[INFO] Finished at: 2025-05-06T15:38:08Z
[INFO] ------------------------------------------------------------------------
```
Looks like the project is set up properly for compilation!

**Creating an agent**
Create the `ScienceTeacherAgent.java` file under the `src/main/java/agents/` directory with the following content:
```java
package samples.liveaudio;

import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.LlmAgent;

/** Science teacher agent. */
public class ScienceTeacherAgent {
  // Field expected by the Dev UI to load the agent dynamically
  // (the agent must be initialized at declaration time)
  public static BaseAgent ROOT_AGENT = initAgent();

  public static BaseAgent initAgent() {
    return LlmAgent.builder()
        .name("science-app")
        .description("Science teacher agent")
        .model("gemini-2.0-flash-exp")
        .instruction(
            """
            You are a helpful science teacher that explains science concepts to kids and teenagers.
            """)
        .build();
  }
}
```
*Troubleshooting*: The model `gemini-2.0-flash-exp` will be deprecated in the future. If you see any issues on using it, try using `gemini-2.0-flash-live-001` instead.

We will use Dev UI to run this agent later. For the tool to automatically recognize the agent, its Java class has to comply with the following two rules:
1.  The agent should be stored in a global public static variable named `ROOT_AGENT` of type `BaseAgent` and initialized at declaration time.
2.  The agent definition has to be a static method so it can be loaded during the class initialization by the dynamic compiling classloader.

##### Run agent with Dev UI
Dev UI is a web server where you can quickly run and test your agents for development purpose, without building your own UI application for the agents.

**Define environment variables**
To run the server, you’ll need to export two environment variables:
*   a Gemini key that you can get from AI Studio,
*   a variable to specify we’re not using Vertex AI this time.
```bash
export GOOGLE_GENAI_USE_VERTEXAI=FALSE
export GOOGLE_API_KEY=YOUR_API_KEY
```

**Run Dev UI**
Run the following command from the terminal to launch the Dev UI.
```bash
mvn exec:java \
-Dexec.mainClass="com.google.adk.web.AdkWebServer" \
-Dexec.args="--adk.agents.source-dir=src/main/java" \
-Dexec.classpathScope="compile"
```
Step 1: Open the URL provided (usually `http://localhost:8080` or `http://127.0.0.1:8080`) directly in your browser.
Step 2. In the top-left corner of the UI, you can select your agent in the dropdown. Select "science-app".
    *Troubleshooting*: If you do not see "science-app" in the dropdown menu, make sure you are running the `mvn` command at the location where your Java source code is located (usually `src/main/java`).

**Try Dev UI with text**
With your favorite browser, navigate to: `http://127.0.0.1:8080/`
You should see the following interface:
Click the `Token Streaming` switch at the top right, and ask any questions for the science teacher such as `What's the electron?`. Then you should see the output text in streaming on the UI.
As we saw, you do not have to write any specific code in the agent itself for the text streaming capability. It is provided as an ADK Agent feature by default.

**Try with voice and video**
To try with voice, reload the web browser, click the microphone button to enable the voice input, and ask the same question in voice. You will hear the answer in voice in real-time.
To try with video, reload the web browser, click the camera button to enable the video input, and ask questions like "What do you see?". The agent will answer what they see in the video input.

**Stop the tool**
Stop the tool by pressing `Ctrl-C` on the console.

##### Run agent with a custom live audio app
Now, let's try audio streaming with the agent and a custom live audio application.

**A Maven `pom.xml` build file for Live Audio**
Replace your existing `pom.xml` with the following.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.google.adk.samples</groupId>
    <artifactId>google-adk-sample-live-audio</artifactId>
    <version>0.1.0</version>
    <name>Google ADK - Sample - Live Audio</name>
    <description>
        A sample application demonstrating a live audio conversation using ADK, runnable via
        samples.liveaudio.LiveAudioRun.
    </description>
    <packaging>jar</packaging>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <java.version>17</java.version>
        <auto-value.version>1.11.0</auto-value.version>
        <!-- Main class for exec-maven-plugin -->
        <exec.mainClass>samples.liveaudio.LiveAudioRun</exec.mainClass>
        <google-adk.version>0.1.0</google-adk.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>com.google.cloud</groupId>
                <artifactId>libraries-bom</artifactId>
                <version>26.53.0</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <dependency>
            <groupId>com.google.adk</groupId>
            <artifactId>google-adk</artifactId>
            <version>${google-adk.version}</version>
        </dependency>
        <dependency>
            <groupId>commons-logging</groupId>
            <artifactId>commons-logging</artifactId>
            <version>1.2</version> <!-- Or use a property if defined in a parent POM -->
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
                <configuration>
                    <source>${java.version}</source>
                    <target>${java.version}</target>
                    <parameters>true</parameters>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>com.google.auto.value</groupId>
                            <artifactId>auto-value</artifactId>
                            <version>${auto-value.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>build-helper-maven-plugin</artifactId>
                <version>3.6.0</version>
                <executions>
                    <execution>
                        <id>add-source</id>
                        <phase>generate-sources</phase>
                        <goals>
                            <goal>add-source</goal>
                        </goals>
                        <configuration>
                            <sources>
                                <source>.</source>
                            </sources>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>exec-maven-plugin</artifactId>
                <version>3.2.0</version>
                <configuration>
                    <mainClass>${exec.mainClass}</mainClass>
                    <classpathScope>runtime</classpathScope>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

**Creating Live Audio Run tool**
Create the `LiveAudioRun.java` file under the `src/main/java/` directory with the following content. This tool runs the agent on it with live audio input and output.
```java
package samples.liveaudio;

import com.google.adk.agents.LiveRequestQueue;
import com.google.adk.agents.RunConfig;
import com.google.adk.events.Event;
import com.google.adk.runner.Runner;
import com.google.adk.sessions.InMemorySessionService;
import com.google.common.collect.ImmutableList;
import com.google.genai.types.Blob;
import com.google.genai.types.Modality;
import com.google.genai.types.PrebuiltVoiceConfig;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import com.google.genai.types.SpeechConfig;
import com.google.genai.types.VoiceConfig;
import io.reactivex.rxjava3.core.Flowable;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.URL;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.Mixer;
import javax.sound.sampled.SourceDataLine;
import javax.sound.sampled.TargetDataLine;
import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import agents.ScienceTeacherAgent; // Assuming ScienceTeacherAgent is in 'agents' package

/** Main class to demonstrate running the {@link LiveAudioAgent} for a voice conversation. */
public final class LiveAudioRun {

  private final String userId;
  private final String sessionId;
  private final Runner runner;

  private static final javax.sound.sampled.AudioFormat MIC_AUDIO_FORMAT =
      new javax.sound.sampled.AudioFormat(16000.0f, 16, 1, true, false);
  private static final javax.sound.sampled.AudioFormat SPEAKER_AUDIO_FORMAT =
      new javax.sound.sampled.AudioFormat(24000.0f, 16, 1, true, false);
  private static final int BUFFER_SIZE = 4096;

  public LiveAudioRun() {
    this.userId = "test_user";
    String appName = "LiveAudioApp";
    this.sessionId = UUID.randomUUID().toString();
    InMemorySessionService sessionService = new InMemorySessionService();
    this.runner = new Runner(ScienceTeacherAgent.ROOT_AGENT, appName, null, sessionService);
    ConcurrentMap<String, Object> initialState = new ConcurrentHashMap<>();
    var unused = sessionService.createSession(appName, userId, initialState, sessionId).blockingGet();
  }

  private void runConversation() throws Exception {
    System.out.println("Initializing microphone input and speaker output...");

    RunConfig runConfig =
        RunConfig.builder()
            .setStreamingMode(RunConfig.StreamingMode.BIDI)
            .setResponseModalities(ImmutableList.of(new Modality("AUDIO")))
            .setSpeechConfig(
                SpeechConfig.builder()
                    .voiceConfig(
                        VoiceConfig.builder()
                            .prebuiltVoiceConfig(
                                PrebuiltVoiceConfig.builder().voiceName("Aoede").build())
                            .build())
                    .languageCode("en-US")
                    .build())
            .build();

    LiveRequestQueue liveRequestQueue = new LiveRequestQueue();
    Flowable<Event> eventStream =
        this.runner.runLive(
            runner.sessionService().createSession(userId, sessionId).blockingGet(),
            liveRequestQueue,
            runConfig);

    AtomicBoolean isRunning = new AtomicBoolean(true);
    AtomicBoolean conversationEnded = new AtomicBoolean(false);
    ExecutorService executorService = Executors.newFixedThreadPool(2);

    // Task for capturing microphone input
    Future<?> microphoneTask =
        executorService.submit(() -> captureAndSendMicrophoneAudio(liveRequestQueue, isRunning));

    // Task for processing agent responses and playing audio
    Future<?> outputTask =
        executorService.submit(
            () -> {
              try {
                processAudioOutput(eventStream, isRunning, conversationEnded);
              } catch (Exception e) {
                System.err.println("Error processing audio output: " + e.getMessage());
                e.printStackTrace();
                isRunning.set(false);
              }
            });

    // Wait for user to press Enter to stop the conversation
    System.out.println("Conversation started. Press Enter to stop...");
    System.in.read();

    System.out.println("Ending conversation...");
    isRunning.set(false);

    try {
      // Give some time for ongoing processing to complete
      microphoneTask.get(2, TimeUnit.SECONDS);
      outputTask.get(2, TimeUnit.SECONDS);
    } catch (Exception e) {
      System.out.println("Stopping tasks...");
    }

    liveRequestQueue.close();
    executorService.shutdownNow();
    System.out.println("Conversation ended.");
  }

  private void captureAndSendMicrophoneAudio(
      LiveRequestQueue liveRequestQueue, AtomicBoolean isRunning) {
    TargetDataLine micLine = null;
    try {
      DataLine.Info info = new DataLine.Info(TargetDataLine.class, MIC_AUDIO_FORMAT);
      if (!AudioSystem.isLineSupported(info)) {
        System.err.println("Microphone line not supported!");
        return;
      }
      micLine = (TargetDataLine) AudioSystem.getLine(info);
      micLine.open(MIC_AUDIO_FORMAT);
      micLine.start();
      System.out.println("Microphone initialized. Start speaking...");

      byte[] buffer = new byte[BUFFER_SIZE];
      int bytesRead;
      while (isRunning.get()) {
        bytesRead = micLine.read(buffer, 0, buffer.length);
        if (bytesRead > 0) {
          byte[] audioChunk = new byte[bytesRead];
          System.arraycopy(buffer, 0, audioChunk, 0, bytesRead);
          Blob audioBlob = Blob.builder().data(audioChunk).mimeType("audio/pcm").build();
          liveRequestQueue.realtime(audioBlob);
        }
      }
    } catch (LineUnavailableException e) {
      System.err.println("Error accessing microphone: " + e.getMessage());
      e.printStackTrace();
    } finally {
      if (micLine != null) {
        micLine.stop();
        micLine.close();
      }
    }
  }

  private void processAudioOutput(
      Flowable<Event> eventStream, AtomicBoolean isRunning, AtomicBoolean conversationEnded) {
    SourceDataLine speakerLine = null;
    try {
      DataLine.Info info = new DataLine.Info(SourceDataLine.class, SPEAKER_AUDIO_FORMAT);
      if (!AudioSystem.isLineSupported(info)) {
        System.err.println("Speaker line not supported!");
        return;
      }
      final SourceDataLine finalSpeakerLine = (SourceDataLine) AudioSystem.getLine(info);
      finalSpeakerLine.open(SPEAKER_AUDIO_FORMAT);
      finalSpeakerLine.start();
      System.out.println("Speaker initialized.");

      for (Event event : eventStream.blockingIterable()) {
        if (!isRunning.get()) {
          break;
        }
        event
            .content()
            .ifPresent(
                content ->
                    content
                        .parts()
                        .ifPresent(parts -> parts.forEach(part -> playAudioData(part, finalSpeakerLine))));
      }
      speakerLine = finalSpeakerLine; // Assign to outer variable for cleanup in finally block
    } catch (LineUnavailableException e) {
      System.err.println("Error accessing speaker: " + e.getMessage());
      e.printStackTrace();
    } finally {
      if (speakerLine != null) {
        speakerLine.drain();
        speakerLine.stop();
        speakerLine.close();
      }
      conversationEnded.set(true);
    }
  }

  private void playAudioData(Part part, SourceDataLine speakerLine) {
    part.inlineData()
        .ifPresent(
            inlineBlob ->
                inlineBlob
                    .data()
                    .ifPresent(
                        audioBytes -> {
                          if (audioBytes.length > 0) {
                            System.out.printf(
                                "Playing audio (%s): %d bytes%n",
                                inlineBlob.mimeType(), audioBytes.length);
                            speakerLine.write(audioBytes, 0, audioBytes.length);
                          }
                        }));
  }

  private void processEvent(Event event, java.util.concurrent.atomic.AtomicBoolean audioReceived) {
    event
        .content()
        .ifPresent(
            content ->
                content
                    .parts()
                    .ifPresent(parts -> parts.forEach(part -> logReceivedAudioData(part, audioReceived))));
  }

  private void logReceivedAudioData(Part part, AtomicBoolean audioReceived) {
    part.inlineData()
        .ifPresent(
            inlineBlob ->
                inlineBlob
                    .data()
                    .ifPresent(
                        audioBytes -> {
                          if (audioBytes.length > 0) {
                            System.out.printf(
                                "    Audio (%s): received %d bytes.%n",
                                inlineBlob.mimeType(), audioBytes.length);
                            audioReceived.set(true);
                          } else {
                            System.out.printf(
                                "    Audio (%s): received empty audio data.%n",
                                inlineBlob.mimeType());
                          }
                        }));
  }

  public static void main(String[] args) throws Exception {
    LiveAudioRun liveAudioRun = new LiveAudioRun();
    liveAudioRun.runConversation();
    System.out.println("Exiting Live Audio Run.");
  }
}
```

**Run the Live Audio Run tool**
To run Live Audio Run tool, use the following command on the `adk-agents` directory:
```bash
mvn compile exec:java
```
Then you should see:
```
$ mvn compile exec:java
...
Initializing microphone input and speaker output...
Conversation started. Press Enter to stop...
Speaker initialized.
Microphone initialized. Start speaking...
```
With this message, the tool is ready to take voice input. Talk to the agent with a question like `What's the electron?`.
**Caution**: When you observe the agent keep speaking by itself and doesn't stop, try using earphones to suppress the echoing.

**Summary**
Streaming for ADK enables developers to create agents capable of low-latency, bidirectional voice and video communication, enhancing interactive experiences. The article demonstrates that text streaming is a built-in feature of ADK Agents, requiring no additional specific code, while also showcasing how to implement live audio conversations for real-time voice interaction with an agent. This allows for more natural and dynamic communication, as users can speak to and hear from the agent seamlessly.

### Testing Your Agents
Before you deploy your agent, you should test it to ensure that it is working as intended. The easiest way to test your agent in your development environment is to use the ADK web UI with the following commands.

#### Python
```bash
adk api_server
```

#### Java
```bash
mvn compile exec:java \
-Dexec.args="--adk.agents.source-dir=src/main/java/agents --server.port=8080"
```
In Java, both the Dev UI and the API server are bundled together.

This command will launch a local web server, where you can run cURL commands or send API requests to test your agent.

#### Local testing
Local testing involves launching a local web server, creating a session, and sending queries to your agent. First, ensure you are in the correct working directory:
```
parent_folder/
└── my_sample_agent/
    └── agent.py (or Agent.java)
```

**Launch the Local Server**
Next, launch the local server using the commands listed above.
The output should appear similar to:

Python:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
```

Java:
```
2025-05-13T23:32:08.972-06:00  INFO 37864 --- [ebServer.main()] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port 8080 (http) with context path '/'
2025-05-13T23:32:08.980-06:00  INFO 37864 --- [ebServer.main()] com.google.adk.web.AdkWebServer          : Started AdkWebServer in 1.15 seconds (process running for 2.877)
2025-05-13T23:32:08.981-06:00  INFO 37864 --- [ebServer.main()] com.google.adk.web.AdkWebServer          : AdkWebServer application started successfully.
```
Your server is now running locally. Ensure you use the correct port number in all the subsequent commands.

**Create a new session**
With the API server still running, open a new terminal window or tab and create a new session with the agent using:
```bash
curl -X POST http://localhost:8000/apps/my_sample_agent/users/u_123/sessions/s_123 \
-H "Content-Type: application/json" \
-d '{"state": {"key1": "value1", "key2": 42}}'
```
Let's break down what's happening:
*   `http://localhost:8000/apps/my_sample_agent/users/u_123/sessions/s_123`: This creates a new session for your agent `my_sample_agent`, which is the name of the agent folder, for a user ID (`u_123`) and for a session ID (`s_123`). You can replace `my_sample_agent` with the name of your agent folder. You can replace `u_123` with a specific user ID, and `s_123` with a specific session ID.
*   `{"state": {"key1": "value1", "key2": 42}}`: This is optional. You can use this to customize the agent's pre-existing state (dict) when creating the session.

This should return the session information if it was created successfully. The output should appear similar to:
```json
{
    "id": "s_123",
    "appName": "my_sample_agent",
    "userId": "u_123",
    "state": {
        "state": {
            "key1": "value1",
            "key2": 42
        }
    },
    "events": [],
    "lastUpdateTime": 1743711430.022186
}
```
**Info**: You cannot create multiple sessions with exactly the same user ID and session ID. If you try to, you may see a response, like: `{"detail":"Session already exists: s_123"}`. To fix this, you can either delete that session (e.g., `s_123`), or choose a different session ID.

**Send a query**
There are two ways to send queries via POST to your agent, via the `/run` or `/run_sse` routes.
*   `POST http://localhost:8000/run`: collects all events as a list and returns the list all at once. Suitable for most users (if you are unsure, we recommend using this one).
*   `POST http://localhost:8000/run_sse`: returns as Server-Sent-Events, which is a stream of event objects. Suitable for those who want to be notified as soon as the event is available. With `/run_sse`, you can also set `streaming` to `true` to enable token-level streaming.

**Using `/run`**
```bash
curl -X POST http://localhost:8000/run \
-H "Content-Type: application/json" \
-d '{
    "appName": "my_sample_agent",
    "userId": "u_123",
    "sessionId": "s_123",
    "newMessage": {
        "role": "user",
        "parts": [{ "text": "Hey whats the weather in new york today" }]
    }
}'
```
If using `/run`, you will see the full output of events at the same time, as a list, which should appear similar to:
```json
[{
    "content": {
        "parts": [{
            "functionCall": {
                "id": "af-e75e946d-c02a-4aad-931e-49e4ab859838",
                "args": { "city": "new york" },
                "name": "get_weather"
            }
        }],
        "role": "model"
    },
    "invocationId": "e-71353f1e-aea1-4821-aa4b-46874a766853",
    "author": "weather_time_agent",
    "actions": { "stateDelta": {}, "artifactDelta": {}, "requestedAuthConfigs": {} },
    "longRunningToolIds": [],
    "id": "2Btee6zW",
    "timestamp": 1743712220.385936
}, {
    "content": {
        "parts": [{
            "functionResponse": {
                "id": "af-e75e946d-c02a-4aad-931e-49e4ab859838",
                "name": "get_weather",
                "response": {
                    "status": "success",
                    "report": "The weather in New York is sunny with a temperature of 25 degrees Celsius (41 degrees Fahrenheit)."
                }
            }
        }],
        "role": "user"
    },
    "invocationId": "e-71353f1e-aea1-4821-aa4b-46874a766853",
    "author": "weather_time_agent",
    "actions": { "stateDelta": {}, "artifactDelta": {}, "requestedAuthConfigs": {} },
    "id": "PmWibL2m",
    "timestamp": 1743712221.895042
}, {
    "content": {
        "parts": [{ "text": "OK. The weather in New York is sunny with a temperature of 25 degrees Celsius (41 degrees Fahrenheit).\n" }],
        "role": "model"
    },
    "invocationId": "e-71353f1e-aea1-4821-aa4b-46874a766853",
    "author": "weather_time_agent",
    "actions": { "stateDelta": {}, "artifactDelta": {}, "requestedAuthConfigs": {} },
    "id": "sYT42eVC",
    "timestamp": 1743712221.899018
}]
```

**Using `/run_sse`**
```bash
curl -X POST http://localhost:8000/run_sse \
-H "Content-Type: application/json" \
-d '{
    "appName": "my_sample_agent",
    "userId": "u_123",
    "sessionId": "s_123",
    "newMessage": {
        "role": "user",
        "parts": [{ "text": "Hey whats the weather in new york today" }]
    },
    "streaming": false
}'
```
You can set `streaming` to `true` to enable token-level streaming, which means the response will be returned to you in multiple chunks and the output should appear similar to:
```
data: { "content": { "parts": [{ "functionCall": { "id": "af-f83f8af9-f732-46b6-8cb5-7b5b73bbf13d", "args": { "city": "new york" }, "name": "get_weather" }}], "role": "model" }, "invocationId": "e-3f6d7765-5287-419e-9991-5fffa1a75565", "author": "weather_time_agent", "actions": { "stateDelta": {}, "artifactDelta": {}, "requestedAuthConfigs": {} }, "longRunningToolIds": [], "id": "ptcjaZBa", "timestamp": 1743712255.313043 }
data: { "content": { "parts": [{ "functionResponse": { "id": "af-f83f8af9-f732-46b6-8cb5-7b5b73bbf13d", "name": "get_weather", "response": { "status": "success", "report": "The weather in New York is sunny with a temperature of 25 degrees Celsius (41 degrees Fahrenheit)." } }}], "role": "user" }, "invocationId": "e-3f6d7765-5287-419e-9991-5fffa1a75565", "author": "weather_time_agent", "actions": { "stateDelta": {}, "artifactDelta": {}, "requestedAuthConfigs": {} }, "id": "5aocxjaq", "timestamp": 1743712257.387306 }
data: { "content": { "parts": [{ "text": "OK. The weather in New York is sunny with a temperature of 25 degrees Celsius (41 degrees Fahrenheit).\n" }], "role": "model" }, "invocationId": "e-3f6d7765-5287-419e-9991-5fffa1a75565", "author": "weather_time_agent", "actions": { "stateDelta": {}, "artifactDelta": {}, "requestedAuthConfigs": {} }, "id": "rAnWGSiV", "timestamp": 1743712257.391317 }
```
**Info**: If you are using `/run_sse`, you should see each event as soon as it becomes available.

#### Integrations
ADK uses Callbacks to integrate with third-party observability tools. These integrations capture detailed traces of agent calls and interactions, which are crucial for understanding behavior, debugging issues, and evaluating performance.
*   Comet Opik is an open-source LLM observability and evaluation platform that natively supports ADK.

#### Deploying your agent
Now that you've verified the local operation of your agent, you're ready to move on to deploying your agent! Here are some ways you can deploy your agent:
*   Deploy to Agent Engine, the easiest way to deploy your ADK agents to a managed service in Vertex AI on Google Cloud.
*   Deploy to Cloud Run and have full control over how you scale and manage your agents using serverless architecture on Google Cloud.

## 3. Agents

### Introduction to Agents
In the Agent Development Kit (ADK), an Agent is a self-contained execution unit designed to act autonomously to achieve specific goals. Agents can perform tasks, interact with users, utilize external tools, and coordinate with other agents.
The foundation for all agents in ADK is the `BaseAgent` class. It serves as the fundamental blueprint. To create functional agents, you typically extend `BaseAgent` in one of three main ways, catering to different needs – from intelligent reasoning to structured process control.

### Core Agent Categories
ADK provides distinct agent categories to build sophisticated applications:

*   **LLM Agents (`LlmAgent`, `Agent`)**: These agents utilize Large Language Models (LLMs) as their core engine to understand natural language, reason, plan, generate responses, and dynamically decide how to proceed or which tools to use, making them ideal for flexible, language-centric tasks.
*   **Workflow Agents (`SequentialAgent`, `ParallelAgent`, `LoopAgent`)**: These specialized agents control the execution flow of other agents in predefined, deterministic patterns (sequence, parallel, or loop) without using an LLM for the flow control itself, perfect for structured processes needing predictable execution.
*   **Custom Agents**: Created by extending `BaseAgent` directly, these agents allow you to implement unique operational logic, specific control flows, or specialized integrations not covered by the standard types, catering to highly tailored application requirements.

### Choosing the Right Agent Type
The following table provides a high-level comparison to help distinguish between the agent types. As you explore each type in more detail in the subsequent sections, these distinctions will become clearer.
(Table content was missing in the source, but would typically compare `LlmAgent`, `WorkflowAgent` types, and `CustomAgent` based on criteria like determinism, LLM use, control flow, etc.)

### Agents Working Together: Multi-Agent Systems
While each agent type serves a distinct purpose, the true power often comes from combining them. Complex applications frequently employ multi-agent architectures where:
*   LLM Agents handle intelligent, language-based task execution.
*   Workflow Agents manage the overall process flow using standard patterns.
*   Custom Agents provide specialized capabilities or rules needed for unique integrations.
Understanding these core types is the first step toward building sophisticated, capable AI applications with ADK.

### What's Next?
Now that you have an overview of the different agent types available in ADK, dive deeper into how they work and how to use them effectively:
*   **LLM Agents**: Explore how to configure agents powered by large language models, including setting instructions, providing tools, and enabling advanced features like planning and code execution.
*   **Workflow Agents**: Learn how to orchestrate tasks using `SequentialAgent`, `ParallelAgent`, and `LoopAgent` for structured and predictable processes.
*   **Custom Agents**: Discover the principles of extending `BaseAgent` to build agents with unique logic and integrations tailored to your specific needs.
*   **Multi-Agents**: Understand how to combine different agent types to create sophisticated, collaborative systems capable of tackling complex problems.
*   **Models**: Learn about the different LLM integrations available and how to select the right model for your agents.

### LLM Agent
The `LlmAgent` (often aliased simply as `Agent`) is a core component in ADK, acting as the "thinking" part of your application. It leverages the power of a Large Language Model (LLM) for reasoning, understanding natural language, making decisions, generating responses, and interacting with tools.
Unlike deterministic Workflow Agents that follow predefined execution paths, `LlmAgent` behavior is non-deterministic. It uses the LLM to interpret instructions and context, deciding dynamically how to proceed, which tools to use (if any), or whether to transfer control to another agent.
Building an effective `LlmAgent` involves defining its identity, clearly guiding its behavior through instructions, and equipping it with the necessary tools and capabilities.

#### Defining the Agent's Identity and Purpose
First, you need to establish what the agent is and what it's for.

*   **`name` (Required)**: Every agent needs a unique string identifier. This name is crucial for internal operations, especially in multi-agent systems where agents need to refer to or delegate tasks to each other. Choose a descriptive name that reflects the agent's function (e.g., `customer_support_router`, `billing_inquiry_agent`). Avoid reserved names like `user`.
*   **`description` (Optional, Recommended for Multi-Agent)**: Provide a concise summary of the agent's capabilities. This description is primarily used by other LLM agents to determine if they should route a task to this agent. Make it specific enough to differentiate it from peers (e.g., "Handles inquiries about current billing statements," not just "Billing agent").
*   **`model` (Required)**: Specify the underlying LLM that will power this agent's reasoning. This is a string identifier like `"gemini-2.0-flash"`. The choice of model impacts the agent's capabilities, cost, and performance. See the Models page for available options and considerations.

**Python Example:**
```python
# Example: Defining the basic identity
capital_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="capital_agent",
    description="Answers user questions about the capital city of a given country."
    # instruction and tools will be added next
)
```
**Java Example:**
```java
// Example: Defining the basic identity
LlmAgent capitalAgent = LlmAgent.builder()
    .model("gemini-2.0-flash")
    .name("capital_agent")
    .description("Answers user questions about the capital city of a given country.")
    // instruction and tools will be added next
    .build();
```

#### Guiding the Agent: Instructions (`instruction`)
The `instruction` parameter is arguably the most critical for shaping an `LlmAgent`'s behavior. It's a string (or a function returning a string) that tells the agent:
*   Its core task or goal.
*   Its personality or persona (e.g., "You are a helpful assistant," "You are a witty pirate").
*   Constraints on its behavior (e.g., "Only answer questions about X," "Never reveal Y").
*   How and when to use its `tools`. You should explain the purpose of each tool and the circumstances under which it should be called, supplementing any descriptions within the tool itself.
*   The desired format for its output (e.g., "Respond in JSON," "Provide a bulleted list").

**Tips for Effective Instructions:**
*   **Be Clear and Specific**: Avoid ambiguity. Clearly state the desired actions and outcomes.
*   **Use Markdown**: Improve readability for complex instructions using headings, lists, etc.
*   **Provide Examples (Few-Shot)**: For complex tasks or specific output formats, include examples directly in the instruction.
*   **Guide Tool Use**: Don't just list tools; explain when and why the agent should use them.
*   **State**:
    The `instruction` is a string template, you can use the `{var}` syntax to insert dynamic values into the instruction.
    *   `{var}` is used to insert the value of the state variable named `var`.
    *   `{artifact.var}` is used to insert the text content of the artifact named `var`.
    *   If the state variable or artifact does not exist, the agent will raise an error. If you want to ignore the error, you can append a `?` to the variable name as in `{var?}`.

**Python Example:**
```python
# Example: Adding instructions
capital_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="capital_agent",
    description="Answers user questions about the capital city of a given country.",
    instruction="""You are an agent that provides the capital city of a country.
When a user asks for the capital of a country:
1. Identify the country name from the user's query.
2. Use the `get_capital_city` tool to find the capital.
3. Respond clearly to the user, stating the capital city.

Example Query: "What's the capital of {country}?"
Example Response: "The capital of France is Paris."
""",
    # tools will be added next
)
```
**Java Example:**
```java
// Example: Adding instructions
LlmAgent capitalAgent = LlmAgent.builder()
    .model("gemini-2.0-flash")
    .name("capital_agent")
    .description("Answers user questions about the capital city of a given country.")
    .instruction("""
    You are an agent that provides the capital city of a country.
    When a user asks for the capital of a country:
    1. Identify the country name from the user's query.
    2. Use the `get_capital_city` tool to find the capital.
    3. Respond clearly to the user, stating the capital city.

    Example Query: "What's the capital of {country}?"
    Example Response: "The capital of France is Paris."
    """)
    // tools will be added next
    .build();
```
(Note: For instructions that apply to all agents in a system, consider using `global_instruction` on the root agent, detailed further in the Multi-Agents section.)

#### Equipping the Agent: Tools (`tools`)
Tools give your `LlmAgent` capabilities beyond the LLM's built-in knowledge or reasoning. They allow the agent to interact with the outside world, perform calculations, fetch real-time data, or execute specific actions.

`tools` (Optional): Provide a list of tools the agent can use. Each item in the list can be:
*   A native function or method (wrapped as a `FunctionTool`). Python ADK automatically wraps the native function into a `FuntionTool` whereas, you must explicitly wrap your Java methods using `FunctionTool.create(...)`
*   An instance of a class inheriting from `BaseTool`.
*   An instance of another agent (`AgentTool`, enabling agent-to-agent delegation - see Multi-Agents).

The LLM uses the function/tool names, descriptions (from docstrings or the `description` field), and parameter schemas to decide which tool to call based on the conversation and its instructions.

**Python Example:**
```python
# Define a tool function
def get_capital_city(country: str) -> str:
    """Retrieves the capital city for a given country."""
    # Replace with actual logic (e.g., API call, database lookup)
    capitals = {
        "france": "Paris",
        "japan": "Tokyo",
        "canada": "Ottawa"
    }
    return capitals.get(country.lower(), f"Sorry, I don't know the capital of {country}.")

# Add the tool to the agent
capital_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="capital_agent",
    description="Answers user questions about the capital city of a given country.",
    instruction="""You are an agent that provides the capital city of a country... (previous instruction text)""",
    tools=[get_capital_city]  # Provide the function directly
)
```
**Java Example:**
```java
// Define a tool function
// Retrieves the capital city of a given country.
public static Map<String, Object> getCapitalCity(
    @Schema(name = "country", description = "The country to get capital for") String country
) {
    // Replace with actual logic (e.g., API call, database lookup)
    Map<String, String> countryCapitals = new HashMap<>();
    countryCapitals.put("canada", "Ottawa");
    countryCapitals.put("france", "Paris");
    countryCapitals.put("japan", "Tokyo");
    String result = countryCapitals.getOrDefault(
        country.toLowerCase(), "Sorry, I couldn't find the capital for " + country + "."
    );
    return Map.of("result", result); // Tools must return a Map
}

// Add the tool to the agent
FunctionTool capitalTool = FunctionTool.create(experiment.getClass(), "getCapitalCity"); // Assuming 'experiment' is the class instance
LlmAgent capitalAgent = LlmAgent.builder()
    .model("gemini-2.0-flash")
    .name("capital_agent")
    .description("Answers user questions about the capital city of a given country.")
    .instruction("You are an agent that provides the capital city of a country... (previous instruction text)")
    .tools(capitalTool) // Provide the function wrapped as a FunctionTool
    .build();
```
Learn more about Tools in the Tools section.

#### Advanced Configuration & Control
Beyond the core parameters, `LlmAgent` offers several options for finer control:

##### Fine-Tuning LLM Generation (`generate_content_config`)
You can adjust how the underlying LLM generates responses using `generate_content_config`.
`generate_content_config` (Optional): Pass an instance of `google.genai.types.GenerateContentConfig` to control parameters like `temperature` (randomness), `max_output_tokens` (response length), `top_p`, `top_k`, and safety settings.

**Python Example:**
```python
from google.genai import types
agent = LlmAgent(
    # ... other params
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,  # More deterministic output
        max_output_tokens=250
    )
)
```
**Java Example:**
```java
import com.google.genai.types.GenerateContentConfig;
LlmAgent agent = LlmAgent.builder()
    // ... other params
    .generateContentConfig(GenerateContentConfig.builder()
        .temperature(0.2F) // More deterministic output
        .maxOutputTokens(250)
        .build())
    .build();
```

##### Structuring Data (`input_schema`, `output_schema`, `output_key`)
For scenarios requiring structured data exchange with an `LLM Agent`, the ADK provides mechanisms to define expected input and desired output formats using schema definitions.

*   **`input_schema` (Optional)**: Define a schema representing the expected input structure. If set, the user message content passed to this agent must be a JSON string conforming to this schema. Your instructions should guide the user or preceding agent accordingly.
*   **`output_schema` (Optional)**: Define a schema representing the desired output structure. If set, the agent's final response must be a JSON string conforming to this schema.
    **Constraint**: Using `output_schema` enables controlled generation within the LLM but **disables the agent's ability to use tools or transfer control to other agents**. Your instructions must guide the LLM to produce JSON matching the schema directly.
*   **`output_key` (Optional)**: Provide a string key. If set, the text content of the agent's final response will be automatically saved to the session's state dictionary under this key. This is useful for passing results between agents or steps in a workflow.
    *   In Python, this might look like: `session.state[output_key] = agent_response_text`
    *   In Java: `session.state().put(outputKey, agentResponseText)`

**Python Example (Pydantic):**
```python
from pydantic import BaseModel, Field

class CapitalOutput(BaseModel):
    capital: str = Field(description="The capital of the country.")

structured_capital_agent = LlmAgent(
    # ... name, model, description
    instruction="""You are a Capital Information Agent.
Given a country, respond ONLY with a JSON object containing the capital.
Format: {"capital": "capital_name"}""",
    output_schema=CapitalOutput,  # Enforce JSON output
    output_key="found_capital"    # Store result in state['found_capital']
    # Cannot use tools=[get_capital_city] effectively here
)
```
**Java Example (google.genai.types.Schema):**
```java
import com.google.genai.types.Schema;
// ...
private static final Schema CAPITAL_OUTPUT_SCHEMA = Schema.builder()
    .type("OBJECT")
    .description("Schema for capital city information.")
    .properties(Map.of(
        "capital", Schema.builder()
            .type("STRING")
            .description("The capital city of the country.")
            .build()
    ))
    .build();

LlmAgent structuredCapitalAgent = LlmAgent.builder()
    // ... name, model, description
    .instruction("You are a Capital Information Agent. Given a country, respond ONLY with a JSON object containing the capital. Format: {\"capital\": \"capital_name\"}")
    .outputSchema(CAPITAL_OUTPUT_SCHEMA) // Enforce JSON output
    .outputKey("found_capital")      // Store result in state.get("found_capital")
    // Cannot use tools(getCapitalCity) effectively here
    .build();
```

##### Managing Context (`include_contents`)
Control whether the agent receives the prior conversation history.
`include_contents` (Optional, Default: `'default'`): Determines if the `contents` (history) are sent to the LLM.
*   `'default'`: The agent receives the relevant conversation history.
*   `'none'`: The agent receives no prior `contents`. It operates based solely on its current instruction and any input provided in the current turn (useful for stateless tasks or enforcing specific contexts).

**Python Example:**
```python
stateless_agent = LlmAgent(
    # ... other params
    include_contents='none'
)
```
**Java Example:**
```java
import com.google.adk.agents.LlmAgent.IncludeContents;
LlmAgent statelessAgent = LlmAgent.builder()
    // ... other params
    .includeContents(IncludeContents.NONE)
    .build();
```

##### Planning & Code Execution
For more complex reasoning involving multiple steps or executing code:
*   **`planner` (Optional)**: Assign a `BasePlanner` instance to enable multi-step reasoning and planning before execution. (See Multi-Agents patterns).
*   **`code_executor` (Optional)**: Provide a `BaseCodeExecutor` instance to allow the agent to execute code blocks (e.g., Python) found in the LLM's response. (See Tools/Built-in tools).

#### Putting It Together: Example
Here's the complete basic `capital_agent`:

**Python Example:**
```python
# --- Full example code demonstrating LlmAgent with Tools vs. Output Schema ---
import json # Needed for pretty printing dicts
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel, Field
import asyncio # For async main

# --- 1. Define Constants ---
APP_NAME = "agent_comparison_app"
USER_ID = "test_user_456"
SESSION_ID_TOOL_AGENT = "session_tool_agent_xyz"
SESSION_ID_SCHEMA_AGENT = "session_schema_agent_xyz"
MODEL_NAME = "gemini-2.0-flash"

# --- 2. Define Schemas ---
# Input schema used by both agents
class CountryInput(BaseModel):
    country: str = Field(description="The country to get information about.")

# Output schema ONLY for the second agent
class CapitalInfoOutput(BaseModel):
    capital: str = Field(description="The capital city of the country.")
    # Note: Population is illustrative; the LLM will infer or estimate this
    # as it cannot use tools when output_schema is set.
    population_estimate: str = Field(description="An estimated population of the capital city.")

# --- 3. Define the Tool (Only for the first agent) ---
def get_capital_city(country: str) -> str:
    """Retrieves the capital city of a given country."""
    print(f"\n-- Tool Call: get_capital_city(country='{country}') --")
    country_capitals = {
        "united states": "Washington, D.C.",
        "canada": "Ottawa",
        "france": "Paris",
        "japan": "Tokyo",
    }
    result = country_capitals.get(country.lower(), f"Sorry, I couldn't find the capital for {country}.")
    print(f"-- Tool Result: '{result}' --")
    return result

# --- 4. Configure Agents ---
# Agent 1: Uses a tool and output_key
capital_agent_with_tool = LlmAgent(
    model=MODEL_NAME,
    name="capital_agent_tool",
    description="Retrieves the capital city using a specific tool.",
    instruction="""You are a helpful agent that provides the capital city of a country using a tool.
The user will provide the country name in a JSON format like {"country": "country_name"}.
1. Extract the country name.
2. Use the `get_capital_city` tool to find the capital.
3. Respond clearly to the user, stating the capital city found by the tool.
""",
    tools=[get_capital_city],
    input_schema=CountryInput,
    output_key="capital_tool_result",  # Store final text response
)

# Agent 2: Uses output_schema (NO tools possible)
structured_info_agent_schema = LlmAgent(
    model=MODEL_NAME,
    name="structured_info_agent_schema",
    description="Provides capital and estimated population in a specific JSON format.",
    instruction=f"""You are an agent that provides country information.
The user will provide the country name in a JSON format like {{"country": "country_name"}}.
Respond ONLY with a JSON object matching this exact schema:
{json.dumps(CapitalInfoOutput.model_json_schema(), indent=2)}
Use your knowledge to determine the capital and estimate the population. Do not use any tools.
""",
    # *** NO tools parameter here - using output_schema prevents tool use ***
    input_schema=CountryInput,
    output_schema=CapitalInfoOutput,  # Enforce JSON output structure
    output_key="structured_info_result",  # Store final JSON response
)

# --- 5. Set up Session Management and Runners ---
session_service = InMemorySessionService()
# Create separate sessions for clarity, though not strictly necessary if context is managed
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID_TOOL_AGENT)
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID_SCHEMA_AGENT)

# Create a runner for EACH agent
capital_runner = Runner(
    agent=capital_agent_with_tool,
    app_name=APP_NAME,
    session_service=session_service
)
structured_runner = Runner(
    agent=structured_info_agent_schema,
    app_name=APP_NAME,
    session_service=session_service
)

# --- 6. Define Agent Interaction Logic ---
async def call_agent_and_print(runner_instance: Runner, agent_instance: LlmAgent, session_id: str, query_json: str):
    """Sends a query to the specified agent/runner and prints results."""
    print(f"\n>>> Calling Agent: '{agent_instance.name}' | Query: {query_json}")
    user_content = types.Content(role='user', parts=[types.Part(text=query_json)])
    final_response_content = "No final response received."

    async for event in runner_instance.run_async(user_id=USER_ID, session_id=session_id, new_message=user_content):
        # print(f"Event: {event.type}, Author: {event.author}") # Uncomment for detailed logging
        if event.is_final_response() and event.content and event.content.parts:
            # For output_schema, the content is the JSON string itself
            final_response_content = event.content.parts[0].text

    print(f"<<< Agent '{agent_instance.name}' Response: {final_response_content}")
    current_session = session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    stored_output = current_session.state.get(agent_instance.output_key)

    # Pretty print if the stored output looks like JSON (likely from output_schema)
    print(f"--- Session State ['{agent_instance.output_key}']: ", end="")
    try:
        # Attempt to parse and pretty print if it's JSON
        parsed_output = json.loads(stored_output)
        print(json.dumps(parsed_output, indent=2))
    except (json.JSONDecodeError, TypeError):
        # Otherwise, print as string
        print(stored_output)
    print("-" * 30)

# --- 7. Run Interactions ---
async def main():
    print("--- Testing Agent with Tool ---")
    await call_agent_and_print(capital_runner, capital_agent_with_tool, SESSION_ID_TOOL_AGENT, '{"country": "France"}')
    await call_agent_and_print(capital_runner, capital_agent_with_tool, SESSION_ID_TOOL_AGENT, '{"country": "Canada"}')

    print("\n\n--- Testing Agent with Output Schema (No Tool Use) ---")
    await call_agent_and_print(structured_runner, structured_info_agent_schema, SESSION_ID_SCHEMA_AGENT, '{"country": "France"}')
    await call_agent_and_print(structured_runner, structured_info_agent_schema, SESSION_ID_SCHEMA_AGENT, '{"country": "Japan"}')

if __name__ == "__main__":
    asyncio.run(main())
```

**Java Example:**
```java
// --- Full example code demonstrating LlmAgent with Tools vs. Output Schema ---
import com.google.adk.agents.LlmAgent;
import com.google.adk.events.Event;
import com.google.adk.runner.Runner; // Assuming Runner is correctly imported
import com.google.adk.sessions.InMemorySessionService;
import com.google.adk.sessions.Session;
import com.google.adk.tools.Annotations; // For @Schema
import com.google.adk.tools.FunctionTool;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import com.google.genai.types.Schema;
import io.reactivex.rxjava3.core.Flowable;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

public class LlmAgentExample {
    // --- 1. Define Constants ---
    private static final String MODEL_NAME = "gemini-2.0-flash";
    private static final String APP_NAME = "capital_agent_app_java"; // Changed for clarity
    private static final String USER_ID = "test_user_789"; // Changed for clarity
    private static final String SESSION_ID_TOOL_AGENT = "session_tool_agent_java";
    private static final String SESSION_ID_SCHEMA_AGENT = "session_schema_agent_java";

    // --- 2. Define Schemas ---
    // Input schema used by both agents
    private static final Schema COUNTRY_INPUT_SCHEMA = Schema.builder()
        .type("OBJECT")
        .description("Input for specifying a country.")
        .properties(Map.of(
            "country", Schema.builder()
                .type("STRING")
                .description("The country to get information about.")
                .build()
        ))
        .required(List.of("country"))
        .build();

    // Output schema ONLY for the second agent
    private static final Schema CAPITAL_INFO_OUTPUT_SCHEMA = Schema.builder()
        .type("OBJECT")
        .description("Schema for capital city information.")
        .properties(Map.of(
            "capital", Schema.builder()
                .type("STRING")
                .description("The capital city of the country.")
                .build(),
            "population_estimate", Schema.builder()
                .type("STRING")
                .description("An estimated population of the capital city.")
                .build()
        ))
        .required(List.of("capital", "population_estimate"))
        .build();

    // --- 3. Define the Tool (Only for the first agent) ---
    // Retrieves the capital city of a given country.
    public static Map<String, Object> getCapitalCity(
        @Annotations.Schema(name = "country", description = "The country to get capital for") String country
    ) {
        System.out.printf("%n-- Tool Call: getCapitalCity(country='%s') --%n", country);
        Map<String, String> countryCapitals = new HashMap<>();
        countryCapitals.put("united states", "Washington, D.C.");
        countryCapitals.put("canada", "Ottawa");
        countryCapitals.put("france", "Paris");
        countryCapitals.put("japan", "Tokyo");
        String result = countryCapitals.getOrDefault(
            country.toLowerCase(), "Sorry, I couldn't find the capital for " + country + "."
        );
        System.out.printf("-- Tool Result: '%s' --%n", result);
        return Map.of("result", result); // Tools must return a Map
    }

    public static void main(String[] args){
        LlmAgentExample agentExample = new LlmAgentExample();
        FunctionTool capitalTool = FunctionTool.create(agentExample.getClass(), "getCapitalCity");

        // --- 4. Configure Agents ---
        // Agent 1: Uses a tool and output_key
        LlmAgent capitalAgentWithTool = LlmAgent.builder()
            .model(MODEL_NAME)
            .name("capital_agent_tool_java")
            .description("Retrieves the capital city using a specific tool.")
            .instruction("""
            You are a helpful agent that provides the capital city of a country using a tool.
            1. Extract the country name.
            2. Use the `get_capital_city` tool to find the capital.
            3. Respond clearly to the user, stating the capital city found by the tool.
            """)
            .tools(capitalTool)
            .inputSchema(COUNTRY_INPUT_SCHEMA)
            .outputKey("capital_tool_result") // Store final text response
            .build();

        // Agent 2: Uses an output schema
        LlmAgent structuredInfoAgentSchema = LlmAgent.builder()
            .model(MODEL_NAME)
            .name("structured_info_agent_schema_java")
            .description("Provides capital and estimated population in a specific JSON format.")
            .instruction(String.format("""
            You are an agent that provides country information.
            Respond ONLY with a JSON object matching this exact schema:
            %s
            Use your knowledge to determine the capital and estimate the population. Do not use any tools.
            """, CAPITAL_INFO_OUTPUT_SCHEMA.toJson())) // Use toJson for schema string
            // *** NO tools parameter here - using output_schema prevents tool use ***
            .inputSchema(COUNTRY_INPUT_SCHEMA)
            .outputSchema(CAPITAL_INFO_OUTPUT_SCHEMA) // Enforce JSON output structure
            .outputKey("structured_info_result")   // Store final JSON response
            .build();

        // --- 5. Set up Session Management and Runners ---
        InMemorySessionService sessionService = new InMemorySessionService();
        sessionService.createSession(APP_NAME, USER_ID, null, SESSION_ID_TOOL_AGENT).blockingGet();
        sessionService.createSession(APP_NAME, USER_ID, null, SESSION_ID_SCHEMA_AGENT).blockingGet();

        Runner capitalRunner = new Runner(capitalAgentWithTool, APP_NAME, null, sessionService);
        Runner structuredRunner = new Runner(structuredInfoAgentSchema, APP_NAME, null, sessionService);

        // --- 6. Run Interactions ---
        System.out.println("--- Testing Agent with Tool (Java) ---");
        agentExample.callAgentAndPrint(capitalRunner, capitalAgentWithTool, SESSION_ID_TOOL_AGENT, "{\"country\": \"France\"}");
        agentExample.callAgentAndPrint(capitalRunner, capitalAgentWithTool, SESSION_ID_TOOL_AGENT, "{\"country\": \"Canada\"}");

        System.out.println("\n\n--- Testing Agent with Output Schema (No Tool Use) (Java) ---");
        agentExample.callAgentAndPrint(structuredRunner, structuredInfoAgentSchema, SESSION_ID_SCHEMA_AGENT, "{\"country\": \"France\"}");
        agentExample.callAgentAndPrint(structuredRunner, structuredInfoAgentSchema, SESSION_ID_SCHEMA_AGENT, "{\"country\": \"Japan\"}");
    }

    // --- 7. Define Agent Interaction Logic ---
    public void callAgentAndPrint(Runner runner, LlmAgent agent, String sessionId, String queryJson) {
        System.out.printf("%n>>> Calling Agent: '%s' | Session: '%s' | Query: %s%n", agent.name(), sessionId, queryJson);
        Content userContent = Content.fromParts(Part.fromText(queryJson));
        final String[] finalResponseContent = {"No final response received."};

        Flowable<Event> eventStream = runner.runAsync(USER_ID, sessionId, userContent);

        // Stream event response
        eventStream.blockingForEach(event -> {
            if (event.finalResponse() && event.content().isPresent()) {
                event.content().get().parts()
                    .flatMap(parts -> parts.isEmpty() ? Optional.empty() : Optional.of(parts.get(0)))
                    .flatMap(Part::text)
                    .ifPresent(text -> finalResponseContent[0] = text);
            }
        });
        System.out.printf("<<< Agent '%s' Response: %s%n", agent.name(), finalResponseContent[0]);

        // Retrieve the session again to get the updated state
        Session updatedSession = runner.sessionService().getSession(APP_NAME, USER_ID, sessionId, Optional.empty()).blockingGet();
        if (updatedSession != null && agent.outputKey().isPresent()) {
            // Print to verify if the stored output looks like JSON (likely from output_schema)
            System.out.printf("--- Session State ['%s']: %s%n",
                agent.outputKey().get(),
                updatedSession.state().get(agent.outputKey().get()));
        }
        System.out.println("------------------------------");
    }
}
```

#### Related Concepts (Deferred Topics)
While this page covers the core configuration of `LlmAgent`, several related concepts provide more advanced control and are detailed elsewhere:
*   **Callbacks**: Intercepting execution points (before/after model calls, before/after tool calls) using `before_model_callback`, `after_model_callback`, etc. See Callbacks.
*   **Multi-Agent Control**: Advanced strategies for agent interaction, including planning (`planner`), controlling agent transfer (`disallow_transfer_to_parent`, `disallow_transfer_to_peers`), and system-wide instructions (`global_instruction`). See Multi-Agents.

### Workflow Agents
This section introduces "workflow agents" - specialized agents that control the execution flow of its sub-agents.
Workflow agents are specialized components in ADK designed purely for orchestrating the execution flow of sub-agents. Their primary role is to manage how and when other agents run, defining the control flow of a process.
Unlike LLM Agents, which use Large Language Models for dynamic reasoning and decision-making, Workflow Agents operate based on predefined logic. They determine the execution sequence according to their type (e.g., sequential, parallel, loop) without consulting an LLM for the orchestration itself. This results in deterministic and predictable execution patterns.
ADK provides three core workflow agent types, each implementing a distinct execution pattern:

*   **Sequential Agents**: Executes sub-agents one after another, in sequence.
*   **Loop Agents**: Repeatedly executes its sub-agents until a specific termination condition is met.
*   **Parallel Agents**: Executes multiple sub-agents in parallel.

#### Why Use Workflow Agents?
Workflow agents are essential when you need explicit control over how a series of tasks or agents are executed. They provide:
*   **Predictability**: The flow of execution is guaranteed based on the agent type and configuration.
*   **Reliability**: Ensures tasks run in the required order or pattern consistently.
*   **Structure**: Allows you to build complex processes by composing agents within clear control structures.

While the workflow agent manages the control flow deterministically, the sub-agents it orchestrates can themselves be any type of agent, including intelligent `LLM Agent` instances. This allows you to combine structured process control with flexible, LLM-powered task execution.

#### Sequential agents
The `SequentialAgent` is a workflow agent that executes its sub-agents in the order they are specified in the list.
Use the `SequentialAgent` when you want the execution to occur in a fixed, strict order.

**Example**
You want to build an agent that can summarize any webpage, using two tools: `Get Page Contents` and `Summarize Page`. Because the agent must always call `Get Page Contents` before calling `Summarize Page` (you can't summarize from nothing!), you should build your agent using a `SequentialAgent`.
As with other workflow agents, the `SequentialAgent` is not powered by an LLM, and is thus deterministic in how it executes. That being said, workflow agents are concerned only with their execution (i.e. in sequence), and not their internal logic; the tools or sub-agents of a workflow agent may or may not utilize LLMs.

**How it works**
When the `SequentialAgent`'s `Run Async` method is called, it performs the following actions:
1.  **Iteration**: It iterates through the `sub agents` list in the order they were provided.
2.  **Sub-Agent Execution**: For each sub-agent in the list, it calls the sub-agent's `Run Async` method.

**Full Example: Code Development Pipeline**
Consider a simplified code development pipeline:
1.  **Code Writer Agent**: An LLM Agent that generates initial code based on a specification.
2.  **Code Reviewer Agent**: An LLM Agent that reviews the generated code for errors, style issues, and adherence to best practices. It receives the output of the Code Writer Agent.
3.  **Code Refactorer Agent**: An LLM Agent that takes the reviewed code (and the reviewer's comments) and refactors it to improve quality and address issues.
A `SequentialAgent` is perfect for this:
```python
# SequentialAgent(sub_agents=[CodeWriterAgent, CodeReviewerAgent, CodeRefactorerAgent])
```
This ensures the code is written, then reviewed, and finally refactored, in a strict, dependable order. The output from each sub-agent is passed to the next by storing them in state via `Output Key`.

**Python Example:**
```python
# Part of agent.py --> Follow https://google.github.io/adk-docs/get-started/quickstart/ to learn the setup
from google.adk.agents import LlmAgent, SequentialAgent
# Assume GEMINI_MODEL is defined, e.g., "gemini-2.0-flash"
GEMINI_MODEL = "gemini-2.0-flash"

# --- 1. Define Sub-Agents for Each Pipeline Stage ---
# Code Writer Agent
# Takes the initial specification (from user query) and writes code.
code_writer_agent = LlmAgent(
    name="CodeWriterAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Python Code Generator. Based *only* on the user's request, write Python code that fulfills the requirement.
Output *only* the complete Python code block, enclosed in triple backticks (```python ... ```).
Do not add any other text before or after the code block.
""",
    description="Writes initial Python code based on a specification.",
    output_key="generated_code"  # Stores output in state['generated_code']
)

# Code Reviewer Agent
# Takes the code generated by the previous agent (read from state) and provides feedback.
code_reviewer_agent = LlmAgent(
    name="CodeReviewerAgent",
    model=GEMINI_MODEL,
    instruction="""You are an expert Python Code Reviewer. Your task is to provide constructive feedback on the provided code.
**Code to Review:**
```python
{generated_code}
```
**Review Criteria:**
1.  **Correctness:** Does the code work as intended? Are there logic errors?
2.  **Readability:** Is the code clear and easy to understand? Follows PEP 8 style guidelines?
3.  **Efficiency:** Is the code reasonably efficient? Any obvious performance bottlenecks?
4.  **Edge Cases:** Does the code handle potential edge cases or invalid inputs gracefully?
5.  **Best Practices:** Does the code follow common Python best practices?
**Output:**
Provide your feedback as a concise, bulleted list. Focus on the most important points for improvement.
If the code is excellent and requires no changes, simply state: "No major issues found."
Output *only* the review comments or the "No major issues" statement.
""",
    description="Reviews code and provides feedback.",
    output_key="review_comments",  # Stores output in state['review_comments']
)

# Code Refactorer Agent
# Takes the original code and the review comments (read from state) and refactors the code.
code_refactorer_agent = LlmAgent(
    name="CodeRefactorerAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Python Code Refactoring AI. Your goal is to improve the given Python code based on the provided review comments.
**Original Code:**
```python
{generated_code}
```
**Review Comments:**
{review_comments}
**Task:**
Carefully apply the suggestions from the review comments to refactor the original code.
If the review comments state "No major issues found," return the original code unchanged.
Ensure the final code is complete, functional, and includes necessary imports and docstrings.
**Output:**
Output *only* the final, refactored Python code block, enclosed in triple backticks (```python ... ```).
Do not add any other text before or after the code block.
""",
    description="Refactors code based on review comments.",
    output_key="refactored_code",  # Stores output in state['refactored_code']
)

# --- 2. Create the SequentialAgent ---
# This agent orchestrates the pipeline by running the sub_agents in order.
code_pipeline_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[
        code_writer_agent,
        code_reviewer_agent,
        code_refactorer_agent
    ],
    description="Executes a sequence of code writing, reviewing, and refactoring.",
    # The agents will run in the order provided: Writer -> Reviewer -> Refactorer
)

# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = code_pipeline_agent
```

**Java Example:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.SequentialAgent;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;

public class SequentialAgentExample {
    private static final String APP_NAME = "CodePipelineAgent";
    private static final String USER_ID = "test_user_456";
    private static final String MODEL_NAME = "gemini-2.0-flash";

    public static void main(String[] args) {
        SequentialAgentExample sequentialAgentExample = new SequentialAgentExample();
        sequentialAgentExample.runAgent("Write a Java function to calculate the factorial of a number.");
    }

    public void runAgent(String prompt) {
        LlmAgent codeWriterAgent = LlmAgent.builder()
            .model(MODEL_NAME)
            .name("CodeWriterAgent")
            .description("Writes initial Java code based on a specification.")
            .instruction("""
            You are a Java Code Generator. Based *only* on the user's request, write Java code that fulfills the requirement.
            Output *only* the complete Java code block, enclosed in triple backticks (```java ... ```).
            Do not add any other text before or after the code block.
            """)
            .outputKey("generated_code")
            .build();

        LlmAgent codeReviewerAgent = LlmAgent.builder()
            .model(MODEL_NAME)
            .name("CodeReviewerAgent")
            .description("Reviews code and provides feedback.")
            .instruction("""
            You are an expert Java Code Reviewer. Your task is to provide constructive feedback on the provided code.
            **Code to Review:**
            ```java
            {generated_code}
            ```
            **Review Criteria:**
            1.  **Correctness:** Does the code work as intended? Are there logic errors?
            2.  **Readability:** Is the code clear and easy to understand? Follows Java style guidelines?
            3.  **Efficiency:** Is the code reasonably efficient? Any obvious performance bottlenecks?
            4.  **Edge Cases:** Does the code handle potential edge cases or invalid inputs gracefully?
            5.  **Best Practices:** Does the code follow common Java best practices?
            **Output:**
            Provide your feedback as a concise, bulleted list. Focus on the most important points for improvement.
            If the code is excellent and requires no changes, simply state: "No major issues found."
            Output *only* the review comments or the "No major issues" statement.
            """)
            .outputKey("review_comments")
            .build();

        LlmAgent codeRefactorerAgent = LlmAgent.builder()
            .model(MODEL_NAME)
            .name("CodeRefactorerAgent")
            .description("Refactors code based on review comments.")
            .instruction("""
            You are a Java Code Refactoring AI. Your goal is to improve the given Java code based on the provided review comments.
            **Original Code:**
            ```java
            {generated_code}
            ```
            **Review Comments:**
            {review_comments}
            **Task:**
            Carefully apply the suggestions from the review comments to refactor the original code.
            If the review comments state "No major issues found," return the original code unchanged.
            Ensure the final code is complete, functional, and includes necessary imports and docstrings.
            **Output:**
            Output *only* the final, refactored Java code block, enclosed in triple backticks (```java ... ```).
            Do not add any other text before or after the code block.
            """)
            .outputKey("refactored_code")
            .build();

        SequentialAgent codePipelineAgent = SequentialAgent.builder()
            .name(APP_NAME)
            .description("Executes a sequence of code writing, reviewing, and refactoring.")
            // The agents will run in the order provided: Writer -> Reviewer -> Refactorer
            .subAgents(codeWriterAgent, codeReviewerAgent, codeRefactorerAgent)
            .build();

        // Create an InMemoryRunner
        InMemoryRunner runner = new InMemoryRunner(codePipelineAgent, APP_NAME);
        // InMemoryRunner automatically creates a session service. Create a session using the service
        Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();

        Content userMessage = Content.fromParts(Part.fromText(prompt));

        // Run the agent
        Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);

        // Stream event response
        eventStream.blockingForEach(event -> {
            if (event.finalResponse()) {
                System.out.println(event.stringifyContent());
            }
        });
    }
}
```

#### Parallel agents
The `ParallelAgent` is a workflow agent that executes its sub-agents concurrently. This dramatically speeds up workflows where tasks can be performed independently.
Use `ParallelAgent` when: For scenarios prioritizing speed and involving independent, resource-intensive tasks, a `ParallelAgent` facilitates efficient parallel execution. When sub-agents operate without dependencies, their tasks can be performed concurrently, significantly reducing overall processing time.
As with other workflow agents, the `ParallelAgent` is not powered by an LLM, and is thus deterministic in how it executes. That being said, workflow agents are only concerned with their execution (i.e. executing sub-agents in parallel), and not their internal logic; the tools or sub-agents of a workflow agent may or may not utilize LLMs.

**Example**
This approach is particularly beneficial for operations like multi-source data retrieval or heavy computations, where parallelization yields substantial performance gains. Importantly, this strategy assumes no inherent need for shared state or direct information exchange between the concurrently executing agents.

**How it works**
When the `ParallelAgent`'s `run_async()` method is called:
1.  **Concurrent Execution**: It initiates the `run_async()` method of each sub-agent present in the `sub_agents` list concurrently. This means all the agents start running at (approximately) the same time.
2.  **Independent Branches**: Each sub-agent operates in its own execution branch. There is no automatic sharing of conversation history or state between these branches during execution.
3.  **Result Collection**: The `ParallelAgent` manages the parallel execution and, typically, provides a way to access the results from each sub-agent after they have completed (e.g., through a list of results or events). The order of results may not be deterministic.

**Independent Execution and State Management**
It's crucial to understand that sub-agents within a `ParallelAgent` run independently. If you need communication or data sharing between these agents, you must implement it explicitly. Possible approaches include:
*   **Shared `InvocationContext`**: You could pass a shared `InvocationContext` object to each sub-agent. This object could act as a shared data store. However, you'd need to manage concurrent access to this shared context carefully (e.g., using locks) to avoid race conditions.
*   **External State Management**: Use an external database, message queue, or other mechanism to manage shared state and facilitate communication between agents.
*   **Post-Processing**: Collect results from each branch, and then implement logic to coordinate data afterwards.

**Full Example: Parallel Web Research**
Imagine researching multiple topics simultaneously:
1.  **Researcher Agent 1**: An `LlmAgent` that researches "renewable energy sources."
2.  **Researcher Agent 2**: An `LlmAgent` that researches "electric vehicle technology."
3.  **Researcher Agent 3**: An `LlmAgent` that researches "carbon capture methods."
```python
# ParallelAgent(sub_agents=[ResearcherAgent1, ResearcherAgent2, ResearcherAgent3])
```
These research tasks are independent. Using a `ParallelAgent` allows them to run concurrently, potentially reducing the total research time significantly compared to running them sequentially. The results from each agent would be collected separately after they finish.

**Python Example:**
```python
# Part of agent.py --> Follow https://google.github.io/adk-docs/get-started/quickstart/ to learn the setup
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search # Assuming google_search tool is available
# Assume GEMINI_MODEL is defined, e.g., "gemini-2.0-flash"
GEMINI_MODEL = "gemini-2.0-flash"

# --- 1. Define Researcher Sub-Agents (to run in parallel) ---
# Researcher 1: Renewable Energy
researcher_agent_1 = LlmAgent(
    name="RenewableEnergyResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in energy.
Research the latest advancements in 'renewable energy sources'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.
""",
    description="Researches renewable energy sources.",
    tools=[google_search],
    # Store result in state for the merger agent
    output_key="renewable_energy_result"
)

# Researcher 2: Electric Vehicles
researcher_agent_2 = LlmAgent(
    name="EVResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in transportation.
Research the latest developments in 'electric vehicle technology'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.
""",
    description="Researches electric vehicle technology.",
    tools=[google_search],
    # Store result in state for the merger agent
    output_key="ev_technology_result"
)

# Researcher 3: Carbon Capture
researcher_agent_3 = LlmAgent(
    name="CarbonCaptureResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in climate solutions.
Research the current state of 'carbon capture methods'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.
""",
    description="Researches carbon capture methods.",
    tools=[google_search],
    # Store result in state for the merger agent
    output_key="carbon_capture_result"
)

# --- 2. Create the ParallelAgent (Runs researchers concurrently) ---
# This agent orchestrates the concurrent execution of the researchers.
# It finishes once all researchers have completed and stored their results in state.
parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    sub_agents=[
        researcher_agent_1,
        researcher_agent_2,
        researcher_agent_3
    ],
    description="Runs multiple research agents in parallel to gather information."
)

# --- 3. Define the Merger Agent (Runs *after* the parallel agents) ---
# This agent takes the results stored in the session state by the parallel agents
# and synthesizes them into a single, structured response with attributions.
merger_agent = LlmAgent(
    name="SynthesisAgent",
    model=GEMINI_MODEL,  # Or potentially a more powerful model if needed for synthesis
    instruction="""You are an AI Assistant responsible for combining research findings into a structured report.
Your primary task is to synthesize the following research summaries, clearly attributing findings to their source areas.
Structure your response using headings for each topic. Ensure the report is coherent and integrates the key points smoothly.
**Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**

**Input Summaries:**
*   **Renewable Energy:** {renewable_energy_result}
*   **Electric Vehicles:** {ev_technology_result}
*   **Carbon Capture:** {carbon_capture_result}

**Output Format:**
## Summary of Recent Sustainable Technology Advancements

### Renewable Energy Findings (Based on RenewableEnergyResearcher's findings)
[Synthesize and elaborate *only* on the renewable energy input summary provided above.]

### Electric Vehicle Findings (Based on EVResearcher's findings)
[Synthesize and elaborate *only* on the EV input summary provided above.]

### Carbon Capture Findings (Based on CarbonCaptureResearcher's findings)
[Synthesize and elaborate *only* on the carbon capture input summary provided above.]

### Overall Conclusion
[Provide a brief (1-2 sentence) concluding statement that connects *only* the findings presented above.]

Output *only* the structured report following this format.
Do not include introductory or concluding phrases outside this structure, and strictly adhere to using only the provided input summary content.
""",
    description="Combines research findings from parallel agents into a structured, cited report, strictly grounded on provided inputs.",
    # No tools needed for merging
    # No output_key needed here, as its direct response is the final output of the sequence
)

# --- 4. Create the SequentialAgent (Orchestrates the overall flow) ---
# This is the main agent that will be run. It first executes the ParallelAgent
# to populate the state, and then executes the MergerAgent to produce the final output.
sequential_pipeline_agent = SequentialAgent(
    name="ResearchAndSynthesisPipeline",
    # Run parallel research first, then merge
    sub_agents=[
        parallel_research_agent,
        merger_agent
    ],
    description="Coordinates parallel research and synthesizes the results."
)
root_agent = sequential_pipeline_agent
```

**Java Example:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.ParallelAgent;
import com.google.adk.agents.SequentialAgent;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.adk.tools.GoogleSearchTool;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;

public class ParallelResearchPipeline {
    private static final String APP_NAME = "parallel_research_app";
    private static final String USER_ID = "research_user_01";
    private static final String GEMINI_MODEL = "gemini-2.0-flash";
    // Assume google_search is an instance of the GoogleSearchTool
    private static final GoogleSearchTool googleSearchTool = new GoogleSearchTool();

    public static void main(String[] args) {
        String query = "Summarize recent sustainable tech advancements.";
        SequentialAgent sequentialPipelineAgent = initAgent();
        runAgent(sequentialPipelineAgent, query);
    }

    public static SequentialAgent initAgent() {
        // --- 1. Define Researcher Sub-Agents (to run in parallel) ---
        LlmAgent researcherAgent1 = LlmAgent.builder()
            .name("RenewableEnergyResearcher")
            .model(GEMINI_MODEL)
            .instruction("""
            You are an AI Research Assistant specializing in energy.
            Research the latest advancements in 'renewable energy sources'.
            Use the Google Search tool provided.
            Summarize your key findings concisely (1-2 sentences).
            Output *only* the summary.
            """)
            .description("Researches renewable energy sources.")
            .tools(googleSearchTool)
            .outputKey("renewable_energy_result") // Store result in state
            .build();

        LlmAgent researcherAgent2 = LlmAgent.builder()
            .name("EVResearcher")
            .model(GEMINI_MODEL)
            .instruction("""
            You are an AI Research Assistant specializing in transportation.
            Research the latest developments in 'electric vehicle technology'.
            Use the Google Search tool provided.
            Summarize your key findings concisely (1-2 sentences).
            Output *only* the summary.
            """)
            .description("Researches electric vehicle technology.")
            .tools(googleSearchTool)
            .outputKey("ev_technology_result") // Store result in state
            .build();

        LlmAgent researcherAgent3 = LlmAgent.builder()
            .name("CarbonCaptureResearcher")
            .model(GEMINI_MODEL)
            .instruction("""
            You are an AI Research Assistant specializing in climate solutions.
            Research the current state of 'carbon capture methods'.
            Use the Google Search tool provided.
            Summarize your key findings concisely (1-2 sentences).
            Output *only* the summary.
            """)
            .description("Researches carbon capture methods.")
            .tools(googleSearchTool)
            .outputKey("carbon_capture_result") // Store result in state
            .build();

        // --- 2. Create the ParallelAgent (Runs researchers concurrently) ---
        ParallelAgent parallelResearchAgent = ParallelAgent.builder()
            .name("ParallelWebResearchAgent")
            .subAgents(researcherAgent1, researcherAgent2, researcherAgent3)
            .description("Runs multiple research agents in parallel to gather information.")
            .build();

        // --- 3. Define the Merger Agent (Runs *after* the parallel agents) ---
        LlmAgent mergerAgent = LlmAgent.builder()
            .name("SynthesisAgent")
            .model(GEMINI_MODEL)
            .instruction("""
            You are an AI Assistant responsible for combining research findings into a structured report.
            Your primary task is to synthesize the following research summaries, clearly attributing findings to their source areas.
            Structure your response using headings for each topic. Ensure the report is coherent and integrates the key points smoothly.
            **Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**

            **Input Summaries:**
            *   **Renewable Energy:** {renewable_energy_result}
            *   **Electric Vehicles:** {ev_technology_result}
            *   **Carbon Capture:** {carbon_capture_result}

            **Output Format:**
            ## Summary of Recent Sustainable Technology Advancements

            ### Renewable Energy Findings (Based on RenewableEnergyResearcher's findings)
            [Synthesize and elaborate *only* on the renewable energy input summary provided above.]

            ### Electric Vehicle Findings (Based on EVResearcher's findings)
            [Synthesize and elaborate *only* on the EV input summary provided above.]

            ### Carbon Capture Findings (Based on CarbonCaptureResearcher's findings)
            [Synthesize and elaborate *only* on the carbon capture input summary provided above.]

            ### Overall Conclusion
            [Provide a brief (1-2 sentence) concluding statement that connects *only* the findings presented above.]

            Output *only* the structured report following this format.
            Do not include introductory or concluding phrases outside this structure, and strictly adhere to using only the provided input summary content.
            """)
            .description("Combines research findings from parallel agents into a structured, cited report, strictly grounded on provided inputs.")
            .build();

        // --- 4. Create the SequentialAgent (Orchestrates the overall flow) ---
        SequentialAgent sequentialPipelineAgent = SequentialAgent.builder()
            .name("ResearchAndSynthesisPipeline")
            .subAgents(parallelResearchAgent, mergerAgent) // Run parallel research first, then merge
            .description("Coordinates parallel research and synthesizes the results.")
            .build();
        return sequentialPipelineAgent;
    }

    public static void runAgent(SequentialAgent sequentialPipelineAgent, String query) {
        InMemoryRunner runner = new InMemoryRunner(sequentialPipelineAgent, APP_NAME);
        Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
        Content userMessage = Content.fromParts(Part.fromText(query));
        Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
        eventStream.blockingForEach(event -> {
            if (event.finalResponse()) {
                System.out.printf("Event Author: %s \n Event Response: %s \n\n\n",
                    event.author(), event.stringifyContent());
            }
        });
    }
}
```

#### Loop agents
The `LoopAgent` is a workflow agent that executes its sub-agents in a loop (i.e. iteratively). It repeatedly runs a sequence of agents for a specified number of iterations or until a termination condition is met.
Use the `LoopAgent` when your workflow involves repetition or iterative refinement, such as like revising code.

**Example**
You want to build an agent that can generate images of food, but sometimes when you want to generate a specific number of items (e.g. 5 bananas), it generates a different number of those items in the image (e.g. an image of 7 bananas). You have two tools: `Generate Image`, `Count Food Items`. Because you want to keep generating images until it either correctly generates the specified number of items, or after a certain number of iterations, you should build your agent using a `LoopAgent`.
As with other workflow agents, the `LoopAgent` is not powered by an LLM, and is thus deterministic in how it executes. That being said, workflow agents are only concerned only with their execution (i.e. in a loop), and not their internal logic; the tools or sub-agents of a workflow agent may or may not utilize LLMs.

**How it Works**
When the `LoopAgent`'s `Run Async` method is called, it performs the following actions:
1.  **Sub-Agent Execution**: It iterates through the `Sub Agents` list in order. For each sub-agent, it calls the agent's `Run Async` method.
2.  **Termination Check**: Crucially, the `LoopAgent` itself does not inherently decide when to stop looping. You must implement a termination mechanism to prevent infinite loops. Common strategies include:
    *   **Max Iterations**: Set a maximum number of iterations in the `LoopAgent`. The loop will terminate after that many iterations.
    *   **Escalation from sub-agent**: Design one or more sub-agents to evaluate a condition (e.g., "Is the document quality good enough?", "Has a consensus been reached?"). If the condition is met, the sub-agent can signal termination (e.g., by raising a custom event, setting a flag in a shared context, or returning a specific value).

**Full Example: Iterative Document Improvement**
Imagine a scenario where you want to iteratively improve a document:
*   **Writer Agent**: An `LlmAgent` that generates or refines a draft on a topic.
*   **Critic Agent**: An `LlmAgent` that critiques the draft, identifying areas for improvement.
```python
# LoopAgent(sub_agents=[WriterAgent, CriticAgent], max_iterations=5)
```
In this setup, the `LoopAgent` would manage the iterative process. The `CriticAgent` could be designed to return a "STOP" signal when the document reaches a satisfactory quality level, preventing further iterations. Alternatively, the `max_iterations` parameter could be used to limit the process to a fixed number of cycles, or external logic could be implemented to make stop decisions. The loop would run at most five times, ensuring the iterative refinement doesn't continue indefinitely.

**Python Example:**
```python
# Part of agent.py --> Follow https://google.github.io/adk-docs/get-started/quickstart/ to learn the setup
from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent, BaseAgent
from google.adk.events import Event, EventActions
from google.adk.tools import ToolContext, FunctionTool
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator

# --- Constants ---
APP_NAME = "doc_writing_app_v3"  # New App Name
USER_ID = "dev_user_01"
SESSION_ID_BASE = "loop_exit_tool_session"  # New Base Session ID
GEMINI_MODEL = "gemini-2.0-flash"
STATE_INITIAL_TOPIC = "initial_topic" # Key in session state for initial topic

# --- State Keys ---
STATE_CURRENT_DOC = "current_document"
STATE_CRITICISM = "criticism"

# Define the exact phrase the Critic should use to signal completion
COMPLETION_PHRASE = "No major issues found."

# --- Tool Definition ---
def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the critique indicates no further changes are needed,
    signaling the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True  # Set escalate on EventActions
    # Return empty dict as tools should typically return JSON-serializable output
    return {}

# --- Agent Definitions ---
# STEP 1: Initial Writer Agent (Runs ONCE at the beginning)
initial_writer_agent = LlmAgent(
    name="InitialWriterAgent",
    model=GEMINI_MODEL,
    include_contents='none', # MODIFIED
    # Instruction: Ask for a slightly more developed start
    instruction=f"""You are a Creative Writing Assistant tasked with starting a story.
Write the *first draft* of a short story (aim for 2-4 sentences).
Base the content *only* on the topic provided below.
Try to introduce a specific element (like a character, a setting detail, or a starting action) to make it engaging.

Topic: {{ {STATE_INITIAL_TOPIC} }}

Output *only* the story/document text. Do not add introductions or explanations.
""",
    description="Writes the initial document draft based on the topic, aiming for some initial substance.",
    output_key=STATE_CURRENT_DOC
)

# STEP 2a: Critic Agent (Inside the Refinement Loop)
critic_agent_in_loop = LlmAgent(
    name="CriticAgent",
    model=GEMINI_MODEL,
    include_contents='none', # MODIFIED
    # Instruction: More nuanced completion criteria, look for clear improvement paths.
    instruction=f"""You are a Constructive Critic AI reviewing a short document draft (typically 2-6 sentences).
Your goal is balanced feedback.

**Document to Review:**
```
{{ {STATE_CURRENT_DOC} }}
```

**Task:**
Review the document for clarity, engagement, and basic coherence according to the initial topic (if known).

IF you identify 1-2 *clear and actionable* ways the document could be improved to better capture the topic or enhance reader engagement (e.g., "Needs a stronger opening sentence", "Clarify the character's goal"):
  Provide these specific suggestions concisely. Output *only* the critique text.
ELSE IF the document is coherent, addresses the topic adequately for its length, and has no glaring errors or obvious omissions:
  Respond *exactly* with the phrase "{COMPLETION_PHRASE}" and nothing else. It doesn't need to be perfect, just functionally complete for this stage.
Avoid suggesting purely subjective stylistic preferences if the core is sound.
Do not add explanations. Output only the critique OR the exact completion phrase.
""",
    description="Reviews the current draft, providing critique if clear improvements are needed, otherwise signals completion.",
    output_key=STATE_CRITICISM
)

# STEP 2b: Refiner/Exiter Agent (Inside the Refinement Loop)
refiner_agent_in_loop = LlmAgent(
    name="RefinerAgent",
    model=GEMINI_MODEL,
    # Relies solely on state via placeholders
    include_contents='none',
    instruction=f"""You are a Creative Writing Assistant refining a document based on feedback OR exiting the process.

**Current Document:**
```
{{ {STATE_CURRENT_DOC} }}
```

**Critique/Suggestions:**
{{ {STATE_CRITICISM} }}

**Task:**
Analyze the 'Critique/Suggestions'.
IF the critique is *exactly* "{COMPLETION_PHRASE}":
  You MUST call the 'exit_loop' function. Do not output any text.
ELSE (the critique contains actionable feedback):
  Carefully apply the suggestions to improve the 'Current Document'.
  Output *only* the refined document text. Do not add explanations.

Either output the refined document OR call the exit_loop function.
""",
    description="Refines the document based on critique, or calls exit_loop if critique indicates completion.",
    tools=[exit_loop],  # Provide the exit_loop tool
    output_key=STATE_CURRENT_DOC  # Overwrites state['current_document'] with the refined version
)

# STEP 2: Refinement Loop Agent
refinement_loop = LoopAgent(
    name="RefinementLoop",
    # Agent order is crucial: Critique first, then Refine/Exit
    sub_agents=[
        critic_agent_in_loop,
        refiner_agent_in_loop,
    ],
    max_iterations=5  # Limit loops
)

# STEP 3: Overall Sequential Pipeline
# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = SequentialAgent(
    name="IterativeWritingPipeline",
    sub_agents=[
        initial_writer_agent,  # Run first to create initial doc
        refinement_loop        # Then run the critique/refine loop
    ],
    description="Writes an initial document and then iteratively refines it with critique using an exit tool."
)
```

**Java Example:**
```java
import static com.google.adk.agents.LlmAgent.IncludeContents.NONE;

import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.LoopAgent;
import com.google.adk.agents.SequentialAgent;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.adk.tools.Annotations.Schema;
import com.google.adk.tools.FunctionTool;
import com.google.adk.tools.ToolContext;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import java.util.Map;

public class LoopAgentExample {
    // --- Constants ---
    private static final String APP_NAME = "IterativeWritingPipeline";
    private static final String USER_ID = "test_user_456";
    private static final String MODEL_NAME = "gemini-2.0-flash";

    // --- State Keys ---
    private static final String STATE_CURRENT_DOC = "current_document";
    private static final String STATE_CRITICISM = "criticism";
    private static final String STATE_INITIAL_TOPIC = "initial_topic";


    public static void main(String[] args) {
        LoopAgentExample loopAgentExample = new LoopAgentExample();
        loopAgentExample.runAgent("Write a document about a cat");
    }

    // --- Tool Definition ---
    @Schema(
        description =
            "Call this function ONLY when the critique indicates no further changes are needed,"
                + " signaling the iterative process should end.")
    public static Map<String, Object> exitLoop(@Schema(name = "toolContext") ToolContext toolContext) {
        System.out.printf("[Tool Call] exitLoop triggered by %s \n", toolContext.agentName());
        toolContext.actions().setEscalate(true);
        //  Return empty dict as tools should typically return JSON-serializable output
        return Map.of();
    }

    // --- Agent Definitions ---
    public void runAgent(String prompt) {
        // STEP 1: Initial Writer Agent (Runs ONCE at the beginning)
        LlmAgent initialWriterAgent =
            LlmAgent.builder()
                .model(MODEL_NAME)
                .name("InitialWriterAgent")
                .description(
                    "Writes the initial document draft based on the topic, aiming for some initial"
                        + " substance.")
                .instruction(
                    """
                    You are a Creative Writing Assistant tasked with starting a story.
                    Write the *first draft* of a short story (aim for 2-4 sentences).
                    Base the content *only* on the topic provided in session state with key 'initial_topic'.
                    Try to introduce a specific element (like a character, a setting detail, or a starting action) to make it engaging.
                    Output *only* the story/document text. Do not add introductions or explanations.
                    """)
                .outputKey(STATE_CURRENT_DOC)
                .includeContents(NONE)
                .build();

        // STEP 2a: Critic Agent (Inside the Refinement Loop)
        LlmAgent criticAgentInLoop =
            LlmAgent.builder()
                .model(MODEL_NAME)
                .name("CriticAgent")
                .description(
                    "Reviews the current draft, providing critique if clear improvements are needed,"
                        + " otherwise signals completion.")
                .instruction(
                    """
                    You are a Constructive Critic AI reviewing a short document draft (typically 2-6 sentences).
                    Your goal is balanced feedback.

                    **Document to Review:**
                    ```
                    {{current_document}}
                    ```

                    **Task:**
                    Review the document for clarity, engagement, and basic coherence according to the initial topic (if known).

                    IF you identify 1-2 *clear and actionable* ways the document could be improved to better capture the topic or enhance reader engagement (e.g., "Needs a stronger opening sentence", "Clarify the character's goal"):
                      Provide these specific suggestions concisely. Output *only* the critique text.
                    ELSE IF the document is coherent, addresses the topic adequately for its length, and has no glaring errors or obvious omissions:
                      Respond *exactly* with the phrase "No major issues found." and nothing else. It doesn't need to be perfect, just functionally complete for this stage.
                    Avoid suggesting purely subjective stylistic preferences if the core is sound.
                    Do not add explanations. Output only the critique OR the exact completion phrase.
                    """)
                .outputKey(STATE_CRITICISM)
                .includeContents(NONE)
                .build();

        // STEP 2b: Refiner/Exiter Agent (Inside the Refinement Loop)
        LlmAgent refinerAgentInLoop =
            LlmAgent.builder()
                .model(MODEL_NAME)
                .name("RefinerAgent")
                .description(
                    "Refines the document based on critique, or calls exitLoop if critique indicates"
                        + " completion.")
                .instruction(
                    """
                    You are a Creative Writing Assistant refining a document based on feedback OR exiting the process.

                    **Current Document:**
                    ```
                    {{current_document}}
                    ```

                    **Critique/Suggestions:**
                    {{criticism}}

                    **Task:**
                    Analyze the 'Critique/Suggestions'.
                    IF the critique is *exactly* "No major issues found.":
                      You MUST call the 'exitLoop' function. Do not output any text.
                    ELSE (the critique contains actionable feedback):
                      Carefully apply the suggestions to improve the 'Current Document'.
                      Output *only* the refined document text. Do not add explanations.

                    Either output the refined document OR call the exitLoop function.
                    """)
                .outputKey(STATE_CURRENT_DOC)
                .includeContents(NONE)
                .tools(FunctionTool.create(LoopAgentExample.class, "exitLoop"))
                .build();

        // STEP 2: Refinement Loop Agent
        LoopAgent refinementLoop =
            LoopAgent.builder()
                .name("RefinementLoop")
                .description("Repeatedly refines the document with critique and then exits.")
                .subAgents(criticAgentInLoop, refinerAgentInLoop)
                .maxIterations(5)
                .build();

        // STEP 3: Overall Sequential Pipeline
        SequentialAgent iterativeWriterAgent =
            SequentialAgent.builder()
                .name(APP_NAME)
                .description(
                    "Writes an initial document and then iteratively refines it with critique using an"
                        + " exit tool.")
                .subAgents(initialWriterAgent, refinementLoop)
                .build();

        // Create an InMemoryRunner
        InMemoryRunner runner = new InMemoryRunner(iterativeWriterAgent, APP_NAME);
        // InMemoryRunner automatically creates a session service. Create a session using the service
        Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
        // Set initial topic in state
        session.state().put(STATE_INITIAL_TOPIC, prompt);


        Content userMessage = Content.fromParts(Part.fromText(prompt));

        // Run the agent
        Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);

        // Stream event response
        eventStream.blockingForEach(
            event -> {
              if (event.finalResponse()) {
                System.out.println(event.stringifyContent());
              }
            });
    }
}
```

### Custom agents
Custom agents provide the ultimate flexibility in ADK, allowing you to define arbitrary orchestration logic by inheriting directly from `BaseAgent` and implementing your own control flow. This goes beyond the predefined patterns of `SequentialAgent`, `LoopAgent`, and `ParallelAgent`, enabling you to build highly specific and complex agentic workflows.

> **Advanced Concept**
> Building custom agents by directly implementing `_run_async_impl` (or its equivalent in other languages) provides powerful control but is more complex than using the predefined `LlmAgent` or standard `WorkflowAgent` types. We recommend understanding those foundational agent types first before tackling custom orchestration logic.

#### Introduction: Beyond Predefined Workflows
**What is a Custom Agent?**
A Custom Agent is essentially any class you create that inherits from `google.adk.agents.BaseAgent` (Python) or `com.google.adk.agents.BaseAgent` (Java) and implements its core execution logic within the `_run_async_impl` asynchronous method (Python) or `runAsyncImpl` method (Java). You have complete control over how this method calls other agents (sub-agents), manages state, and handles events.

**Note**: The specific method name for implementing an agent's core asynchronous logic may vary slightly by SDK language (e.g., `runAsyncImpl` in Java, `_run_async_impl` in Python). Refer to the language-specific API documentation for details.

**Why Use Them?**
While the standard Workflow Agents (`SequentialAgent`, `LoopAgent`, `ParallelAgent`) cover common orchestration patterns, you'll need a Custom agent when your requirements include:
*   **Conditional Logic**: Executing different sub-agents or taking different paths based on runtime conditions or the results of previous steps.
*   **Complex State Management**: Implementing intricate logic for maintaining and updating state throughout the workflow beyond simple sequential passing.
*   **External Integrations**: Incorporating calls to external APIs, databases, or custom libraries directly within the orchestration flow control.
*   **Dynamic Agent Selection**: Choosing which sub-agent(s) to run next based on dynamic evaluation of the situation or input.
*   **Unique Workflow Patterns**: Implementing orchestration logic that doesn't fit the standard sequential, parallel, or loop structures.

#### Implementing Custom Logic:
The core of any custom agent is the method where you define its unique asynchronous behavior. This method allows you to orchestrate sub-agents and manage the flow of execution.

**Python (`_run_async_impl`)**
The heart of any custom agent is the `_run_async_impl` method. This is where you define its unique behavior.
*   **Signature**: `async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:`
*   **Asynchronous Generator**: It must be an `async def` function and return an `AsyncGenerator`. This allows it to `yield` events produced by sub-agents or its own logic back to the runner.
*   **`ctx` (`InvocationContext`)**: Provides access to crucial runtime information, most importantly `ctx.session.state`, which is the primary way to share data between steps orchestrated by your custom agent.

Key Capabilities within `_run_async_impl`:
*   **Calling Sub-Agents**: You invoke sub-agents (which are typically stored as instance attributes like `self.my_llm_agent`) using their `run_async` method and `yield` their events:
    ```python
    async for event in self.some_sub_agent.run_async(ctx):
        # Optionally inspect or log the event
        yield event  # Pass the event up
    ```
*   **Managing State**: Read from and write to the session state dictionary (`ctx.session.state`) to pass data between sub-agent calls or make decisions:
    ```python
    # Read data set by a previous agent
    previous_result = ctx.session.state.get("some_key")

    # Make a decision based on state
    if previous_result == "some_value":
        # ... call a specific sub-agent ...
        pass
    else:
        # ... call another sub-agent ...
        pass

    # Store a result for a later step (often done via a sub-agent's output_key)
    # ctx.session.state["my_custom_result"] = "calculated_value"
    ```
*   **Implementing Control Flow**: Use standard Python constructs (`if`/`elif`/`else`, `for`/`while` loops, `try`/`except`) to create sophisticated, conditional, or iterative workflows involving your sub-agents.

**Java (`runAsyncImpl`)**
The heart of any custom agent is the `runAsyncImpl` method, which you override from `BaseAgent`.
*   **Signature**: `protected Flowable<Event> runAsyncImpl(InvocationContext ctx)`
*   **Reactive Stream (`Flowable`)**: It must return an `io.reactivex.rxjava3.core.Flowable<Event>`. This `Flowable` represents a stream of events that will be produced by the custom agent's logic, often by combining or transforming multiple `Flowable`s from sub-agents.
*   **`ctx` (`InvocationContext`)**: Provides access to crucial runtime information, most importantly `ctx.session().state()`, which is a `java.util.concurrent.ConcurrentMap<String, Object>`. This is the primary way to share data between steps orchestrated by your custom agent.

Key Capabilities within `runAsyncImpl`:
*   **Calling Sub-Agents**: You invoke sub-agents (which are typically stored as instance attributes or objects) using their asynchronous run method and return their event streams:
    You typically chain `Flowable`s from sub-agents using RxJava operators like `concatWith`, `flatMapPublisher`, or `concatArray`.
    ```java
    // Example: Running one sub-agent
    // return someSubAgent.runAsync(ctx);

    // Example: Running sub-agents sequentially
    Flowable<Event> firstAgentEvents = someSubAgent1.runAsync(ctx)
        .doOnNext(event -> System.out.println("Event from agent 1: " + event.id()));

    Flowable<Event> secondAgentEvents = Flowable.defer(() ->
        someSubAgent2.runAsync(ctx)
            .doOnNext(event -> System.out.println("Event from agent 2: " + event.id()))
    );
    return firstAgentEvents.concatWith(secondAgentEvents);
    ```
    The `Flowable.defer()` is often used for subsequent stages if their execution depends on the completion or state after prior stages.
*   **Managing State**: Read from and write to the session state to pass data between sub-agent calls or make decisions. The session state is a `java.util.concurrent.ConcurrentMap<String, Object>` obtained via `ctx.session().state()`.
    ```java
    // Read data set by a previous agent
    Object previousResult = ctx.session().state().get("some_key");

    // Make a decision based on state
    if ("some_value".equals(previousResult)) {
        // ... logic to include a specific sub-agent's Flowable ...
    } else {
        // ... logic to include another sub-agent's Flowable ...
    }

    // Store a result for a later step (often done via a sub-agent's output_key)
    // ctx.session().state().put("my_custom_result", "calculated_value");
    ```
*   **Implementing Control Flow**: Use standard language constructs (`if`/`else`, loops, `try`/`catch`) combined with reactive operators (RxJava) to create sophisticated workflows.
    *   **Conditional**: `Flowable.defer()` to choose which `Flowable` to subscribe to based on a condition, or `filter()` if you're filtering events within a stream.
    *   **Iterative**: Operators like `repeat()`, `retry()`, or by structuring your `Flowable` chain to recursively call parts of itself based on conditions (often managed with `flatMapPublisher` or `concatMap`).

#### Managing Sub-Agents and State
Typically, a custom agent orchestrates other agents (like `LlmAgent`, `LoopAgent`, etc.).
*   **Initialization**: You usually pass instances of these sub-agents into your custom agent's constructor and store them as instance fields/attributes (e.g., `this.story_generator = story_generator_instance` or `self.story_generator = story_generator_instance`). This makes them accessible within the custom agent's core asynchronous execution logic (such as: `_run_async_impl` method).
*   **Sub Agents List**: When initializing the `BaseAgent` using it's `super()` constructor, you should pass a `sub agents` list. This list tells the ADK framework about the agents that are part of this custom agent's immediate hierarchy. It's important for framework features like lifecycle management, introspection, and potentially future routing capabilities, even if your core execution logic (`_run_async_impl`) calls the agents directly via `self.xxx_agent`. Include the agents that your custom logic directly invokes at the top level.
*   **State**: As mentioned, `ctx.session.state` is the standard way sub-agents (especially `LlmAgent`s using `output_key`) communicate results back to the orchestrator and how the orchestrator passes necessary inputs down.

#### Design Pattern Example: `StoryFlowAgent`
Let's illustrate the power of custom agents with an example pattern: a multi-stage content generation workflow with conditional logic.
**Goal**: Create a system that generates a story, iteratively refines it through critique and revision, performs final checks, and crucially, *regenerates the story if the final tone check fails*.
**Why Custom?** The core requirement driving the need for a custom agent here is the *conditional regeneration based on the tone check*. Standard workflow agents don't have built-in conditional branching based on the outcome of a sub-agent's task. We need custom logic (`if tone == "negative": ...`) within the orchestrator.

##### Part 1: Simplified custom agent Initialization
**Python:**
We define the `StoryFlowAgent` inheriting from `BaseAgent`. In `__init__`, we store the necessary sub-agents (passed in) as instance attributes and tell the `BaseAgent` framework about the top-level agents this custom agent will directly orchestrate.
```python
from google.adk.agents import LlmAgent, BaseAgent, LoopAgent, SequentialAgent
from pydantic import Field # For model_config if needed

class StoryFlowAgent(BaseAgent):
    """
    Custom agent for a story generation and refinement workflow.
    This agent orchestrates a sequence of LLM agents to generate a story,
    critique it, revise it, check grammar and tone, and potentially
    regenerate the story if the tone is negative.
    """
    # --- Field Declarations for Pydantic ---
    # Declare the agents passed during initialization as class attributes with type hints
    story_generator: LlmAgent
    critic: LlmAgent
    reviser: LlmAgent
    grammar_check: LlmAgent
    tone_check: LlmAgent
    loop_agent: LoopAgent
    sequential_agent: SequentialAgent

    # model_config allows setting Pydantic configurations if needed, e.g., arbitrary_types_allowed
    model_config = {
        "arbitrary_types_allowed": True
    }

    def __init__(
        self,
        name: str,
        story_generator: LlmAgent,
        critic: LlmAgent,
        reviser: LlmAgent,
        grammar_check: LlmAgent,
        tone_check: LlmAgent,
    ):
        """Initializes the StoryFlowAgent.
        Args:
            name: The name of the agent.
            story_generator: An LlmAgent to generate the initial story.
            critic: An LlmAgent to critique the story.
            reviser: An LlmAgent to revise the story based on criticism.
            grammar_check: An LlmAgent to check the grammar.
            tone_check: An LlmAgent to analyze the tone.
        """
        # Create internal agents *before* calling super().__init__
        loop_agent = LoopAgent(
            name="CriticReviserLoop",
            sub_agents=[critic, reviser],
            max_iterations=2
        )
        sequential_agent = SequentialAgent(
            name="PostProcessing",
            sub_agents=[grammar_check, tone_check]
        )

        # Define the sub_agents list for the framework
        sub_agents_list = [
            story_generator,
            loop_agent,
            sequential_agent,
        ]

        # Pydantic will validate and assign them based on the class annotations.
        super().__init__(
            name=name,
            story_generator=story_generator,
            critic=critic,
            reviser=reviser,
            grammar_check=grammar_check,
            tone_check=tone_check,
            loop_agent=loop_agent,
            sequential_agent=sequential_agent,
            sub_agents=sub_agents_list,  # Pass the sub_agents list directly
        )
```

**Java:**
We define the `StoryFlowAgentExample` by extending `BaseAgent`. In its `constructor`, we store the necessary sub-agent instances (passed as parameters) as instance fields. These top-level sub-agents, which this custom agent will directly orchestrate, are also passed to the `super` constructor of `BaseAgent` as a list.
```java
import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.LoopAgent;
import com.google.adk.agents.SequentialAgent;
import java.util.List;
// ... other imports

public class StoryFlowAgentExample extends BaseAgent {
    private final LlmAgent storyGenerator;
    private final LoopAgent loopAgent;
    private final SequentialAgent sequentialAgent;

    public StoryFlowAgentExample(
        String name,
        LlmAgent storyGenerator,
        LoopAgent loopAgent,
        SequentialAgent sequentialAgent
    ) {
        super(
            name,
            "Orchestrates story generation, critique, revision, and checks.",
            List.of(storyGenerator, loopAgent, sequentialAgent), // sub_agents list
            null, // callbacks
            null  // flow
        );
        this.storyGenerator = storyGenerator;
        this.loopAgent = loopAgent;
        this.sequentialAgent = sequentialAgent;
    }
    // ... runAsyncImpl and other methods
}
```

##### Part 2: Defining the Custom Execution Logic
**Python (`_run_async_impl`):**
This method orchestrates the sub-agents using standard Python `async/await` and control flow.
```python
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator
import logging # Assuming logger is configured
from typing_extensions import override

logger = logging.getLogger(__name__)

class StoryFlowAgent(BaseAgent): # Continued from above
    # ... (previous __init__ and field declarations) ...
    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Implements the custom orchestration logic for the story workflow.
        Uses the instance attributes assigned by Pydantic (e.g., self.story_generator).
        """
        logger.info(f"[{self.name}] Starting story generation workflow.")

        # 1. Initial Story Generation
        logger.info(f"[{self.name}] Running StoryGenerator...")
        async for event in self.story_generator.run_async(ctx):
            logger.info(f"[{self.name}] Event from StoryGenerator: {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event

        # Check if story was generated before proceeding
        if "current_story" not in ctx.session.state or not ctx.session.state["current_story"]:
            logger.error(f"[{self.name}] Failed to generate initial story. Aborting workflow.")
            return  # Stop processing if initial story failed
        logger.info(f"[{self.name}] Story state after generator: {ctx.session.state.get('current_story')}")

        # 2. Critic-Reviser Loop
        logger.info(f"[{self.name}] Running CriticReviserLoop...")
        # Use the loop_agent instance attribute assigned during init
        async for event in self.loop_agent.run_async(ctx):
            logger.info(f"[{self.name}] Event from CriticReviserLoop: {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        logger.info(f"[{self.name}] Story state after loop: {ctx.session.state.get('current_story')}")

        # 3. Sequential Post-Processing (Grammar and Tone Check)
        logger.info(f"[{self.name}] Running PostProcessing...")
        # Use the sequential_agent instance attribute assigned during init
        async for event in self.sequential_agent.run_async(ctx):
            logger.info(f"[{self.name}] Event from PostProcessing: {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event

        # 4. Tone-Based Conditional Logic
        tone_check_result = ctx.session.state.get("tone_check_result")
        logger.info(f"[{self.name}] Tone check result: {tone_check_result}")

        if tone_check_result == "negative":
            logger.info(f"[{self.name}] Tone is negative. Regenerating story...")
            async for event in self.story_generator.run_async(ctx): # Call story_generator again
                logger.info(f"[{self.name}] Event from StoryGenerator (Regen): {event.model_dump_json(indent=2, exclude_none=True)}")
                yield event
        else:
            logger.info(f"[{self.name}] Tone is not negative. Keeping current story.")
            pass # Or any other logic

        logger.info(f"[{self.name}] Workflow finished.")
```
Explanation of Logic:
1.  The initial `story_generator` runs. Its output is expected to be in `ctx.session.state["current_story"]`.
2.  The `loop_agent` runs, which internally calls the `critic` and `reviser` sequentially for `max_iterations` times. They read/write `current_story` and `criticism` from/to the state.
3.  The `sequential_agent` runs, calling `grammar_check` then `tone_check`, reading `current_story` and writing `grammar_suggestions` and `tone_check_result` to the state.
4.  **Custom Part**: The `if` statement checks the `tone_check_result` from the state. If it's `"negative"`, the `story_generator` is called *again*, overwriting the `current_story` in the state. Otherwise, the flow ends.

**Java (`runAsyncImpl`):**
The `runAsyncImpl` method orchestrates the sub-agents using RxJava's `Flowable` streams and operators for asynchronous control flow.
```java
import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.InvocationContext;
import com.google.adk.events.Event;
import io.reactivex.rxjava3.core.Flowable;
import java.util.logging.Level;
import java.util.logging.Logger;
// ... other imports from StoryFlowAgentExample

public class StoryFlowAgentExample extends BaseAgent { // Continued from above
    private static final Logger logger = Logger.getLogger(StoryFlowAgentExample.class.getName());
    // ... (constructor and fields from Part 1) ...

    private boolean isStoryGenerated(InvocationContext ctx) { // Helper
        Object currentStoryObj = ctx.session().state().get("current_story");
        return currentStoryObj != null && !String.valueOf(currentStoryObj).isEmpty();
    }

    @Override
    protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) {
        logger.log(Level.INFO, () -> String.format("[%s] Starting story generation workflow.", name()));

        // Stage 1. Initial Story Generation
        Flowable<Event> storyGenFlow = runStage(storyGenerator, invocationContext, "StoryGenerator");

        // Stage 2: Critic-Reviser Loop (runs after story generation completes)
        Flowable<Event> criticReviserFlow = Flowable.defer(() -> {
            if (!isStoryGenerated(invocationContext)) {
                logger.log(Level.SEVERE, () -> String.format("[%s] Failed to generate initial story. Aborting after StoryGenerator.", name()));
                return Flowable.empty(); // Stop further processing if no story
            }
            logger.log(Level.INFO, () -> String.format("[%s] Story state after generator: %s", name(), invocationContext.session().state().get("current_story")));
            return runStage(loopAgent, invocationContext, "CriticReviserLoop");
        });

        // Stage 3: Post-Processing (runs after critic-reviser loop completes)
        Flowable<Event> postProcessingFlow = Flowable.defer(() -> {
            logger.log(Level.INFO, () -> String.format("[%s] Story state after loop: %s", name(), invocationContext.session().state().get("current_story")));
            return runStage(sequentialAgent, invocationContext, "PostProcessing");
        });

        // Stage 4: Conditional Regeneration (runs after post-processing completes)
        Flowable<Event> conditionalRegenFlow = Flowable.defer(() -> {
            String toneCheckResult = (String) invocationContext.session().state().get("tone_check_result");
            logger.log(Level.INFO, () -> String.format("[%s] Tone check result: %s", name(), toneCheckResult));

            if ("negative".equalsIgnoreCase(toneCheckResult)) {
                logger.log(Level.INFO, () -> String.format("[%s] Tone is negative. Regenerating story...", name()));
                return runStage(storyGenerator, invocationContext, "StoryGenerator (Regen)");
            } else {
                logger.log(Level.INFO, () -> String.format("[%s] Tone is not negative. Keeping current story.", name()));
                return Flowable.empty(); // No regeneration needed
            }
        });

        return Flowable.concatArray(storyGenFlow, criticReviserFlow, postProcessingFlow, conditionalRegenFlow)
            .doOnComplete(() -> logger.log(Level.INFO, () -> String.format("[%s] Workflow finished.", name())));
    }

    // Helper method for a single agent run stage with logging
    private Flowable<Event> runStage(BaseAgent agentToRun, InvocationContext ctx, String stageName) {
        logger.log(Level.INFO, () -> String.format("[%s] Running %s...", name(), stageName));
        return agentToRun.runAsync(ctx)
            .doOnNext(event -> logger.log(Level.INFO, () -> String.format("[%s] Event from %s: %s", name(), stageName, event.toJson())))
            .doOnError(err -> logger.log(Level.SEVERE, String.format("[%s] Error in %s", name(), stageName), err))
            .doOnComplete(() -> logger.log(Level.INFO, () -> String.format("[%s] %s finished.", name(), stageName)));
    }
     @Override
    protected Flowable<Event> runLiveImpl(InvocationContext invocationContext) {
        // For simplicity, this example does not implement runLive
        return Flowable.error(new UnsupportedOperationException("runLive not implemented."));
    }
}
```
Explanation of Logic:
1.  The initial `storyGenerator.runAsync(invocationContext)` `Flowable` is executed. Its output is expected to be in `invocationContext.session().state().get("current_story")`.
2.  The `loopAgent`'s `Flowable` runs next (due to `Flowable.concatArray` and `Flowable.defer`). The `LoopAgent` internally calls the `critic` and `reviser` sub-agents sequentially for up to `maxIterations`. They read/write `current_story` and `criticism` from/to the state.
3.  Then, the `sequentialAgent`'s `Flowable` executes. It calls the `grammar_check` then `tone_check`, reading `current_story` and writing `grammar_suggestions` and `tone_check_result` to the state.
4.  **Custom Part**: After the `sequentialAgent` completes, logic within a `Flowable.defer` checks the `"tone_check_result"` from `invocationContext.session().state()`. If it's `"negative"`, the `storyGenerator` `Flowable` is conditionally concatenated and executed again, overwriting `"current_story"`. Otherwise, an empty `Flowable` is used, and the overall workflow proceeds to completion.

##### Part 3: Defining the LLM Sub-Agents
These are standard `LlmAgent` definitions, responsible for specific tasks. Their `output_key` parameter is crucial for placing results into the `session.state` where other agents or the custom orchestrator can access them.

**Python:**
```python
# Define model constant
GEMINI_2_FLASH = "gemini-2.0-flash"

# --- Define the individual LLM agents ---
story_generator = LlmAgent(
    name="StoryGenerator",
    model=GEMINI_2_FLASH,
    instruction="""You are a story writer. Write a short story (around 100 words) about a cat,
based on the topic provided in session state with key 'topic'""",
    input_schema=None,
    output_key="current_story",  # Key for storing output in session state
)

critic = LlmAgent(
    name="Critic",
    model=GEMINI_2_FLASH,
    instruction="""You are a story critic. Review the story provided in session state with key 'current_story'.
Provide 1-2 sentences of constructive criticism on how to improve it. Focus on plot or character.""",
    input_schema=None,
    output_key="criticism",  # Key for storing criticism in session state
)

reviser = LlmAgent(
    name="Reviser",
    model=GEMINI_2_FLASH,
    instruction="""You are a story reviser. Revise the story provided in session state with key 'current_story',
based on the criticism in session state with key 'criticism'. Output only the revised story.""",
    input_schema=None,
    output_key="current_story",  # Overwrites the original story
)

grammar_check = LlmAgent(
    name="GrammarCheck",
    model=GEMINI_2_FLASH,
    instruction="""You are a grammar checker. Check the grammar of the story provided in session state with key 'current_story'.
Output only the suggested corrections as a list, or output 'Grammar is good!' if there are no errors.""",
    input_schema=None,
    output_key="grammar_suggestions",
)

tone_check = LlmAgent(
    name="ToneCheck",
    model=GEMINI_2_FLASH,
    instruction="""You are a tone analyzer. Analyze the tone of the story provided in session state with key 'current_story'.
Output only one word: 'positive' if the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral' otherwise.""",
    input_schema=None,
    output_key="tone_check_result",  # This agent's output determines the conditional flow
)
```

**Java:**
```java
// Assuming MODEL_NAME is defined, e.g., "gemini-2.0-flash"
String MODEL_NAME = "gemini-2.0-flash";

// --- Define the individual LLM agents ---
LlmAgent storyGenerator = LlmAgent.builder()
    .name("StoryGenerator")
    .model(MODEL_NAME)
    .description("Generates the initial story.")
    .instruction("""
    You are a story writer. Write a short story (around 100 words) about a cat,
    based on the topic provided in session state with key 'topic'
    """)
    .inputSchema(null)
    .outputKey("current_story") // Key for storing output in session state
    .build();

LlmAgent critic = LlmAgent.builder()
    .name("Critic")
    .model(MODEL_NAME)
    .description("Critiques the story.")
    .instruction("""
    You are a story critic. Review the story provided in session state with key 'current_story'.
    Provide 1-2 sentences of constructive criticism on how to improve it. Focus on plot or character.
    """)
    .inputSchema(null)
    .outputKey("criticism") // Key for storing criticism in session state
    .build();

LlmAgent reviser = LlmAgent.builder()
    .name("Reviser")
    .model(MODEL_NAME)
    .description("Revises the story based on criticism.")
    .instruction("""
    You are a story reviser. Revise the story provided in session state with key 'current_story',
    based on the criticism in session state with key 'criticism'. Output only the revised story.
    """)
    .inputSchema(null)
    .outputKey("current_story") // Overwrites the original story
    .build();

LlmAgent grammarCheck = LlmAgent.builder()
    .name("GrammarCheck")
    .model(MODEL_NAME)
    .description("Checks grammar and suggests corrections.")
    .instruction("""
    You are a grammar checker. Check the grammar of the story provided in session state with key 'current_story'.
    Output only the suggested corrections as a list, or output 'Grammar is good!' if there are no errors.
    """)
    .outputKey("grammar_suggestions")
    .build();

LlmAgent toneCheck = LlmAgent.builder()
    .name("ToneCheck")
    .model(MODEL_NAME)
    .description("Analyzes the tone of the story.")
    .instruction("""
    You are a tone analyzer. Analyze the tone of the story provided in session state with key 'current_story'.
    Output only one word: 'positive' if the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral' otherwise.
    """)
    .outputKey("tone_check_result") // This agent's output determines the conditional flow
    .build();

LoopAgent loopAgent = LoopAgent.builder()
    .name("CriticReviserLoop")
    .description("Iteratively critiques and revises the story.")
    .subAgents(critic, reviser)
    .maxIterations(2)
    .build();

SequentialAgent sequentialAgent = SequentialAgent.builder()
    .name("PostProcessing")
    .description("Performs grammar and tone checks sequentially.")
    .subAgents(grammarCheck, toneCheck)
    .build();
```

##### Part 4: Instantiating and Running the custom agent
Finally, you instantiate your `StoryFlowAgent` and use the `Runner` as usual.

**Python:**
```python
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types as genai_types # Renamed to avoid conflict
import json # For pretty printing state

# --- Constants for Runner ---
APP_NAME = "story_app"
USER_ID = "12345"
SESSION_ID = "123344"

# --- Create the custom agent instance ---
story_flow_agent = StoryFlowAgent(
    name="StoryFlowAgent",
    story_generator=story_generator, # from Part 3
    critic=critic,                   # from Part 3
    reviser=reviser,                 # from Part 3
    grammar_check=grammar_check,     # from Part 3
    tone_check=tone_check            # from Part 3
)

# --- Setup Runner and Session ---
session_service = InMemorySessionService()
initial_state = {"topic": "a brave kitten exploring a haunted house"}
session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state  # Pass initial state here
)
logger.info(f"Initial session state: {session.state}")

runner = Runner(
    agent=story_flow_agent,  # Pass the custom orchestrator agent
    app_name=APP_NAME,
    session_service=session_service
)

# --- Function to Interact with the Agent ---
def call_agent(user_input_topic: str):
    """Sends a new topic to the agent (overwriting the initial one if needed) and runs the workflow."""
    current_session = session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    if not current_session:
        logger.error("Session not found!")
        return

    current_session.state["topic"] = user_input_topic # Update topic
    logger.info(f"Updated session state topic to: {user_input_topic}")

    content = genai_types.Content(role='user', parts=[genai_types.Part(text=f"Generate a story about: {user_input_topic}")])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    final_response = "No final response captured."
    for event in events:
        if event.is_final_response() and event.content and event.content.parts:
            logger.info(f"Potential final response from [{event.author}]: {event.content.parts[0].text}")
            final_response = event.content.parts[0].text

    print("\n--- Agent Interaction Result ---")
    print("Agent Final Response: ", final_response)
    final_session = session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    print("Final Session State:")
    print(json.dumps(final_session.state, indent=2))
    print("-------------------------------\n")

# --- Run the Agent ---
# call_agent("a lonely robot finding a friend in a junkyard") # Call this from your main execution block
```

**Java:**
```java
import com.google.adk.runner.InMemoryRunner; // Assuming this class exists for Java ADK
import com.google.adk.sessions.Session;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional; // For optional session retrieval
import java.util.concurrent.ConcurrentHashMap; // For initial state
// ... other imports from StoryFlowAgentExample and sub-agent definitions

public class MainApp { // Or your main class
    private static final String APP_NAME = "story_app_java";
    private static final String USER_ID = "user_java_123";
    private static final String SESSION_ID = "session_java_456";

    public static void main(String[] args) {
        // Instantiate sub-agents (storyGenerator, critic, reviser, grammarCheck, toneCheck, loopAgent, sequentialAgent from Part 3)
        // ... (Assume these are instantiated as per Part 3)

        StoryFlowAgentExample storyFlowOrchestrator = new StoryFlowAgentExample(
            "StoryFlowAgentJava",
            storyGenerator, // from Part 3
            loopAgent,      // from Part 3
            sequentialAgent // from Part 3
        );

        runAgent(storyFlowOrchestrator, "a lonely robot finding a friend in a junkyard");
    }

    public static void runAgent(StoryFlowAgentExample agent, String userTopic) {
        InMemoryRunner runner = new InMemoryRunner(agent); // Assuming similar constructor
        Map<String, Object> initialState = new HashMap<>();
        initialState.put("topic", "a brave kitten exploring a haunted house"); // Initial topic

        Session session = runner.sessionService()
            .createSession(APP_NAME, USER_ID, new ConcurrentHashMap<>(initialState), SESSION_ID)
            .blockingGet();
        logger.log(Level.INFO, () -> String.format("Initial session state: %s", session.state()));

        session.state().put("topic", userTopic); // Update the state in the retrieved session
        logger.log(Level.INFO, () -> String.format("Updated session state topic to: %s", userTopic));

        Content userMessage = Content.fromParts(Part.fromText("Generate a story about: " + userTopic));
        Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);

        final String[] finalResponse = {"No final response captured."};
        eventStream.blockingForEach(event -> {
            if (event.finalResponse() && event.content().isPresent()) {
                String author = event.author() != null ? event.author() : "UNKNOWN_AUTHOR";
                Optional<String> textOpt = event.content()
                    .flatMap(Content::parts)
                    .filter(parts -> !parts.isEmpty())
                    .map(parts -> parts.get(0).text().orElse(""));
                logger.log(Level.INFO, () -> String.format("Potential final response from [%s]: %s", author, textOpt.orElse("N/A")));
                textOpt.ifPresent(text -> finalResponse[0] = text);
            }
        });

        System.out.println("\n--- Agent Interaction Result ---");
        System.out.println("Agent Final Response: " + finalResponse[0]);

        Session finalSession = runner.sessionService()
            .getSession(APP_NAME, USER_ID, SESSION_ID, Optional.empty())
            .blockingGet();
        assert finalSession != null;
        System.out.println("Final Session State:" + finalSession.state());
        System.out.println("-------------------------------\n");
    }
}
```

##### Full Code Example
(Note: The full runnable code, including imports and execution logic, can be found linked below in the original document.)

**Python:**
```python
# Full runnable code for the StoryFlowAgent example
import logging
from typing import AsyncGenerator
from typing_extensions import override # For older Python versions, ensure this is installed or use typing.override for Python 3.12+

from google.adk.agents import LlmAgent, BaseAgent, LoopAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
from google.genai import types as genai_types # Renamed to avoid conflict with 'types' module
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.events import Event
from pydantic import Field # For model_config if needed
import json # For pretty printing state

# --- Constants ---
APP_NAME = "story_app"
USER_ID = "12345"
SESSION_ID = "123344"
GEMINI_2_FLASH = "gemini-2.0-flash"

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --- Custom Orchestrator Agent ---
class StoryFlowAgent(BaseAgent):
    """
    Custom agent for a story generation and refinement workflow.
    This agent orchestrates a sequence of LLM agents to generate a story,
    critique it, revise it, check grammar and tone, and potentially
    regenerate the story if the tone is negative.
    """
    # --- Field Declarations for Pydantic ---
    story_generator: LlmAgent
    critic: LlmAgent
    reviser: LlmAgent
    grammar_check: LlmAgent
    tone_check: LlmAgent
    loop_agent: LoopAgent
    sequential_agent: SequentialAgent

    model_config = {
        "arbitrary_types_allowed": True
    }

    def __init__(
        self,
        name: str,
        story_generator: LlmAgent,
        critic: LlmAgent,
        reviser: LlmAgent,
        grammar_check: LlmAgent,
        tone_check: LlmAgent,
    ):
        loop_agent = LoopAgent(
            name="CriticReviserLoop", sub_agents=[critic, reviser], max_iterations=2
        )
        sequential_agent = SequentialAgent(
            name="PostProcessing", sub_agents=[grammar_check, tone_check]
        )
        sub_agents_list = [
            story_generator,
            loop_agent,
            sequential_agent,
        ]
        super().__init__(
            name=name,
            story_generator=story_generator,
            critic=critic,
            reviser=reviser,
            grammar_check=grammar_check,
            tone_check=tone_check,
            loop_agent=loop_agent,
            sequential_agent=sequential_agent,
            sub_agents=sub_agents_list,
        )

    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        logger.info(f"[{self.name}] Starting story generation workflow.")
        logger.info(f"[{self.name}] Running StoryGenerator...")
        async for event in self.story_generator.run_async(ctx):
            logger.info(f"[{self.name}] Event from StoryGenerator: {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event

        if "current_story" not in ctx.session.state or not ctx.session.state["current_story"]:
            logger.error(f"[{self.name}] Failed to generate initial story. Aborting workflow.")
            return
        logger.info(f"[{self.name}] Story state after generator: {ctx.session.state.get('current_story')}")

        logger.info(f"[{self.name}] Running CriticReviserLoop...")
        async for event in self.loop_agent.run_async(ctx):
            logger.info(f"[{self.name}] Event from CriticReviserLoop: {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event
        logger.info(f"[{self.name}] Story state after loop: {ctx.session.state.get('current_story')}")

        logger.info(f"[{self.name}] Running PostProcessing...")
        async for event in self.sequential_agent.run_async(ctx):
            logger.info(f"[{self.name}] Event from PostProcessing: {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event

        tone_check_result = ctx.session.state.get("tone_check_result")
        logger.info(f"[{self.name}] Tone check result: {tone_check_result}")
        if tone_check_result == "negative":
            logger.info(f"[{self.name}] Tone is negative. Regenerating story...")
            async for event in self.story_generator.run_async(ctx):
                logger.info(f"[{self.name}] Event from StoryGenerator (Regen): {event.model_dump_json(indent=2, exclude_none=True)}")
                yield event
        else:
            logger.info(f"[{self.name}] Tone is not negative. Keeping current story.")
        logger.info(f"[{self.name}] Workflow finished.")

# --- Define the individual LLM agents ---
story_generator = LlmAgent(
    name="StoryGenerator", model=GEMINI_2_FLASH,
    instruction="""You are a story writer. Write a short story (around 100 words) about a cat,
based on the topic provided in session state with key 'topic'""",
    input_schema=None, output_key="current_story",
)
critic = LlmAgent(
    name="Critic", model=GEMINI_2_FLASH,
    instruction="""You are a story critic. Review the story provided in session state with key 'current_story'.
Provide 1-2 sentences of constructive criticism on how to improve it. Focus on plot or character.""",
    input_schema=None, output_key="criticism",
)
reviser = LlmAgent(
    name="Reviser", model=GEMINI_2_FLASH,
    instruction="""You are a story reviser. Revise the story provided in session state with key 'current_story',
based on the criticism in session state with key 'criticism'. Output only the revised story.""",
    input_schema=None, output_key="current_story",
)
grammar_check = LlmAgent(
    name="GrammarCheck", model=GEMINI_2_FLASH,
    instruction="""You are a grammar checker. Check the grammar of the story provided in session state with key 'current_story'.
Output only the suggested corrections as a list, or output 'Grammar is good!' if there are no errors.""",
    input_schema=None, output_key="grammar_suggestions",
)
tone_check = LlmAgent(
    name="ToneCheck", model=GEMINI_2_FLASH,
    instruction="""You are a tone analyzer. Analyze the tone of the story provided in session state with key 'current_story'.
Output only one word: 'positive' if the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral' otherwise.""",
    input_schema=None, output_key="tone_check_result",
)

# --- Create the custom agent instance ---
story_flow_agent = StoryFlowAgent(
    name="StoryFlowAgent",
    story_generator=story_generator,
    critic=critic,
    reviser=reviser,
    grammar_check=grammar_check,
    tone_check=tone_check,
)

# --- Setup Runner and Session ---
session_service = InMemorySessionService()
initial_state = {"topic": "a brave kitten exploring a haunted house"}
session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state
)
logger.info(f"Initial session state: {session.state}")

runner = Runner(
    agent=story_flow_agent,
    app_name=APP_NAME,
    session_service=session_service
)

# --- Function to Interact with the Agent ---
def call_agent(user_input_topic: str):
    current_session = session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    if not current_session:
        logger.error("Session not found!")
        return
    current_session.state["topic"] = user_input_topic
    logger.info(f"Updated session state topic to: {user_input_topic}")
    content = genai_types.Content(role='user', parts=[genai_types.Part(text=f"Generate a story about: {user_input_topic}")])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    final_response = "No final response captured."
    for event in events:
        if event.is_final_response() and event.content and event.content.parts:
            logger.info(f"Potential final response from [{event.author}]: {event.content.parts[0].text}")
            final_response = event.content.parts[0].text
    print("\n--- Agent Interaction Result ---")
    print("Agent Final Response: ", final_response)
    final_session = session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    print("Final Session State:")
    print(json.dumps(final_session.state, indent=2))
    print("-------------------------------\n")

# --- Run the Agent ---
# To run this, you would call:
# import asyncio
# asyncio.run(call_agent("a lonely robot finding a friend in a junkyard"))
# Or if call_agent is not async, just:
# call_agent("a lonely robot finding a friend in a junkyard")
# For this example, we'll assume call_agent is called from a synchronous context.
# If runner.run is async, call_agent needs to be async too.
# Assuming runner.run is synchronous for this example to match the original structure.
if __name__ == "__main__":
     call_agent("a lonely robot finding a friend in a junkyard")

```

**Java:**
```java
// Full runnable code for the StoryFlowAgent example
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.InvocationContext;
import com.google.adk.agents.LoopAgent;
import com.google.adk.agents.SequentialAgent;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.logging.Level;
import java.util.logging.Logger;


public class StoryFlowAgentExample extends BaseAgent {
    // --- Constants ---
    private static final String APP_NAME = "story_app";
    private static final String USER_ID = "user_12345";
    private static final String SESSION_ID = "session_123344";
    private static final String MODEL_NAME = "gemini-2.0-flash"; // Ensure this model is available
    private static final Logger logger = Logger.getLogger(StoryFlowAgentExample.class.getName());

    private final LlmAgent storyGenerator;
    private final LoopAgent loopAgent;
    private final SequentialAgent sequentialAgent;

    public StoryFlowAgentExample(
        String name,
        LlmAgent storyGenerator,
        LoopAgent loopAgent,
        SequentialAgent sequentialAgent
    ) {
        super(
            name,
            "Orchestrates story generation, critique, revision, and checks.",
            List.of(storyGenerator, loopAgent, sequentialAgent),
            null,
            null
        );
        this.storyGenerator = storyGenerator;
        this.loopAgent = loopAgent;
        this.sequentialAgent = sequentialAgent;
    }

    public static void main(String[] args) {
        // --- Define the individual LLM agents ---
        LlmAgent storyGenerator = LlmAgent.builder()
            .name("StoryGenerator")
            .model(MODEL_NAME)
            .description("Generates the initial story.")
            .instruction("""
            You are a story writer. Write a short story (around 100 words) about a cat,
            based on the topic provided in session state with key 'topic'
            """)
            .inputSchema(null)
            .outputKey("current_story")
            .build();

        LlmAgent critic = LlmAgent.builder()
            .name("Critic")
            .model(MODEL_NAME)
            .description("Critiques the story.")
            .instruction("""
            You are a story critic. Review the story provided in session state with key 'current_story'.
            Provide 1-2 sentences of constructive criticism on how to improve it. Focus on plot or character.
            """)
            .inputSchema(null)
            .outputKey("criticism")
            .build();

        LlmAgent reviser = LlmAgent.builder()
            .name("Reviser")
            .model(MODEL_NAME)
            .description("Revises the story based on criticism.")
            .instruction("""
            You are a story reviser. Revise the story provided in session state with key 'current_story',
            based on the criticism in session state with key 'criticism'. Output only the revised story.
            """)
            .inputSchema(null)
            .output
            ```markdown
            .outputKey("current_story")
            .build();

        LlmAgent grammarCheck = LlmAgent.builder()
            .name("GrammarCheck")
            .model(MODEL_NAME)
            .description("Checks grammar and suggests corrections.")
            .instruction("""
            You are a grammar checker. Check the grammar of the story provided in session state with key 'current_story'.
            Output only the suggested corrections as a list, or output 'Grammar is good!' if there are no errors.
            """)
            .outputKey("grammar_suggestions")
            .build();

        LlmAgent toneCheck = LlmAgent.builder()
            .name("ToneCheck")
            .model(MODEL_NAME)
            .description("Analyzes the tone of the story.")
            .instruction("""
            You are a tone analyzer. Analyze the tone of the story provided in session state with key 'current_story'.
            Output only one word: 'positive' if the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral' otherwise.
            """)
            .outputKey("tone_check_result")
            .build();

        LoopAgent loopAgent = LoopAgent.builder()
            .name("CriticReviserLoop")
            .description("Iteratively critiques and revises the story.")
            .subAgents(critic, reviser)
            .maxIterations(2)
            .build();

        SequentialAgent sequentialAgent = SequentialAgent.builder()
            .name("PostProcessing")
            .description("Performs grammar and tone checks sequentially.")
            .subAgents(grammarCheck, toneCheck)
            .build();

        StoryFlowAgentExample storyFlowAgentExample = new StoryFlowAgentExample(
            APP_NAME, // Using APP_NAME as the custom agent's name
            storyGenerator,
            loopAgent,
            sequentialAgent
        );

        // --- Run the Agent ---
        runAgent(storyFlowAgentExample, "a lonely robot finding a friend in a junkyard");
    }

    // --- Function to Interact with the Agent ---
    public static void runAgent(StoryFlowAgentExample agent, String userTopic) {
        // --- Setup Runner and Session ---
        InMemoryRunner runner = new InMemoryRunner(agent);
        Map<String, Object> initialState = new HashMap<>();
        initialState.put("topic", "a brave kitten exploring a haunted house");
        Session session = runner.sessionService()
            .createSession(APP_NAME, USER_ID, new ConcurrentHashMap<>(initialState), SESSION_ID)
            .blockingGet();
        logger.log(Level.INFO, () -> String.format("Initial session state: %s", session.state()));

        session.state().put("topic", userTopic); // Update the state in the retrieved session
        logger.log(Level.INFO, () -> String.format("Updated session state topic to: %s", userTopic));

        Content userMessage = Content.fromParts(Part.fromText("Generate a story about: " + userTopic));

        // Use the modified session object for the run
        Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);

        final String[] finalResponse = {"No final response captured."};
        eventStream.blockingForEach(event -> {
            if (event.finalResponse() && event.content().isPresent()) {
                String author = event.author() != null ? event.author() : "UNKNOWN_AUTHOR";
                Optional<String> textOpt = event.content()
                    .flatMap(Content::parts)
                    .filter(parts -> !parts.isEmpty())
                    .map(parts -> parts.get(0).text().orElse(""));
                logger.log(Level.INFO, () -> String.format("Potential final response from [%s]: %s", author, textOpt.orElse("N/A")));
                textOpt.ifPresent(text -> finalResponse[0] = text);
            }
        });

        System.out.println("\n--- Agent Interaction Result ---");
        System.out.println("Agent Final Response: " + finalResponse[0]);

        // Retrieve session again to see the final state after the run
        Session finalSession = runner.sessionService()
            .getSession(APP_NAME, USER_ID, SESSION_ID, Optional.empty())
            .blockingGet();
        assert finalSession != null;
        System.out.println("Final Session State:" + finalSession.state());
        System.out.println("-------------------------------\n");
    }

    private boolean isStoryGenerated(InvocationContext ctx) {
        Object currentStoryObj = ctx.session().state().get("current_story");
        return currentStoryObj != null && !String.valueOf(currentStoryObj).isEmpty();
    }

    @Override
    protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) {
        logger.log(Level.INFO, () -> String.format("[%s] Starting story generation workflow.", name()));

        Flowable<Event> storyGenFlow = runStage(storyGenerator, invocationContext, "StoryGenerator");

        Flowable<Event> criticReviserFlow = Flowable.defer(() -> {
            if (!isStoryGenerated(invocationContext)) {
                logger.log(Level.SEVERE, () -> String.format("[%s] Failed to generate initial story. Aborting after StoryGenerator.", name()));
                return Flowable.empty();
            }
            logger.log(Level.INFO, () -> String.format("[%s] Story state after generator: %s", name(), invocationContext.session().state().get("current_story")));
            return runStage(loopAgent, invocationContext, "CriticReviserLoop");
        });

        Flowable<Event> postProcessingFlow = Flowable.defer(() -> {
            logger.log(Level.INFO, () -> String.format("[%s] Story state after loop: %s", name(), invocationContext.session().state().get("current_story")));
            return runStage(sequentialAgent, invocationContext, "PostProcessing");
        });

        Flowable<Event> conditionalRegenFlow = Flowable.defer(() -> {
            String toneCheckResult = (String) invocationContext.session().state().get("tone_check_result");
            logger.log(Level.INFO, () -> String.format("[%s] Tone check result: %s", name(), toneCheckResult));
            if ("negative".equalsIgnoreCase(toneCheckResult)) {
                logger.log(Level.INFO, () -> String.format("[%s] Tone is negative. Regenerating story...", name()));
                return runStage(storyGenerator, invocationContext, "StoryGenerator (Regen)");
            } else {
                logger.log(Level.INFO, () -> String.format("[%s] Tone is not negative. Keeping current story.", name()));
                return Flowable.empty();
            }
        });

        return Flowable.concatArray(storyGenFlow, criticReviserFlow, postProcessingFlow, conditionalRegenFlow)
            .doOnComplete(() -> logger.log(Level.INFO, () -> String.format("[%s] Workflow finished.", name())));
    }

    private Flowable<Event> runStage(BaseAgent agentToRun, InvocationContext ctx, String stageName) {
        logger.log(Level.INFO, () -> String.format("[%s] Running %s...", name(), stageName));
        return agentToRun.runAsync(ctx)
            .doOnNext(event -> logger.log(Level.INFO, () -> String.format("[%s] Event from %s: %s", name(), stageName, event.toJson())))
            .doOnError(err -> logger.log(Level.SEVERE, String.format("[%s] Error in %s", name(), stageName), err))
            .doOnComplete(() -> logger.log(Level.INFO, () -> String.format("[%s] %s finished.", name(), stageName)));
    }

    @Override
    protected Flowable<Event> runLiveImpl(InvocationContext invocationContext) {
        return Flowable.error(new UnsupportedOperationException("runLive not implemented."));
    }
}
```

### Multi-Agent Systems in ADK
As agentic applications grow in complexity, structuring them as a single, monolithic agent can become challenging to develop, maintain, and reason about. The Agent Development Kit (ADK) supports building sophisticated applications by composing multiple, distinct `BaseAgent` instances into a Multi-Agent System (MAS).
In ADK, a multi-agent system is an application where different agents, often forming a hierarchy, collaborate or coordinate to achieve a larger goal. Structuring your application this way offers significant advantages, including enhanced modularity, specialization, reusability, maintainability, and the ability to define structured control flows using dedicated workflow agents.
You can compose various types of agents derived from `BaseAgent` to build these systems:
*   **LLM Agents**: Agents powered by large language models. (See LLM Agents)
*   **Workflow Agents**: Specialized agents (`SequentialAgent`, `ParallelAgent`, `LoopAgent`) designed to manage the execution flow of their sub-agents. (See Workflow Agents)
*   **Custom agents**: Your own agents inheriting from `BaseAgent` with specialized, non-LLM logic. (See Custom Agents)

The following sections detail the core ADK primitives—such as agent hierarchy, workflow agents, and interaction mechanisms—that enable you to construct and manage these multi-agent systems effectively.

#### 1. ADK Primitives for Agent Composition
ADK provides core building blocks—primitives—that enable you to structure and manage interactions within your multi-agent system.
**Note**: The specific parameters or method names for the primitives may vary slightly by SDK language (e.g., `sub_agents` in Python, `subAgents` in Java). Refer to the language-specific API documentation for details.

##### 1.1. Agent Hierarchy (Parent agent, Sub Agents)
The foundation for structuring multi-agent systems is the parent-child relationship defined in `BaseAgent`.
*   **Establishing Hierarchy**: You create a tree structure by passing a list of agent instances to the `sub_agents` argument when initializing a parent agent. ADK automatically sets the `parent_agent` attribute on each child agent during initialization.
*   **Single Parent Rule**: An agent instance can only be added as a sub-agent once. Attempting to assign a second parent will result in a `ValueError` (Python) or an equivalent error/behavior in Java.
*   **Importance**: This hierarchy defines the scope for Workflow Agents and influences the potential targets for LLM-Driven Delegation. You can navigate the hierarchy using `agent.parent_agent` or find descendants using `agent.find_agent(name)`.

**Python Conceptual Example:**
```python
from google.adk.agents import LlmAgent, BaseAgent

# Define individual agents
greeter = LlmAgent(name="Greeter", model="gemini-2.0-flash")
task_doer = BaseAgent(name="TaskExecutor") # Custom non-LLM agent

# Create parent agent and assign children via sub_agents
coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    description="I coordinate greetings and tasks.",
    sub_agents=[  # Assign sub_agents here
        greeter,
        task_doer
    ]
)
# Framework automatically sets:
# assert greeter.parent_agent == coordinator
# assert task_doer.parent_agent == coordinator
```

**Java Conceptual Example:**
```java
import com.google.adk.agents.SequentialAgent; // Example workflow agent
import com.google.adk.agents.LlmAgent;
import java.util.List;


// Define individual agents
LlmAgent greeter = LlmAgent.builder().name("Greeter").model("gemini-2.0-flash").build();
// Assuming taskDoer is a SequentialAgent or other BaseAgent derivative
SequentialAgent taskDoer = SequentialAgent.builder().name("TaskExecutor") /* .subAgents(...) */ .build();

// Create parent agent and assign sub_agents
LlmAgent coordinator = LlmAgent.builder()
    .name("Coordinator")
    .model("gemini-2.0-flash")
    .description("I coordinate greetings and tasks")
    .subAgents(greeter, taskDoer) // Assign sub_agents here
    .build();

// Framework automatically sets:
// assert greeter.parentAgent().equals(coordinator);
// assert taskDoer.parentAgent().equals(coordinator);
```

##### 1.2. Workflow Agents as Orchestrators
ADK includes specialized agents derived from `BaseAgent` that don't perform tasks themselves but orchestrate the execution flow of their `sub_agents`.

*   **`SequentialAgent`**: Executes its `sub_agents` one after another in the order they are listed.
    *   **Context**: Passes the same `InvocationContext` sequentially, allowing agents to easily pass results via shared state.
    **Python Conceptual Example:**
    ```python
    from google.adk.agents import SequentialAgent, LlmAgent
    step1 = LlmAgent(name="Step1_Fetch", output_key="data") # Saves output to state['data']
    step2 = LlmAgent(name="Step2_Process", instruction="Process data from state key 'data'.")
    pipeline = SequentialAgent(name="MyPipeline", sub_agents=[step1, step2])
    # When pipeline runs, Step2 can access the state['data'] set by Step1.
    ```
    **Java Conceptual Example:**
    ```java
    import com.google.adk.agents.SequentialAgent;
    import com.google.adk.agents.LlmAgent;
    LlmAgent step1 = LlmAgent.builder().name("Step1_Fetch").outputKey("data").build(); // Saves output to state.get("data")
    LlmAgent step2 = LlmAgent.builder().name("Step2_Process").instruction("Process data from state key 'data'.").build();
    SequentialAgent pipeline = SequentialAgent.builder().name("MyPipeline").subAgents(step1, step2).build();
    // When pipeline runs, Step2 can access the state.get("data") set by Step1.
    ```
*   **`ParallelAgent`**: Executes its `sub_agents` in parallel. Events from sub-agents may be interleaved.
    *   **Context**: Modifies the `InvocationContext.branch` for each child agent (e.g., `ParentBranch.ChildName`), providing a distinct contextual path which can be useful for isolating history in some memory implementations.
    *   **State**: Despite different branches, all parallel children access the same shared `session.state`, enabling them to read initial state and write results (use distinct keys to avoid race conditions).
    **Python Conceptual Example:**
    ```python
    from google.adk.agents import ParallelAgent, LlmAgent
    fetch_weather = LlmAgent(name="WeatherFetcher", output_key="weather")
    fetch_news = LlmAgent(name="NewsFetcher", output_key="news")
    gatherer = ParallelAgent(name="InfoGatherer", sub_agents=[fetch_weather, fetch_news])
    # When gatherer runs, WeatherFetcher and NewsFetcher run concurrently.
    # A subsequent agent could read state['weather'] and state['news'].
    ```
    **Java Conceptual Example:**
    ```java
    import com.google.adk.agents.LlmAgent;
    import com.google.adk.agents.ParallelAgent;
    LlmAgent fetchWeather = LlmAgent.builder().name("WeatherFetcher").outputKey("weather").build();
    LlmAgent fetchNews = LlmAgent.builder().name("NewsFetcher").outputKey("news").build(); // Fixed: outputKey not instruction
    ParallelAgent gatherer = ParallelAgent.builder().name("InfoGatherer").subAgents(fetchWeather, fetchNews).build();
    // When gatherer runs, WeatherFetcher and NewsFetcher run concurrently.
    // A subsequent agent could read state.get("weather") and state.get("news").
    ```
*   **`LoopAgent`**: Executes its `sub_agents` sequentially in a loop.
    *   **Termination**: The loop stops if the optional `max_iterations` is reached, or if any sub-agent returns an `Event` with `escalate=True` in its `EventActions`.
    *   **Context & State**: Passes the same `InvocationContext` in each iteration, allowing state changes (e.g., counters, flags) to persist across loops.
    **Python Conceptual Example:**
    ```python
    from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
    from google.adk.events import Event, EventActions
    from google.adk.agents.invocation_context import InvocationContext
    from typing import AsyncGenerator

    class CheckCondition(BaseAgent): # Custom agent to check state
        async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
            status = ctx.session.state.get("status", "pending")
            is_done = (status == "completed")
            yield Event(author=self.name, actions=EventActions(escalate=is_done)) # Escalate if done

    process_step = LlmAgent(name="ProcessingStep") # Agent that might update state['status']
    poller = LoopAgent(
        name="StatusPoller",
        max_iterations=10,
        sub_agents=[process_step, CheckCondition(name="Checker")]
    )
    # When poller runs, it executes process_step then Checker repeatedly
    # until Checker escalates (state['status'] == 'completed') or 10 iterations pass.
    ```
    **Java Conceptual Example:**
    ```java
    import com.google.adk.agents.*;
    import com.google.adk.events.Event;
    import com.google.adk.events.EventActions;
    import io.reactivex.rxjava3.core.Flowable;
    import java.util.List;
    import java.util.Map;
    // Custom agent to check state and potentially escalate
    public static class CheckConditionAgent extends BaseAgent {
        public CheckConditionAgent(String name, String description) {
            super(name, description, List.of(), null, null);
        }

        @Override
        protected Flowable<Event> runAsyncImpl(InvocationContext ctx) {
            String status = (String) ctx.session().state().getOrDefault("status", "pending");
            boolean isDone = "completed".equalsIgnoreCase(status);
            Event checkEvent = Event.builder()
                .author(name())
                .id(Event.generateEventId()) // Important to give events unique IDs
                .actions(EventActions.builder().escalate(isDone).build()) // Escalate if done
                .build();
            return Flowable.just(checkEvent);
        }
         @Override protected Flowable<Event> runLiveImpl(InvocationContext ctx) {return Flowable.empty();} // Placeholder
    }

    // Agent that might update state.put("status")
    LlmAgent processingStepAgent = LlmAgent.builder().name("ProcessingStep").model("gemini-2.0-flash").build();
    // Custom agent instance for checking the condition
    CheckConditionAgent conditionCheckerAgent = new CheckConditionAgent("ConditionChecker", "Checks if the status is 'completed'.");
    LoopAgent poller = LoopAgent.builder()
        .name("StatusPoller")
        .maxIterations(10)
        .subAgents(processingStepAgent, conditionCheckerAgent)
        .build();
    // When poller runs, it executes processingStepAgent then conditionCheckerAgent repeatedly
    // until Checker escalates (state.get("status") == "completed") or 10 iterations pass.
    ```

##### 1.3. Interaction & Communication Mechanisms
Agents within a system often need to exchange data or trigger actions in one another. ADK facilitates this through:

**a) Shared Session State (`session.state`)**
The most fundamental way for agents operating within the same invocation (and thus sharing the same `Session` object via the `InvocationContext`) to communicate passively.
*   **Mechanism**: One agent (or its tool/callback) writes a value (`context.state['data_key'] = processed_data`), and a subsequent agent reads it (`data = context.state.get('data_key')`). State changes are tracked via `CallbackContext`.
*   **Convenience**: The `output_key` property on `LlmAgent` automatically saves the agent's final response text (or structured output) to the specified state key.
*   **Nature**: Asynchronous, passive communication. Ideal for pipelines orchestrated by `SequentialAgent` or passing data across `LoopAgent` iterations.
See Also: State Management

**Python Conceptual Example:**
```python
from google.adk.agents import LlmAgent, SequentialAgent
agent_A = LlmAgent(name="AgentA", instruction="Find the capital of France.", output_key="capital_city", model="gemini-2.0-flash")
agent_B = LlmAgent(name="AgentB", instruction="Tell me about the city stored in state key 'capital_city'.", model="gemini-2.0-flash")
pipeline = SequentialAgent(name="CityInfo", sub_agents=[agent_A, agent_B])
# AgentA runs, saves "Paris" to state['capital_city'].
# AgentB runs, its instruction processor reads state['capital_city'] to get "Paris".
```
**Java Conceptual Example:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.SequentialAgent;
LlmAgent agentA = LlmAgent.builder().name("AgentA").instruction("Find the capital of France.").outputKey("capital_city").model("gemini-2.0-flash").build();
LlmAgent agentB = LlmAgent.builder().name("AgentB").instruction("Tell me about the city stored in state key 'capital_city'.").outputKey("capital_city_info").model("gemini-2.0-flash").build(); // Fixed: outputKey to be different if it's a new value
SequentialAgent pipeline = SequentialAgent.builder().name("CityInfo").subAgents(agentA, agentB).build();
// AgentA runs, saves "Paris" to state.get("capital_city").
// AgentB runs, its instruction processor reads state.get("capital_city") to get "Paris".
```

**b) LLM-Driven Delegation (Agent Transfer)**
Leverages an `LlmAgent`'s understanding to dynamically route tasks to other suitable agents within the hierarchy.
*   **Mechanism**: The agent's LLM generates a specific function call: `transfer_to_agent(agent_name='target_agent_name')`.
*   **Handling**: The `AutoFlow`, used by default when sub-agents are present or transfer isn't disallowed, intercepts this call. It identifies the target agent using `root_agent.find_agent()` and updates the `InvocationContext` to switch execution focus.
*   **Requires**: The calling `LlmAgent` needs clear `instructions` on when to transfer, and potential target agents need distinct `description`s for the LLM to make informed decisions. Transfer scope (parent, sub-agent, siblings) can be configured on the `LlmAgent`.
*   **Nature**: Dynamic, flexible routing based on LLM interpretation.

**Python Conceptual Setup:**
```python
from google.adk.agents import LlmAgent
booking_agent = LlmAgent(name="Booker", description="Handles flight and hotel bookings.", model="gemini-2.0-flash")
info_agent = LlmAgent(name="Info", description="Provides general information and answers questions.", model="gemini-2.0-flash")
coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    instruction="You are an assistant. Delegate booking tasks to Booker and info requests to Info.",
    description="Main coordinator.",
    # AutoFlow is typically used implicitly here
    sub_agents=[booking_agent, info_agent]
)
# If coordinator receives "Book a flight", its LLM should generate:
# FunctionCall(name='transfer_to_agent', args={'agent_name': 'Booker'})
# ADK framework then routes execution to booking_agent.
```
**Java Conceptual Setup:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.common.collect.ImmutableMap; // For function call args if needed

LlmAgent bookingAgent = LlmAgent.builder().name("Booker").description("Handles flight and hotel bookings.").model("gemini-2.0-flash").build();
LlmAgent infoAgent = LlmAgent.builder().name("Info").description("Provides general information and answers questions.").model("gemini-2.0-flash").build();

// Define the coordinator agent
LlmAgent coordinator = LlmAgent.builder()
    .name("Coordinator")
    .model("gemini-2.0-flash") // Or your desired model
    .instruction("You are an assistant. Delegate booking tasks to Booker and info requests to Info.")
    .description("Main coordinator.")
    // AutoFlow will be used by default (implicitly) because subAgents are present
    // and transfer is not disallowed.
    .subAgents(bookingAgent, infoAgent)
    .build();

// If coordinator receives "Book a flight", its LLM should generate:
// FunctionCall.builder.name("transferToAgent").args(ImmutableMap.of("agent_name", "Booker")).build()
// ADK framework then routes execution to bookingAgent.
```

**c) Explicit Invocation (`AgentTool`)**
Allows an `LlmAgent` to treat another `BaseAgent` instance as a callable function or `Tool`.
*   **Mechanism**: Wrap the target agent instance in `AgentTool` and include it in the parent `LlmAgent`'s `tools` list. `AgentTool` generates a corresponding function declaration for the LLM.
*   **Handling**: When the parent LLM generates a function call targeting the `AgentTool`, the framework executes `AgentTool.run_async`. This method runs the target agent, captures its final response, forwards any state/artifact changes back to the parent's context, and returns the response as the tool's result.
*   **Nature**: Synchronous (within the parent's flow), explicit, controlled invocation like any other tool.
(Note: `AgentTool` needs to be imported and used explicitly).

**Python Conceptual Setup:**
```python
from google.adk.agents import LlmAgent, BaseAgent, InvocationContext
from google.adk.tools import agent_tool # Correct import path
from google.adk.events import Event
from google.genai import types # For Content/Part
from typing import AsyncGenerator

# Define a target agent (could be LlmAgent or custom BaseAgent)
class ImageGeneratorAgent(BaseAgent): # Example custom agent
    name: str = "ImageGen"
    description: str = "Generates an image based on a prompt."
    # ... internal logic ...
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]: # Corrected signature
        # Simplified run logic
        prompt = ctx.session.state.get("image_prompt", "default prompt")
        # ... generate image bytes ...
        image_bytes = b"..." # Placeholder
        yield Event(
            author=self.name,
            content=types.Content(parts=[types.Part.from_data(data=image_bytes, mime_type="image/png")]) # Corrected Part creation
        )

image_agent = ImageGeneratorAgent(name="ImageGenAgentInstance") # Instantiate with a name
image_tool = agent_tool.AgentTool(agent=image_agent) # Wrap the agent

# Parent agent uses the AgentTool
artist_agent = LlmAgent(
    name="Artist",
    model="gemini-2.0-flash",
    instruction="Create a prompt and use the ImageGen tool to generate the image.",
    tools=[image_tool]  # Include the AgentTool
)
# Artist LLM generates a prompt, then calls:
# FunctionCall(name='ImageGenAgentInstance', args={'image_prompt': 'a cat wearing a hat'})
# Framework calls image_tool.run_async(...), which runs ImageGeneratorAgent.
# The resulting image Part is returned to the Artist agent as the tool result.
```
**Java Conceptual Setup:**
```java
import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.InvocationContext;
import com.google.adk.tools.AgentTool;
import com.google.adk.events.Event;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import java.util.List; // For List.of()

// Example custom agent (could be LlmAgent or custom BaseAgent)
public class ImageGeneratorAgent extends BaseAgent {
    public ImageGeneratorAgent(String name, String description) {
        super(name, description, List.of(), null, null);
    }
    // ... internal logic ...
    @Override
    protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) {
        // Simplified run logic
        invocationContext.session().state().get("image_prompt");
        // Generate image bytes
        // ...
        Event responseEvent = Event.builder()
            .author(this.name())
            .content(Content.fromParts(Part.fromText("\b..."))) // Placeholder bytes
            .id(Event.generateEventId())
            .build();
        return Flowable.just(responseEvent);
    }
    @Override
    protected Flowable<Event> runLiveImpl(InvocationContext invocationContext) {
        return Flowable.error(new UnsupportedOperationException("runLive not implemented"));
    }
}

// Wrap the agent using AgentTool
ImageGeneratorAgent imageAgent = new ImageGeneratorAgent("ImageGenAgentInstance", "generates images");
AgentTool imageTool = AgentTool.create(imageAgent); // Use create method

// Parent agent uses the AgentTool
LlmAgent artistAgent = LlmAgent.builder()
    .name("Artist")
    .model("gemini-2.0-flash")
    .instruction("You are an artist. Create a detailed prompt for an image and then " +
                 "use the 'ImageGenAgentInstance' tool to generate the image. " + // Tool name matches agent's name
                 "The tool expects a single string argument named 'request' " +
                 "containing the image prompt. The tool will return a JSON string in its " +
                 "'result' field, containing 'image_base64', 'mime_type', and 'status'.")
    .description("An agent that can create images using a generation tool.")
    .tools(imageTool)  // Include the AgentTool
    .build();

// Artist LLM generates a prompt, then calls:
// FunctionCall(name='ImageGenAgentInstance', args={'imagePrompt': 'a cat wearing a hat'})
// Framework calls imageTool.runAsync(...), which runs ImageGeneratorAgent.
// The resulting image Part is returned to the Artist agent as the tool result.
```

These primitives provide the flexibility to design multi-agent interactions ranging from tightly coupled sequential workflows to dynamic, LLM-driven delegation networks.

#### 2. Common Multi-Agent Patterns using ADK Primitives
By combining ADK's composition primitives, you can implement various established patterns for multi-agent collaboration.

##### Coordinator/Dispatcher Pattern
*   **Structure**: A central `LlmAgent` (Coordinator) manages several specialized `sub_agents`.
*   **Goal**: Route incoming requests to the appropriate specialist agent.
*   **ADK Primitives Used**:
    *   **Hierarchy**: Coordinator has specialists listed in `sub_agents`.
    *   **Interaction**: Primarily uses LLM-Driven Delegation (requires clear `description`s on sub-agents and appropriate `instruction` on Coordinator) or Explicit Invocation (`AgentTool`) (Coordinator includes `AgentTool`-wrapped specialists in its `tools`).

**Python Conceptual Code:**
```python
from google.adk.agents import LlmAgent
billing_agent = LlmAgent(name="Billing", description="Handles billing inquiries.", model="gemini-2.0-flash")
support_agent = LlmAgent(name="Support", description="Handles technical support requests.", model="gemini-2.0-flash")
coordinator = LlmAgent(
    name="HelpDeskCoordinator",
    model="gemini-2.0-flash",
    instruction="Route user requests: Use Billing agent for payment issues, Support agent for technical problems.",
    description="Main help desk router.",
    # allow_transfer=True is often implicit with sub_agents in AutoFlow
    sub_agents=[billing_agent, support_agent]
)
# User asks "My payment failed" -> Coordinator's LLM should call transfer_to_agent(agent_name='Billing')
# User asks "I can't log in" -> Coordinator's LLM should call transfer_to_agent(agent_name='Support')
```
**Java Conceptual Code:**
```java
import com.google.adk.agents.LlmAgent;
LlmAgent billingAgent = LlmAgent.builder().name("Billing").description("Handles billing inquiries and payment issues.").model("gemini-2.0-flash").build();
LlmAgent supportAgent = LlmAgent.builder().name("Support").description("Handles technical support requests and login problems.").model("gemini-2.0-flash").build();
LlmAgent coordinator = LlmAgent.builder()
    .name("HelpDeskCoordinator")
    .model("gemini-2.0-flash")
    .instruction("Route user requests: Use Billing agent for payment issues, Support agent for technical problems.")
    .description("Main help desk router.")
    .subAgents(billingAgent, supportAgent) // Agent transfer is implicit with sub agents in the Autoflow, unless specified
    // using .disallowTransferToParent or disallowTransferToPeers.
    .build();
// User asks "My payment failed" -> Coordinator's LLM should call
// transferToAgent(agentName='Billing')
// User asks "I can't log in" -> Coordinator's LLM should call
// transferToAgent(agentName='Support')
```

##### Sequential Pipeline Pattern
*   **Structure**: A `SequentialAgent` contains `sub_agents` executed in a fixed order.
*   **Goal**: Implement a multi-step process where the output of one step feeds into the next.
*   **ADK Primitives Used**:
    *   **Workflow**: `SequentialAgent` defines the order.
    *   **Communication**: Primarily uses Shared Session State. Earlier agents write results (often via `output_key`), later agents read those results from `context.state`.

**Python Conceptual Code:**
```python
from google.adk.agents import SequentialAgent, LlmAgent
validator = LlmAgent(name="ValidateInput", instruction="Validate the input.", output_key="validation_status", model="gemini-2.0-flash")
processor = LlmAgent(name="ProcessData", instruction="Process data if state key 'validation_status' is 'valid'.", output_key="result", model="gemini-2.0-flash")
reporter = LlmAgent(name="ReportResult", instruction="Report the result from state key 'result'.", model="gemini-2.0-flash")
data_pipeline = SequentialAgent(name="DataPipeline", sub_agents=[validator, processor, reporter])
# validator runs -> saves to state['validation_status']
# processor runs -> reads state['validation_status'], saves to state['result']
# reporter runs -> reads state['result']
```
**Java Conceptual Code:**
```java
import com.google.adk.agents.SequentialAgent;
import com.google.adk.agents.LlmAgent;
LlmAgent validator = LlmAgent.builder()
    .name("ValidateInput")
    .instruction("Validate the input")
    .outputKey("validation_status") // Saves its main text output to session.state["validation_status"]
    .model("gemini-2.0-flash")
    .build();
LlmAgent processor = LlmAgent.builder()
    .name("ProcessData")
    .instruction("Process data if state key 'validation_status' is 'valid'")
    .outputKey("result") // Saves its main text output to session.state["result"]
    .model("gemini-2.0-flash")
    .build();
LlmAgent reporter = LlmAgent.builder()
    .name("ReportResult")
    .instruction("Report the result from state key 'result'")
    .model("gemini-2.0-flash")
    .build();
SequentialAgent dataPipeline = SequentialAgent.builder()
    .name("DataPipeline")
    .subAgents(validator, processor, reporter)
    .build();
// validator runs -> saves to state.get("validation_status")
// processor runs -> reads state.get("validation_status"), saves to state.get("result")
// reporter runs -> reads state.get("result")
```

##### Parallel Fan-Out/Gather Pattern
*   **Structure**: A `ParallelAgent` runs multiple `sub_agents` concurrently, often followed by a later agent (in a `SequentialAgent`) that aggregates results.
*   **Goal**: Execute independent tasks simultaneously to reduce latency, then combine their outputs.
*   **ADK Primitives Used**:
    *   **Workflow**: `ParallelAgent` for concurrent execution (Fan-Out). Often nested within a `SequentialAgent` to handle the subsequent aggregation step (Gather).
    *   **Communication**: Sub-agents write results to distinct keys in Shared Session State. The subsequent "Gather" agent reads multiple state keys.

**Python Conceptual Code:**
```python
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent
fetch_api1 = LlmAgent(name="API1Fetcher", instruction="Fetch data from API 1.", output_key="api1_data", model="gemini-2.0-flash")
fetch_api2 = LlmAgent(name="API2Fetcher", instruction="Fetch data from API 2.", output_key="api2_data", model="gemini-2.0-flash")
gather_concurrently = ParallelAgent(name="ConcurrentFetch", sub_agents=[fetch_api1, fetch_api2])
synthesizer = LlmAgent(name="Synthesizer", instruction="Combine results from state keys 'api1_data' and 'api2_data'.", model="gemini-2.0-flash")
overall_workflow = SequentialAgent(name="FetchAndSynthesize", sub_agents=[gather_concurrently, synthesizer]) # Run parallel fetch, then synthesize
# fetch_api1 and fetch_api2 run concurrently, saving to state.
# synthesizer runs afterwards, reading state['api1_data'] and state['api2_data'].
```
**Java Conceptual Code:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.ParallelAgent;
import com.google.adk.agents.SequentialAgent;
LlmAgent fetchApi1 = LlmAgent.builder().name("API1Fetcher").instruction("Fetch data from API 1.").outputKey("api1_data").model("gemini-2.0-flash").build();
LlmAgent fetchApi2 = LlmAgent.builder().name("API2Fetcher").instruction("Fetch data from API 2.").outputKey("api2_data").model("gemini-2.0-flash").build();
ParallelAgent gatherConcurrently = ParallelAgent.builder().name("ConcurrentFetcher").subAgents(fetchApi1, fetchApi2).build(); // Corrected order
LlmAgent synthesizer = LlmAgent.builder().name("Synthesizer").instruction("Combine results from state keys 'api1_data' and 'api2_data'.").model("gemini-2.0-flash").build();
SequentialAgent overallWorkflow = SequentialAgent.builder() // Renamed for clarity
    .name("FetchAndSynthesize") // Run parallel fetch, then synthesize
    .subAgents(gatherConcurrently, synthesizer)
    .build();
// fetchApi1 and fetchApi2 run concurrently, saving to state.
// synthesizer runs afterwards, reading state.get("api1_data") and state.get("api2_data").
```

##### Hierarchical Task Decomposition
*   **Structure**: A multi-level tree of agents where higher-level agents break down complex goals and delegate sub-tasks to lower-level agents.
*   **Goal**: Solve complex problems by recursively breaking them down into simpler, executable steps.
*   **ADK Primitives Used**:
    *   **Hierarchy**: Multi-level `parent_agent` / `sub_agents` structure.
    *   **Interaction**: Primarily LLM-Driven Delegation or Explicit Invocation (`AgentTool`) used by parent agents to assign tasks to subagents. Results are returned up the hierarchy (via tool responses or state).

**Python Conceptual Code:**
```python
from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool

# Low-level tool-like agents
web_searcher = LlmAgent(name="WebSearch", description="Performs web searches for facts.", model="gemini-2.0-flash")
summarizer = LlmAgent(name="Summarizer", description="Summarizes text.", model="gemini-2.0-flash")

# Mid-level agent combining tools
research_assistant = LlmAgent(
    name="ResearchAssistant",
    model="gemini-2.0-flash",
    description="Finds and summarizes information on a topic.",
    tools=[
        agent_tool.AgentTool(agent=web_searcher),
        agent_tool.AgentTool(agent=summarizer)
    ]
)

# High-level agent delegating research
report_writer = LlmAgent(
    name="ReportWriter",
    model="gemini-2.0-flash",
    instruction="Write a report on topic X. Use the ResearchAssistant to gather information.",
    tools=[agent_tool.AgentTool(agent=research_assistant)]
    # Alternatively, could use LLM Transfer if research_assistant is a sub_agent
)
# User interacts with ReportWriter.
# ReportWriter calls ResearchAssistant tool.
# ResearchAssistant calls WebSearch and Summarizer tools.
# Results flow back up.
```
**Java Conceptual Code:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.tools.AgentTool;
import java.util.List;

// Low-level tool-like agents
LlmAgent webSearcher = LlmAgent.builder().name("WebSearch").description("Performs web searches for facts.").model("gemini-2.0-flash").build();
LlmAgent summarizer = LlmAgent.builder().name("Summarizer").description("Summarizes text.").model("gemini-2.0-flash").build();

// Mid-level agent combining tools
LlmAgent researchAssistant = LlmAgent.builder()
    .name("ResearchAssistant")
    .model("gemini-2.0-flash")
    .description("Finds and summarizes information on a topic.")
    .tools(AgentTool.create(webSearcher), AgentTool.create(summarizer))
    .build();

// High-level agent delegating research
LlmAgent reportWriter = LlmAgent.builder()
    .name("ReportWriter")
    .model("gemini-2.0-flash")
    .instruction("Write a report on topic X. Use the ResearchAssistant to gather information.")
    .tools(AgentTool.create(researchAssistant)) // Alternatively, could use LLM Transfer if research_assistant is a subAgent
    .build();

// User interacts with ReportWriter.
// ReportWriter calls ResearchAssistant tool.
// ResearchAssistant calls WebSearch and Summarizer tools.
// Results flow back up.
```

##### Review/Critique Pattern (Generator-Critic)
*   **Structure**: Typically involves two agents within a `SequentialAgent`: a Generator and a Critic/Reviewer.
*   **Goal**: Improve the quality or validity of generated output by having a dedicated agent review it.
*   **ADK Primitives Used**:
    *   **Workflow**: `SequentialAgent` ensures generation happens before review.
    *   **Communication**: Shared Session State (Generator uses `output_key` to save output; Reviewer reads that state key). The Reviewer might save its feedback to another state key for subsequent steps.

**Python Conceptual Code:**
```python
from google.adk.agents import SequentialAgent, LlmAgent
generator = LlmAgent(name="DraftWriter", instruction="Write a short paragraph about subject X.", output_key="draft_text", model="gemini-2.0-flash")
reviewer = LlmAgent(name="FactChecker", instruction="Review the text in state key 'draft_text' for factual accuracy. Output 'valid' or 'invalid' with reasons.", output_key="review_status", model="gemini-2.0-flash")
# Optional: Further steps based on review_status
review_pipeline = SequentialAgent(name="WriteAndReview", sub_agents=[generator, reviewer])
# generator runs -> saves draft to state['draft_text']
# reviewer runs -> reads state['draft_text'], saves status to state['review_status']
```
**Java Conceptual Code:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.SequentialAgent;
LlmAgent generator = LlmAgent.builder().name("DraftWriter").instruction("Write a short paragraph about subject X.").outputKey("draft_text").model("gemini-2.0-flash").build();
LlmAgent reviewer = LlmAgent.builder().name("FactChecker").instruction("Review the text in state key 'draft_text' for factual accuracy. Output 'valid' or 'invalid' with reasons.").outputKey("review_status").model("gemini-2.0-flash").build();
// Optional: Further steps based on review_status
SequentialAgent reviewPipeline = SequentialAgent.builder().name("WriteAndReview").subAgents(generator, reviewer).build();
// generator runs -> saves draft to state.get("draft_text")
// reviewer runs -> reads state.get("draft_text"), saves status to state.get("review_status")
```

##### Iterative Refinement Pattern
*   **Structure**: Uses a `LoopAgent` containing one or more agents that work on a task over multiple iterations.
*   **Goal**: Progressively improve a result (e.g., code, text, plan) stored in the session state until a quality threshold is met or a maximum number of iterations is reached.
*   **ADK Primitives Used**:
    *   **Workflow**: `LoopAgent` manages the repetition.
    *   **Communication**: Shared Session State is essential for agents to read the previous iteration's output and save the refined version.
    *   **Termination**: The loop typically ends based on `max_iterations` or a dedicated checking agent setting `escalate=True` in the `EventActions` when the result is satisfactory.

**Python Conceptual Code:**
```python
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent, InvocationContext
from google.adk.events import Event, EventActions
from typing import AsyncGenerator

# Agent to generate/refine code based on state['current_code'] and state['requirements']
code_refiner = LlmAgent(
    name="CodeRefiner",
    instruction="Read state['current_code'] (if exists) and state['requirements']. Generate/refine Python code to meet requirements. Save to state['current_code'].",
    output_key="current_code", # Overwrites previous code in state
    model="gemini-2.0-flash"
)

# Agent to check if the code meets quality standards
quality_checker = LlmAgent(
    name="QualityChecker",
    instruction="Evaluate the code in state['current_code'] against state['requirements']. Output 'pass' or 'fail'.",
    output_key="quality_status",
    model="gemini-2.0-flash"
)

# Custom agent to check the status and escalate if 'pass'
class CheckStatusAndEscalate(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        status = ctx.session.state.get("quality_status", "fail")
        should_stop = (status == "pass")
        yield Event(author=self.name, actions=EventActions(escalate=should_stop))

refinement_loop = LoopAgent(
    name="CodeRefinementLoop",
    max_iterations=5,
    sub_agents=[
        code_refiner,
        quality_checker,
        CheckStatusAndEscalate(name="StopChecker") # Instantiate custom agent
    ]
)
# Loop runs: Refiner -> Checker -> StopChecker
# State['current_code'] is updated each iteration.
# Loop stops if QualityChecker outputs 'pass' (leading to StopChecker escalating) or after 5 iterations.
```
**Java Conceptual Code:**
```java
import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.LoopAgent;
import com.google.adk.events.Event;
import com.google.adk.events.EventActions;
import com.google.adk.agents.InvocationContext;
import io.reactivex.rxjava3.core.Flowable;
import java.util.List;

// Agent to generate/refine code
LlmAgent codeRefiner = LlmAgent.builder()
    .name("CodeRefiner")
    .instruction("Read state.get(\"current_code\") (if exists) and state.get(\"requirements\"). Generate/refine Java code to meet requirements. Save to state.put(\"current_code\").")
    .outputKey("current_code") // Overwrites previous code in state
    .model("gemini-2.0-flash")
    .build();

// Agent to check if the code meets quality standards
LlmAgent qualityChecker = LlmAgent.builder()
    .name("QualityChecker")
    .instruction("Evaluate the code in state.get(\"current_code\") against state.get(\"requirements\"). Output 'pass' or 'fail'.")
    .outputKey("quality_status")
    .model("gemini-2.0-flash")
    .build();

BaseAgent checkStatusAndEscalate = new BaseAgent("StopChecker", "Checks quality_status and escalates if 'pass'.", List.of(), null, null) {
    @Override
    protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) {
        String status = (String) invocationContext.session().state().getOrDefault("quality_status", "fail");
        boolean shouldStop = "pass".equals(status);
        EventActions actions = EventActions.builder().escalate(shouldStop).build();
        Event event = Event.builder().author(this.name()).actions(actions).id(Event.generateEventId()).build();
        return Flowable.just(event);
    }
    @Override protected Flowable<Event> runLiveImpl(InvocationContext ctx) {return Flowable.empty();} // Placeholder
};

LoopAgent refinementLoop = LoopAgent.builder()
    .name("CodeRefinementLoop")
    .maxIterations(5)
    .subAgents(codeRefiner, qualityChecker, checkStatusAndEscalate)
    .build();

// Loop runs: Refiner -> Checker -> StopChecker
// State.get("current_code") is updated each iteration.
// Loop stops if QualityChecker outputs 'pass' (leading to StopChecker escalating) or after 5 iterations.
```

##### Human-in-the-Loop Pattern
*   **Structure**: Integrates human intervention points within an agent workflow.
*   **Goal**: Allow for human oversight, approval, correction, or tasks that AI cannot perform.
*   **ADK Primitives Used (Conceptual)**:
    *   **Interaction**: Can be implemented using a custom `Tool` that pauses execution and sends a request to an external system (e.g., a UI, ticketing system) waiting for human input. The tool then returns the human's response to the agent.
    *   **Workflow**: Could use LLM-Driven Delegation (`transfer_to_agent`) targeting a conceptual "Human Agent" that triggers the external workflow, or use the custom tool within an `LlmAgent`.
    *   **State/Callbacks**: State can hold task details for the human; callbacks can manage the interaction flow.
    *   **Note**: ADK doesn't have a built-in "Human Agent" type, so this requires custom integration.

**Python Conceptual Code:**
```python
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import FunctionTool

# --- Assume external_approval_tool exists ---
# This tool would:
# 1. Take details (e.g., request_id, amount, reason).
# 2. Send these details to a human review system (e.g., via API).
# 3. Poll or wait for the human response (approved/rejected).
# 4. Return the human's decision.
# async def external_approval_tool(amount: float, reason: str) -> str: ...
# For this example, let's mock it
def mock_external_approval_tool(amount: float, reason: str) -> dict:
    print(f"TOOL: Requesting human approval for amount: {amount}, reason: {reason}")
    # In a real scenario, this would interact with an external system.
    # Here, we simulate an approval.
    return {"decision": "approved", "approved_by": "human_reviewer_01"}

approval_tool = FunctionTool(func=mock_external_approval_tool)


# Agent that prepares the request
prepare_request = LlmAgent(
    name="PrepareApproval",
    model="gemini-2.0-flash",
    instruction="Prepare the approval request details based on user input. Store amount and reason in state.",
    # ... likely sets state['approval_amount'] and state['approval_reason'] ...
    output_key="approval_details" # Example: saves a dict {'amount': 100, 'reason': 'lunch'}
)

# Agent that calls the human approval tool
request_approval = LlmAgent(
    name="RequestHumanApproval",
    model="gemini-2.0-flash",
    instruction="Use the external_approval_tool with amount from state.approval_details.amount and reason from state.approval_details.reason.", # Simplified access for instruction
    tools=[approval_tool],
    output_key="human_decision"
)

# Agent that proceeds based on human decision
process_decision = LlmAgent(
    name="ProcessDecision",
    model="gemini-2.0-flash",
    instruction="Check state key 'human_decision'. If 'approved', proceed. If 'rejected', inform user."
)

approval_workflow = SequentialAgent(
    name="HumanApprovalWorkflow",
    sub_agents=[prepare_request, request_approval, process_decision]
)
```
**Java Conceptual Code:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.SequentialAgent;
import com.google.adk.tools.FunctionTool;
import com.google.adk.tools.ToolContext;
import com.google.adk.tools.Annotations.Schema;
import java.util.Map; // For tool return type

// --- Assume external_approval_tool exists ---
// This tool would:
// 1. Take details (e.g., request_id, amount, reason).
// 2. Send these details to a human review system (e.g., via API).
// 3. Poll or wait for the human response (approved/rejected).
// 4. Return the human's decision.
public static Map<String, Object> externalApprovalTool(
    @Schema(name="amount") double amount,
    @Schema(name="reason") String reason,
    @Schema(name="toolContext") ToolContext toolContext // For state access if needed
) {
    System.out.printf("TOOL: Requesting human approval for amount: %f, reason: %s%n", amount, reason);
    return Map.of("decision", "approved", "approved_by", "human_reviewer_01"); // Mocked
}
// FunctionTool approvalTool = FunctionTool.create(YourClass.class, "externalApprovalTool"); // Wrap it

// Agent that prepares the request
LlmAgent prepareRequest = LlmAgent.builder()
    .name("PrepareApproval")
    .model("gemini-2.0-flash")
    .instruction("Prepare the approval request details based on user input. Store amount and reason in state.")
    .outputKey("approval_details") // Example: saves a map {"amount": 100.0, "reason": "lunch"}
    .build();

// Agent that calls the human approval tool
LlmAgent requestApproval = LlmAgent.builder()
    .name("RequestHumanApproval")
    .model("gemini-2.0-flash")
    .instruction("Use the external_approval_tool with amount from state.approval_details.amount and reason from state.approval_details.reason.")
    .tools(FunctionTool.create(HumanInTheLoopPattern.class, "externalApprovalTool")) // Assume this class and method
    .outputKey("human_decision")
    .build();

// Agent that proceeds based on human decision
LlmAgent processDecision = LlmAgent.builder()
    .name("ProcessDecision")
    .model("gemini-2.0-flash")
    .instruction("Check state key 'human_decision'. If 'approved', proceed. If 'rejected', inform user.")
    .build();

SequentialAgent approvalWorkflow = SequentialAgent.builder()
    .name("HumanApprovalWorkflow")
    .subAgents(prepareRequest, requestApproval, processDecision)
    .build();
```

These patterns provide starting points for structuring your multi-agent systems. You can mix and match them as needed to create the most effective architecture for your specific application.

## 4. Events
Events are the fundamental units of information flow within the Agent Development Kit (ADK). They represent every significant occurrence during an agent's interaction lifecycle, from initial user input to the final response and all the steps in between. Understanding events is crucial because they are the primary way components communicate, state is managed, and control flow is directed.

### What Events Are and Why They Matter
An `Event` in ADK is an immutable record representing a specific point in the agent's execution. It captures user messages, agent replies, requests to use tools (function calls), tool results, state changes, control signals, and errors.
Technically, it's an instance of the `google.adk.events.Event` class (Python) or `com.google.adk.events.Event` class (Java), which builds upon the basic `LlmResponse` structure by adding essential ADK-specific metadata and an `actions` payload.

**Conceptual Structure of an Event (Python):**
```python
# from google.adk.events import Event, EventActions
# from google.genai import types
#
# class Event(LlmResponse): # Simplified view
#     # --- LlmResponse fields ---
#     content: Optional[types.Content]
#     partial: Optional[bool]
#     # ... other response fields ...
#
#     # --- ADK specific additions ---
#     author: str          # 'user' or agent name
#     invocation_id: str   # ID for the whole interaction run
#     id: str              # Unique ID for this specific event
#     timestamp: float     # Creation time
#     actions: EventActions # Important for side-effects & control
#     branch: Optional[str] # Hierarchy path
#     # ...
```

**Conceptual Structure of an Event (Java):**
```java
// Simplified view based on the provided com.google.adk.events.Event.java
// public class Event extends JsonBaseModel {
//     // --- Fields analogous to LlmResponse ---
//     private Optional<Content> content;
//     private Optional<Boolean> partial;
//     // ... other response fields like errorCode, errorMessage ...
//
//     // --- ADK specific additions ---
//     private String author;         // 'user' or agent name
//     private String invocationId;   // ID for the whole interaction run
//     private String id;             // Unique ID for this specific event
//     private long timestamp;        // Creation time (epoch milliseconds)
//     private EventActions actions;  // Important for side-effects & control
//     private Optional<String> branch; // Hierarchy path
//     // ... other fields like turnComplete, longRunningToolIds etc.
// }
```

Events are central to ADK's operation for several key reasons:
*   **Communication**: They serve as the standard message format between the user interface, the `Runner`, agents, the LLM, and tools. Everything flows as an `Event`.
*   **Signaling State & Artifact Changes**: Events carry instructions for state modifications and track artifact updates. The `SessionService` uses these signals to ensure persistence. In Python changes are signaled via `event.actions.state_delta` and `event.actions.artifact_delta`.
*   **Control Flow**: Specific fields like `event.actions.transfer_to_agent` or `event.actions.escalate` act as signals that direct the framework, determining which agent runs next or if a loop should terminate.
*   **History & Observability**: The sequence of events recorded in `session.events` provides a complete, chronological history of an interaction, invaluable for debugging, auditing, and understanding agent behavior step-by-step.

In essence, the entire process, from a user's query to the agent's final answer, is orchestrated through the generation, interpretation, and processing of `Event` objects.

### Understanding and Using Events
As a developer, you'll primarily interact with the stream of events yielded by the `Runner`. Here's how to understand and extract information from them:
**Note**: The specific parameters or method names for the primitives may vary slightly by SDK language (e.g., `event.content` in Python, `event.content().get().parts()` in Java). Refer to the language-specific API documentation for details.

#### Identifying Event Origin and Type
Quickly determine what an event represents by checking:
*   **Who sent it? (`event.author`)**
    *   `'user'`: Indicates input directly from the end-user.
    *   `'AgentName'`: Indicates output or action from a specific agent (e.g., `'WeatherAgent'`, `'SummarizerAgent'`).
*   **What's the main payload? (`event.content` and `event.content.parts`)**
    *   **Text**: Indicates a conversational message. For Python, check if `event.content.parts[0].text` exists. For Java, check if `event.content()` is present, its `parts()` are present and not empty, and the first part's `text()` is present.
    *   **Tool Call Request**: Check `event.get_function_calls()`. If not empty, the LLM is asking to execute one or more tools. Each item in the list has `.name` and `.args`.
    *   **Tool Result**: Check `event.get_function_responses()`. If not empty, this event carries the result(s) from tool execution(s). Each item has `.name` and `.response` (the dictionary returned by the tool). Note: For history structuring, the `role` inside the `content` is often `'user'`, but the event `author` is typically the agent that requested the tool call.
*   **Is it streaming output? (`event.partial`)** Indicates whether this is an incomplete chunk of text from the LLM.
    *   `True`: More text will follow.
    *   `False` or `None` / `Optional.empty()`: This part of the content is complete (though the overall turn might not be finished if `turn_complete` is also false).

**Python Pseudocode:**
```python
# async for event in runner.run_async(...):
#     print(f"Event from: {event.author}")
#
#     if event.content and event.content.parts:
#         if event.get_function_calls():
#             print("  Type: Tool Call Request")
#         elif event.get_function_responses():
#             print("  Type: Tool Result")
#         elif event.content.parts[0].text:
#             if event.partial:
#                 print("  Type: Streaming Text Chunk")
#             else:
#                 print("  Type: Complete Text Message")
#         else:
#             print("  Type: Other Content (e.g., code result)")
#     elif event.actions and (event.actions.state_delta or event.actions.artifact_delta):
#         print("  Type: State/Artifact Update")
#     else:
#         print("  Type: Control Signal or Other")
```
**Java Pseudocode:**
```java
// import com.google.genai.types.Content;
// import com.google.adk.events.Event;
// import com.google.adk.events.EventActions;
// runner.runAsync(...).forEach(event -> {
// Assuming a synchronous stream or reactive stream
//     System.out.println("Event from: " + event.author());
//
//     if (event.content().isPresent()) {
//         Content content = event.content().get();
//         if (!event.functionCalls().isEmpty()) {
//             System.out.println("  Type: Tool Call Request");
//         } else if (!event.functionResponses().isEmpty()) {
//             System.out.println("  Type: Tool Result");
//         } else if (content.parts().isPresent() && !content.parts().get().isEmpty() &&
//                    content.parts().get().get(0).text().isPresent()) {
//             if (event.partial().orElse(false)) {
//                 System.out.println("  Type: Streaming Text Chunk");
//             } else {
//                 System.out.println("  Type: Complete Text Message");
//             }
//         } else {
//             System.out.println("  Type: Other Content (e.g., code result)");
//         }
//     } else if (event.actions() != null &&
//                ((event.actions().stateDelta() != null && !event.actions().stateDelta().isEmpty()) ||
//                 (event.actions().artifactDelta() != null && !event.actions().artifactDelta().isEmpty()))) {
//         System.out.println("  Type: State/Artifact Update");
//     } else {
//         System.out.println("  Type: Control Signal or Other");
//     }
// });
```

#### Extracting Key Information
Once you know the event type, access the relevant data:
*   **Text Content**: Always check for the presence of content and parts before accessing text. In Python its `text = event.content.parts[0].text`.
*   **Function Call Details**:
    **Python:**
    ```python
    calls = event.get_function_calls()
    if calls:
        for call in calls:
            tool_name = call.name
            arguments = call.args  # This is usually a dictionary
            print(f"  Tool: {tool_name}, Args: {arguments}")
            # Application might dispatch execution based on this
    ```
    **Java:**
    ```java
    import com.google.genai.types.FunctionCall;
    import com.google.common.collect.ImmutableList;
    import java.util.Map;

    ImmutableList<FunctionCall> calls = event.functionCalls(); // from Event.java
    if (!calls.isEmpty()) {
        for (FunctionCall call : calls) {
            String toolName = call.name().get(); // args is Optional<Map<String, Object>>
            Map<String, Object> arguments = call.args().get();
            System.out.println("  Tool: " + tool_name + ", Args: " + arguments);
            // Application might dispatch execution based on this
        }
    }
    ```
*   **Function Response Details**:
    **Python:**
    ```python
    responses = event.get_function_responses()
    if responses:
        for response in responses:
            tool_name = response.name
            result_dict = response.response  # The dictionary returned by the tool
            print(f"  Tool Result: {tool_name} -> {result_dict}")
    ```
    **Java:**
    ```java
    import com.google.genai.types.FunctionResponse;
    import com.google.common.collect.ImmutableList;
    import java.util.Map;

    ImmutableList<FunctionResponse> responses = event.functionResponses(); // from Event.java
    if (!responses.isEmpty()) {
        for (FunctionResponse response : responses) {
            String toolName = response.name().get();
            Map<String, Object> result = (Map<String, Object>) response.response().get(); // Corrected casting
            System.out.println("  Tool Result: " + toolName + " -> " + result);
        }
    }
    ```
*   **Identifiers**:
    *   `event.id`: Unique ID for this specific event instance.
    *   `event.invocation_id`: ID for the entire user-request-to-final-response cycle this event belongs to. Useful for logging and tracing.

#### Detecting Actions and Side Effects
The `event.actions` object signals changes that occurred or should occur. Always check if `event.actions` and its fields/methods exists before accessing them.

*   **State Changes**: Gives you a collection of key-value pairs that were modified in the session state during the step that produced this event.
    *   Python: `delta = event.actions.state_delta` (a dictionary of `{key: value}` pairs).
        ```python
        if event.actions and event.actions.state_delta:
            print(f"  State changes: {event.actions.state_delta}")
            # Update local UI or application state if necessary
        ```
    *   Java: `ConcurrentMap<String, Object> delta = event.actions().stateDelta();`
        ```java
        import java.util.concurrent.ConcurrentMap;
        import com.google.adk.events.EventActions;

        EventActions actions = event.actions(); // Assuming event.actions() is not null
        if (actions != null && actions.stateDelta() != null && !actions.stateDelta().isEmpty()) {
            ConcurrentMap<String, Object> stateChanges = actions.stateDelta();
            System.out.println("  State changes: " + stateChanges);
            // Update local UI or application state if necessary
        }
        ```
*   **Artifact Saves**: Gives you a collection indicating which artifacts were saved and their new version number (or relevant `Part` information).
    *   Python: `artifact_changes = event.actions.artifact_delta` (a dictionary of `{filename: version}`).
        ```python
        if event.actions and event.actions.artifact_delta:
            print(f"  Artifacts saved: {event.actions.artifact_delta}")
            # UI might refresh an artifact list
        ```
    *   Java: `ConcurrentMap<String, Part> artifactChanges = event.actions().artifactDelta();`
        ```java
        import java.util.concurrent.ConcurrentMap;
        import com.google.genai.types.Part;
        import com.google.adk.events.EventActions;

        EventActions actions = event.actions(); // Assuming event.actions() is not null
        if (actions != null && actions.artifactDelta() != null && !actions.artifactDelta().isEmpty()) {
            ConcurrentMap<String, Part> artifactChanges = actions.artifactDelta();
            System.out.println("  Artifacts saved: " + artifactChanges);
            // UI might refresh an artifact list
            // Iterate through artifactChanges.entrySet() to get filename and Part details
        }
        ```
*   **Control Flow Signals**: Check boolean flags or string values:
    *   Python:
        *   `event.actions.transfer_to_agent` (string): Control should pass to the named agent.
        *   `event.actions.escalate` (bool): A loop should terminate.
        *   `event.actions.skip_summarization` (bool): A tool result should not be summarized by the LLM.
        ```python
        if event.actions:
            if event.actions.transfer_to_agent:
                print(f"  Signal: Transfer to {event.actions.transfer_to_agent}")
            if event.actions.escalate:
                print("  Signal: Escalate (terminate loop)")
            if event.actions.skip_summarization:
                print("  Signal: Skip summarization for tool result")
        ```
    *   Java:
        *   `event.actions().transferToAgent()` (returns `Optional<String>`): Control should pass to the named agent.
        *   `event.actions().escalate()` (returns `Optional<Boolean>`): A loop should terminate.
        *   `event.actions().skipSummarization()` (returns `Optional<Boolean>`): A tool result should not be summarized by the LLM.
        ```java
        import com.google.adk.events.EventActions;
        import java.util.Optional;

        EventActions actions = event.actions(); // Assuming event.actions() is not null
        if (actions != null) {
            Optional<String> transferAgent = actions.transferToAgent();
            if (transferAgent.isPresent()) {
                System.out.println("  Signal: Transfer to " + transferAgent.get());
            }
            Optional<Boolean> escalate = actions.escalate();
            if (escalate.orElse(false)) { // or escalate.isPresent() && escalate.get()
                System.out.println("  Signal: Escalate (terminate loop)");
            }
            Optional<Boolean> skipSummarization = actions.skipSummarization();
            if (skipSummarization.orElse(false)) { // or skipSummarization.isPresent() && skipSummarization.get()
                System.out.println("  Signal: Skip summarization for tool result");
            }
        }
        ```

#### Determining if an Event is a "Final" Response
Use the built-in helper method `event.is_final_response()` to identify events suitable for display as the agent's complete output for a turn.
*   **Purpose**: Filters out intermediate steps (like tool calls, partial streaming text, internal state updates) from the final user-facing message(s).
*   **When `True`?**
    *   The event contains a tool result (`function_response`) and `skip_summarization` is `True`.
    *   The event contains a tool call (`function_call`) for a tool marked as `is_long_running=True`. In Java, check if the `longRunningToolIds` list is not empty: `event.longRunningToolIds().isPresent() && !event.longRunningToolIds().get().isEmpty()` is `true`.
    *   OR, all of the following are met:
        *   No function calls (`get_function_calls()` is empty).
        *   No function responses (`get_function_responses()` is empty).
        *   Not a partial stream chunk (`partial` is not `True`).
        *   Doesn't end with a code execution result that might need further processing/display.
*   **Usage**: Filter the event stream in your application logic.
    **Python Pseudocode:**
    ```python
    # full_response_text = ""
    # async for event in runner.run_async(...):
    #     # Accumulate streaming text if needed...
    #     if event.partial and event.content and event.content.parts and event.content.parts[0].text:
    #         full_response_text += event.content.parts[0].text
    #
    #     # Check if it's a final, displayable event
    #     if event.is_final_response():
    #         print("\n--- Final Output Detected ---")
    #         if event.content and event.content.parts and event.content.parts[0].text:
    #              # If it's the final part of a stream, use accumulated text
    #              final_text = full_response_text + (event.content.parts[0].text if not event.partial else "")
    #              print(f"Display to user: {final_text.strip()}")
    #              full_response_text = "" # Reset accumulator
    #         elif event.actions and event.actions.skip_summarization and event.get_function_responses():
    #              # Handle displaying the raw tool result if needed
    #              response_data = event.get_function_responses()[0].response
    #              print(f"Display raw tool result: {response_data}")
    #         elif hasattr(event, 'long_running_tool_ids') and event.long_running_tool_ids:
    #              print("Display message: Tool is running in background...")
    #         else:
    #              # Handle other types of final responses if applicable
    #              print("Display: Final non-textual response or signal.")
    ```
    **Java Pseudocode:**
    ```java
    // import com.google.adk.events.Event;
    // import com.google.genai.types.Content;
    // import com.google.genai.types.FunctionResponse;
    // import java.util.Map;
    //
    // StringBuilder fullResponseText = new StringBuilder();
    // runner.run(...).forEach(event -> { // Assuming a stream of events
    //     // Accumulate streaming text if needed...
    //     if (event.partial().orElse(false) && event.content().isPresent()) {
    //         event.content().flatMap(Content::parts).ifPresent(parts -> {
    //             if (!parts.isEmpty() && parts.get(0).text().isPresent()) {
    //                 fullResponseText.append(parts.get(0).text().get());
    //             }
    //         });
    //     }
    //
    //     // Check if it's a final, displayable event
    //     if (event.finalResponse()) { // Using the method from Event.java
    //         System.out.println("\n--- Final Output Detected ---");
    //         if (event.content().isPresent() &&
    //             event.content().flatMap(Content::parts).map(parts -> !parts.isEmpty() && parts.get(0).text().isPresent()).orElse(false)) {
    //             // If it's the final part of a stream, use accumulated text
    //             String eventText = event.content().get().parts().get().get(0).text().get();
    //             String finalText = fullResponseText.toString() + (event.partial().orElse(false) ? "" : eventText);
    //             System.out.println("Display to user: " + finalText.trim());
    //             fullResponseText.setLength(0); // Reset accumulator
    //         } else if (event.actions() != null && event.actions().skipSummarization().orElse(false) && !event.functionResponses().isEmpty()) {
    //             // Handle displaying the raw tool result if needed,
    //             // especially if finalResponse() was true due to other conditions
    //             // or if you want to display skipped summarization results regardless of finalResponse()
    //             Map<String, Object> responseData = (Map<String, Object>) event.functionResponses().get(0).response().get();
    //             System.out.println("Display raw tool result: " + responseData);
    //         } else if (event.longRunningToolIds().isPresent() && !event.longRunningToolIds().get().isEmpty()) {
    //             // This case is covered by event.finalResponse()
    //             System.out.println("Display message: Tool is running in background...");
    //         } else {
    //             // Handle other types of final responses if applicable
    //             System.out.println("Display: Final non-textual response or signal.");
    //         }
    //     }
    // });
    ```

By carefully examining these aspects of an event, you can build robust applications that react appropriately to the rich information flowing through the ADK system.

### How Events Flow: Generation and Processing
Events are created at different points and processed systematically by the framework. Understanding this flow helps clarify how actions and history are managed.

**Generation Sources**:
*   **User Input**: The `Runner` typically wraps initial user messages or mid-conversation inputs into an `Event` with `author='user'`.
*   **Agent Logic**: Agents (`BaseAgent`, `LlmAgent`) explicitly `yield Event(...)` objects (setting `author=self.name`) to communicate responses or signal actions.
*   **LLM Responses**: The ADK model integration layer translates raw LLM output (text, function calls, errors) into `Event` objects, authored by the calling agent.
*   **Tool Results**: After a tool executes, the framework generates an `Event` containing the `function_response`. The `author` is typically the agent that requested the tool, while the `role` inside the `content` is set to `'user'` for the LLM history.

**Processing Flow**:
1.  **Yield/Return**: An event is generated and yielded (Python) or returned/emitted (Java) by its source.
2.  **Runner Receives**: The main `Runner` executing the agent receives the event.
3.  **`SessionService` Processing**: The `Runner` sends the event to the configured `SessionService`. This is a critical step:
    *   **Applies Deltas**: The service merges `event.actions.state_delta` into `session.state` and updates internal records based on `event.actions.artifact_delta`. (Note: The actual artifact saving usually happened earlier when `context.save_artifact` was called).
    *   **Finalizes Metadata**: Assigns a unique `event.id` if not present, may update `event.timestamp`.
    *   **Persists to History**: Appends the processed event to the `session.events` list.
4.  **External Yield**: The `Runner` yields (Python) or returns/emits (Java) the processed event outwards to the calling application (e.g., the code that invoked `runner.run_async`).

This flow ensures that state changes and history are consistently recorded alongside the communication content of each event.

### Common Event Examples (Illustrative Patterns)
Here are concise examples of typical events you might see in the stream:

*   **User Input**:
    ```json
    {
        "author": "user",
        "invocation_id": "e-xyz...",
        "content": { "parts": [{ "text": "Book a flight to London for next Tuesday" }]}
        // actions usually empty
    }
    ```
*   **Agent Final Text Response**: (`is_final_response() == True`)
    ```json
    {
        "author": "TravelAgent",
        "invocation_id": "e-xyz...",
        "content": { "parts": [{ "text": "Okay, I can help with that. Could you confirm the departure city?" }]},
        "partial": false,
        "turn_complete": true
        // actions might have state delta, etc.
    }
    ```
*   **Agent Streaming Text Response**: (`is_final_response() == False`)
    ```json
    {
        "author": "SummaryAgent",
        "invocation_id": "e-abc...",
        "content": { "parts": [{ "text": "The document discusses three main points:" }]},
        "partial": true,
        "turn_complete": false
    }
    // ... more partial=True events follow ...
    ```
*   **Tool Call Request (by LLM)**: (`is_final_response() == False`)
    ```json
    {
        "author": "TravelAgent",
        "invocation_id": "e-xyz...",
        "content": { "parts": [{ "function_call": { "name": "find_airports", "args": { "city": "London" }}}]}
        // actions usually empty
    }
    ```
*   **Tool Result Provided (to LLM)**: (`is_final_response()` depends on `skip_summarization`)
    ```json
    {
        "author": "TravelAgent", // Author is agent that requested the call
        "invocation_id": "e-xyz...",
        "content": {
            "role": "user", // Role for LLM history
            "parts": [{ "function_response": { "name": "find_airports", "response": { "result": ["LHR", "LGW", "STN"]}}}]
        }
        // actions might have skip_summarization=True
    }
    ```
*   **State/Artifact Update Only**: (`is_final_response() == False`)
    ```json
    {
        "author": "InternalUpdater",
        "invocation_id": "e-def...",
        "content": null,
        "actions": {
            "state_delta": { "user_status": "verified" },
            "artifact_delta": { "verification_doc.pdf": 2 }
        }
    }
    ```
*   **Agent Transfer Signal**: (`is_final_response() == False`)
    ```json
    {
        "author": "OrchestratorAgent",
        "invocation_id": "e-789...",
        "content": { "parts": [{ "function_call": { "name": "transfer_to_agent", "args": { "agent_name": "BillingAgent" }}}]},
        "actions": { "transfer_to_agent": "BillingAgent" } // Added by framework
    }
    ```
*   **Loop Escalation Signal**: (`is_final_response() == False`)
    ```json
    {
        "author": "CheckerAgent",
        "invocation_id": "e-loop...",
        "content": { "parts": [{ "text": "Maximum retries reached." }]}, // Optional content
        "actions": { "escalate": true }
    }
    ```

### Additional Context and Event Details
Beyond the core concepts, here are a few specific details about context and events that are important for certain use cases:

*   **`ToolContext.function_call_id` (Linking Tool Actions)**: When an LLM requests a tool (FunctionCall), that request has an ID. The `ToolContext` provided to your tool function includes this `function_call_id`.
    *   **Importance**: This ID is crucial for linking actions like authentication back to the specific tool request that initiated them, especially if multiple tools are called in one turn. The framework uses this ID internally.
*   **How State/Artifact Changes are Recorded**: When you modify state or save an artifact using `CallbackContext` or `ToolContext`, these changes aren't immediately written to persistent storage. Instead, they populate the `state_delta` and `artifact_delta` fields within the `EventActions` object. This `EventActions` object is attached to the next event generated after the change (e.g., the agent's response or a tool result event). The `SessionService.append_event` method reads these deltas from the incoming event and applies them to the session's persistent state and artifact records. This ensures changes are tied chronologically to the event stream.
*   **State Scope Prefixes (`app:`, `user:`, `temp:`)**: When managing state via `context.state`, you can optionally use prefixes:
    *   `app:my_setting`: Suggests state relevant to the entire application (requires a persistent `SessionService`).
    *   `user:user_preference`: Suggests state relevant to the specific user across sessions (requires a persistent `SessionService`).
    *   `temp:intermediate_result` or no prefix: Typically session-specific or temporary state for the current invocation.
    The underlying `SessionService` determines how these prefixes are handled for persistence.
*   **Error Events**: An `Event` can represent an error. Check the `event.error_code` and `event.error_message` fields (inherited from `LlmResponse`). Errors might originate from the LLM (e.g., safety filters, resource limits) or potentially be packaged by the framework if a tool fails critically. Check tool `FunctionResponse` content for typical tool-specific errors.
    ```json
    // Example Error Event (conceptual)
    {
        "author": "LLMAgent",
        "invocation_id": "e-err...",
        "content": null,
        "error_code": "SAFETY_FILTER_TRIGGERED",
        "error_message": "Response blocked due to safety settings.",
        "actions": {}
    }
    ```

These details provide a more complete picture for advanced use cases involving tool authentication, state persistence scope, and error handling within the event stream.

### Best Practices for Working with Events
To use events effectively in your ADK applications:

*   **Clear Authorship**: When building custom agents, ensure correct attribution for agent actions in the history. The framework generally handles authorship correctly for LLM/tool events.
    *   Python: Use `yield Event(author=self.name, ...)` in `BaseAgent` subclasses.
    *   Java: When constructing an `Event` in your custom agent logic, set the author, for example: `Event.builder().author(this.getAgentName()) /* ... */ .build();`
*   **Semantic Content & Actions**: Use `event.content` for the core message/data (text, function call/response). Use `event.actions` specifically for signaling side effects (state/artifact deltas) or control flow (`transfer`, `escalate`, `skip_summarization`).
*   **Idempotency Awareness**: Understand that the `SessionService` is responsible for applying the state/artifact changes signaled in `event.actions`. While ADK services aim for consistency, consider potential downstream effects if your application logic re-processes events.
*   **Use `is_final_response()`**: Rely on this helper method in your application/UI layer to identify complete, user-facing text responses. Avoid manually replicating its logic.
*   **Leverage History**: The session's event list is your primary debugging tool. Examine the sequence of authors, content, and actions to trace execution and diagnose issues.
*   **Use Metadata**: Use `invocation_id` to correlate all events within a single user interaction. Use `event.id` to reference specific, unique occurrences.

Treating events as structured messages with clear purposes for their content and actions is key to building, debugging, and managing complex agent behaviors in ADK.

## 5. Sessions and Context
### Introduction to Conversational Context: Session, State, and Memory
Meaningful, multi-turn conversations require agents to understand context. Just like humans, they need to recall the conversation history: what's been said and done to maintain continuity and avoid repetition. The Agent Development Kit (ADK) provides structured ways to manage this context through `Session`, `State`, and `Memory`.

#### Core Concepts
Think of different instances of your conversations with the agent as distinct **conversation threads**, potentially drawing upon **long-term knowledge**.

*   **`Session`: The Current Conversation Thread**
    *   Represents a single, ongoing interaction between a user and your agent system.
    *   Contains the chronological sequence of messages and actions taken by the agent (referred to `Events`) during that specific interaction.
    *   A `Session` can also hold temporary data (`State`) relevant only during this conversation.
*   **`State` (`session.state`): Data Within the Current Conversation**
    *   Data stored within a specific `Session`.
    *   Used to manage information relevant only to the current, active conversation thread (e.g., items in a shopping cart during this chat, user preferences mentioned in this session).
*   **`Memory`: Searchable, Cross-Session Information**
    *   Represents a store of information that might span multiple past sessions or include external data sources.
    *   It acts as a knowledge base the agent can search to recall information or context beyond the immediate conversation.

#### Managing Context: Services
ADK provides services to manage these concepts:

*   **`SessionService`: Manages the different conversation threads (`Session` objects)**
    *   Handles the lifecycle: creating, retrieving, updating (appending `Events`, modifying `State`), and deleting individual `Session`s.
*   **`MemoryService`: Manages the Long-Term Knowledge Store (`Memory`)**
    *   Handles ingesting information (often from completed `Session`s) into the long-term store.
    *   Provides methods to search this stored knowledge based on queries.
*   **Implementations**: ADK offers different implementations for both `SessionService` and `MemoryService`, allowing you to choose the storage backend that best fits your application's needs. Notably, in-memory implementations are provided for both services; these are designed specifically for local testing and fast development. It's important to remember that all data stored using these in-memory options (sessions, state, or long-term knowledge) is lost when your application restarts. For persistence and scalability beyond local testing, ADK also offers cloud-based and database service options.

**In Summary:**
*   **`Session` & `State`**: Focus on the current interaction – the history and data of the single, active conversation. Managed primarily by a `SessionService`.
*   **`Memory`**: Focuses on the past and external information – a searchable archive potentially spanning across conversations. Managed by a `MemoryService`.

### Session: Tracking Individual Conversations
Following our Introduction, let's dive into the `Session`. Think back to the idea of a "conversation thread." Just like you wouldn't start every text message from scratch, agents need context regarding the ongoing interaction. `Session` is the ADK object designed specifically to track and manage these individual conversation threads.

#### The Session Object
When a user starts interacting with your agent, the `SessionService` creates a `Session` object (`google.adk.sessions.Session`). This object acts as the container holding everything related to that one specific chat thread. Here are its key properties:
*   **Identification (`id`, `appName`, `userId`)**: Unique labels for the conversation.
    *   `id`: A unique identifier for this specific conversation thread, essential for retrieving it later.
    *   `appName`: Identifies which agent application this conversation belongs to.
    *   `userId`: Links the conversation to a particular user.
*   **History (`events`)**: A chronological sequence of all interactions (`Event` objects – user messages, agent responses, tool actions) that have occurred within this specific thread.
*   **Session `State` (`state`)**: A place to store temporary data relevant only to this specific, ongoing conversation. This acts as a scratchpad for the agent during the interaction. We will cover how to use and manage state in detail in the next section.
*   **Activity Tracking (`lastUpdateTime`)**: A timestamp indicating the last time an event occurred in this conversation thread.

**Example: Examining Session Properties (Python)**
```python
from google.adk.sessions import InMemorySessionService, Session
import asyncio # Needed for async create_session

async def examine_session():
    # Create a simple session to examine its properties
    temp_service = InMemorySessionService()
    example_session = await temp_service.create_session(
        app_name="my_app",
        user_id="example_user",
        state={"initial_key": "initial_value"}  # State can be initialized
    )

    print("--- Examining Session Properties ---")
    print(f"ID (`id`): {example_session.id}")
    print(f"Application Name (`app_name`): {example_session.app_name}")
    print(f"User ID (`user_id`): {example_session.user_id}")
    print(f"State (`state`): {example_session.state}")  # Note: Only shows initial state here
    print(f"Events (`events`): {example_session.events}")  # Initially empty
    print(f"Last Update (`last_update_time`): {example_session.last_update_time:.2f}")
    print("---------------------------------")

    # Clean up (optional for this example)
    # Note: delete_session in Python ADK returns a boolean or None, not the service instance.
    await temp_service.delete_session(
        app_name=example_session.app_name,
        user_id=example_session.user_id,
        session_id=example_session.id
    )
    print("Session deleted.")

# asyncio.run(examine_session()) # Run in a script
```
**Example: Examining Session Properties (Java)**
```java
import com.google.adk.sessions.InMemorySessionService;
import com.google.adk.sessions.Session;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;


String sessionId = "123";
String appName = "example-app"; // Example app name
String userId = "example-user"; // Example user id
ConcurrentMap<String, Object> initialState = new ConcurrentHashMap<>(Map.of("newKey", "newValue"));

InMemorySessionService exampleSessionService = new InMemorySessionService();
// Create Session
Session exampleSession = exampleSessionService.createSession(appName, userId, initialState, Optional.of(sessionId)).blockingGet();

System.out.println("Session created successfully.");
System.out.println("--- Examining Session Properties ---");
System.out.printf("ID (`id`): %s%n", exampleSession.id());
System.out.printf("Application Name (`appName`): %s%n", exampleSession.appName());
System.out.printf("User ID (`userId`): %s%n", exampleSession.userId());
System.out.printf("State (`state`): %s%n", exampleSession.state());
System.out.println("------------------------------------");

// Clean up (optional for this example)
exampleSessionService.deleteSession(appName, userId, sessionId).blockingGet(); // Corrected: deleteSession returns Completable
```
(Note: The `state` shown above is only the initial state. State updates happen via events, as discussed in the State section.)

#### Managing Sessions with a `SessionService`
As seen above, you don't typically create or manage `Session` objects directly. Instead, you use a `SessionService`. This service acts as the central manager responsible for the entire lifecycle of your conversation sessions.
Its core responsibilities include:
*   Starting New Conversations: Creating fresh `Session` objects when a user begins an interaction.
*   Resuming Existing Conversations: Retrieving a specific `Session` (using its ID) so the agent can continue where it left off.
*   Saving Progress: Appending new interactions (`Event` objects) to a session's history. This is also the mechanism through which session `state` gets updated (more in the State section).
*   Listing Conversations: Finding the active session threads for a particular user and application.
*   Cleaning Up: Deleting `Session` objects and their associated data when conversations are finished or no longer needed.

#### `SessionService` Implementations
ADK provides different `SessionService` implementations, allowing you to choose the storage backend that best suits your needs:

*   **`InMemorySessionService`**
    *   **How it works**: Stores all session data directly in the application's memory.
    *   **Persistence**: None. All conversation data is lost if the application restarts.
    *   **Requires**: Nothing extra.
    *   **Best for**: Quick development, local testing, examples, and scenarios where long-term persistence isn't required.
    ```python
    from google.adk.sessions import InMemorySessionService
    session_service = InMemorySessionService()
    ```
    ```java
    import com.google.adk.sessions.InMemorySessionService;
    InMemorySessionService exampleSessionService = new InMemorySessionService();
    ```
*   **`VertexAiSessionService`**
    *   **How it works**: Uses Google Cloud's Vertex AI infrastructure via API calls for session management.
    *   **Persistence**: Yes. Data is managed reliably and scalably via Vertex AI Agent Engine.
    *   **Requires**:
        *   A Google Cloud project (`pip install vertexai`)
        *   A Google Cloud storage bucket that can be configured by this step.
        *   A Reasoning Engine resource name/ID that can setup following this tutorial.
    *   **Best for**: Scalable production applications deployed on Google Cloud, especially when integrating with other Vertex AI features.
    ```python
    # Requires: pip install google-adk[vertexai]
    # Plus GCP setup and authentication
    from google.adk.sessions import VertexAiSessionService

    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "us-central1"
    # The app_name used with this service should be the Reasoning Engine ID or name
    REASONING_ENGINE_APP_NAME = "projects/your-gcp-project-id/locations/us-central1/reasoningEngines/your-engine-id"

    session_service = VertexAiSessionService(project=PROJECT_ID, location=LOCATION)
    # Use REASONING_ENGINE_APP_NAME when calling service methods, e.g.:
    # session = await session_service.create_session(app_name=REASONING_ENGINE_APP_NAME, ...)
    ```
    ```java
    // Please look at the set of requirements above, consequently export the following in your bashrc file:
    // export GOOGLE_CLOUD_PROJECT=my_gcp_project
    // export GOOGLE_CLOUD_LOCATION=us-central1
    // export GOOGLE_API_KEY=my_api_key
    import com.google.adk.sessions.VertexAiSessionService;
    import com.google.adk.sessions.Session;
    import java.util.UUID;
    import java.util.Optional;
    import java.util.concurrent.ConcurrentHashMap;

    String sessionId = UUID.randomUUID().toString();
    String reasoningEngineAppName = "123456789"; // Example Engine ID
    String userId = "u_123"; // Example user id
    ConcurrentHashMap<String, Object> initialState = new ConcurrentHashMap<>(); // No initial state needed for this example

    VertexAiSessionService sessionService = new VertexAiSessionService();
    Session mySession = sessionService.createSession(reasoningEngineAppName, userId, initialState, Optional.of(sessionId)).blockingGet();
    ```
*   **`DatabaseSessionService`** (Python Only)
    *   **How it works**: Connects to a relational database (e.g., PostgreSQL, MySQL, SQLite) to store session data persistently in tables.
    *   **Persistence**: Yes. Data survives application restarts.
    *   **Requires**: A configured database.
    *   **Best for**: Applications needing reliable, persistent storage that you manage yourself.
    ```python
    from google.adk.sessions import DatabaseSessionService
    # Example using a local SQLite file:
    db_url = "sqlite:///./my_agent_data.db"
    session_service = DatabaseSessionService(db_url=db_url)
    ```
Choosing the right `SessionService` is key to defining how your agent's conversation history and temporary data are stored and persist.

#### The Session Lifecycle
Here’s a simplified flow of how `Session` and `SessionService` work together during a conversation turn:
1.  **Start or Resume**: Your application's `Runner` uses the `SessionService` to either `create_session` (for a new chat) or `get_session` (to retrieve an existing one).
2.  **Context Provided**: The `Runner` gets the appropriate `Session` object from the appropriate service method, providing the agent with access to the corresponding `Session`'s `state` and `events`.
3.  **Agent Processing**: The user prompts the agent with a query. The agent analyzes the query and potentially the session `state` and `events` history to determine the response.
4.  **Response & State Update**: The agent generates a response (and potentially flags data to be updated in the `state`). The `Runner` packages this as an `Event`.
5.  **Save Interaction**: The `Runner` calls `sessionService.append_event(session, event)` with the session and the new event as the arguments. The service adds the `Event` to the history and updates the session's `state` in storage based on information within the event. The session's `last_update_time` also get updated.
6.  **Ready for Next**: The agent's response goes to the user. The updated `Session` is now stored by the `SessionService`, ready for the next turn (which restarts the cycle at step 1, usually with the continuation of the conversation in the current session).
7.  **End Conversation**: When the conversation is over, your application calls `sessionService.delete_session(...)` to clean up the stored session data if it is no longer required.

This cycle highlights how the `SessionService` ensures conversational continuity by managing the history and state associated with each `Session` object.

### State: The Session's Scratchpad
Within each `Session` (our conversation thread), the `state` attribute acts like the agent's dedicated scratchpad for that specific interaction. While `session.events` holds the full history, `session.state` is where the agent stores and updates dynamic details needed during the conversation.

#### What is `session.state`?
Conceptually, `session.state` is a collection (dictionary or Map) holding key-value pairs. It's designed for information the agent needs to recall or track to make the current conversation effective:
*   **Personalize Interaction**: Remember user preferences mentioned earlier (e.g., `'user_preference_theme': 'dark'`).
*   **Track Task Progress**: Keep tabs on steps in a multi-turn process (e.g., `'booking_step': 'confirm_payment'`).
*   **Accumulate Information**: Build lists or summaries (e.g., `'shopping_cart_items': ['book', 'pen']`).
*   **Make Informed Decisions**: Store flags or values influencing the next response (e.g., `'user_is_authenticated': True`).

#### Key Characteristics of State
*   **Structure: Serializable Key-Value Pairs**
    *   Data is stored as `key: value`.
    *   Keys: Always strings (`str`). Use clear names (e.g., `'departure_city'`, `'user:language_preference'`).
    *   Values: Must be serializable. This means they can be easily saved and loaded by the `SessionService`. Stick to basic types in the specific languages (Python/ Java) like strings, numbers, booleans, and simple lists or dictionaries containing only these basic types. (See API documentation for precise details).
    *   ⚠️ **Avoid Complex Objects**: Do not store non-serializable objects (custom class instances, functions, connections, etc.) directly in the state. Store simple identifiers if needed, and retrieve the complex object elsewhere.
*   **Mutability: It Changes**
    *   The contents of the `state` are expected to change as the conversation evolves.
*   **Persistence: Depends on `SessionService`**
    *   Whether state survives application restarts depends on your chosen service:
        *   `InMemorySessionService`: Not Persistent. State is lost on restart.
        *   `DatabaseSessionService` / `VertexAiSessionService`: Persistent. State is saved reliably.

**Note**: The specific parameters or method names for the primitives may vary slightly by SDK language (e.g., `session.state['current_intent'] = 'book_flight'` in Python, `session.state().put("current_intent", "book_flight)` in Java). Refer to the language-specific API documentation for details.

#### Organizing State with Prefixes: Scope Matters
Prefixes on state keys define their scope and persistence behavior, especially with persistent services:
*   **No Prefix (Session State)**:
    *   **Scope**: Specific to the current session (`id`).
    *   **Persistence**: Only persists if the `SessionService` is persistent (`Database`, `VertexAI`).
    *   **Use Cases**: Tracking progress within the current task (e.g., `'current_booking_step'`), temporary flags for this interaction (e.g., `'needs_clarification'`).
    *   **Example**: `session.state['current_intent'] = 'book_flight'`
*   **`user:` Prefix (User State)**:
    *   **Scope**: Tied to the `user_id`, shared across all sessions for that user (within the same `app_name`).
    *   **Persistence**: Persistent with `Database` or `VertexAI`. (Stored by `InMemory` but lost on restart).
    *   **Use Cases**: User preferences (e.g., `'user:theme'`), profile details (e.g., `'user:name'`).
    *   **Example**: `session.state['user:preferred_language'] = 'fr'`
*   **`app:` Prefix (App State)**:
    *   **Scope**: Tied to the `app_name`, shared across all users and sessions for that application.
    *   **Persistence**: Persistent with `Database` or `VertexAI`. (Stored by `InMemory` but lost on restart).
    *   **Use Cases**: Global settings (e.g., `'app:api_endpoint'`), shared templates.
    *   **Example**: `session.state['app:global_discount_code'] = 'SAVE10'`
*   **`temp:` Prefix (Temporary Session State)**:
    *   **Scope**: Specific to the current session processing turn.
    *   **Persistence**: Never Persistent. Guaranteed to be discarded, even with persistent services.
    *   **Use Cases**: Intermediate results needed only immediately, data you explicitly don't want stored.
    *   **Example**: `session.state['temp:raw_api_response'] = {...}`

**How the Agent Sees It**: Your agent code interacts with the combined state through the single `session.state` collection (dict/Map). The `SessionService` handles fetching/merging state from the correct underlying storage based on prefixes.

#### How State is Updated: Recommended Methods
State should always be updated as part of adding an `Event` to the session history using `session_service.append_event()`. This ensures changes are tracked, persistence works correctly, and updates are thread-safe.

1.  **The Easy Way: `output_key` (for Agent Text Responses)**
    This is the simplest method for saving an agent's final text response directly into the state. When defining your `LlmAgent`, specify the `output_key`:
    **Python Example:**
    ```python
    from google.adk.agents import LlmAgent
    from google.adk.sessions import InMemorySessionService, Session
    from google.adk.runners import Runner
    from google.genai.types import Content, Part
    import asyncio

    # Define agent with output_key
    greeting_agent = LlmAgent(
        name="Greeter",
        model="gemini-2.0-flash",  # Use a valid model
        instruction="Generate a short, friendly greeting.",
        output_key="last_greeting"  # Save response to state['last_greeting']
    )

    async def main_state_output_key():
        # --- Setup Runner and Session ---
        app_name, user_id, session_id = "state_app", "user1", "session1"
        session_service = InMemorySessionService()
        runner = Runner(
            agent=greeting_agent,
            app_name=app_name,
            session_service=session_service
        )
        session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        print(f"Initial state: {session.state}")

        # --- Run the Agent ---
        # Runner handles calling append_event, which uses the output_key
        # to automatically create the state_delta.
        user_message = Content(parts=[Part(text="Hello")])
        # Assuming runner.run is synchronous for simplicity here.
        # If it's async, this loop should be awaited.
        for event in runner.run(user_id=user_id, session_id=session_id, new_message=user_message):
            if event.is_final_response():
                print("Agent responded.")
                # Response text is also in event.content

        # --- Check Updated State ---
        updated_session = await session_service.get_session(
            app_name=app_name, # Corrected: use app_name
            user_id=user_id,   # Corrected: use user_id
            session_id=session_id
        )
        print(f"State after agent run: {updated_session.state}")
        # Expected output might include: {'last_greeting': 'Hello there! How can I help you today?'}

    # asyncio.run(main_state_output_key())
    ```
    **Java Example:**
    ```java
    import com.google.adk.agents.LlmAgent;
    import com.google.adk.agents.RunConfig;
    import com.google.adk.events.Event;
    import com.google.adk.runner.Runner;
    import com.google.adk.sessions.InMemorySessionService;
    import com.google.adk.sessions.Session;
    import com.google.genai.types.Content;
    import com.google.genai.types.Part;
    import java.util.List;
    import java.util.Optional;

    public class GreetingAgentExample {
        public static void main(String[] args) {
            // Define agent with output_key
            LlmAgent greetingAgent = LlmAgent.builder()
                .name("Greeter")
                .model("gemini-2.0-flash")
                .instruction("Generate a short, friendly greeting.")
                .description("Greeting agent")
                .outputKey("last_greeting") // Save response to state.get("last_greeting")
                .build();

            // --- Setup Runner and Session ---
            String appName = "state_app";
            String userId = "user1";
            String sessionId = "session1";
            InMemorySessionService sessionService = new InMemorySessionService();
            Runner runner = new Runner(greetingAgent, appName, null, sessionService); // artifactService can be null

            Session session = sessionService.createSession(appName, userId, null, sessionId).blockingGet();
            System.out.println("Initial state: " + session.state().entrySet());

            // --- Run the Agent ---
            Content userMessage = Content.builder().parts(List.of(Part.fromText("Hello"))).build();
            RunConfig runConfig = RunConfig.builder().build(); // RunConfig might be needed

            for (Event event : runner.runAsync(userId, sessionId, userMessage, runConfig).blockingIterable()) {
                if (event.finalResponse()) {
                    System.out.println("Agent responded.");
                }
            }

            // --- Check Updated State ---
            Session updatedSession = sessionService.getSession(appName, userId, sessionId, Optional.empty()).blockingGet();
            assert updatedSession != null;
            System.out.println("State after agent run: " + updatedSession.state().entrySet());
        }
    }
    ```
    Behind the scenes, the `Runner` uses the `output_key` to create the necessary `EventActions` with a `state_delta` and calls `append_event`.

2.  **The Standard Way: `EventActions.state_delta` (for Complex Updates)**
    For more complex scenarios (updating multiple keys, non-string values, specific scopes like `user:` or `app:`, or updates not tied directly to the agent's final text), you manually construct the `state_delta` within `EventActions`.
    **Python Example:**
    ```python
    from google.adk.sessions import InMemorySessionService, Session
    from google.adk.events import Event, EventActions
    from google.genai.types import Part, Content
    import time
    import asyncio

    async def main_manual_state():
        # --- Setup ---
        session_service = InMemorySessionService()
        app_name, user_id, session_id = "state_app_manual", "user2", "session2"
        session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state={"user:login_count": 0, "task_status": "idle"}
        )
        print(f"Initial state: {session.state}")

        # --- Define State Changes ---
        current_time = time.time()
        state_changes = {
            "task_status": "active",  # Update session state
            "user:login_count": session.state.get("user:login_count", 0) + 1,  # Update user state
            "user:last_login_ts": current_time,  # Add user state
            "temp:validation_needed": True  # Add temporary state (will be discarded)
        }

        # --- Create Event with Actions ---
        actions_with_update = EventActions(state_delta=state_changes)
        # This event might represent an internal system action, not just an agent response
        system_event = Event(
            invocation_id="inv_login_update",
            author="system",  # Or 'agent', 'tool' etc.
            actions=actions_with_update,
            timestamp=current_time
            # content might be None or represent the action taken
        )

        # --- Append the Event (This updates the state) ---
        await session_service.append_event(session, system_event)
        print("`append_event` called with explicit state delta.")

        # --- Check Updated State ---
        updated_session = await session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        print(f"State after event: {updated_session.state}")
        # Expected: {'user:login_count': 1, 'task_status': 'active', 'user:last_login_ts': <timestamp>}
        # Note: 'temp:validation_needed' is NOT present.

    # asyncio.run(main_manual_state())
    ```
    **Java Example:**
    ```java
    import com.google.adk.events.Event;
    import com.google.adk.events.EventActions;
    import com.google.adk.sessions.InMemorySessionService;
    import com.google.adk.sessions.Session;
    import java.time.Instant;
    import java.util.Optional;
    import java.util.concurrent.ConcurrentHashMap;
    import java.util.concurrent.ConcurrentMap;

    public class ManualStateUpdateExample {
        public static void main(String[] args) {
            // --- Setup ---
            InMemorySessionService sessionService = new InMemorySessionService();
            String appName = "state_app_manual";
            String userId = "user2";
            String sessionId = "session2";
            ConcurrentMap<String, Object> initialState = new ConcurrentHashMap<>();
            initialState.put("user:login_count", 0);
            initialState.put("task_status", "idle");

            Session session = sessionService.createSession(appName, userId, initialState, sessionId).blockingGet();
            System.out.println("Initial state: " + session.state().entrySet());

            // --- Define State Changes ---
            long currentTimeMillis = Instant.now().toEpochMilli();
            ConcurrentMap<String, Object> stateChanges = new ConcurrentHashMap<>();
            stateChanges.put("task_status", "active");

            Object loginCountObj = session.state().get("user:login_count");
            int currentLoginCount = 0;
            if (loginCountObj instanceof Number) {
                currentLoginCount = ((Number) loginCountObj).intValue();
            }
            stateChanges.put("user:login_count", currentLoginCount + 1);
            stateChanges.put("user:last_login_ts", currentTimeMillis);
            stateChanges.put("temp:validation_needed", true);

            // --- Create Event with Actions ---
            EventActions actionsWithUpdate = EventActions.builder().stateDelta(stateChanges).build();
            Event systemEvent = Event.builder()
                .invocationId("inv_login_update")
                .author("system")
                .actions(actionsWithUpdate)
                .timestamp(currentTimeMillis)
                .id(Event.generateEventId()) // Ensure event has an ID
                .build();

            // --- Append the Event (This updates the state) ---
            sessionService.appendEvent(session, systemEvent).blockingGet();
            System.out.println("`appendEvent` called with explicit state delta.");

            // --- Check Updated State ---
            Session updatedSession = sessionService.getSession(appName, userId, sessionId, Optional.empty()).blockingGet();
            assert updatedSession != null;
            System.out.println("State after event: " + updatedSession.state().entrySet());
        }
    }
    ```
    What `append_event` Does:
    1.  Adds the `Event` to `session.events`.
    2.  Reads the `state_delta` from the event's `actions`.
    3.  Applies these changes to the state managed by the `SessionService`, correctly handling prefixes and persistence based on the service type.
    4.  Updates the session's `last_update_time`.
    5.  Ensures thread-safety for concurrent updates.

#### ⚠️ A Warning About Direct State Modification
Avoid directly modifying the `session.state` dictionary after retrieving a session (e.g., `retrieved_session.state['key'] = value`).
**Why this is strongly discouraged**:
*   **Bypasses Event History**: The change isn't recorded as an `Event`, losing auditability.
*   **Breaks Persistence**: Changes made this way will likely NOT be saved by `DatabaseSessionService` or `VertexAiSessionService`. They rely on `append_event` to trigger saving.
*   **Not Thread-Safe**: Can lead to race conditions and lost updates.
*   **Ignores Timestamps/Logic**: Doesn't update `last_update_time` or trigger related event logic.

**Recommendation**: Stick to updating state via `output_key` or `EventActions.state_delta` within the `append_event` flow for reliable, trackable, and persistent state management. Use direct access only for *reading* state.

#### Best Practices for State Design Recap
*   **Minimalism**: Store only essential, dynamic data.
*   **Serialization**: Use basic, serializable types.
*   **Descriptive Keys & Prefixes**: Use clear names and appropriate prefixes (`user:`, `app:`, `temp:`, or none).
*   **Shallow Structures**: Avoid deep nesting where possible.
*   **Standard Update Flow**: Rely on `append_event`.

### Memory: Long-Term Knowledge with `MemoryService`
We've seen how `Session` tracks the history (`events`) and temporary data (`state`) for a single, ongoing conversation. But what if an agent needs to recall information from past conversations or access external knowledge bases? This is where the concept of Long-Term Knowledge and the `MemoryService` come into play.

Think of it this way:
*   `Session` / `State`: Like your short-term memory during one specific chat.
*   Long-Term Knowledge (`MemoryService`): Like a searchable archive or knowledge library the agent can consult, potentially containing information from many past chats or other sources.

#### The `MemoryService` Role
The `BaseMemoryService` defines the interface for managing this searchable, long-term knowledge store. Its primary responsibilities are:
*   **Ingesting Information (`add_session_to_memory`)**: Taking the contents of a (usually completed) `Session` and adding relevant information to the long-term knowledge store.
*   **Searching Information (`search_memory`)**: Allowing an agent (typically via a `Tool`) to query the knowledge store and retrieve relevant snippets or context based on a search query.

#### `MemoryService` Implementations
ADK provides different ways to implement this long-term knowledge store:

*   **`InMemoryMemoryService`** (Python only for now)
    *   **How it works**: Stores session information in the application's memory and performs basic keyword matching for searches.
    *   **Persistence**: None. All stored knowledge is lost if the application restarts.
    *   **Requires**: Nothing extra.
    *   **Best for**: Prototyping, simple testing, scenarios where only basic keyword recall is needed and persistence isn't required.
    ```python
    from google.adk.memory import InMemoryMemoryService
    memory_service = InMemoryMemoryService()
    ```
*   **`VertexAiRagMemoryService`** (Python only for now)
    *   **How it works**: Leverages Google Cloud's Vertex AI RAG (Retrieval-Augmented Generation) service. It ingests session data into a specified RAG Corpus and uses powerful semantic search capabilities for retrieval.
    *   **Persistence**: Yes. The knowledge is stored persistently within the configured Vertex AI RAG Corpus.
    *   **Requires**: A Google Cloud project, appropriate permissions, necessary SDKs (`pip install google-adk[vertexai]`), and a pre-configured Vertex AI RAG Corpus resource name/ID.
    *   **Best for**: Production applications needing scalable, persistent, and semantically relevant knowledge retrieval, especially when deployed on Google Cloud.
    ```python
    # Requires: pip install google-adk[vertexai]
    # Plus GCP setup, RAG Corpus, and authentication
    from google.adk.memory import VertexAiRagMemoryService

    # The RAG Corpus name or ID
    RAG_CORPUS_RESOURCE_NAME = "projects/your-gcp-project-id/locations/us-central1/ragCorpora/your-corpus-id"
    # Optional configuration for retrieval
    SIMILARITY_TOP_K = 5
    VECTOR_DISTANCE_THRESHOLD = 0.7

    memory_service = VertexAiRagMemoryService(
        rag_corpus=RAG_CORPUS_RESOURCE_NAME,
        similarity_top_k=SIMILARITY_TOP_K,
        vector_distance_threshold=VECTOR_DISTANCE_THRESHOLD
    )
    ```

#### How Memory Works in Practice
The typical workflow involves these steps:
1.  **Session Interaction**: A user interacts with an agent via a `Session`, managed by a `SessionService`. `Events` are added, and `state` might be updated.
2.  **Ingestion into Memory**: At some point (often when a session is considered complete or has yielded significant information), your application calls `memory_service.add_session_to_memory(session)`. This extracts relevant information from the session's events and adds it to the long-term knowledge store (in-memory dictionary or RAG Corpus).
3.  **Later Query**: In a different (or the same) session, the user might ask a question requiring past context (e.g., "What did we discuss about project X last week?").
4.  **Agent Uses Memory Tool**: An agent equipped with a memory-retrieval tool (like the built-in `load_memory` tool) recognizes the need for past context. It calls the tool, providing a search query (e.g., "discussion project X last week").
5.  **Search Execution**: The tool internally calls `memory_service.search_memory(app_name, user_id, query)`.
6.  **Results Returned**: The `MemoryService` searches its store (using keyword matching or semantic search) and returns relevant snippets as a `SearchMemoryResponse` containing a list of `MemoryResult` objects (each potentially holding events from a relevant past session).
7.  **Agent Uses Results**: The tool returns these results to the agent, usually as part of the context or function response. The agent can then use this retrieved information to formulate its final answer to the user.

**Example: Adding and Searching Memory (Python)**
This example demonstrates the basic flow using the `InMemory` services for simplicity.
```python
import asyncio
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService, Session
from google.adk.memory import InMemoryMemoryService # Import MemoryService
from google.adk.runners import Runner
from google.adk.tools import load_memory # Tool to query memory
from google.genai.types import Content, Part

# --- Constants ---
APP_NAME = "memory_example_app"
USER_ID = "mem_user"
MODEL = "gemini-2.0-flash"  # Use a valid model

async def memory_example():
    # --- Agent Definitions ---
    # Agent 1: Simple agent to capture information
    info_capture_agent = LlmAgent(
        model=MODEL,
        name="InfoCaptureAgent",
        instruction="Acknowledge the user's statement."
    )

    # Agent 2: Agent that can use memory
    memory_recall_agent = LlmAgent(
        model=MODEL,
        name="MemoryRecallAgent",
        instruction="Answer the user's question. Use the 'load_memory' tool "
                    "if the answer might be in past conversations.",
        tools=[load_memory]  # Give the agent the tool
    )

    # --- Services and Runner ---
    session_service = InMemorySessionService()
    memory_service_instance = InMemoryMemoryService() # Use instance name
    runner = Runner(
        agent=info_capture_agent, # Start with the info capture agent
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service_instance # Provide the memory service to the Runner
    )

    # --- Scenario ---
    # Turn 1: Capture some information in a session
    print("--- Turn 1: Capturing Information ---")
    session1_id = "session_info"
    session1 = await runner.session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session1_id
    )
    user_input1 = Content(parts=[Part(text="My favorite project is Project Alpha.")], role="user")

    final_response_text = "(No final response)"
    async for event in runner.run_async(user_id=USER_ID, session_id=session1_id, new_message=user_input1):
        if event.is_final_response() and event.content and event.content.parts:
            final_response_text = event.content.parts[0].text
    print(f"Agent 1 Response: {final_response_text}")

    completed_session1 = await runner.session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session1_id
    )
    print("\n--- Adding Session 1 to Memory ---")
    await memory_service_instance.add_session_to_memory(completed_session1) # Use instance
    print("Session added to memory.")

    # Turn 2: In a *new* (or same) session, ask a question requiring memory
    print("\n--- Turn 2: Recalling Information ---")
    session2_id = "session_recall" # Can be same or different session ID
    session2 = await runner.session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session2_id
    )

    runner.agent = memory_recall_agent # Switch runner to the recall agent
    user_input2 = Content(parts=[Part(text="What is my favorite project?")], role="user")

    print("Running MemoryRecallAgent...")
    final_response_text_2 = "(No final response)"
    async for event in runner.run_async(user_id=USER_ID, session_id=session2_id, new_message=user_input2):
        print(f"  Event: {event.author} - Type: {'Text' if event.content and event.content.parts and event.content.parts[0].text else ''} "
              f"{'FuncCall' if event.get_function_calls() else ''} "
              f"{'FuncResp' if event.get_function_responses() else ''}")
        if event.is_final_response() and event.content and event.content.parts:
            final_response_text_2 = event.content.parts[0].text
            print(f"Agent 2 Final Response: {final_response_text_2}")
            break # Stop after final response

# asyncio.run(memory_example())
```

## 6. Artifacts
In ADK, Artifacts represent a crucial mechanism for managing named, versioned binary data associated either with a specific user interaction session or persistently with a user across multiple sessions. They allow your agents and tools to handle data beyond simple text strings, enabling richer interactions involving files, images, audio, and other binary formats.

**Note**: The specific parameters or method names for the primitives may vary slightly by SDK language (e.g., `save_artifact` in Python, `saveArtifact` in Java). Refer to the language-specific API documentation for details.

### What are Artifacts?
*   **Definition**: An Artifact is essentially a piece of binary data (like the content of a file) identified by a unique `filename` string within a specific scope (session or user). Each time you save an artifact with the same filename, a new version is created.
*   **Representation**: Artifacts are consistently represented using the standard `google.genai.types.Part` object. The core data is typically stored within an `inline_data` structure of the `Part` (accessed via `inline_data`), which itself contains:
    *   `data`: The raw binary content as bytes.
    *   `mime_type`: A string indicating the type of the data (e.g., `"image/png"`, `"application/pdf"`). This is essential for correctly interpreting the data later.
    **Python Example:**
    ```python
    import google.genai.types as types
    # Assume 'image_bytes' contains the binary data of a PNG image
    image_bytes = b'\x89PNG\r\n\x1a\n...'  # Placeholder
    image_artifact = types.Part(
        inline_data=types.Blob(mime_type="image/png", data=image_bytes)
    )
    # You can also use the convenience constructor:
    # image_artifact_alt = types.Part.from_data(data=image_bytes, mime_type="image/png")
    print(f"Artifact MIME Type: {image_artifact.inline_data.mime_type}")
    print(f"Artifact Data (first 10 bytes): {image_artifact.inline_data.data[:10]}...")
    ```
    **Java Example:**
    ```java
    import com.google.genai.types.Part;
    import com.google.genai.types.Blob; // For Blob creation
    import java.nio.charset.StandardCharsets;

    // Assume 'imageBytes' contains the binary data of a PNG image
    byte[] imageBytes = {(byte) 0x89, (byte) 0x50, (byte) 0x4E, (byte) 0x47, /* ... */}; // Placeholder
    // Create an image artifact using Part.fromBytes
    Part imageArtifact = Part.fromBytes(imageBytes, "image/png");
    System.out.println("Artifact MIME Type: " + imageArtifact.inlineData().get().mimeType().get());
    // System.out.println("Artifact Data (first 10 bytes): " + new String(imageArtifact.inlineData().get().data().get(), 0, 10, StandardCharsets.UTF_8) + "...");
    ```
*   **Persistence & Management**: Artifacts are not stored directly within the agent or session state. Their storage and retrieval are managed by a dedicated **Artifact Service** (an implementation of `BaseArtifactService`, defined in `google.adk.artifacts`). ADK provides various implementations, such as:
    *   An in-memory service for testing or temporary storage (e.g., `InMemoryArtifactService` in Python, defined in `google.adk.artifacts.in_memory_artifact_service.py`).
    *   A service for persistent storage using Google Cloud Storage (GCS) (e.g., `GcsArtifactService` in Python, defined in `google.adk.artifacts.gcs_artifact_service.py`).
    The chosen service implementation handles versioning automatically when you save data.

### Why Use Artifacts?
While session `state` is suitable for storing small pieces of configuration or conversational context (like strings, numbers, booleans, or small dictionaries/lists), Artifacts are designed for scenarios involving binary or large data:
*   **Handling Non-Textual Data**: Easily store and retrieve images, audio clips, video snippets, PDFs, spreadsheets, or any other file format relevant to your agent's function.
*   **Persisting Large Data**: Session state is generally not optimized for storing large amounts of data. Artifacts provide a dedicated mechanism for persisting larger blobs without cluttering the session state.
*   **User File Management**: Provide capabilities for users to upload files (which can be saved as artifacts) and retrieve or download files generated by the agent (loaded from artifacts).
*   **Sharing Outputs**: Enable tools or agents to generate binary outputs (like a PDF report or a generated image) that can be saved via `save_artifact` and later accessed by other parts of the application or even in subsequent sessions (if using user namespacing).
*   **Caching Binary Data**: Store the results of computationally expensive operations that produce binary data (e.g., rendering a complex chart image) as artifacts to avoid regenerating them on subsequent requests.

In essence, whenever your agent needs to work with file-like binary data that needs to be persisted, versioned, or shared, Artifacts managed by an `ArtifactService` are the appropriate mechanism within ADK.

### Common Use Cases
Artifacts provide a flexible way to handle binary data within your ADK applications. Here are some typical scenarios where they prove valuable:
*   **Generated Reports/Files**: A tool or agent generates a report (e.g., a PDF analysis, a CSV data export, an image chart).
*   **Handling User Uploads**: A user uploads a file (e.g., an image for analysis, a document for summarization) through a front-end interface.
*   **Storing Intermediate Binary Results**: An agent performs a complex multi-step process where one step generates intermediate binary data (e.g., audio synthesis, simulation results).
*   **Persistent User Data**: Storing user-specific configuration or data that isn't a simple key-value state.
*   **Caching Generated Binary Content**: An agent frequently generates the same binary output based on certain inputs (e.g., a company logo image, a standard audio greeting).

### Core Concepts

#### Artifact Service (`BaseArtifactService`)
*   **Role**: The central component responsible for the actual storage and retrieval logic for artifacts. It defines how and where artifacts are persisted.
*   **Interface**: Defined by the abstract base class `BaseArtifactService`. Any concrete implementation must provide methods for:
    *   **Save Artifact**: Stores the artifact data and returns its assigned version number.
    *   **Load Artifact**: Retrieves a specific version (or the latest) of an artifact.
    *   **List Artifact keys**: Lists the unique filenames of artifacts within a given scope.
    *   **Delete Artifact**: Removes an artifact (and potentially all its versions, depending on implementation).
    *   **List versions**: Lists all available version numbers for a specific artifact filename.
*   **Configuration**: You provide an instance of an artifact service (e.g., `InMemoryArtifactService`, `GcsArtifactService`) when initializing the `Runner`. The `Runner` then makes this service available to agents and tools via the `InvocationContext`.
    **Python Example:**
    ```python
    from google.adk.runners import Runner
    from google.adk.artifacts import InMemoryArtifactService # Or GcsArtifactService
    from google.adk.agents import LlmAgent # Any agent
    from google.adk.sessions import InMemorySessionService

    # Example: Configuring the Runner with an Artifact Service
    my_agent = LlmAgent(name="artifact_user_agent", model="gemini-2.0-flash")
    artifact_service = InMemoryArtifactService()  # Choose an implementation
    session_service = InMemorySessionService()
    runner = Runner(
        agent=my_agent,
        app_name="my_artifact_app",
        session_service=session_service,
        artifact_service=artifact_service  # Provide the service instance here
    )
    # Now, contexts within runs managed by this runner can use artifact methods
    ```
    **Java Example:**
    ```java
    import com.google.adk.agents.LlmAgent;
    import com.google.adk.runner.Runner;
    import com.google.adk.sessions.InMemorySessionService;
    import com.google.adk.artifacts.InMemoryArtifactService; // Or GcsArtifactService

    // Example: Configuring the Runner with an Artifact Service
    LlmAgent myAgent = LlmAgent.builder()
        .name("artifact_user_agent")
        .model("gemini-2.0-flash")
        .build();
    InMemoryArtifactService artifactService = new InMemoryArtifactService(); // Choose an implementation
    InMemorySessionService sessionService = new InMemorySessionService();
    Runner runner = new Runner(myAgent, "my_artifact_app", artifactService, sessionService);
    // Now, contexts within runs managed by this runner can use artifact methods
    ```

#### Artifact Data
*   **Standard Representation**: Artifact content is universally represented using the `google.genai.types.Part` object, the same structure used for parts of LLM messages.
*   **Key Attribute (`inline_data`)**: For artifacts, the most relevant attribute is `inline_data`, which is a `google.genai.types.Blob` object containing:
    *   `data` (`bytes`): The raw binary content of the artifact.
    *   `mime_type` (`str`): A standard MIME type string (e.g., `'application/pdf'`, `'image/png'`, `'audio/mpeg'`) describing the nature of the binary data. This is crucial for correct interpretation when loading the artifact.
    **Python Example:**
    ```python
    import google.genai.types as types
    # Example: Creating an artifact Part from raw bytes
    pdf_bytes = b'%PDF-1.4...'  # Your raw PDF data
    pdf_mime_type = "application/pdf"

    # Using the constructor
    pdf_artifact_py = types.Part(
        inline_data=types.Blob(data=pdf_bytes, mime_type=pdf_mime_type)
    )
    # Using the convenience class method (equivalent)
    pdf_artifact_alt_py = types.Part.from_data(data=pdf_bytes, mime_type=pdf_mime_type)
    print(f"Created Python artifact with MIME type: {pdf_artifact_py.inline_data.mime_type}")
    ```
    **Java Example:**
    ```java
    import com.google.genai.types.Blob;
    import com.google.genai.types.Part;
    import java.nio.charset.StandardCharsets;

    public class ArtifactDataExample {
        public static void main(String[] args) {
            // Example: Creating an artifact Part from raw bytes
            byte[] pdfBytes = "%PDF-1.4...".getBytes(StandardCharsets.UTF_8); // Your raw PDF data
            String pdfMimeType = "application/pdf";

            // Using the Part.fromBlob() constructor with a Blob
            Blob pdfBlob = Blob.builder().data(pdfBytes).mimeType(pdfMimeType).build();
            Part pdfArtifactJava = Part.builder().inlineData(pdfBlob).build();

            // Using the convenience static method Part.fromBytes() (equivalent)
            Part pdfArtifactAltJava = Part.fromBytes(pdfBytes, pdfMimeType);

            // Accessing mimeType, note the use of Optional
            String mimeType = pdfArtifactJava.inlineData().flatMap(Blob::mimeType).orElse("unknown");
            System.out.println("Created Java artifact with MIME type: " + mimeType);

            // Accessing data
            byte[] data = pdfArtifactJava.inlineData().flatMap(Blob::data).orElse(new byte[0]);
            System.out.println("Java artifact data (first 10 bytes): "
                + new String(data, 0, Math.min(data.length, 10), StandardCharsets.UTF_8) + "...");
        }
    }
    ```

#### Filename
*   **Identifier**: A simple string used to name and retrieve an artifact within its specific namespace.
*   **Uniqueness**: Filenames must be unique within their scope (either the session or the user namespace).
*   **Best Practice**: Use descriptive names, potentially including file extensions (e.g., `"monthly_report.pdf"`, `"user_avatar.jpg"`), although the extension itself doesn't dictate behavior – the `mime_type` does.

#### Versioning
*   **Automatic Versioning**: The artifact service automatically handles versioning. When you call `save_artifact`, the service determines the next available version number (typically starting from 0 and incrementing) for that specific filename and scope.
*   **Returned by `save_artifact`**: The `save_artifact` method returns the integer version number that was assigned to the newly saved artifact.
*   **Retrieval**:
    *   `load_artifact(..., version=None)` (default): Retrieves the latest available version of the artifact.
    *   `load_artifact(..., version=N)`: Retrieves the specific version `N`.
*   **Listing Versions**: The `list_versions` method (on the service, not context) can be used to find all existing version numbers for an artifact.

#### Namespacing (Session vs. User)
*   **Concept**: Artifacts can be scoped either to a specific session or more broadly to a user across all their sessions within the application. This scoping is determined by the `filename` format and handled internally by the `ArtifactService`.
*   **Default (Session Scope)**: If you use a plain filename like `"report.pdf"`, the artifact is associated with the specific `app_name`, `user_id`, and `session_id`. It's only accessible within that exact session context.
*   **User Scope (`"user:"` prefix)**: If you prefix the filename with `"user:"`, like `"user:profile.png"`, the artifact is associated only with the `app_name` and `user_id`. It can be accessed or updated from any session belonging to that user within the app.
    ```python
    # Example illustrating namespace difference (conceptual)
    # Session-specific artifact filename
    session_report_filename = "summary.txt"
    # User-specific artifact filename
    user_config_filename = "user:settings.json"

    # When saving 'summary.txt' via context.save_artifact,
    # it's tied to the current app_name, user_id, and session_id.

    # When saving 'user:settings.json' via context.save_artifact,
    # the ArtifactService implementation should recognize the "user:" prefix
    # and scope it to app_name and user_id, making it accessible across sessions for that user.
    ```
    ```java
    // Example illustrating namespace difference (conceptual)
    // Session-specific artifact filename
    String sessionReportFilename = "summary.txt";
    // User-specific artifact filename
    String userConfigFilename = "user:settings.json"; // The "user:" prefix is key

    // When saving 'summary.txt' via context.save_artifact,
    // it's tied to the current app_name, user_id, and session_id.
    // artifactService.saveArtifact(appName, userId, sessionId1, sessionReportFilename, someData);

    // When saving 'user:settings.json' via context.save_artifact,
    // the ArtifactService implementation should recognize the "user:" prefix
    // and scope it to app_name and user_id, making it accessible across sessions for that user.
    // artifactService.saveArtifact(appName, userId, sessionId1, userConfigFilename, someData);
    ```

These core concepts work together to provide a flexible system for managing binary data within the ADK framework.

### Interacting with Artifacts (via Context Objects)
The primary way you interact with artifacts within your agent's logic (specifically within callbacks or tools) is through methods provided by the `CallbackContext` and `ToolContext` objects. These methods abstract away the underlying storage details managed by the `ArtifactService`.

#### Prerequisite: Configuring the `ArtifactService`
Before you can use any artifact methods via the context objects, you must provide an instance of a `BaseArtifactService` implementation (like `InMemoryArtifactService` or `GcsArtifactService`) when initializing your `Runner`.

**Python:**
```python
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService # Or GcsArtifactService
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService

# Your agent definition
agent = LlmAgent(name="my_agent", model="gemini-2.0-flash")
# Instantiate the desired artifact service
artifact_service = InMemoryArtifactService()
# Provide it to the Runner
runner = Runner(
    agent=agent,
    app_name="artifact_app",
    session_service=InMemorySessionService(),
    artifact_service=artifact_service  # Service must be provided here
)
```
If no `artifact_service` is configured in the `InvocationContext` (which happens if it's not passed to the `Runner`), calling `save_artifact`, `load_artifact`, or `list_artifacts` on the context objects will raise a `ValueError`.

**Java:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.artifacts.InMemoryArtifactService; // Or GcsArtifactService
import com.google.adk.runner.Runner;
import com.google.adk.sessions.InMemorySessionService;

public class SampleArtifactAgent {
    public static void main(String[] args) {
        // Your agent definition
        LlmAgent agent = LlmAgent.builder()
            .name("my_agent")
            .model("gemini-2.0-flash")
            .build();
        // Instantiate the desired artifact service
        InMemoryArtifactService artifactService = new InMemoryArtifactService();
        // Provide it to the Runner
        Runner runner = new Runner(
            agent,
            "APP_NAME",
            artifactService, // Service must be provided here
            new InMemorySessionService()
        );
    }
}
```
In Java, if an `ArtifactService` instance is not available (e.g., `null`) when artifact operations are attempted, it would typically result in a `NullPointerException` or a custom error, depending on how your application is structured. Robust applications often use dependency injection frameworks to manage service lifecycles and ensure availability.

#### Accessing Methods
The artifact interaction methods are available directly on instances of `CallbackContext` (passed to agent and model callbacks) and `ToolContext` (passed to tool callbacks). Remember that `ToolContext` inherits from `CallbackContext`.

##### Saving Artifacts
**Python Example:**
```python
import google.genai.types as types
from google.adk.agents.callback_context import CallbackContext # Or ToolContext
import asyncio

async def save_generated_report_py(context: CallbackContext, report_bytes: bytes):
    """Saves generated PDF report bytes as an artifact."""
    report_artifact = types.Part.from_data(data=report_bytes, mime_type="application/pdf")
    filename = "generated_report.pdf"
    try:
        version = await context.save_artifact(filename=filename, artifact=report_artifact) # save_artifact is async
        print(f"Successfully saved Python artifact '{filename}' as version {version}.")
        # The event generated after this callback will contain:
        # event.actions.artifact_delta == {"generated_report.pdf": version}
    except ValueError as e:
        print(f"Error saving Python artifact: {e}. Is ArtifactService configured in Runner?")
    except Exception as e: # Handle potential storage errors (e.g., GCS permissions)
        print(f"An unexpected error occurred during Python artifact save: {e}")

# --- Example Usage Concept (Python) ---
# async def main_py():
#   callback_context: CallbackContext = ... # obtain context
#   report_data = b'...' # Assume this holds the PDF bytes
#   await save_generated_report_py(callback_context, report_data)
```
**Java Example:**
```java
import com.google.adk.agents.CallbackContext;
import com.google.adk.artifacts.BaseArtifactService;
import com.google.adk.artifacts.InMemoryArtifactService;
import com.google.genai.types.Part;
import java.nio.charset.StandardCharsets;
import java.util.Optional;


public class SaveArtifactExample {
    public void saveGeneratedReport(CallbackContext callbackContext, byte[] reportBytes) {
        // Saves generated PDF report bytes as an artifact.
        Part reportArtifact = Part.fromBytes(reportBytes, "application/pdf");
        String filename = "generatedReport.pdf";
        // In Java, saveArtifact on CallbackContext might return Optional<Integer> or void
        // depending on ADK version. The actual saving is delegated to the service.
        // The example provided earlier used context.saveArtifact directly.
        // Here we assume it's a method on context.
        Optional<Integer> versionOpt = callbackContext.saveArtifact(filename, reportArtifact); // Assuming it returns Optional<Integer>
        versionOpt.ifPresent(version ->
            System.out.println("Successfully saved Java artifact '" + filename + "' as version " + version)
        );
        if (!versionOpt.isPresent()){
             System.out.println("Successfully saved Java artifact '" + filename + "' (version not immediately available from context method).");
        }
        // The event generated after this callback will contain:
        // event().actions().artifactDelta == {"generated_report.pdf": version}
    }

    // --- Example Usage Concept (Java) ---
    // public static void main(String[] args) {
    //     BaseArtifactService service = new InMemoryArtifactService(); // Or GcsArtifactService
    //     SaveArtifactExample myTool = new SaveArtifactExample();
    //     byte[] reportData = "...".getBytes(StandardCharsets.UTF_8); // PDF bytes
    //     CallbackContext callbackContext; // ... obtain callback context from your app
    //     myTool.saveGeneratedReport(callbackContext, reportData);
    //     // Due to async nature, in a real app, ensure program waits or handles completion.
    // }
}
```

##### Loading Artifacts
**Python Example:**
```python
import google.genai.types as types
from google.adk.agents.callback_context import CallbackContext # Or ToolContext
import asyncio

async def process_latest_report_py(context: CallbackContext):
    """Loads the latest report artifact and processes its data."""
    filename = "generated_report.pdf"
    try:
        # Load the latest version
        report_artifact = await context.load_artifact(filename=filename) # load_artifact is async
        if report_artifact and report_artifact.inline_data:
            print(f"Successfully loaded latest Python artifact '{filename}'.")
            print(f"MIME Type: {report_artifact.inline_data.mime_type}")
            # Process the report_artifact.inline_data.data (bytes)
            pdf_bytes = report_artifact.inline_data.data
            print(f"Report size: {len(pdf_bytes)} bytes.")
            # ... further processing ...
        else:
            print(f"Python artifact '{filename}' not found.")

        # Example: Load a specific version (if version 0 exists)
        # specific_version_artifact = await context.load_artifact(filename=filename, version=0)
        # if specific_version_artifact:
        #     print(f"Loaded version 0 of '{filename}'.")

    except ValueError as e:
        print(f"Error loading Python artifact: {e}. Is ArtifactService configured?")
    except Exception as e: # Handle potential storage errors
        print(f"An unexpected error occurred during Python artifact load: {e}")

# --- Example Usage Concept (Python) ---
# async def main_py():
#   callback_context: CallbackContext = ... # obtain context
#   await process_latest_report_py(callback_context)
```
**Java Example:**
```java
import com.google.adk.artifacts.BaseArtifactService;
import com.google.adk.agents.CallbackContext; // Assuming context is passed or available
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.MaybeObserver;
import io.reactivex.rxjava3.disposables.Disposable;
import java.util.Optional;


public class MyArtifactLoaderService {
    // In a real app, artifactService, appName, userId, sessionId would be passed or injected
    // For this example, let's assume context is available.
    public void processLatestReportJava(CallbackContext context, String filename) {
        // Load the latest version by passing Optional.empty() for the version
        // Assuming loadArtifact is available on CallbackContext
        context.loadArtifact(filename, Optional.empty()) // This is a conceptual call based on Python's context.
                                                        // Java might directly use artifactService.
            .subscribe(new MaybeObserver<Part>() {
                @Override
                public void onSubscribe(Disposable d) { /* Optional: handle subscription */ }

                @Override
                public void onSuccess(Part reportArtifact) {
                    System.out.println("Successfully loaded latest Java artifact '" + filename + "'.");
                    reportArtifact.inlineData().ifPresent(blob -> {
                        System.out.println("MIME Type: " + blob.mimeType().orElse("N/A"));
                        byte[] pdfBytes = blob.data().orElse(new byte[0]);
                        System.out.println("Report size: " + pdfBytes.length + " bytes.");
                        // ... further processing of pdfBytes ...
                    });
                }
                @Override
                public void onError(Throwable e) {
                    System.err.println("An error occurred during Java artifact load for '" + filename + "': " + e.getMessage());
                }
                @Override
                public void onComplete() {
                    System.out.println("Java artifact '" + filename + "' not found.");
                }
            });
    }
}
```

##### Listing Artifact Filenames
**Python Example:**
```python
from google.adk.tools.tool_context import ToolContext # list_artifacts is on ToolContext
import asyncio

async def list_user_files_py(tool_context: ToolContext) -> str:
    """Tool to list available artifacts for the user."""
    try:
        available_files = await tool_context.list_artifacts() # list_artifacts is async
        if not available_files:
            return "You have no saved artifacts."
        else:
            # Format the list for the user/LLM
            file_list_str = "\n".join([f"- {fname}" for fname in available_files])
            return f"Here are your available Python artifacts:\n{file_list_str}"
    except ValueError as e:
        print(f"Error listing Python artifacts: {e}. Is ArtifactService configured?")
        return "Error: Could not list Python artifacts."
    except Exception as e:
        print(f"An unexpected error occurred during Python artifact list: {e}")
        return "Error: An unexpected error occurred while listing Python artifacts."

# This function would typically be wrapped in a FunctionTool
# from google.adk.tools import FunctionTool
# list_files_tool = FunctionTool(func=list_user_files_py)
```
**Java Example:**
```java
import com.google.adk.artifacts.BaseArtifactService;
import com.google.adk.artifacts.ListArtifactsResponse;
import com.google.common.collect.ImmutableList;
import io.reactivex.rxjava3.core.SingleObserver;
import io.reactivex.rxjava3.disposables.Disposable;
import com.google.adk.tools.ToolContext; // Assuming listArtifacts is available on ToolContext

public class MyArtifactListerService {
    // Assuming context is passed or available
    public void listUserFilesJava(ToolContext toolContext) { // Using ToolContext
        toolContext.listArtifacts() // Conceptual call on ToolContext
            .subscribe(new SingleObserver<ListArtifactsResponse>() {
                @Override
                public void onSubscribe(Disposable d) { /* Optional: handle subscription */ }

                @Override
                public void onSuccess(ListArtifactsResponse response) {
                    ImmutableList<String> availableFiles = response.filenames();
                    if (availableFiles.isEmpty()) {
                        System.out.println("User has no saved Java artifacts.");
                    } else {
                        StringBuilder fileListStr = new StringBuilder("Here are the available Java artifacts:\n");
                        for (String fname : availableFiles) {
                            fileListStr.append("- ").append(fname).append("\n");
                        }
                        System.out.println(fileListStr.toString());
                    }
                }
                @Override
                public void onError(Throwable e) {
                    System.err.println("Error listing Java artifacts: " + e.getMessage());
                }
            });
    }
}
```
These methods for saving, loading, and listing provide a convenient and consistent way to manage binary data persistence within ADK, whether using Python's context objects or directly interacting with the `BaseArtifactService` in Java, regardless of the chosen backend storage implementation.

### Available Implementations
ADK provides concrete implementations of the `BaseArtifactService` interface, offering different storage backends suitable for various development stages and deployment needs. These implementations handle the details of storing, versioning, and retrieving artifact data based on the `app_name`, `user_id`, `session_id`, and `filename` (including the `user:` namespace prefix).

#### `InMemoryArtifactService`
*   **Storage Mechanism**:
    *   Python: Uses a Python dictionary (`self.artifacts`) held in the application's memory. The dictionary keys represent the artifact path, and the values are lists of `types.Part`, where each list element is a version.
    *   Java: Uses nested `HashMap` instances (`private final Map<String, Map<String, Map<String, Map<String, List<Part>>>>> artifacts;`) held in memory. The keys at each level are `appName`, `userId`, `sessionId`, and `filename` respectively. The innermost `List<Part>` stores the versions of the artifact, where the list index corresponds to the version number.
*   **Key Features**:
    *   **Simplicity**: Requires no external setup or dependencies beyond the core ADK library.
    *   **Speed**: Operations are typically very fast as they involve in-memory map/dictionary lookups and list manipulations.
    *   **Ephemeral**: All stored artifacts are lost when the application process terminates. Data does not persist between application restarts.
*   **Use Cases**:
    *   Ideal for local development and testing where persistence is not required.
    *   Suitable for short-lived demonstrations or scenarios where artifact data is purely temporary within a single run of the application.
*   **Instantiation**:
    **Python:**
    ```python
    from google.adk.artifacts import InMemoryArtifactService
    # Simply instantiate the class
    in_memory_service_py = InMemoryArtifactService()
    # Then pass it to the Runner
    # runner = Runner(..., artifact_service=in_memory_service_py)
    ```
    **Java:**
    ```java
    import com.google.adk.artifacts.BaseArtifactService;
    import com.google.adk.artifacts.InMemoryArtifactService;

    public class InMemoryServiceSetup {
        public static void main(String[] args) {
            // Simply instantiate the class
            BaseArtifactService inMemoryServiceJava = new InMemoryArtifactService();
            System.out.println("InMemoryArtifactService (Java) instantiated: " + inMemoryServiceJava.getClass().getName());
            // This instance would then be provided to your Runner.
            // Runner runner = new Runner(
            //     /* other services */,
            //     inMemoryServiceJava
            // );
        }
    }
    ```

#### `GcsArtifactService`
*   **Storage Mechanism**: Leverages Google Cloud Storage (GCS) for persistent artifact storage. Each version of an artifact is stored as a separate object (blob) within a specified GCS bucket.
*   **Object Naming Convention**: It constructs GCS object names (blob names) using a hierarchical path structure.
*   **Key Features**:
    *   **Persistence**: Artifacts stored in GCS persist across application restarts and deployments.
    *   **Scalability**: Leverages the scalability and durability of Google Cloud Storage.
    *   **Versioning**: Explicitly stores each version as a distinct GCS object. The `saveArtifact` method in `GcsArtifactService`.
    *   **Permissions Required**: The application environment needs appropriate credentials (e.g., Application Default Credentials) and IAM permissions to read from and write to the specified GCS bucket.
*   **Use Cases**:
    *   Production environments requiring persistent artifact storage.
    *   Scenarios where artifacts need to be shared across different application instances or services (by accessing the same GCS bucket).
    *   Applications needing long-term storage and retrieval of user or session data.
*   **Instantiation**:
    **Python:**
    ```python
    from google.adk.artifacts import GcsArtifactService
    # Specify the GCS bucket name
    gcs_bucket_name_py = "your-gcs-bucket-for-adk-artifacts"  # Replace with your bucket name
    try:
        gcs_service_py = GcsArtifactService(bucket_name=gcs_bucket_name_py)
        print(f"Python GcsArtifactService initialized for bucket: {gcs_bucket_name_py}")
        # Ensure your environment has credentials to access this bucket.
        # e.g., via Application Default Credentials (ADC)
        # Then pass it to the Runner
        # runner = Runner(..., artifact_service=gcs_service_py)
    except Exception as e: # Catch potential errors during GCS client initialization
        print(f"Error initializing Python GcsArtifactService: {e}")
        # Handle the error appropriately - maybe fall back to InMemory or raise
    ```
    **Java:**
    ```java
    import com.google.adk.artifacts.BaseArtifactService;
    import com.google.adk.artifacts.GcsArtifactService;
    import com.google.cloud.storage.Storage;
    import com.google.cloud.storage.StorageOptions;

    public class GcsServiceSetup {
        public static void main(String[] args) {
            // Specify the GCS bucket name
            String gcsBucketNameJava = "your-gcs-bucket-for-adk-artifacts"; // Replace with your bucket name
            try {
                // Initialize the GCS Storage client.
                // This will use Application Default Credentials by default.
                // Ensure the environment is configured correctly (e.g., GOOGLE_APPLICATION_CREDENTIALS).
                Storage storageClient = StorageOptions.getDefaultInstance().getService();
                // Instantiate the GcsArtifactService
                BaseArtifactService gcsServiceJava = new GcsArtifactService(gcsBucketNameJava, storageClient);
                System.out.println("Java GcsArtifactService initialized for bucket: " + gcsBucketNameJava);
                // This instance would then be provided to your Runner.
                // Runner runner = new Runner(
                //     /* other services */,
                //     gcsServiceJava
                // );
            } catch (Exception e) { // Catch potential errors during GCS client initialization
                System.err.println("Error initializing Java GcsArtifactService: " + e.getMessage());
                e.printStackTrace();
                // Handle the error appropriately
            }
        }
    }
    ```
Choosing the appropriate `ArtifactService` implementation depends on your application's requirements for data persistence, scalability, and operational environment.

### Best Practices
To use artifacts effectively and maintainably:
*   **Choose the Right Service**: Use `InMemoryArtifactService` for rapid prototyping, testing, and scenarios where persistence isn't needed. Use `GcsArtifactService` (or implement your own `BaseArtifactService` for other backends) for production environments requiring data persistence and scalability.
*   **Meaningful Filenames**: Use clear, descriptive filenames. Including relevant extensions (`.pdf`, `.png`, `.wav`) helps humans understand the content, even though the `mime_type` dictates programmatic handling. Establish conventions for temporary vs. persistent artifact names.
*   **Specify Correct MIME Types**: Always provide an accurate `mime_type` when creating the `types.Part` for `save_artifact`. This is critical for applications or tools that later `load_artifact` to interpret the `bytes` data correctly. Use standard IANA MIME types where possible.
*   **Understand Versioning**: Remember that `load_artifact()` without a specific `version` argument retrieves the latest version. If your logic depends on a specific historical version of an artifact, be sure to provide the integer version number when loading.
*   **Use Namespacing (`user:`) Deliberately**: Only use the `"user:"` prefix for filenames when the data truly belongs to the user and should be accessible across all their sessions. For data specific to a single conversation or session, use regular filenames without the prefix.
*   **Error Handling**:
    *   Always check if an `artifact_service` is actually configured before calling context methods (`save_artifact`, `load_artifact`, `list_artifacts`) – they will raise a `ValueError` if the service is `None`.
    *   Check the return value of `load_artifact`, as it will be `None` if the artifact or version doesn't exist. Don't assume it always returns a `Part`.
    *   Be prepared to handle exceptions from the underlying storage service, especially with `GcsArtifactService` (e.g., `google.api_core.exceptions.Forbidden` for permission issues, `NotFound` if the bucket doesn't exist, network errors).
*   **Size Considerations**: Artifacts are suitable for typical file sizes, but be mindful of potential costs and performance impacts with extremely large files, especially with cloud storage. `InMemoryArtifactService` can consume significant memory if storing many large artifacts. Evaluate if very large data might be better handled through direct GCS links or other specialized storage solutions rather than passing entire byte arrays in-memory.
*   **Cleanup Strategy**: For persistent storage like `GcsArtifactService`, artifacts remain until explicitly deleted. If artifacts represent temporary data or have a limited lifespan, implement a strategy for cleanup. This might involve:
    *   Using GCS lifecycle policies on the bucket.
    *   Building specific tools or administrative functions that utilize the `artifact_service.delete_artifact` method (note: delete is not exposed via context objects for safety).
    *   Carefully managing filenames to allow pattern-based deletion if needed.

## 7. Callbacks
### Introduction: What are Callbacks and Why Use Them?
Callbacks are a cornerstone feature of ADK, providing a powerful mechanism to hook into an agent's execution process. They allow you to observe, customize, and even control the agent's behavior at specific, predefined points without modifying the core ADK framework code.

**What are they?** In essence, callbacks are standard functions that you define. You then associate these functions with an agent when you create it. The ADK framework automatically calls your functions at key stages, letting you observe or intervene. Think of it like checkpoints during the agent's process:
*   **Before the agent starts its main work on a request, and after it finishes**:
    *   The **Before Agent** callback executes right before this main work begins for that specific request.
    *   The **After Agent** callback executes right after the agent has finished all its steps for that request and has prepared the final result, but just before the result is returned.
    This "main work" encompasses the agent's entire process for handling that single request.
*   **Before sending a request to, or after receiving a response from, the Large Language Model (LLM)**: These callbacks (**Before Model**, **After Model**) allow you to inspect or modify the data going to and coming from the LLM specifically.
*   **Before executing a tool (like a Python function or another agent) or after it finishes**: Similarly, **Before Tool** and **After Tool** callbacks give you control points specifically around the execution of tools invoked by the agent.

**Why use them?** Callbacks unlock significant flexibility and enable advanced agent capabilities:
*   **Observe & Debug**: Log detailed information at critical steps for monitoring and troubleshooting.
*   **Customize & Control**: Modify data flowing through the agent (like LLM requests or tool results) or even bypass certain steps entirely based on your logic.
*   **Implement Guardrails**: Enforce safety rules, validate inputs/outputs, or prevent disallowed operations.
*   **Manage State**: Read or dynamically update the agent's session state during execution.
*   **Integrate & Enhance**: Trigger external actions (API calls, notifications) or add features like caching.

**How are they added:**
**Python Example:**
```python
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from typing import Optional

# --- Define your callback function ---
def my_before_model_logic(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print(f"Callback running before model call for agent: {callback_context.agent_name}")
    # ... your custom logic here ...
    return None  # Allow the model call to proceed

# --- Register it during Agent creation ---
my_agent = LlmAgent(
    name="MyCallbackAgent",
    model="gemini-2.0-flash",  # Or your desired model
    instruction="Be helpful.",
    # Other agent parameters...
    before_model_callback=my_before_model_logic  # Pass the function here
)
```
**Java Example:**
```java
import com.google.adk.agents.CallbackContext;
import com.google.adk.agents.Callbacks; // For functional interface
import com.google.adk.agents.LlmAgent;
import com.google.adk.models.LlmRequest;
import com.google.adk.models.LlmResponse; // For Optional<LlmResponse>
import io.reactivex.rxjava3.core.Maybe; // Or Optional if that's the signature
import java.util.Optional;


public class AgentWithBeforeModelCallback {
    public static void main(String[] args) {
        // --- Define your callback logic ---
        Callbacks.BeforeModelCallback myBeforeModelLogic = // Assuming async callback by default
            (CallbackContext callbackContext, LlmRequest llmRequest) -> {
                System.out.println("Callback running before model call for agent: " + callbackContext.agentName());
                // ... your custom logic here ...
                // Return Optional.empty() to allow the model call to proceed,
                // similar to returning None in the Python example.
                // If you wanted to return a response and skip the model call,
                // you would return Optional.of(yourLlmResponse).
                return Maybe.empty(); // For async callbacks
            };
        // For sync: Callbacks.BeforeModelCallbackSync syncLogic = ... return Optional.empty();

        // --- Register it during Agent creation ---
        LlmAgent myAgent = LlmAgent.builder()
            .name("MyCallbackAgent")
            .model("gemini-2.0-flash") // Or your desired model
            .instruction("Be helpful.")
            // Other agent parameters...
            .beforeModelCallback(myBeforeModelLogic) // Pass the callback implementation here
            // .beforeModelCallbackSync(syncLogic) // For synchronous version
            .build();
        System.out.println("Agent created: " + myAgent.name());
    }
}
```

### The Callback Mechanism: Interception and Control
When the ADK framework encounters a point where a callback can run (e.g., just before calling the LLM), it checks if you provided a corresponding callback function for that agent. If you did, the framework executes your function.

**Context is Key**: Your callback function isn't called in isolation. The framework provides special context objects (`CallbackContext` or `ToolContext`) as arguments. These objects contain vital information about the current state of the agent's execution, including the invocation details, session state, and potentially references to services like artifacts or memory. You use these context objects to understand the situation and interact with the framework. (See the dedicated "Context Objects" section for full details).

**Controlling the Flow (The Core Mechanism)**: The most powerful aspect of callbacks lies in how their return value influences the agent's subsequent actions. This is how you intercept and control the execution flow:
*   **`return None` (Python) / `return Optional.empty()` or `Maybe.empty()` (Java) (Allow Default Behavior)**:
    This is the standard way to signal that your callback has finished its work (e.g., logging, inspection, minor modifications to mutable input arguments like `llm_request`) and that the ADK agent should proceed with its normal operation.
    *   For `before_*` callbacks (`before_agent`, `before_model`, `before_tool`), returning this means the next step in the sequence (running the agent logic, calling the LLM, executing the tool) will occur.
    *   For `after_*` callbacks (`after_agent`, `after_model`, `after_tool`), returning this means the result just produced by the preceding step (the agent's output, the LLM's response, the tool's result) will be used as is.
*   **`return <Specific Object>` (Override Default Behavior)**:
    Returning a specific type of object (instead of `None` or empty Optional/Maybe) is how you override the ADK agent's default behavior. The framework will use the object you return and skip the step that would normally follow or replace the result that was just generated.
    *   `before_agent_callback` → `types.Content`: Skips the agent's main execution logic (`_run_async_impl` / `_run_live_impl`). The returned `Content` object is immediately treated as the agent's final output for this turn. Useful for handling simple requests directly or enforcing access control.
    *   `before_model_callback` → `LlmResponse`: Skips the call to the external Large Language Model. The returned `LlmResponse` object is processed as if it were the actual response from the LLM. Ideal for implementing input guardrails, prompt validation, or serving cached responses.
    *   `before_tool_callback` → `dict` or `Map`: Skips the execution of the actual tool function (or sub-agent). The returned `dict` is used as the result of the tool call, which is then typically passed back to the LLM. Perfect for validating tool arguments, applying policy restrictions, or returning mocked/cached tool results.
    *   `after_agent_callback` → `types.Content`: Replaces the `Content` that the agent's run logic just produced.
    *   `after_model_callback` → `LlmResponse`: Replaces the `LlmResponse` received from the LLM. Useful for sanitizing outputs, adding standard disclaimers, or modifying the LLM's response structure.
    *   `after_tool_callback` → `dict` or `Map`: Replaces the `dict` result returned by the tool. Allows for post-processing or standardization of tool outputs before they are sent back to the LLM.

**Conceptual Code Example (Guardrail - Python):**
```python
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from google.adk.runners import Runner # Assuming Runner is used
from typing import Optional
from google.genai import types
from google.adk.sessions import InMemorySessionService
import asyncio

GEMINI_2_FLASH = "gemini-2.0-flash"

# --- Define the Callback Function ---
def simple_before_model_modifier(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Inspects/modifies the LLM request or skips the call."""
    agent_name = callback_context.agent_name
    print(f"[Callback] Before model call for agent: {agent_name}")

    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == 'user':
        if llm_request.contents[-1].parts:
            last_user_message = llm_request.contents[-1].parts[0].text
    print(f"[Callback] Inspecting last user message: '{last_user_message}'")

    # --- Modification Example ---
    original_instruction = llm_request.config.system_instruction or types.Content(role="system", parts=[])
    prefix = "[Modified by Callback] "
    if not isinstance(original_instruction, types.Content):
        original_instruction = types.Content(role="system", parts=[types.Part(text=str(original_instruction))])
    if not original_instruction.parts:
        original_instruction.parts.append(types.Part(text=""))
    modified_text = prefix + (original_instruction.parts[0].text or "")
    original_instruction.parts[0].text = modified_text
    llm_request.config.system_instruction = original_instruction
    print(f"[Callback] Modified system instruction to: '{modified_text}'")

    # --- Skip Example ---
    if "BLOCK" in last_user_message.upper():
        print("[Callback] 'BLOCK' keyword found. Skipping LLM call.")
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="LLM call was blocked by before_model_callback.")],
            )
        )
    else:
        print("[Callback] Proceeding with LLM call.")
        return None

my_llm_agent = LlmAgent(
    name="ModelCallbackAgent",
    model=GEMINI_2_FLASH,
    instruction="You are a helpful assistant.",
    description="An LLM agent demonstrating before_model_callback",
    before_model_callback=simple_before_model_modifier
)

# APP_NAME = "guardrail_app" (Python only)
# USER_ID = "user_1"
# SESSION_ID = "session_001"

# async def main_guardrail_py(): # Python specific main
#     session_service = InMemorySessionService()
#     session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
#     runner = Runner(agent=my_llm_agent, app_name=APP_NAME, session_service=session_service)
#
#     async def call_agent(query):
#         content = types.Content(role='user', parts=[types.Part(text=query)])
#         events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content) # run_async for Python
#         async for event in events: # iterate async
#             if event.is_final_response():
#                 final_response = event.content.parts[0].text
#                 print("Agent Response: ", final_response)
#
#     await call_agent("Tell me a joke. BLOCK the response.")
#     await call_agent("Tell me about callbacks.")

# if __name__ == "__main__": # Python specific
#    asyncio.run(main_guardrail_py())
```
**Java Example:**
```java
import com.google.adk.agents.CallbackContext;
import com.google.adk.agents.LlmAgent;
import com.google.adk.events.Event;
import com.google.adk.models.LlmRequest;
import com.google.adk.models.LlmResponse;
import com.google.adk.runner.InMemoryRunner; // Assuming for Java ADK
import com.google.adk.sessions.Session;
import com.google.genai.types.Content;
import com.google.genai.types.GenerateContentConfig;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import io.reactivex.rxjava3.core.Maybe;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

public class BeforeModelGuardrailExample {
    private static final String MODEL_ID = "gemini-2.0-flash";
    private static final String APP_NAME = "guardrail_app_java";
    private static final String USER_ID = "user_1_java";

    public static void main(String[] args) {
        BeforeModelGuardrailExample example = new BeforeModelGuardrailExample();
        example.defineAgentAndRun("Tell me about quantum computing. This is a test. BLOCK this.");
        example.defineAgentAndRun("Tell me about callbacks.");
    }

    public Maybe<LlmResponse> simpleBeforeModelModifier(
        CallbackContext callbackContext, LlmRequest llmRequest
    ) {
        System.out.printf("%n[Callback] Before model call for agent: %s%n", callbackContext.agentName());
        String lastUserMessageText = "";
        List<Content> requestContents = llmRequest.contents();
        if (requestContents != null && !requestContents.isEmpty()) {
            Content lastContent = requestContents.get(requestContents.size() - 1);
            if (lastContent.role().isPresent() && "user".equals(lastContent.role().get())) {
                lastUserMessageText = lastContent.parts().orElse(List.of()).stream()
                    .flatMap(part -> part.text().stream())
                    .collect(Collectors.joining(" "));
            }
        }
        System.out.printf("[Callback] Inspecting last user message: '%s'%n", lastUserMessageText);

        String prefix = "[Modified by Callback] ";
        GenerateContentConfig currentConfig = llmRequest.config().orElse(GenerateContentConfig.builder().build());
        Optional<Content> optOriginalSystemInstruction = currentConfig.systemInstruction();
        Content conceptualModifiedSystemInstruction;

        if (optOriginalSystemInstruction.isPresent()) {
            Content originalSystemInstruction = optOriginalSystemInstruction.get();
            List<Part> originalParts = new ArrayList<>(originalSystemInstruction.parts().orElse(List.of()));
            String originalText = "";
            if (!originalParts.isEmpty()) {
                Part firstPart = originalParts.get(0);
                if (firstPart.text().isPresent()) {
                    originalText = firstPart.text().get();
                }
                originalParts.set(0, Part.fromText(prefix + originalText));
            } else {
                originalParts.add(Part.fromText(prefix));
            }
            conceptualModifiedSystemInstruction = originalSystemInstruction.toBuilder().parts(originalParts).build();
        } else {
            conceptualModifiedSystemInstruction = Content.builder()
                .role("system")
                .parts(List.of(Part.fromText(prefix)))
                .build();
        }

        // This demonstrates building a new LlmRequest with the modified config.
        // In a real scenario, you might directly modify llmRequest.config if mutable,
        // or rebuild the LlmRequest if immutable.
        // For this example, we'll assume llmRequest.config().systemInstruction() can be updated.
        // llmRequest = llmRequest.toBuilder() // Assuming LlmRequest has a toBuilder()
        //     .config(currentConfig.toBuilder()
        //         .systemInstruction(conceptualModifiedSystemInstruction)
        //         .build())
        //     .build();
        System.out.printf("[Callback] Conceptually modified system instruction is: '%s'%n",
            conceptualModifiedSystemInstruction.parts().get().get(0).text().get());


        if (lastUserMessageText.toUpperCase().contains("BLOCK")) {
            System.out.println("[Callback] 'BLOCK' keyword found. Skipping LLM call.");
            LlmResponse skipResponse = LlmResponse.builder()
                .content(Content.builder()
                    .role("model")
                    .parts(List.of(Part.builder()
                        .text("LLM call was blocked by before_model_callback.")
                        .build()))
                    .build())
                .build();
            return Maybe.just(skipResponse);
        }
        System.out.println("[Callback] Proceeding with LLM call.");
        return Maybe.empty();
    }

    public void defineAgentAndRun(String prompt) {
        LlmAgent myLlmAgent = LlmAgent.builder()
            .name("ModelCallbackAgent")
            .model(MODEL_ID)
            .instruction("You are a helpful assistant.")
            .description("An LLM agent demonstrating before_model_callback")
            .beforeModelCallback(this::simpleBeforeModelModifier)
            .build();

        InMemoryRunner runner = new InMemoryRunner(myLlmAgent, APP_NAME);
        Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
        Content userMessage = Content.fromParts(Part.fromText(prompt));

        System.out.printf("%n--- Running agent with query: \"%s\" ---%n", prompt);
        Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
        eventStream.blockingForEach(event -> {
            if (event.finalResponse() && event.content().isPresent()) {
                 event.content().flatMap(Content::parts)
                    .filter(parts -> !parts.isEmpty() && parts.get(0).text().isPresent())
                    .ifPresent(parts -> System.out.println("Agent Response: " + parts.get(0).text().get()));
            }
        });
    }
}
```
By understanding this mechanism of returning `None` (Python) / empty `Optional`/`Maybe` (Java) versus returning specific objects, you can precisely control the agent's execution path, making callbacks an essential tool for building sophisticated and reliable agents with ADK.

### Types of Callbacks
The framework provides different types of callbacks that trigger at various stages of an agent's execution. Understanding when each callback fires and what context it receives is key to using them effectively.

#### Agent Lifecycle Callbacks
These callbacks are available on any agent that inherits from `BaseAgent` (including `LlmAgent`, `SequentialAgent`, `ParallelAgent`, `LoopAgent`, etc).
**Note**: The specific method names or return types may vary slightly by SDK language (e.g., `return None` in Python, `return Optional.empty()` or `Maybe.empty()` in Java). Refer to the language-specific API documentation for details.

##### Before Agent Callback
*   **When**: Called immediately before the agent's `_run_async_impl` (or `_run_live_impl`) method is executed. It runs after the agent's `InvocationContext` is created but before its core logic begins.
*   **Purpose**: Ideal for setting up resources or state needed only for this specific agent's run, performing validation checks on the session state (`callback_context.state`) before execution starts, logging the entry point of the agent's activity, or potentially modifying the invocation context before the core logic uses it.
*   **Return Value Effect**:
    *   `None` (Python) / `Optional.empty()` or `Maybe.empty()` (Java): The agent's `_run_async_impl` / `runAsyncImpl` method executes normally.
    *   `types.Content` (Python) / `Content` (Java): The agent's core logic is skipped. The returned `Content` is treated as the final response for this agent's turn.

**Python Example:**
```python
# ADK Imports
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import InMemoryRunner # Use InMemoryRunner
from google.genai import types # For types.Content
from typing import Optional
import asyncio

# Define the model - Use the specific model name requested
GEMINI_2_FLASH = "gemini-2.0-flash"

# --- 1. Define the Callback Function ---
def check_if_agent_should_run(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Logs entry and checks 'skip_llm_agent' in session state.
    If True, returns Content to skip the agent's execution.
    If False or not present, returns None to allow execution.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict() # Get a dictionary view of state

    print(f"\n[Callback] Entering agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback] Current State: {current_state}")

    # Check the condition in session state dictionary
    if current_state.get("skip_llm_agent", False):
        print(f"[Callback] State condition 'skip_llm_agent=True' met: Skipping agent {agent_name}.")
        # Return Content to skip the agent's run
        return types.Content(
            parts=[types.Part(text=f"Agent {agent_name} skipped by before_agent_callback due to state.")],
            role="model"  # Assign model role to the overriding response
        )
    else:
        print(f"[Callback] State condition not met: Proceeding with agent {agent_name}.")
        # Return None to allow the LlmAgent's normal execution
        return None

# --- 2. Setup Agent with Callback ---
llm_agent_with_before_cb = LlmAgent(
    name="MyControlledAgent",
    model=GEMINI_2_FLASH,
    instruction="You are a concise assistant.",
    description="An LLM agent demonstrating stateful before_agent_callback",
    before_agent_callback=check_if_agent_should_run  # Assign the callback
)

# --- 3. Setup Runner and Sessions using InMemoryRunner ---
async def main_before_agent():
    app_name = "before_agent_demo"
    user_id = "test_user"
    session_id_run = "session_will_run"
    session_id_skip = "session_will_skip"

    runner = InMemoryRunner(agent=llm_agent_with_before_cb, app_name=app_name)
    session_service = runner.session_service

    await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id_run
    )
    await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id_skip,
        state={"skip_llm_agent": True}
    )

    # --- Scenario 1: Run where callback allows agent execution ---
    print("\n" + "="*20 + f" SCENARIO 1: Running Agent on Session '{session_id_run}' (Should Proceed) " + "="*20)
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id_run,
        new_message=types.Content(role="user", parts=[types.Part(text="Hello, please respond.")])
    ):
        if event.is_final_response() and event.content:
            print(f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}")
        elif event.is_error(): # is_error is not a standard ADK event attribute, check error_message
            print(f"Error Event: {event.error_message if hasattr(event, 'error_message') else 'Unknown error'}")


    # --- Scenario 2: Run where callback intercepts and skips agent ---
    print("\n" + "="*20 + f" SCENARIO 2: Running Agent on Session '{session_id_skip}' (Should Skip) " + "="*20)
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id_skip,
        new_message=types.Content(role="user", parts=[types.Part(text="This message won't reach the LLM.")])
    ):
        if event.is_final_response() and event.content:
            print(f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}")
        elif hasattr(event, 'error_message') and event.error_message:
             print(f"Error Event: {event.error_message}")


# if __name__ == "__main__":
#     asyncio.run(main_before_agent())
```
**Java Example:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.BaseAgent; // For BaseAgent type
import com.google.adk.agents.CallbackContext;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.adk.sessions.State;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import io.reactivex.rxjava3.core.Maybe;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class BeforeAgentCallbackExample {
    private static final String APP_NAME_JAVA = "AgentWithBeforeAgentCallbackJava"; // Unique name
    private static final String USER_ID_JAVA = "test_user_789"; // Unique name
    private static final String MODEL_NAME_JAVA = "gemini-2.0-flash";

    public static void main(String[] args) {
        BeforeAgentCallbackExample callbackAgent = new BeforeAgentCallbackExample();
        callbackAgent.defineAgentAndRunScenarios();
    }

    public Maybe<Content> checkIfAgentShouldRun(CallbackContext callbackContext) {
        String agentName = callbackContext.agentName();
        String invocationId = callbackContext.invocationId();
        State currentState = callbackContext.state();
        System.out.printf("%n[Callback] Entering agent: %s (Inv: %s)%n", agentName, invocationId);
        System.out.printf("[Callback] Current State: %s%n", currentState.asMap()); // Use asMap for printing

        if (Boolean.TRUE.equals(currentState.get("skip_llm_agent"))) {
            System.out.printf("[Callback] State condition 'skip_llm_agent=True' met: Skipping agent %s%n", agentName);
            return Maybe.just(Content.fromParts(Part.fromText(
                String.format("Agent %s skipped by before_agent_callback due to state.", agentName))));
        }
        System.out.printf("[Callback] State condition 'skip_llm_agent=True' NOT met: Running agent %s%n", agentName);
        return Maybe.empty();
    }

    public void defineAgentAndRunScenarios() {
        BaseAgent llmAgentWithBeforeCallback = LlmAgent.builder()
            .model(MODEL_NAME_JAVA)
            .name(APP_NAME_JAVA) // Agent name
            .instruction("You are a concise assistant.")
            .description("An LLM agent demonstrating stateful before_agent_callback")
            .beforeAgentCallback(this::checkIfAgentShouldRun)
            .build();

        InMemoryRunner runner = new InMemoryRunner(llmAgentWithBeforeCallback, APP_NAME_JAVA); // App name for runner

        // Scenario 1: Agent will run
        System.out.println("\n" + "=".repeat(20) + " SCENARIO 1 (Java): Agent Should Proceed " + "=".repeat(20));
        runScenario(runner, "session_run_java", null, "Hello from Java, please respond.");

        // Scenario 2: Agent will be skipped
        System.out.println("\n" + "=".repeat(20) + " SCENARIO 2 (Java): Agent Should Skip " + "=".repeat(20));
        ConcurrentHashMap<String, Object> skipState = new ConcurrentHashMap<>(Map.of("skip_llm_agent", true));
        runScenario(runner, "session_skip_java", skipState, "This Java message won't reach LLM.");
    }

    private void runScenario(InMemoryRunner runner, String sessionId, ConcurrentHashMap<String, Object> initialState, String prompt) {
        Session session = runner.sessionService()
            .createSession(APP_NAME_JAVA, USER_ID_JAVA, initialState, sessionId)
            .blockingGet();
        Content userMessage = Content.fromParts(Part.fromText(prompt));
        Flowable<Event> eventStream = runner.runAsync(USER_ID_JAVA, session.id(), userMessage);

        eventStream.blockingForEach(event -> {
            if (event.finalResponse() && event.content().isPresent() && event.content().get().parts().isPresent() && !event.content().get().parts().get().isEmpty()) {
                 event.content().get().parts().get().get(0).text().ifPresent(text ->
                    System.out.printf("Final Output for %s: [%s] %s%n", sessionId, event.author(), text.strip())
                );
            } else if (event.errorCode().isPresent()){
                 System.out.printf("Error Event for %s: %s%n", sessionId, event.errorMessage().orElse("Unknown error"));
            }
        });
    }
}
```

##### After Agent Callback
*   **When**: Called immediately after the agent's `_run_async_impl` (or `_run_live_impl`) method successfully completes. It does not run if the agent was skipped due to `before_agent_callback` returning content or if `end_invocation` was set during the agent's run.
*   **Purpose**: Useful for cleanup tasks, post-execution validation, logging the completion of an agent's activity, modifying final state, or augmenting/replacing the agent's final output.
*   **Return Value Effect**:
    *   `None` (Python) / `Optional.empty()` or `Maybe.empty()` (Java): The agent's original output is used.
    *   `types.Content` (Python) / `Content` (Java): Replaces the agent's original output.

**Python Example:**
```python
# ADK Imports (ensure these are at the top of your script/notebook)
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import InMemoryRunner
from google.genai import types
from typing import Optional
import asyncio

GEMINI_2_FLASH = "gemini-2.0-flash"

# --- 1. Define the Callback Function ---
def modify_output_after_agent(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Logs exit from an agent and checks 'add_concluding_note' in session state.
    If True, returns new Content to *replace* the agent's original output.
    If False or not present, returns None, allowing the agent's original output to be used.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[Callback] Exiting agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback] Current State: {current_state}")

    if current_state.get("add_concluding_note", False):
        print(f"[Callback] State condition 'add_concluding_note=True' met: Replacing agent {agent_name}'s output.")
        return types.Content(
            parts=[types.Part(text="Concluding note added by after_agent_callback, replacing original output.")],
            role="model"
        )
    else:
        print(f"[Callback] State condition not met: Using agent {agent_name}'s original output.")
        return None

# --- 2. Setup Agent with Callback ---
llm_agent_with_after_cb = LlmAgent(
    name="MySimpleAgentWithAfter",
    model=GEMINI_2_FLASH,
    instruction="You are a simple agent. Just say 'Processing complete!'",
    description="An LLM agent demonstrating after_agent_callback for output modification",
    after_agent_callback=modify_output_after_agent
)

# --- 3. Setup Runner and Sessions using InMemoryRunner ---
async def main_after_agent():
    app_name = "after_agent_demo"
    user_id = "test_user_after"
    session_id_normal = "session_run_normally"
    session_id_modify = "session_modify_output"

    runner = InMemoryRunner(agent=llm_agent_with_after_cb, app_name=app_name)
    session_service = runner.session_service

    await session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id_normal)
    await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id_modify,
        state={"add_concluding_note": True}
    )

    async def call_agent_local(query, current_session_id): # Local helper to avoid repetition
        print(f"\n--- Running Query: {query} on Session: {current_session_id} ---")
        async for event in runner.run_async(
            user_id=user_id, session_id=current_session_id,
            new_message=types.Content(role="user", parts=[types.Part(text=query)])
        ):
            if event.is_final_response() and event.content:
                print(f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}")
            elif hasattr(event, 'error_message') and event.error_message:
                 print(f"Error Event: {event.error_message}")


    print("\n" + "="*20 + f" SCENARIO 1: Running Agent on Session '{session_id_normal}' (Should Use Original Output) " + "="*20)
    await call_agent_local("Process this please.", session_id_normal)

    print("\n" + "="*20 + f" SCENARIO 2: Running Agent on Session '{session_id_modify}' (Should Replace Output) " + "="*20)
    await call_agent_local("Process this and add note.", session_id_modify)

# if __name__ == "__main__":
#    asyncio.run(main_after_agent())
```
**Java Example:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.CallbackContext;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.State; // For state access
import com.google.adk.sessions.Session; // For session object
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import io.reactivex.rxjava3.core.Maybe;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

public class AfterAgentCallbackExample {
    private static final String APP_NAME_JAVA_AFTER = "after_agent_demo_java";
    private static final String USER_ID_JAVA_AFTER = "test_user_after_java";
    private static final String MODEL_NAME_JAVA_AFTER = "gemini-2.0-flash";

    public static void main(String[] args) {
        AfterAgentCallbackExample demo = new AfterAgentCallbackExample();
        demo.defineAgentAndRunScenarios();
    }

    public Maybe<Content> modifyOutputAfterAgent(CallbackContext callbackContext) {
        String agentName = callbackContext.agentName();
        String invocationId = callbackContext.invocationId();
        State currentState = callbackContext.state();
        System.out.printf("%n[Callback] Exiting agent: %s (Inv: %s)%n", agentName, invocationId);
        System.out.printf("[Callback] Current State: %s%n", currentState.asMap());

        Object addNoteFlag = currentState.get("add_concluding_note");
        if (Boolean.TRUE.equals(addNoteFlag)) {
            System.out.printf("[Callback] State condition 'add_concluding_note=True' met: Replacing agent %s's output.%n", agentName);
            return Maybe.just(Content.builder()
                .parts(List.of(Part.fromText("Concluding note added by after_agent_callback, replacing original output.")))
                .role("model")
                .build());
        } else {
            System.out.printf("[Callback] State condition not met: Using agent %s's original output.%n", agentName);
            return Maybe.empty();
        }
    }

    public void defineAgentAndRunScenarios() {
        LlmAgent llmAgentWithAfterCb = LlmAgent.builder()
            .name(APP_NAME_JAVA_AFTER) // Agent name
            .model(MODEL_NAME_JAVA_AFTER)
            .description("An LLM agent demonstrating after_agent_callback for output modification")
            .instruction("You are a simple agent. Just say 'Processing complete!'")
            .afterAgentCallback(this::modifyOutputAfterAgent)
            .build();

        InMemoryRunner runner = new InMemoryRunner(llmAgentWithAfterCb, APP_NAME_JAVA_AFTER);

        // Scenario 1
        System.out.printf("%n%s SCENARIO 1 (Java): Agent Should Use Original Output %s%n", "=".repeat(20), "=".repeat(20));
        runScenario(runner, "session_normal_java", null, "Process this please.");

        // Scenario 2
        System.out.printf("%n%s SCENARIO 2 (Java): Agent Should Replace Output %s%n", "=".repeat(20), "=".repeat(20));
        Map<String, Object> modifyState = new HashMap<>();
        modifyState.put("add_concluding_note", true);
        runScenario(runner, "session_modify_java", new ConcurrentHashMap<>(modifyState), "Process this and add note.");
    }

    private void runScenario(InMemoryRunner runner, String sessionId, ConcurrentHashMap<String, Object> initialState, String userQuery) {
        runner.sessionService().createSession(APP_NAME_JAVA_AFTER, USER_ID_JAVA_AFTER, initialState, sessionId).blockingGet();
        System.out.printf("Running scenario for session: %s, initial state: %s%n", sessionId, initialState != null ? initialState : "{}");

        Content userMessage = Content.builder().role("user").parts(List.of(Part.fromText(userQuery))).build();
        Flowable<Event> eventStream = runner.runAsync(USER_ID_JAVA_AFTER, sessionId, userMessage);

        eventStream.blockingForEach(event -> {
            if (event.finalResponse() && event.content().isPresent()) {
                String author = event.author() != null ? event.author() : "UNKNOWN";
                String text = event.content().flatMap(Content::parts)
                    .filter(parts -> !parts.isEmpty() && parts.get(0).text().isPresent())
                    .map(parts -> parts.get(0).text().get().trim())
                    .orElse("[No text in final response]");
                System.out.printf("Final Output for %s: [%s] %s%n", sessionId, author, text);
            } else if (event.errorCode().isPresent()) {
                System.out.printf("Error Event for %s: %s%n", sessionId, event.errorMessage().orElse("Unknown error"));
            }
        });
    }
}
```

#### LLM Interaction Callbacks
These callbacks are specific to `LlmAgent` and provide hooks around the interaction with the Large Language Model.

##### Before Model Callback
*   **When**: Called just before the `generate_content_async` (or equivalent) request is sent to the LLM within an `LlmAgent`'s flow.
*   **Purpose**: Allows inspection and modification of the request going to the LLM. Use cases include adding dynamic instructions, injecting few-shot examples based on state, modifying model config, implementing guardrails (like profanity filters), or implementing request-level caching.
*   **Return Value Effect**:
    *   If the callback returns `None` (or a `Maybe.empty()` object in Java), the LLM continues its normal workflow.
    *   If the callback returns an `LlmResponse` object, then the call to the LLM is skipped. The returned `LlmResponse` is used directly as if it came from the model. This is powerful for implementing guardrails or caching.
(See example in "The Callback Mechanism: Interception and Control" section above.)

##### After Model Callback
*   **When**: Called just after a response (`LlmResponse`) is received from the LLM, before it's processed further by the invoking agent.
*   **Purpose**: Allows inspection or modification of the raw LLM response. Use cases include:
    *   logging model outputs,
    *   reformatting responses,
    *   censoring sensitive information generated by the model,
    *   parsing structured data from the LLM response and storing it in `callback_context.state`
    *   or handling specific error codes.
*   **Return Value Effect**:
    *   `None` (Python) / `Maybe.empty()` (Java): The original `LlmResponse` is used.
    *   `LlmResponse` (Python/Java): Replaces the original `LlmResponse` received from the LLM.

**Python Example:**
```python
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import Runner # For a complete example
from typing import Optional
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.models import LlmResponse, LlmRequest # LlmRequest needed if you modify it
import copy # For deepcopy
import asyncio

GEMINI_2_FLASH = "gemini-2.0-flash"

def simple_after_model_modifier(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    agent_name = callback_context.agent_name
    print(f"[Callback] After model call for agent: {agent_name}")

    original_text = ""
    if llm_response.content and llm_response.content.parts:
        if llm_response.content.parts[0].text:
            original_text = llm_response.content.parts[0].text
            print(f"[Callback] Inspected original response text: '{original_text[:100]}...'")
        elif llm_response.content.parts[0].function_call:
            print(f"[Callback] Inspected response: Contains function call '{llm_response.content.parts[0].function_call.name}'. No text modification.")
            return None
        else:
            print("[Callback] Inspected response: No text content found.")
            return None
    elif llm_response.error_message: # Assuming error_message is an attribute
        print(f"[Callback] Inspected response: Contains error '{llm_response.error_message}'. No modification.")
        return None
    else:
        print("[Callback] Inspected response: Empty LlmResponse.")
        return None

    search_term = "joke"
    replace_term = "funny story"
    if search_term in original_text.lower():
        print(f"[Callback] Found '{search_term}'. Modifying response.")
        modified_text = original_text.replace(search_term, replace_term)
        modified_text = modified_text.replace(search_term.capitalize(), replace_term.capitalize())

        modified_parts = [copy.deepcopy(part) for part in llm_response.content.parts]
        modified_parts[0].text = modified_text
        new_response = LlmResponse(
            content=types.Content(role="model", parts=modified_parts),
            grounding_metadata=llm_response.grounding_metadata
        )
        print("[Callback] Returning modified response.")
        return new_response
    else:
        print(f"[Callback] '{search_term}' not found. Passing original response through.")
        return None

# my_llm_agent_after = LlmAgent(
#     name="AfterModelCallbackAgent",
#     model=GEMINI_2_FLASH,
#     instruction="Tell me a good joke about computers.",
#     description="An LLM agent demonstrating after_model_callback",
#     after_model_callback=simple_after_model_modifier
# )
# async def main_after_model():
#     # ... (Runner and session setup similar to before_model_callback example)
#     # await call_agent(my_llm_agent_after, "Tell me a joke.") # Example call
# if __name__ == "__main__":
#    asyncio.run(main_after_model())
```
**Java Example:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.CallbackContext;
import com.google.adk.events.Event;
import com.google.adk.models.LlmResponse;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.common.collect.ImmutableList;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import io.reactivex.rxjava3.core.Maybe;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class AfterModelCallbackExample {
    private static final String AGENT_NAME_JAVA = "AfterModelCallbackAgentJava";
    private static final String MODEL_NAME_JAVA = "gemini-2.0-flash";
    private static final String AGENT_INSTRUCTION_JAVA = "Tell me a good joke about computers.";
    private static final String APP_NAME_JAVA = "AfterModelCbAppJava";
    private static final String USER_ID_JAVA = "user_after_cb_java";
    private static final String SEARCH_TERM = "joke";
    private static final String REPLACE_TERM = "funny story";
    private static final Pattern SEARCH_PATTERN = Pattern.compile("\\b" + Pattern.quote(SEARCH_TERM) + "\\b", Pattern.CASE_INSENSITIVE);

    public static void main(String[] args) {
        AfterModelCallbackExample example = new AfterModelCallbackExample();
        example.defineAgentAndRun();
    }

    public Maybe<LlmResponse> simpleAfterModelModifier(
        CallbackContext callbackContext, LlmResponse llmResponse
    ) {
        String agentName = callbackContext.agentName();
        System.out.printf("%n[Callback] After model call for agent: %s%n", agentName);

        if (llmResponse.errorMessage().isPresent()) {
            System.out.printf("[Callback] Response has error: '%s'. No modification.%n", llmResponse.errorMessage().get());
            return Maybe.empty();
        }

        Optional<Part> firstTextPartOpt = llmResponse.content()
            .flatMap(Content::parts)
            .filter(parts -> !parts.isEmpty() && parts.get(0).text().isPresent())
            .map(parts -> parts.get(0));

        if (!firstTextPartOpt.isPresent()) {
             llmResponse.content()
                .flatMap(Content::parts)
                .filter(parts -> !parts.isEmpty() && parts.get(0).functionCall().isPresent())
                .ifPresent(parts -> System.out.printf("[Callback] Response is a function call ('%s'). No text modification.%n",
                    parts.get(0).functionCall().get().name().orElse("N/A")));
            if (!llmResponse.content().isPresent() || !llmResponse.content().flatMap(Content::parts).isPresent() || llmResponse.content().flatMap(Content::parts).get().isEmpty()) {
                System.out.println("[Callback] Response content is empty or has no parts. No modification.");
            } else if (!firstTextPartOpt.isPresent()) {
                System.out.println("[Callback] First part has no text content. No modification.");
            }
            return Maybe.empty();
        }

        String originalText = firstTextPartOpt.get().text().get();
        System.out.printf("[Callback] Inspected original text: '%.100s...'%n", originalText);

        Matcher matcher = SEARCH_PATTERN.matcher(originalText);
        if (!matcher.find()) {
            System.out.printf("[Callback] '%s' not found. Passing original response through.%n", SEARCH_TERM);
            return Maybe.empty();
        }

        System.out.printf("[Callback] Found '%s'. Modifying response.%n", SEARCH_TERM);
        String foundTerm = matcher.group(0);
        String actualReplaceTerm = REPLACE_TERM;
        if (Character.isUpperCase(foundTerm.charAt(0)) && REPLACE_TERM.length() > 0) {
            actualReplaceTerm = Character.toUpperCase(REPLACE_TERM.charAt(0)) + REPLACE_TERM.substring(1);
        }
        String modifiedText = matcher.replaceFirst(Matcher.quoteReplacement(actualReplaceTerm));

        Content originalContent = llmResponse.content().get();
        List<Part> originalParts = originalContent.parts().orElse(ImmutableList.of());
        List<Part> modifiedPartsList = new ArrayList<>(originalParts.size());
        if (!originalParts.isEmpty()) {
            modifiedPartsList.add(Part.fromText(modifiedText));
            for (int i = 1; i < originalParts.size(); i++) {
                modifiedPartsList.add(originalParts.get(i));
            }
        } else {
            modifiedPartsList.add(Part.fromText(modifiedText));
        }

        LlmResponse.Builder newResponseBuilder = LlmResponse.builder()
            .content(originalContent.toBuilder().parts(ImmutableList.copyOf(modifiedPartsList)).build())
            .groundingMetadata(llmResponse.groundingMetadata()); // Copy other fields

        System.out.println("[Callback] Returning modified response.");
        return Maybe.just(newResponseBuilder.build());
    }

    public void defineAgentAndRun() {
        LlmAgent myLlmAgent = LlmAgent.builder()
            .name(AGENT_NAME_JAVA)
            .model(MODEL_NAME_JAVA)
            .instruction(AGENT_INSTRUCTION_JAVA)
            .description("An LLM agent demonstrating after_model_callback")
            .afterModelCallback(this::simpleAfterModelModifier)
            .build();

        InMemoryRunner runner = new InMemoryRunner(myLlmAgent, APP_NAME_JAVA);
        Session session = runner.sessionService().createSession(APP_NAME_JAVA, USER_ID_JAVA).blockingGet();
        Content userMessage = Content.fromParts(Part.fromText("Tell me a joke about quantum computing. Make sure to use the word joke."));

        System.out.printf("%n--- Running agent ---%n");
        Flowable<Event> eventStream = runner.runAsync(USER_ID_JAVA, session.id(), userMessage);
        eventStream.blockingForEach(event -> {
            if (event.finalResponse() && event.content().isPresent()) {
                 event.content().flatMap(Content::parts)
                    .filter(parts -> !parts.isEmpty() && parts.get(0).text().isPresent())
                    .ifPresent(parts -> System.out.println("Agent Response: " + parts.get(0).text().get()));
            }
        });
    }
}
```

#### Tool Execution Callbacks
These callbacks are also specific to `LlmAgent` and trigger around the execution of tools (including `FunctionTool`, `AgentTool`, etc.) that the LLM might request.

##### Before Tool Callback
*   **When**: Called just before a specific tool's `run_async` method is invoked, after the LLM has generated a function call for it.
*   **Purpose**: Allows inspection and modification of tool arguments, performing authorization checks before execution, logging tool usage attempts, or implementing tool-level caching.
*   **Return Value Effect**:
    *   If the callback returns `None` (or a `Maybe.empty()` object in Java), the tool's `run_async` method is executed with the (potentially modified) `args`.
    *   If a dictionary (or `Map` in Java) is returned, the tool's `run_async` method is **skipped**. The returned dictionary is used directly as the result of the tool call. This is useful for caching or overriding tool behavior.

**Python Example:**
```python
from google.adk.agents import LlmAgent
# from google.adk.runners import Runner # Assuming Runner is used
from typing import Optional, Dict, Any
# from google.genai import types # Assuming types is used
# from google.adk.sessions import InMemorySessionService # Assuming service is used
from google.adk.tools import FunctionTool, BaseTool
from google.adk.tools.tool_context import ToolContext
# import asyncio

GEMINI_2_FLASH = "gemini-2.0-flash"

def get_capital_city_tool_cb(country: str) -> dict: # Renamed for clarity
    """Retrieves the capital city of a given country."""
    print(f"--- Tool 'get_capital_city_tool_cb' executing with country: {country} ---")
    country_capitals = {"united states": "Washington, D.C.", "canada": "Ottawa", "france": "Paris", "germany": "Berlin"}
    return {"result": country_capitals.get(country.lower(), f"Capital not found for {country}")}

capital_tool_for_cb = FunctionTool(func=get_capital_city_tool_cb, name="get_capital_city") # Explicit name

def simple_before_tool_modifier(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"[Callback] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    print(f"[Callback] Original args: {args}")

    if tool_name == 'get_capital_city' and args.get('country', '').lower() == 'canada':
        print("[Callback] Detected 'Canada'. Modifying args to 'France'.")
        args['country'] = 'France' # Modify in-place
        print(f"[Callback] Modified args: {args}")
        return None # Proceed with modified args

    if tool_name == 'get_capital_city' and args.get('country', '').upper() == 'BLOCK':
        print("[Callback] Detected 'BLOCK'. Skipping tool execution.")
        return {"result": "Tool execution was blocked by before_tool_callback."}

    print("[Callback] Proceeding with original or previously modified args.")
    return None

# my_llm_agent_before_tool = LlmAgent(
#     name="ToolCallbackAgent",
#     model=GEMINI_2_FLASH,
#     instruction="You are an agent that can find capital cities. Use the get_capital_city tool.",
#     description="An LLM agent demonstrating before_tool_callback",
#     tools=[capital_tool_for_cb],
#     before_tool_callback=simple_before_tool_modifier
# )
# async def main_before_tool():
#     # ... (Runner and session setup)
#     await call_agent(my_llm_agent_before_tool, "What is the capital of Canada?") # Will be changed to France
#     await call_agent(my_llm_agent_before_tool, "What is the capital of BLOCK?")   # Will be blocked
# if __name__ == "__main__":
#    asyncio.run(main_before_tool())
```
**Java Example:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.InvocationContext; // For callback signature
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.adk.tools.Annotations.Schema;
import com.google.adk.tools.BaseTool;
import com.google.adk.tools.FunctionTool;
import com.google.adk.tools.ToolContext;
import com.google.common.collect.ImmutableMap;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import io.reactivex.rxjava3.core.Maybe;

import java.util.HashMap;
import java.util.Map;

public class BeforeToolCallbackExample {
    private static final String APP_NAME_JAVA_BT = "ToolCbAgentAppJava";
    private static final String USER_ID_JAVA_BT = "user_bt_java";
    private static final String MODEL_NAME_JAVA_BT = "gemini-2.0-flash";

    public static void main(String[] args) {
        BeforeToolCallbackExample example = new BeforeToolCallbackExample();
        example.runAgent("capital of canada"); // Should be modified to France
        example.runAgent("capital of BLOCK"); // Should be blocked
    }

    public static Map<String, Object> getCapitalCity(
        @Schema(name = "country", description = "The country to find the capital of.") String country
    ) {
        System.out.printf("--- Tool 'getCapitalCity' executing with country: %s ---%n", country);
        Map<String, String> countryCapitals = new HashMap<>();
        countryCapitals.put("united states", "Washington, D.C.");
        countryCapitals.put("canada", "Ottawa");
        countryCapitals.put("france", "Paris");
        countryCapitals.put("germany", "Berlin");
        String capital = countryCapitals.getOrDefault(country.toLowerCase(), "Capital not```markdown
found for " + country);
        return ImmutableMap.of("capital", capital);
    }

    public Maybe<Map<String, Object>> simpleBeforeToolModifier(
        InvocationContext invocationContext, BaseTool tool, Map<String, Object> args, ToolContext toolContext
    ) {
        String agentName = invocationContext.agent().name(); // Correct way to get agent name from InvocationContext
        String toolName = tool.name();
        System.out.printf("[Callback] Before tool call for tool '%s' in agent '%s'%n", toolName, agentName);
        System.out.printf("[Callback] Original args: %s%n", args);

        if ("getCapitalCity".equals(toolName)) {
            String countryArg = (String) args.get("country");
            if (countryArg != null) {
                if ("canada".equalsIgnoreCase(countryArg)) {
                    System.out.println("[Callback] Detected 'Canada'. Modifying args to 'France'.");
                    args.put("country", "France"); // Args map is mutable here
                    System.out.printf("[Callback] Modified args: %s%n", args);
                    return Maybe.empty(); // Proceed with modified args
                } else if ("BLOCK".equalsIgnoreCase(countryArg)) {
                    System.out.println("[Callback] Detected 'BLOCK'. Skipping tool execution.");
                    return Maybe.just(ImmutableMap.of("result", "Tool execution was blocked by before_tool_callback."));
                }
            }
        }
        System.out.println("[Callback] Proceeding with original or previously modified args.");
        return Maybe.empty();
    }

    public void runAgent(String query) {
        FunctionTool capitalTool = FunctionTool.create(this.getClass(), "getCapitalCity");
        LlmAgent myLlmAgent = LlmAgent.builder()
            .name(APP_NAME_JAVA_BT) // Agent name
            .model(MODEL_NAME_JAVA_BT)
            .instruction("You are an agent that can find capital cities. Use the getCapitalCity tool.")
            .description("An LLM agent demonstrating before_tool_callback")
            .tools(capitalTool)
            .beforeToolCallback(this::simpleBeforeToolModifier)
            .build();

        InMemoryRunner runner = new InMemoryRunner(myLlmAgent, APP_NAME_JAVA_BT); // App name for runner
        Session session = runner.sessionService().createSession(APP_NAME_JAVA_BT, USER_ID_JAVA_BT).blockingGet();
        Content userMessage = Content.fromParts(Part.fromText(query));

        System.out.printf("%n--- Calling agent with query: \"%s\" ---%n", query);
        Flowable<Event> eventStream = runner.runAsync(USER_ID_JAVA_BT, session.id(), userMessage);
        eventStream.blockingForEach(event -> {
            if (event.finalResponse() && event.content().isPresent()) {
                 event.content().flatMap(Content::parts)
                    .filter(parts -> !parts.isEmpty() && parts.get(0).text().isPresent())
                    .ifPresent(parts -> System.out.println("Agent Response: " + parts.get(0).text().get()));
            }
        });
    }
}
```

##### After Tool Callback
*   **When**: Called just after the tool's `run_async` method completes successfully.
*   **Purpose**: Allows inspection and modification of the tool's result before it's sent back to the LLM (potentially after summarization). Useful for logging tool results, post-processing or formatting results, or saving specific parts of the result to the session state.
*   **Return Value Effect**:
    *   If the callback returns `None` (or a `Maybe.empty()` object in Java), the original `tool_response` is used.
    *   If a new dictionary is returned, it replaces the original `tool_response`. This allows modifying or filtering the result seen by the LLM.

**Python Example:**
```python
from google.adk.agents import LlmAgent
# from google.adk.runners import Runner
from typing import Optional, Dict, Any
# from google.genai import types
# from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool, BaseTool
from google.adk.tools.tool_context import ToolContext
from copy import deepcopy # Corrected import for deepcopy
# import asyncio

GEMINI_2_FLASH = "gemini-2.0-flash"

def get_capital_city_tool_after_cb(country: str) -> dict: # Renamed for clarity
    """Retrieves the capital city of a given country."""
    print(f"--- Tool 'get_capital_city_tool_after_cb' executing with country: {country} ---")
    country_capitals = {"united states": "Washington, D.C.", "canada": "Ottawa", "france": "Paris", "germany": "Berlin"}
    return {"result": country_capitals.get(country.lower(), f"Capital not found for {country}")}

capital_tool_for_after_cb = FunctionTool(func=get_capital_city_tool_after_cb, name="get_capital_city") # Explicit name


def simple_after_tool_modifier(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"[Callback] After tool call for tool '{tool_name}' in agent '{agent_name}'")
    print(f"[Callback] Args used: {args}")
    print(f"[Callback] Original tool_response: {tool_response}")

    original_result_value = tool_response.get("result", "")

    if tool_name == 'get_capital_city' and original_result_value == "Washington, D.C.":
        print("[Callback] Detected 'Washington, D.C.'. Modifying tool response.")
        modified_response = deepcopy(tool_response)
        modified_response["result"] = f"{original_result_value} (Note: This is the capital of the USA)."
        modified_response["note_added_by_callback"] = True
        print(f"[Callback] Modified tool_response: {modified_response}")
        return modified_response

    print("[Callback] Passing original tool response through.")
    return None

# my_llm_agent_after_tool = LlmAgent(
#     name="AfterToolCallbackAgent",
#     model=GEMINI_2_FLASH,
#     instruction="You are an agent that finds capital cities using the get_capital_city tool. Report the result clearly.",
#     description="An LLM agent demonstrating after_tool_callback",
#     tools=[capital_tool_for_after_cb],
#     after_tool_callback=simple_after_tool_modifier
# )
# async def main_after_tool():
#     # ... (Runner and session setup)
#     await call_agent(my_llm_agent_after_tool, "What is the capital of the United States?")
# if __name__ == "__main__":
#    asyncio.run(main_after_tool())
```
**Java Example:**
```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.InvocationContext;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.adk.tools.Annotations.Schema;
import com.google.adk.tools.BaseTool;
import com.google.adk.tools.FunctionTool;
import com.google.adk.tools.ToolContext;
import com.google.common.collect.ImmutableMap;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import io.reactivex.rxjava3.core.Maybe;

import java.util.HashMap;
import java.util.Map;

public class AfterToolCallbackExample {
    private static final String APP_NAME_JAVA_AT = "AfterToolCbAgentAppJava";
    private static final String USER_ID_JAVA_AT = "user_at_java";
    private static final String MODEL_NAME_JAVA_AT = "gemini-2.0-flash";

    public static void main(String[] args) {
        AfterToolCallbackExample example = new AfterToolCallbackExample();
        example.runAgent("What is the capital of the United States?");
        example.runAgent("What is the capital of France?"); // Should not be modified
    }

    @Schema(description = "Retrieves the capital city of a given country.")
    public static Map<String, Object> getCapitalCity(
        @Schema(description = "The country to find the capital of.") String country
    ) {
        System.out.printf("--- Tool 'getCapitalCity' executing with country: %s ---%n", country);
        Map<String, String> countryCapitals = new HashMap<>();
        countryCapitals.put("united states", "Washington, D.C.");
        countryCapitals.put("canada", "Ottawa");
        countryCapitals.put("france", "Paris");
        countryCapitals.put("germany", "Berlin");
        String capital = countryCapitals.getOrDefault(country.toLowerCase(), "Capital not found for " + country);
        return ImmutableMap.of("result", capital);
    }

    public Maybe<Map<String, Object>> simpleAfterToolModifier(
        InvocationContext invocationContext, BaseTool tool, Map<String, Object> args,
        ToolContext toolContext, Object toolResponse // Object type for toolResponse
    ) {
        String agentName = invocationContext.agent().name();
        String toolName = tool.name();
        System.out.printf("[Callback] After tool call for tool '%s' in agent '%s'%n", toolName, agentName);
        System.out.printf("[Callback] Args used: %s%n", args);
        System.out.printf("[Callback] Original tool_response: %s%n", toolResponse);

        if (!(toolResponse instanceof Map)) {
            System.out.println("[Callback] toolResponse is not a Map, cannot process further.");
            return Maybe.empty();
        }

        @SuppressWarnings("unchecked") // Safe cast after instanceof check
        Map<String, Object> responseMap = (Map<String, Object>) toolResponse;
        Object originalResultValue = responseMap.get("result");

        if ("getCapitalCity".equals(toolName) && "Washington, D.C.".equals(originalResultValue)) {
            System.out.println("[Callback] Detected 'Washington, D.C.'. Modifying tool response.");
            Map<String, Object> modifiedResponse = new HashMap<>(responseMap);
            modifiedResponse.put("result", originalResultValue + " (Note: This is the capital of the USA).");
            modifiedResponse.put("note_added_by_callback", true);
            System.out.printf("[Callback] Modified tool_response: %s%n", modifiedResponse);
            return Maybe.just(modifiedResponse);
        }

        System.out.println("[Callback] Passing original tool response through.");
        return Maybe.empty();
    }

    public void runAgent(String query) {
        FunctionTool capitalTool = FunctionTool.create(this.getClass(), "getCapitalCity");
        LlmAgent myLlmAgent = LlmAgent.builder()
            .name(APP_NAME_JAVA_AT)
            .model(MODEL_NAME_JAVA_AT)
            .instruction("You are an agent that finds capital cities using the getCapitalCity tool. Report the result clearly.")
            .description("An LLM agent demonstrating after_tool_callback")
            .tools(capitalTool)
            .afterToolCallback(this::simpleAfterToolModifier)
            .build();

        InMemoryRunner runner = new InMemoryRunner(myLlmAgent, APP_NAME_JAVA_AT);
        Session session = runner.sessionService().createSession(APP_NAME_JAVA_AT, USER_ID_JAVA_AT).blockingGet();
        Content userMessage = Content.fromParts(Part.fromText(query));

        System.out.printf("%n--- Calling agent with query: \"%s\" ---%n", query);
        Flowable<Event> eventStream = runner.runAsync(USER_ID_JAVA_AT, session.id(), userMessage);
        eventStream.blockingForEach(event -> {
            if (event.finalResponse() && event.content().isPresent()) {
                 event.content().flatMap(Content::parts)
                    .filter(parts -> !parts.isEmpty() && parts.get(0).text().isPresent())
                    .ifPresent(parts -> System.out.println("Agent Response: " + parts.get(0).text().get()));
            }
        });
    }
}
```

### Design Patterns and Best Practices for Callbacks
Callbacks offer powerful hooks into the agent lifecycle. Here are common design patterns illustrating how to leverage them effectively in ADK, followed by best practices for implementation.

#### Design Patterns
These patterns demonstrate typical ways to enhance or control agent behavior using callbacks:

1.  **Guardrails & Policy Enforcement**
    *   **Pattern**: Intercept requests before they reach the LLM or tools to enforce rules.
    *   **How**: Use `before_model_callback` to inspect the `LlmRequest` prompt or `before_tool_callback` to inspect tool arguments. If a policy violation is detected (e.g., forbidden topics, profanity), return a predefined response (`LlmResponse` or `dict`/`Map`) to block the operation and optionally update `context.state` to log the violation.
    *   **Example**: A `before_model_callback` checks `llm_request.contents` for sensitive keywords and returns a standard "Cannot process this request" `LlmResponse` if found, preventing the LLM call.
2.  **Dynamic State Management**
    *   **Pattern**: Read from and write to session state within callbacks to make agent behavior context-aware and pass data between steps.
    *   **How**: Access `callback_context.state` or `tool_context.state`. Modifications (`state['key'] = value`) are automatically tracked in the subsequent `Event.actions.state_delta` for persistence by the `SessionService`.
    *   **Example**: An `after_tool_callback` saves a `transaction_id` from the tool's result to `tool_context.state['last_transaction_id']`. A later `before_agent_callback` might read `state['user_tier']` to customize the agent's greeting.
3.  **Logging and Monitoring**
    *   **Pattern**: Add detailed logging at specific lifecycle points for observability and debugging.
    *   **How**: Implement callbacks (e.g., `before_agent_callback`, `after_tool_callback`, `after_model_callback`) to print or send structured logs containing information like agent name, tool name, invocation ID, and relevant data from the context or arguments.
    *   **Example**: Log messages like `INFO: [Invocation: e-123] Before Tool: search_api - Args: {'query': 'ADK'}`.
4.  **Caching**
    *   **Pattern**: Avoid redundant LLM calls or tool executions by caching results.
    *   **How**: In `before_model_callback` or `before_tool_callback`, generate a cache key based on the request/arguments. Check `context.state` (or an external cache) for this key. If found, return the cached `LlmResponse` or result directly, skipping the actual operation. If not found, allow the operation to proceed and use the corresponding `after_` callback (`after_model_callback`, `after_tool_callback`) to store the new result in the cache using the key.
    *   **Example**: `before_tool_callback` for `get_stock_price(symbol)` checks `state[f"cache:stock:{symbol}"]`. If present, returns the cached price; otherwise, allows the API call and `after_tool_callback` saves the result to the state key.
5.  **Request/Response Modification**
    *   **Pattern**: Alter data just before it's sent to the LLM/tool or just after it's received.
    *   **How**:
        *   `before_model_callback`: Modify `llm_request` (e.g., add system instructions based on `state`).
        *   `after_model_callback`: Modify the returned `LlmResponse` (e.g., format text, filter content).
        *   `before_tool_callback`: Modify the tool `args` dictionary (or `Map` in Java).
        *   `after_tool_callback`: Modify the `tool_response` dictionary (or `Map` in Java).
    *   **Example**: `before_model_callback` appends "User language preference: Spanish" to `llm_request.config.system_instruction` if `context.state['lang'] == 'es'`.
6.  **Conditional Skipping of Steps**
    *   **Pattern**: Prevent standard operations (agent run, LLM call, tool execution) based on certain conditions.
    *   **How**: Return a value from a `before_` callback (`Content` from `before_agent_callback`, `LlmResponse` from `before_model_callback`, `dict` from `before_tool_callback`). The framework interprets this returned value as the result for that step, skipping the normal execution.
    *   **Example**: `before_tool_callback` checks `tool_context.state['api_quota_exceeded']`. If `True`, it returns `{'error': 'API quota exceeded'}`, preventing the actual tool function from running.
7.  **Tool-Specific Actions (Authentication & Summarization Control)**
    *   **Pattern**: Handle actions specific to the tool lifecycle, primarily authentication and controlling LLM summarization of tool results.
    *   **How**: Use `ToolContext` within tool callbacks (`before_tool_callback`, `after_tool_callback`).
        *   **Authentication**: Call `tool_context.request_credential(auth_config)` in `before_tool_callback` if credentials are required but not found (e.g., via `tool_context.get_auth_response` or state check). This initiates the auth flow.
        *   **Summarization**: Set `tool_context.actions.skip_summarization = True` if the raw dictionary output of the tool should be passed back to the LLM or potentially displayed directly, bypassing the default LLM summarization step.
    *   **Example**: A `before_tool_callback` for a secure API checks for an auth token in state; if missing, it calls `request_credential`. An `after_tool_callback` for a tool returning structured JSON might set `skip_summarization = True`.
8.  **Artifact Handling**
    *   **Pattern**: Save or load session-related files or large data blobs during the agent lifecycle.
    *   **How**: Use `callback_context.save_artifact` / `await tool_context.save_artifact` to store data (e.g., generated reports, logs, intermediate data). Use `load_artifact` to retrieve previously stored artifacts. Changes are tracked via `Event.actions.artifact_delta`.
    *   **Example**: An `after_tool_callback` for a "generate_report" tool saves the output file using `await tool_context.save_artifact("report.pdf", report_part)`. A `before_agent_callback` might load a configuration artifact using `callback_context.load_artifact("agent_config.json")`.

#### Best Practices for Callbacks
*   **Keep Focused**: Design each callback for a single, well-defined purpose (e.g., just logging, just validation). Avoid monolithic callbacks.
*   **Mind Performance**: Callbacks execute synchronously within the agent's processing loop. Avoid long-running or blocking operations (network calls, heavy computation). Offload if necessary, but be aware this adds complexity.
*   **Handle Errors Gracefully**: Use `try...except`/`catch` blocks within your callback functions. Log errors appropriately and decide if the agent invocation should halt or attempt recovery. Don't let callback errors crash the entire process.
*   **Manage State Carefully**: Be deliberate about reading from and writing to `context.state`. Changes are immediately visible within the current invocation and persisted at the end of the event processing. Use specific state keys rather than modifying broad structures to avoid unintended side effects. Consider using state prefixes (`State.APP_PREFIX`, `State.USER_PREFIX`, `State.TEMP_PREFIX`) for clarity, especially with persistent `SessionService` implementations.
*   **Consider Idempotency**: If a callback performs actions with external side effects (e.g., incrementing an external counter), design it to be idempotent (safe to run multiple times with the same input) if possible, to handle potential retries in the framework or your application.
*   **Test Thoroughly**: Unit test your callback functions using mock context objects. Perform integration tests to ensure callbacks function correctly within the full agent flow.
*   **Ensure Clarity**: Use descriptive names for your callback functions. Add clear docstrings explaining their purpose, when they run, and any side effects (especially state modifications).
*   **Use Correct Context Type**: Always use the specific context type provided (`CallbackContext` for agent/model, `ToolContext` for tools) to ensure access to the appropriate methods and properties.

By applying these patterns and best practices, you can effectively use callbacks to create more robust, observable, and customized agent behaviors in ADK.

## 8. Runtime and Context
### Runtime
#### What is runtime?
The ADK Runtime is the underlying engine that powers your agent application during user interactions. It's the system that takes your defined agents, tools, and callbacks and orchestrates their execution in response to user input, managing the flow of information, state changes, and interactions with external services like LLMs or storage.
Think of the Runtime as the "engine" of your agentic application. You define the parts (agents, tools), and the Runtime handles how they connect and run together to fulfill a user's request.

#### Core Idea: The Event Loop
At its heart, the ADK Runtime operates on an **Event Loop**. This loop facilitates a back-and-forth communication between the `Runner` component and your defined "Execution Logic" (which includes your Agents, the LLM calls they make, Callbacks, and Tools).

In simple terms:
1.  The `Runner` receives a user query and asks the main `Agent` to start processing.
2.  The `Agent` (and its associated logic) runs until it has something to report (like a response, a request to use a tool, or a state change) – it then `yields` or emits an `Event`.
3.  The `Runner` receives this `Event`, processes any associated actions (like saving state changes via `Services`), and forwards the event onwards (e.g., to the user interface).
4.  Only after the `Runner` has processed the event does the `Agent`'s logic resume from where it paused, now potentially seeing the effects of the changes committed by the `Runner`.
This cycle repeats until the agent has no more events to yield for the current user query.
This event-driven loop is the fundamental pattern governing how ADK executes your agent code.

#### The Heartbeat: The Event Loop - Inner workings
The Event Loop is the core operational pattern defining the interaction between the `Runner` and your custom code (Agents, Tools, Callbacks, collectively referred to as "Execution Logic" or "Logic Components" in the design document). It establishes a clear division of responsibilities:
**Note**: The specific method names and parameter names may vary slightly by SDK language (e.g., `agent_to_run.runAsync(...)` in Java, `agent_to_run.run_async(...)` in Python). Refer to the language-specific API documentation for details.

##### `Runner`'s Role (Orchestrator)
The `Runner` acts as the central coordinator for a single user invocation. Its responsibilities in the loop are:
1.  **Initiation**: Receives the end user's query (`new_message`) and typically appends it to the session history via the `SessionService`.
2.  **Kick-off**: Starts the event generation process by calling the main agent's execution method (e.g., `agent_to_run.run_async(...)`).
3.  **Receive & Process**: Waits for the agent logic to `yield` or emit an `Event`. Upon receiving an event, the `Runner` promptly processes it. This involves:
    *   Using configured `Services` (`SessionService`, `ArtifactService`, `MemoryService`) to commit changes indicated in `event.actions` (like `state_delta`, `artifact_delta`).
    *   Performing other internal bookkeeping.
4.  **Yield Upstream**: Forwards the processed event onwards (e.g., to the calling application or UI for rendering).
5.  **Iterate**: Signals the agent logic that processing is complete for the yielded event, allowing it to resume and generate the next event.

**Conceptual Python Runner Loop:**
```python
# Simplified view of Runner's main loop logic
# def run(new_query, ...) -> Generator[Event]:
#     # 1. Append new_query to session event history (via SessionService)
#     session_service.append_event(session, Event(author='user', content=new_query))
#
#     # 2. Kick off event loop by calling the agent
#     agent_event_generator = agent_to_run.run_async(context)
#     async for event in agent_event_generator:
#         # 3. Process the generated event and commit changes
#         session_service.append_event(session, event) # Commits state/artifact deltas etc.
#         # memory_service.update_memory(...) # If applicable
#         # artifact_service might have already been called via context during agent run
#
#         # 4. Yield event for upstream processing (e.g., UI rendering)
#         yield event
#     # Runner implicitly signals agent generator can continue after yielding
```
**Conceptual Java Runner Loop:**
```java
// Simplified conceptual view of the Runner's main loop logic in Java.
// public Flowable<Event> runConceptual(Session session, InvocationContext invocationContext, Content newQuery) {
//     // 1. Append new_query to session event history (via SessionService)
//     // ... sessionService.appendEvent(session, userEvent).blockingGet();
//
//     // 2. Kick off event stream by calling the agent
//     Flowable<Event> agentEventStream = agentToRun.runAsync(invocationContext);
//
//     // 3. Process each generated event, commit changes, and "yield" or "emit"
//     return agentEventStream.map(event -> {
//         // This mutates the session object (adds event, applies stateDelta).
//         // The return value of appendEvent (a Single<Event>) is conceptually
//         // just the event itself after processing.
//         sessionService.appendEvent(session, event).blockingGet(); // Simplified blocking call
//         // memory_service.update_memory(...) // If applicable - conceptual
//         // artifact_service might have already been called via context during agent run
//
//         // 4. "Yield" event for upstream processing
//         //    In RxJava, returning the event in map effectively yields it to the next operator or subscriber.
//         return event;
//     });
// }
```

##### Execution Logic's Role (Agent, Tool, Callback)
Your code within agents, tools, and callbacks is responsible for the actual computation and decision-making. Its interaction with the loop involves:
1.  **Execute**: Runs its logic based on the current `InvocationContext`, including the session state *as it was when execution resumed*.
2.  **Yield**: When the logic needs to communicate (send a message, call a tool, report a state change), it constructs an `Event` containing the relevant content and actions, and then `yield`s this event back to the `Runner`.
3.  **Pause**: Crucially, execution of the agent logic pauses immediately after the `yield` statement (or `return` in RxJava). It waits for the `Runner` to complete step 3 (processing and committing).
4.  **Resume**: Only after the `Runner` has processed the yielded event does the agent logic resume execution from the statement immediately following the `yield`.
5.  **See Updated State**: Upon resumption, the agent logic can now reliably access the session state (`ctx.session.state`) reflecting the changes that were committed by the `Runner` from the previously yielded event.

**Conceptual Python Execution Logic:**
```python
# Simplified view of logic inside Agent.run_async, callbacks, or tools
# ... previous code runs based on current state ...

# 1. Determine a change or output is needed, construct the event
# Example: Updating state
# update_data = {'field_1': 'value_2'}
# event_with_state_change = Event(
#     author=self.name,
#     actions=EventActions(state_delta=update_data),
#     content=types.Content(parts=[types.Part(text="State updated.")])
#     # ... other event fields ...
# )

# 2. Yield the event to the Runner for processing & commit
# yield event_with_state_change
# # <<<<<<<<<<<< EXECUTION PAUSES HERE >>>>>>>>>>>>
# # <<<<<<<<<<<< RUNNER PROCESSES & COMMITS THE EVENT >>>>>>>>>>>>

# 3. Resume execution ONLY after Runner is done processing the above event.
# Now, the state committed by the Runner is reliably reflected.
# Subsequent code can safely assume the change from the yielded event happened.
# val = ctx.session.state['field_1'] # here `val` is guaranteed to be "value_2"
# print(f"Resumed execution. Value of field_1 is now: {val}")
# ... subsequent code continues ...
# Maybe yield another event later...
```
**Conceptual Java Execution Logic:**
```java
// Simplified view of logic inside Agent.runAsync, callbacks, or tools
// ... previous code runs based on current state ...

// 1. Determine a change or output is needed, construct the event
// Example: Updating state
// ConcurrentMap<String, Object> updateData = new ConcurrentHashMap<>();
// updateData.put("field_1", "value_2");
// EventActions actions = EventActions.builder().stateDelta(updateData).build();
// Content eventContent = Content.builder().parts(Part.fromText("State updated.")).build();
// Event eventWithStateChange = Event.builder()
//     .author(self.name()) // Assuming self.name() or equivalent
//     .actions(actions)
//     .content(Optional.of(eventContent))
//     // ... other event fields ...
//     .build();

// 2. "Yield" the event. In RxJava, this means emitting it into the stream.
//    The Runner (or upstream consumer) will subscribe to this Flowable.
//    When the Runner receives this event, it will process it (e.g., call sessionService.appendEvent).
//    The 'appendEvent' in Java ADK mutates the 'Session' object held within 'ctx' (InvocationContext).
//
// return Flowable.just(eventWithStateChange) // Step 2: Yield the event
//     .concatMap(yieldedEvent -> {
//         // <<<<<<<<<<<< RUNNER CONCEPTUALLY PROCESSES & COMMITS THE EVENT >>>>>>>>>>>>
//         // At this point, in a real runner, ctx.session().appendEvent(yieldedEvent) would have been called
//         // by the Runner, and ctx.session().state() would be updated.
//         // Since we are *inside* the agent's conceptual logic trying to model this,
//         // we assume the Runner's action has implicitly updated our 'ctx.session()'.
//
//         // 3. Resume execution.
//         // Now, the state committed by the Runner (via sessionService.appendEvent)
//         // is reliably reflected in ctx.session().state().
//         Object val = ctx.session().state().get("field_1"); // here `val` is guaranteed to be "value_2"
//         System.out.println("Resumed execution. Value of field_1 is now: " + val);
//         // ... subsequent code continues ...
//         // If this subsequent logic needs to yield another event, it would do so here.
//         return Flowable.just(yieldedEvent); // Or a new event
//     });
```
This cooperative yield/pause/resume cycle between the `Runner` and your Execution Logic, mediated by `Event` objects, forms the core of the ADK Runtime.

#### Key components of the Runtime
Several components work together within the ADK Runtime to execute an agent invocation. Understanding their roles clarifies how the event loop functions:
*   **`Runner`**:
    *   **Role**: The main entry point and orchestrator for a single user query (`run_async`).
    *   **Function**: Manages the overall Event Loop, receives events yielded by the Execution Logic, coordinates with `Services` to process and commit event actions (state/artifact changes), and forwards processed events upstream (e.g., to the UI). It essentially drives the conversation turn by turn based on yielded events. (Defined in `google.adk.runners.runner`).
*   **Execution Logic Components**:
    *   **Role**: The parts containing your custom code and the core agent capabilities.
    *   **Components**:
        *   **Agent** (`BaseAgent`, `LlmAgent`, etc.): Your primary logic units that process information and decide on actions. They implement the `_run_async_impl` method which yields events.
        *   **Tools** (`BaseTool`, `FunctionTool`, `AgentTool`, etc.): External functions or capabilities used by agents (often `LlmAgent`) to interact with the outside world or perform specific tasks. They execute and return results, which are then wrapped in events.
        *   **Callbacks** (Functions): User-defined functions attached to agents (e.g., `before_agent_callback`, `after_model_callback`) that hook into specific points in the execution flow, potentially modifying behavior or state, whose effects are captured in events.
    *   **Function**: Perform the actual thinking, calculation, or external interaction. They communicate their results or needs by yielding `Event` objects and pausing until the `Runner` processes them.
*   **`Event`**:
    *   **Role**: The message passed back and forth between the `Runner` and the Execution Logic.
    *   **Function**: Represents an atomic occurrence (user input, agent text, tool call/result, state change request, control signal). It carries both the content of the occurrence and the intended side effects (`actions` like `state_delta`).
*   **`Services`**:
    *   **Role**: Backend components responsible for managing persistent or shared resources. Used primarily by the `Runner` during event processing.
    *   **Components**:
        *   **`SessionService`** (`BaseSessionService`, `InMemorySessionService`, etc.): Manages `Session` objects, including saving/loading them, applying `state_delta` to the session state, and appending events to the event history.
        *   **`ArtifactService`** (`BaseArtifactService`, `InMemoryArtifactService`, `GcsArtifactService`, etc.): Manages the storage and retrieval of binary artifact data. Although `save_artifact` is called via context during execution logic, the `artifact_delta` in the event confirms the action for the `Runner`/`SessionService`.
        *   **`MemoryService`** (`BaseMemoryService`, etc.): (Optional) Manages long-term semantic memory across sessions for a user.
    *   **Function**: Provide the persistence layer. The `Runner` interacts with them to ensure changes signaled by `event.actions` are reliably stored before the Execution Logic resumes.
*   **`Session`**:
    *   **Role**: A data container holding the state and history for one specific conversation between a user and the application.
    *   **Function**: Stores the current `state` dictionary, the list of all past `events` (event history), and references to associated artifacts. It's the primary record of the interaction, managed by the `SessionService`.
*   **`Invocation`**:
    *   **Role**: A conceptual term representing everything that happens in response to a single user query, from the moment the `Runner` receives it until the agent logic finishes yielding events for that query.
    *   **Function**: An invocation might involve multiple agent runs (if using agent transfer or `AgentTool`), multiple LLM calls, tool executions, and callback executions, all tied together by a single `invocation_id` within the `InvocationContext`.

These players interact continuously through the Event Loop to process a user's request.

#### How It Works: A Simplified Invocation
Let's trace a simplified flow for a typical user query that involves an LLM agent calling a tool:

##### Step-by-Step Breakdown
1.  **User Input**: The User sends a query (e.g., "What's the capital of France?").
2.  **`Runner` Starts**: `Runner.run_async` begins. It interacts with the `SessionService` to load the relevant `Session` and adds the user query as the first `Event` to the session history. An `InvocationContext` (`ctx`) is prepared.
3.  **Agent Execution**: The `Runner` calls `agent.run_async(ctx)` on the designated root agent (e.g., an `LlmAgent`).
4.  **LLM Call (Example)**: The `Agent_Llm` determines it needs information, perhaps by calling a tool. It prepares a request for the LLM. Let's assume the LLM decides to call `MyTool`.
5.  **Yield `FunctionCall` Event**: The `Agent_Llm` receives the `FunctionCall` response from the LLM, wraps it in an `Event(author='Agent_Llm', content=Content(parts=[Part(function_call=...)]))`, and `yields` or `emits` this event.
6.  **Agent Pauses**: The `Agent_Llm`'s execution pauses immediately after the `yield`.
7.  **`Runner` Processes**: The `Runner` receives the `FunctionCall` event. It passes it to the `SessionService` to record it in the history. The `Runner` then `yields` the event upstream to the User (or application).
8.  **Agent Resumes**: The `Runner` signals that the event is processed, and `Agent_Llm` resumes execution.
9.  **Tool Execution**: The `Agent_Llm`'s internal flow now proceeds to execute the requested `MyTool`. It calls `tool.run_async(...)`.
10. **Tool Returns Result**: `MyTool` executes and returns its result (e.g., `{'result': 'Paris'}`).
11. **Yield `FunctionResponse` Event**: The agent (`Agent_Llm`) wraps the tool result into an `Event` containing a `FunctionResponse` part (e.g., `Event(author='Agent_Llm', content=Content(role='user', parts=[Part(function_response=...)]))`). This event might also contain `actions` if the tool modified state (`state_delta`) or saved artifacts (`artifact_delta`). The agent `yields` this event.
12. **Agent Pauses**: `Agent_Llm` pauses again.
13. **`Runner` Processes**: `Runner` receives the `FunctionResponse` event. It passes it to `SessionService` which applies any `state_delta` / `artifact_delta` and adds the event to history. `Runner` `yields` the event upstream.
14. **Agent Resumes**: `Agent_Llm` resumes, now knowing the tool result and any state changes are committed.
15. **Final LLM Call (Example)**: `Agent_Llm` sends the tool result back to the LLM to generate a natural language response.
16. **Yield Final Text Event**: `Agent_Llm` receives the final text from the LLM, wraps it in an `Event(author='Agent_Llm', content=Content(parts=[Part(text=...)]))`, and `yields` it.
17. **Agent Pauses**: `Agent_Llm` pauses.
18. **`Runner` Processes**: `Runner` receives the final text event, passes it to `SessionService` for history, and `yields` it upstream to the User. This is likely marked as the `is_final_response()`.
19. **Agent Resumes & Finishes**: `Agent_Llm` resumes. Having completed its task for this invocation, its `run_async` generator finishes.
20. **`Runner` Completes**: The `Runner` sees the agent's generator is exhausted and finishes its loop for this invocation.

This yield/pause/process/resume cycle ensures that state changes are consistently applied and that the execution logic always operates on the most recently committed state after yielding an event.

#### Important Runtime Behaviors
Understanding a few key aspects of how the ADK Runtime handles state, streaming, and asynchronous operations is crucial for building predictable and efficient agents.

##### State Updates & Commitment Timing
*   **The Rule**: When your code (in an agent, tool, or callback) modifies the session state (e.g., `context.state['my_key'] = 'new_value'`), this change is initially recorded locally within the current `InvocationContext`. The change is only guaranteed to be persisted (saved by the `SessionService`) after the `Event` carrying the corresponding `state_delta` in its `actions` has been `yield`-ed by your code and subsequently processed by the `Runner`.
*   **Implication**: Code that runs *after* resuming from a `yield` can reliably assume that the state changes signaled in the yielded event have been committed.
    **Python Conceptual Example:**
    ```python
    # Inside agent logic (conceptual)
    # 1. Modify state
    # ctx.session.state['status'] = 'processing'
    # event1 = Event(..., actions=EventActions(state_delta={'status': 'processing'}))
    # # 2. Yield event with the delta
    # yield event1
    # # --- PAUSE --- Runner processes event1, SessionService commits 'status' = 'processing' ---
    # # 3. Resume execution
    # # Now it's safe to rely on the committed state
    # current_status = ctx.session.state['status']  # Guaranteed to be 'processing'
    # print(f"Status after resuming: {current_status}")
    ```
    **Java Conceptual Example:**
    ```java
    // Inside agent logic (conceptual)
    // // ... previous code runs based on current state ...
    // // 1. Prepare state modification and construct the event
    // ConcurrentHashMap<String, Object> stateChanges = new ConcurrentHashMap<>();
    // stateChanges.put("status", "processing");
    // EventActions actions = EventActions.builder().stateDelta(stateChanges).build();
    // Content content = Content.builder().parts(Part.fromText("Status update: processing")).build();
    // Event event1 = Event.builder().actions(actions) /* ... */ .build();
    //
    // // 2. Yield event with the delta
    // return Flowable.just(event1)
    //     .map(emittedEvent -> {
    //         // --- CONCEPTUAL PAUSE & RUNNER PROCESSING ---
    //         // 3. Resume execution (conceptually)
    //         // Now it's safe to rely on the committed state.
    //         String currentStatus = (String) ctx.session().state().get("status");
    //         System.out.println("Status after resuming (inside agent logic): " + currentStatus); // Guaranteed to be 'processing'
    //         // The event itself (event1) is passed on.
    //         // If subsequent logic within this agent step produced *another* event,
    //         // you'd use concatMap to emit that new event.
    //         return emittedEvent;
    //     });
    // // ... subsequent agent logic might involve further reactive operators
    // // or emitting more events based on the now-updated `ctx.session().state()`.
    ```

##### "Dirty Reads" of Session State
*   **Definition**: While commitment happens *after* the `yield`, code running *later within the same invocation*, but *before* the state-changing event is actually yielded and processed, can often see the local, uncommitted changes. This is sometimes called a "dirty read".
    **Python Example:**
    ```python
    # Code in before_agent_callback
    # callback_context.state['field_1'] = 'value_1'  # State is locally set
    # ... agent runs ...
    # Code in a tool called later *within the same invocation*
    # val = tool_context.state['field_1']  # 'val' will likely be 'value_1' here
    # print(f"Dirty read value in tool: {val}")
    # Assume the event carrying the state_delta={'field_1': 'value_1'}
    # is yielded *after* this tool runs and is processed by the Runner.
    ```
    **Java Example:**
    ```java
    // // Modify state - Code in BeforeAgentCallback
    // // AND stages this change in callbackContext.eventActions().stateDelta().
    // callbackContext.state().put("field_1", "value_1");
    // // --- agent runs ... ---
    // // --- Code in a tool called later *within the same invocation* ---
    // // Readable (dirty read), but 'value_1' isn't guaranteed persistent yet.
    // Object val = toolContext.state().get("field_1"); // 'val' will likely be 'value_1' here
    // System.out.println("Dirty read value in tool: " + val);
    // // Assume the event carrying the state_delta={'field_1': 'value_1'}
    // // is yielded *after* this tool runs and is processed by the Runner.
    ```
*   **Implications**:
    *   **Benefit**: Allows different parts of your logic within a single complex step (e.g., multiple callbacks or tool calls before the next LLM turn) to coordinate using state without waiting for a full yield/commit cycle.
    *   **Caveat**: Relying heavily on dirty reads for critical logic can be risky. If the invocation fails before the event carrying the `state_delta` is yielded and processed by the `Runner`, the uncommitted state change will be lost. For critical state transitions, ensure they are associated with an event that gets successfully processed.

##### Streaming vs. Non-Streaming Output (`partial=True`)
This primarily relates to how responses from the LLM are handled, especially when using streaming generation APIs.
*   **Streaming**: The LLM generates its response token-by-token or in small chunks.
    *   The framework (often within `BaseLlmFlow`) `yields` multiple `Event` objects for a single conceptual response. Most of these events will have `partial=True`.
    *   The `Runner`, upon receiving an event with `partial=True`, typically forwards it immediately upstream (for UI display) but skips processing its `actions` (like `state_delta`).
    *   Eventually, the framework `yields` a final event for that response, marked as non-partial (`partial=False` or implicitly via `turn_complete=True`).
    *   The `Runner` fully processes only this final event, committing any associated `state_delta` or `artifact_delta`.
*   **Non-Streaming**: The LLM generates the entire response at once. The framework `yields` a single event marked as non-partial, which the `Runner` processes fully.
*   **Why it Matters**: Ensures that state changes are applied atomically and only once based on the complete response from the LLM, while still allowing the UI to display text progressively as it's generated.

##### Async is Primary (`run_async`)
*   **Core Design**: The ADK Runtime is fundamentally built on asynchronous libraries (like Python's `asyncio` and Java's RxJava) to handle concurrent operations (like waiting for LLM responses or tool executions) efficiently without blocking.
*   **Main Entry Point**: `Runner.run_async` is the primary method for executing agent invocations. All core runnable components (Agents, specific flows) use asynchronous methods internally.
*   **Synchronous Convenience (`run`)**: A synchronous `Runner.run` method exists mainly for convenience (e.g., in simple scripts or testing environments). However, internally, `Runner.run` typically just calls `Runner.run_async` and manages the async event loop execution for you.
*   **Developer Experience**: We recommend designing your applications (e.g., web servers using ADK) to be asynchronous for best performance. In Python, this means using `asyncio`; in Java, leverage RxJava's reactive programming model.
*   **Sync Callbacks/Tools**: The ADK framework supports both asynchronous and synchronous functions for tools and callbacks.
    *   **Blocking I/O**: For long-running synchronous I/O operations, the framework attempts to prevent stalls. Python ADK may use `asyncio.to_thread`, while Java ADK often relies on appropriate RxJava schedulers or wrappers for blocking calls.
    *   **CPU-Bound Work**: Purely CPU-intensive synchronous tasks will still block their execution thread in both environments.

Understanding these behaviors helps you write more robust ADK applications and debug issues related to state consistency, streaming updates, and asynchronous execution.

### Runtime Configuration (`RunConfig`)
`RunConfig` defines runtime behavior and options for agents in the ADK. It controls speech and streaming settings, function calling, artifact saving, and limits on LLM calls.
When constructing an agent run, you can pass a `RunConfig` to customize how the agent interacts with models, handles audio, and streams responses. By default, no streaming is enabled and inputs aren’t retained as artifacts. Use `RunConfig` to override these defaults.

#### Class Definition
The `RunConfig` class holds configuration parameters for an agent's runtime behavior.
Python ADK uses Pydantic for this validation. Java ADK typically uses immutable data classes.

**Python:**
```python
class RunConfig(BaseModel):
    """Configs for runtime behavior of agents."""
    model_config = ConfigDict(extra='forbid',)
    speech_config: Optional[types.SpeechConfig] = None
    response_modalities: Optional[list[str]] = None
    save_input_blobs_as_artifacts: bool = False
    support_cfc: bool = False # Experimental
    streaming_mode: StreamingMode = StreamingMode.NONE
    output_audio_transcription: Optional[types.AudioTranscriptionConfig] = None
    max_llm_calls: int = 500
```
**Java:**
```java
public abstract class RunConfig {
    public enum StreamingMode { NONE, SSE, BIDI }
    public abstract @Nullable SpeechConfig speechConfig();
    public abstract ImmutableList<Modality> responseModalities();
    public abstract boolean saveInputBlobsAsArtifacts();
    public abstract @Nullable AudioTranscriptionConfig outputAudioTranscription();
    public abstract int maxLlmCalls();
    // ... (builder and other methods)
}
```

#### Runtime Parameters

| Parameter                       | Python Type                                | Java Type                                    | Default (Python)     | Default (Java)       | Description                                                                                                                                                                      |
| ------------------------------- | ------------------------------------------ | -------------------------------------------- | -------------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `speech_config`                 | `Optional[types.SpeechConfig]`             | `@Nullable SpeechConfig`                     | `None`               | `null`               | Speech configuration settings for live agents. See details below.                                                                                                                |
| `response_modalities`           | `Optional[list[str]]`                      | `ImmutableList<Modality>`                    | `None` (defaults to `["TEXT"]` internally) | `ImmutableList.of()` (defaults to `TEXT` internally if not set) | Output modalities for the agent (e.g., "TEXT", "AUDIO").                                                                                                                         |
| `save_input_blobs_as_artifacts` | `bool`                                     | `boolean`                                    | `False`              | `false`              | If `True`, input blobs are saved as artifacts. Useful for debugging.                                                                                                             |
| `streaming_mode`                | `StreamingMode`                            | `StreamingMode`                              | `StreamingMode.NONE` | `StreamingMode.NONE` | Configures streaming behavior: `NONE`, `SSE` (Server-Sent Events), `BIDI` (Bidirectional).                                                                                         |
| `output_audio_transcription`    | `Optional[types.AudioTranscriptionConfig]` | `@Nullable AudioTranscriptionConfig`         | `None`               | `null`               | Configuration for transcribing audio outputs from live agents.                                                                                                                   |
| `max_llm_calls`                 | `int`                                      | `int`                                        | `500`                | `500`                | Limit on LLM calls per run. `0` or less means unbounded (not recommended). Values too large (e.g., `sys.maxsize`) may be disallowed.                                            |
| `support_cfc`                   | `bool` (Python only)                       | N/A                                          | `False`              | N/A                  | (Experimental) Enables Compositional Function Calling. Only applicable when `streaming_mode=SSE`. The LIVE API will be invoked.                                                    |

##### `speech_config` Details
The `SpeechConfig` class has the following structure (Python example, Java is analogous):
```python
class SpeechConfig(_common.BaseModel):
    """The speech generation configuration."""
    voice_config: Optional[VoiceConfig] = Field(
        default=None,
        description="""The configuration for the speaker to use."""
    )
    language_code: Optional[str] = Field(
        default=None,
        description="""Language code (ISO 639. e.g. en-US) for the speech synthesization.
        Only available for Live API."""
    )

class VoiceConfig(_common.BaseModel):
    """The configuration for the voice to use."""
    prebuilt_voice_config: Optional[PrebuiltVoiceConfig] = Field(
        default=None,
        description="""The configuration for the speaker to use."""
    )

class PrebuiltVoiceConfig(_common.BaseModel):
    """The configuration for the prebuilt speaker to use."""
    voice_name: Optional[str] = Field(
        default=None,
        description="""The name of the prebuilt voice to use."""
    )
```
These nested configuration classes allow you to specify:
*   `voice_config`: The name of the prebuilt voice to use (in the `PrebuiltVoiceConfig`)
*   `language_code`: ISO 639 language code (e.g., "en-US") for speech synthesis

When implementing voice-enabled agents, configure these parameters to control how your agent sounds when speaking.

##### Warning for `support_cfc`
The `support_cfc` feature is experimental and its API or behavior might change in future releases.

#### Examples

##### Basic runtime configuration
**Python:**
```python
from google.adk.agents.run_config import RunConfig, StreamingMode # Corrected import
config = RunConfig(
    streaming_mode=StreamingMode.NONE,
    max_llm_calls=100
)
```
**Java:**
```java
import com.google.adk.agents.RunConfig;
import com.google.adk.agents.RunConfig.StreamingMode;

RunConfig config = RunConfig.builder()
    .setStreamingMode(StreamingMode.NONE)
    .setMaxLlmCalls(100)
    .build();
```
This configuration creates a non-streaming agent with a limit of 100 LLM calls, suitable for simple task-oriented agents where complete responses are preferable.

##### Enabling streaming
**Python:**
```python
from google.adk.agents.run_config import RunConfig, StreamingMode
config = RunConfig(
    streaming_mode=StreamingMode.SSE,
    max_llm_calls=200
)
```
**Java:**
```java
import com.google.adk.agents.RunConfig;
import com.google.adk.agents.RunConfig.StreamingMode;

RunConfig config = RunConfig.builder()
    .setStreamingMode(StreamingMode.SSE)
    .setMaxLlmCalls(200)
    .build();
```
Using SSE streaming allows users to see responses as they're generated, providing a more responsive feel for chatbots and assistants.

##### Enabling speech support
**Python:**
```python
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.genai import types # For SpeechConfig etc.

config = RunConfig(
    speech_config=types.SpeechConfig(
        language_code="en-US",
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
        ),
    ),
    response_modalities=["AUDIO", "TEXT"],
    save_input_blobs_as_artifacts=True,
    support_cfc=True, # Python only for now
    streaming_mode=StreamingMode.SSE,
    max_llm_calls=1000,
)
```
**Java:**
```java
import com.google.adk.agents.RunConfig;
import com.google.adk.agents.RunConfig.StreamingMode;
import com.google.common.collect.ImmutableList;
import com.google.genai.types.Modality;
import com.google.genai.types.PrebuiltVoiceConfig;
import com.google.genai.types.SpeechConfig;
import com.google.genai.types.VoiceConfig;

RunConfig runConfig = RunConfig.builder()
    .setStreamingMode(StreamingMode.SSE)
    .setMaxLlmCalls(1000)
    .setSaveInputBlobsAsArtifacts(true)
    .setResponseModalities(ImmutableList.of(new Modality("AUDIO"), new Modality("TEXT")))
    .setSpeechConfig(SpeechConfig.builder()
        .voiceConfig(VoiceConfig.builder()
            .prebuiltVoiceConfig(PrebuiltVoiceConfig.builder().voiceName("Kore").build())
            .build())
        .languageCode("en-US")
        .build())
    .build();
```
This comprehensive example configures an agent with:
*   Speech capabilities using the "Kore" voice (US English)
*   Both audio and text output modalities
*   Artifact saving for input blobs (useful for debugging)
*   Experimental CFC support enabled (Python only)
*   SSE streaming for responsive interaction
*   A limit of 1000 LLM calls

##### Enabling Experimental CFC Support (Python only)
```python
from google.adk.agents.run_config import RunConfig, StreamingMode
config = RunConfig(
    streaming_mode=StreamingMode.SSE,
    support_cfc=True,
    max_llm_calls=150
)
```
Enabling Compositional Function Calling creates an agent that can dynamically execute functions based on model outputs, powerful for applications requiring complex workflows.

### Context
#### What is Context?
In the Agent Development Kit (ADK), "context" refers to the crucial bundle of information available to your agent and its tools during specific operations. Think of it as the necessary background knowledge and resources needed to handle a current task or conversation turn effectively.
Agents often need more than just the latest user message to perform well. Context is essential because it enables:
*   **Maintaining State**: Remembering details across multiple steps in a conversation (e.g., user preferences, previous calculations, items in a shopping cart). This is primarily managed through **session state**.
*   **Passing Data**: Sharing information discovered or generated in one step (like an LLM call or a tool execution) with subsequent steps. **Session state** is key here too.
*   **Accessing Services**: Interacting with framework capabilities like:
    *   **Artifact Storage**: Saving or loading files or data blobs (like PDFs, images, configuration files) associated with the session.
    *   **Memory**: Searching for relevant information from past interactions or external knowledge sources connected to the user.
    *   **Authentication**: Requesting and retrieving credentials needed by tools to access external APIs securely.
*   **Identity and Tracking**: Knowing which agent is currently running (`agent.name`) and uniquely identifying the current request-response cycle (`invocation_id`) for logging and debugging.
*   **Tool-Specific Actions**: Enabling specialized operations within tools, such as requesting authentication or searching memory, which require access to the current interaction's details.

The central piece holding all this information together for a single, complete user-request-to-final-response cycle (an **invocation**) is the `InvocationContext`. However, you typically won't create or manage this object directly. The ADK framework creates it when an invocation starts (e.g., via `runner.run_async`) and passes the relevant contextual information implicitly to your agent code, callbacks, and tools.

**Python Conceptual Pseudocode:**
```python
# runner = Runner(agent=my_root_agent, session_service=..., artifact_service=...)
# user_message = types.Content(...)
# session = session_service.get_session(...) # Or create new
#
# --- Inside runner.run_async(...) ---
# 1. Framework creates the main context for this specific run
# invocation_context = InvocationContext(
#     invocation_id="unique-id-for-this-run",
#     session=session,
#     user_content=user_message,
#     agent=my_root_agent, # The starting agent
#     session_service=session_service,
#     artifact_service=artifact_service,
#     memory_service=memory_service,
#     # ... other necessary fields ...
# )
#
# 2. Framework calls the agent's run method, passing the context implicitly
#    (The agent's method signature will receive it)
# await my_root_agent.run_async(invocation_context)
#   --- End Internal Logic ---
#
# As a developer, you work with the context objects provided in method arguments.
```
**Java Conceptual Pseudocode:**
```java
/* Conceptual Pseudocode: How the framework provides context (Internal Logic) */
// InMemoryRunner runner = new InMemoryRunner(agent);
// Session session = runner.sessionService().createSession(runner.appName(), USER_ID, initialState, SESSION_ID).blockingGet();
//
// try (Scanner scanner = new Scanner(System.in, StandardCharsets.UTF_8)) {
//     while (true) {
//         System.out.print("\nYou > ");
//         String userInput = scanner.nextLine(); // Corrected from scanner.next()
//         if ("quit".equalsIgnoreCase(userInput)) {
//             break;
//         }
//         Content userMsg = Content.fromParts(Part.fromText(userInput));
//         Flowable<Event> events = runner.runAsync(session.userId(), session.id(), userMsg);
//         System.out.print("\nAgent > ");
//         events.blockingForEach(event -> System.out.print(event.stringifyContent()));
//     }
// }
```

#### The Different types of Context
While `InvocationContext` acts as the comprehensive internal container, ADK provides specialized context objects tailored to specific situations. This ensures you have the right tools and permissions for the task at hand without needing to handle the full complexity of the internal context everywhere. Here are the different "flavors" you'll encounter:

##### `InvocationContext`
*   **Where Used**: Received as the `ctx` argument directly within an agent's core implementation methods (`_run_async_impl`, `_run_live_impl`).
*   **Purpose**: Provides access to the entire state of the current invocation. This is the most comprehensive context object.
*   **Key Contents**: Direct access to `session` (including `state` and `events`), the current `agent` instance, `invocation_id`, initial `user_content`, references to configured services (`artifact_service`, `memory_service`, `session_service`), and fields related to live/streaming modes.
*   **Use Case**: Primarily used when the agent's core logic needs direct access to the overall session or services, though often state and artifact interactions are delegated to callbacks/tools which use their own contexts. Also used to control the invocation itself (e.g., setting `ctx.end_invocation = True`).

**Python Pseudocode:**
```python
# from google.adk.agents import BaseAgent, InvocationContext
# from google.adk.events import Event
# from typing import AsyncGenerator
#
# class MyAgent(BaseAgent):
#     async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
#         # Direct access example
#         agent_name = ctx.agent.name
#         session_id = ctx.session.id
#         print(f"Agent {agent_name} running in session {session_id} for invocation {ctx.invocation_id}")
#         # ... agent logic using ctx ...
#         # yield Event(...) # Example
```
**Java Pseudocode:**
```java
// import com.google.adk.agents.BaseAgent;
// import com.google.adk.agents.InvocationContext;
// import com.google.adk.events.Event;
// import io.reactivex.rxjava3.core.Flowable;
//
// public class MyAgent extends BaseAgent {
//    // ... constructor ...
//    @Override
//    protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) {
//        // Direct access example
//        String agentName = invocationContext.agent().name(); // Corrected: agent() then name()
//        String sessionId = invocationContext.session().id(); // Corrected: session() then id()
//        String invocationId = invocationContext.invocationId();
//        System.out.println("Agent " + agentName + " running in session " + sessionId + " for invocation " + invocationId);
//        // ... agent logic using invocationContext ...
//        return Flowable.empty(); // Example
//    }
//    // ... other methods ...
// }
```

##### `ReadonlyContext`
*   **Where Used**: Provided in scenarios where only read access to basic information is needed and mutation is disallowed (e.g., `InstructionProvider` functions). It's also the base class for other contexts.
*   **Purpose**: Offers a safe, read-only view of fundamental contextual details.
*   **Key Contents**: `invocation_id`, `agent_name`, and a read-only view of the current `state`.

**Python Pseudocode:**
```python
# from google.adk.agents import ReadonlyContext # In Python, state is a direct dict-like object
#
# def my_instruction_provider(context: ReadonlyContext) -> str:
#     # Read-only access example
#     user_tier = context.state.get("user_tier", "standard")  # Can read state via .state
#     # context.state['new_key'] = 'value' # This would typically cause an error or be ineffective
#     return f"Process the request for a {user_tier} user."
```
**Java Pseudocode:**
```java
// import com.google.adk.agents.ReadonlyContext;
//
// public String myInstructionProvider(ReadonlyContext context){
//     // Read-only access example
//     String userTier = (String) context.state().getOrDefault("user_tier", "standard"); // state() returns a Map
//     // context.state().put("new_key", "value"); // This would typically cause an error or be ineffective
//     return "Process the request for a " + userTier + " user.";
// }
```

##### `CallbackContext`
*   **Where Used**: Passed as `callback_context` to agent lifecycle callbacks (`before_agent_callback`, `after_agent_callback`) and model interaction callbacks (`before_model_callback`, `after_model_callback`).
*   **Purpose**: Facilitates inspecting and modifying state, interacting with artifacts, and accessing invocation details specifically within **callbacks**.
*   **Key Capabilities (Adds to `ReadonlyContext`)**:
    *   Mutable `state` Property: Allows reading and writing to session state. Changes made here (`callback_context.state['key'] = value`) are tracked and associated with the event generated by the framework after the callback.
    *   Artifact Methods: `load_artifact(filename)` and `save_artifact(filename, part)` methods for interacting with the configured `artifact_service`.
    *   Direct `user_content` access.

**Python Pseudocode:**
```python
# from google.adk.agents import CallbackContext
# from google.adk.models import LlmRequest
# from google.genai import types
# from typing import Optional
#
# def my_before_model_cb(callback_context: CallbackContext, request: LlmRequest) -> Optional[types.Content]: # Return type depends on callback
#     # Read/Write state example
#     call_count = callback_context.state.get("model_calls", 0)
#     callback_context.state["model_calls"] = call_count + 1  # Modify state
#     # Optionally load an artifact
#     # config_part = await callback_context.load_artifact("model_config.json") # If async
#     print(f"Preparing model call #{call_count + 1} for invocation {callback_context.invocation_id}")
#     return None  # Allow model call to proceed
```
**Java Pseudocode:**
```java
// import com.google.adk.agents.CallbackContext;
// import com.google.adk.models.LlmRequest;
// import com.google.adk.models.LlmResponse; // For return type
// import com.google.genai.types.Content; // For return type if overriding
// import io.reactivex.rxjava3.core.Maybe;
//
// public Maybe<LlmResponse> myBeforeModelCb(CallbackContext callbackContext, LlmRequest request){ // Return type LlmResponse for before_model
//     // Read/Write state example
//     int callCount = (Integer) callbackContext.state().getOrDefault("model_calls", 0);
//     callbackContext.state().put("model_calls", callCount + 1); // Modify state
//     // Optionally load an artifact
//     // Maybe<Part> configPart = callbackContext.loadArtifact("model_config.json");
//     System.out.println("Preparing model call " + (callCount + 1));
//     return Maybe.empty(); // Allow model call to proceed
// }
```

##### `ToolContext`
*   **Where Used**: Passed as `tool_context` to the functions backing `FunctionTool`s and to tool execution callbacks (`before_tool_callback`, `after_tool_callback`).
*   **Purpose**: Provides everything `CallbackContext` does, plus specialized methods essential for tool execution, like handling authentication, searching memory, and listing artifacts.
*   **Key Capabilities (Adds to `CallbackContext`)**:
    *   **Authentication Methods**: `request_credential(auth_config)` to trigger an auth flow, and `get_auth_response(auth_config)` to retrieve credentials provided by the user/system.
    *   **Artifact Listing**: `list_artifacts()` to discover available artifacts in the session.
    *   **Memory Search**: `search_memory(query)` to query the configured `memory_service`.
    *   **`function_call_id` Property**: Identifies the specific function call from the LLM that triggered this tool execution, crucial for linking authentication requests or responses back correctly.
    *   **`actions` Property**: Direct access to the `EventActions` object for this step, allowing the tool to signal state changes, auth requests, etc.

**Python Pseudocode:**
```python
# from google.adk.tools import ToolContext
# from typing import Dict, Any
# # Assume this function is wrapped by a FunctionTool
#
# def search_external_api(query: str, tool_context: ToolContext) -> Dict[str, Any]:
#     api_key = tool_context.state.get("api_key")
#     if not api_key:
#         # Define required auth config
#         # auth_config = AuthConfig(...)
#         # tool_context.request_credential(auth_config)  # Request credentials
#         # Use the 'actions' property to signal the auth request has been made
#         # tool_context.actions.requested_auth_configs[tool_context.function_call_id] = auth_config
#         return {"status": "Auth Required"}
#
#     # Use the API key...
#     print(f"Tool executing for query '{query}' using API key. Invocation: {tool_context.invocation_id}")
#     # Optionally search memory or list artifacts
#     # relevant_docs = await tool_context.search_memory(f"info related to {query}")
#     # available_files = await tool_context.list_artifacts()
#     return {"result": f"Data for {query} fetched."}
```
**Java Pseudocode:**
```java
// import com.google.adk.tools.ToolContext;
// import com.google.adk.auth.AuthConfig; // Assuming AuthConfig class
// import java.util.Map;
//
// // Assume this function is wrapped by a FunctionTool
// public Map<String, Object> searchExternalApi(String query, ToolContext toolContext) {
//     String apiKey = (String) toolContext.state().get("api_key"); // Cast as needed
//     if (apiKey == null || apiKey.isEmpty()) { // Check for null or empty
//         // Define required auth config
//         // AuthConfig authConfig = new AuthConfig(...);
//         // toolContext.requestCredential(authConfig); // Request credentials
//         // Use the 'actions' property to signal the auth request has been made
//         // toolContext.actions().setRequestedAuthConfigs(...); // Example
//         return Map.of("status", "Auth Required");
//     }
//
//     // Use the API key...
//     System.out.println("Tool executing for query " + query + " using API key. Invocation: " + toolContext.invocationId());
//     // Optionally list artifacts
//     // Single<ListArtifactsResponse> availableFiles = toolContext.listArtifacts();
//     return Map.of("result", "Data for " + query + " fetched");
// }
```

Understanding these different context objects and when to use them is key to effectively managing state, accessing services, and controlling the flow of your ADK application.

#### Common Tasks Using Context
Now that you understand the different context objects, let's focus on how to use them for common tasks when building your agents and tools.

##### Accessing Information
You'll frequently need to read information stored within the context.

*   **Reading Session State**: Access data saved in previous steps or user/app-level settings. Use dictionary-like access on the `state` property.
    **Python Pseudocode:**
    ```python
    # # In a Tool function
    # def my_tool(tool_context: ToolContext, **kwargs):
    #     user_pref = tool_context.state.get("user_display_preference", "default_mode")
    #     api_endpoint = tool_context.state.get("app:api_endpoint") # Read app-level state
    #     if user_pref == "dark_mode":
    #         # ... apply dark mode logic ...
    #         pass
    #     print(f"Using API endpoint: {api_endpoint}")
    #     # ... rest of tool logic ...

    # # In a Callback function
    # def my_callback(callback_context: CallbackContext, **kwargs):
    #     last_tool_result = callback_context.state.get("temp:last_api_result") # Read temporary state
    #     if last_tool_result:
    #         print(f"Found temporary result from last tool: {last_tool_result}")
    #     # ... callback logic ...
    ```
    **Java Pseudocode:**
    ```java
    // // In a Tool function
    // public void myTool(ToolContext toolContext) {
    //     String userPref = (String) toolContext.state().getOrDefault("user_display_preference", "default_mode");
    //     String apiEndpoint = (String) toolContext.state().get("app:api_endpoint"); // Read app-level state
    //     if ("dark_mode".equals(userPref)) { // Use .equals for string comparison
    //         // ... apply dark mode logic ...
    //     }
    //     System.out.println("Using API endpoint: " + apiEndpoint);
    //     // ... rest of tool logic ...
    // }

    // // In a Callback function
    // public void myCallback(CallbackContext callbackContext) {
    //     String lastToolResult = (String) callbackContext.state().get("temp:last_api_result"); // Read temporary state
    //     if (lastToolResult != null && !lastToolResult.isEmpty()) { // Check for null or empty
    //         System.out.println("Found temporary result from last tool: " + lastToolResult);
    //     }
    //     // ... callback logic ...
    // }
    ```
*   **Getting Current Identifiers**: Useful for logging or custom logic based on the current operation.
    **Python Pseudocode:**
    ```python
    # # In any context (ToolContext shown)
    # def log_tool_usage(tool_context: ToolContext, **kwargs):
    #     agent_name = tool_context.agent_name # agent_name is directly available
    #     inv_id = tool_context.invocation_id
    #     func_call_id = getattr(tool_context, 'function_call_id', 'N/A') # Specific to ToolContext
    #     print(f"Log: Invocation={inv_id}, Agent={agent_name}, FunctionCallID={func_call_id} - Tool Executed.")
    ```
    **Java Pseudocode:**
    ```java
    // // In any context (ToolContext shown)
    // public void logToolUsage(ToolContext toolContext) {
    //     String agentName = toolContext.agentName(); // agentName() method
    //     String invId = toolContext.invocationId();
    //     String functionCallId = toolContext.functionCallId().orElse("N/A"); // Specific to ToolContext
    //     System.out.println("Log: Invocation=" + invId + " Agent=" + agentName + " FunctionCallID=" + functionCallId);
    // }
    ```
*   **Accessing the Initial User Input**: Refer back to the message that started the current invocation.
    **Python Pseudocode:**
    ```python
    # # In a Callback
    # def check_initial_intent(callback_context: CallbackContext, **kwargs):
    #     initial_text = "N/A"
    #     if callback_context.user_content and callback_context.user_content.parts:
    #         initial_text = callback_context.user_content.parts[0].text or "Non-text input"
    #     print(f"This invocation started with user input: '{initial_text}'")

    # # In an Agent's _run_async_impl
    # async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
    #     if ctx.user_content and ctx.user_content.parts:
    #         initial_text = ctx.user_content.parts[0].text
    #         print(f"Agent logic remembering initial query: {initial_text}")
    #     # ...
    ```
    **Java Pseudocode:**
    ```java
    // // In a Callback
    // public void checkInitialIntent(CallbackContext callbackContext) {
    //     String initialText = "N/A";
    //     if (callbackContext.userContent().isPresent() &&
    //         callbackContext.userContent().get().parts().isPresent() &&
    //         !callback_context.userContent().get().parts().get().isEmpty()) {
    //         initialText = callback_context.userContent().get().parts().get().get(0).text().orElse("Non-text input");
    //     }
    //     System.out.println("This invocation started with user input: " + initialText);
    // }
    ```

##### Managing Session State
State is crucial for memory and data flow. When you modify state using `CallbackContext` or `ToolContext`, the changes are automatically tracked and persisted by the framework.
**How it Works**: Writing to `callback_context.state['my_key'] = my_value` or `tool_context.state['my_key'] = my_value` adds this change to the `EventActions.state_delta` associated with the current step's event. The `SessionService` then applies these deltas when persisting the event.

*   **Passing Data Between Tools**:
    **Python Pseudocode:**
    ```python
    # # Tool 1 - Fetches user ID
    # import uuid
    # def get_user_profile(tool_context: ToolContext) -> dict:
    #     user_id = str(uuid.uuid4()) # Simulate fetching ID
    #     # Save the ID to state for the next tool
    #     tool_context.state["temp:current_user_id"] = user_id
    #     return {"profile_status": "ID generated"}

    # # Tool 2 - Uses user ID from state
    # def get_user_orders(tool_context: ToolContext) -> dict:
    #     user_id = tool_context.state.get("temp:current_user_id")
    #     if not user_id:
    #         return {"error": "User ID not found in state"}
    #     print(f"Fetching orders for user ID: {user_id}")
    #     # ... logic to fetch orders using user_id ...
    #     return {"orders": ["order123", "order456"]}
    ```
    **Java Pseudocode:**
    ```java
    // // Tool 1 - Fetches user ID
    // import java.util.UUID;
    // import java.util.Map;
    // public Map<String, String> getUserProfile(ToolContext toolContext) {
    //     String userId = UUID.randomUUID().toString();
    //     // Save the ID to state for the next tool
    //     toolContext.state().put("temp:current_user_id", userId); // Corrected: use userId variable
    //     return Map.of("profile_status", "ID generated");
    // }

    // // Tool 2 - Uses user ID from state
    // public Map<String, Object> getUserOrders(ToolContext toolContext) { // Return type Object for list
    //     String userId = (String) toolContext.state().get("temp:current_user_id");
    //     if (userId == null || userId.isEmpty()) {
    //         return Map.of("error", "User ID not found in state");
    //     }
    //     System.out.println("Fetching orders for user id: " + userId);
    //     // ... logic to fetch orders using user_id ...
    //     return Map.of("orders", List.of("order123", "order456")); // Example with List
    // }
    ```
*   **Updating User Preferences**:
    **Python Pseudocode:**
    ```python
    # # Tool or Callback identifies a preference
    # def set_user_preference(tool_context: ToolContext, preference: str, value: str) -> dict:
    #     # Use 'user:' prefix for user-level state (if using a persistent SessionService)
    #     state_key = f"user:{preference}"
    #     tool_context.state[state_key] = value
    #     print(f"Set user preference '{preference}' to '{value}'")
    #     return {"status": "Preference updated"}
    ```
    **Java Pseudocode:**
    ```java
    // // Tool or Callback identifies a preference
    // public Map<String, String> setUserPreference(ToolContext toolContext, String preference, String value) {
    //     // Use 'user:' prefix for user-level state (if using a persistent SessionService)
    //     String stateKey = "user:" + preference;
    //     tool_context.state().put(stateKey, value);
    //     System.out.println("Set user preference '" + preference + "' to '" + value + "'");
    //     return Map.of("status", "Preference updated");
    // }
    ```
*   **State Prefixes**: While basic state is session-specific, prefixes like `app:` and `user:` can be used with persistent `SessionService` implementations (like `DatabaseSessionService` or `VertexAiSessionService`) to indicate broader scope (app-wide or user-wide across sessions). `temp:` can denote data only relevant within the current invocation.

##### Working with Artifacts
Use artifacts to handle files or large data blobs associated with the session. Common use case: processing uploaded documents.

**Document Summarizer Example Flow**:
1.  **Ingest Reference** (e.g., in a Setup Tool or Callback): Save the path or URI of the document, not the entire content, as an artifact.
    **Python Pseudocode:**
    ```python
    # # In a callback or initial tool
    # from google.adk.agents import CallbackContext # Or ToolContext
    # from google.genai import types
    #
    # async def save_document_reference(context: CallbackContext, file_path: str) -> None:
    #     # Assume file_path is something like "gs://my-bucket/docs/report.pdf" or "/local/path/to/report.pdf"
    #     try:
    #         # Create a Part containing the path/URI text
    #         artifact_part = types.Part(text=file_path) # Use text for URI/path
    #         version = await context.save_artifact("document_to_summarize.txt", artifact_part)
    #         print(f"Saved document reference '{file_path}' as artifact version {version}")
    #         # Store the filename in state if needed by other tools
    #         context.state["temp:doc_artifact_name"] = "document_to_summarize.txt"
    #     except ValueError as e:
    #         print(f"Error saving artifact: {e}") # E.g., Artifact service not configured
    #     except Exception as e:
    // ...
    ```