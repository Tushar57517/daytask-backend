# DayTask Backend

## Setup Instructions

Follow these steps to set up the SplitPay backend on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/Tushar57517/splitpay-backend.git
cd splitpay-backend
```

### 2. Create and Activate Virtual Environment

#### For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate a Secret Key

Generate a secure Django secret key using Python:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key as you'll need it in the next step.

### 5. Set Up Environment Variables

Create a `.env` file by copying the example file:

```bash
cp .env.example .env
```

Update the values in the `.env` file according to `.env.example` .

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user with your preferred credentials.

### 8. Run the Development Server

```bash
python manage.py runserver
```

The API will be accessible at `http://localhost:8000/`.

The admin panel can be accessed at `http://localhost:8000/admin/` using the superuser credentials you created.