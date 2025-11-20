from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reparacion',
            name='mecanico_asignado',
            field=models.ForeignKey(
                blank=True, 
                null=True, 
                on_delete=django.db.models.deletion.SET_NULL,
                to='gestion.empleado',
                verbose_name='Mecánico Asignado',
                related_name='reparaciones_asignadas'
            ),
        ),
    ]
