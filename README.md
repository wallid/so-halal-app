# So Halal App

**So Halal App** is an open-source mobile application designed to provide users with a reliable tool for verifying the Halal status of products through barcode scanning. This project includes a FastAPI backend and a React Native mobile frontend.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Makefile Commands](#makefile-commands)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Barcode Scanning**: Scan barcodes to determine the Halal status of products.
- **Backend Service**: FastAPI backend handling data processing and communication with external databases.
- **Mobile App**: React Native app for cross-platform functionality.
- **Docker Compose**: Easy setup for development environments.
- **Linter Support**: Code linting for quality assurance.

## Getting Started
### Prerequisites
- [Python 3.x](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/)
- [Docker](https://www.docker.com/)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/so-halal-app.git
   cd so-halal-app
   ```

2. Run the installation:
   ```bash
   make install
   ```

### Running the Application
- To start the entire application (backend, mobile, and Docker services):
  ```bash
  make up
  ```

- To stop the entire application:
  ```bash
  make down
  ```

### Other Commands
- Run the backend locally:
  ```bash
  make backend
  ```
- Run the mobile app:
  ```bash
  make mobile
  ```
- View Docker Compose logs:
  ```bash
  make logs
  ```
- Run linter for backend:
  ```bash
  make lint-backend
  ```
- Run linter for mobile:
  ```bash
  make lint-mobile
  ```
- Clean up containers, images, and volumes:
  ```bash
  make clean
  ```

## Development
For development, ensure that the backend and mobile apps are running on separate ports without conflicts. Use `make develop` to provision Docker services for databases and caching layers.

## Contributing
We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our development workflow.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

---
