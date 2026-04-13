# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This repository is a comprehensive educational guide and practical implementation repository for building a local LLM application on a Raspberry Pi. It covers everything from hardware selection and Linux basics to deploying Ollama, Open WebUI, and advanced customizations like MCP (Model Context Protocol) servers and Pipelines.

## Core Technologies
- **Hardware**: Raspberry Pi (optimized for Pi 5 with 8GB/16GB RAM).
- **OS**: PiOS (64-bit).
- **LLM Runtime**: Ollama.
- **Web Interface**: Open WebUI (deployed via Docker/Docker Compose).
- **Connectivity**: SSH, Cloudflare Tunnel, Ngrok.
- **Extensibility**: 
  - **Open WebUI Functions**: Python-based plugins (Filters, Actions, Pipes).
  - **Open WebUI Pipelines**: Modular workflow framework (OpenAI-compatible API).
  - **MCP (Model Context Protocol)**: Standardized protocol for connecting models to external tools/data.
- **Containerization**: Docker & Docker Compose.

## Repository Structure
- `Docker/`: Guides and documentation for Docker installation and usage on Raspberry Pi.
- `Docker_compose快速部署open-webui/`: Practical examples of deploying Open WebUI using Docker Compose.
- `file_server安裝流程說明/`: Guide for setting up a Raspberry Pi file server.
- `Linux指令操作說明/`: Comprehensive Linux command tutorials.
- `OpenWebUI/`: 
  - `Functions/`: Tutorials on Open WebUI's built-in Python extensibility (Filters, Actions, Pipes).
  - `mcp/`: Tutorials on implementing and deploying MCP servers to extend Open WebUI.
  - `pipeline/`: Tutorials on using the Open WebUI Pipelines framework.
  - `知識庫文件/`: RAG (Retrieval-Augmented Generation) test documents.
- `ollama安裝流程說明/`: Guide for installing Ollama.
- `pi安裝流程說明/`: Initial Raspberry Pi setup guide.
- `tunnel/`: Tutorials on various remote access and tunneling solutions.
- `前端開發環境配置/`: Tutorials on setting up web development environments (JS, TS, React) for custom UI development.

## Development & Learning Workflow
The repository is organized as a learning path. When working with specific components, refer to their respective `README.md` files for the intended learning sequence and practical exercises.

### Open WebUI Customization
1. **Functions**: Use for lightweight logic within the Open WebUI interface (e.g., adding buttons or filtering text).
2. **Pipelines**: Use for complex, multi-step workflows and external API integrations that require an OpenAI-compatible API.
3. **MCP**: Use for standardized tool/data access that follows the Model Context Protocol.

### Docker Usage
Most services are intended to be run via `docker-compose`. Always check the local `compose.yaml` or `docker-compose.yml` in the relevant directory before making changes.

## Language Preference
- **Responses**: All communications should be in **Traditional Chinese (繁體中文)**.
- **Terminology**: Do not translate technical terms or code.
