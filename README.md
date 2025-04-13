# Personal Website

A personal website built with modern web technologies to showcase skills, projects, and experience.

## Overview

This repository contains the source code for my personal website. The website is designed to be a clean, responsive, and informative platform for visitors to learn more about me, my work, and my interests.  It includes sections for my portfolio, resume, contact information, and blog (potentially pulling data from an external source).

## Built With

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoWidth=60) ![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoWidth=60) ![Vite](https://img.shields.io/badge/Vite-B44F47?style=for-the-badge&logo=vite&logoColor=white&logoWidth=60) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoWidth=60) ![Express.js](https://img.shields.io/badge/Express.js-000000?style=for-the-badge&logo=express&logoWidth=60) ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoWidth=60) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoWidth=60) ![Framer Motion](https://img.shields.io/badge/Framer_Motion-0055FF?style=for-the-badge&logo=framer&logoColor=white&logoWidth=60)

## Installation

Follow these steps to set up the project locally:

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd my-portfolio
    ```

2.  **Install dependencies:**

    ```bash
    npm install
    ```

## Usage

### Development

To start the development server:

```bash
npm run dev
```

This will start the Vite development server, usually on `http://localhost:5173/`.

### Production Build

To build the project for production:

```bash
npm run build
```

This will create an optimized build of the website in the `dist` directory.  You can then deploy the contents of this directory to a web server.

### Linting

To run the linter:

```bash
npm run lint
```

This will check the code for any linting errors and warnings, following the rules defined in the `.eslintrc.js` configuration file.

## Dependencies

The project utilizes the following key dependencies:

*   **React:** A JavaScript library for building user interfaces.
*   **React Router DOM:**  For handling navigation and routing within the application.
*   **Vite:** A fast and modern build tool.
*   **Axios:** For making HTTP requests.
*   **Express:** A minimal and flexible Node.js web application framework (likely used for any backend API routes or server-side functionality).
*   **Cors:**  Node.js package for providing a Connect/Express middleware that can be used to enable CORS.
*   **Cheerio:** A fast, flexible, and lean implementation of core jQuery designed specifically for the server.
*   **csv-parser**: A parser for CSV files.
*   **framer-motion**:  A production-ready motion library for React.
*   **lucide-react**:  A collection of beautiful icons for React.
*   **rss-parser**: A library for parsing RSS feeds.
*   **@emailjs/browser**: Allows sending emails directly from the client-side using EmailJS.
*   **node-fetch**: For fetching data from external sources.

See the `package.json` file for a complete list of dependencies and their versions.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).