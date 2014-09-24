from urllib import urlencode
import lxml.objectify
import urllib2


class EdostClient(object):
	def __init__(self, client_id, password):
		self.client_id = client_id
		self.password = password
		pass

	def make_request(self, **kwargs):
		data = {
			'id': self.client_id,
			'p': self.password,
		}
		data.update(kwargs)
		xml = urllib2.urlopen('http://www.edost.ru/edost_calc_kln.php', urlencode(data)).read()
		doc = lxml.objectify.fromstring(xml)
		return doc

	def get_tariffs(self, **kwargs):
		"""
		Fetch available tariffs. All keyword arguments will be sent to edost.ru.
		Advised arguments: to_city, weight, strah.
		"""
		doc = self.make_request(**kwargs)
		if hasattr(doc, 'tarif'):
			options = []
			for t in list(doc.tarif):
				options.append({
					'id': int(t.id),
					'company': unicode(t.company),
					'name': t.name and unicode(t.name) or None,
					'delivery_time': unicode(t.day),
					'price': float(t.price),
				})
			return options
		return None
