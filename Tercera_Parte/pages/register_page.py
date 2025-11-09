from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegisterPage(BasePage):
    """Clase Page Object para la página de registro de cuentas."""

    # Localizadores
    INPUT_FIRST_NAME = (By.ID, 'input-firstname')
    INPUT_LAST_NAME = (By.ID, 'input-lastname')
    INPUT_EMAIL = (By.ID, 'input-email')
    INPUT_TELEPHONE = (By.ID, 'input-telephone')
    INPUT_PASSWORD = (By.ID, 'input-password')
    INPUT_CONFIRM = (By.ID, 'input-confirm')
    CHECKBOX_PRIVACY_POLICY = (By.NAME, 'agree')
    BTN_CONTINUE = (By.XPATH, '//input[@value="Continue"]')
    SUCCESS_MESSAGE = (By.XPATH, '//div[@id="content"]/h1') # Texto: "Your Account Has Been Created!"

    def fill_registration_form(self, first_name, last_name, email, telephone, password):
        """Rellena todos los campos del formulario de registro."""
        print(f"-> Registrando usuario: {email}")
        self._type(self.INPUT_FIRST_NAME, first_name)
        self._type(self.INPUT_LAST_NAME, last_name)
        self._type(self.INPUT_EMAIL, email)
        self._type(self.INPUT_TELEPHONE, telephone)
        self._type(self.INPUT_PASSWORD, password)
        self._type(self.INPUT_CONFIRM, password)
        self._click(self.CHECKBOX_PRIVACY_POLICY)

    def submit_registration(self):
        """Envía el formulario de registro."""
        self._click(self.BTN_CONTINUE)
    
    def get_success_message(self):
        """Obtiene el mensaje de éxito de creación de cuenta."""
        return self._get_text(self.SUCCESS_MESSAGE)

    def is_account_created_successfully(self):
        """Verifica si la página de éxito es visible."""
        return self._is_displayed(self.SUCCESS_MESSAGE)