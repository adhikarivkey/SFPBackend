# SFPBackend  

**SFPBackend** is a Django-based project designed to help users find gas stations along their travel route within the USA. By taking inputs for the start and finish locations, the system calculates the travel route and lists all available gas stations along the way.

## Features  
- Users can input their starting and ending locations.  
- The system calculates the travel route and retrieves nearby gas stations along the way.  
- Uses geolocation services to ensure accurate route and gas station information.  
- Built with Django and Django REST Framework for a robust and scalable backend.  

## Prerequisites  
Make sure you have the following installed:  
- Python 3.8+  
- Django 3.2.23  

## Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/adhikarivkey/SFPBackend.git
   cd SFPBackend
   ```  

2. Install `virtualenv`:  
   ```bash
   pip install virtualenv
   ```  

3. Create and activate a virtual environment:  
   ```bash
   virtualenv env  
   source env/bin/activate  # For Linux/Mac
   env\Scripts\activate  # For Windows
   ```  

4. Install the required packages:  
   ```bash
   pip install -r requirements.txt
   ```  

5. Create a `.env` file in the project root and add your environment-specific variables, such as API keys for geolocation services.  

6. Run the migrations:  
   ```bash
   python manage.py makemigrations  
   python manage.py migrate  
   ```  

7. Start the development server:  
   ```bash
   python manage.py runserver
   ```  

## Requirements  

Here is the list of dependencies used in this project, as listed in the `requirements.txt`:  

```
asgiref==3.8.1  
beautifulsoup4==4.13.2  
certifi==2025.1.31  
charset-normalizer==3.4.1  
Django==3.2.23  
djangorestframework==3.12.0  
geographiclib==2.0  
geopy==2.4.1  
idna==3.10  
numpy==2.2.2  
pandas==2.2.3  
polyline==2.0.2  
python-dateutil==2.9.0.post0  
python-dotenv==1.0.1  
pytz==2025.1  
requests==2.32.3  
shapely==2.0.7  
six==1.17.0  
soupsieve==2.6  
sqlparse==0.5.3  
typing_extensions==4.12.2  
tzdata==2025.1  
urllib3==2.3.0  
```

## Usage  

1. Start the server using the command:  
   ```bash
   python manage.py runserver
   ```  
2. Access the API endpoint at `http://127.0.0.1:8000/` to input your start and finish locations and get a list of gas stations along the route.  

## Technologies Used  
- **Django 3.2.23**: Web framework  
- **Django REST Framework**: API development  
- **Geopy**: Geolocation services  
- **Pandas**: Data manipulation and analysis  
- **Open Route Service**: Route Coordinate  

## License  
This project is licensed under the MIT License. See the `LICENSE` file for details.  
