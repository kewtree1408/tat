# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.utils import translation

from core.mostrans import fetch


class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        translation.activate('ru')

        numbers = args or None

        fetch(only_numbers=numbers)

        translation.deactivate()
