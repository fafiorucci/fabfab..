/**
 * Stato reattivo salvato sul dispositivo (localStorage): i dati dei moduli di bordo
 * restano disponibili anche offline e dopo aver chiuso l'app.
 */
export function persisted<T>(key: string, initial: T): { value: T } {
	const storeKey = `skipper:${key}`;
	let value = $state<T>(load());

	function load(): T {
		try {
			const raw = localStorage.getItem(storeKey);
			return raw ? (JSON.parse(raw) as T) : structuredClone(initial);
		} catch {
			return structuredClone(initial);
		}
	}

	$effect.root(() => {
		$effect(() => {
			const json = JSON.stringify(value);
			try {
				localStorage.setItem(storeKey, json);
			} catch {
				/* spazio esaurito o storage non disponibile */
			}
		});
	});

	return {
		get value() {
			return value;
		},
		set value(v: T) {
			value = v;
		}
	};
}

export const uid = () => Math.random().toString(36).slice(2, 10) + Date.now().toString(36);

/** Condivide un testo con il menu nativo (WhatsApp, Mail, AirDrop…) o lo copia. */
export async function shareText(title: string, text: string): Promise<'shared' | 'copied' | 'cancelled'> {
	if (navigator.share) {
		try {
			await navigator.share({ title, text });
			return 'shared';
		} catch (e) {
			if ((e as Error).name === 'AbortError') return 'cancelled';
		}
	}
	await navigator.clipboard?.writeText(text).catch(() => {});
	return 'copied';
}
