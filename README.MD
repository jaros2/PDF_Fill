# Child Care Leave Application

## Requirements
- Python 3.8+
- Flask
- Flask-WTF
- Flask-SQLAlchemy

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/your-repo/child_care_leave_app.git
    ```
2. Navigate to the project directory:
    ```sh
    cd child_care_leave_app
    ```
3. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4. Install the requirements:
    ```sh
    pip install -r requirements.txt
    ```
5. Set up the database:
    ```sh
    python setup.py
    ```

## Running the Application
1. Run the Flask application:
    ```sh
    flask run
    ```
2. Open your browser and go to `http://127.0.0.1:5000/`.

## Usage
1. Add at least one parent.
2. Add children.
3. Create a leave entry.
4. Download the filled PDF form from the provided link.