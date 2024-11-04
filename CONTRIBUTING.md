
# Contributing to So Halal App

Thank you for your interest in contributing to **So Halal App**! We appreciate your efforts and value your time.

## Development Workflow
We use a trunk-based development approach. Follow the steps below to contribute:

### 1. Create an Issue
Before starting to code, create an issue that outlines your proposed changes or the bug you're fixing. Ensure it is well-documented so the maintainers and contributors understand the context.

### 2. Fork the Repository
Fork the repo to your own GitHub account and clone it to your local machine:
```bash
git clone https://github.com/yourusername/so-halal-app.git
cd so-halal-app
```

### 3. Create a Feature Branch
Create a branch from `main` for your work:
```bash
git checkout -b feature/your-feature-name
```

### 4. Code Your Changes
Implement your changes, ensuring you follow project guidelines. Run tests and lint your code:
- For backend:
  ```bash
  make lint-backend
  ```
- For mobile:
  ```bash
  make lint-mobile
  ```

### 5. Commit Your Changes
Commit your changes with a meaningful commit message:
```bash
git commit -m "Add [feature/bugfix]: brief description"
```

### 6. Push to GitHub
Push your branch to your forked repository:
```bash
git push origin feature/your-feature-name
```

### 7. Create a Pull Request
Navigate to the main repository and create a pull request from your feature branch. Ensure your pull request passes all CI checks.

### 8. Pass CI
Your pull request must pass all continuous integration (CI) checks. Please review any comments or suggestions from the maintainers and make necessary changes.

---
We look forward to your contributions!

