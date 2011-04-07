# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Region.polygon'
        db.add_column('djangopeople_region', 'polygon', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True), keep_default=False)

        # Adding field 'Country.polygon'
        db.add_column('djangopeople_country', 'polygon', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True), keep_default=False)

        # Adding field 'DjangoPerson.location'
        db.add_column('djangopeople_djangoperson', 'location', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Region.polygon'
        db.delete_column('djangopeople_region', 'polygon')

        # Deleting field 'Country.polygon'
        db.delete_column('djangopeople_country', 'polygon')

        # Deleting field 'DjangoPerson.location'
        db.delete_column('djangopeople_djangoperson', 'location')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'djangopeople.country': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Country'},
            'area_in_sq_km': ('django.db.models.fields.FloatField', [], {}),
            'bbox_east': ('django.db.models.fields.FloatField', [], {}),
            'bbox_north': ('django.db.models.fields.FloatField', [], {}),
            'bbox_south': ('django.db.models.fields.FloatField', [], {}),
            'bbox_west': ('django.db.models.fields.FloatField', [], {}),
            'capital': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'fips_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_alpha3': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'iso_numeric': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'languages': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'num_people': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {})
        },
        'djangopeople.countrysite': {
            'Meta': {'object_name': 'CountrySite'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangopeople.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'djangopeople.djangoperson': {
            'Meta': {'object_name': 'DjangoPerson'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangopeople.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_active_on_irc': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'location_description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'openid_delegate': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'openid_server': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'profile_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangopeople.Region']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'djangopeople.portfoliosite': {
            'Meta': {'object_name': 'PortfolioSite'},
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangopeople.DjangoPerson']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'djangopeople.region': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Region'},
            'bbox_east': ('django.db.models.fields.FloatField', [], {}),
            'bbox_north': ('django.db.models.fields.FloatField', [], {}),
            'bbox_south': ('django.db.models.fields.FloatField', [], {}),
            'bbox_west': ('django.db.models.fields.FloatField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangopeople.Country']"}),
            'flag': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'num_people': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'})
        },
        'machinetags.machinetaggeditem': {
            'Meta': {'ordering': "('namespace', 'predicate', 'value')", 'object_name': 'MachineTaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namespace': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'predicate': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['djangopeople']
