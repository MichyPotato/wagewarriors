from django.db import migrations, models

def convert_skills_to_json(apps, schema_editor):
    jobSeeker = apps.get_model('account', 'jobSeeker')
    for profile in jobSeeker.objects.all():
        if profile.skills is None or profile.skills == '':
            profile.skills = '[]'
        elif isinstance(profile.skills, str):
            import json
            skills_list = [s.strip() for s in profile.skills.split(',') if s.strip()]
            profile.skills = json.dumps(skills_list)
        profile.save()

class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_jobseeker_curlat_jobseeker_curlong_recruiter_curlat_and_more'),
    ]

    operations = [
        migrations.RemoveField(model_name='jobseeker', name='curLat'),
        migrations.RemoveField(model_name='jobseeker', name='curLong'),
        migrations.RemoveField(model_name='recruiter', name='curLat'),
        migrations.RemoveField(model_name='recruiter', name='curLong'),
        migrations.RemoveField(model_name='recruiter', name='currentLocation'),
        migrations.RunPython(convert_skills_to_json, migrations.RunPython.noop),
    ]