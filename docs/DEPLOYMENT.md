# Deployment Guide: Render

This guide provides step-by-step instructions for deploying the Kitchen Management System to Render using the pre-configured `render.yaml` Blueprint.

## How It Works

The repository is configured for **Infrastructure as Code** using `render.yaml`. This file automatically tells Render how to build and deploy two services:
1.  A **Web Service** running the Django application with Gunicorn.
2.  A **PostgreSQL Database** for storing all application data.

Continuous deployment is enabled, so every push to the `main` branch will automatically trigger a new build and deployment on Render.

## Prerequisites

- A GitHub account with the project repository pushed.
- A Render account (the free tier is sufficient).

## Step 1: Create a Render Account and Connect GitHub

1.  **Sign Up**: Go to [render.com](https://render.com) and sign up, preferably using your GitHub account for seamless integration.
2.  **Authorize Access**: Grant Render permission to access your GitHub repositories. You can choose to grant access to all repositories or just the `kitchen-management-system` repo.

## Step 2: Deploy the Blueprint

1.  From the Render Dashboard, click **New +** and select **Blueprint**.
2.  **Connect Repository**: If you haven't already, connect the GitHub repository for this project.
3.  **Review Services**: Render will automatically detect and parse the `render.yaml` file. It will show you the two services to be created:
    *   `kitchen-management-system` (Web Service)
    *   `kitchen_db` (PostgreSQL Database)
4.  **Approve**: Click **Approve** to start the initial deployment.

The first deployment will take several minutes as Render provisions the database, installs Python dependencies, and runs the build script for the first time.

## Step 3: Access Your Application

Once the deployment status shows **"Live"**, your application is ready.

-   **URL**: Your app will be available at the URL shown on your Render dashboard (e.g., `https://kitchen-management-system.onrender.com`).
-   **Login**: Navigate to the `/accounts/login/` path to log in.

### Automatic Admin User Creation

On the very first deployment, the `build.sh` script automatically runs a command (`python manage.py create_superuser`) to create an admin user for you.

**This only runs if no other superusers exist.**

The credentials for this user are taken directly from the environment variables defined in `render.yaml`:
-   **Username**: `admin` (from the `ADMIN_USERNAME` variable)
-   **Password**: A securely generated random password (from the `ADMIN_PASSWORD` variable, which has `generateValue: true`).

**To find the auto-generated password:**
1.  In your Render dashboard, navigate to the `kitchen-management-system` web service.
2.  Go to the **Environment** tab.
3.  Find the `ADMIN_PASSWORD` key and click the "eye" icon or "copy" button to get the value.

You can now log in to the application and the Django Admin panel (`/admin/`) with these credentials.

## The Build Process (`build.sh`)

Every time you push a change to `main`, Render executes the `build.sh` script. Here's what it does:
1.  `set -o errexit`: Ensures the build will fail if any command fails.
2.  `pip install -r requirements.txt`: Installs all necessary Python packages.
3.  `python manage.py collectstatic --no-input`: Collects all static files (CSS, JS) for `whitenoise` to serve.
4.  `python manage.py migrate`: Applies any pending database migrations.
5.  `python manage.py setup_groups`: Ensures the 'Admin', 'Management', and 'Viewer' user groups exist in the database.
6.  `python manage.py create_superuser`: Creates an initial superuser (if and only if one doesn't already exist).

## Environment Variables

All necessary environment variables are defined in `render.yaml`.
-   `SECRET_KEY` and `ADMIN_PASSWORD` are generated securely by Render.
-   `DATABASE_URL` is automatically provided by the linked PostgreSQL service.
-   `DEBUG` is correctly set to `False`.

If you need to change a variable (like `ADMIN_USERNAME`), you can do so in the **Environment** tab of your web service in Render. Changing a variable will automatically trigger a new deployment.

## Troubleshooting

### Deployment Fails
-   **Check the Logs**: The first place to look is the **Logs** tab for your web service in Render. Scroll through the build and deploy logs to find the specific error message.
-   **Common Causes**:
    -   A syntax error in your Python code.
    -   A missing dependency in `requirements.txt`.
    -   A failing database migration.

### Static Files (CSS/JS) Not Loading
-   This is almost always a `collectstatic` issue. Check the build logs to ensure the `python manage.py collectstatic` command completed successfully.
-   Ensure `whitenoise` is in your `requirements.txt` and configured in `settings.py`.

### "DisallowedHost" Error
-   This means a request is coming from a URL not in your `ALLOWED_HOSTS` setting.
-   In `render.yaml`, `ALLOWED_HOSTS` is set to `.onrender.com`, which covers all subdomains. If you add a custom domain, you must add it to the `ALLOWED_HOSTS` environment variable in Render. For example: `kitchen.yourdomain.com,.onrender.com`.

### Can't Log In / Admin User Not Found
-   Verify that the initial build completed successfully. The `create_superuser` command only runs at the end of a successful build.
-   Double-check that you are using the correct auto-generated password from the **Environment** tab in Render.
-   If a superuser was created previously and you have since changed the `ADMIN_` environment variables, a *new* user will not be created. The script only runs if **no superusers exist**. You would need to manage users from the Django admin panel or connect to the database shell to make manual changes.