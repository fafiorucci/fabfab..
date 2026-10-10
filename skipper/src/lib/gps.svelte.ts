/** Posizione GPS del dispositivo, aggiornata in continuo finché il componente è attivo. */
export function useGps() {
	let pos = $state<{ lat: number; lon: number; acc: number; sog: number | null; cog: number | null; time: number } | null>(null);
	let error = $state<string | null>(null);
	let watch: number | null = null;

	function start() {
		if (!('geolocation' in navigator)) {
			error = 'GPS non disponibile su questo dispositivo.';
			return;
		}
		error = null;
		watch = navigator.geolocation.watchPosition(
			(p) => {
				pos = {
					lat: p.coords.latitude,
					lon: p.coords.longitude,
					acc: p.coords.accuracy,
					// m/s → nodi
					sog: p.coords.speed != null ? p.coords.speed * 1.943844 : null,
					cog: p.coords.heading,
					time: p.timestamp
				};
			},
			(e) => (error = e.code === e.PERMISSION_DENIED ? 'Permesso di posizione negato: abilitalo nelle impostazioni del browser.' : 'Posizione non disponibile.'),
			{ enableHighAccuracy: true, maximumAge: 5000, timeout: 20000 }
		);
	}

	function stop() {
		if (watch != null) navigator.geolocation.clearWatch(watch);
		watch = null;
	}

	return {
		get pos() {
			return pos;
		},
		get error() {
			return error;
		},
		start,
		stop
	};
}
