import pytest

import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone

from polls.models import Poll


def create_poll(question, days):
    """
    Creates a poll with the given `question` published the given number of
    `days` offset to now (negative for polls published in the past,
    positive for polls that have yet to be published).
    """
    return Poll.objects.create(
        question=question,
        pub_date=timezone.now() + datetime.timedelta(days=days)
    )


@pytest.mark.django_db
class TestPollIndexView(object):
    def test_index_view_with_no_polls(self, client):
        """
        If no polls exist, an appropriate message should be displayed.
        """
        response = client.get(reverse('polls:index'))

        assert response.status_code == 200
        assert "No polls are available" in str(response)
        assert len(response.context['latest_poll_list']) == 0

    def test_index_view_with_a_past_poll(self, client):
        """
        Polls with a pub_date in the past should be displayed on the index page.
        """
        create_poll(question="Past poll.", days=-30)
        response = client.get(reverse('polls:index'))

        assert 'Past poll.' == response.context['latest_poll_list'][0].question

    def test_index_view_with_a_future_poll(self, client):
        """
        Polls with a pub_date in the future should not be displayed on the
        index page.
        """
        create_poll(question="Future poll.", days=30)
        response = client.get(reverse('polls:index'))

        assert response.status_code == 200
        assert "No polls are available" in str(response)

        assert len(response.context['latest_poll_list']) == 0

    def test_index_view_with_future_poll_and_past_poll(self, client):
        """
        Even if both past and future polls exist, only past polls should be
        displayed.
        """
        create_poll(question="Past poll.", days=-30)
        create_poll(question="Future poll.", days=30)
        response = client.get(reverse('polls:index'))

        assert 'Past poll.' == response.context['latest_poll_list'][0].question

    def test_index_view_with_two_past_polls(self, client):
        """
        The polls index page may display multiple polls.
        """
        create_poll(question="Past poll 1.", days=-30)
        create_poll(question="Past poll 2.", days=-5)
        response = client.get(reverse('polls:index'))

        assert 'Past poll 2.' == response.context['latest_poll_list'][0].question
        assert 'Past poll 1.' == response.context['latest_poll_list'][1].question


@pytest.mark.django_db
class TestPollIndexDetailView(object):
    def test_detail_view_with_a_future_poll(self, client):
        """
        The detail view of a poll with a pub_date in the future should
        return a 404 not found.
        """
        future_poll = create_poll(question='Future poll.', days=5)
        response = client.get(reverse('polls:detail', args=(future_poll.id,)))

        assert response.status_code == 404

    def test_detail_view_with_a_past_poll(self, client):
        """
        The detail view of a poll with a pub_date in the past should display
        the poll's question.
        """
        past_poll = create_poll(question='Past poll.', days=-5)
        response = client.get(reverse('polls:detail', args=(past_poll.id,)))

        assert response.status_code == 200
        assert 'Past poll.' == response.context['poll'].question
