from joins.models import Join

# This middleware allows us to get the reference id from the url/request
# if it exists. This will be needed if someone comes to the site using
# the reference id of an existing Skifer user.
class ReferMiddleware():
	def process_request(self, request):
		ref_id = request.GET.get("ref", "")
		try:
			obj = Join.objects.get(ref_id = ref_id)
		except:
			obj = None

		if obj:
			request.session['brought_by_id'] = obj.id