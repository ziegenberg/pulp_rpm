# Generated by Django 3.2.15 on 2022-08-12 16:28

from django.core.files.storage import default_storage
from django.db import migrations, models, transaction


def convert_artifact_to_snippets(apps, schema_editor):
    """Create snippet from artifact and remove artifact."""
    with transaction.atomic():
        Modulemd = apps.get_model("rpm", "Modulemd")
        ModulemdDefaults = apps.get_model("rpm", "ModulemdDefaults")
        ContentArtifact = apps.get_model("core", "ContentArtifact")
        modules_with_snippet = []
        defaults_with_snippet = []

        for module in Modulemd.objects.all():
            artifact = module._artifacts.get()
            if default_storage.exists(artifact.file.name):
                module.snippet = artifact.file.read().decode("utf-8")
            content_artifact = ContentArtifact.objects.filter(content__pk=module.pk)
            content_artifact.delete()
            modules_with_snippet.append(module)

        for default in ModulemdDefaults.objects.all():
            artifact = default._artifacts.get()
            if default_storage.exists(artifact.file.name):
                default.snippet = artifact.file.read().decode("utf-8")
            content_artifact = ContentArtifact.objects.filter(content__pk=default.pk)
            content_artifact.delete()
            defaults_with_snippet.append(default)

        Modulemd.objects.bulk_update(modules_with_snippet, ["snippet"])
        ModulemdDefaults.objects.bulk_update(defaults_with_snippet, ["snippet"])


class Migration(migrations.Migration):

    dependencies = [
        ("rpm", "0043_textfield_conversion"),
    ]

    operations = [
        migrations.AddField(
            model_name="modulemd",
            name="snippet",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="modulemddefaults",
            name="snippet",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.RunPython(convert_artifact_to_snippets),
    ]
