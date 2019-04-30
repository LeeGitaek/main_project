
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileListBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.TextField(max_length=255)),
                ('class_name', models.CharField(max_length=20)),
                ('uploaded_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('team_title', models.CharField(max_length=20)),
                ('user_name', models.CharField(max_length=10)),
                ('weights_num', models.FloatField(blank=True, default=1200.0, null=True)),
                ('assignment_title', models.CharField(blank=True, max_length=20)),
                ('deadline_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('file_size', models.FloatField(blank=True, default=0, null=True)),
                ('document', models.FileField(max_length=1500, upload_to='documents/')),
                ('t_num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='InviteBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=10)),
                ('receiver', models.CharField(max_length=10)),
                ('class_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_filename', models.TextField(max_length=255)),
                ('uploaded_account', models.CharField(max_length=10)),
                ('uploaded_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('uploaded_teamtitle', models.CharField(max_length=20)),
                ('edited_orwhat', models.BooleanField(default=False)),
                ('read_ox', models.BooleanField(default=False)),
                ('uploaded_groupid', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_file', models.CharField(max_length=255)),
                ('review_uploader', models.CharField(max_length=10)),
                ('review_subject', models.CharField(max_length=20)),
                ('review_team', models.IntegerField(default=0)),
                ('review_er', models.CharField(max_length=20)),
                ('review_score', models.FloatField(default=0.0)),
                ('review_comments', models.CharField(blank=True, default='의견 없음', max_length=255)),
                ('review_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('subject_name', models.CharField(max_length=100)),
                ('userid', models.CharField(default='DEFAULT VALUE', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TaskBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_user', models.CharField(max_length=20)),
                ('task_role', models.CharField(max_length=10)),
                ('task_status', models.CharField(max_length=10)),
                ('task_percent', models.IntegerField(default=0)),
                ('task_dead', models.CharField(max_length=20)),
                ('task_subject', models.CharField(max_length=20)),
                ('task_team', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('team_name', models.CharField(max_length=100)),
                ('project_name', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('doc_link', models.CharField(max_length=100, null=True)),
                ('subject_num', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Team')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='team_num',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Team'),
        ),
    ]
