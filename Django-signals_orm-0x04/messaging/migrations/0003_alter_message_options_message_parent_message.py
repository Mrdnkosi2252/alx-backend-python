# Generated by Django 4.2.23 on 2025-07-31 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_message_edited_messagehistory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['timestamp']},
        ),
        migrations.AddField(
            model_name='message',
            name='parent_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='messaging.message'),
        ),
    ]
