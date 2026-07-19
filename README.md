# system-health-automation-cli
Python CLI tool for automated system health checks, including CPU, RAM, disk, uptime, services, ports, logging, exports and alerting.
System Health Automation CLI

A lightweight Python CLI tool for checking the health of a local system directly from the terminal.

The main idea is simple: run one command and quickly understand if the machine has any obvious problems with CPU, memory, disk usage, or uptime.

This project is built as a practical automation tool and can be extended step by step into a more advanced monitoring utility.

    Features

Currently, the tool checks:

🧠 CPU usage
💾 Memory usage
🗄️ Disk usage
⏱️ System uptime
🟢 Global health status
⚙️ Automation-friendly exit codes
📊 Clean terminal table output
📸 Example

Run a local health check:

python -m healthcheck.cli local

Global status: OK
    How it works

The CLI runs several health checks and combines their results into one global system status.

Terminal command
      ↓
healthcheck/cli.py
      ↓
CPU / Memory / Disk / Uptime checks
      ↓
Results are collected
      ↓
Global status is calculated

Output is displayed in the terminal
🟢 Status logic

The tool uses simple health statuses:

Status	Meaning
🟢 OK	Everything looks normal
🟡 WARNING	The system is close to a risky level
🔴 CRITICAL	The system needs attention
⚫ UNKNOWN	Something went wrong during the check

Example threshold logic:

Metric	🟡 WARNING	🔴 CRITICAL
CPU	80%+	90%+
Memory	80%+	90%+
Disk	85%+	95%+
⚙️ Exit codes

The CLI returns exit codes, which makes it useful for automation scripts, CI/CD pipelines, cron jobs, and monitoring workflows.

Exit code	Status
0	🟢 OK
1	🟡 WARNING
2	🔴 CRITICAL
3	⚫ UNKNOWN / ERROR

Example:

python -m healthcheck.cli local
echo $?
📁 Project structure
system-health-automation-cli/
│
├── healthcheck/
│   ├── __init__.py
│   ├── cli.py
│   └── checks/
│       ├── __init__.py
│       ├── cpu.py
│       ├── memory.py
│       ├── disk.py
│       └── uptime.py
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE

The project is split into small modules so each part has one clear responsibility.

File	Responsibility
cli.py	Handles the terminal command and output
cpu.py	Checks CPU usage
memory.py	Checks memory usage
disk.py	Checks disk usage
uptime.py	Checks system uptime

This makes the project easier to read, maintain, test, and extend.

🛠️ Installation

Clone the repository:

git clone https://github.com/sasho500/system-health-automation-cli.git
cd system-health-automation-cli

Create a virtual environment:

python -m venv .venv

Activate the virtual environment.

On Windows PowerShell:

.venv\Scripts\activate

On Git Bash:

source .venv/Scripts/activate

On Linux/macOS:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

🐳 Docker Usage

This project can also be run inside a Docker container.

Build the Docker image:

docker build -t system-health-cli .

Show the CLI help menu:

docker run --rm system-health-cli --help

Run a local health check inside the container:

docker run --rm system-health-cli local

Run a port check:

docker run --rm system-health-cli ports --ports 22,80,443

Run a service/process check:

docker run --rm system-health-cli services --names python

Export a JSON report and keep it on the host machine:

mkdir reports
docker run --rm -v ${PWD}/reports:/app/reports system-health-cli local --format json

Save logs on the host machine:

mkdir logs
docker run --rm -v ${PWD}/logs:/app/logs system-health-cli local


▶️ Usage

Run the local system health check:

python -m healthcheck.cli local
📦 Dependencies

This project uses:

psutil — for system metrics
typer — for building the CLI
rich — for clean terminal output
🧪 Current version

The current version supports basic local system checks.

Implemented:

CPU check
Memory check
Disk check
Uptime check
Global status
Exit codes
Rich table output
🗺️ Roadmap

Planned improvements:

📄 JSON report export
📊 CSV report export
📝 Log file support
⚙️ Custom warning and critical thresholds
🌐 Port checks
🧩 Service/process checks
💬 Messenger or Telegram alerts
🔐 Remote server checks over SSH
🐳 Docker container health checks
🚀 GitHub Actions workflow
🎯 Why I built this

I built this project to practice real-world Python automation.

The goal is not just to write a simple script, but to create a clean and extendable CLI tool that can grow into something closer to a real operational utility.

This project focuses on:

clean Python project structure
practical system checks
terminal automation
readable output
exit codes for automation
future extensibility
📌 Example use cases

This tool can be useful for:

quick local server checks
basic workstation health checks
automation scripts
cron jobs
CI/CD health validation
learning Python automation
building a portfolio project for DevOps or automation roles


## Version

Current version: `0.1.0`

📄 License

This project is licensed under the MIT License.