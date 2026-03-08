🎓 Exam Prep Pro: SQL Database Assistant
A streamlined tool designed to help students prepare for exams using an automated SQL environment. This project features a self-initializing database, meaning the schema and seed data are generated automatically upon the first run—no manual SQL imports required.

🚀 Features
Auto-Provisioning: The database is created and populated on startup.

Interactive Quizzing: SQL-driven logic to pull random questions or track progress.

Performance Tracking: Stores your results to identify weak areas.

Lightweight: Minimal dependencies for a quick setup.

🏗️ System Architecture
The application follows a modular workflow. Upon execution, the system performs a handshake with the local environment to ensure the data layer is ready before the user interaction begins.

Core Components:
Initialization Engine: Checks for the existing database file. If not found, it triggers the DDL (Data Definition Language) scripts to build the structure.

Data Seeder: Injects initial exam questions and categories from a raw configuration file into the newly created tables.

Query Controller: Handles the logic between user inputs and the SQL backend, ensuring data integrity during the exam simulation.
