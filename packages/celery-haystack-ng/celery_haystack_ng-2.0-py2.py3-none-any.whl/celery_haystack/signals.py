from django.db import transaction
from django.db.models import signals

from haystack.signals import RealtimeSignalProcessor
from haystack.exceptions import NotHandled
from haystack.utils import get_identifier

from .conf import settings
from .utils import get_update_task
from .indexes import CelerySearchIndex


class CelerySignalProcessor(RealtimeSignalProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue = []
        self._on_commit_registered = False

    def handle_save(self, sender, instance, **kwargs):
        return self.enqueue('update', instance, sender, **kwargs)

    def handle_delete(self, sender, instance, **kwargs):
        return self.enqueue('delete', instance, sender, **kwargs)

    def run_task(self):
        options = {}
        if settings.CELERY_HAYSTACK_QUEUE:
            options['queue'] = settings.CELERY_HAYSTACK_QUEUE
        if settings.CELERY_HAYSTACK_COUNTDOWN:
            options['countdown'] = settings.CELERY_HAYSTACK_COUNTDOWN

        if self._queue:
            task = get_update_task()
            task.apply_async((self._queue,), {}, **options)

            self._queue = []


    def enqueue(self, action, instance, sender, **kwargs):
        """
        Given an individual model instance, determine if a backend
        handles the model, check if the index is Celery-enabled and
        enqueue task.
        """
        using_backends = self.connection_router.for_write(instance=instance)

        for using in using_backends:
            try:
                connection = self.connections[using]
                index = connection.get_unified_index().get_index(sender)
            except NotHandled:
                continue  # Check next backend

            if isinstance(index, CelerySearchIndex):
                if action == 'update' and not index.should_update(instance):
                    continue
                self._queue.append((action, get_identifier(instance)))

                if not self._on_commit_registered:
                    transaction.on_commit(self.run_task)
