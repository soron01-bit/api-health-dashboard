import json
from datetime import datetime
from urllib.error import URLError
from urllib.request import Request, urlopen

from django.shortcuts import render


def dashboard(request):
	simulate_error = request.GET.get('simulate_error', '').strip().lower()
	simulate_targets = {
		target.strip() for target in simulate_error.split(',') if target.strip()
	}

	api_sources = [
		('posts', 'Posts API', 'https://jsonplaceholder.typicode.com/posts', 100),
		('users', 'Users API', 'https://jsonplaceholder.typicode.com/users', 10),
	]

	api_results = []
	healthy_count = 0
	simulated_count = 0
	anomaly_notes = []
	for key, name, url, expected_count in api_sources:
		result = {
			'key': key,
			'name': name,
			'url': url,
			'status': 'ERROR',
			'record_count': 0,
			'last_updated': 'N/A',
			'is_simulated': False,
		}

		should_simulate = 'all' in simulate_targets or key in simulate_targets
		if should_simulate:
			result['is_simulated'] = True
			result['last_updated'] = 'Simulated failure'
			simulated_count += 1
			api_results.append(result)
			continue

		try:
			request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
			with urlopen(request, timeout=8) as response:
				if response.status == 200:
					payload = json.loads(response.read().decode('utf-8'))
					record_count = len(payload) if isinstance(payload, list) else 1
					result['status'] = 'OK'
					result['record_count'] = record_count
					result['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
					healthy_count += 1
					if record_count != expected_count:
						anomaly_notes.append(
							f"{name} returned {record_count} records (expected {expected_count})."
						)
		except (URLError, ValueError, TimeoutError):
			pass

		api_results.append(result)

	error_count = len(api_results) - healthy_count
	alerts = []
	if error_count > 0:
		alerts.append(
			{
				'type': 'danger',
				'message': f"{error_count} API(s) currently failing. Check status table for details.",
			}
		)
	else:
		alerts.append(
			{
				'type': 'success',
				'message': 'All monitored APIs are healthy right now.',
			}
		)

	if simulated_count > 0:
		alerts.append(
			{
				'type': 'warning',
				'message': f"Simulation active for {simulated_count} API(s).",
			}
		)

	if error_count == 0 and not anomaly_notes:
		ai_insight = (
			"AI Insight: Service health is stable. No API failures or data anomalies detected."
		)
	elif error_count > 0:
		ai_insight = (
			f"AI Insight: {error_count} API(s) are failing. Prioritize endpoint connectivity and retry checks."
		)
	else:
		ai_insight = (
			"AI Insight: APIs are reachable, but data pattern changes were detected. Review record counts."
		)

	context = {
		'api_results': api_results,
		'healthy_count': healthy_count,
		'error_count': error_count,
		'alerts': alerts,
		'ai_insight': ai_insight,
		'anomaly_notes': anomaly_notes,
		'simulate_error': simulate_error,
		'last_refresh_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
	}
	return render(request, 'tracker/dashboard.html', context)
