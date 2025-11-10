from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    """Clase base que contiene métodos genéricos y el inicializador del driver."""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 50) # Espera explícita de 50 segundos

    def _find_element(self, locator):
        """Espera y encuentra un elemento."""
        try:
            return self.wait.until(EC.presence_of_element_located(locator),
                                   message=f"Elemento no encontrado con locator: {locator}")
        except TimeoutException:
            raise NoSuchElementException(f"Tiempo de espera agotado al buscar el elemento: {locator}")

    def _click(self, locator):
        """Espera a que el elemento sea clickeable y luego hace clic."""
        element = self.wait.until(EC.element_to_be_clickable(locator),
                                   message=f"Elemento no clickeable con locator: {locator}")
        element.click()

    def _type(self, locator, text):
        """Escribe texto en un campo y lo borra primero."""
        element = self._find_element(locator)
        element.clear()
        element.send_keys(text)

    def _get_text(self, locator):
        """Obtiene el texto de un elemento."""
        return self._find_element(locator).text
    
    def _is_displayed(self, locator):
        """Verifica si un elemento es visible."""
        try:
            return self._find_element(locator).is_displayed()
        except NoSuchElementException:
            return False
