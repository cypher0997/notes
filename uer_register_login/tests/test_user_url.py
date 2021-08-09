from django.urls import reverse, resolve


class TestUrls:
    # class contains methods to test urls fo user register and login api
    def test_login_url(self):
        """
        method to test login url
        :return: true or false
        """
        path = reverse('uer_register_login:login_method')
        assert resolve(path).view_name == 'uer_register_login:login_method'

    def test_register_url(self):
        """
        method to test register url
        :return: true or false
        """
        path = reverse('uer_register_login:register_method')
        assert resolve(path).view_name == 'uer_register_login:register_method'
