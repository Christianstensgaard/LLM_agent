@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
pip install pyautogen requests python-dotenv

echo.
echo Setup complete!
echo To activate your environment later, run:
echo     venv\Scripts\activate
pause
