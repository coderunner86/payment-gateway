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

# API PAYMENT WITH STRIPE AND CHATGPT INTEGRATION

## Description
This project presents a comprehensive solution, combining the robustness of Stripe's payment platform with the advanced AI capabilities of ChatGPT. Designed to streamline CRUD operations, it also facilitates the creation and management of Stripe users (customers), products, and payment confirmations directly from the application interface.

Key Features:
Stripe Integration: Simplifies the handling of financial transactions. Users can effortlessly create Stripe customers, add and manage products, and handle payments, all within a unified system.
CRUD Functionalities: Offers full Create, Read, Update, Delete (CRUD) capabilities, ensuring a flexible and efficient management of database records.
AI-Enhanced Product Information Retrieval: With the power of ChatGPT, our API can intelligently retrieve detailed information about products stored in the database. This feature is especially useful for providing customers with in-depth product insights.
AI-Driven Product Recommendations: ChatGPT's integration goes a step further by offering personalized product recommendations. Depending on user inquiries, it can suggest suitable products, enhancing the customer experience.


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
## Testing and Documentation
The API can be easily tested and explored using FastAPI's interactive documentation at `localhost:8000/docs`. This feature allows for a hands-on experience with the API's endpoints, providing real-time testing and a clear understanding of its capabilities.

## Ideal Use Cases
- **E-commerce platforms** seeking a comprehensive payment system with AI-enhanced customer interaction.
- **Businesses** looking to provide detailed product information and tailored recommendations.
- **Developers** in need of an integrated solution for managing products, transactions, and user interactions.

## Technology Stack
- **FastAPI**: For building a high-performance, easy-to-use backend with asynchronous features.
- **Prisma**: As the ORM for efficient database operations.
- **Stripe**: For secure and versatile payment processing.
- **ChatGPT**: For advanced natural language processing in information retrieval and recommendations.


## Acknowledgements

Special thanks to [PEAKU](https://peaku.co/es/bootcamp-fullstack) for their invaluable support and contributions to this project. 

