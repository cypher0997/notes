from django.urls import reverse, resolve


class TestUrls:
    # class contains methods to test url of notes api
    def test_notes_url(self):
        """
        method to test notes url
        :return: true or false
        """
        path = reverse('notes')
        assert resolve(path).view_name == 'notes'

    def test_label_url(self):
        """
        method to test notes url
        :return: true or false
        """
        path = reverse('label')
        assert resolve(path).view_name == 'label'

    def test_collaborator_url(self):
        """
        method to test notes url
        :return: true or false
        """
        path = reverse('collaborator')
        assert resolve(path).view_name == 'collaborator'
