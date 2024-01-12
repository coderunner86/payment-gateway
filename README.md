<div align="center">
  <a style="vertical-align: middle;" href="https://fastapi.tiangolo.com/" target="blank">
    <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="450" alt="FastAPI Logo">
  </a>
</div>

[circleci-image]: https://img.shields.io/circleci/build/github/nestjs/nest/master?token=abc123def456
[circleci-url]: https://circleci.com/gh/nestjs/nest

<p align="center">
  FastAPI framework, high performance, easy to learn, fast to code, ready for production.
</p>
<p align="center">
  <a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&amp;branch=master" alt="Test">
  </a>
  <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="Coverage">
  </a>
  <a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&amp;label=pypi%20package" alt="Package version">
  </a>
  <a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
  </a>
</p>

# API PAYMENT

## Description

API Payment

## Development

### Local

```bash
# 1. Create virtual environment
$ python -m venv venv

# 2. Activate virtual environment

# Windows
$ .\venv\Scripts\activate

# Linux
$ source venv/bin/activate

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Generate schema
$ prisma generate

# 5. Run the migration on the instance
$ prisma db push

# 6. Execute app
$ uvicorn main:app --reload
```
