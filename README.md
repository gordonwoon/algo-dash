# Stock Trading Dashboard

This project is a comprehensive stock trading dashboard that leverages a React frontend to display live financial data and trade records, paired with a FastAPI backend for robust data handling and server-side logic. Structured as an NX monorepo, it offers a unified development experience for both the frontend and backend components.

## Features

- **Live Financial Data**: Real-time display of stock prices and financial metrics using React.
- **Trade Records Management**: View and manage historical trade data through a user-friendly interface.
- **Historical Data Fetching**: Backend service to fetch and store historical stock data using yFinance.
- **RESTful API**: FastAPI backend to serve financial data and trade records to the frontend.
- **Monorepo Structure**: NX monorepo setup for streamlined development and deployment processes.

## Technology Stack

- **Frontend**: React
- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Data Fetching**: yFinance
- **Monorepo Management**: NX

## Getting Started

### Prerequisites

- Node.js and npm
- Python 3.8+
- PostgreSQL
- NX CLI

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/gordonwoon/algo-dash.git
   cd algo-dash
   ```

2. **Install dependencies**:

   - Backend (Python packages):
     ```bash
     pip install -r requirements.txt
     ```
   - Frontend (Node.js packages):
     ```bash
     yarn install
     ```

3. **Set up environment variables**:

   Create `.env` files for both frontend and backend projects as needed, including the database connection string for the backend:

   ```env
   DATABASE_URL=postgresql+asyncpg://username:password@localhost/yourdatabase
   ```

### Running the Application

- **Start the Backend**:

  Navigate to the backend directory and run:

  ```bash
  uvicorn app.main:app --reload
  ```

- **Start the Frontend**:

  In a new terminal, navigate to the frontend directory and run:

  ```bash
  npm start
  ```

Your React application will be available at `http://localhost:3000`, and the FastAPI backend will serve APIs at `http://localhost:8000`.

## Usage

- **View Live Financial Data**: Access the React frontend for real-time financial information.
- **Manage Trade Records**: Utilize the frontend interface to review and manage your historical trades.
- **Fetch Historical Data**: The FastAPI backend provides endpoints to fetch and store historical stock data, accessible to the frontend for display.

## Versioning

This project uses [SemVer](http://semver.org/) for versioning. For available versions, see the [tags on this repository](https://yourrepository.com/yourproject/tags).

## Authors

- **Gordon Woon** - _Initial Work_ - [Gordon](https://github.com/gordonwoon)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Hat tip to the creators and contributors of React, FastAPI, NX, and yFinance for their fantastic tools and libraries that made this project possible.
