# CodeIn - LinkedIn Clone

CodeIn is a clone of the popular professional networking platform LinkedIn. It aims to replicate some of the core features and functionalities of LinkedIn, providing users with a familiar experience while serving as a learning resource for developers. This project is built using HTML, CSS, Bootstrap, and JavaScript for the frontend, Python with Flask framework for the backend, and PostgreSQL as the database.

## Features(current)

- User authentication and registration system
- User profiles with editable information
- News feed displaying posts and updates from connections
- Ability to follow and unfollow
- 85% same UI

## Technologies Used

- Frontend:
  - HTML
  - CSS
  - Bootstrap
  - JavaScript

- Backend:
  - Python
  - Flask (web framework)

- Database:
  - PostgreSQL

## Setup and Usage

To run Codeln on your local machine, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/Kamalkoranga/CodeIn
   ```

2. Navigate to the project directory:

    ```
    cd CodeIn
    ```

3. Install the necessary dependencies. Make sure you have Python and pip installed. Use the following command:

   ```
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:

   - Create a new database in PostgreSQL(or you can use SQLite).
   - Update the database URL in the .env file with the appropriate details.

5. Set up the environment variables:

    - Create a new file named .env.
    - Add the following environment variables to the .env file:
      - MAIL_SERVER - mail server (you can use sendinblue for email)
      - MAIL_USERNAME - Your email address for sending emails.
      - MAIL_PASSWORD - Your email password or an app-specific password for email service.
      - MAIL_PORT - 587
      - MAIL_USE_TLS - True
      - FLASK_APP - codein.py.
      - SECRET_KEY - secret key for web app.
      - CODEIN_ADMIN - your email
      - DATABASE_URL = your db url

6. Run the database migrations to set up the required tables:

   ```
   flask db upgrade
   ```

5. Start the Flask development server:

   ```
   flask run
   ```

6. Access the application by visiting `http://localhost:5000` in your browser.

## Contributing

Contributions are welcome and encouraged! If you'd like to contribute to Codeln, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bug fix:

   ```
   git checkout -b feature/your-feature-name
   ```

3. Make your modifications and commit your changes:

   ```
   git commit -m "Add your commit message"
   ```

4. Push your branch to your forked repository:

   ```
   git push origin feature/your-feature-name
   ```

5. Open a pull request against the main repository.

Please ensure that your code adheres to the existing coding style and conventions used in the project. Include detailed information about your changes and test your modifications thoroughly before submitting a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

We would like to acknowledge the contributions of all the developers who have contributed to this project and the open-source community for their invaluable resources and support.

---

Feel free to update and modify this README to reflect any additional details specific to your Codeln LinkedIn Clone project. Happy coding! 🚀✨
