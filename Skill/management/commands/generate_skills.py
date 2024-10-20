# your_app/management/commands/generate_skills.py

import random
from django.core.management.base import BaseCommand
from faker import Faker
from Skill.models import Skill

class Command(BaseCommand):
    help = 'Generate 50 skills using Faker'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # List of common skill categories
        skill_categories = [
            'Programming', 'Design', 'Writing', 'Marketing', 'Sales',
            'Management', 'Finance', 'Engineering', 'Healthcare', 'Education'
        ]

        for _ in range(50):
            category = random.choice(skill_categories)
            skill_name = f"{fake.word().capitalize()} {category}"
            skill_description = fake.sentence()

            # Create the skill if it doesn't already exist
            if not Skill.objects.filter(name=skill_name).exists():
                Skill.objects.create(name=skill_name, description=skill_description)

        self.stdout.write(self.style.SUCCESS('Successfully generated 50 skills'))
