# 🌐 Cloud Resume Challenge - David Martinez

This repository is part of the **Cloud Resume Challenge**, a project designed to strengthen skills in **web development, cloud, and DevOps** through a practical and scalable hands-on project.

In **Phase 1**, the main goal was to create and publish an **online resume** using **HTML and CSS**, hosted on **GitHub Pages**.

Currently, it is at **Phase 2**, where the main goal is to add a dynamic visitor counter to the resume, integrating Azure Functions and Azure Storage.

For the **Phase 3**, I will be updating my resume to create a multilingual resume 

🔗 **Live Demo**: [My Online Resume](https://DavidMF13.github.io/cloud-resume)

---

## 📌 Project Goals

* Build a professional **resume website**.
* Deploy it to the cloud using free hosting (GitHub Pages).
* Create a Serverless Function to track page visits.
* Implement a database to store the visit count.
* Apply development best practices:

  * Semantic HTML validated with [W3C Validator](https://validator.w3.org/).
  * Responsive design for mobile and desktop.
  * Version control with Git and GitHub.

---

## 🛠️ Technologies Used

* **Frontend**: HTML5, CSS3
* **Hosting**: GitHub Pages
* **Version Control**: Git & GitHub
* **Backend**: Azure Functions (Python)
* **Database**: Azure Cosmos DB Storage
* **Automation**: Github Actions

---

## 📂 Repository Structure

```bash

cloud-resume/
├── backend/
│   ├── api/                 # Azure Functions project
│   │   ├── __init__.py      # Function code for the visit counter
│   │   ├── function.json    # Function configuration
│   │   ├── requirements.txt # Python dependencies
│   │   ├── host.json
│   │   └── .gitignore
│   └── .vscode/             # VS Code settings for backend
├── .github/
│   └── workflows/
│       └── main.yml         # GitHub Actions workflow for CI/CD
├── index.html               # Main resume page
└── README.md                # Project documentation

```
