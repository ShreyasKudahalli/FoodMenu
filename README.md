# Restaurant Menu Management System

**A Django-based web application for restaurants to create, manage, and share digital menus with customers via QR codes.**

A Django-based web application that allows restaurants to manage their digital menu and share it with customers through QR codes.

## Features

- **Restaurant Management**: Create and manage restaurant profiles
- **Food Item Management**: Add, view, and organize food items with images
- **QR Code Generation**: Automatically generate unique QR codes for each restaurant
- **Menu Categorization**: Organize items by category (Vegetarian, Non-Vegetarian, Beverage, Dessert)
- **Customer Menu View**: Customers can view the digital menu using the restaurant's QR code
- **User Authentication**: Secure login system for restaurant owners
- **Image Support**: Upload and display food item images
- **Subscription Management**: Track restaurant subscription status

## Project Structure

```
RestaurantMenu/
├── base/                          # Main app
│   ├── models.py                  # Restaurant and FoodItem models
│   ├── views.py                   # Application views
│   ├── urls.py                    # URL routing
│   ├── admin.py                   # Django admin configuration
│   └── migrations/                # Database migrations
├── RestaurantMenu/                # Project configuration
│   ├── settings.py                # Django settings
│   ├── urls.py                    # Main URL configuration
│   └── wsgi.py                    # WSGI configuration
├── templates/                     # HTML templates
│   └── Home/
│       ├── base.html              # Base template
│       ├── login.html             # Login page
│       ├── add-food.html          # Add food item form
│       ├── view-food.html         # View food items
│       ├── customer-menu.html     # Customer menu view
│       └── my-qr.html             # QR code display
├── static/                        # Static files (CSS, JavaScript)
├── media/                         # User-uploaded files
│   ├── food_images/               # Food item images
│   └── qr_codes/                  # Generated QR codes
├── manage.py                      # Django management utility
└── requirements.txt               # Project dependencies
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository and navigate to the project directory**
   ```bash
   cd RestaurantMenu
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### For Restaurant Owners

1. **Login**: Access the login page at `/login/`
2. **Add Food Items**: Navigate to `/add-food/` to add new menu items
3. **View Menu**: Go to `/view-food/` to see all your menu items
4. **Get QR Code**: Visit `/my-qr/` to view and download your restaurant's QR code

### For Customers

1. **Scan QR Code**: Use a QR code scanner to scan your restaurant's QR code
2. **View Menu**: The QR code will direct you to your restaurant's digital menu
3. **Browse Items**: View all available food items with prices, descriptions, and images

## Database Models

### Restaurant Model
- `user`: OneToOne relationship with Django User model
- `restaurant_name`: Name of the restaurant
- `slug`: URL-friendly identifier (auto-generated)
- `is_active`: Active/inactive status
- `subscription_end`: Subscription expiration date
- `qr_code`: Auto-generated QR code image

### FoodItem Model
- `restaurant`: Foreign key to Restaurant
- `name`: Food item name
- `price`: Item price
- `quantity`: Available quantity
- `description`: Item description
- `category`: Category (Vegetarian, Non-Vegetarian, Beverage, Dessert)
- `food_image`: Item image

## URL Routes

| Route | View | Description |
|-------|------|-------------|
| `/login/` | `login_user()` | Restaurant owner login |
| `/add-food/` | `add_food()` | Add new food item |
| `/view-food/` | `view_food()` | View restaurant's food items |
| `/menu/<slug>/` | `customer_menu()` | Customer view of restaurant menu |
| `/my-qr/` | `my_qr()` | View restaurant's QR code |

## Configuration

### Settings
- Database: SQLite (default) - Change in `RestaurantMenu/settings.py` for production
- Media files: Stored in `media/` directory
- Static files: Stored in `static/` directory and `staticfiles/`

### QR Code Generation
QR codes are automatically generated when a restaurant is created or updated. The QR code URL points to the customer menu view:
```
http://127.0.0.1:8000/menu/{restaurant_slug}/
```

## Deployment

For deployment instructions, see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

## Technologies Used

- **Backend**: Django 3.x/4.x
- **Database**: SQLite (Development), PostgreSQL (Production recommended)
- **Frontend**: HTML, CSS, JavaScript
- **QR Code**: qrcode library
- **Authentication**: Django built-in authentication

## Security Considerations

- Use environment variables for sensitive settings in production
- Enable HTTPS for all deployed sites
- Set `DEBUG = False` in production
- Use a production-grade database (PostgreSQL)
- Configure CORS and CSRF settings appropriately
- Keep dependencies updated

## Future Enhancements

- [ ] Order management system
- [ ] Payment integration
- [ ] Admin dashboard analytics
- [ ] Menu templates
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Inventory tracking
- [ ] Customer reviews and ratings

## Contact & Support

For issues, feature requests, or questions, please open an issue in the project repository.

## License

This project is open source and available under the MIT License.
