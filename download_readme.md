# PersonalWebsite

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This repository contains the source code for my personal website. This website showcases my skills, projects, and contact information. It's built using React and utilizes a variety of libraries for features like animations, routing, and data fetching.

**Key Features:**

*   Modern and responsive design.
*   Project showcase with detailed descriptions.
*   Contact form integrated with email services.
*   Blog/Articles section (potentially pulling data from RSS feeds or other sources).

**Primary Language:** JavaScript

**Topics:** React, Portfolio, Personal Website, Web Development

## Installation

Follow these steps to set up the development environment:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/[your-username]/PersonalWebsite.git
    cd PersonalWebsite
    ```

2.  **Install dependencies:**

    ```bash
    npm install  # or yarn install or pnpm install
    ```

3.  **Environment Variables:**

    Some features of this website might rely on environment variables.  Create a `.env` file in the root directory of the project and add any necessary environment variables.  For example, if you're using EmailJS for the contact form, you'll need to add your service ID, template ID, and user ID:

    ```
    EMAILJS_SERVICE_ID=your_service_id
    EMAILJS_TEMPLATE_ID=your_template_id
    EMAILJS_PUBLIC_KEY=your_public_key
    ```

    **Note:**  Never commit your `.env` file to the repository.  Make sure to add it to your `.gitignore` file.

## Usage

### Development

To start the development server:

```bash
npm run dev  # or yarn dev or pnpm dev
