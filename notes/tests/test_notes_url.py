from django.urls import reverse, resolve


class TestUrls:
    # class contains methods to test url of notes api
    def test_detail_url(self):
        """
        method to test notes url
        :return: true or false
        """
        path = reverse('notes')
        assert resolve(path).view_name == 'notes'
