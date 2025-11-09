import pytest
from selenium import webdriver
import configparser
import os
import random
import string
import time

# Importar Page Objects
from pages.home_page import HomePage
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.shopping_cart_page import ShoppingCartPage
from pages.checkout_page import CheckoutPage

# --- Configuración y Setup ---

@pytest.fixture(scope="session")
def config():
    """Carga la configuración desde config.ini."""
    config = configparser.ConfigParser()
    # Path relativo al archivo config.ini
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.ini')
    config.read(config_path)
    return config

@pytest.fixture(scope="session")
def user_data(config):
    """Genera un email aleatorio y combina con las credenciales."""
    # Función de utilidad para generar un email único
    def generate_random_email():
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{username}@testmail.com"

    data = config['CREDENTIALS']
    data['email'] = generate_random_email()
    return data

@pytest.fixture(scope="module")
def driver(config):
    """Inicializa el WebDriver y establece el teardown."""
    browser = config['DEFAULT']['BROWSER'].lower()
    
    if browser == 'chrome':
        # Instancia el driver de Chrome
        driver = webdriver.Chrome()
    # Puedes añadir más navegadores aquí (e.g., elif browser == 'firefox':)
    else:
        raise ValueError(f"Navegador '{browser}' no soportado.")

    driver.implicitly_wait(5) # Espera implícita general
    driver.maximize_window()
    yield driver
    # Teardown: cerrar el navegador al finalizar la suite
    driver.quit()

# --- Clase de Prueba ---

class TestE2EFlow:
    
    def test_complete_purchase_flow(self, driver, config, user_data):
        """Ejecuta el flujo completo de E2E: Registro -> Login -> Compra -> Checkout."""
        
        base_url = config['DEFAULT']['BASE_URL']
        
        # 1. ACCEDER A LA URL
        driver.get(base_url)
        print(f"\n✅ Navegando a: {base_url}")
        
        # --- TAREA 1: CREAR UNA NUEVA CUENTA DE USUARIO ---
        
        home_page = HomePage(driver)
        home_page.go_to_register_page()
        
        register_page = RegisterPage(driver)
        register_page.fill_registration_form(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            telephone=user_data['telephone'],
            password=user_data['password']
        )
        register_page.submit_registration()
        
        # VALIDACIÓN 1: Verificar creación exitosa
        assert register_page.is_account_created_successfully(), "❌ Error: La cuenta no se creó exitosamente."
        print(f"✅ Éxito: Cuenta creada para {user_data['email']}. Mensaje: '{register_page.get_success_message()}'")
        
        # Navegar de vuelta a la Home Page después del registro
        home_page.go_to_home_page()
        
        # --- TAREA 2: REALIZAR EL INICIO DE SESIÓN ---
        
        home_page.go_to_login_page()
        
        login_page = LoginPage(driver)
        login_page.login(user_data['email'], user_data['password'])
        
        # VALIDACIÓN 2: Verificar inicio de sesión exitoso (revisando el título de la página 'My Account')
        assert "My Account" in driver.title, "❌ Error: El inicio de sesión falló."
        print("✅ Éxito: Inicio de sesión realizado correctamente.")
        
        # --- TAREA 3 & 4: SELECCIONAR Y AÑADIR ARTÍCULO AL CARRITO ---
        
        # Clic en el primer producto de la home (iPhone, por ejemplo)
        home_page.select_first_product() 
        
        product_page = ProductPage(driver)
        product_page.add_to_cart()
        
        # VALIDACIÓN 3: Verificar que el artículo fue añadido
        success_alert = product_page.get_alert_success_message()
        assert "Success: You have added" in success_alert, f"❌ Error: El artículo no se añadió al carrito. Mensaje: {success_alert}"
        print(f"✅ Éxito: Artículo añadido al carrito. Mensaje: {success_alert.split('!')[0]}")
        
        # --- TAREA 5: PROCEDER AL CARRITO DE COMPRAS Y FINALIZAR LA COMPRA ---
        
        product_page.go_to_shopping_cart()
        
        shopping_cart_page = ShoppingCartPage(driver)
        shopping_cart_page.go_to_checkout()
        
        checkout_page = CheckoutPage(driver)
        # Asumimos que los detalles de la dirección se completan automáticamente por ser nuevo usuario
        
        # Finalizar compra (paso 6)
        checkout_page.confirm_order()
        
        # VALIDACIÓN 4: Verificar la finalización de la compra
        assert checkout_page.is_order_placed_successfully(), "❌ Error: La compra no se finalizó exitosamente."
        print(f"✅ Éxito: ¡Compra finalizada! Mensaje: '{checkout_page.get_order_success_message()}'")